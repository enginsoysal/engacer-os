# Install the M14.1 development candidate in VMware

Status: native qualification passes. The matching M14.1 native release is published; actual website verification is pending.

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

Open Start and search for **Windows Apps** to use the included original 7-Zip console profile or check an original x64 EXE/DLL. Open **Browser → Browser choices** for the Firefox installer download. Checking a file or downloading its MSI does not mean its Windows GUI or installer is supported. Follow the [M14.1 Windows and browser guide](windows-m141.md).

M14.1 is a loader stage in the [ordered M14 program](../milestones/m14.md). Later stages add threads/TLS, Windows GUI and reusable MSI behavior. This stage does not establish general Windows 1–11, MS-DOS, modern browser, GPU gaming or universal hardware compatibility.
