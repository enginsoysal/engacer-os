# M12.8 shared native file dialogs

Status: implementation and qualification in progress. M12.7 remains the
published native download. This plan does not claim pending tests passed.

## One bounded owner dialog

Open, Save as and Choose folder share one native picker, using the existing
owner-scoped review/input broker. It consumes no additional app-window slot,
worker, framebuffer or heap queue. A second request cannot replace an unfinished
dialog. Other windows remain usable; returning to the owner restores its dialog.
Cancel preserves its document, selection and original location. Optional apps
cannot become required dependencies of Files or the desktop.

Reuse shared typography, controls, original file icons, natural folder-first
ordering and real native volume metadata. Back/Forward/Up, an editable location,
Home/Documents/Downloads/Pictures and bounded page controls retain the same
meaning as Files. One click selects; double-click or Enter opens a folder/file.
The picker retains at most eight locations and 1,024 stable source IDs, rather
than duplicating file payloads or allocating a cache for every app window.

The initial consumers are Text Editor Open/Save as, Image Viewer Open BMP,
Archive Manager Open ZIP and its actual Choose folder extraction destination.
Existing format/size/worker limits still apply. This is native app integration,
not a new foreign Windows common-dialog ABI. USB files must first be copied into
a native folder through Files; direct USB editing/overwrite remains unsupported.
Explain that capability instead of presenting a writable external destination.

## Preserve work until a checked commit

Navigating and selecting write no file. Open validates the selected source and
format before replacing the app's view. Dirty Editor documents require an
explicit Save/Discard/Cancel review; failed saves or invalid new sources retain
the unsaved document. Save as accepts an actual writable native folder and a
validated supported filename. Text type adds .txt only when appropriate; the
All files choice retains an explicitly chosen extension policy.

An existing destination requires explicit replacement review. Capture and check
its identity/size/CRC again before writing; a changed or protected/in-use target
is refused. Cancel/Back never mean Replace. Keep the original Editor path and
unsaved text on failure. New folder is a separate explicit create operation,
with validation and a clear return to the picker; it is not a side effect of
typing a location. Native storage still controls quotas, read-only state and I/O.

Choose folder controls a real Archive Manager extraction destination. Extraction
still creates a new unique subfolder and retains the original ZIP, format limits
and partial-output explanation. A chosen folder must not bypass system or
stream-ownership guards. It does not authorize arbitrary overwrite or USB writes.

## Appropriate remembered locations

Keep separate bounded Open/Save/folder destinations for the current local user.
Commit a versioned CRC-checked optional preference only after a successful
choice. Invalid, missing or removed paths fall back to Documents/Downloads as
appropriate. Cancel does not update these preferences. Startup and the base
desktop must still work without this record or any optional consumer app.

## Required verification

Use ordinary guest input on exact-source owned installations for navigation,
single/double click, filters, Open/Save as/Cancel, dirty documents, explicit
replace/back, missing or changed destinations, protected paths, real chosen
extraction, independent persisted bytes and ordinary installed restarts. Verify
owner modality and other-window work. Check actual narrow layouts, Light/Dark,
150% and 3840x2160/200%, fixed/peak/retained memory and halted idle CPUs. Run the
matching VMware/BIOS, compressed recovery and cached/full rendering checks.
Host validation tests supplement these native tasks; they cannot replace them.

M12.14 owns the previously recorded menu/conflict feedback refinements, M12.16
owns HiDPI cursor isolation and M12.18 owns final controller/application and
BIOS/AHCI stress qualification. Every native stage still closes its English
manuals, immutable GitHub assets and complete website before its successor.

## Guarded-stack correction found by the first native probe

The initial candidate installed and passed Save as/Cancel, but native Enter in
Open caused a double fault. Compile-only stack usage measured 8,248 bytes in
keyboard and another 8,248 in the new text-load helper, exceeding the existing
guarded 16-KiB kernel stack even before intermediate calls. That failed candidate
is not qualified; its serial log, manifest and frame report are retained.

Keep the stack guard and stack size. Stage each checked source block directly
from the native volume's existing 4096-byte scratch page into the selected
worker's already allocated IPC input pages. Validation-only requests do not
change those input pages. Applying rechecks ASCII/size, complete CRC and source
identity, then invokes the ordinary response-validating broker. The old kernel
view is replaced only after a valid successful worker response. No new kernel
payload buffer, per-window allocation or mailbox ABI is introduced. The prepared
input flag stays private to the trusted broker; ordinary requests still require
and copy their supplied input. Hosted source/I/O/identity/fault tests supplement,
rather than replace, the real CPL3 and dialog retry.
