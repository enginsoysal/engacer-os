# M14.2 - Windows execution lifetime

Status: **implementation in progress, not release qualification**. M14.1 remains the public download. This contract describes required behavior and explicitly separates the initial implementation from remaining work.

## Ownership and scheduling

A Windows process owns its CR3, virtual reservations, module graph, file handles, writer and exit status. Threads share those process resources while owning separate integer/FPU contexts, a guarded stack, TEB, dynamic/static TLS and thread exit status. A process ending normally does not implicitly terminate a child process. A closed handle does not terminate its thread. Recycled slots require generation-bound handles.

Reuse the existing M3 timer clock, page allocator and protected transition conventions. The M3 demonstration scheduler has smaller, fixed address-space and IPC contracts; inserting Windows mappings into those fixtures would conflate independent ownership. Extend the existing protected Windows worker incrementally, keeping the desktop/kernel outside its address space. Initial thread execution is preemptive and serialized on the existing Windows worker CPU; this is concurrency, not Windows SMP qualification.

The first implementation bounds each process at sixteen thread records including the initial thread. Secondary stacks reserve a one-MiB address interval with a separate stride, start with four resident pages and grow through checked faults. Each TEB consumes two pages. Thread registers and 512-byte FPU states stay in fixed kernel records. The existing aggregate 128-MiB virtual and 10,000-page physical process limits remain. Limits refuse additional work rather than silently increasing memory.

## Blocking, locks and timers

An expected-value park syscall checks a process-owned user word before blocking. Wake changes matching waiters back to runnable. This check-and-block ordering prevents a wake arriving between a runtime test and its suspension from being lost. Finite sleeps and waits use the existing monotonic clock and a shared ownership lease on the existing PIT interrupt; the network and Windows paths cannot mask each other’s active lease. No finite Windows deadline means no Windows timer lease. The RTC-only development regression is preserved in the stage record. Infinite waits have a distinct sentinel. A process with no runnable Windows thread returns to the desktop loop. No user-mode periodic polling worker is introduced.

Runtime heap and loader data require recursive ownership locks before concurrent Windows APIs can be qualified. Dynamic TLS slot allocation is shared, values and last-error state are per thread. A new thread must not inherit the previous occupant's values. Event/semaphore mutation, wait-all consumption and handle close must be serialized; wait-all must not consume a subset. Thread and process termination must signal their retained waitable objects. Named-object references, stale-handle rejection, timer cancellation and resource reuse need independent tests.

## Normal and forced termination

Normal ExitProcess quiesces other threads, invokes attached DLL process-detach notifications in reverse attachment order, then asks the kernel to release process ownership. DLL mappings remain alive during every notification. The termination reserved argument is non-null, unlike FreeLibrary's null argument. Already detached modules, EXEs and no-entry DLLs do not receive an extra callback. Recursive cleanup cannot replay notifications.

Unhandled faults and forced cancellation bypass application cleanup and release kernel ownership directly. A callback fault must remain contained. A deadlock in application detach code remains cancellable; a fake successful cleanup would conceal an application failure.

## Static TLS and exception qualification gates

The current development static TLS implementation validates relocated PE templates, zero-fill, index pointers, callback arrays and executable callback targets. It bounds each module to 64 KiB of template plus zero-fill, one MiB in aggregate per thread, sixteen thread vectors, 32 module indexes and at most 63 callbacks followed by a terminator. Alignment above 4096 bytes is refused. These are explicit development-profile limits, not complete Windows coverage. The initial native EXE/imported-DLL/dynamic-DLL task corpus passes; full M14.2 lifetime and exception qualification remains pending. Each live thread must receive its independent template before original code runs. Serialize load/unload with thread start/exit and cover thread/process attach/detach, dynamically loaded modules and slot reuse. Preserve bounded module and aggregate memory quotas.

Implement x64 exception/context records, checked runtime-function/unwind metadata and the required unwind operations and handler dispositions. A fault dispatcher must validate continuation addresses, stack bounds and handler nesting; malformed metadata or unsupported operations end the protected process clearly. Host parser success is not native exception handling. Test handled access violations, stack unwinds, invalid handlers, callback faults and repeated cancellation in the guest.

## Acceptance before publication

Require exact-source native concurrency probes, original console-task regression, independent child-process lifetimes, TLS initialization/callbacks, waits/timers, handled/unhandled faults, cancellation and twenty repeated close cycles with resource accounting. Repeat real installation, retained-ISO and independent disk starts, constrained RAM and physical 4K, then the exact VMware starter package. CPU/I/O and fixed, peak and retained memory must remain separately reported.

Only after these checks pass may M14.2 replace M14.1 on GitHub downloads and the actual BrixCanvas homepage. Update English manuals, source links, site search/mobile/navigation, release assets and independent checksums together. No original GUI/browser compatibility is inferred from this stage.

Sources: [ExitProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-exitprocess), [wait-all semantics](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitformultipleobjects), [DllMain lifetime](https://learn.microsoft.com/en-us/windows/win32/dlls/dllmain), [x64 exception handling](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64), [PE format and TLS](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format).

## Last thread and child-process follow-up

The scoped native follow-up implements an atomic begin-exit decision before thread TLS cleanup. The final surviving thread must route through process termination while its own TLS is still available; freeing that TLS first would make process-detach callbacks unsafe. Loader notifications are serialized before quiescing other threads. A separate native last-thread fixture passes twenty repeated closes with zero retained managed pages; complete M14.2 qualification is still pending. [Planned child-process isolation and lazy metadata](children-m142.md) remains a design, not completed behavior.
