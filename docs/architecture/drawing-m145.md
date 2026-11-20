# M14.5 drawing and control implementation

Development candidate, not accepted M14.5 compatibility. Original application
interfaces and exact new media still require independent native qualification.

## Copied image tiles

The existing retained primitive contains 512 payload bytes. An anonymous union
uses those same bytes for either UTF-8 text or 128 straight-alpha ARGB pixels;
the fixed IPC record size does not increase. Kind 4 accepts tiles at most 16 by
8 pixels. The kernel copies the whole command, checks ownership, thread, signed
coordinates, dimensions and clipping, and never retains an application pointer.

ImageList_Draw and DrawIcon/DrawIconEx translate private decoded resources into
these bounded tiles. The native compositor blends them through its existing
clipped framebuffer path at the actual display scale. Alpha-zero pixels retain
the underlying surface. Optional unsupported raster flags fail explicitly.

This reuses the existing 224-command per-window and 128-page global drawing
quotas instead of adding unbounded full-window image surfaces. Large image
operations can hit that quota and report failure; this is not arbitrary GDI,
GPU acceleration or a general image canvas. Existing process-private image
storage remains separately bounded at 16 MiB. Calls do not create a timer or
polling renderer.

The first physical-pixel fixture exposed an older LoadImage default-size bug:
zero dimensions without LR_DEFAULTSIZE incorrectly requested 32 by 32. The
corrected loader takes the first resource image's actual dimensions; only
LR_DEFAULTSIZE requests the default metrics. LoadIcon retains its documented
default-size behavior. The failed candidate remains separate development
evidence. [LoadImage sizing contract](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-loadimagew).

## Toolbar measurement and input

Copied toolbar labels are measured using the native font metrics at insertion.
Paint, TB_GETITEMRECT/TB_GETRECT, maximum size and pointer hit testing use one
geometry routine. Separators and hidden items have their own rules; enabled
buttons capture the pointer and only send WM_COMMAND when release matches the
pressed button. Disabled buttons do not invoke the owner command. Text is
clipped inside its button. Original image-list indices supply the actual icon
pixels; the implementation does not recognize an application name or paint a
replacement application interface.

The width cache costs 256 bytes per allocated toolbar model; it avoids repeated
font-measure system calls during pointer movement. These are component costs,
not total OS performance. M14.15 remains mandatory whole-system optimization.

References: [toolbar contracts](https://learn.microsoft.com/windows/win32/controls/toolbar-control-reference),
[button states](https://learn.microsoft.com/windows/win32/controls/toolbar-button-states),
[image-list draw flags](https://learn.microsoft.com/windows/win32/controls/imagelistdrawflags).
