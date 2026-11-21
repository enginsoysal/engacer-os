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

## Shared window/bitmap alpha rounding correction

Straight ARGB snapshots must first round source premultiplication and then
separately round the destination contribution, matching actual Windows GDI+
memory-HDC output. A fused division can differ by one channel level. The scalar
helper now lives in a common original header used by both kernel image rendering
and user bitmap processing; its exact host reference covers 65,536 pack pairs,
32,895 inverse pairs and 65,536 source/destination alpha pairs. A separate
4096-case HDC reference and a physical native framebuffer counterexample bind
the window behavior. Existing native UI glyph/icon blend paths are unchanged.
The corrected kernel requires new full-media qualification.

## Actual single-monitor placement candidate

MonitorFromRect/Point use the current native logical display bounds and real
primary/nearest/null fallback in the existing single-display profile. An empty
or inverted rectangle uses its top-left point, not a normalized area. Checked
GetMonitorInfoA/W returns actual monitor/work-area rectangles and native display
identity for base and matching extended records. No dynamic display list or
background discovery worker is added, and no second monitor is invented. This
supports original window placement while keeping multiple displays and arbitrary
Windows per-monitor DPI awareness outside the current qualification.

The next candidate appends a foreground operation without renumbering earlier
calls. Only a live, visible, enabled, non-minimized, same-thread owned top-level
window can request activation. A single scalar pending handle adds no allocation;
the real desktop consumes it, changes actual focus/z-order and publishes actual
foreground identity. Native modal surfaces, menus/dragging and another active
Windows process refuse. A currently active Windows frontend can admit its
newly launched original window. GetForegroundWindow reads the actual published
state, never the pending request. Destruction clears stale pending/current
handles. Asynchronous activation remains subject to native admission; full
Windows foreground-lock timeout, arbitrary cross-process grants and thread
priority boosting are not implemented. Native invalid/hidden-window refusal
and actual keyboard/foreground checks are pending on a new full build.

Primary contract: [SetForegroundWindow](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setforegroundwindow).

### Native foreground passes; queue-only message wait candidate

Full media `45399d7e462020a46060872374d95f70`, source `db262e46`, passes
fresh install/two independent starts, retained original 7-Zip tasks, all three
owned API sessions and three real framebuffer/keyboard lifetimes. The owned
GUI actually receives a key and verifies GetForegroundWindow against its HWND;
closing retains zero managed task pages. Original Sumatra reaches its RunApp
message loop, then refuses MsgWaitForMultipleObjects at return RVA 0x73daa.
Original disassembly proves count=0, null handle array, wait-all=true, a computed
finite frame timeout and QS_ALLINPUT=0x1cff. This is not a successful installation.
Preserve the scope in `evidence/M14/8/development/native-foreground-pass-message-wait-refusal`.

Implement that real zero-handle queue wait through the existing object-wait
scheduler. A reserved request mode distinguishes it from ordinary object waits;
request and thread record sizes remain unchanged. Queue new-input bits and a
last-observed timer timestamp fit within the existing lazy 4-KiB queue page.
Actual posts, native keys/mouse and timer deadlines wake the thread. Infinite
waits without timers do not add polling, services or periodic wakeups. Finite
waits use existing scheduler deadline ownership and return WAIT_TIMEOUT.

Peek/Get mark applicable input old. QS_POSTMESSAGE clears even with a filtered
peek; QS_ALLPOSTMESSAGE clears only without a range filter. A posted WM_KEYDOWN,
WM_MOUSEMOVE, WM_PAINT or WM_TIMER is posted input, not fabricated hardware,
paint invalidation or an actual timer. Own Windows thread-queue comparisons
confirm those categories, repeated wait behavior, filtered PM_NOREMOVE, actual
25-ms timeout and a real timer wake. No visible host window is created.

Real local paint invalidation is separately checked before sleeping; inspecting
its WM_PAINT marks it old until new invalidation. The added per-window scalar
shares the existing runtime window allocation. Mixed object/message arrays
remain explicitly unsupported (error 50); oversized counts/unknown wake masks
refuse. The implementation does not substitute a Sleep loop for an input wait.
Native queue-age, finite empty-mask timeout, actual cross-thread post wake and
actual GUI timer tests are pending on new full media. The foreground pending
handoff additionally uses atomic exchange, and its getter reports no Windows
foreground while the native desktop/modal surface is active.

