# M14.2 - Child-process ownership design

Status: **child-process design; its lazy kernel metadata foundation passes scoped root-task native checks, but child-process compatibility is not delivered yet**. Native threads, synchronization and static TLS have separate scoped development evidence. M14.2 remains incomplete.

## Native execution and address spaces

A child must get its own CR3, runtime data, heap, PE module graph, thread list, TEB/TLS and file/writer state. It executes AMD64 instructions directly through the same protected runtime entry path. An embedded Windows VM, second operating system or host application execution is not an implementation route.

Keep four simultaneous process address spaces and sixteen threads per process as an explicit first profile. Process-local page ownership and the existing 128-MiB virtual/10,000-page physical limits remain independent, while allocation can still fail against actual guest RAM. A 128-MiB guest does not promise that four maximum-size processes fit.

## Lazy kernel metadata

Duplicating the current large static ownership tables four times would increase idle kernel reservations and pressure the boot image's bounded address layout. The first implemented step allocates a bounded kernel-only metadata slab for the current root task; the next step extends this to child address spaces. Reserve up to 192 KiB per process in four separate strides within the existing shared upper-half kernel page-table window, starting one MiB above KERNEL_STACK. Existing AP, emergency, native-app and Windows trap stacks remain below that window. Validate empty page-table slots and enforce the slab size at compile time; map only supervisor read/write, non-executable pages.

Store the slab backing-page list outside the slab so teardown can unmap/free it without reading already freed memory. Finish status/object updates and file/rollback cleanup before releasing the slab. Return all slab pages at process close. Report their memory separately and include them in total process-related peak accounting. Keep the existing root UI information object stable so native desktop observers and user-facing progress retain their owner.

This uses the existing allocator and shared supervisor kernel branch. It avoids an unbounded kernel heap, a large permanent table matrix and copying native process demo address layouts into the Windows runtime.

## Process and handle lifetime

A compact retained process object is separate from the live address space. A process handle can remain signaled and expose its real exit code after address-space pages have been freed. A primary-thread handle can become signaled while another thread keeps that process alive. Bound retained process objects and per-process handle grants, use generation-checked handles and reject stale/foreign handles.

CreateProcess returns separate process/thread handles and process/thread IDs. The selected first profile inherits only the parent's existing application/user path grants, defaults to the parent's working directory and preserves the supplied command line. Unsupported explicit environment/security/handle-inheritance features must refuse clearly instead of being ignored. Suspended creation does not execute a callback or entry point before ResumeThread.

Exiting or faulting a parent does not implicitly terminate its children. An explicit user cancellation of the foreground task group may cancel its descendants; document this UI ownership action separately from natural process exit. Kernel scheduling must continue an orphaned child after the root UI task finishes. Releasing one process must never clear another process's ownership tables, output, timer lease or writer.

## Scheduling, waits and output

Select runnable processes and then their runnable threads fairly, preserving per-thread integer/FPU state and private CR3 mappings. Aggregate finite deadlines across all live processes when acquiring the shared PIT lease. No runnable Windows context means return to the normal desktop halt path.

Process and primary-thread completion wake waiters to recheck their actual object state. Wait success means signaled lifetime state, independently of whether the application exit code is zero or nonzero. Preserve real exit codes, including faults. A child failure must not be mistaken for a root failure by the UI or test observer.

The initial console profile shares the root task's bounded output surface. Preserve individual status and lifetime even when output is combined. Pipes, inherited arbitrary handles and general desktop multi-root integration require their own implemented contracts; do not silently approximate them.

## Required native evidence

Run concurrent unmodified original console tasks together with isolation probes. Check distinct IDs, suspended start, parent/child waits, primary-thread versus process exit, nonzero exit codes, stale/closed handle rejection, parent exit with a surviving child, child faults contained from the parent/desktop, explicit group cancellation and repeated process-slot reuse. Verify actual files/output and zero unexplained retained managed pages after twenty closes. Repeat ordinary installation and independent startup on the final frozen media.

Sources: [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw), [process termination and child lifetime](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-exitprocess), [ExitThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-exitthread).
