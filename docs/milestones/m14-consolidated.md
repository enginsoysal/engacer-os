# M14.9-M14.16 - Approved consolidated Windows x64 program

Approved by the owner on 21 November 2026. All eight stages are **planned, not
started**. This replaces the former future M14.9-M14.15 schedule and the longer
intermediate proposals. M14.0-M14.7 retain their scoped evidence. M14.8 native qualification now passes; native homepage publication remains
blocked as recorded in current status. Current authorization ends after M14.8.
Do not start M14.9 implementation until the owner resumes work.

## Product scope and architecture

The product target is the complete original x64 Windows application landscape
for Windows 7, 8, 8.1, 10 and 11, including necessary installation programs,
mixed-architecture helpers, runtimes, services and drivers. Named applications
are regression fixtures, not the scope or an application whitelist. No complete
application list is required from the owner.

Original instructions execute natively through the independent Engacer kernel
and compatibility environment. The implementation is not an embedded Windows
guest. Preserve Windows-visible binary contracts and behavior at explicit
boundaries; internal scheduling, storage and resource management remain our own.

Inventory contracts, compare behavior with reference Windows versions and
discover dependencies continuously. A matching function name, metadata signature
or finite passing app corpus is not proof of universal compatibility. Newly
discovered necessary functionality becomes tracked work in its owning subsystem;
it cannot be silently excluded from scope or reported as successful execution.

## M14.9 - Compatibility architecture and reference laboratory

**Deliver:** A version-bound inventory of APIs, ABIs, system calls, component and
driver interfaces, formats and protocols; a dependency graph and missing-behavior
register; automated differential tests against Windows 7/8/8.1/10/11.

**How and why:** Use primary documentation and SDK/WDK metadata to inventory
interfaces. Run owned probes to compare results, side effects, errors, ordering,
lifetime and concurrency. Signatures alone do not specify behavior.

**Acceptance:** Reproducible reference/native mismatches, provenance and baseline
versions are recorded. Known requirements have an implementation owner and test
or explicit investigation task. The reference lab operates independently of
specific commercial app success.

## M14.10 - Complete execution foundation

**Deliver:** Required loader, DLL, NT object, process, memory, thread, exception,
file, registry, identity and access-control behavior. Include necessary x86
installers/helpers of x64 products instead of deferring those dependencies to M15.

**How and why:** Translate Windows-visible contracts into own kernel operations,
preserving binary layouts, results, errors, lifetime and security semantics.

**Acceptance:** Real effects, faults, concurrent execution, mixed-architecture
transitions and resource cleanup pass reference and native tests. Unimplemented
operations never become successful no-ops.

## M14.11 - Windows platform services

**Deliver:** Required services, IPC/RPC, COM/OLE/WinRT, native/managed runtimes,
command/script environments, data interfaces, network, cryptography and
authentication.

**How and why:** Build shared providers and actual component/service lifetimes.
Resolve dependencies of original runtimes and helpers instead of substituting
product-specific effects.

**Acceptance:** Components execute and communicate, errors propagate, appropriate
state survives restart, and peak/retained resources remain bounded.

## M14.12 - General installation and maintenance

**Deliver:** MSI/MSP, EXE bootstrappers, MSIX/AppX, prerequisites, custom actions,
updates, repair, rollback, restart/resume and removal.

**How and why:** Provide general package and execution semantics. An application
name/digest allowlist is not the compatibility architecture. Source integrity,
explicit consent and authorization checks remain mandatory.

**Acceptance:** Original installation and maintenance chains run including
helpers/services. Independently verify files, registry, shared ownership, user
data and interrupted-operation recovery.

## M14.13 - Hardware drivers and acceleration

**Deliver:** Required Windows driver contracts, device stacks, GPU graphics and
compute, multimedia, input and virtualization facilities over Engacer hardware
management.

**How and why:** Implement actual operations and necessary binary/kernel
structures, requests, synchronization and device lifetimes. Discovery is not
functional acceleration.

**Acceptance:** Original callers perform actual device/render/media/virtualization
tasks on declared hardware profiles. Preserve device-specific results and
peak/retained resource measurements.

## M14.14 - Application interfaces and desktop integration

**Deliver:** Windows, controls, text, fonts, DPI, accessibility, international
input, clipboard, printing, shortcuts, associations and shell integration.

**How and why:** Keep the Engacer desktop while honoring original callbacks,
message ordering, owner identities and visible effects.

**Acceptance:** Original interfaces are readable and usable. Ordinary launch,
open/save/close, integration and actual ordinary/HiDPI physical rendering pass.

## M14.15 - Broad compatibility and stability

**Deliver:** Windows-version behavior, historical quirks, external platform
integrations, broad original-app campaigns, long-duration/concurrent execution,
fault injection and recovery.

**How and why:** Contract tests provide the foundation; diverse original software
checks composition. New dependencies feed back to their owning subsystems.
Necessary external service or vendor-trust integration remains explicit work,
not a fabricated success or an exception removed from the product scope.

**Acceptance:** Preserve reproducible failures and actual install/start/use/update/
remove outcomes, resource observations and resolutions. A finite corpus is
scoped evidence, not an automatic universal-compatibility declaration.

## M14.16 - Whole-system optimization and release qualification

**Deliver:** Optimize CPU, peak/retained RAM, latency, storage bytes/requests/
flushes and idle behavior. Repeat full regression on exact frozen media and
publish matching ISO/VMware artifacts, documentation and actual website content.

**How and why:** Efficiency is measured throughout every stage. This is the final
integrated optimization round, replacing the former M14.15 optimization gate.
Correctness, user data and readable interfaces cannot be traded for benchmarks.

**Acceptance:** Exact source/media bindings, functional/performance evidence,
hardware profiles, independently downloaded assets and fresh website readback
agree. Unresolved required functionality remains open; a release number does
not establish universal compatibility.

## Every-stage closure

Test actual effects, errors, isolation, persistence, concurrency and cleanup.
Measure CPU, peak/retained RAM, I/O and idle costs during implementation. Update
English architecture, user guides, status, GitHub source/evidence and the actual
website after every milestone. Preserve accepted historical artifacts. Never
promote a development image or private diagnostic route to qualified release.

The initial pinned originals remain regression fixtures and provenance records.
M15 remains standalone x86 expansion; required x86 dependencies of x64 products
are already included in M14.10. M16 remains Win16/DOS.

## Primary research sources

- [Windows API index](https://learn.microsoft.com/en-us/windows/win32/apiindex/windows-api-list)
- [Microsoft Win32 metadata](https://github.com/microsoft/win32metadata)
- [Windows protocols](https://learn.microsoft.com/en-us/openspecs/windows_protocols/)
- [WDM and WDF](https://learn.microsoft.com/en-us/windows-hardware/drivers/wdf/differences-between-wdm-and-kmdf)
- [Version-dependent application behavior](https://learn.microsoft.com/en-us/windows/compatibility/application-executable-manifest)

[Current status](../roadmap/status.md), [current M14.8 work](m14-8.md),
[program history](m14.md), [architecture](../architecture/windows-m14.md).
