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
