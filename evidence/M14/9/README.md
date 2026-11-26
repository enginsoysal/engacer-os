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
| Windows 7 SP1 x64 | ISO hash checked and disposable VM started with a blank disk. Installed guest capture pending. |
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

## Guest preparation

Use a disposable guest with its own virtual disk. Record the publisher URL,
edition, language, ISO SHA-256 and expected publisher digest when available.
Keep installation media and virtual disks in local lab storage outside the
repository. Start with offline networking and no host folder mappings. Record
the guest build, architecture and fixture filesystem with each capture.
An install ISO or VM configuration does not count as an observation.

Run the portable probe from Windows PowerShell inside the installed guest:

~~~powershell
powershell.exe -NoProfile -File windows_probe.ps1
~~~

Capture stdout as JSON. On x64 Windows run the same probe separately in the
native and WOW64 Windows PowerShell processes, recording the process bitness.
The portable probe records the WMI OS version and SKU. Its x64 development-host
capture agrees with the three Python observations and remains host evidence.

- Windows 7: verified image and dedicated VM preparation are recorded in the
  [behavior reference](../../../docs/architecture/windows-behavior-reference-m149.md).
  Windows 8 and 8.1 guest captures remain open.
- Windows 10: Microsoft publishes a retail ISO download page. A suitable
  licensed or evaluation guest and installed-system capture remain open.
- Windows 11: Microsoft publishes an Enterprise LTSC evaluation ISO. Download
  started and an isolated VMware configuration and growable disk were created.
  Download verification, guest installation and probe execution remain open.

Sources: [Microsoft subscription downloads](https://learn.microsoft.com/en-us/visualstudio/subscriptions/download-software),
[Windows 10 ISO](https://www.microsoft.com/en-us/software-download/windows10ISO),
[Windows 11 evaluation](https://www.microsoft.com/en-us/evalcenter/download-windows-11-enterprise).