Primary contracts: [MsgWaitForMultipleObjects](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-msgwaitformultipleobjects), [queue-state categories](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getqueuestatus).

### Native queue/timer waits pass; real text raster candidate

Source-bound production worker `292cb370` on full kernel/media
`790c2d5bbc9991ac7a7206479045e2b9` passes all three native API sessions,
including repeated/new versus old posted input, filtered/unfiltered peeks,
finite empty-mask deadlines, actual cross-thread post wake and a GUI timer.
Heap probe pages return 270 to 270. All three actual font/image/shield/focus
lifetimes retain zero managed task pages. Original Sumatra reaches painting in
RunApp and reports a real delay-load failure for gdiplus!GdipDrawString. The
exception is not swallowed. Preserve the pass and original refusal in
`evidence/M14/8/development/native-message-wait-pass-draw-string-refusal`.

A new appended raster operation exports copied, public OFL Inter coverage from
the existing immutable atlas. It never maps kernel memory into an application
or retains an app pointer. A checked 528-byte request selects an actual canonical
96-DPI strike (14/16 regular, 21/28 semibold). A size/metric query copies only a
32-byte header. A draw query returns a 3872-byte bounded metadata table plus
packed grayscale glyph pixels, with at most 160 glyphs, 64x64 per glyph and
128 KiB per packet. A temporary managed kernel page holds the metadata and is
freed on every result; the caller's temporary packet is freed after drawing.
No second full atlas, per-character syscall, persistent font cache, interpreter
or new service is introduced. Invalid pointers, writable-page rights, sizes,
missing termination and unsupported strikes are checked before publication.

GDI+ bitmap measurement now uses the same canonical advances as bitmap drawing,
independent of physical monitor scale. Direct native GDI text retains the actual
physical 100/150/200% strikes. The new DrawString candidate paints actual
SourceOver grayscale coverage into PARGB backing with a per-call 1-KiB color
table, actual brush opacity, bounds/layout clipping, alignment and optional
underline/strike pixels. Opaque plain client text can use the native retained
text command. Original bitmap presentation remains the qualified copied-image
route. Family aliases report Inter; this is not Windows font/shaping identity.

The first bounded drawing profile covers fitting horizontal single lines in
Display/Pixel page units and default/grayscale rendering. Multiple/control-line
text, wrapping/partial fit, complex shaping/RTL, SourceCopy text, other hinting
modes, non-PARGB bitmap targets, translucent/decorated client text and other
units still return unsupported. They must be implemented if original tasks
require them. No unsupported drawing call reports success.

Native packet query/coverage/buffer guards, actual transparent glyph pixels,
clip/sentinel/lifetime checks and visible bitmap/direct-client glyphs are added.
Both owned fixtures compile; execution on a new full kernel/media remains
pending. Source disposal and zero retained pages are required in all three
visible cycles. This is development, not original installer acceptance.

### Actual glyph pixels pass; affine text candidate

Full media `3dcc08715fc0fd410ccb9bfc2ed3712f`, source `abdd7a50`, passes fresh
compact installation/two disk-only starts, retained original 7-Zip tasks and all
three expanded native sessions. Glyph packet size queries, copied coverage,
write sentinels, malformed input and all four actual strike selections pass.
Borrowed PARGB backing contains actual clipped half-alpha green text; unsupported
layouts/modes return errors. Three physical framebuffer lifetimes show green
bitmap glyphs and brown direct-client text after the source font/image objects
are disposed. Every visible close retains zero managed task pages; the heap
probe returns 271 to 271 pages. Original Sumatra next delay-loads
GdipRotateWorldTransform. Preserve this actual pass/refusal under
`evidence/M14/8/development/native-draw-string-pass-transform-refusal`.

Add actual six-float row-vector world matrices, prepend/append composition,
rotation/translation/scaling/reset/get/set/multiply, and 32 bounded independently
owned matrix objects. Each lazy graphics record gains 24 bytes of state; no
kernel structure, new service or permanent pixel cache is added. Matrix copies
remain independent after source-object deletion. Unknown order, nonfinite or
out-of-profile values refuse without changing the old matrix. The original
window's required transform is not treated as an ignored drawing hint.

The production scalar math is shared directly with an owned off-screen Windows
reference: 511 angles in the named -720..720 degree corpus and 512 actual
prepend/append products pass. Maximum observed absolute differences are
9.984e-7 for rotation and 2.289e-5 for products. This is bounded numerical
agreement, not bit identity or native execution qualification.

