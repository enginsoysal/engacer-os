# Engacer OS

An independent, MIT-licensed operating system with its own BIOS/UEFI loaders,
kernel and native desktop. Convenience, readable graphics, customization and
bounded CPU/RAM use are product requirements.

**M12.17 / 0.12.17 passes M12-STAGE17-VM-v1.**
[Install](docs/handbook/install-m1217.md), [Motion and resource use](docs/handbook/performance-m1217.md),
[release scope](docs/releases/m1217-v0.12.17.md),
[exact-source acceptance](evidence/M12/17/acceptance-results.json).
599 compiled Git inputs and 16 native task/profile checks cover
actual keyboard/accessibility carry, independent saved choices, five display
profiles, reverse pane focus, default-effect motion and Escape-cancelled moves.
The exact production raster matches M12.16 in 3,073 host cases while visiting
92.5% fewer positions in its 4K shadow test; this is not native FPS.
Exact enabled-device VMware, BIOS, twelve default-effects movement comparisons
and compressed repair pass. Fixed shell state stays 553,452 bytes (+0);
completed tasks retain zero managed pages. No new animation worker/cache is added.
Public release and complete website verification remain the gates before M12.18.

Previous [M12.16 complete public delivery](evidence/M12/16/publication-results.json)
remains immutable: twenty downloads, 395 pages and 2,749 HTTP links.


M12.18 retains the earlier BIOS/AHCI observation and final matrix. Native stage
proof does not imply universal hardware or Windows support. Agent review is not
a human usability study.

The owner authorized [M12.0 through M12.18](docs/milestones/m12.md) strictly in
order, with tests, English manuals, matching GitHub releases and complete website
verification after each stage. [Design](docs/architecture/desktop-m12.md).

**Previous complete M11 delivery: M11.6 / 0.11.6 - final installation and desktop qualification**,
within **M11-FINAL-VM-v1**. [Release and checksums](docs/releases/m116-v0.11.6.md),
[exact-source acceptance](evidence/M11/6/acceptance-results.json),
[current status](docs/roadmap/status.md). Thirty-six native report groups include
fourteen enabled-device VMware controller/starter profiles, eight-step setup,
real partition/format/error/recovery, Files, Start/taskbar, window commands,
ordinary/150%/actual-4K rendering, USB round trips and the original 7-Zip MSI/console
lifecycle. Every controller profile installs, resets with its matching ISO and
starts twice without it. The exact starter's 106 original application payloads
are independently verified. This is named VM qualification; physical hardware,
ARM, vendor GPU 3D and universal Windows compatibility remain unqualified.

**The M11 sequence now has its final native qualification.**
[Interaction and design](docs/architecture/desktop-m11.md),
[Files](docs/handbook/files-m11.md), [Start/taskbar](docs/handbook/start-m11.md),
[windows/appearance](docs/handbook/windows-m11.md),
[eight-step setup](docs/handbook/install-m116.md) and
[final qualification decisions](docs/architecture/qualification-m116.md).
Final fixed desktop state is unchanged from M11.5. Window movement, USB reconnect
and offline Calculator lifecycle retain no extra managed pages; idle CPUs halt.
GitHub release and fresh public website verification are recorded separately
with the final publication evidence. Earlier accepted releases remain immutable.

## Try it in VMware

