# Contributing

Engacer OS is an independent own-kernel project with a native graphical installer,
installed folder desktop and a bounded original 7-Zip Windows console/MSI profile.
M14.1 is the current qualified loader release; M14.2 process/thread/TLS/exception work is in development. The [current status](docs/roadmap/status.md) identifies the accepted release and remaining limits. Read the
[architecture](docs/architecture/overview.md), [decisions](docs/architecture/decisions.md)
and [agent instructions](AGENTS.md) first. Historical Engine OS artifacts remain
verifiable under their original identities.

## Language, structure and documentation

All current documents, code comments, UI strings and release notes are English. Keep code under its source subsystem, docs under architecture/roadmap/milestones/releases, and tests/evidence grouped by milestone. Do not add root-level planning files or put OS files in BrixCanvas. Never publish ignored local archives.

Every behavior/scope change updates contracts/status, user commands, tests/evidence and known limitations in the same coherent change. New findings supersede plans explicitly. Historical tags/reports retain their original identity; do not rewrite their hashes to match new source paths.

## Current UI quality gate

Use the five questions in [product principles](docs/architecture/product-principles.md) and inspect actual native setup/desktop captures at minimum and HiDPI sizes. Do not use browser mockups or enlarged screenshots as 4K proof. The Inter source/rasterizer/output digest is pinned; preserve the full OFL notices. Reproduce M7.3 only in a separate release checkout using [its commands and limits](evidence/M7.3/README.md). New changes require new milestone/revision outputs; never overwrite accepted historical evidence or binaries.

## Verification and resources

For the current **unaccepted M14.2 development stage**, the initial checks are:

```powershell
python tools/build/m14.py --stage 2
python tests/m14/native1.py --stage 2 --profile compact
python tests/m14/thread_native2.py
python tests/m14/lifetime_native2.py
```

These checks are part of development, not the complete M14.2 release gate. Read the [stage record](docs/milestones/m14-2.md) and [runtime contract](docs/architecture/runtime-m142.md) before adding tests or claiming compatibility. Build tools refuse accepted stages; reproduce an accepted tag only in a separate checkout. Do not overwrite prior media or evidence. [Custom distribution instructions](docs/handbook/distributions.md).

Use the [pinned host tools](tools/README.md). Native qualification needs the pinned compiler, QEMU/OVMF, VMware Workstation and the named Python dependencies. Tests use disposable images without host disk/directory exposure. Keep large scratch storage outside OneDrive. Source, host-test and native execution evidence must be distinguished. Windows code executes directly through the compatibility runtime; an embedded Windows VM is not an implementation route.
