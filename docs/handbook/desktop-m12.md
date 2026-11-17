# M12 desktop experience — staged development

M12.0 established the original design and ordered plan. M12.8 now qualifies
[shared native file dialogs](dialogs-m128.md); each stage retains its own scope.
Use the [current native guide and scoped media](index.md); each newer native
stage requires its own matching acceptance and release. [Progress and acceptance](../milestones/m12.md).

The target is recognizable app icons, consistent desktop/Start/taskbar/window
identity and one Files frame for native folders and USB. Buttons/menu commands
activate once; objects select on one click and open on double-click or Enter.
Back, Forward, Up and Home remain distinct. Unsupported functions stay explicit.

## Complete tasks used for acceptance

- Install on a disposable supported VM disk; restart into the installed desktop,
  disconnect only the ISO and start twice with saved choices.
- Recognize Calculator/Calendar/Clock; launch, minimize/restore and close them
  while Files and required services remain usable.
- Documents → USB drives without a stick → Back. Insert supported media, open a
  folder, use Up/Back/Forward and retain a truthful path and title.
- Create/rename/copy, resolve conflicts, cancel, recycle/restore and inspect real
  stored bytes. Unsupported USB operations explain their limits.
- Open/save using common dialogs, cancel safely and preserve unsaved work.
- Customize appearance/pins/categories, restart and retain supported choices.
- Repeat keyboard-only routes, themes, supported scaling, actual 4K and reduced
  motion; measure idle behavior and peak/retained memory separately.

Concepts show proposed behavior, never a completed driver or runtime feature.
Native-stage manuals and downloads update after each accepted implementation.
