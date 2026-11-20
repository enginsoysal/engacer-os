# Install the M14.6 candidate in VMware

Native/source/media qualification passes for build 5f49030d412bd7f0587568c029becc2c. The matching public release and all twenty independent asset downloads pass. Public content/link verification is recorded separately in evidence/M14/6; reported advanced platform controls remain unqualified.


## Before starting

Use a separate test VM and a disposable virtual disk. Installation erases the selected target. Keep your personal files and other operating systems outside the test VM. Public media are unsigned: use x64 UEFI with Secure Boot disabled. The prepared package includes a blank growable 20-GiB SATA disk, two CPUs and 128 MiB RAM. The small profile is for supported native tasks; it does not promise that every future Windows app fits in 128 MiB.

Extract the whole matching VMware ZIP into a normal local folder. Open **EngacerOS.vmx** and choose **I Copied It** if VMware asks. Keep the included disk and matching ISO connected. Start the VM. Installation and desktop exploration do not need a network connection. The optional Firefox download requires networking, available hardware entropy and a valid UTC clock.

## Follow setup

1. Read Welcome and choose Next.
2. Choose your keyboard layout and continue.
3. Click the disk's row in the installation list. The selected row is highlighted. Review the disk tools and erasure notice before continuing.
4. Choose the optional apps you want. These choices do not remove required system components.
5. Choose your supported appearance settings.
6. Review the target disk and choices. Return with Back if anything is wrong.
7. Choose Install and wait for copying and verification to finish.
8. Choose Restart to Engacer OS. The matching ISO may remain connected; the installed desktop should start. You may subsequently disconnect the ISO and start from the installed virtual disk.

If setup refuses a disk, read its specific reason rather than repeatedly clicking Install. Do not reformat a disk containing wanted data. The matching [storage guide](vmware-storage.md) explains supported controllers; wider physical hardware and ARM remain separate qualification.

## Try the changes

Open Start, search for **Windows Apps**, and open it. Choose **Install 7-Zip**, review the confirmation and install. **Open file manager** starts the original Windows x64 7-Zip file-manager window. Try moving, resizing, minimizing/restoring and closing it. This stage retains menus/About, images and folder navigation and adds original-to-native Unicode text clipboard transfer and the bounded original Browse/Save preview. The native editor reopens UTF-8 files and renders complete scalars; Windows CRLF remains unchanged in storage and becomes one visual line ending. Complete GUI archive tasks remain unqualified. Use the existing **Open 7-Zip**, **Create test archive** and **Extract test archive** console actions for the supported archive tasks. Follow the [M14.6 Windows guide](windows-m146.md).

The original process runs through our own kernel and compatibility APIs. There is no embedded Windows guest. Notepad++ and SumatraPDF interfaces and installer/use scenarios remain unqualified; their current startup diagnostics are not supported user tasks. Firefox can be downloaded through **Browser > Browser choices**, but cannot install or run yet. Later ordered stages cover reusable installation, required runtimes and complete original-app tasks. M14.15 remains the whole-system optimization gate.
