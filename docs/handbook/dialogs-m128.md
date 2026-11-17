# Open, Save as and Choose folder

M12.8 is in development. The qualified download remains M12.7 until its matching
release and public verification are complete. This guide describes the implemented
shared native dialogs; pending qualification is not a completed release.

## Open a file

In Text Editor choose **Open**, or press **Ctrl+O**. Image Viewer and Archive
Manager also provide **Open**. Choose Home, Documents, Downloads or Pictures,
or edit the location field. Back, Forward and Up navigate folders. A single
click selects an item; double-click or Enter opens it. The file-type button
switches between the app's supported extensions and All files. All files does
not expand the app's supported formats or size limit.

Text Editor accepts supported ASCII text of at most 8,191 bytes. Image Viewer
opens supported BMP files; Archive Manager opens supported ZIP archives. To
edit a file on USB, first copy it into Downloads using Files. Direct USB editing
and replacement are not supported by this dialog.

An unsaved text document requires a separate decision: Save and open, Discard
and open, Back or Cancel. Back and Cancel keep your work. A failed source check
does not replace the current document.

## Save with a different name or location

Choose **Save as**, or press **Ctrl+Shift+S**. Choose a writable personal folder,
enter a filename and choose Save. Text type adds `.txt` when no extension is
supplied. All files preserves your chosen extension. Names use 1–63 supported
characters and cannot end with a space or dot.

If a file already exists, review its name and choose Replace explicitly. Back
returns to the picker; Cancel closes it. If another app changes the target
after review, review it again. A protected folder, open target or storage error
does not authorize replacement. Keep the dialog open to correct the choice,
or cancel and retain the document.

New folder is an explicit create operation. Enter a valid name and choose Create
and open. This makes the folder; it does not save the document until you choose
Save. Cancelling later does not remove a folder you explicitly created.

## Choose where to extract an archive

Open a supported ZIP in Archive Manager and choose **Extract to...**. Choose a
writable personal folder, then confirm. Extraction creates a new uniquely named
Extracted subfolder there, retaining the ZIP. Existing format, quota and transfer
limits still apply. If extraction stops, inspect any partial output in Files;
the dialog does not claim that all members were extracted.

## Navigation and remembered choices

Use Tab and Shift+Tab to move focus, Ctrl+L to edit the location, Alt+Left/Right
for history and Alt+Up for the parent. Escape returns from a review before
cancelling the picker. At most eight navigation locations are retained.

Successful Open, Save as and Choose folder choices remember separate locations
for the current user. Cancel does not update them. Missing or invalid optional
preferences fall back to a usable default. The dialog uses its owner's existing
window slot; finish or cancel it before requesting another file dialog. Finish
or cancel an active file transfer before opening a file dialog in this stage.

See [the architecture and qualification contract](../architecture/dialogs-m128.md)
and [the currently qualified installation guide](install-m127.md).