[Download the prepared VMware ZIP](https://github.com/enginsoysal/engacer-os/releases/download/m1217-v0.12.17/EngacerOS-M12STAGE17-VMware.zip) ·
[Standalone ISO](https://github.com/enginsoysal/engacer-os/releases/download/m1217-v0.12.17/EngacerOS-M12STAGE17.iso) ·
[Step-by-step installation](docs/handbook/install-m1217.md) ·
[English documentation and downloads](https://engaceros.brixcanvas.com).

Extract the whole ZIP, open **EngacerOS.vmx**, and choose **I Copied It** if asked.
Start the VM, click the disk row inside the bordered list, follow Next, review
your choices and choose **Install Engacer OS**. Finish with **Restart to Engacer OS**.
The package includes a new blank growable 20-GiB SATA disk, two CPUs and 128 MiB RAM.
It performs a real installation; the disk is not preinstalled. No online account,
terminal command or guest driver installer is required. Keep Secure Boot off.
The matching ISO may remain attached. For an independent boot, disconnect only
CD/DVD and keep the same installed hard disk connected.

## Hardware and original-app qualification

[M11.6 acceptance](evidence/M11/6/acceptance-results.json) reruns the controller,
device and original-app tasks on the final bytes. [M10](docs/releases/m10-v0.10.0.md)
remains a separate historical record; its hashes are preserved.

- Automatic supported-device binding and common capability/status reporting in
  **Start → Settings → Devices**. Ready, Limited, Detected and Unavailable reflect
  actual providers; recognition alone is not usable functionality.
- Saved US QWERTY/Dvorak choices, qualified keyboard/mouse/wheel input, supported
  xHCI HID/hubs, disconnect and reconnect.
- **Files → USB drives**: browse supported FAT32 media, copy files to Downloads,
  right-click a native file and choose **Copy to USB...**, flush, safely remove and reconnect.
- Ordinary and actual 4K presentation, reachable partially off-screen windows,
  checked repaint, stable retained pages during movement and halted idle CPUs.
- New-artifact VMware installation, persistence and two detached boots on SATA,
  IDE, LSI Logic, LSI SAS, PVSCSI and NVMe under BIOS/UEFI, plus BusLogic BIOS.
- The exact prepared ZIP also passes native Devices/layout interaction and the
  original 7-Zip 26.06 x64 MSI install/run/archive/extract/remove/reinstall task.

[Current device and USB tutorial](docs/handbook/install-m116.md#use-a-usb-drive) ·
[Hardware architecture: how and why](docs/architecture/hardware-m10.md) ·
[Standard applications](docs/handbook/apps-m74.md) ·
[Original Windows app guide](docs/handbook/windows-apps-m8.md).

## Boundaries and next work

USB writes require supported BOT media, 512-byte sectors, working flush and a
clean mirrored FAT32 volume. Copies create files without overwriting; each file
is bounded at 64 MiB. Directory growth, exFAT/NTFS writes, USB installation and
formatting are outside this slice. Failure can require an offline FAT check.
The release guide records the exact bounds and the unqualified 64-MiB OVMF
boot-attached USB allocation case. The ordinary VMware package uses 128 MiB.

Wi-Fi setup, comprehensive audio, vendor GPU 3D, multi-monitor support, laptops,
ARM/Raspberry Pi and Steam gaming remain [later hardware phases](docs/milestones/m10.md).
Original MS-DOS and Windows 1.x through Windows 11 compatibility remains a wider
program: only the named 7-Zip console/MSI profile is currently qualified.

## Build, customize and verify

Use a separate checkout to reproduce accepted releases. For new work choose a
distinct revision and preserve frozen accepted outputs.

```powershell
python tools/build/m10.py
python tools/release/vmware_starter10.py
# Run the complete frozen-artifact sequence in tests/m10/README.md.
python tests/m10/verify.py
```

[Host tools](tools/README.md) · [Qualification commands](tests/m10/README.md) ·
[Custom distributions](docs/handbook/distributions.md) ·
[Contributing](CONTRIBUTING.md) · [Architecture](docs/architecture/overview.md) ·
[OS folder structure](docs/architecture/filesystem.md).
Optional apps remain separate from required Files/Settings/services. A changed
profile needs its own qualification; the standard ISO's evidence does not
qualify an arbitrary custom build.

## Repository structure

```text
boot/                  Original BIOS/UEFI loaders
kernel/                Core, device, storage, input, network and desktop providers
include/engine/        Stable internal ABI and shared headers
runtime/, user/        Freestanding runtime and protected native/Windows workers
distros/               Validated profiles and independent data/app packages
tools/build/           Milestone builds and media authoring
tools/release/, tools/vm/ Release packages and owned guest tooling
tests/m*/              Per-milestone qualification harnesses
docs/                  Architecture, handbook, milestones, roadmap and releases
evidence/              Sanitized reports, native captures and accepted hashes
website/               Native BrixCanvas composition and GitHub article publisher
build/, dist/          Generated outputs, ignored by Git
tools/local/           Local pinned dependencies, ignored by Git
```

OS sources remain independent from BrixCanvas. The website uses editable native
BrixCanvas blocks and automatically synchronized English GitHub documentation.
The product and repository are Engacer OS / `enginsoysal/engacer-os`; internal
ABI identifiers and historical Engine OS releases remain stable for verification.
[Historical release index](docs/releases/CHANGELOG.md).

All current documentation, UI strings and comments are English. Behavior changes
update design, tests, evidence and user instructions together and are pushed to
[GitHub](https://github.com/enginsoysal/engacer-os). Never publish credentials,
private host paths or local archives. Original code uses the [MIT license](LICENSE);
third-party components retain their licenses and notices. Guest RAM is not a
measurement of total kernel consumption, and a boot screen is not app compatibility.
