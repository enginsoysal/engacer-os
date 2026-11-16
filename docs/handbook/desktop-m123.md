# Use the M12.3 desktop

M12.3 passes its scoped native qualification. Use the matching
[installation guide](install-m123.md), [release scope](../releases/m123-v0.12.3.md)
and public media. Complete final M12 regression remains M12.18.

## Select, then open

The desktop has My files, Documents, Appearance and Recycle Bin references.
Your own objects live in `/Users/Owner/Desktop`. A single click selects an
object; double-click or press Enter to open it. Buttons and menu commands need
one click. Selected objects have a filled background; keyboard focus adds an
outline. Point to an object or focus a selected object to read its full supported
name above the grid when the two-line caption is shortened.

Use Ctrl-click to toggle selection, Shift-click to select a range, or drag a
rectangle from empty desktop space. Escape clears selection or cancels an open
menu. Arrow keys move to the next actual object on the corresponding row or
column. Home selects the first object; End selects the last user object and
shows its page. More desktop objects appear on Previous/Next pages. A disabled
page button does not change pages. Icons remain aligned automatically; free
placement is not part of this stage.

## Create and rename

Right-click empty desktop space and choose **New folder...** or **New text
file...**. Type a name and confirm. Ctrl+Shift+N also opens New folder. The new
object is selected and brought into view. Select a user object and press F2, or
choose **Rename...** from its menu. Cancel keeps the original name.

Names use the existing 1–63 ASCII-character limit. Unsupported characters and
trailing dots/spaces receive an explanation. The visual changes do not enlarge
the filesystem's limits.

## Shortcuts and folder pins

Right-click a native file or folder and choose **Create desktop shortcut**.
The resulting `.link` file is a reference. Open it with double-click or Enter.
Deleting the shortcut does not delete the original. A missing target explains
why it cannot open; it does not silently choose a different item.

Choose **Pin folder to Start** in a native folder's context menu to create a
saved Start reference. Unpin removes the reference. Recycling the underlying
folder removes its pin; restoring the folder restores the object, and you can
pin it again. Restore does not recreate removed customization automatically.

## Recycle and restore

Select a user object and press Delete, or choose **Move to Recycle Bin**.
Open the desktop Recycle Bin, select the recycled item and choose **Restore**.
It returns to its original folder when the destination is available. Name
conflicts or unavailable destinations are handled by the existing file reviews.
Permanent deletion and Empty Recycle Bin require their explicit review.

To remove a built-in icon, right-click it and choose **Hide desktop icon**.
Right-click empty space and choose **Restore desktop icons** to bring the four
standard references back. These display choices save immediately for your user;
you do not need to remove an app. Even with all four hidden, Start still opens
Files and Settings. Trying Delete explains the Hide route and cannot delete the
desktop, kernel or required services.
Optional applications and user shortcuts retain their independent lifecycle.

## Personalize and understand limits

Open Appearance, or right-click empty space and choose **Personalize**. The
desktop chooses icon ink from its actual wallpaper independently of the window
theme. Existing supported light/dark, scale and wallpaper choices remain
available. Use Save preferences when you want existing supported appearance
choices retained after restart.

M12.3 does not complete the later M12 Files/navigation, taskbar, accessibility or
hardware milestones. Native and USB capabilities remain different. Read the
matching installation guide and release scope before using a different device
profile. The earlier BIOS/AHCI test observation is still open; universal physical
hardware, Windows compatibility and GPU 3D are not claimed.
