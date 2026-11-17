# Engacer OS user handbook

**M12.17 / 0.12.17 passes M12-STAGE17-VM-v1.**
[Install](install-m1217.md), [Motion and resource use](performance-m1217.md),
[release scope](../releases/m1217-v0.12.17.md),
[exact-source acceptance](../../evidence/M12/17/acceptance-results.json).
599 compiled Git inputs and 16 native task/profile checks cover
actual keyboard/accessibility carry, independent saved choices, five display
profiles, reverse pane focus, default-effect motion and Escape-cancelled moves.
The exact production raster matches M12.16 in 3,073 host cases while visiting
92.5% fewer positions in its 4K shadow test; this is not native FPS.
Exact enabled-device VMware, BIOS, twelve default-effects movement comparisons
and compressed repair pass. Fixed shell state stays 553,452 bytes (+0);
completed tasks retain zero managed pages. No new animation worker/cache is added.
Public release and complete website verification remain the gates before M12.18.

Previous [M12.16 complete public delivery](../../evidence/M12/16/publication-results.json)
remains immutable: twenty downloads, 395 pages and 2,749 HTTP links.


The previous M11.6 final artifact has fourteen controller/starter profiles and a
broader original-app/USB regression; those results qualify its own bytes.

- [Download and install M12.17](install-m1217.md)
- [Motion and resource use](performance-m1217.md)
- [Keyboard and accessibility](accessibility-m1216.md)
- [Use the eight-step setup and first-start guide](setup-m1215.md)
- [Understand messages, refusals and preserved work](feedback-m1214.md)
- [Preview, apply, cancel and reset Settings](settings-m1213.md)
- [Use quick settings, USB safe removal and Calendar](tray-m1212.md)
- [Open, Save as, Cancel and choose an extraction folder](dialogs-m128.md)
- [Copy, move, cancel and inspect transfer results](transfers-m127.md)
- [Choose Files views, order and full names](files-m126.md)
- [Navigate native folders and USB](files-m125.md)
- [Use desktop objects, shortcuts and hidden/restored icons](desktop-m123.md)
- [Recognize original app, folder and file icons](icons-m122.md)
- [Use the shared desktop controls and Files scrollbar](components-m121.md)
- [Select, open and manage real Files items](files-m11.md)
- [Use Start search, categories and pins](start-m129.md)
- [Use title-bar controls and arrange windows](windows-m124.md)
- [Save appearance preferences](windows-m11.md)
- [Install, run and remove the original Windows 7-Zip console app](windows-apps-m8.md)
- [Use the standard apps and manage optional packages](apps-m74.md)
- [Explore the desktop and navigate your folders](desktop-m73.md)
- [Current release, checksums and qualified limits](../releases/m1217-v0.12.17.md)
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
