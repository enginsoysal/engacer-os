# M12.7 file commands and transfers

Status: implementation and native qualification in progress. M12.6 remains the
published download until this stage closes its exact-source/media tests and
public delivery. This document does not claim that pending checks passed.

## A command must be reachable and applicable

The common Files frame retains navigation and puts Actions on the native toolbar,
including its actual 500x420 minimum. Copy, Cut, Paste, Rename, Recycle, New
folder/text, supported Undo, Properties and the last transfer result belong to
the same bounded menu. Wider windows also expose frequent direct commands.
Disabled commands describe unavailable selection, destination or busy state;
their keyboard routes still enforce the storage checks. Hidden controls must
not become the only way to perform an ordinary action.

Reuse the existing native transaction and generation-bound provider objects.
Do not implement a second filesystem in the toolbar or infer permissions from
an icon. Native Cut/Paste moves metadata within the native volume. USB remains
one-file/create-only: importing a folder, cutting a USB source or replacing an
existing USB file is unavailable. Native files and their system protections
remain distinct from removable-drive capabilities.

## Cooperative importing and actual progress

The direct Copy to Downloads route uses the same job/conflict machinery as
Copy/Paste. A matching name asks Keep both, Skip or Cancel; USB replacement is
disabled. This replaces the earlier direct synchronous import and its separate
automatic-renaming behavior, so the route does not silently choose a different
conflict policy.

A single bounded FAT32 read lease keeps cluster/sector state, source size and
device generation. Each job step reads at most 4096 bytes into the existing
shared buffer and appends to an unpublished native stream. It checks the device
lease before every read. The destination stream is sealed and checked back in
4096-byte steps before metadata publication. A cancellation or removed source
aborts the uncommitted stream. USB source failures have a separate actionable
status; they do not falsely claim that the native destination has stopped all
writes or requires recovery. Already completed items remain available and the
source is never removed by copying. This adds fixed state, not a growing queue,
worker process or per-window data buffer.

The progress strip names the phase, current source and actual destination and
uses completed copy/read-back work for its percentage. It does not invent a
throughput or remaining-time estimate. The Cancel control remains outside the
file-name-tip area; tips are suppressed during an active job and otherwise fit
within the content body. Completion, cancellation and failure all retain a
Details route. Cancellation of a tree can leave already confirmed files/folders;
it is not an all-or-nothing undo of earlier completed work.

The separately checked FAT32 export remains a synchronous create-only operation.
It must state that limitation; this stage must not advertise mid-export
cancellation or arbitrary USB moves. Further concurrent write operations cannot
borrow the shared stream while a cooperative job is active. Source/destination
names, provider capability and final flush remain real backend constraints.

## Verification and limits

Use owned virtual images and ordinary guest input for real installation,
Copy/Cut/Paste, native conflicts, Keep both/Skip/Replace, protected paths,
Recycle/Restore, Undo, compact commands and actual large-file cancellation.
Inspect independent on-disk bytes/CRC and unchanged USB source-image hashes.
Test source removal during reading, confirmed partial completion, two ordinary
installed boots, actual 150% and 3840x2160/200%, matching VMware/BIOS profiles,
cached/full movement, idle CPU halt and retained versus peak memory separately.

Native observations and screenshots are not a human usability study. M12.14
menu-footer fitting, M12.16 cursor isolation and M12.18 BIOS/AHCI stress and final
controller/application regression retain their explicit scope. USB sorting,
general Windows compatibility, physical/ARM qualification and vendor GPU 3D do
not follow from this stage.
