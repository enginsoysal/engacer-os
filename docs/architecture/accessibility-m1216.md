# M12.16 native accessibility

M12-STAGE16-VM-v1 native qualification passes. Complete public delivery passes: twenty downloads, 395 pages and 2,749 HTTP links, with native Save and desktop/mobile/manual/search/archive readback. M12.17 follows in order.

## Independent preferences

Accessibility uses a separate per-user 16-byte native record: magic, version,
flags and a zero reserved word. The existing filesystem CRC protects the record;
semantic validation also checks its exact length, magic, version, allowed two
flag bits and reserved value. Invalid or missing data activates safe defaults.
A malformed existing record is identified in Settings without silently rewriting
it. Choosing a setting writes and flushes a valid record before changing the
active flags. I/O failure retains the previous choices.

The high-contrast and reduced-effects bits do not repurpose the 352-byte
appearance record or assign an unsupported third value to its Light/Dark field.
Contrast overrides the shared palette for this session while the original
appearance remains intact. Turning it off restores that appearance. Resetting
accessibility affects these flags alone. Busy file operations retain ownership;
Settings refuses a competing accessibility write with an explanation.

## Native controls and visible focus

Settings adds an Accessibility category using the existing native control
renderer. High contrast supplies black surfaces, white text/borders and yellow
selected controls. Rendering that previously chose a dark/light background uses
an effective dark choice without modifying the saved preference. The desktop
wallpaper is visually overridden rather than rewritten. Keyboard control focus
has a stronger inset; the clock and system indicators have explicit visible
focus on their dark taskbar background. The first-start card has its own
contrasting border, resolving the M12.15 observation.

Reduced motion removes decorative shadows, pressed-text nudges and hover washes.
Interaction feedback remains immediate. The compositor has no timed transition
engine; this option does not pretend to disable animations that do not exist.
There are no new workers, timers, app windows or framebuffer caches.

## Keyboard regions and current-focus semantics

USB HID and PS/2 translate F6 and F1 into the same native broker actions. F6 and
Shift+F6 cycle available window, taskbar, desktop and notification regions. Tab
and Shift+Tab traverse actual registered controls; unavailable controls are not
invented. Enter and Space activate supported buttons and checkboxes. Existing
text fields keep their own typing and selection behavior. File review, guide,
tray, menu and drag owners retain their existing keyboard ownership; F6 does
not escape an active review.

The renderer captures the actual name of the current focused control into one
bounded semantic record containing its full window generation, action, role
and an 80-byte label. Named icon buttons, apps, file/folder items, desktop
references and tray actions provide names at their real drawing sites. Roles
include button, text field, item and checkbox; checked state remains explicit
in the checkbox label. This avoids allocating an array of labels for all 2048
possible registered controls. Owner generation and current registration are
validated before help consumes a record.

F1 is a real native visual consumer of that record. Focus Help uses a second
bounded copy while its card owns input. Escape closes only the help and restores
the still-valid original control; existing documents and file reviews remain.
The two records and four state words have a compile-time bound of 224 bytes.
The picker owns a separate actual dialog focus index. Focus Help reads that
index and its current purpose/review/selection directly, then returns to the
unchanged dialog focus rather than restoring an unrelated window control.
F1 does not implement an external screen-reader protocol or a speech reader;
those require a separate working service and consumer before qualification.

## Scale and cursor qualification

Explicit M12 display choices use the same logical 800×600 minimum as compact
startup. A choice that would produce a smaller workspace remains refused;
1280×1024 at 200% is not admitted. Legacy non-M12 scale limits stay unchanged.
Advanced partition tools retain their separately documented 1024×768 minimum.

Native tests isolate the previous cursor observation using settled physical
input coordinates, logical hit coordinates, the actual cursor rectangle and
real front-buffer pixels at 150% and 200%. A framebuffer screenshot alone is
insufficient to identify an input defect. Ordinary, compact and physical 4K
captures, preference bytes, retained/peak memory and idle halt remain separate
checks. Automated task and visual review are not a human usability study.

## Cursor and screen boundaries

The pointer hotspot can reach the last physical row and column. The renderer
clips the cursor rectangle at the physical viewport instead of moving its
hotspot to fit the entire arrow. The direct-framebuffer fallback remembers
the previous clipped dimensions so restoring a saved cursor never uses the
new rectangle width. Physical input, logical hit testing and cursor rendering
retain the same scale conversion. Actual 150% and 200% native observations
compare front VRAM with the compositor shadow and exercise real scaled clicks.
