# M14.9 Windows reference matrix

Run the owned probe with 64-bit Windows Python on each pinned Windows guest
and save its JSON output. Record edition, build, patch level, guest image
provenance and process architecture alongside each capture. Run separately in
a 32-bit process on a 64-bit guest for the WOW64 cases as those probes land.
Use fresh owned disk state. No original installer is required for this probe.

~~~powershell
python tests/m14/reference149/windows_probe.py
~~~

| Target | Capture |
| --- | --- |
| Windows 7 SP1 x64 | Pending |
| Windows 8 x64 | Pending |
| Windows 8.1 x64 | Pending |
| Windows 10 x64 | Pending |
| Windows 11 x64 | [Development host sample](windows-host.json). Exact edition and guest provenance are pending. The Python platform-version tuple and reported OS build differ and are preserved separately. |
| Engacer | Native comparison pending M14.10. |

The initial host sample records loader results 126 and 193 and alternate-case
lookup on its temporary directory. Preserve filesystem profile with future
captures because case handling can differ by directory. The probe records API
observations, while the matrix distinguishes absent, observed and compared.

| Gap | Comparison needed | Owner |
| --- | --- | --- |
| Loader, paths and registry views | Delay-load and activation outcomes, path aliases, handle lifetime, HKCR merge and WOW64 per-key behavior | M14.10 |
| .NET, COM and service attribution | Late required activation versus optional probes, broker ownership and restart | M14.11 |
| Installer lifecycle | Nested owner binding and interrupted commit readback | M14.12 |
| Device calls | Request privileges, teardown and actual device effects | M14.13 |
| Desktop assistance | Distinct missing, corrupt, incompatible and denied cases, plus the three entry routes | M14.14 |
