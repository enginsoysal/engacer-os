# M11.5 native setup and installed-startup evidence

Native qualification passed on 16 November 2026 within **M11-STAGE5-VM-v1**.
[Acceptance](acceptance-results.json) binds build
`a3b7513cdcf772f5b3a2b4845b84509e`, 562 compiled source inputs and fourteen
artifacts, including the exact separately tested VMware starter ZIP.
Visible release and complete fresh website/download verification close separately.

## Real tasks

- [Ordinary 1280×800](ordinary/results.json), [1920×1200 at 150%](150/results.json)
  and [actual 3840×2160](4k/results.json): eight-step setup, real layout typing,
  size refusal/selection, retained Back choices, explicit disk row, app choices,
  account editing and appearance, independent on-disk preference payloads,
  retained-ISO reset and two disk-only boots using original NVRAM.
- [Disk and recovery](safety/results.json): actual partition create/delete and
  FAT32/native format; unchecked/cancelled consent; independent foreign disk/
  partition byte preservation; fresh whole-disk consent; missing/small disk
  refusal; injected write error, safe quarantine, same-disk/NVRAM retry after
  fixing the fault/restarting; visible UEFI Escape entry, real boot-slot repair
  and disk-only BIOS startup after deliberately corrupting an owned payload.
- [Minimal install package lifecycle](packages/results.json): active saved Dvorak
  and 150% providers; offline Calculator installation, original native-worker
  launch, reviewed removal and working Files afterward, with zero retained pages.
- [Exact VMware starter](vmware/results.json): all shipped network/USB/HDA devices
  enabled; real blank 20-GiB SATA/UEFI install, retained-ISO reset, DHCP,
  first-start guide, window/Appearance interaction and two disk-only boots.
  Existing user VM inventory remains unchanged; host desktop is not controlled.

The 26 native task groups use ordinary guest mouse/keyboard events. No test writes
guest memory. State inspection is read-only. Capture JSON identifies physical
framebuffer size/stride and raw SHA256; images are not resized mockups.

## Screens and review

| Step | Actual native capture |
|---|---|
| Welcome | [Ordinary](ordinary/01-welcome.png) |
| Keyboard / size | [Ordinary](ordinary/02-keyboard.png) |
| Disk selection | [Selected](ordinary/03-disk-selected.png) |
| Components | [Apps](ordinary/04-apps.png), [more apps](ordinary/04-more-apps.png) |
| Account and appearance | [Style](ordinary/05-your-style.png) |
| Before writes | [Review](ordinary/06-review.png) |
| Verified completion | [Ready](ordinary/07-installed-verified.png) |
| Real installed desktop | [First-start guide](vmware/first-start-guide.png), [ordinary Files](ordinary/09-installed-desktop.png) |
| 150% minimal desktop | [Start without optional apps](150/no-optional-apps-start.png) |
| Actual 4K | [Installed Files](4k/09-installed-desktop.png), [capture metadata](4k/09-installed-desktop-capture.json) |
| Recovery | [Recovery complete](safety/recovery-complete.png) |

[Clarity, convenience, visual and readability review](../../../docs/architecture/usability-review-m115.md)
is an agent scenario review, not a human study. [Resource evidence](resources.json)
separates fixed desktop state, managed-page observations and configured RAM.
Fixed desktop BSS/data is sixteen bytes above M11.4 and remains inside the total
512-KiB added-state budget. Boot allocation-failure counters include existing
deliberate stress probes and are not represented as new installer failures.

## Diagnostics and limits

[Initial retry assumption](safety/retry-assumption-first-run.json) is deliberately
retained as a failed preliminary harness expectation. It assumed the driver
would immediately become writable after a one-shot host fault. The actual safe
controller quarantine refused Next. Final verification preserves that refusal,
then proves retry after fixing the fault and restarting with the same disk/NVRAM.
It is not counted as a successful native task or hidden as a pass.

The original [pointer classifier](pointer-host-results.json) and
[Start/power validator](start-host-results.json) also pass their host checks;
these are separate from native integration evidence. [Earlier media hashes](preserved-releases.json)
remain unchanged. [Candidate manifest](candidate-manifest.json) and
[starter manifest](starter-manifest.json) identify exact artifacts.

The full new-artifact controller/device/original-Windows-app matrix remains
M11.6. No universal/physical/ARM devices, vendor GPU 3D or general Windows
compatibility claim follows from these virtual setup tasks. Installation still
uses the qualified whole-disk layout and documented sector/capacity bounds.
The English manual documents quarantined-controller restart, limited layouts,
UTC and the absence of partition resize/dual boot/selected-partition OS install.
