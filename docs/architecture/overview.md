# Engacer OS architecture

The current native runtime stage is [M14.3](../releases/m143-v0.14.3.md). Engacer OS has its own loaders, kernel, installed desktop, Files, Settings, installer and bounded Windows x64 compatibility implementation. It is not a Linux distribution and does not embed a Windows VM. The original supported 7-Zip console/MSI tasks run through its own APIs. General Windows GUI, arbitrary installers, modern browser execution, Windows x86 and Win16/DOS remain later work. [Status](../roadmap/status.md), [current handbook](../handbook/index.md).

Each release binds its own source, media and named native tests. Older M0-M13 results explain established mechanisms; they do not automatically qualify new media. The M14.3 exact candidate separately qualifies native file/settings and runtime tasks, compact/ordinary/4K installation, independent startup and its exact VMware package. Complete public delivery is recorded separately from native acceptance.

## Layers

```text
Native desktop/apps        Selected original Windows x64 programs
         |                      CPU instructions execute directly
         |                      Own PE loader and Windows API runtime
         +----------------------+-------------------------------+
                       Engacer OS kernel and services
             native storage, input, networking, window ownership
             protected address spaces, threads, handles and faults
                                    |
                    Supported platform/controller drivers
                                    |
                                 Hardware
```

Linux ELF, Darwin/Mach-O, Windows x86 and Win16/DOS are extension targets, not implemented compatibility claims. A shared CPU architecture permits direct instructions; the expected ABI, APIs, object semantics and hardware protocols still need implementation. [Windows plan](../milestones/m14.md), [original architecture contracts](../roadmap/milestones.md).

## Kernel boundary

The modular native kernel owns address spaces, page permissions, scheduling, protected references, interrupt/DMA handling and checked transitions. The current desktop/installer and several native services remain kernel-resident. Describing a future user-service boundary must not imply that the entire desktop is already an isolated user process.

The Windows compatibility runtime runs in the protected program address space; kernel brokers own process/thread lifetimes, shared synchronization, protected path grants and fault capture. This keeps complex compatibility code separate from supervisor ownership while allowing bounded native transitions. Initial Windows scheduling is preemptive concurrency on one Windows worker CPU, not qualified Windows SMP. The older [M3 native SMP profile](../milestones/m3.md) is a separate baseline.

## Memory and isolation

Keep kernel text RX, constants RO/NX and data RW/NX. User images preserve their checked PE protections; stack guards and invalid user access faults remain contained. Each Windows process owns private CR3 state, heaps, module mappings, writer and TLS. Threads share process resources and own their TEB, guarded stack and integer/FPU context.

M14.3 retains the bound of four live Windows processes and sixteen threads per process. Existing process admission limits include 10,000 owned physical pages, 128 MiB virtual reservations, 32 modules and a 32-MiB image limit. Metadata and exception stacks allocate lazily. Root metadata maps 28 pages; child slabs include private output and map 32. Shared object data pages allocate only while needed and return when unused. These are component/ownership bounds, not total OS RAM. [Runtime](runtime-m142.md), [children](children-m142.md), [resource measurements](../../evidence/M14/3/resources.json).

File/image reservation, resident ownership, peak use and retained memory are measured separately. Broad file-backed paging, compression and swap must not be inferred from the selected demand-backed Windows allocation mechanisms. Configured guest RAM is not measured kernel consumption. M14.15 is the blocking whole-system CPU/RAM/storage optimization gate.

## Execution environments

The loader assigns the native or selected Windows execution profile. Windows PE relocation/import/DLL/TLS processing uses Engacer OS code, and the program's instructions execute in its protected address space. M14.2 supplies real CreateProcess/threads, independent TLS and selected hardware-fault/C structured exception behavior. Unimplemented Windows services must fail clearly. [Loader contract](loader-m141.md), [runtime](runtime-m142.md), [exception boundaries](exceptions-m142.md).

Kernel-owned generation-checked grants keep a recycled slot from becoming an unrelated valid handle. Atomic mixed waits cover supported processes, threads, events, semaphores and timers. Finite deadlines share an interrupt lease; indefinite blocked tasks need no Windows polling timer. The desktop returns to halt when no runnable work remains. [Synchronization and limits](synchronization-m142.md).

## Files, namespaces and identity

