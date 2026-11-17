# M12.14 — Feedback and preserved work

Status: implementation under native verification. M12.13 remains the qualified public download until the separate release and website gates pass.

## How and why

Reuse existing bounded message buffers and file-dialog/transfer owners. Avoid another process, retained notification surface or polling timer. Global shell messages appear in a bounded top-right card with an explicit Dismiss control; they yield to menus, modal reviews and dragging. File errors stay in the originating Files window. The card owns its hit region, so its body and Dismiss cannot click through to a caption or control underneath. Shared context menus have a 400-pixel body and two-line explanation footer, including protected and in-use item reasons. All geometry uses logical coordinates.

The existing cooperative transfer refuses admission when a dialog already exists. Open/Save as now also refuses admission during an active or waiting transfer or Windows file operation. Properties, Open with and transfer-result dialogs also refuse admission during an active operation. Editor Save preserves unsaved work during these operations. Refusal occurs before resetting picker state, changing its owner or publishing bytes. Existing conflict review and Keep both policies remain authoritative. This is admission control, rather than a hidden queue that might execute a stale destructive choice later.

Settings offers Show current dialog when a save or display choice is blocked by another valid dialog owner. It revalidates the current generation, restores/focuses that window, and neither accepts nor cancels the review. Input preferences and appearance persistence remain independent.

## Clear scope and state

Global Start search covers installed apps and pinned folders. Browse tabs lose their selected appearance during a query; category and grid controls are replaced by Clear search. Clearing returns to the retained browsing preferences. Editing a query clears stale pin-success feedback. No new app process starts while typing.

A new empty Editor document is labelled New document - not saved. Saved document requires an existing document entry after an actual successful Save. Failed saves keep the text and give a next action. Invalid appearance instructions refer to saving new choices rather than an internal record.

## Verification and limits

The stage tests actual installed guest input, persistent file bytes, both dialog/transfer admission directions, conflict ownership, an interrupted removable-source copy, compact light/dark, 150% and 4K geometry, no-ISO startup, exact enabled-device VMware media, BIOS startup, repair and pixel comparisons. Qualification results are recorded separately after these checks finish. Automated scenario/visual review does not establish a human usability study.

M12.16 accessibility/cursor/scale work, M12.17 rendering performance and M12.18 final controller/original-app regression remain separate ordered stages. Existing native filesystem, removable-media and Windows ABI limits remain in force.
