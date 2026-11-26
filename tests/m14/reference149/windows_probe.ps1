# Run with Windows PowerShell 2.0 or later. All fixtures are temporary.
$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class EngacerReference149 {
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
    public static extern IntPtr LoadLibraryEx(string path, IntPtr file, uint flags);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool FreeLibrary(IntPtr module);
}
"@
$root = Join-Path ([IO.Path]::GetTempPath()) ('engacer-reference-' + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($root) | Out-Null
try {
    [IO.File]::WriteAllText((Join-Path $root 'invalid.dll'), 'Engacer-owned invalid image')
    $errors = @()
    foreach ($leaf in @('absent.dll', 'invalid.dll')) {
        $path = Join-Path $root $leaf
        $module = [EngacerReference149]::LoadLibraryEx($path, [IntPtr]::Zero, 0)
        $errorCode = [Runtime.InteropServices.Marshal]::GetLastWin32Error()
        if ($module -ne [IntPtr]::Zero) {
            [EngacerReference149]::FreeLibrary($module) | Out-Null
            throw "Unexpected load of fixture $leaf"
        }
        $errors += $errorCode
    }
    [IO.File]::WriteAllText((Join-Path $root 'MiXeD.txt'), 'reference')
    $caseRead = [IO.File]::Exists((Join-Path $root 'mixed.txt')).ToString().ToLowerInvariant()
    $system = Get-WmiObject -Class Win32_OperatingSystem
    $bits = [IntPtr]::Size * 8
    $osVersion = [Version]$system.Version
    $systemTuple = "$($osVersion.Major),$($osVersion.Minor),$($osVersion.Build)"
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $digest = [BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($MyInvocation.MyCommand.Path))).Replace('-', '').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
    @"
{
  "system": [$systemTuple],
  "operating_system_sku": $($system.OperatingSystemSKU),
  "service_pack_major": $($system.ServicePackMajorVersion),
  "process_bits": $bits,
  "probe_sha256": "$digest",
  "cases": {
    "absent_image": {"loaded": false, "last_error": $($errors[0])},
    "invalid_image": {"loaded": false, "last_error": $($errors[1])},
    "case_lookup": {"alternate_case_read": $caseRead}
  }
}
"@
} finally {
    [IO.File]::Delete((Join-Path $root 'invalid.dll'))
    [IO.File]::Delete((Join-Path $root 'MiXeD.txt'))
    [IO.Directory]::Delete($root)
}
