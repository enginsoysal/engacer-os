# M14.9-M14.16 - Independent Windows app environments and full x64 compatibility

Owner-approved future program, revised 23 November 2026 after the 21 November
consolidation. **M14.9 is in progress** as of 26 November 2026. M14.10-M14.16 remain planned. The owner authorized M14.9 contracts and reference laboratory work.
M14.8 remains the qualified native release within its recorded scope; its
blocked native homepage publication is recorded separately in current status.
No new OS implementation, ISO or compatibility claim is created here.

## Mandatory architecture

The owner-selected rule is one self-contained app directory with independent
copies of its DLLs, runtimes, helper programs, private registry and installed
state. If A and B need the same component, install it twice. No global mutable
Windows application registry, shared dependency store, cross-app file/link/
dedup shortcut or app-code page coalescing. Removing/updating A must not affect
B's components or real behavior.

The [complete environment contract](../architecture/windows-app-environments.md)
defines ownership, physical layout, private Windows views, services/drivers,
legacy migration, detection and acceptance. Native OS/kernel/hardware management
remains the foundation; it is not an app-owned dependency shared through A.
Personal documents stay separate by default and are preserved on uninstall.

The full product goal remains original Windows 7/8/8.1/10/11 x64 applications
and their necessary installers, mixed-architecture helpers, runtimes, services
and drivers. Named apps are fixtures, not a whitelist or the compatibility scope.
Original x64/x86 instructions use the own kernel/compatibility environment, not
an embedded Windows guest. Private packaging does not implement missing APIs.

## Three routes, one installation engine

1. Automatic assistance for a confidently attributed necessary missing component,
   including one requested after successful launch; explicit user consent.
2. Right-click the target app and choose Add dependency.
3. Open an installer normally; under collapsed Advanced options choose Install
   as dependency for an existing app, then explicitly select the target.

Ordinary standalone installation is always primary/default for a separately
opened installer. Recognition or the most recent foreground app cannot change
that default or grant authority. Unknown cases retain manual routes. Optional
probes are not compulsory failures; no permanent scanner or automatic arbitrary
DLL download is part of the design.

## Ordered implementation

Each linked stage specifies its work, how/why, deliverables, native acceptance
cases, resource budget and handoff. Earlier contracts are prerequisites; later
UI or benchmarks cannot replace missing runtime behavior.

## M14.9 - Environment contracts and compatibility reference laboratory

**Work:** Freeze environment identity, private storage/registry/component contracts, dependency records and versioned Windows reference probes.

**How and why:** One ownership model prevents conflicting assumptions in loaders, runtime activation and installer UX.

**Exit gate:** Schemas, ownership/escape matrix, reference provenance, migration policy and all-three-route walkthroughs are reviewed; no runtime feature is claimed.

[Detailed work, tests and handoff](m14-9.md).

## M14.10 - Private execution, files, registry and process ownership

**Work:** Implement native owner context, private loader/files/registry/object views and required x86 helpers for x64 products.

**How and why:** Enforce ownership at kernel/handle boundaries and preserve real Windows-visible semantics, errors and lifetime.

**Exit gate:** Native A/B private-copy/backing tests, inherited context, cross-owner rejection, delayed loading, mixed-architecture execution and cleanup pass.

[Detailed work, tests and handoff](m14-10.md).

## M14.11 - Private runtimes, services and dependency activation

**Work:** Execute private runtimes, COM/services/helpers and transitive dependency activation, including real .NET family/version behavior.

**How and why:** A private directory or registry version flag is not a working CLR or service; implement and test actual dependencies.

**Exit gate:** Original runtime/helper tasks activate correctly, late/optional failures are distinguished and two apps retain independent components and service state.

[Detailed work, tests and handoff](m14-11.md).

## M14.12 - Owner-bound installation, dependency setup and maintenance

**Work:** Provide general original installers, owner-bound dependency setup, private durable inventory and install/update/repair/recovery/removal.

**How and why:** All three user entry routes converge on one reviewed owner-bound transaction; ordinary standalone installation remains primary.

