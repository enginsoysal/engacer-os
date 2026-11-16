# M12.6 file presentation decisions

Status: native qualification passes M12-STAGE6-VM-v1. Public release and full
website verification close separately before M12.7. Host rules supplement actual
installed behavior; final comprehensive qualification remains M12.18.

## Responsive views and actual metadata

Keep the M12.5 navigation frame and provider identities. Details gives Name
priority, adds a 96-pixel Size column from 360 available pixels, and a 148-pixel
Type column from 560. Narrow views omit a column rather than crushing names or
overlapping text. File type names describe supported filename associations;
they do not validate file contents. Size comes from the real directory entry;
folders show a dash because no recursive size scan occurs. No dates are invented.

Icons uses shared 48-pixel original artwork and 112-pixel rows, with centered
two-line labels. Explicit ellipsis replaces overflowing paragraph rendering.
Native and USB use the same column and tile geometry. USB retains six metadata
rows at a time; its grid, keyboard movement and page controls use that actual
capacity. USB directory ordering remains unchanged and sorting stays unavailable
rather than advertising a sort that the provider does not implement.

The minimum Files window keeps its body below the complete navigation/toolbar.
The current graphical minimum is 500x420. The content offset also remains safe
if later validated sizes become smaller, instead of using the old below-360
branch. Empty-state instructions stay short enough for the body.

## Ordering and selection identity

Native Name, Type and Size headers are real buttons, use the shared focus/hover
states and expose the current direction. Repeating a header reverses its order.
The sort menu remains available in narrow windows. Type sorting uses exactly
the displayed type names, grouping txt/md/log as Text document. Natural ASCII
name comparison handles digit runs by their length and digits, without numeric
conversion or overflow: File2 precedes File10. Leading-zero ties use the shorter
run first. Directories remain first in either direction. Fully equal names retain
their stable source-entry order even in reverse mode.

The existing bounded native heap sort and listing cache remain. Selection stays
bound to source-entry IDs. Sorting remaps keyboard focus and range anchor to
those IDs and reveals a focused selected item. Active selection, inactive
selection, hover and keyboard focus have different visual roles. Changing view also reveals the focused selected object in the new page size.
Changing order or view does not open an object; ordinary single-select/double-click/Enter remains.

Native breadcrumbs show every ancestor when it fits; a skipped middle is marked
with explicit ellipsis. USB similarly marks omitted ancestors. This avoids
showing Home/Scene as though Documents were not part of the actual hierarchy.
Ancestor controls retain their checked path-prefix commands; Edit has the full
address.

## Complete names and preferences

Hover an abbreviated supported filename for its full name in a measured opaque
tip. Bounded wrapping uses native Inter at 14 pixels, at most twelve 63-character
lines and no heap allocation. The tip stays inside the visible window and screen;
if there is insufficient room it is not clipped into an unreadable popup.
Moving away invalidates its old bounds. Drawing rechecks the real topmost window
and current row under the pointer: a native probe found stale hover state after
keyboard window/location changes in the first candidate, and that candidate is
not accepted. Capture, dialogs, menus and the launcher
suppress it. USB name lookup uses its own one-entry stack record, preserving
the shared visible rows and generation-bound identity.

Native paths reuse the existing 32 view/order preferences. USB adds one validated
16-byte per-user view record under System/Settings, separate from device identity.
Missing/invalid state defaults to Details; preference write failure keeps the
session's choice and explains that it could not be saved. No app or core service
depends on that optional preference file. Existing USB windows retain their own
view; subsequent navigation uses the saved USB default without rebinding a lease.

## Qualification boundary

Host checks cover comparator antisymmetry/transitivity, stable identities,
folders-first ordering, numeric strings beyond integer range and responsive
geometry. Native qualification must separately exercise installed startup,
different real file sizes/types, selection through ordering, full-name tips,
minimum size, both views/providers, saved choices after ordinary boots, USB
detach and actual 150%/4K. Exact VMware and BIOS media, idle/resource and twelve
cached/full comparisons remain gates before release and full website closure.

No second native listing cache, per-window framebuffer, idle timer or raster
icon cache is introduced. Configured RAM, linked fixed state, transient stack
space and managed display/device pages are separate measurements. Physical
hardware, vendor GPU 3D and universal Windows compatibility remain unqualified.
The existing M12.14/M12.16/M12.18 carry-forward observations remain open.

The corrected candidate passes ten native journeys, separate real 150%/4K name
tips, twelve cached/full comparisons, exact enabled-device VMware and BIOS
install/ordinary starts. Linked fixed shell state is 545,636 bytes, 16 above
M12.5 and 1,808 above M11.6. Main tasks return to 1,047 managed pages (4,288,512
bytes), peak 1,059 pages, with zero retained pages or new allocation failures.
Font coverage remains 251,248 bytes, raster icon cache zero and temporary icon
row 512 bytes. Idle paints stay unchanged and CPUs halt. These are distinct
from configured VM RAM and full kernel consumption.
[Exact-source acceptance](../../evidence/M12/6/acceptance-results.json).
