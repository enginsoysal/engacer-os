# Find apps and switch work in Engacer OS M13.6

This guide describes the M13.6 Start, taskbar and system-tray implementation. Qualification and current downloads are reported in the [stage record](../milestones/m13-6.md); do not assume a development build is already the qualified download.

## Find and open an app

Choose **Start**, or press the Windows key. Pinned shows recognizable app and folder icons with their names below. Click a tile once to open it. Start buttons and tiles need one click; desktop and Files objects retain single-click selection and double-click/Enter opening.

Type an installed app or pinned-folder name into Search. Results update locally without opening an app; Enter opens the chosen result. Up/Down and Left/Right navigate the actual drawn grid. Home/End reach its ends. Tab moves through controls. Clear search returns to browsing. Escape first clears a nonempty query; another Escape closes Start. No-results offers a shorter query or All apps. Search covers app names, pin labels and category aliases, not full-disk file contents.

All apps lists the installed catalogue. Grid/List changes presentation. Categories is optional. Previous/Next page through larger result sets without hiding controls. Right-click a result (or Shift+F10) to see its supported pin/category actions. Unpin removes a shortcut, not the installed app or folder.

## Keep your own layout

Choose Customize to manage Start pins, category names/order/visibility and taskbar pins/alignment. These choices belong to your user and save automatically; a save failure explicitly says the change is session-only. Renaming a pin changes its displayed name, not the original file/app. Hidden categories remain searchable. Restore defaults reviews the layout reset and keeps files and installed apps.

## Return to your work

The taskbar has one icon and short label per pinned or running app. An unopened pin has no running mark. A running app has an underline; the active app has a longer accent mark. An app whose windows are all minimized has two small marks. Several windows show a count. Choose its group to select the particular window; dirty documents and minimized windows are identified in the chooser. A single active-window group minimizes it; choose it again to restore. More apps exposes groups that do not fit. Alt+Tab switches real windows.

Right-click an app group for supported window and pin commands. A saved-layout notification has a visible Dismiss; use it before a caption that it covers. Compact notification placement is being refined in M13.8. Unsaved documents and active file pickers keep their existing reviews and ownership guards. Removing an optional app cannot remove the desktop; close its active windows before removal. An eight-window limit explains when a window must be closed first.

## Network, sound, USB and time

Choose a status icon or press Windows+A for the system panel. Quick settings reports the real local wired-network state and software PCM playback level. A local DHCP address does not prove Internet access. Wi-Fi, Bluetooth and battery providers are explicitly unavailable in this build. Volume changes while a picker owns dirty work are session-only and do not interrupt that work.

USB drives lists readable removable providers. Opening a drive does not format it. Safe remove waits for the provider flush before unplugging. A replacement drive must be chosen explicitly; an older held click cannot safely remove its replacement. A no-device panel keeps navigation and explains what to connect.

The date/time area opens the UTC calendar. Previous/Next month and Today use the actual clock values. Open Calendar opens the selected date in the optional Calendar app. Close or Escape returns to work without creating an extra panel window.

## Power and safe cancellation

Start > Power offers Restart and Shut down with explicit confirmation. Cancel keeps the session. Save dirty work and finish/cancel transfers before power actions. A refused flush or owned operation cannot be reported as successful shutdown. Use the [installation and recovery instructions](install-m135.md) appropriate to the currently qualified release until the M13.6 release is published.
