# M12 coherent desktop design contract

Status: M12.0 design baseline, authorized 16 November 2026. This specification and
[concept screens](figures/m12/overview.svg) are design, not native runtime proof.
[Ordered stages](../milestones/m12.md), [inventory](m12-inventory.md) and
[tokens](m12-tokens.json) govern implementation. Current native delivery is recorded in the
[handbook index](../handbook/index.md) and stage progress; M11.6 was the native
baseline when this original design contract was accepted.
The owner authorized proceeding with this baseline; agent review does not claim
that the owner or study participants reviewed the newly generated concepts.

## Original concept gallery

These are design diagrams with illustrative content, not guest captures or
evidence that the depicted functionality has shipped.

| Concept | Review focus |
|---|---|
| [Start and app identity](figures/m12/overview.svg) | Distinct icons, hierarchy, search and taskbar |
| [USB file browsing](figures/m12/files-usb.svg) | Shared frame, path, selection, metadata and capability limits |
| [USB without a connected drive](figures/m12/usb-empty.svg) | Back, sidebar and Refresh remain visible |
| [Settings and personalization](figures/m12/settings.svg) | Dedicated navigation, themes and display size |
| [Transfer feedback](figures/m12/transfer.svg) | Destination, confirmed progress and Cancel |
| [Installer disk selection](figures/m12/setup.svg) | Obvious selected row, Disk tools and review before erasure |

## Visual system and interaction

Recognize before reading; keep navigation stable; distinguish selection, hover,
focus and activation; provide useful feedback; preserve work. Theme data cannot
change device capabilities or destructive permissions.

Use original artwork with existing licensed Inter. Body is 16 logical pixels,
secondary 14, section 21 and heading 28. Use a 4-pixel spacing base, normally
8/16/24 for alignment. Default controls have 36-pixel hit height; setup primary
actions have 44. Light, dark and high contrast share layout and semantics.
Accent distinguishes selection/primary action rather than coloring every tile.

Controls define normal, hover, pressed, disabled and keyboard-focused states.
Objects also define selected and selected-but-inactive states. Focus is not
selection. Buttons activate on release inside the same target; files select once
and open on double-click or Enter. Selection never waits for a second click.

Primary captions fit fully. Long user names may ellipsize with a full-name tip
or Properties route. Prefer shorter clear actions over clipped labels. Enforce
text/layout bounds at actual scales. Unsupported 100/150/200% choices preserve
the previous usable setting. A resized screenshot never proves native 4K.

## Shared identity

App icons use a recognizable object/silhouette: calculator, clock, calendar,
terminal, archive, image or settings. Toolbar actions use restrained line icons.
Keep identity across Start, taskbar, captions, search and shortcuts. Provide
small-size simplifications, contrast and a deliberate generic fallback. Shipped
app icons must not normally be ambiguous letters. Share bounded raster caches
from original code/vector definitions; no copied Windows product assets.

## Desktop, windows and commands

Preserve real object identity, selection, grid alignment, labels, background
menus and protected base launchers. Shortcuts remain references. Close, unpin
and remove are distinct operations. Title bars contain accurate title and app
identity; active/inactive styles differ. Caption controls have pointer/focus
states and tooltips. Reuse M11 geometry/capture, restore bounds and safe clipping.
Blocked closing explains unsaved work and does not discard it.

Menus group applicable commands, preserve multi-selection and show shortcuts.
Keep them in the usable viewport with Shift+F10/arrows/Enter/Escape support.
Tooltips identify icons but never hide an essential instruction. Reviews block
only their owner and initially choose a safe action. Ordinary tasks avoid
unnecessary confirmation.

## One Files frame across providers

The common frame always owns title, Back, Forward, Up, address/breadcrumbs,
sidebar, toolbar and status. Location records include provider, device identity,
path and generation. History restores the real preceding location; Back is not
a renamed Home. Device removal invalidates the affected location with an
explanation, keeps navigation available and never silently targets another disk.

USB root, native Documents and an empty folder use this same frame. No-device
state keeps navigation and offers Refresh. Discovery/refresh exposes real
accessible drives. Provider-specific content must not replace the entire frame.
Capabilities determine commands; unavailable actions have a useful reason.

Details/icons share selection identity, scrolling, sorting and saved view.
Type/size/timestamps/previews require real metadata or supported decoders. Do not
invent timestamps or enlarge filesystem limits cosmetically. Dialogs reuse this
navigation model with suitable last location, validation, cancellation and
explicit overwrite decisions.

## Shell and preferences

Start retains local catalogue search, categories and pins with recognizable
identity and concise layout. No process per key or idle disk scanner. Broader
file search requires explicit indexing/query bounds. Taskbar grouping connects
pinned/running identity to actual windows, active/minimized state and bounded
overflow. Previews do not allocate full-size buffers for every window.

Snap/assist and switcher use actual geometry and the existing window quota.
Tray clock/calendar, device actions and safe removal use real providers.
Unsupported network/audio/battery functions are explained. Drawing controls
does not implement drivers, sleep, authentication or screen-reader compatibility.

