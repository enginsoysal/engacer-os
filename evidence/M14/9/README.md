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


## Repeatable review

Run `uv run --no-project --with jsonschema==4.25.1 python tests/m14/reference149/check_lab.py`
from the repository root. The check validates the schema, exercises accepted
and rejected records, verifies the committed reference probe hash and tests
comparison reporting with owned fixture data. Pass `--candidate <capture.json>`
to compare another capture against the shipped host observation. Differences
and missing observations are reported separately. Use matched OS, architecture
and filesystem profiles when interpreting measurements.

The discovered Windows 7 VM directory had VMware lock entries. Its running state,
guest access and reference provenance were unverified. No reference guests for
Windows 8, 8.1 or 10 were identified in the inspected VM locations. A pinned
Windows 11 guest capture also remains open. The host sample is the only measured
platform in the current report.
