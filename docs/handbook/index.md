# Engacer OS user handbook


## Start here

**Current native release: [M14.8](https://github.com/enginsoysal/engacer-os/releases/tag/m148-v0.14.8).** M14.8 native/source/media qualification passes: 105 native and 41 supporting host groups across 147 campaign tasks, including actual VMware installation and two independent starts. Original SumatraPDF 3.6.1 x64 EXE GUI installation, cold removal and cold reinstall pass. Both installation cycles verify four original payloads and two actual shortcuts. The PDF reader itself remains unqualified. Previous 7-Zip and Notepad++ MSI scopes are retained. Follow matching media and guides.

- [Download, verify and install](install-m148.md)
- [Original MSI and EXE installer walkthrough](windows-m148.md)
- [First day](first-day-m148.md)
- [Current supported behavior and limits](../roadmap/status.md)
- [Release scope and checksums](../releases/m148-v0.14.8.md)
- [Build your distribution](distributions.md)

Arbitrary EXE/MSI installers, the PDF reader, Notepad++ editor, full graphical archive tasks and Firefox execution remain unqualified. The fixtures are not the full product scope. M14.9-M14.16 remain planned, not started; final integrated optimization is M14.16.

## Use the desktop

These task guides explain retained desktop features. Their original test records belong to their named historical media; use the current installation guide and release scope above for current downloads and qualification.

- [First day, desktop and folders](first-day-m147.md)
- [Saved work, screensaver and stability limits](stability-m1313.md)
- [Select files, navigate folders and use USB drives](files-m137.md)
- [Choose views, sorting and full names](files-m126.md)
- [Copy, move and cancel transfers](transfers-m137.md)
- [Open, Save as and extraction-folder dialogs](dialogs-m1310.md)
- [Start search, categories and pinned items](start-m136.md)
- [Window controls and arrangement](desktop-m135.md)
- [Quick settings, safe removal and Calendar](tray-m1212.md)
- [Preview, apply and reset Settings](settings-m1311.md)
- [Keyboard and accessibility](accessibility-m1216.md)
- [Standard apps and optional packages](apps-m1310.md)
- [Disk management and formatting safeguards](disk-manager-m71.md)

## Customize and troubleshoot

- [Personalization and screensaver](personalization-m1311.md)

- [Create your own distribution](distributions.md)
- [Understand messages and preserved work](feedback-m1214.md)
- [Recovery and its limitations](apps-m74.md#disks-and-recovery)
- [Product principles](../architecture/product-principles.md)
- [Find your way around the website](website-m130.md)
- [Website maintenance and publication](../../website/README.md)

The current starter uses an empty growable 20-GiB SATA disk, two CPUs, 128 MiB RAM, NAT networking, HDA audio and Secure Boot off. UEFI installation requires writable firmware variables. Existing-disk replacement requires separate final erasure consent. To check independent disk startup, disconnect CD/DVD while retaining the installed hard disk. Consult the matching release before changing the supported hardware profile or migrating an older installation.

## Historical releases and evidence

Historical guides remain available for the exact versions they describe. Their limits and test results do not qualify newer media.

| Release | Installation and scope |
| --- | --- |
| M13.13 | [Installation](install-m1313.md), [release scope](../releases/m1313-v0.13.13.md) |
| M12.18 | [Installation](install-m1218.md), [release scope](../releases/m1218-v0.12.18.md) |
| M11.6 | [Installation and matrix](install-m116.md), [milestone record](../milestones/m11.md) |
| M8 | [Original supported Windows console/MSI profile](windows-apps-m8.md) |
| M5.1 and earlier | [Numbered setup](install-m51.md), [command installation](install.md), [console reference](m5-console.md) |

M13.13 used the owner's revised ninety-minute stability gate, with 108.78 minutes observed. The original eight-hour/two-hour gates did not pass. M13.7/M13.8 historical freeze causes are not independently established. Named VM checks are not universal hardware or unlimited-uptime qualification. Accepted evidence remains immutable.

[Online documentation and downloads](https://engaceros.brixcanvas.com) are published from canonical GitHub Markdown and official release assets. Whole-system CPU/RAM/storage efficiency remains a core requirement; M14.15 is the mandatory optimization gate.
