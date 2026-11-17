# Install Engacer OS M12.18 in VMware

M12.18 passes M12-STAGE18-VM-v1 native qualification. Use only its matching official release assets.

M12.18 is the final M12 named-VM desktop and setup qualification. Use its exact
ISO and prepared VMware ZIP. Earlier stage media and tests remain historical.
The [final qualification guide](final-m1218.md) lists what was actually tested.

## Start the prepared VM

Download `EngacerOS-M12STAGE18-VMware.zip` from the official M12.18 release. Extract
the **whole ZIP** into an ordinary local folder, open **EngacerOS.vmx** and choose
**I Copied It** if VMware asks. Start the VM. The package contains a new blank
growable 20-GiB SATA disk, 128 MiB configured RAM, two CPUs, UEFI and Secure Boot
off. Its shipped network, USB and audio devices remain enabled.

This is a real installation, rather than a preinstalled desktop. Use a disposable
test VM and keep your existing disks separate. Configured RAM is not measured
kernel consumption. No online account or guest driver installer is required.

## Follow the eight steps

1. **Welcome:** choose Next.
2. **Keyboard / size:** keep the defaults or choose your supported layout and
   readable display size. Test the keyboard, then choose Next.
3. **Choose a disk:** click the disk's whole row inside the bordered list. Its
   selection is visible. Next becomes available for a usable target. Disk tools
   inspect partitions and provide separately reviewed changes.
4. **Your apps:** retain the defaults or select optional apps.
5. **Your style:** choose your local profile and appearance.
6. **Review:** check the disk and proposed changes. Existing-disk replacement
   requires fresh explicit erasure consent. Back lets you revise choices.
7. **Installing:** wait for verified completion. A failure offers details and
   recovery; it is not labeled a successful installation.
8. **Ready:** choose **Restart to Engacer OS**. The actual installed desktop
   starts. The optional first-start guide can be dismissed with Escape.

The matching ISO may remain connected. For independent disk-only startup,
disconnect only CD/DVD and retain the same installed disk, VM and firmware
variables. Keep Secure Boot off for these public unsigned media.

## Try the desktop

The final guide rechecks selection, folders, shortcuts, Start, grouped taskbar,
window controls, USB transfers, dialogs, Settings and accessibility on this release.


[Motion and resource use](performance-m1217.md) explains direct movement, Escape cancellation, reduced effects and honest memory/performance measurements.

[Keyboard and accessibility](accessibility-m1216.md) explains F1, F6, visible focus, independent contrast/reduced effects and readable display sizes.

[Setup and first use](setup-m1215.md) explains every choice, compact layout, independent app management and recovery.

[Messages and recovery](feedback-m1214.md) explains Clear search, complete menu help, safe save refusals, Show current dialog and bounded Dismiss messages.

[Settings and personalization](settings-m1213.md) explains the ordinary categories, explicit visual preview Apply/Cancel/defaults, independent input choices and malformed preference recovery.

[System tray and quick settings](tray-m1212.md) explains Windows+A, real local-network/audio status, USB Open/Safe remove and the UTC calendar. These base services remain usable when optional apps are removed.

[The multitasking guide](multitasking-m1211.md) covers switching, layout previews, paired windows and safe cancellation. [The taskbar guide](taskbar-m1210.md) covers grouped apps, window choice, overflow and pinning. [Start and local search](start-m129.md) retain their documented behavior. [Shared dialogs](dialogs-m128.md) retain their documented controls and limits. [File commands and transfers](transfers-m127.md) remain available with their recorded provider limits. The [Files views guide](files-m126.md) covers ordering and full names.
The [desktop guide](desktop-m123.md) continues to cover folders and references. The shared
[icon guide](icons-m122.md), controls, Light/Dark and display size remain.
Open Documents/Welcome.txt
for the included guide. Save appearance changes before restarting.

M12.18 freshly qualifies SATA, IDE, LSI Logic, LSI SAS 1068, PVSCSI and NVMe
with both BIOS and UEFI, BusLogic with BIOS, and the exact SATA/UEFI starter.
Each case installs, resets with its ISO retained and starts twice without it.
The supported original 7-Zip console MSI lifecycle and 106 original payloads
are independently checked. Other Windows installers and vendor GPU 3D remain
outside this release. Historical media retain their original guides and hashes.
Use the matching release scope and complete SHA256 checksums from
[official downloads](https://engaceros.brixcanvas.com/blog/downloads).

Named USB/input profiles include BIOS, UEFI, a 4K hub, larger FAT32 clusters,
reconnect, write protection, injected I/O refusal and quota cleanup. The 64-MiB
QEMU UEFI profile attaches USB after startup; boot-attached USB at 64 MiB remains
an explicit loader refusal. This does not qualify physical or universal hardware.

The earlier M12.2 BIOS/AHCI observation remains immutable. Its final repeat and
stress outcome are recorded in the [final qualification](final-m1218.md) and
matching acceptance; a successful scoped repeat does not identify an earlier
unreproduced trigger or prove a universal absence of failures.
