# Install Engacer OS M11.5 in VMware (historical)

Historical M11 stage guide. For current media use [M14.3 installation](install-m143.md). [M11.6 installation](install-m116.md) remains the final guide for that older series.

M11.5 / 0.11.5 is the expanded guided-setup stage, qualified within
**M11-STAGE5-VM-v1**. [Exact release, checksums and boundaries](../releases/m115-v0.11.5.md).
The full controller/device/original-app regression remains M11.6.

## Start with the prepared virtual machine

Download `EngacerOS-M11STAGE5-VMware.zip` from the
[M11.5 release](https://github.com/enginsoysal/engacer-os/releases/tag/m115-v0.11.5)
when available. Extract the **entire ZIP into a local folder**, open
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
   individual apps. More apps and Previous show the other pages. Files, Settings,
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
