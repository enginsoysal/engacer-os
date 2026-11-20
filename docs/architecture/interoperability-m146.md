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

## Initial native result and next clipboard candidate

Initial frozen development build `da6cd42df3ae3393702bdfda06587e10`, bound to source `77a09674406ffcd57ad1961a9a5319e6d340d0bc` and 696 compiled inputs, passes compact installation/independent starts and the original MSI/console/archive/extract/removal/reinstall regression with all 106 payload hashes. Its owned global-memory fixture passes 21 lifetimes, each with 200 concurrent allocation/free rounds, zero retained managed pages and a subsequent original console execution. These are development results, not complete M14.6 acceptance.

The next candidate adds a checked clipboard broker and an explicit eager-text profile. It reuses the desktop's existing 8-KiB UTF-8 text buffer. Two separately allocated transient pages stage at most 8,192 bytes including NUL; UTF-8 validation spans their boundary without assuming physically contiguous allocation. Inputs are validated before commit. Open ownership is process/thread/window-bound and released on owner/thread teardown. Desktop copy/cut/paste checks exclusivity; a failed cut preserves its source.

This first publication profile accepts eager CF_UNICODETEXT. CF_TEXT/CF_OEMTEXT reads are synthesized under the runtime's declared UTF-8 ACP/OEM code pages. Other publication formats, delayed rendering, rich objects and CF_LOCALE remain unsupported. System-owned private handles are readable only while open, refuse caller freeing and expire on Close/Empty/replacement, while copied session text survives source exit. This follows the permitted handle-use lifetime and avoids retaining a private source buffer after Close.

Owner notifications currently use the checked native message queue. Full synchronous cross-process callback ordering and delayed-render callbacks are not established by that queued notification profile. Queue admission must refuse before clearing live data when a required notification cannot be admitted. The new native fixture exercises real private children, thread ownership/exit, exact Unicode and byte-text reads, invalid pointers/encodings, page boundaries, the quota and failure atomicity. The next candidate and original 7-Zip-to-native-editor task are not yet qualified. File-dialog integration remains open.


## Original clipboard input investigation

Development build `f809cac5ba9c53125aa021de2e88643d` passes the owned clipboard and global-memory lifetime groups, compact installation/startup and original MSI/console regression. The original 7-Zip copy task fails: the session clipboard remains empty. The failed report and screenshot are preserved; owned ABI success does not replace this original task.

The foreign keyboard bridge discarded control bytes such as Ctrl+C. The next candidate retains the pre-Control character and modifier snapshot in two bytes per queued key (512 bytes total for 256 entries), for both PS/2 and USB. The consumer scopes this metadata to ordinary keyboard dispatch. This distinguishes Ctrl+H/I/J from Backspace/Tab/Enter and avoids consulting a later physical modifier state. An owned native physical-chord fixture and the original copy task must pass on new frozen media before this correction is qualified. No clipboard history, background synchronization or polling is added. File-dialog work remains pending.


## Native UTF-8 document consistency

The next candidate extends the native document staging validator to strict UTF-8. A twelve-byte streaming decoder spans existing 4096-byte filesystem reads, rejects NUL/unsupported controls, overlong encodings, surrogate scalars, truncated sequences and values above U+10FFFF, and adds no document payload buffer. The existing CRC/source-identity and old-view-on-error guards remain. Editor left/right/backspace/delete operate on complete UTF-8 scalar boundaries; this is scalar movement, not full grapheme-cluster editing or an IME. The owned hosted staging regression passes all fourteen original guards with multibyte characters including a four-byte scalar across a storage-read boundary. Native reopen and editing remain pending on new media.


## First common-dialog candidate (not yet qualified)

The checked broker accepts classic Win64 OPENFILENAMEW sizes 136 and 152, a live caller-thread-owned window, one selected file, up to eight bounded UTF-8 labels/ASCII wildcard filters, granted initial directories, a bounded filename/title/default extension and the documented selected flags. Hooks, templates, custom filters, multiselection, ownerless requests, ANSI APIs and other flags remain explicitly refused. The implementation does not claim the newer Common Item Dialog COM interface.

One lazy request page binds copied inputs to process/thread/window/generation. Only the requesting context copies checked output buffers. A too-small file buffer receives the required UTF-16 unit count and FNERR_BUFFERTOOSMALL; cancellation leaves buffers unchanged and reports extended error zero. The modal loop dispatches messages in the private runtime and blocks on the existing scheduler, with a completion recheck before sleep. Teardown releases request ownership. No callback executes in the kernel.

The native picker restricts navigation/listing to granted roots, supports Unicode names, explicit cancellation and replacement review bound to the observed destination identity. Selecting Save never creates/truncates a file: the requesting app performs real writes after return. Native shared text fields preserve scalar boundaries and validate UTF-8 paste. The first owned fixture exercises exact open/read/save/replace bytes, a legacy-size structure, invalid structure/hook refusal, cancellation, extension/title offsets and short-buffer bounds. Syntax and compilation checks are development evidence only; native execution and original-app common-dialog tasks remain pending.


## Retained live-image envelope and build-only encoding improvement

The first complete common-dialog build was refused: its live ELF ended at 0x803988, crossing the unchanged 0x800000 boundary by 14,728 bytes. The qualified firmware owns ACPI NVS there; raising/removing this guard would be incorrect. No native test is attributed to that refused media.

