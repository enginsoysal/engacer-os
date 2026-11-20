# M14.5 list-view input development

This implementation is under native qualification. Original application
navigation and complete M14.5 acceptance remain open.

Plain pointer input selects/focuses the actual application-owned row. A
single click does not activate it. Double-click and Enter send the documented
activation notifications to the original parent procedure; no native Files
listing or fabricated application command substitutes for those callbacks.
The initial profile covers ordinary report/list input, not complete modifier,
drag/drop, owner-data, grouped or icon-grid behavior.

Selection changes preflight LVN_ITEMCHANGING and respect a veto. A bounded,
temporary vector contains only the rows whose states actually change, up to
the existing 2,048-row limit. State commits precede LVN_ITEMCHANGED callbacks.
The original row model has a revision counter: if a callback destroys the HWND
or replaces/mutates its model, the outer operation stops before touching old
rows or sending stale activation. Equal row counts do not establish identity.
Reentrant input depth is bounded to eight; temporary vectors are freed on
every callback/veto/teardown path. Identical state assignments do not count as
mutations. Keyboard selection scrolls within the current native viewport.

Notification layout is a compatibility requirement. NMITEMACTIVATE is 72 bytes
on x64. NMLVKEYDOWN is explicitly packed: the virtual key starts at byte 24,
flags at byte 26 and the total size is 30 bytes. These follow the published
[control declarations](https://github.com/microsoft/win32metadata/blob/main/generation/WinSDK/RecompiledIdlHeaders/um/CommCtrl.h),
not an assumption that every notification has default member alignment.
[Selection veto](https://learn.microsoft.com/en-us/windows/win32/controls/lvn-itemchanging)
and [double-click](https://learn.microsoft.com/en-us/windows/win32/controls/nm-dblclk-list-view)
behavior have separate native checks.

## Corrected column-order identifiers

Review found that both the earlier runtime and its owned M14.4 fixture used
incorrect column-order message constants. The published identifiers are
SETCOLUMNORDERARRAY = 0x103a and GETCOLUMNORDERARRAY = 0x103b; 0x1039 belongs
to SUBITEMHITTEST. M14.5 corrects the implementation. Earlier accepted source
and evidence stay immutable, but that historical fixture does not establish
correct interoperability for those identifiers.

The new controls145 builder generates a corrected fixture from the unchanged
accepted C source. It changes only those message IDs, retains every functional
assertion and records canonical/generated hashes and replacement counts. The
new regression must pass against the real identifiers; accepting the old
incorrect IDs as aliases would obscure the separate hit-test operation.

## Painting and checks

Cells follow stored column order and clip labels to their column. The actual
small image list supplies row artwork. Callback-supplied text is accepted only
while the HWND/model revision remains valid; replacement requests a fresh
paint rather than reading stale row pointers.

The owned fixture checks selection without activation, real timed double-click,
Enter, veto preserving the earlier selection, callbacks that replace a list
with the same number of different rows, and final resource cleanup. Original
7-Zip navigation must be checked separately, including genuine file-provider
errors and the existing path grants. Do not widen grants to make a UI test pass.

## Input state and image-list correction in development

A native fixture using the published SDK image-list messages exposed a second
identifier error: GETIMAGELIST is 0x1002 and SETIMAGELIST is 0x1003. Earlier
code reversed them, preventing original applications from assigning row icons.
The corrected source is pending native qualification; the failing observation
and the earlier selection-only pass are retained separately.

Original 7-Zip folder activation also reached the missing GetKeyState API.
The new implementation keeps 256 key bytes in the existing lazy thread queue
page. Broker-created input carries a hardware snapshot; removing an input
message updates that thread's state. PM_NOREMOVE and application-posted key
messages do not fabricate transitions. GetKeyboardState copies those same
bytes. Modifier and mouse snapshots retain the input-time state even when
physical release occurs before the application consumes its queued message.
This does not claim complete keyboard layouts, IME, or asynchronous key APIs.

Review also found that the cursor-position metrics query consumed pending
mouse edges. A separate read-only pointer snapshot now serves cursor queries;
the normal input consumer retains ownership of the edge queue. The owned
native keyboard fixture stresses cursor queries, removal versus peeking,
posted messages, and delayed modifier/mouse state. These source changes must
pass native tests before being described as qualified behavior.

Development candidate `f80837a0dfa91d1a26a1b511f85393d4` binds 684 compiled
inputs to `a6b9c143a2edb34dda1778ac5abd0ec2f6414b1b`. Compact installation
and two disk-only boots, the original MSI/console lifecycle and all 106 payload
hashes pass. The owned list fixture now passes the published image-list
assignment/retrieval as well as selection, activation, veto and reentrant-model
checks. The owned keyboard fixture passes actual input, no-remove peeking,
posted-message refusal and a callback delayed beyond physical modifier/mouse
release; both fixtures retain zero pages after completion. Supporting host
checks cover 8,704 modifier/key assertions and 100,000 queue operations. The
complete queue structure measures 3,376 bytes, still one lazy page; the older
queue report's 3,072-byte field counts its message slots only.

Original Documents activation now passes the former GetKeyState stop and reaches
the missing SHGetSpecialFolderPathW contract. The follow-up source resolves
physical user folders through USERPROFILE and the existing checked file provider;
it does not expose C:\ root or virtual namespace items as physical directories.
A false create flag never creates a missing folder. A true flag attempts actual
directory creation and verifies the result. Unsupported folders return failure.
This follow-up awaits a fresh frozen build and original navigation test.

The input contract follows Microsoft's [GetKeyboardState](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-getkeyboardstate)
and [GetKeyState](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-getkeystate)
definitions. Physical-folder behavior follows [SHGetSpecialFolderPathW](https://learn.microsoft.com/windows/win32/api/shlobj_core/nf-shlobj_core-shgetspecialfolderpathw).

The physical-folder diagnostic on `70a1bcfa693f900dc600d0b788b63262` passes
its owned create/no-create/delete checks and advances original activation to
FindFirstChangeNotificationW. That candidate is **not qualified**: two local
source files had CRLF bytes whereas their committed blobs had LF bytes. The
byte mismatch and exact base64 snapshots are retained, alongside diagnostic
results. A build-integrity guard now compares every captured input with its
committed blob before compilation and rechecks working bytes before publishing
the manifest. Independent host checks reproduce Git-clean CRLF drift, missing
committed inputs and changes after capture; all are refused.

Directory change notifications remain unsupported. The follow-up explicitly
returns INVALID_HANDLE_VALUE with ERROR_NOT_SUPPORTED for a valid directory,
matching the documented [failure contract](https://learn.microsoft.com/windows/win32/api/fileapi/nf-fileapi-findfirstchangenotificationw),
rather than claiming a functioning watch or terminating the requesting process.
There is no watch handle, fabricated signal or new polling worker. Missing or
unauthorized paths retain the checked file-provider error. Original application
recovery and further navigation still require native verification. Live
notification support remains an open file-interoperability dependency.

Frozen candidate `c66c3940b0623be100a4350c5978de53` passes the new build
integrity checks for all 687 inputs. Compact and actual 4K installation, two
disk-only starts per profile and original MSI/106-hash regressions pass. The
owned folder/list fixture passes with zero retained pages. The native consumed-
input fixture passes 21 lifetimes, each retaining zero pages. Original 7-Zip
opens Documents and the actual nested folder, renders notes.txt, then stops at
the missing MapVirtualKeyW API on Backspace. That failure remains preserved;
the original browse/back task has not passed. Follow-up [keyboard translation
and cursor work](keyboard-m145.md) is pending new native qualification.

Candidate `9dadeb6f2a2fa2ba91d972128491d63b` binds all 689 inputs to
`dd86c7822ae471a7512000878613089a8bac897e`. Compact installation/two
disk-only starts, original MSI regression, owned list input and the enhanced
keyboard/cursor fixture pass. The unmodified original 7-Zip completes Documents,
nested-folder and Backspace navigation, preserving independently checked file
bytes. Its one retained page is the previously qualified shared registered-
format cache; the owned keyboard/list fixtures retain zero pages. Native edit
and arrow cursor captures were also visually inspected.

That functional navigation pass does not close visual acceptance. Independent
review finds blank original detail columns. A separate hidden Windows control
reference confirms that unassigned subitems request LVN_GETDISPINFOW even when
the main item has stored text; an explicitly empty subitem suppresses that
callback. No original app runs on the host and the reference windows are never
shown. The former native painter incorrectly treated those missing subitems as
empty strings. The failing visual review and observer are preserved.

The follow-up shares one checked text resolver between painting, GETITEMW and
GETITEMTEXTW, adds SETITEMTEXTW, and honors DI_SETITEM text caching. A callback
that changes the model cancels the stale operation even when the row count is
unchanged. Callback depth is bounded to eight. Only callback-driven model
mutation requests another paint; allocation/quota failure must not create an
infinite repaint loop. Column alignment follows the application format while
remaining clipped. Owned tests cover missing versus explicitly empty text,
caching, equal-sized callback replacement and actual copied drawing commands;
the original task now also requires its independently known file size. These
source changes pass on frozen development fa4828b3ea8d8b0a33191f687a3dea7f and ea2a705c4fe43c5079ef2d8913a42c0d, including actual visible file size, preserved file bytes and zero-retention owned lifetimes. Original detail dates honor requested column clipping; full header interaction and ellipsis remain unqualified. The current full integration candidate is still under test.
