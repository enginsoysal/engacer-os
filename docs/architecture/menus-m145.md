# M14.5 native menu development

This is a development contract, not complete original-application or stage
qualification. M14.4 remains the qualified download.

The runtime paints the application's actual process-owned menu tree. It does
not substitute an application-specific toolbar or send a fabricated command
from a test. Menu labels use native font measurement and copied draw commands.
Original procedures receive menu initialization, entry/exit, uninitialization
and the selected WM_COMMAND in their protected thread.

The top-level menubar occupies 24 logical pixels outside the client area.
GetClientRect, ClientToScreen, child screen rectangles, compositor placement,
native pointer translation and WM_SIZE all account for that same inset. This
keeps application content and its ordinary input below the menu instead of
painting labels over the app's toolbar. The former reserved word in the copied
window view reports menu height; record size and earlier field offsets stay
unchanged. The broker accepts only zero or 24, for an owned top-level window
on its own UI thread.

Menu drawing has a distinct retained surface so application BeginPaint cannot
erase the menubar. Its 64-command bound shares the existing global 128-page
drawing quota; application client drawing retains its independent 224-command
window limit. Metadata remains inside the existing checked one-page window
allocation. No additional fixed desktop array or polling thread is introduced.
All surface pages are freed on window/process/thread teardown.

The initial popup implementation uses an internal captured child overlay,
rendered after ordinary siblings. Paint order and hit order use matching
topmost/generation rules, including reused HWND slots. It shows real menu state,
disabled commands, separators, checks and submenu indicators. Pointer and
arrow/Enter/Escape input act on the actual menu model. Nested levels use a
bounded 16-level history; eight concurrent/reentrant tracks are allowed.
Visible rows are bounded to 28, with keyboard navigation scrolling larger
models. Its nested message loop blocks on the existing atomic queue wait.
The original focus returns after the overlay is destroyed and capture released.

This child overlay is constrained to its parent's client area. Arbitrary
desktop-spanning TrackPopupMenu, side-by-side cascading presentation, complete
mnemonic/Alt/F10 behavior, owner-drawn menu items and every accessibility route
are not qualified by this initial implementation. Resource/static menu
foundations do not establish Notepad++/Sumatra execution or full 7-Zip tasks.

Verification must distinguish the owned menu fixture from the unmodified
original executable. The owned fixture checks client/screen coordinates,
disabled-command refusal, actual pointer commands, nested keyboard commands,
Escape cancellation, callback balance and retained pages. The separate
original test reaches Help/About with ordinary pointer input, observes the
original resource/dialog callback, closes through its actual OK control and
checks original process cleanup. Failures stay preserved under the candidate
build ID; none of these checks alone closes M14.5.
