# M14.5 image-list operations and import refusal development

This follow-up is awaiting native qualification. It does not qualify original
Notepad++ or SumatraPDF entry, installation, interfaces or complete tasks.

## Real image objects

The additional image-list operations query dimensions, extract a caller-owned
icon, remove/shift or clear images, resize and clear a list, copy a bitmap strip,
and set/query the background color. Extracted icons and copied bitmap pixels
survive destruction/removal of the source. Dimensions, indices, flags, source
strips and allocation budgets are checked. A list without ILC_MASK ignores its
mask parameter. The initial mask profile uses decoded black/white mask pixels;
arbitrary palettes, overlays, blending styles and device formats are not all
qualified. [ImageList_Add](https://learn.microsoft.com/windows/win32/api/commctrl/nf-commctrl-imagelist_add),
[caller-owned extraction](https://learn.microsoft.com/windows/win32/api/commctrl/nf-commctrl-imagelist_geticon).

Background state occupies former padding: the image record remains 72 bytes.
The existing 16-MiB process image budget, 256 objects, 512 entries per list and
checked copied-tile drawing bounds remain. Normal drawing applies the actual
background; transparent drawing preserves the destination. Failed insertion
rolls back copied pixels and never advertises a successful new entry.

The owned pixel fixture now uses a contrasting bitmap strip: removing the first
black/magenta image must expose the second green/white image. Independent physical
pixels also check copied-icon lifetime and background color. These native checks
are pending; host compilation is not evidence that they passed.

## Explicitly unavailable operations

The drag service is not implemented. BeginDrag, DragEnter, DragMove and
DragShowNolock return failure; BeginDrag never creates an active operation, so
EndDrag has nothing to complete. GetImageInfo returns failure because no atlas
bitmap handle is exposed. These are typed refusal paths, not working features.
No drag success, ghost overlay or bitmap identity is invented.

## Compact import diagnostics

The two pinned main images request many functions that remain unavailable.
Additional provider names are ABI namespaces, not shipped Windows DLLs or a
claim that their services work. Existing provider IDs and actual API resolution
remain stable. Known unresolved function imports can bind to one shared fatal
refusal body, enabling precise startup diagnostics without one function body
and message string per export. Optional GetProcAddress discovery hides these
addresses and returns null. Unregistered imports still fail at binding.

The generated 639-key table occupies 5,112 immutable bytes. Its collision-checked
64-bit keys cover only the frozen main-image function imports; updaters, plugins
and helper packages are separate profiles. The host generation/lookup check
passes 1,714 assertions. These numbers are not a compatibility percentage.
The refusal reports its real return address and main-image base; a read-only
observer may resolve a direct IAT call or simple import thunk from the pinned
original bytes. It never guesses a symbol for other call shapes.

An owned negative native fixture must verify null optional discovery, explicit
static-call failure, actual call-site identification, resource cleanup and a
subsequent successful original console run. Original entry diagnostics remain
separate and unqualified until their real interfaces/tasks pass.
