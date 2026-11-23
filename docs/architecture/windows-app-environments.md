# Independent Windows app environments

Status: owner-approved design, 23 November 2026. Implementation is planned,
not started. M14.8 media and accepted evidence remain unchanged. This contract
supersedes future cross-application dependency-sharing proposals. The current
authorization is to revise and publish plans only.

## Product rule and scope

One application owns one self-contained directory and its complete installed
dependency tree. Two applications needing identical DLLs, runtimes or helper
programs receive two independently owned physical copies. Removing, repairing
or updating A must not change B's installed components or private state.

Apply this packaging and management model to Windows x64, x86, Win16 and DOS.
Their execution contracts differ; a folder does not implement an ABI, CPU
instruction set, CLR, DOS extender or device model. Windows is the current
focus; Linux, macOS and other historic machine architectures remain deferred.
No nested Windows guest is introduced for x64/x86 execution. Any emulation
needed for historical execution is identified and measured explicitly.

The common foundation is the Engacer kernel and its native hardware/resource
management. App-owned Windows compatibility modules, DLLs, runtime packages,
framework stores and helper programs must not become a hidden shared app
dependency pool. Identify this boundary before implementation. Common kernel
operations do not authorize one app to consume another app's installed files.

## Physical ownership and logical layout

Illustrative layout, to be frozen as a versioned format in M14.9:

~~~text
/Applications/Windows/<AppId>/
    Program/                       original program and private program files
    Dependencies/<ComponentId>/     private runtime/helper installations
    System/                        private Windows-visible system components
    Registry/                      private machine/class and per-user stores
    Profiles/<UserId>/             private settings, cache and temporary data
    .Engacer/                      protected manifest, ownership and transactions
~~~

All installed app-specific executable components and durable app state belong
under this root. The original installer may see C:\Program Files, Windows,
System32, SysWOW64, ProgramData or AppData; the environment maps those logical
names to its own owned locations without rewriting vendor program bodies.
Mappings must preserve architecture, permissions, identity, locking and errors.

Use a stable AppId independent of display name and current pathname. Kernel
ownership is authoritative; a writable manifest, environment variable, path
string or foreground-window guess cannot grant a different owner's access.
Protect .Engacer metadata from ordinary app processes. Keep only minimal,
rebuildable app/launcher/location references in the OS control-plane index,
not an external app registry hive, dependency store or required runtime cache.

An explicit user-selected document or device can be accessed through a checked
OS grant. Personal documents are not dependencies and remain outside the
application directory by default. Uninstall preserves them. Private settings
may be retained or erased through an explicit choice, without moving runtime
dependencies into another app. Multiuser state remains separated inside the
bundle, subject to actual filesystem permissions and the owning user's rights.

Prohibit cross-app hard links, reflinks, content-addressed dependency stores,
dependency-file deduplication, app-code page coalescing and cross-AppId module
cache hits as Engacer-managed optimizations. Copies with identical hashes still
have separate app ownership and backing. Processes belonging to the same AppId
may use their own environment's components; this is not cross-app dependency
sharing. Do not turn the download folder into a required runtime dependency.

## Registry, objects and component identity

Each app receives its own Windows-visible registry, including appropriate
machine, user, class/COM and architecture views. No global writable Windows
registry is the application dependency authority. Queries for real OS/user/
device facts use explicit native interfaces or controlled projections into
the app view; they do not expose another app's registrations.

Scope loader lookup, assembly/GAC views, COM registration, service names,
named synchronization, local IPC endpoints, runtime discovery, PATH, temporary
paths and child-process state by AppId plus user/architecture where required.
The Windows-visible name may be identical in A and B while ownership remains
distinct. Broker external workflows and hardware explicitly; never solve a
missing dependency by silently attaching to B's service or loading B's DLL.

Logical HKLM writes inside an app are not host administrator or kernel rights.
Registry isolation must cover x64 processes, services and helpers as well as
interactive x86 processes. Windows UAC registry virtualization is a reference
behavior to investigate, not a sufficient implementation of this contract.

## Dependency graph and installation context

Represent dependencies by identity, architecture, supported version constraints,
ABI/runtime family, required feature, source provenance and actual installation
state. Record recursively required components and detect cycles or unresolved
version conflicts before unbounded recursive installation. An installed desktop
App B does not satisfy an App A dependency; A receives its own installed copy.

States distinguish unknown, declared, requested, missing, installing, installed,
verified, incompatible and failed. A file existing or a setup process returning
zero is not proof that the runtime can activate or the app can use it. Preserve
the original failing request and add a real verification task.

Attach an immutable kernel-controlled owner/context to the main installer and
its children, elevated brokers, services and restart/resume operations. A
download or a long delay cannot lose that ownership. A ticket must bind the
target AppId, selected operation, reviewed source, authority and transaction;
stale tickets, removed targets and recycled IDs cannot retarget an installation.

Separate app context from privilege. An installer can be allowed to populate
its own virtual Windows directories without receiving unrestricted physical
disk, kernel, foreign-bundle or user-document access.

## Exactly three user entry routes

1. Automatic assistance: a confidently identified necessary failure is attached
   to the actual requesting app. Explain the component and offer Add component
   or Select installer, with target, source, disk cost and consent visible.
