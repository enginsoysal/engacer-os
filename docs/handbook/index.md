# Engacer OS user handbook

Current native delivery: **M12.3 / 0.12.3**, within M12-STAGE3-VM-v1.
[Release scope, retained BIOS observation and exact evidence](../releases/m123-v0.12.3.md). Earlier stage
releases remain historical.

Development now follows [M12.0–M12.18](../milestones/m12.md).
[The M12 user journeys](desktop-m12.md) describe the planned consistent desktop.
M12.0 concepts are design evidence. M12.3 supplies the current tested native stage;
the complete final M12 regression remains M12.18.

Extract the complete prepared VMware ZIP, open EngacerOS.vmx and choose I Copied
It if asked. Start, select the disk row in the bordered list, follow Next, review
and install, then choose **Restart to Engacer OS**. The matching ISO may stay
connected. No terminal command, network account or guest driver installer is needed.

M12.3 tests its exact enabled-device VMware starter and QEMU SATA/UEFI and BIOS
journeys, native/empty desktop tasks, actual 150%/4K icons and cached/full
rendering, and idle/resources.
The retained observation concerns an earlier M12.2 concurrent BIOS/AHCI timeout.
A repeat of that candidate passes; its trigger is not isolated and stress
reliability remains unqualified.
The previous M11.6 final artifact has fourteen controller/starter profiles and a
broader original-app/USB regression; those results qualify its own bytes.

- [Download and install M12.3](install-m123.md)
- [Use desktop objects, shortcuts and hidden/restored icons](desktop-m123.md)
- [Recognize original app, folder and file icons](icons-m122.md)
- [Use the shared desktop controls and Files scrollbar](components-m121.md)
- [Select, open and manage real Files items](files-m11.md)
- [Use Start search, categories, pins and taskbar](start-m11.md)
- [Arrange windows and save your appearance](windows-m11.md)
- [Install, run and remove the original Windows 7-Zip console app](windows-apps-m8.md)
- [Use the standard apps and manage optional packages](apps-m74.md)
- [Explore the desktop and navigate your folders](desktop-m73.md)
- [Current release, checksums and qualified limits](../releases/m123-v0.12.3.md)
- [Previous M11.6 final installation and matrix](install-m116.md)
- [Repair boot files and review recovery limits](apps-m74.md#disks-and-recovery)
- [Manage partitions and format safely](disk-manager-m71.md)
- [Build and customize your own distribution](distributions.md)
- [Product principles](../architecture/product-principles.md) and [current status](../roadmap/status.md)

The prepared VM has a new empty growable 20-GiB SATA disk, two CPUs, 128 MiB RAM, NAT networking, HDA audio and Secure Boot off. Use this fresh starter for this storage release; cross-version package-cache migration is not qualified. UEFI startup adds a dedicated boot entry and requires writable firmware variables. Existing-disk replacement requires separate final erasure consent. For a separate disk-only test disconnect only CD/DVD and keep the SATA hard disk connected. The new tests retain the same VMware configuration/NVRAM and use ordinary disk discovery, without forced boot priority.

[Online documentation and downloads](https://engaceros.brixcanvas.com) update from canonical GitHub Markdown and official release assets. [Website maintenance](../../website/README.md).

## Historical and advanced references

[M5.1 numbered setup](install-m51.md), [M5 command-based installation](install.md), [old recovery](recovery.md), [old command reference](m5-console.md), [M4.5 storage](vmware-storage.md) and [console](console.md) describe their respective historical releases. M5/M5.1 data formats are not migrated by M6. Old releases and accepted evidence remain immutable.

M11 installation and desktop qualification is complete within its named VM scope.
M11.0 design, M11.1 input, M11.2 Files, M11.3 Start/taskbar, M11.4 windows/appearance and M11.5 guided setup are complete
within their stage scopes. [M11 progress](../milestones/m11.md) ·
[Files user guide](files-m11.md) · [Start/taskbar guide](start-m11.md) · [setup/desktop contract](desktop-install-m11.md).
M11.6 adds [the full matching regression](../../evidence/M11/6/acceptance-results.json), final media and current manuals. Publication also requires fresh release/site/download verification. Later hardware and Windows expansion are separate milestones.
The earlier [M9 graphics record](../milestones/m9.md) remains historical; it does
not claim 3D acceleration or runtime physical-mode switching.

## Current product delivery order

M6 real installation is complete within its named VM scope. M7 real desktop/networking is complete within M7-VM-v1; M8 qualifies one original Windows console/MSI profile; the wider MS-DOS and Windows 1.x through Windows 11 tracks remain in progress. Engacer OS is the current product name. Convenience, optional diagnostics, distribution freedom and measured CPU/RAM use apply throughout. See [the contracts](../roadmap/milestones.md).

[Native display sizing and design decisions](../architecture/graphics-m73.md). The 4K evidence uses an actual framebuffer; firmware mode availability still applies. Choose Appearance for Auto/100%/150%/200% and save preferences.
