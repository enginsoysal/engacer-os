# Install Engacer OS M14.8 in VMware

**Candidate instructions: final M14.8 qualification and publication are pending.**
The current qualified public release remains M14.7. Use media and guides from
the same release; do not combine an older ISO with a newer installed kernel.

## Prepare the VM

Use a separate test VM and a disposable virtual disk. Setup erases the selected
target; keep wanted files outside that disk. Extract the complete matching
VMware package into a normal local folder, open EngacerOS.vmx and choose
I Copied It if asked. Keep its included ISO and blank 20-GiB SATA disk connected.
The prepared profile has two CPUs and 128 MiB RAM. This small native-test profile
does not promise that arbitrary future Windows apps fit in that memory.

The unsigned x64 media require Secure Boot disabled. Supported BIOS and UEFI
ISO/USB firmware profiles are checked separately from physical hardware and ARM.
See [VMware storage](vmware-storage.md) for supported controllers and disk tools.

## Follow the wizard

1. Read Welcome and choose Next.
2. Choose your keyboard layout and continue.
3. Click the installation disk's row. Check that it is highlighted and review
   the disk tools and erasure notice.
4. Choose the optional apps you want. Required system components stay present.
5. Choose the supported appearance settings.
6. Review the disk and choices. Use Back to change anything before installing.
7. Choose Install and wait for copying and verification to finish.
8. Choose Restart to Engacer OS. The installed desktop should start even if the
   matching ISO remains connected. You can then disconnect it and start from disk.

If setup refuses a target, read its specific reason. Do not repeatedly format a
disk containing wanted data. Installation and desktop use work offline. Optional
browser downloads additionally need networking, entropy and a valid UTC clock.

## Try the original installer workflow

Open Start, search for Windows Apps and open it. Choose Choose installer...,
select the unchanged installer in Downloads and choose Review installer. Read
the supported profile and confirmation before installing. EXE installation opens
the original setup window; it is not performed by an embedded Windows guest.

The [M14.8 Windows installer guide](windows-m148.md) distinguishes the original
SumatraPDF installer from its still-unqualified reader, and explains removing,
reinstalling and preserving interrupted EXE records. Existing 7-Zip console and
graphical-preview tasks remain separate buttons. Notepad++ editor use and
Firefox browsing are not qualified tasks. Whole-system optimization is M14.16.
