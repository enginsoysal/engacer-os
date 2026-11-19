# Contributing

Engacer OS is an independent own-kernel project with a native graphical installer,
installed folder desktop and a bounded original 7-Zip Windows console/MSI profile.
M14.2 is the current qualified native process/thread/TLS, shared synchronization and selected C exception/unwind stage. General Windows GUI/browser execution remains unavailable. The [current status](docs/roadmap/status.md) identifies the accepted release and remaining limits. Read the
[architecture](docs/architecture/overview.md), [decisions](docs/architecture/decisions.md)
and [agent instructions](AGENTS.md) first. Historical Engine OS artifacts remain
verifiable under their original identities.

## Language, structure and documentation

All current documents, code comments, UI strings and release notes are English. Keep code under its source subsystem, docs under architecture/roadmap/milestones/releases, and tests/evidence grouped by milestone. Do not add root-level planning files or put OS files in BrixCanvas. Never publish ignored local archives.

Every behavior/scope change updates contracts/status, user commands, tests/evidence and known limitations in the same coherent change. New findings supersede plans explicitly. Historical tags/reports retain their original identity; do not rewrite their hashes to match new source paths.

## Current UI quality gate

Use the five questions in [product principles](docs/architecture/product-principles.md) and inspect actual native setup/desktop captures at minimum and HiDPI sizes. Do not use browser mockups or enlarged screenshots as 4K proof. The Inter source/rasterizer/output digest is pinned; preserve the full OFL notices. Reproduce M7.3 only in a separate release checkout using [its commands and limits](evidence/M7.3/README.md). New changes require new milestone/revision outputs; never overwrite accepted historical evidence or binaries.

## Verification and resources

M14.2 media and native evidence are frozen. Read the [stage record](docs/milestones/m14-2.md), [runtime scope](docs/architecture/runtime-m142.md) and [exact native acceptance](evidence/M14/2/acceptance-results.json). Reproduce an accepted tag only in a separate checkout; never overwrite its source/media/maps/evidence. The stage builder deliberately refuses accepted output.

For a custom edition, follow the [current distribution recipe](docs/handbook/distributions.md), choose a distinct identity/revision and independently qualify changed media. For future milestone work, use the next authorized unaccepted stage's separate output prefix and freeze its compiled inputs and artifacts while guests run. Do not present an unchanged rebuild or host unit test as new native compatibility.

The M14.2 corpus under `tests/m14/` separates real installed starts, original 7-Zip/MSI tasks, process/thread/TLS/synchronization/exception probes, malformed/fault/cancellation cases, original-file inspection, actual Firefox transfer, host-only HTTP/storage checks and the exact headless VMware ZIP. `verify2.py` is the final source/media/native gate, not a substitute for running its required matching reports. Follow that stage's recorded command sequence and fixture prerequisites when reproducing it. Public asset hashes, actual native website Saves and complete site/search/mobile/link checks close publication separately.

Use the [pinned host tools](tools/README.md). Native qualification needs the pinned compiler, QEMU/OVMF, VMware Workstation and the named Python dependencies. Tests use disposable images without host disk/directory exposure. Keep large scratch storage outside OneDrive. Source, host-test and native execution evidence must be distinguished. Windows code executes directly through the compatibility runtime; an embedded Windows VM is not an implementation route.
