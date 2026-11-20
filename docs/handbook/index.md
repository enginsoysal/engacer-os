# Engacer OS user handbook

## Start here

**Current native candidate: [M14.5](https://github.com/enginsoysal/engacer-os/releases/tag/m145-v0.14.5).** Native qualification passes within M14-STAGE5-VM-v1. Complete actual website verification passes within the owner-approved content/layout scope: 588 pages, 379 exact-source articles and 4307 links; zero known broken targets and 12 explicitly unverified external references. All twenty public release assets are independently downloaded and verified. Missing advanced BrixCanvas search/task navigation remains reported and unqualified. Follow the guide matching your download.

- [Download, verify and install in VMware](install-m145.md)
- [Original Windows menus, folders and browser downloads](windows-m145.md)
- [Current supported behavior and limits](../roadmap/status.md)
- [Release scope and checksums](../releases/m145-v0.14.5.md)
- [Build your distribution](distributions.md)

M14.5 adds original 7-Zip menu/About, toolbar images, list details and folder-navigation preview tasks. Complete GUI archive tasks, Notepad++/Sumatra interfaces and Firefox execution remain unqualified. [Native acceptance](../../evidence/M14/5/acceptance-results.json). M14.15 remains the mandatory whole-system optimization gate.

## Use the desktop

These task guides explain retained desktop features. Their original test records belong to their named historical media; use the current installation guide and release scope above for current downloads and qualification.

- [First day, desktop and folders](first-day-m145.md)
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
