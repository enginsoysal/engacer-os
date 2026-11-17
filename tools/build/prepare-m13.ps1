# Prepare large M13 scratch output outside OneDrive; never replace existing data.
$ErrorActionPreference='Stop'
$projectRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$buildLink=Join-Path $projectRoot 'build/m13-native'
$externalRoot=[IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'EngacerOS/Build/m13'))
if ($externalRoot.StartsWith($projectRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'M13 scratch must be outside the source checkout.' }
if (Test-Path -LiteralPath $buildLink) {
 $existing=Get-Item -LiteralPath $buildLink -Force
 if ($existing.LinkType -ne 'Junction' -or [IO.Path]::GetFullPath($existing.Target) -ne $externalRoot) { throw 'Existing M13 output is not the expected owned junction; no files were changed.' }
 Write-Output 'M13 external workspace is already ready.'
 exit 0
}
New-Item -ItemType Directory -Path $externalRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $projectRoot 'build') -Force | Out-Null
New-Item -ItemType Junction -Path $buildLink -Target $externalRoot | Out-Null
Write-Output 'M13 external workspace is ready. Historical M12 and M13.0 output was preserved.'
