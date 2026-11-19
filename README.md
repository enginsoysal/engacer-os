# Engacer OS

An independent, MIT-licensed operating system with its own BIOS/UEFI loaders, kernel and native desktop. Readable graphics, convenient installation, customization and bounded CPU/RAM/storage use are product requirements. Windows applications are the first foreign application ecosystem; Linux, macOS and ARM remain later extensions.

## Download and get started

**Current qualified release: [M14.2 / 0.14.2](https://github.com/enginsoysal/engacer-os/releases/tag/m142-v0.14.2).** Use its matching ISO or prepared VMware package and checksums.

- [Install and restart in VMware](docs/handbook/install-m142.md)
- [Your first day](docs/handbook/first-day-m142.md)
- [Windows files and browser downloads](docs/handbook/windows-m142.md)
- [Exact tested scope and limitations](docs/releases/m142-v0.14.2.md)
- [Online documentation and downloads](https://engaceros.brixcanvas.com)

M14.2 qualifies its bounded native runtime and original supported 7-Zip console/MSI profile. Original Notepad++ and Sumatra images can be mapped and inspected; their GUI is not qualified. Firefox can be downloaded and hash-checked, but cannot yet install or run. Named virtual-machine checks do not establish universal physical-hardware, GPU 3D or general Windows compatibility.

## Native runtime qualification: M14.2

M14.2 passes exact-source native and VMware qualification for private parent/child processes, preemptive threads, static/dynamic TLS, events/semaphores/timers, cross-process named sharing and the documented AMD64 hardware-fault/C exception profile. Original concurrent 7-Zip children and repeated resource-release checks pass. Complete actual website verification passes: 545 pages, 352 exact-source articles and 3,932 links, with zero known broken targets and 12 explicitly unverified external references. [Publication receipt](evidence/M14/2/publication-results.json).

Windows program instructions execute through Engacer OS's own compatibility APIs and kernel. An embedded Windows guest or second operating system is not the implementation. VMware and QEMU are external test hosts.

- [M14.2 progress and remaining gates](docs/milestones/m14-2.md)
- [Execution and lifetime](docs/architecture/runtime-m142.md)
- [Child-process ownership](docs/architecture/children-m142.md)
- [Shared synchronization and limits](docs/architecture/synchronization-m142.md)
- [Exception dispatch and unwind scope](docs/architecture/exceptions-m142.md)
- [Ordered M14.0-M14.25 plan](docs/milestones/m14.md)

M14.25 is the mandatory whole-system CPU/RAM/storage optimization gate. Resource bounds, idle halt, peak usage and retained memory are measured separately; configured guest RAM is not total OS consumption. M15 covers Windows x86 and M16 covers Win16/DOS. Each stage closes tests, English guides, GitHub delivery and actual website verification before the next.

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

- [M13.13 release and revised stability scope](docs/releases/m1313-v0.13.13.md)
- [M12.18 desktop release](docs/releases/m1218-v0.12.18.md)
- [M11.6 installation and matrix](docs/handbook/install-m116.md)
- [Ordered online project archive](https://engaceros.brixcanvas.com/blog/documentation-archive)

[MIT license](LICENSE). Third-party components retain their own licenses and provenance records. Source, documentation and release assets belong to [enginsoysal/engacer-os](https://github.com/enginsoysal/engacer-os).