For transformed PARGB text, compose actual glyph coverage into a temporary
bounded mask (at most 1 MiB), map destination pixel centers through the inverse
affine matrix, sample coverage bilinearly and perform the existing scalar
SourceOver operation. This prevents forward-mapping holes when letters rotate
or scale. The identity fast path allocates no mask. Temporary masks/packets are
freed on every result; real native lifetime/peak checks are pending. Bitmap
bounds and transformed layout clipping remain enforced. Singular transforms
have zero-area output. Transformed image/rectangle and transformed client-text
paths explicitly refuse until implemented; required original calls must guide
those extensions. Complex shaping/layout and other prior limits remain open.

Owned native tests now cover real float ABI, matrix copies/orders/quotas,
quarter-turn pixel placement and a physical purple vertical text image after
source deletion. Supporting reference and fixture compilation pass; native
execution on a source-bound production worker is pending. Full M14.8 shipped
EXE installation, original removal/reinstall and publication remain mandatory.

## Scoped product-file metadata candidate

Keep file metadata outside application directories in protected owner records,
bound to both the owner root and exact file path. M14.8 extends that existing
record store from user files to the current kernel-validated product root.
Reads/defaults, writes, modification tracking and cleanup use the same scope.
Actual file effects still require existing handle access and path8 permissions;
this is not an administrator or cross-product write grant. Ignoring a failed
metadata update would conceal a real installation error, so refusal remains
visible until this scoped persistence works.

For CopyFileW, retain destination creation time (new for a new file), refresh
access time and copy source last-write plus supported attributes. Owned Windows
new/replacement references establish this behavior. Earlier development tests
that expected all three source times are explicitly superseded, without rewriting
their captured results. Direct handle-to-extent copying reuses the volume page,
retains the 8-MiB ordinary dirty-data budget and performs existing complete
storage readback verification. An 11-MiB deterministic native copy checks bytes
beyond that budget; it does not qualify arbitrary unbounded WriteFile use.

Private `.EngacerMSI` staging/journal paths are excluded from normal product-file
metadata. The existing staging move requires absence of metadata records;
expanding that trusted move to accept them would change its security contract.
Keep that guard and preserve the failed initial extension as development evidence.

## Windows-contract-first validation

Implement shared Windows contracts rather than vendor-name branches or fixed
successful responses. For each compatibility family, establish Microsoft's ABI
and behavior first, use owned Windows reference programs where safe and useful,
then test native observable effects and unchanged original programs. Preserve
reference/native differences explicitly. Original applications are independent
integration callers, not substitutes for the contract.

The initial SHChangeNotify profile is the documented association-change/IDLIST/
NULL-items event measured in the original installer source. Its consumer is the
real native shell: reload durable association preferences, invalidate listing
caches and request native repaint. A delivered revision/serial marker follows
those effects. This does not introduce Windows change-listener registration,
COM thumbnail handlers or Windows-program association launching before their
separate implementation/qualification.

## Shared UTC clock continuity

A valid RTC sample seeds one compatibility UTC clock. Its value advances with
existing HPET elapsed microseconds across applications and CPU halt periods.
Initialization alone retries RTC stability, bounded by both attempts and five
milliseconds; subsequent Win32 time and file/registry timestamp calls avoid raw
CMOS sampling. This corrects an observed transient zero-time result rather than
returning a fixed fallback date. The initial absolute precision remains the RTC
second. Setting/resynchronizing wall time and suspend calibration are separate.
A disposable-VM RTC SET fault, restored through monitor I/O, tests continuity after
a real initial seed; it is not proof that UTC can be obtained with no trusted
initial time source.

## Version queries are compatibility predicates, not feature promises

Keep GetVersionExW and VerifyVersionInfoW consistent with the explicit existing
6.1/build-7601, zero-service-pack workstation query profile. Compare actual
requested fields, hierarchical version conditions, suite AND/OR and independent
build/platform/product values. False predicates use error 1150; malformed inputs
use error 87. The pure implementation is compared with original Windows using
its own reported reference version. This neither imports host-version data into
the guest nor claims that every feature of that Windows version exists. Manifest
negotiation and additional version profiles remain separate work. Feature/API
presence and original application behavior must still be tested independently.
