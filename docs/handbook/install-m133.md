# Install and feel at home in Engacer OS M13.3

This guide covers the M13.3 disk-tools release. Use its matching ISO or VMware package. Later M13 stages remain separate; this is not universal hardware or Windows application support.

## The easiest start

Download `EngacerOS-M13STAGE3-VMware.zip` from the [matching release](../releases/m133-v0.13.3.md). Extract the entire ZIP into an ordinary local folder, open **EngacerOS.vmx**, choose **I Copied It** if asked and start. Keep the supplied blank growable 20-GiB SATA disk, two CPUs, 128 MiB RAM, UEFI and Secure Boot off. Leave the included devices enabled. Existing personal disks should remain separate.

The centered startup screen reports real disk, keyboard/mouse/USB and workspace preparation. It deliberately shows no invented percentage or forced waiting time. You do not need an online account, terminal command or guest driver installer.

## Follow the installer

1. **Welcome:** choose **Next**. **More startup options** reveals recovery and opening an existing installation. Escape closes those extra options. Opening an installed system on a blank disk reports that no usable installation is available; it does not install or erase anything.
2. **Keyboard / size:** keep the recommended settings or select US QWERTY / US Dvorak and a supported size. Select the typing box and try the keys. Clear clears only the test text. Enter in that box continues. Back and Next retain the sample and choices. An unsupported size explains the refusal and keeps the previous readable size.
3. **Choose a disk:** click the whole row inside the bordered list. The selected disk is highlighted. Disk tools provide separately reviewed supported operations. Selection alone does not write the disk.
4. **Your apps:** keep the default selection, choose Essentials or remove every optional app. Desktop, Files, Settings and recovery services remain available.
5. **Your style:** set your local name, accent, light/dark appearance and wallpaper. Selected choices have a soft highlight; the main Next action remains distinct.
6. **Review:** check the target and choices. Back revises them. Whole-disk replacement requires explicit fresh erasure consent. **Install** begins actual disk changes.
7. **Installing:** wait for verified completion. If an operation fails, read Details and use the offered recovery action. Failure is never described as successful installation.
8. **Ready:** choose **Restart to Engacer OS**. The next workspace must be the installed system. Escape dismisses the optional first-start guide.

Ordinary Next/Back changes the content pane without clearing the outer frame. A real display-size change recreates the frame to fit. Keyboard users can Tab / Shift+Tab between controls and Enter to activate the focused action. Recovery stays secondary to the ordinary installation route.

## Manage a disk or partition

For ordinary installation, select the intended disk and continue. Engacer OS installs to the whole selected disk; creating a data partition does not select it as an installation location. Disk tools are optional. Back up existing data before changing it.

Choose **Disk tools...** after selecting a disk. The bordered list shows partitions and free space, actual sizes, names/formats and protection. **Previous disk / Next disk** changes the inspected disk; the separate arrow buttons page through partition rows. Check the disk number and capacity again before every change.

- **Create:** on a disk with blank boot metadata, choose **New GPT**, review and confirm first. Select a free-space row, then **New partition**. Select a size/name field and type to replace the suggested value; Ctrl+A selects it again. Use all free space fills the size. Review creation, check the confirmation and Apply. The new partition is unformatted until you format it.
- **Format:** select a mutable partition, choose Format, then FAT32 or Engacer data. Review repeats the partition number, size and name. FAT32 needs at least 64 MiB; native data needs at least 1 MiB and proper alignment. Files on the selected partition are lost. Other partitions remain separate.
- **Delete:** select a mutable partition and choose Delete. Review and confirm. The partition becomes free space; deletion is not secure erasure. Protected system/extended partitions cannot be formatted or deleted through these actions.
- **Clear disk:** a distinct whole-disk metadata operation makes all its partitions inaccessible. Review the exact disk and consent before Apply. It does not securely wipe old content.
- **Repair GPT:** available verified copies can repair damaged partition metadata. Choosing the wrong valid copy can hide partitions. This does not repair arbitrary filesystem damage.

**Apply changes** stays unavailable until the confirmation is checked. **Keep / Cancel** preserves the reviewed target. Back to setup retains installation choices. Supported operations report actual completion; an error asks you to refresh/review rather than claiming success. Read-only/unsupported devices retain a readable inspection or refusal state. Quick format, deletion and clearing do not securely erase old data. Resizing, filesystem conversion and data-preserving dual boot are unavailable.

The qualified transport profiles are named in the release scope. The existing QEMU-PVSCSI refusal remains unqualified; do not infer VMware-PVSCSI results from that emulator.

## Start again and explore

The matching ISO may remain connected for the first restart. For disk-only startup, disconnect only CD/DVD, retain the installed disk and use the same VM/firmware variables. Keep the matching ISO for recovery. These unsigned development media require Secure Boot off.

One click selects a file; double-click or Enter opens it. Existing [Files](files-m126.md), [Start](start-m129.md), [Settings](settings-m1213.md) and [keyboard/accessibility](accessibility-m1216.md) guides explain retained features. Their historical qualification does not certify untested configurations of this ISO.

## Readable display choices

The exact starter is the compact 128-MiB case. Separate named native profiles cover actual 1024×768 and 1280×800 at 100%, 1920×1080 at 100%, 1920×1200 at 150% and actual 3840×2160 at 200%. Configured RAM is not measured OS memory use. Larger scaling needs enough logical space; a refused choice retains the readable viewport.

Check the release's SHA256 values before booting. Supported VM profiles, physical hardware, vendor GPU 3D and general DOS/Windows compatibility are separate qualifications.
