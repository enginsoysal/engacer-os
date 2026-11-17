# Setup and first use — M12.15

M12.15 is under qualification. Use the current qualified download until its
matching release is published. This guide describes the new setup workflow.

## Install in eight steps

1. **Welcome:** choose Next for installation. Recovery and details is for an
   existing installation; Open installed system starts a matching installed disk.
2. **Keyboard / size:** choose US QWERTY or US Dvorak and try typing in the box.
   Clear empties only that test. Auto is the recommended display size. Explicit
   100%, 150% and 200% are available when the current screen can hold the UI.
3. **Choose a disk:** click anywhere in the disk row. The highlight and selected
   circle show your choice. An empty usable disk needs no manual partitioning.
   Disk tools opens advanced partition tools. A disk with existing data requires
   Replace disk, a backup and a separate final erase confirmation.
4. **Your apps:** choose All available, Essentials or No optional apps, then
   change individual checked tiles. More apps and Previous show further choices.
   Desktop, Files, Settings and recovery remain required. The first-start guide
   is optional and can be disabled here.
5. **Your style:** enter your local account name, choose an accent, Light or Dark
   and wallpaper. No online account is required. Normal-size screens also show a
   decorative preview; compact screens retain every actual choice.
6. **Review:** check the actual disk, capacity, account, keyboard, app count,
   appearance, display size and guide. Back changes your choices. Replacing a
   used disk requires the separate entire-disk erase checkbox. Installation
   replaces the whole selected disk, not just a selected partition.
7. **Installing:** keep the VM powered on and its disk connected. Progress shows
   completed phases while files are copied and verified. A failure is not a
   completed installation; follow its message and use recovery when appropriate.
8. **Ready:** choose Restart to Engacer OS. Keep the hard disk connected. The
   matching ISO may stay connected; for a disk-only test disconnect CD/DVD only.

No disk writes should occur during ordinary choices before Install. Formatting
or partition changes explicitly confirmed inside Disk tools are separate writes.
Other disks are not installation targets unless selected and confirmed.

## Disk tools and recovery

The ordinary wizard fits a logical 800×600 workspace. Advanced partition tools
currently need at least logical 1024×768; use a larger display or smaller scale
for them. Supported installation disks need native readable, writable and flush
capabilities, 512-byte logical sectors and capacity from 2 GiB to 2 TiB. An
inspection-only disk cannot be made writable merely by clicking Next.

Disk tools can create/delete supported partitions and quick-format FAT32 or the
native data filesystem. These actions destroy data in the reviewed target.
They do not provide partition resizing, dual boot installation or arbitrary
filesystem conversion. Back up valuable files first.

Recovery and details offers Repair boot files, Update boot slot, Roll back boot
slot and an advanced terminal. Guided recovery shows Choose a disk, Review,
Applying and Ready. Review names the actual disk and operation. Same-build
recovery preserves personal files; cross-release migration remains unqualified.
After a controller write failure, power-cycle the VM after fixing its connection
or external fault; a quarantined controller deliberately refuses more writes.

## First desktop

The first-start card follows the saved theme. Explore Files opens the file
manager, Open Start opens the launcher and Appearance opens required Settings.
Go to my desktop or Escape closes the guide and saves its dismissal. These
routes work independently of optional Calculator or Text Editor packages.

Click a file once to select it. Double-click or Enter opens it. Right-click shows
its actions. Files keeps Back, Forward, Up and Places available for navigation.
Settings previews appearance: Apply and save persists choices; Cancel preview
restores the previous appearance. Optional apps can be installed and removed
without removing the base desktop. The packaged Welcome.txt contains the
current quickstart and the actual USB/file-operation limits.

## Scope

These are native OS controls and startup routes, not a website mockup. Matching
native, VMware, BIOS, display, disk-preservation and failure evidence is required
before release. Automated scenario and visual review are not a human usability
study. Named virtual-device support does not imply universal hardware support.
