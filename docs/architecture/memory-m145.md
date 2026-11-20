# M14.5 native memory-protection follow-up

In development, not yet native-qualified. Original Notepad++ and SumatraPDF both reach actual `VirtualProtect` calls with `PAGE_READONLY` for a 256-byte data block. The original caller/IAT diagnosis and hashes are preserved in development evidence; neither app has a qualified interface yet.

## How and why

Translate supported Windows protections to real process-private PTE rights. The initial profile supports read-only, read/write and execute/read, retaining the existing write-xor-execute policy. No-access, guard, copy-on-write, execute-only and writable/executable modes fail explicitly. Returning success without changing hardware rights would be incorrect.

The wrapper rounds the actual touched pages, verifies an entire single live VirtualAlloc allocation or loaded image, and rejects overflow, cross-allocation ranges, unmapped pages and invalid outputs. Virtual allocation state has a process-local recursive lock; loaded images remain locked across the kernel operation to prevent unload races. The existing VirtualAlloc commit/release subset is retained; reserve-only/decommit and general managed-heap protection are not added implicitly.

The kernel first checks every mapped or demand-backed page, then writes the old first-page protection through the checked user-copy path, then updates PTEs and invalidates each affected TLB entry. Invalid ranges/outputs do not partially change protections. Demand-backed image pages are logically committed Windows image memory; changing protection does not allocate physical backing unless the output itself needs a page. No periodic worker, surface or new per-page side table is introduced.

The owned native fixture must check unaligned rounding, a boundary crossing, the actual old rights, real write faults/resumption, unchanged bytes, failed cross-allocation and invalid-output atomicity, unsupported RWX refusal, RW-to-RX execution of owned instructions, restoration, release and repeated cleanup. It does not execute original apps on the host or qualify them through synthetic results.

[Microsoft VirtualProtect contract](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect). Full Windows virtual-memory semantics and universal Windows application compatibility remain unqualified.
