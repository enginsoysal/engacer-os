# M12.8 shared native file dialogs

Status: M12-STAGE8-VM-v1 native qualification passes. [Matching complete public delivery](../../evidence/M12/8/publication-results.json)
passed before M12.9. Failed
prototypes remain diagnostic records, not qualified media.

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

The retry now passes actual multi-page CPL3 Open, Save as and Cancel with zero
retained managed pages. Other Files windows may navigate, select and open known
handlers while a different owner holds the picker. Requests that would replace
the shared modal broker remain refused, including unknown-type Open with. The
expanded fault, format, display and restart matrix is still pending.

The exact current VMware ZIP installs and starts twice without its ISO with all
shipped devices enabled. An isolated native write-fault clone keeps dirty text
and its original path, reports the error and permits Cancel without losing work.
Compile-only frames now measure 56 bytes for picker_editor_open12, 168 for the
checked staging helper and 312 for its broker, retaining the guarded 16-KiB stack.
The expanded feature/display/recovery gates are still incomplete.

A second native probe opened the actual BMP, then found a ZIP/Enter stack
overflow. The generic keyboard function reserved an 8192-byte control-index
array on every key, including nested file-dialog handling. M12 now computes Tab
focus with two bounded scans over existing controls, with the same order and
wrap behavior, no array, no new persistent buffer and no idle work. M11 retains
its historical conditional path. The failed candidate and frames are retained;
all current-media qualification must be repeated after rebuilding this fix.

The updated compile-only keyboard frame is 56 bytes, down from 8248; ZIP load
remains 4376 and the stack remains guarded at 16384. A fresh native probe
passes generic Tab/Shift+Tab order and wrap, BMP and ZIP Enter, chosen-folder
extraction and zero retained pages. An independent read matches all three ZIP
member payloads; its observer initially expected Extracted instead of the actual
unique Extracted1 name. That failed observer result is retained and the corrected
complete probe is being repeated. This is not final M12.8 acceptance.

Owner review also identified a second-window shortcut hazard: while a picker
was open, Ctrl+Shift+S could fall through to ordinary Save. Shortcuts now defer
to picker keys only for its focused owner. A different Editor routes through
the existing refusal, retaining its dirty text/path and the original owner.
Native regression explicitly checks both Ctrl+Shift+S and Ctrl+O, followed by
an intentional Ctrl+S. The interrupted candidate is recorded as an intentional
owned-test stop, not an OS crash; qualification restarts on the corrected media.

The shared dialog has a defensive 560x512 logical admission bound. Review
layout reserves a bounded three-line filename, path and separate feedback and
buttons. This bound is not a claim of native qualification at exactly 560x512.
The real 1280x1024 probe showed that the existing global scale control refuses
200% and retains 100%, because ui73_set_scale requires at least 1024x768 logical
pixels. Record that as a refused-size route, not a 200% or minimum-height pass.
Actual compact 800x600 startup, light/dark, 150% and 4K are separate profiles.
M12.16 must reconcile the global choice limit with smaller startup modes and
qualify appropriate disabled choices and feedback. Smaller picker admission
receives an explicit sizing message rather than overlapping review controls.

While a picker is open, Settings explains that it must be finished or
cancelled before display-size changes. This preserves the admitted layout and
all pending work across other-window use; theme changes remain independent.
Dialog feedback uses shared readable text ink in both themes instead of the
legacy fixed red (about 4.07:1 on light paper and lower on dark backgrounds).
The dedicated native probe covers the scale refusal and other-owner shortcuts.

## Background transfer review boundary

The native M12.8 owner checks qualify foreground app requests. Admission while
a pre-existing background transfer is active is not qualified: that transfer
can later request its own conflict review through the shared broker. Finish
or cancel transfers before opening a picker in this stage. M12.14 must qualify
bounded admission/arbitration against actual transfer conflicts, retaining the
original document and pending choice. This is an explicit feedback-integration
carry-forward, not a claim that concurrent background review passed.

## Qualified outcome

The final candidate passes nineteen native scenarios, five display routes
(including explicit size refusal), two ordinary starts, three BIOS and three
exact VMware checks, actual compressed repair and twelve cached/full comparisons.
Independent reads verify original, saved/replaced, discarded-dirty and extracted
payloads. Fault clones preserve work and the original fixture. Added fixed shell
state is 6449 bytes, with zero retained managed pages and unchanged deliberate
allocation-failure count. [Acceptance](../../evidence/M12/8/acceptance-results.json)
and [resources](../../evidence/M12/8/resources.json) describe the exact scope.
