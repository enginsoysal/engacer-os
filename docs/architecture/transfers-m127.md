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

The read lease coalesces at most 4096 physically consecutive bytes only after
checking their FAT links. Fragmented chains retain their real order. Three
512-byte FAT-sector slots cover the current/slow/fast chain cursors; entries are
validated against mirrored FATs on insertion and invalidated with the lease.
Their data/tags/mask use 1,568 fixed bytes. Larger-sector media retain the checked
uncached chain path. This bounded working set is chosen over an entire FAT in
RAM or repeated reads of the same metadata for every cluster.

The production old/new host reader comparison validates the same 64-MiB data:
229,378 sector requests in the earlier M12.7 prototype versus 16,384 data requests
and 514 sector requests in the new path. This is 13.57 times fewer I/O requests,
not a measured physical-device speedup. Real fragmented/unaligned data, mirror
faults, read failure and generation replacement remain separate correctness
checks; native VM copying/CRC and memory qualification are still required.

The progress strip names the phase, current source and actual destination and
uses completed copy/read-back work for its percentage. It does not invent a
throughput or remaining-time estimate. The Cancel control remains outside the
file-name-tip area; tips are suppressed during an active job and otherwise fit
within the content body. Completion, cancellation and failure all retain a
Details route. Cancellation of a tree can leave already confirmed files/folders;
it is not an all-or-nothing undo of earlier completed work.

Admitting or finishing a job redraws shared command state across Files windows.
Steady progress damages only its strip; a minimized owner damages the global
progress strip instead. Whole-window repainting for each percentage change
wastes CPU and can conceal a usable background progress control. Undo/Restore
also respect the native volume's read-only state. A rejected new attempt clears
the previous summary before reusing the one bounded job record, so old completed
counts cannot be displayed beside a new source/destination. This is a last-result
record, not an unbounded operation history. Safe removal and competing USB copy
routes share the busy guard in the toolbar, context menu and command handler.

The separately checked FAT32 export remains a synchronous create-only operation.
It must state that limitation; this stage must not advertise mid-export
cancellation or arbitrary USB moves. Further concurrent write operations cannot
borrow the shared stream while a cooperative job is active. Source/destination
names, provider capability and final flush remain real backend constraints.

## Compact live installation payload

The M12.7 live image initially crossed physical 8 MiB, which the named OVMF
profile reserves as ACPI NVS. The loader correctly refused allocation; VMware
alone did not expose that conflict. The fixed-address ELF contract is unchanged:
firmware-owned memory is never reclaimed or overwritten. M12 independently
compresses each nonzero installation page using original bounded LZ4 block
encoding; zero/raw records remain readable. Bit 30 marks an encoded record,
followed by a 16-bit encoded length; bit 31 retains zero-page semantics. Both
flags together are invalid. Addresses retain 30 bits, well above payload LBAs.
Earlier build modes retain their original format and immutable artifacts.

The production decoder uses no heap or persistent dictionary. Output is exactly
4096 bytes; lengths, back-references, input/output boundaries and complete input
are checked before destination I/O. Whole bundle CRC and every record/destination
are validated before install or recovery writes. The existing scratch buffers
are reused. Recovery slots keep their opaque checked bundle, with both validation
and replay using the same decoder. Independent installed pages remain unchanged;
this compresses distribution bytes, not the running installed filesystem.

A build guard refuses a live ELF extending beyond the qualified low 8-MiB
envelope. This saves live memory without weakening ownership checks or moving
installed BIOS data beyond its boot-area limit. It does not solve arbitrary
firmware maps: relocatable/sparse loading remains a separate architectural task.
Production decoder round trips, malformed lengths/references, recovery replay,
actual QEMU/VMware UEFI and BIOS startup are required on the final candidate.

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
