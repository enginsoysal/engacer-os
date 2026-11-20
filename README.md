# Engacer OS

An independent, MIT-licensed operating system with its own BIOS/UEFI loaders, kernel and native desktop. Readable graphics, convenient installation, customization and bounded CPU/RAM/storage use are product requirements. Windows applications are the first foreign application ecosystem; Linux, macOS and ARM remain later extensions.

## Download and get started

**Current native release: [M14.4 / 0.14.4](https://github.com/enginsoysal/engacer-os/releases/tag/m144-v0.14.4).** Twenty matching assets are published. Independent downloads and full 569-page readback pass. Complete browser qualification is blocked because BrixCanvas omits the saved same-page search and article navigation. [Reproduction](evidence/M14/4/development/public-search/brixcanvas-report.txt). M14.4 is not fully closed.

- [Install and restart in VMware](docs/handbook/install-m144.md)
- [Your first day](docs/handbook/first-day-m144.md)
- [Original Windows window preview and supported tasks](docs/handbook/windows-m144.md)
- [Exact tested scope and limitations](docs/releases/m144-v0.14.4.md)
- [Online documentation and downloads](https://engaceros.brixcanvas.com)

M14.4 adds an original 7-Zip x64 window/input/lifetime preview through the own native USER32/compositor, retaining the supported console/MSI profile. Window movement, resizing, minimize/maximize/restore, modal ownership and cleanup pass. Full GUI archive/navigation tasks, Notepad++/Sumatra execution and Firefox execution are not qualified. M14.15 remains the mandatory whole-system CPU/RAM/storage optimization gate.

## Native runtime qualification: M14.4

All 47 native groups and eight supporting host groups pass on the frozen 672-input candidate. Original compact, ordinary and actual 4K/200% window profiles pass alongside process/thread/TLS/exception, files/settings, installation and cancellation regressions. The exact enabled-device VMware package installs, starts the original window, moves/closes it and boots twice without its ISO. [Acceptance](evidence/M14/4/acceptance-results.json), [resource accounting](evidence/M14/4/resources.json).

Windows program instructions execute through Engacer OS's own compatibility APIs and kernel. An embedded Windows guest or second OS is not the implementation. VMware and QEMU are external test hosts.

- [M14.4 stage and publication gates](docs/milestones/m14-4.md)
- [File/settings ownership and bounds](docs/architecture/files-m143.md)
- [Retained execution and lifetime contract](docs/architecture/runtime-m142.md)
- [Child ownership](docs/architecture/children-m142.md), [synchronization](docs/architecture/synchronization-m142.md), [exception scope](docs/architecture/exceptions-m142.md)
- [Ordered M14.0-M14.15 plan](docs/milestones/m14.md)

Twenty repeated closes retain zero managed pages after initialization. Normal exit, UI cancellation and unhandled faults release file/registry state while preserving acknowledged settings. Root/child metadata is 13 pages smaller per process than M14.2 in that component; this is not total OS RAM or original GUI performance. **M14.15 remains the mandatory whole-system CPU/RAM/storage optimization gate.** M15 covers Windows x86 and M16 covers Win16/DOS. Every stage closes tests, English docs, GitHub and the actual complete website before the next.

## Use, customize and contribute

| Task | Guide |
| --- | --- |
| Find instructions | [User handbook](docs/handbook/index.md) |
| Check capabilities and known limits | [Current status](docs/roadmap/status.md) |
| Build your own distribution | [Current recipe and historical editions](docs/handbook/distributions.md) |
| Understand the architecture | [Architecture overview](docs/architecture/overview.md) |
| Build or contribute | [Contributing](CONTRIBUTING.md), [pinned tools](tools/README.md) |
| Review project requirements | [Product principles](docs/architecture/product-principles.md) |

Optional applications have separate ownership: removing Calculator must not remove Files, Settings or the desktop. Custom distributions must validate their recipe and independently qualify their changed media. Core storage consent and protected ownership remain enforced.

## Release history and license

Earlier media, source tags and accepted evidence remain immutable. Follow the guide matching the version you download.

- [M14.2 accepted native runtime and public delivery](docs/releases/m142-v0.14.2.md)
- [M13.13 release and revised stability scope](docs/releases/m1313-v0.13.13.md)
- [M12.18 desktop release](docs/releases/m1218-v0.12.18.md)
- [M11.6 installation and matrix](docs/handbook/install-m116.md)
- [Ordered online project archive](https://engaceros.brixcanvas.com/blog/documentation-archive)

[MIT license](LICENSE). Third-party components retain their own licenses and provenance records. Source, documentation and release assets belong to [enginsoysal/engacer-os](https://github.com/enginsoysal/engacer-os).
