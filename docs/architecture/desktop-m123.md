# M12.3 desktop and shortcut decisions

Status: implementation and qualification in progress. M12.2 remains the public
qualified download until the M12.3 native and publication gates pass.

## One bounded grid

The desktop uses shared 120 by 96 logical-pixel object cells, with 128 by 104
spacing. Four built-in references lead the grid: My files, Documents, Appearance
and Recycle Bin. User objects come from the real per-user Desktop directory.
The original M12 icon renderer draws 48-pixel vector identities; labels use the
same native Inter body typography and two-line limit. Hover and selection have
different backgrounds; keyboard focus has an additional outline. A focused or
hovered user object's full supported name is also shown above the grid.

`include/engine/ui/desktop12.h` owns geometry and spatial neighbors. Rendering,
hit targets and marquee intersection use the same rectangles. The previous
hard-coded three-launcher hit strip is disabled for M12. This prevents visible
art and input bounds from drifting. The helper reserves enough columns for all
four built-ins at short display heights and caps each user page at 128 objects.
Previous/Next expose overflow without placing icons underneath the taskbar;
unavailable page buttons have disabled styling and no activation target.

We chose deterministic alignment rather than adding a position database or
per-object buffers. Free placement, arbitrary icon sizes and arbitrary Unicode
filenames are not introduced by this stage. Existing filesystem name and entry
limits remain real. Arrow keys find the next actual object on the corresponding
row or column, skipping the empty reserved-grid gap. Home/End and range selection
retain their distinct meanings. Newly created desktop objects are selected and
their page is revealed.

## References and safe file operations

A single object click selects; a double-click or Enter opens. Context commands
activate once. Tab-focused desktop controls route to the same validated open
operation. Built-in references are protected launchers, separate from removable
user shortcuts and optional applications. Their removal cannot delete required
services. The background menu exposes creation, Desktop in Files, Recycle Bin,
Personalize and supported clipboard/Undo actions.

The Recycle Bin opens the existing real per-user recycle provider in Files.
Native file actions retain the M11 transactional implementation, metadata/CRC
checks and original-location Restore. Shortcuts retain the versioned validated
reference format: removing a shortcut leaves its target unchanged; unavailable
targets explain their failure without executing another file. Folder pins reuse
the existing persisted Start preferences instead of another desktop-only pin
store. No new disk layout or settings format is introduced.

## Resources and qualification

There are no new heap allocations, timers, idle animations, per-icon raster
caches or per-window framebuffers. Grid state is computed from existing display,
selection and directory state. Fixed state, transient stack use and managed
framebuffer allocations are measured separately during qualification.

Host checks exhaustively inspect bounded, non-overlapping cells over more than
ten thousand display geometries and compare spatial navigation with an
independent nearest-object oracle. They do not prove native input or persistence.
Native tests separately traverse installation, selection, context commands,
rename, shortcuts, pinning, recycle/restore, overflow, disk-only restarts,
ordinary/150%/actual 4K display, idle behavior and retained memory. Exact packaged
VMware and BIOS qualification are separate required records. Native captures
and a five-question visual/scenario review will accompany acceptance; these are
agent review, not a human usability study.

The earlier M12.2 BIOS/AHCI timeout observation remains open. A passing repeat
does not isolate its cause. Complete controller/application/device regression
remains M12.18; universal hardware, Windows compatibility and vendor GPU 3D are
not qualified by desktop changes.