The native root is `/System`, `/Applications`, `/Users`, `/Data`, `/Cache`, `/Logs`, `/Temporary`, `/Volumes`; there are no mandatory native drive letters or `/var`. Windows paths are translated through the implemented profile and explicit authorized roots, rather than treating a string alias as authorization. Personal documents remain separate from owned product files. [Filesystem contract](filesystem.md), [original Windows runtime baseline](windows-runtime-m8.md).

Native persistent storage, installer ownership and selected removable-file operations are implemented. M14.3 qualifies bounded Unicode paths/search, generation-checked shared file grants, existing-file edits, synchronous byte locks, persistent user registry values and copied environments. User file timestamps/attributes survive app removal and independent startup. These are selected profiles, not complete Windows filesystem, network namespace, NTFS/ACL or registry semantics. [Implementation and limits](files-m143.md). Product removal preserves personal documents and modified files under the documented supported MSI profile; arbitrary MSI behavior remains later work.

## Boot and recovery

Original BIOS and UEFI loaders normalize firmware information and enter the native kernel. UEFI boot services end before kernel operation. The exact M14.3 VMware package uses x64 UEFI, Secure Boot disabled, a blank growable 20-GiB SATA disk and the matching ISO. It installs, restarts with the ISO retained and starts twice independently without the ISO. [Installation](../handbook/install-m143.md), [storage instructions](../handbook/vmware-storage.md).

Historical BIOS/controller/trust tests keep their named scopes. Normal public media remain unsigned; an earlier owner-enrolled trust experiment does not establish factory Secure Boot support. Installed persistence and implemented same-build boot repair/update-slot/rollback controls are distinct from unqualified cross-release migration or a universal power-loss guarantee.

## Graphics and hardware

Discover bus/protocol identity, bind an implemented driver, initialize it and expose actual capabilities. A device class or VRAM size alone cannot supply a GPU's command protocol. Current rendering uses bounded CPU/framebuffer presentation and implemented virtual display/input integration. Modern vendor GPU 3D and universal hardware compatibility are not qualified. [Graphics baseline](graphics-m9.md), [hardware contract](hardware-m10.md).

The current exact VMware starter is separately tested with its shipped devices enabled. Earlier integration/controller matrices remain historical, not automatic proof for every new ISO. Physical hardware, ARM/Pi and broader vendor protocols require their own implementation and qualification.

## Evidence and change control

Cross-compile without a host CRT. Preserve build IDs, exact Git input bytes, artifact hashes, failed observations and sanitized native logs. Native test fixtures are distinct from original unmodified applications and host-only parser tests. Real user tasks, independent boots, fault containment, cancellation and repeated ownership cleanup remain separate checks. [M14.2 native acceptance](../../evidence/M14/2/acceptance-results.json), [scope](../releases/m142-v0.14.2.md).

## M4.5 firmware increment

The historical BIOS EDD/E820/VBE and UEFI paths normalize their handoff to the same kernel contract. Their original reservation/trust observations remain bound to the older named media. [Boot design and evidence](../milestones/m4.5-boot.md), [storage/trust boundaries](../milestones/m4.5-storage.md).

## M4.5 USB topology and transport

Historical USB hub/HID/storage topology, generation-bound reconnect and bounded read-only UAS work remain documented under their original scope. They do not establish every current removable-device or controller combination. [Original USB contract](../milestones/m4.5-usb-topology.md), [current Files/USB use](../handbook/files-m137.md).

## Guided interaction and distribution identity

Readable graphics, explicit disk selection/consent, optional diagnostics and independently removable apps are product requirements. Validated schema-3 recipes select supported identity, appearance, optional apps and data packages; they cannot disable protected ownership or add unimplemented drivers/APIs. Changed media require independent qualification. [Distribution recipe](../handbook/distributions.md), [product principles](product-principles.md).

## Current product delivery order

Finish each M14 stage's native tests, English documentation, GitHub assets and actual complete website verification before the next stage. M14.3 qualifies the selected files/settings profile; later stages add Windows GUI and broader runtime/installer services. M14.15 blocks the final x64 release on optimization. M15 covers Windows x86; M16 covers Win16/DOS. Linux/macOS and broader hardware remain extensions. Earlier release names, tags and accepted evidence remain immutable.
