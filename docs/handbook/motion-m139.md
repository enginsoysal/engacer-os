# Pointer and window movement in M13.9

M13.9 refines native motion and pointer feedback. Use the matching ISO or VMware ZIP from the M13.9 release. Installation follows the [step-by-step guide](install-m139.md).

## Resize and move

Move the pointer to an edge or corner: the horizontal, vertical or diagonal arrow shows the available resize direction. Hold the left mouse button and drag. Release to keep the bounds; Escape cancels and restores them. Drag the caption to move a window. The existing snap preview, minimize, maximize and restore controls retain each window's owner and normal bounds.

## Text fields and selection

Search boxes and supported editable fields show a text cursor. Moving the pointer does not launch an app, change the insertion point or select a file. Click once to select an item; double-click or Enter opens it. Text cursor shapes do not add selection support to a view that does not implement it.

## Scaling and resource use

The cursor outlines are generated at the current supported scale. They do not stretch a small bitmap or allocate a framebuffer. Completed motion tasks retain no extra managed pages in the named tests. Configured VM RAM, framebuffer storage and fixed kernel state are separate measurements.

## What the measurements mean

The release reports native input receipt through completed CPU composition/framebuffer/cursor writes, and separately the host observer's exact visible pixels and timings. Native completion is not physical scanout or GPU FPS. External observation targets remain disclosed where unmet. This stage does not qualify vendor 3D, every physical GPU or general Windows apps.

Stability investigation, freeze/reset diagnosis and long-duration acceptance are deferred exclusively to M13.13. Keep test work separate from personal data until that gate passes.
