# VMware disks and installation storage

## Current M14.3 installer

Use the [matching prepared VMware package and installation guide](install-m144.md). It contains a new blank growable 20-GiB SATA disk and the matching ISO. Extract the whole package, open EngacerOS.vmx and keep its hard disk connected. This is the exact VMware configuration qualified for M14.3; older controller-matrix results remain historical, not repeated qualification of these media.

In **Choose a disk**, click the disk row: its highlight and selection circle show the chosen target. A blank usable disk needs no manual partition creation. Next leads to app/style choices and a separate review; installation writes only after the reviewed Install action. Existing data requires the explicit replacement/erasure route. The ordinary installer replaces the entire selected disk, not one chosen partition. Back up anything wanted before confirming erasure.

**Disk tools** provides the implemented partition create/delete and quick-format operations for supported writable targets. Formatting destroys data; it is not a remedy for an unrecognized controller. Advanced tools require the documented larger logical workspace. Partition resizing, general filesystem conversion and dual-boot installation are unavailable. [Detailed retained setup behavior](setup-m1215.md).

A disk must be discovered through its actual controller before partitions can be inspected. An empty disk and an undetected disk are different conditions. Installation needs readable, writable and flush capabilities, 512-byte logical sectors and capacity from 2 GiB to 2 TiB. Read-only or inspection-only discovery is not installation support. The driver must implement the controller's protocol; the words IDE, SATA, SCSI or NVMe alone do not establish compatibility with every device in that family.

If no usable target appears, shut down the test VM and check that its virtual disk is connected. For the simplest reproducible test, use the unchanged matching starter instead of changing a personal VM. Keep physical/raw host disks and wanted VMDKs outside the test. Collect the displayed reason, release version and controller configuration if it still refuses. Never erase wanted data to work around discovery failure.

After successful setup choose **Restart to Engacer OS**. The matching ISO may remain connected. For an independent installed-system test disconnect only CD/DVD; retain the hard disk and firmware settings. The public package uses x64 UEFI with Secure Boot disabled. [Current release scope](../releases/m144-v0.14.4.md), [historical integration matrix](../releases/m1312-v0.13.12.md).

## Historical M4.5 console troubleshooting

The remaining commands and read-only limitations describe the old M4.5 media. They are retained for that release and do not describe today's graphical installer.

**Historical follow-up:** M5 subsequently added its own [installation tutorial](install.md), [commands](m5-console.md) and [recovery](recovery.md). Use the current guide above for M14.3.

## Disk discovery comes before partitions

A disk with no partition table must still appear under `disks` when its controller is supported and a first-sector read succeeds. For a 20-GiB disk, M4.5 prints approximately `20480 MiB` and its logical sector size. `parts N` then reports no MBR/GPT table. An empty partition table is different from an undetected disk.

`No readable storage devices discovered` with no disk entries means no storage record was registered. It does not mean that the OS examined a detected disk and found no partitions. `No writable development filesystem mounted` separately means that no marked M4 development volume is mounted; ordinary disks are deliberately read-only.

## VMware controller selection

| Virtual disk controller | M4.5 status |
|---|---|
| SATA / AHCI | Qualified on VMware EFI and BIOS |
| IDE / ATA | Qualified on VMware EFI and BIOS |
| NVMe | Qualified on VMware EFI |
| SCSI LSI Logic, LSI Logic SAS, BusLogic or VMware Paravirtual SCSI | No driver in M4.5; a connected disk can remain undetected |

The FreeBSD guest preset can choose SCSI. Its virtual hardware selection is separate from Engine OS support. A controller that works for another guest needs an Engine OS driver too. A USB device count of zero is unrelated to whether a SATA disk is readable; VMware USB 2 controllers are also outside the qualified xHCI input profile.

## Safe setup for a new 20-GB test disk

1. Power off this test VM normally from VMware. Changing a controller requires a powered-off VM; Engine OS `halt` only halts the guest CPU and is not a VMware power-off operation.
2. Open **VM settings > Add > Hard Disk** and select **SATA**. Select a new virtual disk and a maximum size of **20 GB**. Do not select a physical/raw host disk.
3. Keep existing SCSI disk files intact. For a simple test, add the new SATA disk alongside them; there is no need to delete or overwrite the original VMDK. This procedure does not convert an existing SCSI disk.
4. Keep the Engine OS ISO connected to CD/DVD at power-on and boot it with Secure Boot disabled.
5. Run `disks`. Identify the disk by its displayed controller and capacity; disk numbering depends on discovery order.
6. Run `parts N`, replacing `N` with that disk's number. For a new blank disk, `No MBR/GPT partition table - unknown or empty filesystem` is expected. Status zero means inspection succeeded; it does not mean a partition was created.

If the SATA disk still does not appear, run `hardware` and `info`, and record the complete output and virtual controller configuration. Do not format the disk as a workaround for failed controller detection.

## Creating a partition

M4.5 has **no partition-create or format command**. `parts N` only inspects. Partitioning, formatting, target confirmation, installation and independently booting an installed disk belong to M5 and have not been implemented. There is no Engine OS command to turn this 20-GB disk into an install target yet.

M4.5 can inspect supported existing FAT32/ext2 filesystems on ordinary disks read-only. Its legacy writable filesystem is a separately marked, bounded M4 development fixture; it is not a general formatter for arbitrary disks. Creating a partition elsewhere therefore does not turn an ordinary disk into the writable development volume.

[Handbook](index.md), [console commands](console.md), [VMware release guide](../releases/m45-v0.4.5.md).
