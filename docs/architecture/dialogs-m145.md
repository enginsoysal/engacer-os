# M14.5 resource dialogs

Development implementation, not yet original-application dialog qualification.

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

References: [DialogBoxParam](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-dialogboxparamw),
[EndDialog](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-enddialog),
[standard control data](https://learn.microsoft.com/windows/win32/api/winuser/ns-winuser-dlgitemtemplate),
[extended control data](https://learn.microsoft.com/windows/win32/dlgbox/dlgitemtemplateex).
