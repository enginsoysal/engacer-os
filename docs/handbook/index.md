# Engacer OS user handbook

## Start here

**Current qualified release: [Engacer OS M14.3](https://github.com/enginsoysal/engacer-os/releases/tag/m143-v0.14.3).** Native qualification and complete public delivery pass within M14-STAGE3-VM-v1. Complete actual website verification passes: 555 pages, 359 exact-source articles and 4,063 links, with zero known broken targets and 12 explicitly unverified external references. [Publication receipt](../../evidence/M14/3/publication-results.json). Follow the guide matching the release you download.

- [Download, verify and install in VMware](install-m143.md)
- [Windows files, persistent settings and browser downloads](windows-m143.md)
- [What works today and current limitations](../roadmap/status.md)
- [Release scope and checksums](../releases/m143-v0.14.3.md)
- [Build and customize your own distribution](distributions.md)

M14.3 adds selected Unicode file/path/search, sharing/locking, persistent user registry and environment behavior over the native process/thread runtime. It retains the original supported 7-Zip console/MSI tasks. Notepad++/Sumatra remain inspection-only; Firefox remains download-only. There is no embedded Windows guest. [Native acceptance](../../evidence/M14/3/acceptance-results.json), [resource bounds](../../evidence/M14/3/resources.json). M14.15 remains the mandatory whole-system optimization gate.

## Use the desktop

These task guides explain retained desktop features. Their original test records belong to their named historical media; use the current installation guide and release scope above for current downloads and qualification.

- [First day, desktop and folders](first-day-m143.md)
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
