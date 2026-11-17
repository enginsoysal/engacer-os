# M12.11 — bounded native multitasking

Status: implementation and native qualification in progress. M12.10 remains the
completed tested download until the matching M12.11 publication gates close.

## How and why

Reuse the existing eight generation-bound window tokens and geometry state.
Alt+Tab presents original app icons and numbered document/folder identities,
including minimized and unsaved state. A snapshot preserves MRU order during
selection. Arrow/Tab selection changes no focus until Enter, Alt release or a
mouse choice; Escape cancels. No application thumbnail buffers are allocated. Selected labels and monochrome
layout icons use the same contrast foreground as the shared button style,
including hover/pressed/disabled states. A native pixel check guards against
drawing ordinary paper ink on an accent-filled selection. The first candidate
was deliberately stopped for this visual correction; it is diagnostic evidence,
not a qualified artifact.

The window menu adds **Arrange windows...**. Its Left half, Right half and
Maximize choices show a geometry outline before commitment. Cancel keeps the
original rectangle. Unsupported halves are disabled using actual app minimums,
with an explanation when selected by keyboard. Files uses its 500-pixel native
layout minimum. App minimums continue to be clamped to the actual work area.

Committing a supported half through the menu, Windows+arrow or edge drag offers
other real windows that can fit the complementary half. Choose a window or
leave that side unchanged. This is optional assistance, not a new desktop or
window quota. The chosen windows retain independent normal bounds; Restore
returns those bounds. No quarter layouts are advertised where apps cannot fit.

The shared overlay has switch, arrange and complementary-choice modes. It
reuses the existing eight-token array and selected index, adding only one owner
token and a side value (at most 16 logical bytes). Every action revalidates full
generation tokens. Missing owners cancel rather than acting on reused slots.
Active file-dialog owners cannot be rearranged and are excluded from snap
assistance. Switching focus preserves existing owner modality and dirty work.

## Alternatives and limits

Live full-size thumbnails and animated previews would add retained surfaces and
idle work; icons and accurate names provide bounded identification instead.
Half/maximize layouts reuse the tested geometry state machine. A second window
manager, arbitrary tiling or virtual desktops would widen this stage's scope.

The eight-window quota, implemented providers and actual display limits remain.
Physical/ARM, vendor GPU acceleration and arbitrary Windows applications are
not qualified by shell appearance. Agent scenario review is not a human study.
M12.14 retains feedback/transfer arbitration; M12.16 retains cursor/scale work;
M12.18 retains the BIOS/AHCI observation and complete final controller/app matrix.

## Verification contract

Freeze matching source/media through native install, actual switch/arrange/drag,
cancel, owner guards, minimum-size refusal and quota tests. Test compact light/
dark, actual 150% and physical 3840x2160/200%, independent installed starts,
exact enabled-device VMware, separate BIOS, movement equivalence and real boot
repair. Use two deliberately different pointer-moved normal rectangles when checking
independent restoration; identical defaults alone cannot detect shared restore
state. Measure retained pages, fixed bytes and halted idle CPUs. Publish only
after exact-source acceptance and fresh complete public delivery checks.

## M12.17 performance carry-forward

The instrumented eight-window 150%/4K journey takes substantially longer under
QEMU TCG than a single-window case. That observer duration is not FPS or a
VMware responsiveness benchmark. Source inspection finds that `round_alpha73`
still visits every shadow-interior pixel before skipping it, for each of eight
shadow layers and each repainted window. M12.17 should measure this separately
and evaluate equivalent bounded edge-span traversal before considering extra
retained caches. Preserve audio pumping, signed clipping, alpha coverage and
exact cached/full-frame equivalence. No renderer optimization is implemented
in M12.11.
