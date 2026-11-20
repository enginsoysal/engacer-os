# M14.5 native memory-protection follow-up

Frozen development `06c8de63a527c32ad9ec73f4b9e333bc`, built from `da8a1c143da73f3716d838548bb51549ebfa7f46`, passes 21 native protection lifetimes, eight real access faults per lifetime, zero retained pages and a subsequent original console execution. Both original Notepad++ and SumatraPDF pass their previous VirtualProtect startup calls and now stop at FlsAlloc. Neither app has a qualified interface yet; the complete native M14.5 regression now passes, with public delivery being finalized.

## How and why

Translate supported Windows protections to real process-private PTE rights. The initial profile supports read-only, read/write and execute/read, retaining the existing write-xor-execute policy. No-access, guard, copy-on-write, execute-only and writable/executable modes fail explicitly. Returning success without changing hardware rights would be incorrect.

The wrapper rounds the actual touched pages, verifies an entire single live VirtualAlloc allocation or loaded image, and rejects overflow, cross-allocation ranges, unmapped pages and invalid outputs. Virtual allocation state has a process-local recursive lock; loaded images remain locked across the kernel operation to prevent unload races. The existing VirtualAlloc commit/release subset is retained; reserve-only/decommit and general managed-heap protection are not added implicitly.

The kernel first checks every mapped or demand-backed page, then writes the old first-page protection through the checked user-copy path, then updates PTEs and invalidates each affected TLB entry. Invalid ranges/outputs do not partially change protections. Demand-backed image pages are logically committed Windows image memory; changing protection does not allocate physical backing unless the output itself needs a page. No periodic worker, surface or new per-page side table is introduced.

The owned native fixture checks unaligned rounding, a boundary crossing, the actual old rights, real write faults/resumption, unchanged bytes, failed cross-allocation and invalid-output atomicity, unsupported RWX refusal, RW-to-RX execution of owned instructions, restoration, release and repeated cleanup. It does not execute original apps on the host or qualify them through synthetic results.

[Microsoft VirtualProtect contract](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect). Full Windows virtual-memory semantics and universal Windows application compatibility remain unqualified.

The next original-runtime dependency is [tracked separately](../roadmap/runtime-followups-m14.md), retaining both mandatory targets and the full M14.12 task gate.
