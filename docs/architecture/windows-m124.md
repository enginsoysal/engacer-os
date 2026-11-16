# M12.4 window and title-bar decisions

Status: implementation and qualification in progress. The current qualified
download remains in the [handbook index](../handbook/index.md). This document
does not claim that an untested development ISO is accepted.

## One geometry for drawing and input

`include/engine/ui/chrome12.h` defines the shared forty-pixel caption. Minimize,
Maximize/Restore and Close each have a 44 by 36 logical-pixel target. The app icon
has a 32 by 32 menu target. Drawing, pointer lookup and registered keyboard
controls use these rectangles. The outer edge remains available for resizing;
caption buttons take precedence over the former overlapping resize strip.
Gaps outside the drawn controls remain caption space rather than invisible
Minimize/Close buttons. Native Inter and the original app icon remain shared.

The active frame has a two-pixel border and accent underline. Inactive windows
use a quieter one-pixel border, muted title and different caption background.
Hover, press and keyboard focus are separate states. Close uses a red background
and white line artwork; all monochrome caption glyphs accept a semantic ink
override. This reuses the same vector shapes and bounded 512-byte row; it does
not introduce an icon cache, per-window framebuffer or heap allocation.

## Commands and ownership

Buttons activate on release inside the same target. Tab exposes caption actions
without activating them; Enter invokes the same validated command as a click.
The app icon and Alt+Space open the existing window menu. Maximize/Restore
preserves normal bounds; resizing respects actual application minimum sizes.
Existing signed clipping permits partially off-screen movement while retaining
a reachable caption. The menu anchor is clamped before unsigned layout arithmetic
so a negative window position cannot wrap its menu outside the display.

Close retains the existing unsaved-work review. Keep editing returns to the
document; an explicit Discard closes it. A file dialog blocks its own window's
caption controls without pretending that every other window is modal. Keyboard
commands use the actual owner: selecting the desktop must not let Alt+F4 close
the previously focused background window.

The caption labels are small, measured overlays shown on hover or keyboard
focus. They use native secondary typography and clamp inside the usable screen.
Old and new overlay rectangles are invalidated together. No animation timer or
idle polling is added. The M12.3 suppression of ordinary hover during caption
capture remains necessary for exact cached/full repaint equivalence.

## Scope and verification

Qualification must exercise real installation, retained-media reset and two
ordinary installed starts, caption states and ownership, all resize directions,
unsaved close, light/dark, real 150% and 3840 by 2160 rendering, exact shipped
VMware media, BIOS and cached/full movement comparisons. Host geometry and
contrast checks support those guest tasks; they do not replace native proof.
Memory and idle checks distinguish fixed shell state, retained managed pages
and configured guest RAM. Final comprehensive regression remains M12.18.

This stage does not add the later shared Open/Save dialogs, file navigation,
taskbar redesign, arbitrary Unicode names or vendor GPU acceleration. The earlier
BIOS/AHCI concurrent-install observation remains open until isolated and tested.
