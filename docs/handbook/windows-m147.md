# Original Windows MSI applications in M14.7

**M14.7 native/source/media qualification passes.** These instructions cover the tested original MSI profiles. Installing the Notepad++ package does not qualify using its editor or arbitrary Windows installers.

## What works in this release

| Application | Installation and removal | Using the application |
| --- | --- | --- |
| 7-Zip 26.06 x64 MSI | Original files, settings, shortcuts and recovery | Console archive tasks and the qualified graphical previews |
| Notepad++ 8.9.9.1 x64 MSI | Original installation, language actions, removal and reinstall | The editor remains unqualified |
| SumatraPDF | Installation remains unqualified | Interface remains unqualified |
| Firefox | Installer download only | Installation and browsing remain unqualified |

Windows program instructions run through Engacer OS's own kernel and compatibility APIs. An embedded Windows guest does not perform the installation. Compatibility belongs to the tested application/version/task profile; reading a package's name is not proof that its application can run.

## Install the included 7-Zip

1. Open Start, search for **Windows Apps**, and open it.
2. Choose **Install app**. Read the product identity and confirmation, then choose **Install app** again.
3. Wait for the completion message. **Open 7-Zip** runs the original console program.
4. Use **Create test archive** and **Extract test archive** for the supported archive tasks. **Open file manager** opens the qualified original graphical preview.

Personal documents stay separate from application files. The original file manager's complete graphical archive workflow remains a later qualification gate.

## Review and install an original MSI

1. Put the original MSI in your Engacer OS **Downloads** folder. For the tested Notepad++ profile, use [npp.8.9.9.1.Installer.x64.msi](https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.9.9.1/npp.8.9.9.1.Installer.x64.msi). You can transfer it with the existing Files workflow.
2. Open **Windows Apps**, then choose **Choose MSI...**.
3. Open Downloads, click the MSI to select it, and choose **Open**.
4. Choose **Review installer**. Review does not execute its custom actions or install its files.
5. Check the product name, version, publisher and file count. The tested Notepad++ package shows version **8.9.9.1** and **217 files**.
6. Choose **Install app**, read the confirmation, and confirm. Wait for the verified completion message.

If the file changes, review it again before installing. A review-only result means required installer behavior is unsupported; repeated confirmation cannot enable it. Installing Notepad++ in this release does not qualify opening or editing documents with it yet.

Existing supported language preferences are read from the original package's authored registry search. The original WiX DLL executes its selected copy/delete actions through native services. A separate native test establishes an existing French preference; the ordinary interface does not currently offer a new language chooser.

## Remove an installed application

1. Open **Windows Apps** and choose **Installed apps**.
2. Choose the application in the list.
3. Choose **Remove app**, read the confirmation, and confirm removal.
4. Wait for the completion message.

The original download is not needed: the installed application retains its checked original installer for removal and recovery. Unchanged owned application files are removed. Personal documents and changed application files are kept.

If changed files were saved, open **Documents > Recovered applications**. Open the app's folder there. Each saved file has an accompanying text file identifying its original location and content. An unfamiliar differently cased file is preserved before the original language-delete command can reach it.

To reinstall, choose the original MSI again, review it and install. Saved recovery files remain separate and are not overwritten by reinstallation.

## Cancel or finish recovery

During a running task, choose **Cancel task**. Cancellation before publication clears the new uncommitted product files. If a durable transaction already exists, the task keeps its recovery record.

After restarting, open **Installed apps**, choose the affected application, then choose **Recover app** and **Finish recovery**. Recovery uses the original cached installer and ownership records. Final removal cleanup can also finish when only its protected completion record remains; it does not need the deleted download or already-removed cache.

If the record needs inspection, read **Details** and keep the files. A damaged or conflicting record is not a successful removal. Recovery does not run an interrupted forward-install copy action merely to make the operation appear complete.

## Limits and measurements

The engine has bounded MSI input, cabinet, file, property and transaction limits. Unsupported required tables/actions, upgrades, transforms, advertised shortcuts and shared-component behavior are not silently skipped. An x64 application label does not establish that its separate EXE installer is AMD64; mixed x86 chains remain M15 work.

Native tests cover actual original payload hashes, required WiX bodies, registry bytes, changed-file preservation, restart, reinstall and cancellation. The full 138-task native/source/media campaign passes on the exact candidate. Public download and website delivery are verified separately. Fixed kernel data, managed task peaks, framebuffer memory and configured VM RAM are different measurements. Whole-system CPU/RAM/storage optimization remains mandatory in M14.15.

[Current milestone and exact evidence](../milestones/m14-7.md), [execution contract and bounds](../architecture/msi-m147.md), [qualified M14.6 guide](windows-m146.md).

The unreviewed supplied-MSI screen still has a helper paragraph referring to the included 7-Zip. Choose the visible **Review installer** action; an unreviewed supplied package cannot be installed. This wording is recorded for the M14.9 integration work.
