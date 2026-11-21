$ErrorActionPreference = 'Stop'
$projectRoot147 = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$output147 = Join-Path $projectRoot147 'evidence/M14/7/development/msi-tables147.json'
New-Item -ItemType Directory -Force -Path (Split-Path $output147) | Out-Null
$installer147 = New-Object -ComObject WindowsInstaller.Installer
$packages147 = @(
    (Join-Path $projectRoot147 'third_party/7zip/7z2606-x64.msi'),
    (Join-Path $env:LOCALAPPDATA 'EngacerOS/Research/M14/0/npp.8.9.9.1.Installer.x64.msi')
)
$records147 = @()
foreach ($package147 in $packages147) {
    # Metadata queries only. Never open an installation session or execute a
    # package, embedded DLL, custom action or application on the host.
    $database147 = $installer147.OpenDatabase($package147, 0)
    $catalog147 = $database147.OpenView('SELECT `Name` FROM `_Tables`')
    $catalog147.Execute()
    $names147 = @()
    while ($null -ne ($row147 = $catalog147.Fetch())) { $names147 += $row147.StringData(1) }
    $catalog147.Close()
    $tables147 = @{}
    foreach ($table147 in @('Property','File','Component','Directory','Feature','FeatureComponents','Condition','Media','InstallExecuteSequence','CustomAction','LaunchCondition','Registry','Shortcut','RemoveFile','CreateFolder','Upgrade','AppSearch','RegLocator')) {
        if ($table147 -notin $names147) { $tables147[$table147] = @{absent=$true}; continue }
        $view147 = $database147.OpenView('SELECT * FROM `' + $table147 + '`')
        $view147.Execute()
        $rows147 = @()
        while ($null -ne ($row147 = $view147.Fetch())) {
            $count147 = $row147.GetType().InvokeMember('FieldCount', [System.Reflection.BindingFlags]::GetProperty, $null, $row147, $null)
            if ($count147 -lt 1 -or $count147 -gt 32) { throw 'MSI metadata column count is unsupported.' }
            $values147 = @()
            for ($column147=1; $column147 -le $count147; $column147++) { $values147 += $row147.StringData($column147) }
            $rows147 += ,$values147
        }
        $view147.Close()
        $tables147[$table147] = $rows147
    }
    $records147 += @{
        file=[IO.Path]::GetFileName($package147)
        sha256=(Get-FileHash -LiteralPath $package147 -Algorithm SHA256).Hash.ToLowerInvariant()
        tables=$tables147
    }
}
@{scope='Read-only original MSI metadata; no installer/application/custom-action execution';packages=$records147} | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $output147 -Encoding utf8
Write-Output 'Complete selected MSI metadata collected read-only.'
