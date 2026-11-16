# M11.5 guided setup and first installed desktop

Native qualification passed on 16 November 2026 within M11-STAGE5-VM-v1.
[Exact-source acceptance](../../evidence/M11/5/acceptance-results.json) binds 562
source inputs, fourteen artifacts and 26 native task groups. Visible release and
fresh public site/download verification are separate required publication gates.

## Model and navigation

The existing original native installer gains a bounded Keyboard / size page
between Welcome and disk selection. The mature internal disk/install/recovery
step identities remain unchanged; a separate visual index describes eight steps.
This avoids changing the destructive-operation state machine to add a preference
page. One fixed setup record holds layout, theme, wallpaper, pattern, display size
and the initial optional-app bitmask. Back retains choices and invalidates any
destructive consent as before. No account or network service is required.

English UI and UTC are explicit current limits. US QWERTY and Dvorak call the
actual existing keyboard provider; a bounded typing box permits verification.
Display choices use the same automatic/100/150/200-percent provider as the desktop.
An unsuitable size is refused with an explanation, preserving the old choice.
Only a successful size change recalculates the frame. Normal Next/Back redraws
the content pane; no animation, polling loop or additional framebuffer is added.

## Components and persisted choices

The installer enumerates only optional apps admitted by the distribution profile.
All, Essentials and No optional apps are real install selections, with paginated
individual choices. Desktop, Files, Settings and required services remain base.
Existing package cache objects are retained to allow offline later installation;
removal of an optional executable cannot remove its unrelated services or files.
The complete offline cache and existing kernel handlers remain in this build;
omitting apps is not a claim that their compiled handler code was removed from
the kernel or that the cache consumes no disk space.
The old calculator choice ABI is retained for older profiles.

The local user name is limited to 31 ASCII letters/digits/underscore/hyphen, as
required by the existing storage contract. Selection, Ctrl+A, cursor movement,
Home/End and Delete permit replacement and correction rather than append-only
editing. Appearance choices persist through the existing version-1 352-byte
appearance record; its definition is now shared with setup without changing its
format. Layout uses the existing keyboard record. A new per-user versioned
first-start record contains only whether the optional guide was dismissed.

The installer validates the option mask and ranges before any installation write.
It writes and verifies preference payloads before publishing the installed
activation record. A failed preference save therefore cannot be reported as a
successful installation. The earlier setup record ABI and recovery slots remain
unchanged. Maintenance changes boot files without replacing personal preferences.

An I/O-faulted controller can remain quarantined until restart. The first fault
scenario incorrectly assumed immediate same-session retry after a one-shot host
I/O failure; the actual safe driver state refused Next. The recorded diagnostic
is retained. Final verification requires refusal while quarantined and a genuine
successful retry with the same disk/NVRAM after the external fault is removed and
the VM is power-cycled. This retains the storage safety contract rather than
silently unquarantining a failed controller.

## Disk safety and first start

Disk rows and supported partition create/delete/format operations retain their
native checked plans. The OS install uses the whole selected disk, including its
boot/recovery/data layout. Installing into a selected existing partition,
partition resizing and dual boot remain unsupported. Review distinguishes an
empty disk from an explicit reviewed whole-disk replacement. Unselected disks
must retain their bytes. Disk tools have their own destructive-operation consent.

Ready is reached only after copying, readback, metadata verification and flush.
Restart must exercise the real firmware/installed loader/kernel, including a
retained matching ISO and two separate disk-only boots with original NVRAM.
A live-session screenshot is insufficient.

When a matching installation is found, the M11 UEFI media presents a two-second
firmware message and Escape choice before automatic disk-loader redirection.
The previous single instantaneous input check was insufficiently discoverable
for recovery. This bounded firmware-only wait uses UEFI Stall and Simple Text
Input; it adds no kernel timer loop or persistent allocation. Without Escape the
actual installed loader still starts. Historical loaders remain unchanged.

The first-start card is optional and dismissible, with genuine Files, Start and
Appearance routes. It depends only on base components, never on Text Editor or
Help. Dismissal is durable; a save failure closes it for the session with an
honest notice. There is no second mandatory setup wizard. Existing installations
without the new record do not acquire an unsolicited first-start tour.

## Verification boundary

Native normal-input journeys and independent disk payload/CRC inspection must
cover choices, Back, consent, formatting, failure/recovery, saved preferences,
minimal apps, guide dismissal and installed boots. Ordinary, 150-percent and real
4K screenshots receive a clarity/convenience/readability review. Resource checks
distinguish fixed shell state, managed pages and configured guest RAM. These are
agent scenario reviews, not a human usability study. M11.6 still owns the full
controller/device/original-Windows-app regression matrix.
