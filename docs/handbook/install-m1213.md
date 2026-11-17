# Install Engacer OS M12.13 in VMware

M12.13 passes M12-STAGE11-VM-v1 native qualification. Use only its matching official release assets.

M12.13 is the native Settings and personalization stage. Use its matching ISO and prepared
VMware ZIP. The stage's exact-source acceptance passes; the
complete final M12 controller/application regression remains M12.18.

## Start the prepared VM

Download `EngacerOS-M12STAGE13-VMware.zip` from the official M12.13 release. Extract
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

[Settings and personalization](settings-m1213.md) explains the four categories, explicit visual preview Apply/Cancel/defaults, independent input choices and malformed preference recovery.

[System tray and quick settings](tray-m1212.md) explains Windows+A, real local-network/audio status, USB Open/Safe remove and the UTC calendar. These base services remain usable when optional apps are removed.

[The multitasking guide](multitasking-m1211.md) covers switching, layout previews, paired windows and safe cancellation. [The taskbar guide](taskbar-m1210.md) covers grouped apps, window choice, overflow and pinning. [Start and local search](start-m129.md) retain their documented behavior. [Shared dialogs](dialogs-m128.md) retain their documented controls and limits. [File commands and transfers](transfers-m127.md) remain available with their recorded provider limits. The [Files views guide](files-m126.md) covers ordering and full names.
The [desktop guide](desktop-m123.md) continues to cover folders and references. The shared
[icon guide](icons-m122.md), controls, Light/Dark and display size remain.
Open Documents/Welcome.txt
for the included guide. Save appearance changes before restarting.

M12.13 qualifies its named VMware SATA/UEFI starter and separate native QEMU
SATA/UEFI and BIOS journeys. It does not inherit the complete M11.6 matrix as
proof for these new bytes. Broader hardware, general Windows installers and
vendor GPU 3D remain outside this stage. Historical media retain their original
guides and hashes. Use the matching release scope and complete SHA256 checksums
from [official downloads](https://engaceros.brixcanvas.com/blog/downloads).

The stage release retains a BIOS AHCI installation timeout from an earlier
M12.2 candidate's concurrent test. Its fresh repeat passed; the trigger is not isolated.
This does not qualify stress reliability. Use the exact tested VMware starter
and read the matching release limits.
