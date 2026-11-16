# M12.1 — shared native visual components

Native qualification passes M12-STAGE1-VM-v1 on build
`981a97dc89216bba34db0b02c25adab2`. [Exact-source acceptance](../../evidence/M12/1/acceptance-results.json)
and [resources](../../evidence/M12/1/resources.json) record the matching tests.
GitHub assets and website readback are separate publication gates.
This stage follows the [M12 design contract](desktop-m12.md); later stages still
own app icons, unified USB navigation, Start/taskbar redesign and final regression.

## Shared presentation and input

`include/engine/ui/components12.h` supplies semantic roles, theme colors, control
states and bounded scrollbar arithmetic. `kernel/desktop/components12.inc`
draws shared desktop buttons/fields and a working Files scrollbar. Existing M11
selection, activation-on-release, double-click and cancellation remain the input
authority. Disabled buttons are drawn without registering activation targets.

Normal, hover, press, disabled, focus, selected and inactive states are separate.
Press replaces hover tint instead of compounding it: the initial compounded
dark-theme state fell below 4.5 contrast for accent `bbffee`. A 512-byte integer
sRGB table selects readable black/white text on custom primary accents, with no
kernel floating point or allocations. Meaningful control borders have their own
contrast color; decorative dividers remain lighter. Keyboard focus has a distinct
outline and does not activate the control.

The same contrast choice covers legacy Start badge letters, the desktop
Appearance glyph and selected filename/URL text. Text-editor carets use normal
ink rather than a possibly low-contrast decorative accent. Desktop text and
selection outlines choose foreground from the wallpaper. The new dark teal
accent exposed a legacy badge contrast of 2.890598; the consumer is migrated to
the shared foreground rule rather than avoiding the custom color in tests.

Pointer motion damages the previously and newly hovered controls. Scroll motion
damages its owner window. It does not introduce a continuous animation, polling
thread or per-window framebuffer. The native scrollbar uses real row counts,
keeps icon rows aligned, supports thumb dragging, track paging and keyboard
arrows/Home/End, and restores its starting position on Escape or Ctrl+Escape.
Routing requires the active native Files owner; USB, address fields, another
window and foreground dialogs retain their keyboard input.

## Typography and memory decisions

Existing OFL Inter remains the font. Body 16, secondary 14, section 21 and
heading 28 logical pixels are rasterized at their actual physical sizes for
100/150/200%. The 150% section mask rounds 31.5 physical pixels to 32. No enlarged
bitmap or runtime font interpreter is introduced. The M12 raster lock is separate
from M11, whose original output is checked unchanged.

An initial candidate could not reserve its fixed UEFI kernel range after adding
heading masks. M12 now omits unused legacy heading masks and shares the duplicate
42-pixel semantic face. Coverage is **251,248 bytes**, versus **270,910** for M11.6,
a reduction of **19,662 bytes**. Font coverage, fixed shell state, installer
payload, peak managed pages and retained pages are separate measurements. The
existing 1-MiB atlas bound and M12 incremental budgets remain enforced.

The scrollbar stores bounded owner/track records for eight windows and one
capture. It uses generation-bearing window tokens and clamps positions before
indexing. A native regression exposed stale scrollbar focus intercepting End in
the USB view; routing is guarded by owner, provider, foreground and field state.
No storage format or USB write permissions change.

The installed desktop object's BSS/data is 544,164 bytes (544,136 + 28),
336 bytes above the frozen M11.6 reference. This excludes read-only code/data,
including the separate 512-byte luminance table. Measured managed current/peak
is 4,288,512 bytes at ordinary size, 9,408,512 at 150%, and 33,370,112 at actual
4K/200%; shared framebuffer costs are included there. Theme cycling retains
zero additional managed pages. The five intentional boot-stress allocation
failures are unchanged, rather than being omitted from reporting. These numbers
are separate from firmware, configured guest RAM and the complete kernel image.

## Build, distribution and verification

`tools/build/m12.py --stage N` requires the previous stage's successful public
delivery and refuses to rebuild a published stage. M12 inherits working M11
features through explicit flags, but uses independent `M12STAGE<N>` media/maps,
manifests and evidence. BIOS chain handling and media naming include M12. Large
fixtures live outside OneDrive through the owned scratch junction. The matching
M12 distribution includes its own English welcome guide; historical M11 content
and accepted artifacts remain intact.

Production color tests cover all 16,777,216 RGB accents, 1,572,864 state cases and
4,096 scrollbar boundary cases, including independent floating-point reference
contrast. These host checks do not qualify runtime. Native checks use ordinary
guest input and read-only memory/framebuffer observation: real installation,
retained ISO, two unforced disk boots, light/dark states, release outside,
disabled/focus/field behavior, scrollbar cancellation/provider ownership,
actual 150%/4K, and cached/full movement comparison. The exact archived VMware
starter keeps all shipped devices enabled. BIOS is checked separately.

Idle measurement retains intermediate paint observations and requires a bounded
stable 600-ms window with halted CPUs; startup/status/minute-clock updates are
not discarded or called a continuous repaint. Three unstable windows fail.
Agent scenario/visual review is distinct from a human usability study.