Settings are versioned validated data with preview/apply/cancel/reset and usable
malformed-record fallback. Distro choices affect implemented behavior. Optional
app removal cannot remove Files, base Settings, recovery or safety checks.

## Feedback, setup and accessibility

Specify normal, empty, loading, busy, partial success, complete, unavailable and
failed states. Explain outcome, preserved work and next action. Notifications
are bounded/dismissible and not the only location of an important error.
Progress reflects confirmed work; cancellation preserves the only copy.

Setup adopts shared presentation while retaining eight steps, editable choices,
no writes before authorization, fresh erasure consent and truthful Ready.
Actual retained-ISO reset and detached boots remain required. First-start help
is optional and independent of removable apps.

Keyboard access, visible focus, contrast and scale participate from M12.1.
Semantic control names/roles/states form a foundation; a real accessibility
protocol and reader are required before claiming screen-reader support.
Reduced motion and high contrast are real settings. Agent novice scenarios
are not a human study.

## Resource and qualification contract

Retain the native compositor and shared font path. M12 incremental design budgets
above M11.6: 256 KiB new fixed shell state, 1 MiB shared icon cache and 64 KiB
transition scratch. These are budgets, not measured runtime claims. Report fixed
state, shared assets, peak and retained pages separately after every native stage.
No required blur, full 4K buffer per window, continuous idle animation or polling.
Transitions finish and stop; they can be disabled.

Use isolated `build/m12`, `dist/EngacerOS-M12*`, `tests/m12` and
`evidence/M12/<stage>`. Large owned fixtures live outside OneDrive. Never rebuild
accepted M11 artifacts. Freeze candidates while guests use their maps/media.
M12.18 repeats the complete required named-controller/device/original-app matrix;
stage evidence cannot qualify different bytes or universal hardware.

## Research and decisions

Microsoft references inform conventions; Engacer supplies its own code/assets.
Current Fluent principles inform coherence; historical desktop guidance informs
general interaction only.

- [Design principles](https://learn.microsoft.com/en-us/windows/apps/design/design-principles)
- [App icons](https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-design)
- [Explorer](https://support.microsoft.com/en-us/windows/experience/fileexplorer/file-explorer-in-windows)
- [Taskbar](https://support.microsoft.com/en-us/windows/experience/personalization/customize-the-taskbar-in-windows)
- [Common dialogs — historical](https://learn.microsoft.com/en-us/windows/win32/uxguide/win-common-dlg)
- [Keyboard accessibility](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/keyboard-accessibility)

Choose shared widgets/history/identity over per-screen cosmetic patches; solid
default surfaces over mandatory blur; capability-driven commands over fake
parity; preference data over app dependencies; actual task/boot/storage evidence
over screenshots alone. Each stage documents how, why, limits and verification.

## M12.8 native shared dialogs

[The implemented owner/IPC/validation decisions](dialogs-m128.md) and
[matching acceptance](../../evidence/M12/8/acceptance-results.json) qualify
native Open/Save as/Choose folder without another app-window slot. One bounded
picker adds 6449 fixed bytes; existing IPC input pages replace large temporary
stack payloads. This does not expand the foreign Windows common-dialog ABI.
[M12.14 feedback](feedback-m1214.md) now qualifies transfer/dialog admission; small-mode scale-choice
reconciliation and cursor isolation remain M12.16.

## M12.9 native Start and local search

[The bounded catalogue/layout decisions](start-m129.md) and [matching
acceptance](../../evidence/M12/9/acceptance-results.json) qualify native local
search, categories, pins and optional removal/reinstall with exact persisted
preferences. Fixed shell state and shared font bytes remain unchanged from
M12.8. Actual compact/150%/4K routes retain zero managed pages. [M12.14 feedback](feedback-m1214.md) now qualifies query/browse scope and notice lifetime. The taskbar and window stages have their separate matching acceptance.

## M12.14 native feedback

[Admission and feedback decisions](feedback-m1214.md) and [matching acceptance](../../evidence/M12/14/acceptance-results.json) qualify bounded messages, complete context explanations, actionable dialog recovery and preserved work without adding fixed shell state. Complete public publication passes for M12.14; M12.15 follows in order.

## M12.15 setup and first use

[Shared setup decisions](setup-m1215.md) and [matching acceptance](../../evidence/M12/15/acceptance-results.json) qualify the responsive native wizard, base-owned first use and optional-package-independent Settings management. Complete public delivery passes: twenty assets, 387 pages and 2,697 links, native homepage Save and actual desktop/mobile/manual/download/search/archive checks. The historical 502 remains recorded; fresh readback passes. M12.16 follows in order.

## M12.16 accessibility

[Accessibility decisions](accessibility-m1216.md) and [matching acceptance](../../evidence/M12/16/acceptance-results.json) qualify native keyboard routes, focus names, independent contrast/reduced effects, supported scales, cursor boundaries and modal ownership.
