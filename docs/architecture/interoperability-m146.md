# M14.6 document and clipboard contract

Development design, not native qualification. Original AMD64 instructions continue in private native processes; no embedded Windows environment is introduced.

## Memory and clipboard ownership

Use the existing bounded process allocator for global-memory payloads. Movable handles require generation validation and real lock counts; fixed objects expose their allocation address. Keep GlobalAlloc ownership separate from LocalAlloc and ordinary heap pointers. Reject unsupported modes explicitly and preserve live data on failure. Transfer clipboard bytes through checked kernel copies; never expose a pointer from one private process to another.

The session broker must serialize OpenClipboard, preserve complete data until replacement succeeds, distinguish cancel/empty/error, release an open lock on owner teardown, and retain copied session data after the source process exits. Local clipboard handles become system-owned after successful SetClipboardData. Implemented text formats and conversions need exact byte tests, including invalid UTF-16, embedded terminators, maximum lengths and stale handles. Delayed rendering and unsupported object formats must not return fake success.

The desktop already owns an 8-KiB text clipboard. Bridge it through explicit bounded operations and ownership invalidation, rather than adding a polling synchronization loop or duplicating history. Native-to-Windows and Windows-to-native transfers require separate evidence.

## Foreign-window file picker

The existing native picker provides navigation, selection, replacement review and cancellation, but currently rejects requests while Windows work is active. Add a checked request/result channel associated with the requesting foreign window, process, thread and generation. Revalidate after callbacks and before completion. Owner destruction or process exit cancels the request and restores the desktop; another window cannot accept it.

Translate the qualified OPENFILENAMEW profile and native paths through the existing granted path model. Bound filters, titles, initial directories and output buffers. Return extended errors distinctly from user cancellation. Refuse unsupported hooks, templates and selection modes until implemented and tested. A Save dialog only selects a destination; application file writes and replacement safety remain real storage operations.

## Sources and qualification

- [Microsoft global/local memory contracts](https://learn.microsoft.com/en-us/windows/win32/memory/global-and-local-functions)
- [GlobalAlloc](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globalalloc), [GlobalLock](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-globallock)
- [Clipboard operations and ownership](https://learn.microsoft.com/en-us/windows/win32/dataxchg/clipboard-operations)
- [OPENFILENAMEW](https://learn.microsoft.com/en-us/windows/win32/api/commdlg/ns-commdlg-openfilenamew), [GetOpenFileNameW](https://learn.microsoft.com/en-us/windows/win32/api/commdlg/nf-commdlg-getopenfilenamew)

Owned ABI/lifetime tests support but do not replace original application journeys. Independently compare persistent file bytes after restart, and measure peak versus retained memory separately. The complete M14 corpus and M14.15 CPU/RAM/storage gate remain unchanged.

## First development slice

The initial global-memory implementation supports 128 live objects per process, generation-checked movable handles, fixed addresses, actual allocated sizes, lock counts up to 255, discarded zero-byte movable handles and explicit unsupported-mode refusal. Metadata is allocated lazily and released when its final object is freed; the underlying bounded process heap can reuse freed storage and is reclaimed on process teardown. It is not claimed to unmap every individual free.

GlobalAlloc fixed/movable and zero-initialization flags are implemented. Legacy DISCARDABLE/DDESHARE hints do not grant cross-process access. GlobalFree may free a locked object as Windows permits. LocalFree refuses these distinct global objects. GlobalReAlloc and clipboard-data ownership transfer are not implemented by this first slice.

Fifteen supporting host checks pass, including metadata/payload allocation failure rollback, stale handles, maximum generation refusal and full-size zero initialization. The owned Windows ABI fixture compiles; real native execution, thread concurrency and retained-memory checks remain pending on new STAGE6 media. Neither result is M14.6 acceptance.
