param(
 [Parameter(Mandatory=$true)][string]$Original,
 [Parameter(Mandatory=$true)][string]$Work
)
$ErrorActionPreference='Stop'
$Original=(Resolve-Path -LiteralPath $Original).Path
$Work=(New-Item -ItemType Directory -Force -Path $Work).FullName
$zip=Join-Path $env:ProgramFiles '7-Zip/7z.exe'
$payloads=(New-Item -ItemType Directory -Force -Path (Join-Path $Work 'payloads')).FullName
$installer=New-Object -ComObject WindowsInstaller.Installer
$database=$installer.OpenDatabase($Original,0)
$media=$database.OpenView('SELECT * FROM Media')
$media.Execute()
$cabinet=$media.Fetch().StringData(4).TrimStart('#')
$media.Close()
if($cabinet -cne 'product.cab'){throw 'Unexpected original fixture cabinet'}
& $zip x -tCompound -y "-o$Work" $Original $cabinet | Out-Null
if($LASTEXITCODE){throw 'Could not extract original cabinet'}
& expand.exe -F:* (Join-Path $Work $cabinet) $payloads | Out-Null
if($LASTEXITCODE){throw 'Could not extract cabinet members'}
$files=$database.OpenView('SELECT * FROM File ORDER BY Sequence')
$files.Execute()
$consoleId=$null
$copyRows=while($null -ne ($record=$files.Fetch())){
 $leaf=$record.StringData(1)
 if($leaf -cnotmatch '^[a-zA-Z0-9_.-]+$'){throw "Non-leaf cabinet member $leaf"}
 if(($record.StringData(3).Split('|')[-1]) -ceq '7z.exe'){$consoleId=$leaf}
 $member=Get-Item -LiteralPath (Join-Path $payloads $leaf)
 if($member.Length -ne $record.IntegerData(4)){throw "Original member size mismatch $leaf"}
 '"'+$member.FullName+'" "'+$leaf+'"'
}
$files.Close()

if(!$consoleId){throw 'Original console executable is missing'}
$changed=Join-Path $payloads $consoleId
$marker=[Text.Encoding]::ASCII.GetBytes("Engacer OS native update fixture 26.07.00.0"+[char]10)
$append=[IO.File]::Open($changed,[IO.FileMode]::Append,[IO.FileAccess]::Write)
try{$append.Write($marker,0,$marker.Length)}finally{$append.Dispose()}

$directive=Join-Path $Work 'cabinet.ddf'
@(
 '.OPTION EXPLICIT'
 '.Set Cabinet=on'
 '.Set Compress=on'
 '.Set CompressionType=LZX'
 '.Set CompressionMemory=21'
 '.Set MaxDiskSize=0'
 '.Set FolderSizeThreshold=0'
 '.Set CabinetNameTemplate=fixture.cab'
 ('.Set DiskDirectory1="'+$Work+'"')
 $copyRows
) | Set-Content -LiteralPath $directive -Encoding ascii
Push-Location -LiteralPath $Work
try{
 & makecab.exe /F $directive | Out-Null
 if($LASTEXITCODE){throw 'Could not build the replacement cabinet'}
}finally{Pop-Location}

$output=Join-Path $Work 'EngacerOS-7zip-update-fixture.msi'
Copy-Item -LiteralPath $Original -Destination $output -Force
$database=$installer.OpenDatabase($output,1)
foreach($sql in @(
 'UPDATE Property SET Value=''26.07.00.0'' WHERE Property=''ProductVersion'''
 ('UPDATE File SET FileSize='+ (Get-Item -LiteralPath $changed).Length +" WHERE File='$consoleId'")
)){
 $view=$database.OpenView($sql)
 $view.Execute()
 $view.Close()
}
$view=$database.OpenView("SELECT Name,Data FROM _Streams WHERE Name='product.cab'")
$view.Execute()
$record=$view.Fetch()
if($null -eq $record){throw 'Missing product.cab stream'}
$record.SetStream(2,(Join-Path $Work 'fixture.cab'))
$view.Modify(2,$record)
$view.Close()
$database.Commit()
foreach($object in @($record,$view,$database)){
 [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($object)
}
[pscustomobject]@{package=$output;image_sha256=(Get-FileHash -LiteralPath $changed -Algorithm SHA256).Hash.ToLowerInvariant()} | ConvertTo-Json -Compress
