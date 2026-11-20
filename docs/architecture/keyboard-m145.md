# M14.5 keyboard translation and cursor development

This is development behavior, pending qualification on the next frozen native
candidate. M14.4 remains the qualified public download.

## Translation and input scope

MapVirtualKeyW implements the five documented mapping modes. Factual US scan,
character and extended-key tables were measured through read-only calls to the
host's already installed explicit 04090409 layout. No host layout was activated,
installed or changed, and no Windows source or executable content is included.
The recorded reference and table digest are preserved in development evidence.
The own mapping core independently matches 2,304 reference calls; additional
native-Dvorak and boundary assertions bring the mapping check to 2,326. A further 95 printable-character comparisons
against VkKeyScanExW bring the complete host check to 2,421. These are
host checks, not proof that original app keyboard tasks work.

The active native layout is queried through the existing checked UI operation.
Native Dvorak remaps follow input10_hid's logical key positions. Ordinary native
key messages now carry matching scan and extended-key fields instead of zero
scan codes. Home, End and Delete join the existing navigation-key bridge.
Shifted digits retain their actual digit virtual key: exclamation mark uses
Shift+1, rather than VK_PRIOR merely because its character value is 33.
The unmodified original 7-Zip Backspace task must still pass natively.

The factual US tables occupy 2,176 read-only bytes; Dvorak transformation is
bounded and uses no allocation. US queries use direct table lookups. This is
not whole-OS memory or performance qualification. M14.15 remains mandatory.

The current bridge represents ordinary translated keystrokes as complete
keydown/character/keyup cycles. Modifier holds have actual input snapshots.
This is not complete physical letter-hold/repeat, Raw Input, IME, arbitrary HKL,
gaming keyboard or all shortcut interoperability. GetKeyState/GetKeyboardState
follow the requesting thread's consumed broker input; posted messages and
PM_NOREMOVE do not fabricate transitions. Keep these limitations visible while
extending the original application corpus.

[MapVirtualKeyW contract](https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw).

## Cursor ownership and stationary updates

Real pointer hit testing chooses the application-owned child HWND for
WM_SETCURSOR before mouse motion. Parent procedures may override it; the default
procedure revalidates the child after the callback and applies its class cursor.
The same root remaining under the pointer no longer suppresses cursor messages.
The own native fixture checks text-field and client-arrow transitions.

A cursor/motion pair may replace an older, wholly pending pair for the same
HWND. Keys, buttons, other windows and application-posted messages remain
ordering barriers. This keeps the existing bounded queue and input reserve;
there is no new timer or idle polling worker. Host queue tests independently
check pair replacement and barriers, plus the earlier randomized queue corpus.

The graphics cursor setter reports a real shape change. The foreign compositor
redraws the cursor immediately on that change, including while the pointer is
stationary; unchanged shapes do not cause repeated redraw. Native visible-cursor
and screenshot checks are still required before describing this fix as qualified.

Development `9dadeb6f2a2fa2ba91d972128491d63b` passes the enhanced native
consumed-input/shifted-character/cursor fixture with zero retained pages. Both
visible edit and arrow captures were independently inspected. The unmodified
original 7-Zip also completes Backspace navigation and retains only its known
one-page shared registered-format cache. Complete M14.5 qualification remains
open. The subsequent checked subitem callback/cache implementation passes owned tests and original visible file-size/navigation checks; full integration and public release are still required.