**Exit gate:** Original chains, explicit dependency target selection, nested/resumed setup, crash recovery and remove-A/run-B pass without a global dependency pool.

[Detailed work, tests and handoff](m14-12.md).

## M14.13 - Private app device access, driver ownership and acceleration

**Work:** Provide required driver/device contracts and real acceleration through native hardware mediation with attributable app contexts.

**How and why:** Private app-driver files do not automatically isolate kernel privilege; separate component ownership from physical resource arbitration.

**Exit gate:** Real device work and reset/fault/teardown pass on declared profiles; removing A cannot remove B components or native platform drivers.

[Detailed work, tests and handoff](m14-13.md).

## M14.14 - Desktop dependency workflows and original application interfaces

**Work:** Deliver automatic dependency assistance, right-click Add dependency and ordinary installer Advanced targeting with usable original interfaces.

**How and why:** Use evidence from native activation boundaries; optional searches and unknown failures must not generate compulsory installation prompts.

**Exit gate:** All three native flows, late requests, default/Advanced behavior, keyboard access, source/target confirmation and ordinary/HiDPI rendering pass.

[Detailed work, tests and handoff](m14-14.md).

## M14.15 - Independent app composition, broad compatibility and stability

**Work:** Validate broad original workloads, private A/B independence, version behavior, required integrations, stability and recovery.

**How and why:** Contract probes find causes; diverse original apps and repeated concurrent lifecycles verify composition without an app whitelist.

**Exit gate:** Original install/start/use/update/repair/remove tasks and fault/concurrency cases pass with physical ownership proof; necessary unresolved work stays explicit.

[Detailed work, tests and handoff](m14-15.md).

## M14.16 - Whole-system optimization and independent-bundle release

**Work:** Measure and optimize the whole system without cross-app dependency sharing, then qualify exact final release media and publication.

**How and why:** Optimize demand loading, bounded private caches and event-driven work; report duplicated disk/private RAM costs rather than hiding them through sharing.

**Exit gate:** Functional/resource budgets, independent copies, all-three-routes, A/B removal safety and exact source/media/download/website evidence agree.

[Detailed work, tests and handoff](m14-16.md).

## x86, Win16 and DOS

The directory/ownership/dependency/UI format is designed now for all these
families. Required x86 installers/helpers of x64 products are part of M14.10.
[M15](m15.md) expands standalone Windows x86 software. [M16](m16.md) expands
Win16 and DOS formats, execution modes, APIs, extenders and historical devices.
Their code is not implemented by planning or by a successful x64 test.
8/4/2/1-bit machines are not additional Windows application generations; other
historical architectures remain separate future decisions. Linux is deferred.

## Every-stage completion rule

Prove actual effects, errors, owner isolation, persistence, source integrity,
concurrency and cleanup. The mandatory A/B case installs independent copies,
does real work, updates/repairs/removes A, cold-starts B and verifies B's bytes,
private state and behavior. Include forged ownership, late activation, stale
targets, interrupted setup and physical-backing checks.

Measure CPU, private/peak/retained RAM, installed/temporary/rollback storage,
actual I/O and idle cost throughout. M14.16 repeats final integrated budgets
without forbidden sharing. A finite corpus is scoped evidence, not a universal
compatibility declaration; required unresolved behavior remains tracked work.

Update English architecture, progress, manuals, exact-source test evidence,
GitHub and actual website after each implemented stage. Preserve accepted
historical media and distinguish planning, implementation, native qualification
and full public delivery. An external website Save failure is not a successful
homepage update. Current authorization covers M14.9.

## Source contracts

- [Windows API index](https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-api-list)
- [Microsoft Win32 metadata](https://github.com/microsoft/win32metadata)
- [Windows protocols](https://learn.microsoft.com/en-us/openspecs/windows_protocols/)
- [Windows driver models](https://learn.microsoft.com/en-us/windows-hardware/drivers/wdf/differences-between-wdm-and-kmdf)
- [Detailed architecture and primary references](../architecture/windows-app-environments.md)

[Current status](../roadmap/status.md), [qualified M14.8](m14-8.md),
[program history](m14.md), [execution and measurement contract](../architecture/windows-m14.md).
