# M12.0 source-backed desktop inventory

Baseline: accepted M11.6, build `ea730e92bc70d0545b4b8f22385e31bc`.
This inventory separates proven behavior, appearance gaps and new work.
It establishes no new runtime qualification.

| Surface | Existing source / mechanism | Preserve | M12 gap / decision |
|---|---|---|---|
| Shared graphics | `kernel/core/graphics73.inc`, `include/engine/ui/graphics73.h` | Inter, scaling, clipping and shared composition | Semantic tokens and consistent widget states; M12.1 |
| Desktop | `kernel/desktop/session.c`, `files11-desktop.inc` | Selection, shortcuts, recycle and protected launchers | Shared identity, layout and labels; M12.2–3 |
| Start | `start11-ui.inc`, `start11-model.inc`, `start11-keys.inc` | Local search, catalogue, categories, pins and keyboard | Letter tiles, hierarchy and excessive empty area; M12.2/9 |
| Taskbar | `session.c`, `start11-actions.inc` | Real running/active/minimized state, pins, quota and safe power | Text-only identity and duplicate-looking groups; M12.10 |
| Windows | `window11.inc`, `window11-state.inc`, `window.c` | Geometry, resize, focus, snap, switcher and dirty-close review | Shared caption identity and inactive/button states; M12.4/11 |
| Native Files | `files11-ui.inc`, `files11-model.inc`, `files72.inc` | Metadata, sorted entry identities, real navigation and saved choices | Common frame, hierarchy, toolbar and address navigation; M12.5–6 |
| USB Files | `devices10.inc`, `devices10-controls.inc` | Capability guards, FAT32 copy, flush, safe removal and reconnect | Separate frame drops navigation and retains wrong title; M12.5 |
| File commands | `files11-actions.inc`, `files11-ops.inc`, `files11-context.inc` | Transactions, provider limits, conflicts and source preservation | Uniform commands and feedback; M12.7/14 |
| App dialogs | `session.c`, `apps74.inc`, `files11-keys.inc` | Owner focus, saved documents and cancellation | Shared Open/Save as/Choose folder; M12.8 |
| Settings | `devices10.inc`, `appearance11.inc`, `start11-actions.inc` | Actual capabilities, saved appearance and package independence | Coherent hierarchy, previews and tray entry points; M12.12–13 |
| Notifications | `session.c`, `devices10.inc`, `power11.inc` | Real results and work-preserving refusal | Bounded notifications and error vocabulary; M12.14 |
| Setup/recovery | `kernel/install/wizard6.c`, `wizard75-ui.inc`, `setup11-ui.inc` | Consent, quarantine, retry, repair and real reset | Shared presentation and terminology; M12.15 |
| First start | `guide11.inc`, `setup11-store.inc` | Optional base-only card and durable dismissal | Common shell vocabulary; M12.15 |
| Accessibility | `interaction11.inc`, `files11-keys.inc`, `start11-keys.inc` | Existing keyboard/selection contracts | Semantic identities, contrast, focus order and reduced motion; M12.1 onward / M12.16 |

## Owner-reported journeys

1. Start → Categories → Accessories: Calculator, Calendar and Clock share a C
   badge. Replace ambiguous placeholders with original recognizable icons.
2. Documents → USB drives: the title remains Documents and navigation disappears.
   Keep the common frame even without a device. Back restores the preceding
   location; Home remains a separate action.
3. Preserve working M11 selection, commands, stored files and geometry. They are
   not missing features to be reinvented merely for appearance.

## Capability boundaries

A unified frame does not grant USB delete/recycle/overwrite/format or new native
path/Unicode limits. Show metadata only when real. Network/audio/battery controls
need real providers. The eight-window bound remains until separately changed
and tested. Shell appearance does not expand Windows application compatibility.
