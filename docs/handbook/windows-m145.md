# Original Windows menus, folders and browser downloads in M14.5

Native qualification passes within **M14-STAGE5-VM-v1**. Matching GitHub and complete actual website verification are being finalized. The owner made the reported missing BrixCanvas search/navigation nonblocking; their full browser test is not claimed as passed. Read the bounded original-window preview scope below.


## Use the included Windows app

Open Start, search for **Windows Apps**, and open it. Choose **Install 7-Zip**, review the confirmation, and install. **Open 7-Zip** runs the original Windows x64 console executable. The archive buttons create and extract a separate sample document in Documents. **Remove app** removes its unchanged application files and registration while preserving personal documents and modified files.

This remains one supported original MSI profile. **Open file manager** starts the original unmodified 7-Zip x64 application. This stage adds real menus, resource dialogs, toolbar images, list details and folder selection/navigation through the native compatibility APIs.

- Click **Documents** once to select it. Double-click to open it.
- Double-click a folder to enter it. Press **Backspace** to return to its parent.
- Open **Help**, choose **About 7-Zip**, then choose the actual **OK** button to return. The parent remains disabled while its modal dialog is open.
- Move, resize, minimize/restore, maximize/restore and close the original window normally. These routes remain independently checked.

These are the qualified preview tasks, separately from complete GUI archive, document editing and reusable installer support. Date text clips at the original application's requested column widths. Full header dragging, live directory notifications, shell extension menus and universal Windows controls are not qualified. The visible root labels, including Network, come from the original app and do not establish network-share support.

Notepad++ and SumatraPDF remain mandatory targets. Their original startup now passes actual page-protection changes and stops at missing fiber-local storage initialization before an interface. Neither app is advertised as usable. Full original installation/use/save/restart/removal tasks remain mandatory in M14.12 and M14.15; Firefox remains download-only.

## Check an EXE or DLL

In Windows Apps, choose **Check a Windows file**. Navigate with the shared file picker, select an EXE or DLL, then choose **Open**. This checks an AMD64 PE file's mapped layout, relocations and import structure in a protected worker. Read the result and use **More output** for additional details.

The check does not install or start the app. A successful mapping check does not establish that the application can start or complete its tasks. Only the documented process/thread/TLS and exception profile is supported; Windows GUI and arbitrary installers remain unqualified. Invalid, wrong-architecture or over-budget files are refused. Your selected original file is not changed. A missing function or unsupported operation is a compatibility result, not a successful application launch.

## Download Firefox

Open **Browser**, then choose **Browser choices**. Read the compatibility notice and choose **Download Firefox installer**. The Downloads window shows the real transfer from Mozilla and saves a new `.msi` file in your Downloads folder. It never launches automatically. Keep the supported network adapter connected; the existing HTTPS client also requires available hardware entropy and a valid UTC clock. If the connection fails, retry after checking the network. A cancelled or failed transfer must not publish a partial installer.

The pinned choice is the English Windows x64 Firefox 160.0.1 offline installer, about 91.5 MiB. Chrome, Brave and Microsoft Edge are also future candidates. Firefox installation and execution are not available in this stage. The existing basic browser still supports static HTML/plain text, with its documented script/layout limitations.

An independently verified complete file has SHA-256 `6dc28633cbd77cb1d044f339185cd467dda39397e4bcca942bfb0ddb2360c681` and length 95,924,224 bytes. Do not interpret a filename alone as proof of a complete download. [Mozilla release checksums](https://archive.mozilla.org/pub/firefox/releases/160.0.1/SHA256SUMS).

## Files and settings in this stage

The selected Windows API profile now has checked Unicode paths, case-insensitive lookup, shared access, existing-file edits, synchronous byte-range locks and durable user registry values. Process environments are private and copied when a child is created. Temporary files use atomic creation; caller-controlled environment values cannot grant access to another user's or system files.

User documents and their selected dates/attributes are stored independently of an app's directory. Removing the app must preserve them. Confirmed registry updates are durable. Flush or normal file close commits file changes; cancellation and unhandled faults discard unflushed changes. This is not a substitute for explicitly saving important work. The exact [implementation limits and verification](../architecture/files-m143.md) distinguish purpose-built Windows probes from actual supported original applications.

The Windows Apps UI exposes the supported original console profile and the limited original file-manager window preview described above. Complete GUI application tasks, other original installers and modern browser execution remain later gates.

## What follows

M14.5 adds native original windows/messages/input/lifetimes with drawing, menus, resource dialogs, images and folder/detail preview tasks while retaining selected file/settings/runtime profiles; later stages expand clipboard/shared dialogs, reusable installation services and required runtimes. M14.15 is the mandatory whole-system CPU/RAM/storage optimization gate. [Ordered M14 plan](../milestones/m14.md), [loader design and limits](../architecture/loader-m141.md).
