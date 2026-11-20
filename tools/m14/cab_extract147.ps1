$ErrorActionPreference = 'Stop'
$projectRoot147 = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$scratch147 = Join-Path $projectRoot147 'build/m14-native/stage7/cab-inputs'
New-Item -ItemType Directory -Force -Path $scratch147 | Out-Null
$installer147 = New-Object -ComObject WindowsInstaller.Installer
$inputs147 = @(
    (Join-Path $projectRoot147 'third_party/7zip/7z2606-x64.msi'),
    (Join-Path $env:LOCALAPPDATA 'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi')
)
$records147 = @()
foreach ($package147 in $inputs147) {
    # Read-only database and stream access. Never create an installation session
    # or invoke an original installer/application on the development host.
    $database147 = $installer147.OpenDatabase($package147, 0)
    $view147 = $database147.OpenView('SELECT `Name`, `Data` FROM `_Streams` WHERE `Name` = ''product.cab''')
    $view147.Execute()
    $row147 = $view147.Fetch()
    if ($null -eq $row147) { throw 'The selected original CAB stream is missing.' }
    $size147 = $row147.DataSize(2)
    if ($size147 -lt 44 -or $size147 -gt 8388608) { throw 'CAB stream exceeds the reviewed input quota.' }
    $text147 = $row147.ReadStream(2, $size147, 1)
    $bytes147 = [Text.Encoding]::GetEncoding(28591).GetBytes($text147)
    if ($bytes147.Length -ne $size147) { throw 'CAB stream read was incomplete.' }
    $name147 = [IO.Path]::GetFileNameWithoutExtension($package147) + '.cab'
    [IO.File]::WriteAllBytes((Join-Path $scratch147 $name147), $bytes147)
    $records147 += @{
        package = [IO.Path]::GetFileName($package147)
        package_sha256 = (Get-FileHash -LiteralPath $package147 -Algorithm SHA256).Hash.ToLowerInvariant()
        cabinet = $name147
        cabinet_sha256 = (Get-FileHash -LiteralPath (Join-Path $scratch147 $name147) -Algorithm SHA256).Hash.ToLowerInvariant()
        cabinet_bytes = $size147
    }
    $view147.Close()
}
@{scope='Read-only original MSI CAB streams; no installer/application execution';inputs=$records147} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $scratch147 'inputs.json') -Encoding utf8
Write-Output 'Read-only original cabinet extraction completed in owned stage7 scratch.'
