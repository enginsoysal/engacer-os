# M14.5 resource dialogs

The owned standard/extended resource profile passes 21 native lifetimes. The original 7-Zip About/OK/modal-owner task passes on compact and actual 4K profiles. Native M14.5 qualification passes; public delivery passes within the recorded owner scope. Arbitrary original resources and applications remain unqualified.

Standard and extended Windows dialog resources are parsed with explicit byte
bounds, UTF-16 termination limits, DWORD alignment, ordinal names, font records,
32-bit extended control IDs and the distinct standard/extended creation-data
length rules. Parsing is limited to 64 KiB and 31 declared controls. The native
32-window process quota is independently enforced during creation. A partial
creation must destroy its children and restore an owner disabled by this call.

DialogBoxParamW creates actual child HWNDs and calls the original application
dialog procedure in its protected thread. WM_INITDIALOG receives the full 64-bit
application value after children exist. DWLP_USER remains application-owned;
runtime modal state is separate. EndDialog marks completion, including calls
during initialization, and destruction follows after the callback returns.
The original result is returned without truncation. A nested modal message loop
uses the existing atomic blocking message wait; there is no polling task.

The owner is disabled before initialization and re-enabled only if this call
disabled it. Keyboard focus returns to the previous live window. Forward Tab,
default-button Enter and Cancel/Escape are routed within the modal hierarchy.
Pointer buttons send real WM_COMMAND notifications. Callback, malformed-template,
partial-creation, owner and process/thread cleanup require separate native tests.

The current renderer uses the native mapped dialog units and Inter UI font;
arbitrary requested typefaces, custom dialog window classes, indirect/modeless
dialogs, general group-navigation semantics and every control class are not
implemented by this initial resource-dialog path. Unsupported classes/flags and
quota exhaustion fail explicitly. This foundation does not qualify Notepad++
or SumatraPDF execution or the complete M14 application corpus.

Foreign caption actions follow the application's actual window styles.
Dialogs without minimize/maximize boxes do not expose those controls, and
fixed-size dialogs do not accept interactive resize or snap actions. The
native desktop keeps its existing controls. Static dialog labels inherit the
dialog background; the original parent can supply its system brush through
WM_CTLCOLORSTATIC. Control painting revalidates ownership after that callback.
The compositor reads the checked existing style word rather than duplicating
window state or copying an entire window view for every caption action.

Static icon controls load a resource from their actual instance. Default icon
loading uses the native 32-pixel icon metric; SS_REALSIZEIMAGE selects resource
dimensions instead. Without centering/stretch styles, the control adjusts to
the loaded image. SS_CENTERIMAGE keeps the control rectangle and centers/clips
the image; SS_REALSIZECONTROL scales to its rectangle. SS_RIGHTJUST retains
the prior right/bottom corner when image dimensions change. STM_SETICON and
icon STM_SETIMAGE preserve caller ownership and return the previous handle.
Bitmap/metafile static controls remain unsupported by this icon path.
These follow the [documented static styles](https://learn.microsoft.com/en-us/windows/win32/controls/static-control-styles);
the new cases require independent native geometry and pixel checks before
qualification. Resource ordinals are never dereferenced as caption pointers.

References: [DialogBoxParam](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-dialogboxparamw),
[EndDialog](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-enddialog),
[standard control data](https://learn.microsoft.com/windows/win32/api/winuser/ns-winuser-dlgitemtemplate),
[extended control data](https://learn.microsoft.com/windows/win32/dlgbox/dlgitemtemplateex).

## Final named native profile

The 74-task frozen campaign passes: 60 native groups, 13 host groups, 695 exact compiled inputs and the exact enabled-device VMware starter. [Acceptance](../../evidence/M14/5/acceptance-results.json), [release limits](../releases/m145-v0.14.5.md). Earlier candidate waits/failures above are historical development observations, not the final result. Notepad++/Sumatra interfaces, complete original-app tasks and final M14.15 optimization remain unqualified.
