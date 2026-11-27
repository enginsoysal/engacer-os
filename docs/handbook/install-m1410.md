# Install Engacer OS M14.10

Download the ISO or the complete VMware starter and the SHA-256 list from the [M14.10 release](https://github.com/enginsoysal/engacer-os/releases/tag/m1410-v0.14.10).

Use a disposable virtual disk. Setup erases the selected disk. Extract the VMware starter, open EngacerOS.vmx and choose I Copied It if asked. The archive includes a blank 20 GiB SATA disk and the matching ISO, with UEFI, two CPUs, 128 MiB RAM and Secure Boot off. The plain ISO also installed in the compact QEMU profile.

Follow the graphical setup, select the blank disk, review the erase confirmation and install. Restart to the desktop. To verify an independent start, power off, disconnect only the ISO, and restart with the SATA disk attached.

Open Windows Apps from Start. For supported MSI apps, review the original installer, confirm installation and use Installed apps to open or manage the bundle. Choose Repair app to check and restore packaged files from the cached MSI. A reviewed newer package with matching product, layout and registration can offer Update app.

[Release scope](../releases/m1410-v0.14.10.md) · [M14.10 acceptance evidence](../../evidence/M14/10/acceptance-results.json)
