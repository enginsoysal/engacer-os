# Install Engacer OS M14.7 in VMware

**Native/source/media qualification passes.** Use the matching M14.7 ISO or prepared VMware package. Build `1fb03f1b582d4d153441b6b5ca40da06` passes the 138-task campaign, including actual VMware installation and two disk-only starts. Public delivery is verified separately; follow the current release status.

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

Open Start, search for **Windows Apps**, and open it. Choose **Install app**, read the confirmation and confirm. **Open 7-Zip**, **Create test archive** and **Extract test archive** use the original console application. **Open file manager** opens the qualified original graphical preview. Full graphical archive operations remain separately unqualified.

To try another MSI, choose **Choose MSI...**, select the original package in Downloads, choose **Open**, then **Review installer**. The supported Notepad++ profile uses `npp.8.9.9.1.Installer.x64.msi`. Confirm **Install app** only after reviewing the product details. Its original installation, language actions, ownership and removal are implemented; its editor is not yet supported. Opening a file from Files also requires review before installation.

Use **Installed apps** to select an installed package and remove it, including after restarting or deleting the original download. Modified files are saved in **Documents > Recovered applications**. Use the guided **Recover app** action if an interrupted operation requires cleanup. Follow the [M14.7 MSI guide](windows-m147.md) for exact steps and limits.

Original Windows instructions execute through our own kernel and compatibility APIs. There is no embedded Windows guest. Notepad++ editor and SumatraPDF installer/interface tasks remain unqualified; Firefox remains a verified installer download only. M14.15 still blocks final release on whole-system CPU/RAM/storage optimization.
