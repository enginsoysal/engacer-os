# Install Engacer OS M11.6 in VMware

M11.6 / 0.11.6 is the final installation and desktop delivery, qualified within
**M11-FINAL-VM-v1**. [Exact release, checksums and limits](../releases/m116-v0.11.6.md)
cover 14 VMware controller/starter profiles and the same-artifact device,
desktop, setup/recovery and original 7-Zip MSI/console regression.

## Start with the prepared virtual machine

Download `EngacerOS-M11FINAL-VMware.zip` from the
[M11.6 release](https://github.com/enginsoysal/engacer-os/releases/tag/m116-v0.11.6)
Extract the **entire ZIP into a local folder**, open
**EngacerOS.vmx**, and choose **I Copied It** if VMware asks. Start the VM.
The starter supplies a blank growable 20-GiB SATA disk, two CPUs and 128 MiB RAM,
UEFI with Secure Boot off, and enabled network, USB and sound devices. It is
not a preinstalled disk. Keep the supplied disk connected throughout setup.

## Eight simple steps

1. **Welcome:** choose Next. Recovery & details is for repairing an existing
   matching installation, rather than ordinary installation.
2. **Keyboard / size:** choose US QWERTY or US Dvorak. Select the typing box to
   try your layout, and Clear to empty it. Auto is the default text/control size;
   100%, 150% and 200% work where the display can fit the usable viewport. An
   unsuitable size gives an explanation and keeps the previous size. Current
   interface language is English and the clock uses UTC. No network or online
   account is needed.
3. **Choose a disk:** click the disk's **whole row inside the bordered list**.
   Its selection is highlighted. Next becomes available for an eligible empty
   disk. Existing contents require the explicit erase-and-install choice and
   later separate Review consent. Read any unavailable reason below the list.
4. **Your apps:** choose All available, Essentials, No optional apps, or toggle
   individual apps. More apps (shown as More a... on a smaller viewport) and Previous show the other pages. Files, Settings,
   the desktop and required services always stay. Omitted apps can be installed
   later offline from Settings; personal files remain separate. The optional
   first-start guide does not require Help or Text Editor.
5. **Your style:** select the name box to replace Owner. Use up to 31 letters,
   digits, `-` or `_`. Ctrl+A selects the name; arrows/Home/End and Delete or
   Backspace correct it. Choose accent, Light/Dark and wallpaper. These are real
   saved desktop preferences. You can change them again later in Settings.
6. **Review:** verify the disk, account, keyboard, app count and appearance.
   Back retains your choices. For replacement, check the separate whole-disk
   erasure consent only after confirming your target and backups. Returning Back
   clears this consent, so a later install cannot reuse an old authorization.
7. **Installing:** choose Install Engacer OS, then keep the disk connected.
   Progress follows actual copy, verification and saved setup operations.
8. **Ready:** choose **Restart to Engacer OS**. This restarts the machine into
   the installed system. The matching ISO may remain attached. Keep the hard
   disk connected. A failed installation shows an error instead of Ready.

## Disk tools and formatting

Choose a disk row, then **Disk tools**. Select a partition or free-space row.
Supported operations include creating/deleting data partitions and quick format
as FAT32 or native data, with their own target-specific Review and consent.
Keep / Cancel returns without applying the proposed change. Quick format is not
secure erasure. Other partitions and disks are not that operation's target.

The OS installation uses the **whole selected disk**, including boot, recovery
and data partitions. Installing the OS into a selected existing partition,
resizing partitions and dual boot are not implemented. Do not attach host disks
as test targets. Use a disposable virtual disk and back up anything valuable.

## Your first desktop

The optional Welcome home card offers real Files, Start and Appearance routes.
Choose **Go to my desktop** or press Escape while it has focus to dismiss it.
Dismissal is saved, so it does not appear on every startup. There is no mandatory
second setup. Click a file once to select; double-click or press Enter to open.
Right-click opens its available actions. Start searches installed apps locally.

To check independent startup, shut down, disconnect **only CD/DVD**, keep the
same installed disk and start the VM again. Your files and preferences should
remain. The development media are build-specific; retain the matching ISO for
recovery rather than mixing it with a different release.

## If something goes wrong

- **No disk / disabled Next:** check the row and explanation. Installation needs
  verified read/write/flush, 512-byte sectors and a supported 2-GiB to 2-TiB disk.
- **Disk contains data:** back up first; select whole-disk replacement and review
  its separate erasure consent. Disk tools do not imply selected-partition install.
- **Copy or verification failed:** the installer does not claim success. Keep the
  ISO, read Details and use Back to recheck the disk. A failed controller may
  remain safely blocked for the session. If Next stays unavailable after fixing
  the connection or storage fault, restart the VM with the same disk and matching
  ISO before retrying. Do not repeatedly force writes to a faulted controller.
- **Installed boot fails:** keep the same disk; boot its matching ISO and choose
  Recovery & details → Repair. With a matching UEFI installation, press **Escape**
  during the visible two-second setup/recovery prompt to stay in the installer.
  Without Escape, the matching ISO starts the installed disk automatically.
  Review the selected installation before applying the repair.
- **Text is too large:** select a suitable size or Auto; unsupported sizes are
  refused. Display support and vendor GPU acceleration are separate capabilities.

[Files](files-m11.md) · [Start and taskbar](start-m11.md) ·
[Windows and appearance](windows-m11.md) · [Setup decisions](../architecture/setup-m115.md).

## Use a USB drive

1. Connect supported clean FAT32/BOT media through a supported xHCI controller.
   Open **Files → USB drives** and choose the drive.
2. Click a file once to select it, then choose **Copy to Downloads**. Double-click
   a folder or select it and press Enter to open it.
3. To copy back, open the native file's folder, select the file, right-click and
   choose **Copy to USB...**. Choose the destination drive. Select its destination
   folder and **press Enter to open it**, then choose the export action. A single
   click selects a folder; it does not navigate. Existing destination names are
   refused rather than overwritten.
4. Choose **Safe remove**, wait for the safe-to-remove message, then disconnect.
   Reconnecting supported media binds it again automatically.

Copies are create-only, bounded to 64 MiB and the documented clean FAT32/BOT
profile. exFAT/NTFS writes, UAS writes, arbitrary partition formatting on USB and
power-loss atomicity are unavailable. Do not disconnect during a copy.
The 64-MiB OVMF profile attaches USB storage after installed startup; boot-attached
USB at that RAM size remains unqualified. Use the standard 128-MiB VMware starter.

## Other existing virtual machines

Named controller qualification covers SATA, IDE, LSI Logic, SAS1068, PVSCSI and
NVMe with BIOS/UEFI, plus BusLogic with BIOS. Keep Secure Boot off for UEFI.
Use a writable 512-byte-sector disposable disk of 2 GiB–2 TiB and retain the
same disk and firmware configuration after installation. Recognition alone
is not installation eligibility; read the displayed capability/reason.

The wider hardware program and general Windows applications remain separate
work. [Final qualification decisions](../architecture/qualification-m116.md).