The existing independent 4096-byte installer records retain their exact raw/zero/LZ4 wire format and unchanged bounded C decoder. The build encoder now compares its original greedy output with a search over at most eight earlier matches per four-byte key, within the same page, and retains the smaller result. No page grows relative to the previous encoder; no cross-page dictionary or guest allocation is added. The initial installed-kernel/EFI probe saves 33,600 encoded bytes. The unchanged C decoder corpus, including real candidate pages, truncations and 10,000 arbitrary malformed blocks, passes with guard bytes intact. Native install/recovery and actual final ELF placement remain separate gates. Moving embedded assets into another physical segment would require a broader loader/firmware layout change; this bounded encoding change preserves the current ownership envelope.


## Shared sections required by the original Add action (candidate)

The actual unmodified 7-Zip Add action fails at CreateFileMappingW. Its helper transfers filenames through a named shared section; a private buffer copy or returning a dummy handle would not implement that protocol. The next candidate adds committed RAM-backed sections, process-owned generation-checked grants and read/read-write views over the same physical pages. There is no nested OS, host IPC substitute or disk swap claim.

The first profile supports INVALID_HANDLE_VALUE sections with PAGE_READONLY/PAGE_READWRITE and optional SEC_COMMIT, up to sixteen objects of one MiB, sixty-four grants per process and sixteen views per process. Each object has one lazy metadata page and each participating process one lazy grant/view page. Backing pages are zeroed and physically committed before Create succeeds; this bounded eager implementation reports allocation failure at creation, without promising unbacked future commitment. Small filename transfers use one shared payload page. Further demand-backed commitment needs a real allocator reservation policy, rather than silently overcommitting.

Views retain backing independently of handles, closing a view requires its exact base, and process teardown releases its views/grants. Read-only aliases cannot escalate or execute, ordinary VirtualFree cannot discard a shared section, and default private allocations skip overlapping views. Mapping names share the implemented synchronization namespace and own-profile grant boundary; wrong object types refuse. File-backed sections, copy-on-write/executable/reserved/large-page sections, inherited handles and custom security descriptors remain unsupported. This does not establish a Windows ACL or multi-session security implementation.

Supporting hosted tests pass five deterministic allocation-failure positions, zero initialization, existing-name data retention, separate process grant metadata, handle/object quotas, stale generations, output-copy rollback and generation exhaustion. They do not establish native PTE sharing. The compiled native task adds real writer/faulting/source-exit helpers, actual shared bytes across page/64-KiB boundaries, protection changes, namespace collisions and lifetime limits; new media execution remains pending.

Sources: [CreateFileMappingW](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-createfilemappingw), [MapViewOfFile](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffile), [OpenFileMappingW](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-openfilemappingw), [UnmapViewOfFile](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-unmapviewoffile).


## Next original helper import candidate

After native shared-section qualification, the actual Add route maps the original installed 7zG.exe helper and refuses its unresolved lstrcatW import. The next candidate implements UTF-16 code-unit concatenation for valid caller-owned buffers, with the Windows return-pointer contract and explicit NULL refusal. As with the legacy Windows function, the caller must supply sufficient destination capacity; this is not a new safe-string API.

SetDlgItemTextA now converts under the declared UTF-8 ACP, delegates to the actual existing W control operation and keeps existing text when decoding fails. The owned control task verifies changed UTF-16 bytes, malformed input retention and clearing. Both changes still require new native media qualification. CreateFontIndirectW has a known static-import refusal diagnostic only, hidden from optional discovery. It is not implemented or counted as font compatibility; any actual call still fails clearly. This permits diagnosis of the original executed path without advertising a working unused import. The actual original task and visible accented glyph rendering remain open.

## Original large-dialog capacity candidate

The original 7zG.exe Add to Archive resource 4000 contains fifty controls. The prior thirty-one-control template bound refuses it before initialization; the original caller then throws CSystemException with E_ABORT (0x80004004). The new candidate supports 128 sparse shared window slots and 127 controls per template. Per-window state remains lazy; the static pointer table grows by 768 bytes. Top-level native roots remain limited to eight. Nesting is separately limited to 32 levels, retaining the existing compositor stack size and refusing deeper trees at admission instead of silently omitting their drawing. Owned native tests now exercise all 128 slots, refusal of the 129th, fresh recycled generations, recursive cleanup and the separate nesting bound. Historical dialog tests retain their assertions while their generated quota resources are adjusted to 128/127 controls and the observer explicitly validates the new pointer-table size. This is a candidate, not yet native qualification. C++ propagation remains unsupported and is not counted as completed by diagnosing this ordinary-dialog failure.

## Original Browse filter capacity candidate

The visible original Add dialog passes a 136-byte OPENFILENAMEW, supported 0x8000c flags and nine filters. The prior eight-filter bound rejects that actual request before native UI presentation; the original app subsequently attempts its error MessageBoxW. The candidate supports twelve bounded filters while retaining one lazy request page (the complete request remains below 4096 bytes), unchanged path grants and validation. The owned open task now uses nine filters and separately requires refusal of thirteen. This does not implement MessageBoxW or count the diagnosed failure as original common-dialog qualification.

Large-dialog native result: build `085d910fca4891c902f87ada7fff91f2` passes the owned 128-slot/recycled-handle/32-level nesting task, complete Unicode file-dialog task and retained modal callback/template/partial-creation rollback task, with zero retained pages after each. The original Add dialog is visibly initialized with 63 observed windows/controls. Blank combo presentation, accented glyph rendering, original Browse completion and complete archive behavior remain unqualified. The early observer stopped at an invisible title; its result is retained separately and the corrected observer requires visibility.
