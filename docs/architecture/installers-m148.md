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
