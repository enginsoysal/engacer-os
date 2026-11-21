# M14.8 native EXE installer design

M14.7 native and scoped public delivery pass. M14.8 is in development; original Sumatra installation and its reader remain unqualified.

## Execution and authority

Use the existing own kernel, x64 PE loader and ABI. The unchanged installer executes its actual instructions and required original helpers. A source review binds file hash, arguments, destination and installation authority. User mailbox fields cannot grant kernel permissions. Unsupported required operations fail clearly.

First use a labelled diagnostic clone to inspect entry, TLS, exception and actual API behavior. Replace private dispatch instrumentation with the ordinary shipped source-selection route before qualification. A frame, banner, manual extraction or replacement installer is insufficient.

The matching 3.6.1 source identifies self-copy, embedded LZMA extraction, native GUI controls, an installer thread and registry/shortcut effects. Check invocation against that version. Optional preview/search/update families remain separate.

## Resources and persistence

### Restricted Windows identity

Windows clients use the current native owner's restricted interactive profile.
The kernel's read-only W8_SYS_SECURITY148 query verifies the actual owner root
and reports authenticated/user/interactive categories without allocating token
objects or adding services. Existing syscall numbers remain unchanged; the new
query is appended. It changes no filesystem or registry grant.

CheckTokenMembership with a null token maps that profile to Everyone,
Authenticated Users, Builtin Users and Interactive well-known SIDs. It does not
map the process to Administrators, LocalSystem or a service account. A selected
product's installation review gives bounded broker authority, not Windows
administrator membership. This prevents an installer privilege query from
inventing broad OS access. Explicit token handles, impersonation and the full NT
token/ACL model remain unsupported; their calls must fail visibly.

SID allocation/serialization is ordinary caller-owned data. Neither constructing
an Administrators SID nor changing user-writable startup fields changes the
kernel-owned identity profile or authorization. This kernel query is preferred
over inferring membership from mutable environment strings or pretending that
every installation runs as administrator.

Allocate session state lazily and account image, heap, stack, kernel, framebuffer and caches separately. Stream OS-owned copies and hashes in bounded chunks. Preserve original allocation semantics and measure high-water/retained pages rather than silently expanding all quotas. Whole-system optimization remains M14.15.

Use an explicitly selected fresh destination and preserve personal files, modified app data and protected records. Original removal and required children must run. Independently inspect outputs and persistence after restarting. Later M14.11 repair/upgrade work does not waive the normal removal/reinstall chain or current data protection.

## Evidence

Record source/media/build identity, original hashes and architectures, API/fault traces, native windows/input, actual file/registry/shortcut effects, child executions, independent starts and resource limits. Preserve failures and distinguish private routing probes from shipped behavior.

