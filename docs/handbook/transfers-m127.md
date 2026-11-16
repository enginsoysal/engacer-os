# Copy, move and manage files in M12.7

M12.7 passes M12-STAGE7-VM-v1. Use its [matching installation guide](install-m127.md)
and public release; final M12 regression remains M12.18.

## Find an action

Open **Files**, then Home, Documents or another folder. Click an item once to
select it; double-click or Enter opens it. The toolbar's **Actions...** menu
contains Copy, Cut, Paste, Rename, Recycle, New folder, New text file, Undo,
Properties and the last transfer's details. This menu remains visible when the
window is small. Wider windows also have direct Copy and Cut buttons.

Right-click a selected item for its applicable commands. A muted action is
unavailable for that selection or location. System files are protected. Select
your own files and close an app using an item before moving or renaming it.

## Copy or move

1. Select the source item. Use **Copy** (Ctrl+C) to keep the original, or **Cut**
   (Ctrl+X) to move a supported native item.
2. Open the destination folder with Places, the address field or Back/Forward.
3. Choose **Paste** (Ctrl+V).
4. If a name already exists, choose **Keep both**, **Skip matches** or **Cancel**.
   Explicit **Replace files** is available only for supported closed native
   files. Replacing discards the old destination's contents after verification;
   the source remains.
5. During a longer transfer, read its phase and destination in the bottom strip.
   **Cancel** stops unfinished work safely. Already completed items remain.

**Details** is available after completion, cancellation or a stopped job. It
reports confirmed items. A cancellation does not remove earlier completed
copies. An incomplete file is not published as a completed destination.

**Undo** reverses the last supported single action only while the resulting
item remains unchanged and unused. It is not a history of every operation.
Renaming, moving, recycling and removing have different meanings: use Recycle
Bin's **Restore** to recover a recycled file. Permanent deletion has its own
explicit review and cannot be undone.

Renaming, moving or recycling an item clears the current file clipboard under
this stage's retained move policy. Copy or Cut again before pasting elsewhere.
Paste is muted when that clipboard is empty; Ctrl+V explains the next action.

## USB files

Choose **USB drives**, select a connected drive, then double-click or Enter.
Select one file and choose **Copy to Downloads**, or Copy and Paste into a
native folder. Existing names use the same Keep both/Skip/Cancel review. USB
folder imports and Cut/Move of USB sources are unavailable. Imports are limited
to one file at a time and 64 MiB per supported file.

A long import can be cancelled between small read/verification steps. Keep the
drive connected until completion. If it is removed while reading, the operation
stops and its unfinished native destination is not published. Completed files
remain available; inspect Details and reconnect explicitly to start again.

To export a native file, right-click it and choose **Copy to USB...**, select the
drive and folder, then **Copy here**. Export is create-only: an existing USB file
is kept. This export step currently runs synchronously and cannot be cancelled
mid-file. Do not unplug during export. Choose **Safe remove** before unplugging.
The USB filesystem and device write support still determine what is possible;
showing a drive does not imply unrestricted formatting, moves or folder writes.

## If an action is unavailable

- Nothing selected: click one of your files first.
- Protected folder: choose Home, Desktop, Documents or another writable folder.
- Another transfer: wait or Cancel it before changing more files.
- Matching name: review Keep both/Skip; no overwrite occurs by default.
- Drive removed: keep the completed files, reconnect and select the drive again.
- Disk or quota failure: inspect Details; completed items and copy sources remain.

See [Files views and names](files-m126.md) for presentation, and the
[navigation guide](files-m125.md) for Back, Forward, addresses and disconnected
locations. This guide describes the tested M12.7 native scope. Read its matching release
and retained limits; later providers and final regression are separate work.
