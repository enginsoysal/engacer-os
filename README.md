# Engacer OS

An independent, MIT-licensed OS with its own loaders, kernel and desktop. Clear installation, customization and bounded CPU/RAM/storage use are core requirements. Windows applications are the first foreign ecosystem; Linux, macOS and ARM remain later extensions.


## Download and get started

**Current native release: [M14.8 / 0.14.8](https://github.com/enginsoysal/engacer-os/releases/tag/m148-v0.14.8).** M14.8 native/source/media qualification passes: 105 native and 41 supporting host groups across 147 campaign tasks, including actual VMware installation and two independent starts. Original SumatraPDF 3.6.1 x64 EXE GUI installation, cold removal and cold reinstall pass. Both installation cycles verify four original payloads and two actual shortcuts. The PDF reader itself remains unqualified. Previous 7-Zip and Notepad++ MSI scopes are retained.

- [Install and restart in VMware](docs/handbook/install-m148.md)
- [Your first day](docs/handbook/first-day-m148.md)
- [Original MSI and EXE installers](docs/handbook/windows-m148.md)
- [Release scope and limits](docs/releases/m148-v0.14.8.md)
- [Documentation and downloads](https://engaceros.brixcanvas.com/blog/downloads)

Arbitrary EXE/MSI installers, the PDF reader, Notepad++ editor, full graphical archive tasks and Firefox execution remain unqualified. The fixtures are not the full product scope. M14.9-M14.16 remain planned, not started; final integrated optimization is M14.16.

All twenty GitHub release assets were independently downloaded and verified, including ZIP CRC and the embedded ISO. Native homepage Save remains blocked by the reproduced BrixCanvas website-read error; articles synchronize from GitHub. Complete public content checks are recorded separately; a stale homepage is not counted as successful publication.


**Approved planning update (23 November 2026):** future Windows apps receive
one independent directory with private DLL/runtime/helper copies and registry;
no cross-app dependency sharing. Automatic missing-component assistance,
right-click Add dependency and ordinary installer Advanced targeting share one
owner-bound lifecycle. This is a plan, not a shipped M14.8 feature.
[Architecture](docs/architecture/windows-app-environments.md), [detailed M14.9-M14.16 stages](docs/milestones/m14-consolidated.md), [M15/x86](docs/milestones/m15.md), [M16/Win16-DOS](docs/milestones/m16.md). No runtime implementation is authorized by this planning task.

## Native qualification

Build fdb650a0e4cff632bd4945cc1b024567 binds compiled source bd12730bf19eee5a4ab496d798a7c0435728fed0 and 825 exact inputs. [Acceptance](evidence/M14/8/acceptance-results.json), [resources](evidence/M14/8/resources.json), [stage gates](docs/milestones/m14-8.md). Windows instructions execute through the own kernel and compatibility APIs, without an embedded Windows guest.

The [approved M14.9-M14.16 program](docs/milestones/m14-consolidated.md) covers the full Windows 7/8/8.1/10/11 x64 landscape and necessary dependencies. Stop after M14.8; future implementation is not started.

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