2. Right-click the app and choose Add dependency. The app is selected first;
   the user then selects an installer or a supported dependency source.
3. Open an installer normally. The primary action remains ordinary standalone
   installation into a new app environment. A collapsed Advanced section offers
   Install as dependency for an existing app, followed by explicit app selection.

All three converge on one reviewed, owner-bound installation transaction.
Dependency classification or a recent app failure must never silently replace
the ordinary installer's primary action. Unknown installers can still be
explicitly assigned through route 2 or Advanced. Recent requests are suggestions
inside the relevant workflow, not permission or proof of ownership.

An installer launched through an already explicit Add dependency action stays
in the selected environment; its nested installers must not ask the user to
repeat the target selection. Directly opening an unrelated downloaded installer
remains ordinary installation until the user selects Advanced.

## Detection without a permanent scanner

Use import/manifest/configuration inspection and the existing loader, CLR,
COM, service and helper activation boundaries. Record terminal unresolved
requests at the point of failure, including AppId, process/user/architecture,
requested identity/version, searched locations, error, feature and evidence.
Do not poll every running process or continuously scan the disk.

An app may start successfully and request a runtime later. Static imports alone
cannot discover this closure. Classify optional probes separately from required
activation failures; a failed first lookup followed by a successful later search
must not trigger dependency installation. Preserve original API return/error
behavior rather than swallowing faults or retrying unsafe instruction state.

When evidence is insufficient, offer diagnostics and the manual routes instead
of asserting that a particular package is missing. An app's own text-only error,
online entitlement failure, damaged file, access denial or unsupported OS API
must not automatically be labelled a missing dependency. Never automatically
download or execute an arbitrary DLL found through a web search.

## Runtime and maintenance behavior

.NET Framework and modern .NET are separate runtime families. Plan actual
activation, configuration, assembly binding, architecture and operating-system
dependencies; copying a framework directory is not runtime implementation.
Install its own prerequisites inside the same app's dependency graph. Preserve
version and servicing behavior without relying on a global framework store.

Use per-app user-service instances and owner-bound helpers. Start on demand
where semantics permit; required authorized background services may remain
active after the app window closes. Do not launch every installed runtime or
service at boot. Service activation through the OS broker retains AppId.

Stage install/update/repair inside the owning root, with bounded journals and
recoverable publication. Preflight temporary/rollback disk requirements, active
processes and graph constraints. An update to A's runtime never updates B.
Uninstall stops A's owned execution safely, removes only A's integrations and
bundle, and proves B still works. Raw folder deletion is detected and stale
index references are reconciled without following external links or deleting
other apps. Copying/moving a bundle does not guarantee transferable licences,
hardware binding or vendor online access.

A driver binary may belong to the private app package, but executing it with
kernel privilege does not automatically make it isolated. Physical GPU/network/
audio/storage management remains native OS responsibility. M14.13 must define
driver-instance ownership, mediation, privilege and teardown; it may not bypass
the policy by installing a shared vendor app driver globally. Necessary gaps
remain tracked compatibility work, not fake successful installation.

## Migration and evidence

Existing M14.8 ownership records and global compatibility state are historical
implementation, not proof of this future environment contract. Inventory their
provenance; retain immutable release tests/media. Migrate only attributable
state transactionally or reinstall the original source into a new environment.
Do not guess which app owns ambiguous legacy keys or mutate another user's data.

Every implementation stage must include a two-app independence check: install A
and B with identical dependency names, perform real app work, update/repair/
remove A, cold-start B and verify both B's bytes/state and its actual behavior.
Include concurrent use, late dependency requests, restart and failure recovery.
Tests must inspect physical ownership/backing, not just different displayed paths.

Measure duplicate installed bytes, upgrade peak disk space, private code/data
RAM, total OS cost, CPU, latency, block requests/bytes/flushes and event-driven
idle behavior. Do not reduce these numbers through forbidden cross-app sharing.
No claim of universal compatibility follows from a finite successful corpus.

## Milestone allocation

M14.9 freezes contracts and the reference laboratory; M14.10 implements execution
and isolation; M14.11 implements private runtimes/services; M14.12 implements the
owner-bound package lifecycle; M14.13 mediates devices; M14.14 delivers the three
user routes; M14.15 validates composition and stability; M14.16 measures and
optimizes the complete system without dependency sharing. M15 expands standalone
x86 apps and M16 Win16/DOS using this same management contract.

## Primary references and interpretation

These references describe Windows-visible behavior, not an existing Engacer
feature or an App-V implementation being imported:

- [DLL search order](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order)
- [Assembly search and activation contexts](https://learn.microsoft.com/en-us/windows/win32/sbscs/assembly-searching-sequence)
- [.NET Framework runtime selection](https://learn.microsoft.com/en-us/dotnet/framework/configure-apps/file-schema/startup/supportedruntime-element)
- [Registry virtualization and its limited scope](https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-virtualization)
- [App-V environment concepts](https://learn.microsoft.com/en-us/previous-versions/windows/microsoft-desktop-optimization-pack/appv-v4/about-virtual-environments)

Our selected design is stricter on cross-app dependency ownership than the
shared/global-store mechanisms in those references.

[Ordered implementation plan](../milestones/m14-consolidated.md),
[x86 expansion](../milestones/m15.md), [Win16/DOS expansion](../milestones/m16.md).
