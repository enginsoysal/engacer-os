# M12.10 — grouped native taskbar

Status: implementation in progress; M12.9 is the completed tested download.

## How and why

Derive a unique bounded union of existing taskbar pins and live window app IDs.
Preserve pin order, then append running apps in model order. A pinned app and
its windows share one button and original icon. This avoids ambiguous duplicate
launch/window buttons without adding a second window manager or preference ABI.

One running window uses the existing guarded minimize/restore route. Multiple
windows open a real chooser. Each row starts with its live slot number, names
the document/folder or app, and identifies minimized/unsaved state. Choices
capture full generation tokens; closing/reusing a slot cannot target another
window. Closing continues through the existing unsaved-work/modal owner guards.

The selected app has the shared active control style and a wide indicator.
Other open groups have a short indicator, minimized-only groups have dots, and
multiple windows have a numeric badge. Unopened pins have no running marker.
Icons and text reuse the shared renderer; no preview framebuffer, process or
idle animation is created. Actual fixed-state and managed-page measurements
remain required before qualification.

## Bounds and access

There are twenty catalogue slots, eight live windows and eight taskbar pins.
The temporary app union is twenty integers; chooser labels are eight fixed
96-byte strings, independent of filenames' lifetime. Existing generation-token
storage is reused. One integer retains overflow page position. Visible app
buttons have 132-logical-pixel hit targets, separated by eight pixels; overflow
reserves a distinct More apps control. Width arithmetic avoids signed overflow.

Overflow shows hidden apps and supports bounded next/previous pages when needed.
Choosing from overflow focuses/restores a window instead of toggling an already
active window into minimized state; direct single-window button clicks retain
the normal toggle. The overflow control marks an active hidden app.
No menu exceeds the existing twelve-item capacity. Hidden running apps remain
reachable; all live windows remain subject to the existing eight-window quota.
Per-user pin order/alignment and optional package removal use the unchanged
validated preference record. Changes to taskbar observation in future test
harnesses must follow real grouped controls rather than assuming a separate
action-70 button for every window. Historical release tests remain pinned.

## Verification gate

Require actual single/multiple-window mouse and keyboard routes, active and
minimized states, context close with dirty work/modal ownership, overflow/pin
ordering/removal, ordinary installed starts, compact light/dark and native
150%/4K, matching VMware/BIOS media, resources and cached/full movement checks.
Host union/layout checks and screenshots alone are insufficient. Finish the
GitHub release and complete public website verification before M12.11.

M12.14 retains prior menu/conflict/query feedback and transfer/modal arbitration;
M12.16 retains scale/cursor isolation and M12.18 the earlier BIOS/AHCI stress
observation plus the complete final controller/original-app matrix.
