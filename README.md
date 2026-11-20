# Engacer OS

An independent, MIT-licensed OS with its own loaders, kernel and desktop. Clear installation, customization and bounded CPU/RAM/storage use are core requirements. Windows applications are the first foreign ecosystem; Linux, macOS and ARM remain later extensions.

## Download and get started

**Current native candidate: [M14.5 / 0.14.5](https://github.com/enginsoysal/engacer-os/releases/tag/m145-v0.14.5).** Native/source/media qualification passes. Matching GitHub assets and complete actual website verification are being finalized before M14.6. Reported BrixCanvas search/navigation remains nonblocking; missing platform features are not called passed.

- [Install and restart in VMware](docs/handbook/install-m145.md)
- [Your first day](docs/handbook/first-day-m145.md)
- [Original Windows menus, folders and browser choices](docs/handbook/windows-m145.md)
- [Exact release scope and limits](docs/releases/m145-v0.14.5.md)
- [Documentation and downloads](https://engaceros.brixcanvas.com)

M14.5 adds original 7-Zip x64 menus/About dialog, toolbar images, list details and Documents/subfolder/Backspace navigation preview through the own native compatibility APIs. Existing console/MSI tasks remain supported. Full GUI archive tasks, Notepad++/Sumatra interfaces and Firefox execution remain unqualified. All three original target scenarios remain mandatory in M14.12; whole-system CPU/RAM/storage optimization blocks final M14.15.

## Native qualification

All 60 native and 13 supporting host groups pass on build `06c8de63a527c32ad9ec73f4b9e333bc` with 695 exact compiled inputs. Compact, ordinary and actual 4K/200% installation/startup and original MSI/106-payload regressions pass. The exact VMware package installs, starts the original app, moves/closes it and boots twice without ISO. [Acceptance](evidence/M14/5/acceptance-results.json), [resources](evidence/M14/5/resources.json), [stage gates](docs/milestones/m14-5.md).

Windows program instructions run through the own compatibility APIs and kernel. VMware/QEMU are external test hosts; an embedded Windows guest is not the implementation. Optional app removal preserves the desktop and personal files. M14.15 remains the mandatory whole-system optimization gate.

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
