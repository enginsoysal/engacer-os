# M12.13 — Settings and personalization

Status: M12-STAGE13-VM-v1 native qualification passes for build `119eb7a0e54f4914b768c6d31cf3d01c`. The complete public delivery passes: twenty downloads, 370 pages and 2,568 HTTP links, native homepage Save and actual desktop/mobile verification. M12.14 follows in order.

## How and why

Settings has four consistent categories: Appearance, Display, Input and System.
Shared typography, selected controls and bounded messages fit the existing
700-pixel minimum and compact desktop. Devices retains its real provider view;
Back returns to the remembered System category. Applications and Start/taskbar
open their existing independent management surfaces. Quick settings remains a
base flyout, not another application slot.

Appearance and Display preview their actual provider-backed values. Apply and
save uses the existing validated per-user version-one appearance record and
normal window geometry. Cancel preview, Escape or closing its Settings owner
restores the previous session colors, wallpaper, pattern and display choice
without writing preferences. Display changes use the existing guarded renderer
and reflow windows to remain reachable; they do not roll back independent
window arrangements. A live file dialog must finish before a scale change or
scale cancellation. No framebuffer snapshot is retained.

One global generation-scoped preview owner stores five original visual values.
Other Settings windows explain and disable competing visual changes; they do
not silently replace the first preview. Closing a different Settings window
does not cancel it. The eight category bytes clear on reuse. Optional app
state and personal files are never captured or restored by visual cancellation.

Restore defaults previews this distribution's compiled accent, theme,
wallpaper, gradient and automatic display choice. Apply is still explicit.
It does not reset app installation, files, Start pins or independent input
preferences. A Default accent choice works with customized distribution
recipes; it is not hardcoded to a stock color name.

Input provides explicit 200/500/900-ms double-click choices and the existing US
QWERTY/Dvorak provider. This category clearly states that choices save when
clicked. It is independent of visual Apply/Cancel. A failed interval write keeps
the previous actual interval; existing keyboard-layout failures truthfully
report session-only behavior. Active transfers, file reviews/dialogs and Windows
jobs block competing appearance/input preference writes and retain the preview.

An existing malformed, truncated or unreadable appearance record is refused by
the established checksum/schema/range guards. Settings explains the safe
fallback and offers Apply to save a valid record. A missing record is normal.
No new on-disk ABI or mandatory optional application is introduced.

## Resources and verification contract

New logical state is bounded to 64 bytes: one visual preview owner, five values,
eight category bytes and a validation flag. Measure actual compiled fixed state,
peak and completed retention separately. There is no extra worker, application
slot, pixel cache, animation or idle poll.

Freeze media for real install/ordinary startup, Apply/Cancel/close/defaults,
multiple Settings owners, file-operation/modal guards, independent preference
bytes, input persistence, malformed-record fallback, optional-app independence
and four actual display profiles. Retain exact enabled-device VMware, separate
BIOS, cached/full movement equivalence and actual boot recovery. Host compile
guards do not replace these native journeys; agent review is not a human study.

M12.14 feedback/modal arbitration, M12.16 scale/cursor reconciliation, M12.17
renderer work and M12.18 complete final qualification remain separate stages.

## Measured receipt

9 native task/profile checks, four actual display profiles, separate BIOS and exact enabled-device VMware pass. Fixed shell state is 553,228 bytes (+32); completed UI journeys retain zero pages. [Acceptance](../../evidence/M12/13/acceptance-results.json).
