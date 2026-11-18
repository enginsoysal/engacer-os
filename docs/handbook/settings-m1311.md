# Find and change settings in Engacer OS M13.11

Development guide: use the matching qualified M13.11 testing release when published. Exact functional qualification is in progress; stability remains M13.13. [Release scope](../releases/m1311-v0.13.11.md).

Open Settings from Start or Appearance. Choose Appearance, Display, Input, System or Accessibility. Every available choice corresponds to an implemented control; unavailable hardware features are not simulated.

## Search and return to browsing

Click Find a setting or press Ctrl+F. Type a word such as dark, scale, keyboard, apps or contrast. The heading changes to Search results. Choose a category or press Enter for the first match. Clear search returns to categories. A search never applies preferences. Each Settings window keeps its own temporary query.

Search results omit unrelated appearance Apply controls. If an appearance preview is pending, the message tells you to clear search before applying or cancelling it. Escape first clears a nonempty query, then leaves the search field; it does not silently save a preview. F1 names the focused control, including Clear search.

## Preview, apply and cancel

Appearance previews accent, Light/Dark and wallpaper. Display previews a supported scale. Apply and save keeps the choices for your user; Cancel preview restores the previous session look without saving. Closing the owning Settings window also cancels its preview. A second Settings window cannot overwrite an active preview in another window.

A size that leaves too little room is refused with a useful message. File dialogs and operations must finish or be cancelled before saving appearance or changing display size. Show current dialog takes you back to the actual owning window.

If an appearance write fails, the preview stays visible. The message states that it was not saved and offers Try Apply again or Cancel preview. Cancel restores the earlier look and keeps other unsaved documents. A failing disk may need separate recovery; a retry is not a promise that the device is repaired.

Input and Accessibility keep their own explicit preference records. High contrast overrides the visible theme without replacing it; switching it off restores that theme. Removing an optional application does not remove base Settings or the desktop.

See [installation](install-m1311.md), [common dialogs](dialogs-m1310.md) and the [M13 plan](../milestones/m13.md) for current scope. The optional Off-by-default screensaver is available from Appearance → Screensaver. See the [personalization guide](personalization-m1311.md) for styles, timeouts, Preview, Apply and safe input wake. It has a separate saved record and Cancel changes route; it does not save or cancel your appearance preview.
