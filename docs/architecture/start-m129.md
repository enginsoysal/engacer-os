# M12.9 — Start and local search

Status: native qualification passes M12-STAGE9-VM-v1. Public release and
complete website verification remain separate gates before M12.10.

## Design and decisions

Start keeps the installed catalogue IDs, 32 Start pins, eight taskbar pins and
twelve configurable categories. The existing validated version-one preference
record remains readable without migration. Unpinning changes references only;
optional app removal still prunes its references without affecting the shell.

The ordinary panel uses a shorter 560-logical-pixel height where space allows.
A result heading identifies Pinned, Installed apps, a chosen category or local
search, and the visible range/total so pagination is discoverable. Existing vector icons retain app identity. Each result identifies an app
and its category, or a pinned folder; unavailable destinations remain explicit.
Search uses one full-width column so labels do not compete across narrow tiles.
Grid navigation uses the same column calculation as drawing, including a
defensive two-column branch for narrower logical widths. List preference, category labels and pin order are retained.

Search ranks case-insensitive exact labels, prefixes, then substrings, preserving
alphabetical ordering within equal ranks. The maximum catalogue/pin set remains
52 entries. It runs in response to shell drawing/input, without an index, disk
scanner, network query, per-key process, raster cache or new allocation. This is
installed-app/pinned-folder search, not full filesystem or Internet search.

Preserve the existing Enter-to-launch, arrows, Tab, context-menu, Escape,
category customization and explicit power confirmation routes. Typing must not
launch a process. Native qualification must check real launches, optional
removal/reinstall, persisted labels/pins/categories, compact/dark/HiDPI layouts,
idle/resource behavior and ordinary installed startup. Host ranking checks and
compile guards do not replace these guest checks or human usability studies.

## Publication gate

Do not mark this stage complete before matching-source native media, release
downloads, English manuals and fresh public website/homepage verification pass.
Later taskbar redesign remains M12.10. Existing M12.14, M12.16 and M12.18
carry-forward observations remain open in their respective scopes.

Visual review of the first prototype found a truncated New category button and
redundant pinned text in narrow grid cells. The next candidate widens that
button, retains pin status in full-width results, and shows result ranges. The
old prototype reports and controlled test stop remain in diagnostics; they do
not qualify the revised media.

M12.14 feedback follow-up: while a global query is present, the existing
browse-view/category affordances still refer to the saved browse preference;
search remains a full-width global result list. Make that scope explicit in
the visible controls and qualify it with ordinary input during feedback work.
Until then, clear the query before choosing the browse view/category.
Also qualify Start notice lifetime: a prior pin-success message can remain
visible during a later search instead of the ordinary privacy/keyboard hint.
It is informational; result matching and the no-results explanation remain
independent. The feedback stage should make that transition explicit.
