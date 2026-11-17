# Motion and resource use — M12.17

M12-STAGE17-VM-v1 native qualification passes. Use its matching M12.17 media; complete public delivery closes separately before M12.18.

Window movement and controls respond directly. Drag a title bar to move a
window; Escape during the move returns it to its previous position. A completed
move keeps a reachable title bar even when part of the window is outside the
screen. Ordinary Files navigation and Start remain available through their
keyboard and pointer routes.

Settings → Accessibility → Reduced motion removes decorative shadows, hover
washes and pressed-control movement. It saves independently of your normal
appearance. Turning high contrast off restores the appearance you selected.
Optional apps remain independently removable; rendering does not depend on them.

This release avoids scanning shadow pixels that would be covered by the window.
It adds no permanent per-window image buffers or idle animation workers. The
shared framebuffer still uses memory proportional to the physical display, so a
4K desktop uses more graphics memory than a compact desktop. Configured VM RAM,
fixed shell data, peak managed pages and pages retained after a task are distinct.

Read the matching release for measured profiles and limits. Host-observed event
completion and host raster benchmark times are not display refresh rates or
native FPS. Agent checks are not a participant usability study. Vendor GPU 3D,
universal hardware and expanded Windows application support are not introduced
by this rendering improvement.
