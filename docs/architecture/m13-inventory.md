# M13.0 baseline and gap inventory

Baseline: qualified M12.18, source `07743f643687544bb21dcd92a53a993141560cdd`, build `8ee102351039d96f68637a9edbff597b`. This is review of retained real native evidence and current source, not a new M13 runtime test or a fresh human study.

| Surface and evidence | Preserve from M12 | M13 gap / severity | Stage |
|---|---|---|---|
| [Real 4K Files](../../evidence/M12/18/feature.png), `kernel/desktop/files11-ui.inc` | Back/Forward/Up, provider identity, selection, safe removal | Major: navigation/command controls dominate composition; refine density, sidebar and status hierarchy | 1, 7 |
| [Start](../../evidence/M12/18/start-native/pinned.png), `kernel/desktop/start11-ui.inc` | Pins, local search, catalog and categories | Major: launcher composition and default hierarchy must read as apps, not a settings form | 1, 6 |
| [Compact disk choice](../../evidence/M12/18/setup-native-compact/disk-selected.png), `kernel/install/setup11-ui.inc` | Real selection, destructive review, retry and transaction guards | Major: clearer default route and partition explanation; distinguish recommended and advanced actions | 2–4 |
| [4K review](../../evidence/M12/18/setup-profiles/review-4k.png), `kernel/install/wizard6.c` | Real eight-step install and independent boot | Major: review the entire boot/install/restart chain, not only the final screen | 2–4 |
| [Desktop](../../evidence/M12/18/desktop-native/native-4k.png), `kernel/desktop/session.c` | Selection, shortcuts, protected launchers | Major: default wallpaper, icon rhythm, title-bar/taskbar balance and cohesive depth | 5–6 |
| [Taskbar overflow](../../evidence/M12/18/taskbar-native/overflow-with-eight-windows.png) | Group ownership, eight-window quota, overflow | Major: reduce button-like clutter while making running/active/grouped identity obvious | 6 |
| [Save As](../../evidence/M12/18/access-ownership/save-as-focus-help.png) | Owner-bound modal, dirty work, keyboard routes | Major: carry shared visual density and hierarchy through every secondary dialog | 8, 10 |
| Settings/notifications, `kernel/desktop/appearance11.inc`, `devices10.inc` | Real persistence, invalid-value recovery, capability guards | Major: coherent categories, actual supported search and concise message vocabulary | 8, 10–11 |
| Pointer/drag/resize and renderer, `kernel/core/graphics73.inc` | Signed clipping, partial redraw, idle halt | Major: measure whole-journey visible response; still screenshots do not establish smoothness | 5, 9 |
| [Website audit](../../evidence/M12/18/website-audit.json), `website/brix/navigation.mjs` | Stable article URLs, canonical source, official hashes | Major: current guides mixed with milestone history; too much list-like discovery | 0 |
| BrixCanvas public `/search` and native Search preview, inspected 17 Nov | Existing real title/body search and URL fallback | Major: separate search page interrupts reading; overlay/ranking/focus return need a separate production capability | 0 design / tracked portal implementation |

Severity is a design-review priority, not a newly reproduced kernel fault. All caption/window state, storage/provider limits, compressed installer/repair, disabled capability explanations, keyboard guards and measured resource behavior qualified in M12 must be preserved. The older BIOS/AHCI stress trigger remains unidentified; its final scoped repeat pass is not a universal fix. Boot-attached USB at the documented 64-MiB UEFI profile remains unqualified.

## Required coverage before the last appearance release

Boot choices, loading, every installer/repair/disk/error state, first use, desktop objects and menus, Start/search/categories, taskbar/tray, window controls/snap/switcher, Files all providers, transfers/conflicts, Open/Save/Properties, Settings, optional-app framing, notifications, shutdown and restart. Each surface needs normal/empty/hover/focus/selected/disabled/busy/error coverage where applicable, plus long text, scaling, keyboard and recovery.

M13.0 provides the inventory and designs. M13.1–M13.12 supply the native changes and measurements; nothing in this inventory marks them complete.
