# Windows files and browser downloads in M14.2

Status: native qualification passes within M14-STAGE2-VM-v1. Actual website publication is being verified; read the matching release scope before testing.

## Use the included Windows app

Open Start, search for **Windows Apps**, and open it. Choose **Install 7-Zip**, review the confirmation, and install. **Open 7-Zip** runs the original Windows x64 console executable. The archive buttons create and extract a separate sample document in Documents. **Remove app** removes its unchanged application files and registration while preserving personal documents and modified files.

This remains one supported original MSI profile. Other MSI installers, the 7-Zip Windows file-manager interface, Notepad++ and SumatraPDF are not qualified for installation and use in this loader stage.

## Check an EXE or DLL

In Windows Apps, choose **Check a Windows file**. Navigate with the shared file picker, select an EXE or DLL, then choose **Open**. This checks an AMD64 PE file's mapped layout, relocations and import structure in a protected worker. Read the result and use **More output** for additional details.

The check does not install or start the app. A successful mapping check does not establish that the application can start or complete its tasks. Only the documented process/thread/TLS and exception profile is supported; Windows GUI and arbitrary installers remain unqualified. Invalid, wrong-architecture or over-budget files are refused. Your selected original file is not changed. A missing function or unsupported operation is a compatibility result, not a successful application launch.

## Download Firefox

Open **Browser**, then choose **Browser choices**. Read the compatibility notice and choose **Download Firefox installer**. The Downloads window shows the real transfer from Mozilla and saves a new `.msi` file in your Downloads folder. It never launches automatically. Keep the supported network adapter connected; the existing HTTPS client also requires available hardware entropy and a valid UTC clock. If the connection fails, retry after checking the network. A cancelled or failed transfer must not publish a partial installer.

The pinned choice is the English Windows x64 Firefox 160.0.1 offline installer, about 91.5 MiB. Chrome, Brave and Microsoft Edge are also future candidates. Firefox installation and execution are not available in this stage. The existing basic browser still supports static HTML/plain text, with its documented script/layout limitations.

An independently verified complete file has SHA-256 `6dc28633cbd77cb1d044f339185cd467dda39397e4bcca942bfb0ddb2360c681` and length 95,924,224 bytes. Do not interpret a filename alone as proof of a complete download. [Mozilla release checksums](https://archive.mozilla.org/pub/firefox/releases/160.0.1/SHA256SUMS).

## What follows

M14.2 adds bounded native process/thread/TLS and selected C exception/unwind behavior; later stages add the original Windows GUI, controls, dialogs and reusable installation services. M14.25 is the mandatory whole-system CPU/RAM/storage optimization gate. [Ordered M14 plan](../milestones/m14.md), [loader design and limits](../architecture/loader-m142.md).