[Stage gates](../milestones/m14-8.md), [vendor source](https://github.com/sumatrapdfreader/sumatrapdf/blob/3.6.1rel/src/Installer.cpp), [official command line](https://www.sumatrapdfreader.org/docs/Installer-cmd-line-arguments), [M14 requirements](windows-m14.md).

## Bounded native logical fonts (development)

Logical GDI font objects select the existing shared OFL Inter raster strikes:
14/16 regular and 21/28 semibold logical pixels, with actual 100/150/200%
physical coverage. Negative LOGFONT height selects by EM; positive height by
actual cell height. Nearest size takes priority over weight. Missing families
map to Inter; GetTextFace and TEXTMETRIC report the actual selected face and
metrics. This is not arbitrary TrueType family/size support. Rotation, custom
width and italic remain explicit unsupported operations.

This reuses the native immutable atlas instead of allocating per-process glyph
copies or adding a font interpreter/service. Up to 64 lazy logical objects keep
original LOGFONT descriptors and generated handles. Selected objects cannot be
deleted; DC release drops the reference. Text measurement and retained rendering
use the same strike. Underline and strikeout are real retained line primitives.
The copied draw record stays 552 bytes and keeps seven commands per kernel page;
its text height now selects the known strike. An appended read-only IPC reports
actual font metadata without changing earlier operation identifiers.

Initial validation is pending. The original installer reaching CreateFontIndirectW
is a diagnostic observation, not a successful installation. Owned native font
lifetime and pixel tests and the unchanged original installer must pass before
these changes qualify. GetObjectW supports LOGFONTW-sized or smaller buffers;
extended undocumented object records remain unsupported.

## Common-control subclass candidate

COMCTL32 names and ordinals 410-413 bind to actual same-thread subclass
registration/query/removal/continuation. Each callback owns its procedure/id
pair and mutable reference data; duplicate registration updates data in place.
The live chain runs newest first. A bounded stack frame preserves the chain
position across nested sends, self-removal and removal of later callbacks.
Newly registered callbacks join subsequent dispatches. NCDESTROY delivers the
remaining callbacks and then releases the window's metadata automatically.
Cross-thread use is explicitly unsupported rather than unsafely invoking code
on the wrong thread. Limits are 16 entries/window, 128/process, 32 active
subclass dispatches/thread. Metadata is allocated lazily and creates no worker,
service, polling loop or kernel callback pointer. Real mutation/continuation
and native cleanup tests are pending; export identity alone is not behavior.

## Ideal button geometry

BCM_GETIDEALSIZE uses the real selected native font and the native button
padding. Single-line pushbutton width is measured text plus 24 pixels; height
is measured cell height plus 12, at least 32. A requested width is retained,
matching the currently implemented single-line clipped paint behavior. Other
button types return actual window dimensions. Multiline and image pushbutton
layout remain explicit unsupported profiles instead of claiming text wrapping
or image measurement that painting does not perform. The original caller
receives actual native dimensions, not copied Windows theme constants.

Contract: https://learn.microsoft.com/en-us/windows/win32/controls/bcm-getidealsize

## Full-window metadata and rectangle calculation candidate

GetWindowDC exposes real window geometry and selected-font metrics in a
thread-owned DC. Non-client pixel commands fail explicitly; the current retained
compositor only supports client painting. ReleaseDC identifies the actual
thread-owned DC handle; its advisory HWND does not prevent release, matching
own hidden-window Windows observations. This prevents leaking DCs when an
original client releases with a null window.

DrawTextExW/DrawTextW CALCRECT queries measure the same native glyphs, handle
line separators, single-line mode, escaped ampersands and NOPREFIX, and update
the caller's rectangle only after validation. The current profile caps text at
159 UTF-16 units, rejects tabs/word wrapping, custom parameter records and
painting mode. No requested text is silently drawn or wrapped differently.
General DrawText painting remains a separate required implementation when used
by original task paths; measurement alone cannot qualify GUI rendering.

## GDI+ HDC contexts candidate

GdipCreateFromHDC creates one of the existing bounded 32 graphics objects and
borrows a validated thread-owned native DC. It creates no second framebuffer,
bitmap copy or worker. DPI queries report the actual 96-DPI compatibility
coordinate space; native display scaling remains the compositor's job. Releasing
the borrowed HDC invalidates subsequent queries/drawing; deleting the graphics
object never releases a caller-owned DC. Bitmap contexts still hold actual
bitmap references and retain their prior independent lifetime behavior.

Opaque client clears submit a real clipped rectangle to the native compositor.
Translucent, desktop and non-client clears return NotImplemented; alpha blending
is not silently discarded. Mixed DC/graphics operations acquire UI metadata
before graphics metadata, avoiding an inverted lock order. Own visible raster
and bitmap/task-lifetime regressions must pass before qualification.

## Derived premultiplied bitmap candidate

GdipCreateBitmapFromGraphics creates an independent real 32-bit premultiplied
ARGB bitmap, retaining the existing 32-object and 24-MiB-per-bitmap limits and
native allocator bounds. Its source context must be valid; the new bitmap does
not retain the caller's HDC or graphics context. The selected compatibility
profile has actual 96-DPI coordinates, so no unimplemented DPI transform is
invented. GdipGetImagePixelFormat reports the actual storage format.

Premultiplication rounds channel*alpha/255 to nearest; inverse conversion uses
channel multiplied by floor((255<<16)/alpha), shifted right 16, with zero alpha
handled separately. This reproduces the observed lossy Windows readback,
including full channels becoming 254 for some alpha values. Own native scalar
code is exhaustively compared against actual Windows GDI+ bitmap data, not only
against an algebraically similar formula. Clear converts its fill color once
before the pixel loop. No second image, color table or background worker is
allocated. Native storage/clear/lifetime qualification remains required.

## GDI+ logical font families candidate

The native installed family is Inter. Explicit compatibility aliases (Arial,
Segoe UI, Tahoma, Microsoft Sans Serif, MS Shell Dlg/2, Helvetica, sans-serif)
select Inter and expose that actual name in family/logfont queries. Unrecognized
names return FontFamilyNotFound; custom font collections remain unsupported.
This is a declared native substitution profile, not bundled Microsoft fonts.

Up to 32 independently allocated family objects and 32 font objects share the
immutable raster atlas. Fonts clone logical selection instead of borrowing
family objects or selected caller HFONTs. Destroying the source family, DC or
HFONT does not invalidate an independent font. Regular sizes select 14/16 pixel
strikes; bold selects available 21/28 semibold strikes, reporting actual weight
600 and actual selected size. Underline/strike are retained logical decorations;
italic and unsupported physical units fail explicitly. Pixel/point conversion
uses the actual 96-DPI coordinate profile. Arbitrary font sizes/outlines and
font rendering APIs remain unqualified until their actual implementations pass.

GdipCreateFont's emSize is a real Win64 floating argument. Only the necessary
user font functions enable SSE2 code generation; the rest of the freestanding
runtime/kernel retain their current compilation settings. Native scheduling
already saves/restores user floating state. Native callers must verify actual
floating arguments/results, not call these exports with integer substitutes.

## Text-format state candidate

GDI+ text formats are independently owned bounded objects, with actual flags,
horizontal/vertical alignment, trimming, language and up to 32 copied character
ranges. Generic default and typographic requests allocate independent objects;
clones own their state, so one application's mutation cannot change another
format. Arbitrary flags are retained as requested; later layout must explicitly
reject rendering modes it does not implement. Metadata storage cannot qualify
right-to-left/vertical layout, trimming or formatted text drawing by itself.

Own off-screen Windows references verify default values (typographic 0x6004,
no trimming), enum rejection, all flag bits, clone independence, range counts,
ValueOverflow above 32 and normalization of negative counts to zero. Native
format object quota is 32. No background worker or font/glyph copy is added.

## Formatted measurement candidate

GdipMeasureString calculates actual selected-font glyph advances/cell heights
using the existing copied native font service, with no per-character syscall or
glyph duplication for fitting lines. Bounds and optional fitted/line counters
are committed together after validation. Source text is bounded to 159 UTF-16
units and 32 lines. Default native overhang allowance is one third of the EM
across both sides; typographic fitting uses advances without that allowance.
Actual selected raster metrics remain authoritative and differ from substituted
Windows fonts and full shaping engines.

Pixel and point page units, line separators, trailing-space selection and
horizontal/vertical block alignment are supported for rectangles containing the
complete measured text. Wrapped/partial-fit rectangles, tabs, RTL/vertical,
custom fallback and ellipsis layouts explicitly refuse. Metadata success for a
format does not make those layouts supported. Original tasks requiring them
must expand this profile and pass actual drawing/measurement consistency tests.
Formatted drawing itself remains unimplemented; measurement is not a drawing
qualification. Native integer glyph advances remain shared with the compositor.

## Solid brush candidate

Solid brushes own their actual 32-bit ARGB color and remain independent after
clone/mutation/source destruction. They use a lazy 32-object process table and
share existing allocation bounds. Color/type queries report actual retained
state, including transparent colors; no alpha channel is silently removed.
Other brush kinds remain unsupported. These metadata/lifetime operations do not
substitute for the actual pixel drawing APIs required by the original installer.

## Real integer rectangle filling candidate

GdipFillRectangleI clips integer rectangles to real bitmap/client bounds using
64-bit intermediates. Nonpositive dimensions and empty intersections are no-ops,
matching owned Windows observations. Opaque client rectangles submit actual
native retained primitives. Non-client/desktop and translucent DC rectangles
remain unsupported. Premultiplied bitmaps support real SourceOver and SourceCopy;
other bitmap formats currently admit opaque fills only.

Solid source conversion happens once per rectangle. Each premultiplied channel
uses source + round(destination*(255-sourceAlpha)/255), including alpha. Own
Windows GDI+ reference compares 65,536 source/destination alpha pairs and distinct
RGB channels with the exact native integer helper. No framebuffer duplication,
new render thread or per-pixel syscall is introduced. External borrowed backing
is validated before access; stride/padding and bitmap lifetime rules remain.
The visible fixture must show actual red pixels through the GDI+ client path.

## Bitmap blitting candidate

GdipDrawImageI has a real bitmap-to-bitmap path with actual RGB/ARGB/PARGB source
conversion, PARGB destination, source-over/copy, wide clipping and overlap-safe
row/column order. It uses existing backing directly and allocates no full-image
temporary. Both borrowed buffers are checked before access. Pixel/Display page
units use the current native pixel grid; other units refuse.

The window destination remains explicitly unimplemented and stops the task
with actual image dimensions for investigation. Existing tiny icon tiles cannot
qualify arbitrary large image submission. Original window presentation must be
implemented and tested before installer qualification. Own Windows references
also show that logical GetPixel readback can change while an original borrowed
scan pointer remains unchanged after a self-blit; do not infer success/failure
only from the reference's backing pointer. Native tests verify bitmap readback.

## Copied window-image submission candidate

GDI+ window images use one bounded UI request rather than thousands of tiny
icon tiles. The kernel copies its fixed 56-byte request, validates window/thread
ownership, format, dimensions, signed stride, coordinates and quotas, allocates
owned pages, copies checked source rows, then publishes one retained command.
Failed copies/allocations roll back all temporary pages. Source pointers never
reach the compositor. Actual native image disposal/mutation after submission
must leave captured frame pixels unchanged.

The pixel budget is 4 MiB/image and 8 MiB globally, with eight snapshots/window
and 32 globally. Up to two pointer-table pages cover each image. Image metadata,
pointer tables and pixel pages use normal managed UI accounting and are freed
on paint reset, window destruction or process teardown. A source format is
straight or premultiplied ARGB; the latter blends stored premultiplied channels
directly, preserving alpha precision. Client cropping/display scaling reuse the
native compositor, and image updates mark actual graphics damage. This is CPU
compositing, not a GPU acceleration claim. Windows bitmap scaling follows the
current fixed 96-DPI compatibility profile; it is not arbitrary per-monitor
Windows DPI awareness or newly rasterized HiDPI Windows bitmap text.

Earlier UI operation numbers and the 552-byte retained primitive are preserved.
The new image request is appended. The candidate requires a new full media build
and exact native/physical-framebuffer tests; private workers on the previous ABI
cannot qualify it. Per-window/global quota exhaustion and inaccessible source
bytes must not leak pages or publish a partially copied image.

## Native button permission indicator candidate

BCM_SETSHIELD changes actual push/command-button icon state; BM_GETIMAGE returns
the current icon. The return is the previous real HICON, matching independent
version-6 Windows observations rather than inventing BOOL success. The button
reserves actual icon space in ideal sizing and paints an original native blue/
gold shield next to its label. Clearing it invalidates and repaints the control.
This is visual state only: native review grants and restricted Windows identity
remain unchanged; setting the icon cannot grant administrator privileges.

Each enable creates an independently destroyable icon handle. Those handles
share one lazily allocated 1-KiB pixel mask per process, with a reference count;
last destruction frees the mask. A replaced icon is returned to its caller;
current control-owned icons are released with control teardown. Existing image
count/storage caps remain. No font, renderer, service or permission worker is
loaded just to show a shield. Native visible show/hide and resource regressions
must pass before claiming this control behavior.
