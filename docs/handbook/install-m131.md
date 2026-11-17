# Install and try Engacer OS M13.1

This guide covers the M13.1 shared-control preview. M13.2–M13.12 remain separate stages. Use the exact ISO and VMware package listed in the [matching release guide](../releases/m131-v0.13.1.md).

## The easiest start

Download `EngacerOS-M13STAGE1-VMware.zip` from the official M13.1 release and extract the whole ZIP into an ordinary local folder. Open **EngacerOS.vmx**, choose **I Copied It** if VMware asks, then start the VM. Keep the included settings for the simplest test: a new blank growable 20-GiB SATA disk, 128 MiB RAM, two CPUs, UEFI and Secure Boot off. Network, USB and sound stay enabled.

This is a real installation. Use the supplied disposable disk and keep your existing disks separate. No online account, terminal command or guest driver installer is required.

## Follow the installer

1. **Welcome:** choose Next.
2. **Keyboard / size:** keep the defaults or select a supported keyboard layout and readable size. Test your keyboard, then choose Next.
3. **Choose a disk:** click the whole disk row inside the bordered list. The selected row is highlighted. Disk tools inspect partitions and provide separately reviewed changes.
4. **Your apps:** keep the defaults or select optional apps.
5. **Your style:** choose your local profile and appearance.
6. **Review:** check the exact target and proposed changes. Replacing an existing disk needs fresh explicit erasure consent. Back lets you revise your choices.
7. **Installing:** wait for verified completion. If it fails, read Details; a failure is not called success.
8. **Ready:** choose **Restart to Engacer OS**. Dismiss the optional first-start guide with Escape if you prefer.

The matching ISO may remain connected. To test disk-only startup, disconnect only CD/DVD; keep the installed disk, the same VM and its firmware variables. Keep Secure Boot off for these unsigned development media. Retain the matching ISO for recovery.

## Explore the shared controls

Open Start, type **Settings** and press Enter. In Settings choose **System → Interface preview**. Try the normal button, toggle the selection and click the text field to type. Backspace edits the field. F1 describes its focused control; Escape closes focus help and preserves your work. The unavailable button cannot be activated. The preview does not write files or preferences and accepts at most 48 printable characters.

Use **Back to System** to leave the gallery. Appearance and Display use their existing explicit **Apply and save / Cancel preview** controls. Closing an unsaved appearance preview restores the previous settings. High contrast is separate under Accessibility; turn it off to restore your normal theme.

One click selects a file; double-click or Enter opens it. Existing [Files](files-m126.md), [Start](start-m129.md), [Settings](settings-m1213.md) and [keyboard/accessibility](accessibility-m1216.md) guides remain useful references. Their historical test receipts do not qualify every configuration of this new ISO.

## Choose a readable test display

The exact VMware starter is the compact 128-MiB case. Separate native reference tests cover 1920×1080 at 100% with 512 MiB, 1920×1200 at 150% with 512 MiB and actual 3840×2160 at 200% with 1 GiB. These are named virtual profiles, not universal monitor/GPU support. Configured RAM is not measured OS consumption.

Check the release's complete SHA256 values before booting. Hardware expansion, GPU 3D and general DOS/Windows support remain separate work.
