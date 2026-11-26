# Windows behavior reference for M14.9

Use published behavior as the specification. Use a guest observation when a
required result or version distinction remains unknown. Record the question,
fixture, OS build, process architecture and actual outcome for each experiment.

| ID | Published contract | Engacer requirement and verification |
| --- | --- | --- |
| DLL-01 | Search order depends on flags and process configuration. The unpackaged process package dependency graph enters the documented default order from Windows 11 21H2. [DLL search](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order) | M14.10 tests ordered lookup with duplicate names inside one bundle. Resolve other bundles as outside the app scope. Compare the older and newer profiles where package graph behavior is required. |
| DLL-02 | Win32 error 126 identifies a module that could not be found. Error 193 identifies an invalid executable format. [Win32 errors](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-) | The Windows host probe observed both separately with controlled absolute paths. M14.10 verifies distinct failures. M14.14 uses request context before proposing software, because a loader error alone cannot establish intent. |
| PATH-01 | WOW64 normally redirects x86 System32 access on x64 Windows. Microsoft documents exempt paths and the Sysnative alias. [File redirector](https://learn.microsoft.com/en-us/windows/win32/winprog64/file-system-redirector) | M14.10 tests native and x86 views with owned markers, the documented exemptions and Sysnative lookup. Resolve the architecture view inside the app namespace. |
| REG-01 | WOW64 behavior is defined per key family. Some keys have distinct views and others have one view. Registry reflection was removed starting with Windows 7. [WOW64 key families](https://learn.microsoft.com/en-us/windows/win32/winprog64/shared-registry-keys) | M14.10 tests redirected and common keys for the two architecture views of the same app. App A and B always own independent data. |
| REG-02 | HKCR combines user and machine class registrations under documented merge rules. [HKCR merged view](https://learn.microsoft.com/en-us/windows/win32/sysinfo/merged-view-of-hkey-classes-root) | M14.10 tests duplicate class registrations and enumeration. M14.11 tests activation. Both backing stores are scoped to the requesting app. |
| CLR-01 | The CLR identifier and .NET Framework target can differ. CLR v4.0 alone does not identify the requested Framework 4.x release. [Runtime configuration](https://learn.microsoft.com/en-us/dotnet/framework/configure-apps/file-schema/startup/supportedruntime-element) | M14.11 records family, architecture, configuration and activation outcome. M14.14 distinguishes a confirmed required component from an optional probe or unsupported platform call. |

## Targeted experiments

- If DLL lookup with competing errors affects an original workload, put a
  missing dependency and an invalid image in separate controlled cases first,
  then combine them and record the first returned error. Run Windows 7 SP1
  and the affected later release if the workload depends on a version difference.
- For registry merge or redirection discrepancies, record the precise key family,
  explicit 32/64 view flags, account context and enumeration results.
- For late CLR or COM activation, record the actual runtime configuration and
  activation request after startup. Test a feature that needs the dependency
  and an optional lookup separately.
- Run each matching Engacer scenario when the owning milestone provides the
  behavior. The app ownership and physical-copy rules are Engacer requirements
  and have native A/B tests rather than a Windows oracle.

The Windows 7 Ultimate SP1 x64 English image was checked against the expected
SHA-1 36AE90DEFBAD9D9539E649B193AE573B77A71C83. Its measured SHA-256 is
36F4FA2416D0982697AB106E3A72D2E120DBCDB6CC54FD3906D06120D0653808.
The dedicated VMware guest started with an empty disk. This records media and
guest preparation rather than an installed guest measurement.

[Host evidence and probe procedure](../../evidence/M14/9/README.md)
