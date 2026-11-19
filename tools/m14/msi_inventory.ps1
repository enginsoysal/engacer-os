$ErrorActionPreference = 'Stop'
$projectRoot14 = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$scratch14 = Join-Path $env:LOCALAPPDATA 'EngacerOS/Research/M14/0'
$installer14 = New-Object -ComObject WindowsInstaller.Installer
$records14 = @()
foreach ($package14 in @((Join-Path $projectRoot14 'third_party/7zip/7z2606-x64.msi'), (Join-Path $scratch14 'npp.8.9.9.1.Installer.x64.msi'))) {
    # Mode 0 is read-only. Never call InstallProduct or open an installation session.
    $database14 = $installer14.OpenDatabase($package14, 0)
    $catalogView14 = $database14.OpenView('SELECT `Name` FROM `_Tables`')
    $catalogView14.Execute()
    $catalog14 = @()
    while ($null -ne ($catalogRow14 = $catalogView14.Fetch())) { $catalog14 += $catalogRow14.StringData(1) }
    $catalogView14.Close()
    $tables14 = @{}
    foreach ($table14 in @('Property', 'File', 'Component', 'Directory', 'CustomAction', 'InstallExecuteSequence', 'Binary')) {
        if ($table14 -notin $catalog14) { $tables14[$table14] = @{ absent = $true }; continue }
        try {
            $view14 = $database14.OpenView('SELECT * FROM `' + $table14 + '`')
            $view14.Execute()
            $rows14 = @()
            while ($null -ne ($row14 = $view14.Fetch())) {
                $values14 = @()
                $fieldCount14 = $row14.GetType().InvokeMember('FieldCount', [System.Reflection.BindingFlags]::GetProperty, $null, $row14, $null)
                if ($fieldCount14 -lt 1) { throw 'MSI metadata row has no fields' }
                for ($column14 = 1; $column14 -le $fieldCount14; $column14++) {
                    if ($table14 -eq 'Binary' -and $column14 -eq 2) {
                        $streamName14 = $row14.StringData(1)
                        if ($streamName14 -notmatch '^[A-Za-z0-9_.-]+$') { throw 'Unsafe MSI stream identifier' }
                        $streamSize14 = $row14.DataSize(2)
                        if ($streamSize14 -gt 16777216) { throw 'MSI stream exceeds research bound' }
                        $streamText14 = $row14.ReadStream(2, $streamSize14, 1)
                        $streamBytes14 = [Text.Encoding]::GetEncoding(28591).GetBytes($streamText14)
                        if ($streamBytes14.Length -ne $streamSize14) { throw 'MSI stream read was incomplete' }
                        $streamFolder14 = Join-Path $scratch14 ('msi-streams/' + [IO.Path]::GetFileNameWithoutExtension($package14))
                        [IO.Directory]::CreateDirectory($streamFolder14) | Out-Null
                        $streamFile14 = Join-Path $streamFolder14 ($streamName14 + '.bin')
                        [IO.File]::WriteAllBytes($streamFile14, $streamBytes14)
                        $values14 += @{ bytes = $streamSize14; sha256 = (Get-FileHash -LiteralPath $streamFile14 -Algorithm SHA256).Hash.ToLowerInvariant(); relative_path = 'msi-streams/' + [IO.Path]::GetFileNameWithoutExtension($package14) + '/' + $streamName14 + '.bin' }
                    }
                    else { $values14 += $row14.StringData($column14) }
                }
                $rows14 += ,$values14
            }
            $view14.Close()
            $tables14[$table14] = $rows14
        } catch {
            # A table can be absent; errors are retained rather than silently a pass.
            $tables14[$table14] = @{ query_failed = $true; hresult = $_.Exception.HResult }
        }
    }
    $records14 += @{ file = [IO.Path]::GetFileName($package14); sha256 = (Get-FileHash -LiteralPath $package14 -Algorithm SHA256).Hash.ToLowerInvariant(); template = $database14.SummaryInformation(0).Property(7); tables = $tables14 }
}
$output14 = Join-Path $projectRoot14 'evidence/M14/0/msi-inventory.json'
@{ scope = 'Read-only original Windows Installer database queries; no installer/application execution or guest compatibility proof'; packages = $records14 } | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $output14 -Encoding utf8
Write-Output 'Read-only MSI metadata collected; inspect query failures explicitly.'
