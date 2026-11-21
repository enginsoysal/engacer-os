# M14.7 MSI execution contract

## How and why

Retain the checked CFB/MSI reader, pinned cabinet decoder and native protected worker. Replace hard-coded product identity/destination/action behavior with a checked database-derived session. Package hashes identify reproducible qualification inputs; they must not substitute for parsing required behavior. No host Windows Installer service or embedded guest implements the installation.

Properties, conditions and formatted fields form a bounded reusable engine shared by standard and custom actions. Evaluate actual sequence conditions against installation state; required actions that evaluate true must run. Validate the entire selected plan before target mutation. Directory grants remain within the selected product root and explicitly authorized per-user settings, never arbitrary host paths.

Install through a durable recovery plan and bounded staged writes, verify exact payload bytes, and publish product registration only after success. Cancellation/failure must be recoverable without removing unrelated documents or altered product files. Component ownership and registry/shortcut effects require independent verification rather than retaining tables as if their effects were implemented.

The original Notepad++ package contains an AMD64 WiX custom-action DLL and formatted xcopy/cmd operations. Its real export must execute with native MSI services and real child-operation semantics. A synthetic substitute, unconditional skip or manually copied installation is not acceptance. The x86 Notepad++ EXE remains M15; its x64 MSI is mandatory in M14.

## Verification boundaries

Hosted parser/condition/malformed-input tests support native qualification. They do not establish original MSI installation. Native tests must independently inspect installed bytes and registration, restart, remove/reinstall, exercise language conditions and required custom actions, and inject cancellation/write failure against owned disposable media. Preserve failures and evidence; do not waive the required original task corpus.


## Condition core development

The allocation-free production condition core passes 12170 supporting host checks, including the exact original language/install/removal/downgrade conditions, independent boolean truth tables, malformed-input bounds and numeric/string distinctions. It is not yet connected to a native installation session. Limits are 4096 input bytes, 2048 lexical steps, 32 unary/parenthesis levels and 72-byte symbols. Non-ASCII equality/substring bytes remain exact; unsupported non-ASCII insensitive/ordered comparisons return a condition error rather than an incorrect result. [Supporting evidence](../../evidence/M14/7/development/condition-host-initial.json).

Semantics follow the primary [MSI condition contract](https://learn.microsoft.com/en-us/windows/win32/msi/conditional-statement-syntax) and [formatted-field contract](https://learn.microsoft.com/en-us/windows/win32/msi/formatted). Allocation/lifetime and native original-package qualification remain mandatory.


## Property and scalar formatting development

The new private property session allocates lazily and supports bounded insert/update/delete with case-sensitive keys. Deterministic payload/index allocation failures preserve existing values and release partial allocations. The selected original xcopy/cmd formatted fields pass exact-byte tests, including quotes, spaces, missing values and literal bracket escaping. Four hundred supporting checks pass, with zero retained host allocations after destruction. Limits are 256 properties, 72-byte names, 4096-byte values and a 128-KiB transient session allocation budget. This is a ceiling, not a permanent reservation. [Supporting evidence](../../evidence/M14/7/development/properties-host-initial.json).

Nested property keys, optional formatted groups and binary NUL fields currently refuse explicitly. Costed file/component/environment references require an explicit session resolver. These cores are not yet native installer qualification; original standard actions, required WiX execution and durable rollback remain open.


## Native session and streaming development

The owned condition/property/scalar-formatting PE passes 21 complete native lifetimes on immutable accepted M14.6 media, with zero retained managed pages and a successful original 7-Zip console afterward. Independent recompilation matches the executed fixture hash. This qualifies the new core in a protected native process; it is not a new OS build or reusable MSI installation. [Native pilot](../../evidence/M14/7/development/session-native-pilot/results.json).

Original database inspection identifies 217 Notepad++ payload files totaling 28130419 bytes and an 859-block LZX cabinet. The legacy whole-output eight-MiB decoder cannot handle this. The new production reader validates the complete cabinet before output, streams through the pinned decoder and calls a transaction-owned sink. All 106 original 7-Zip and 217 original Notepad++ file hashes match an independent built-in data-only decoder. The 2684 host checks include malformed headers, cancellation and deterministic allocation failures, with zero retained allocations. Notepad++ decoder/metadata peak is 335720 bytes, excluding original MSI/CAB input and transaction state; it is not total OS/process RAM. [CAB evidence](../../evidence/M14/7/development/cab-host-initial.json).

The incremental SHA-256 API reuses the existing compression function while preserving the original one-shot API. Its 261 supporting checks compare padding boundaries and chunk partitions against independent hashlib digests. A consumed context refuses reuse until initialization. The new path permits hashing streamed original files without allocating their complete expanded bytes. [Hash evidence](../../evidence/M14/7/development/sha-host-initial.json). Native streaming and actual standard/custom-action installation remain open.


The combined production streaming-CAB/incremental-SHA PE now passes 21 complete protected native process lifetimes on accepted M14.6 media. Each lifetime verifies all 323 original 7-Zip/Notepad++ files against independently derived SHA-256 values, retains zero managed pages after closing, and the original 7-Zip console still runs afterward. [Native streaming pilot](../../evidence/M14/7/development/cab-native-pilot/results.json). This qualifies the new streaming/hash cores; standard MSI actions, WiX custom actions and a new M14.7 OS/ISO remain unqualified.


## Original database plan development

The read-only plan now derives product identity, properties, launch conditions and sorted execute-sequence actions from the actual MSI tables, rather than admitting a product by one digest. It recognizes the selected standard-action metadata and Type51/Type3137 custom-action metadata; recognition does not execute those actions. The original Type51 property assignments produce the independently expected quoted xcopy/cmd values when explicitly supplied costing results. Directory costing and original WiX execution remain unimplemented.

Notepad++ first refuses the old CFBv3-only reader. That failure is preserved. Checked CFBv4 now uses 4096-byte sectors, 1024 FAT entries per FAT sector, matching directory-sector counts, and a MiniFAT allocation bound scaled to the real sector size. CFBv3 retains 512-byte sectors. Database close releases all owned strings/directory/mini-stream/catalog state, allowing repeated sessions without retained allocations. [Primary CFB geometry contract](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/05060311-bfce-4b12-874d-71fd4ce63aea).

The 3687 supporting host checks compare both original action/property tables with independent read-only Windows Installer metadata, open/close each original 21 times, verify the actual Type51 assignments, and refuse unknown mandatory actions, geometry mismatch, incorrect directory counts, oversized MiniFAT, FAT cycles and partial sectors in isolated owned test processes. All valid closes retain zero allocations. Environment/component/feature condition prefixes currently refuse until their real state resolvers are connected. [Plan evidence](../../evidence/M14/7/development/plan-host-initial.json), [preserved initial CFBv4 refusal](../../evidence/M14/7/development/plan-cfb4-refusal/diagnosis.json). None of these checks qualifies installation, standard-action effects, rollback or original custom-action execution.


## Directory, feature and file costing development

The read-only cost model now resolves the original directory graphs, one isolated program alias, feature levels/conditions, component relationships and all selected file paths. It rejects unsupported overrides, unsafe ASCII leaves, missing/cyclic graph references, unsupported flags, duplicate file destinations and unsupported external/multiple cabinet layouts before target mutation. Original Notepad++ default/language cases select 217 files; the authored NOUPDATER condition selects 212. All 106 original 7-Zip files remain selected. Costed file/component formatted references are actual bound paths; unsupported short-name/environment/binary formatting still refuses.

The 44679 supporting host checks independently compare both original metadata sets, file destinations, byte totals, 21 close/reopen lifetimes per original, four Notepad++ language/updater combinations and Type51/format bindings. Remaining target-writing standard actions and required original WiX execution are still unqualified. [Cost evidence](../../evidence/M14/7/development/cost-host-initial.json).

The x64 MSI profile distinguishes [SystemFolder](https://learn.microsoft.com/en-us/windows/win32/msi/systemfolder) (SysWOW64), [System64Folder](https://learn.microsoft.com/en-us/windows/win32/msi/system64folder) (System32), and 32/64-bit Program Files aliases. Earlier scalar formatter probes supplied example properties; they did not qualify automatic system-folder discovery. Engacer-provided command utilities execute its own native AMD64 code; a logical SysWOW64 utility route does not establish execution of original Windows x86 binaries. M15 remains separate.

## Lazy native service decision

The next integration places the reusable installer in an original Engacer-authored native x64 msi.dll and msiexec.exe, invoked by the existing protected Windows worker. Both execute directly on Engacer APIs/kernel; this introduces no Windows guest, Wine runtime or second OS. Ordinary Windows app startup must not allocate the MSI database tables or cabinet decoder. Existing legacy M8 code remains available to its historical non-M14 build path.

This division lets the original WiX DLL call real MSI session/record/property exports in the same protected native process, while the native desktop owns user confirmation and installation authority. Original OS command semantics are implemented by Engacer-owned native helpers. Required imports reached at runtime must have real behavior; unreachable diagnostic guards must fail explicitly rather than return fake success. Static import admission alone never qualifies a custom action.

Install writes use a new, isolated product root and staged payloads, then known hashes and a durable recovery plan before publication. The original custom actions must see their real installed paths at the proper sequence point. Registry, shortcut, product ownership, cancellation and recovery effects remain separately required. None of this integration is advertised as implemented by the cost-model tests above.

### Boot-module placement

The first development build exceeded the existing 8 MiB low-memory kernel envelope by 56,620 bytes. It is retained as a failed candidate, not qualified media. The own installer DLL and executable now travel in a versioned extension after the unchanged original MSI inside the reserved INIT boot module. The existing 4 MiB module limit remains unchanged. EFI and kernel share bounded shape validation; the kernel checks both asset digests before retaining borrowed pointers. This moves storage away from firmware-reserved low memory; it does not remove the assets from total guest RAM. Runtime installation copies the validated assets into the system installer directory. Native qualification remains pending.

### Native read-only service integration result

Candidate ed82ff06e537d9a4b026625e5ce25653 installs and reaches the desktop through the retained-ISO restart and two independent no-ISO starts. Its own x64 MSI service parses both unchanged original MSI packages in CPL3: 106 7-Zip files and 217 Notepad++ files. Five measured repeated lifetimes per package retain zero managed pages and no native UI state. The existing 7-Zip install/run/archive/extract/remove/reinstall path and all 106 payload hashes also pass. These are development results: generic write actions, actual original WiX execution and Notepad++ installation remain open. No M14.7 release is claimed.

### Native MSI export foundation

The reusable DLL now implements real privately owned record fields, generational handles, property access, condition evaluation and bounded log delivery. Records allocate lazily with 64 live handles, 32 data fields plus field zero, 4096-byte string values and a 256 KiB transient record budget. Failed updates preserve prior values; stale handles refuse. UTF-16 output counts code units and never truncates a surrogate pair. ANSI exports use the existing runtime UTF-8 ACP. A real critical section serializes the shared context; record creation also works without an installation session. Bind/unbind occur only while custom-action threads are quiescent.

Supporting tests pass 3056 ownership checks, 2108 Unicode/buffer checks and 6466 API checks against both original MSI databases, including real host-lock concurrency. Host tests execute only Engacer code; original custom actions remain unqualified. The native DLL caller is being tested separately on the frozen development candidate. Required MSI exports still missing are not silently supplied.

Primary API references: [MSI records](https://learn.microsoft.com/en-us/windows/win32/msi/working-with-records), [record formatting](https://learn.microsoft.com/en-us/windows/win32/api/msiquery/nf-msiquery-msiformatrecordw). Required original ordinal names were read from host export metadata only; no Windows code is copied into the OS.

### Deferred API context and record formatting

The next API revision adds numeric-record-then-property formatting, costed target-directory lookup, real session reboot-request flags, and restricted deferred CustomActionData/ProductCode/UserSID reads. Deferred formatting only exposes CustomActionData/ProductCode, following the primary deferred-context contract. Unsupported nested/optional formatted groups still refuse explicitly. Reboot flags record requests; they do not reboot the machine automatically. Supporting API tests now pass 6512 checks; this revision is not yet the native-export pilot DLL.

References: [deferred context](https://learn.microsoft.com/en-us/windows/win32/msi/obtaining-context-information-for-deferred-execution-custom-actions), [run modes](https://learn.microsoft.com/en-us/windows/win32/api/msiquery/nf-msiquery-msigetmode), [record data size](https://learn.microsoft.com/en-us/windows/win32/api/msiquery/nf-msiquery-msirecorddatasize).

### Machine registry development

The next kernel candidate adds protected persistent machine namespaces with distinct 32/64-bit views. Records use trusted machine identities independent of the current account; the existing HKCU serialization remains unchanged. Opening a machine key for write, creation, value mutation and deletion require the confirmed install/remove worker context. Ordinary RUN workers can query either view, never acquire machine write authority. Cross-view overrides through an already opened opposite-view handle currently refuse rather than silently read the wrong view. The selected MSI software-key profile is the qualification target; complete Windows registry redirection and merged HKCR enumeration remain separate. Compiler checks pass; native persistence/rights tests are pending.

### Initial machine-view native result and retained refusal

Candidate 93b05fbf5b5e9b656c162819633c0d0e passes actual confirmed-worker writes to both machine views, independent no-ISO persistence, ten ordinary read-only lifetimes with zero retained pages, denied ordinary writes, removal-context cleanup and subsequent original-console operation. The separate retained HKCU regression fails check 046 because the first implementation accepted a previously unsupported HKCU view flag. This is a real contract regression, retained as a failure; the next revision restores the prior HKCU refusal instead of weakening that test. Machine-view success does not close the combined registry gate or M14.7.

### Runtime boot-module placement

After adding machine registry support, candidate 93b05fbf5b5e9b656c162819633c0d0e had only 688 bytes left below the unchanged 8 MiB live-kernel boundary. Extension version 2 therefore carries the existing Windows ELF worker as a third checked asset alongside msi.dll/msiexec.exe. The loader and kernel retain the same 4 MiB init-module bound; each own asset is limited to 1 MiB and has an independently checked digest. The installer copies the worker from this validated reserved module instead of a kernel read-only array. Installed boot still uses the ordinary on-disk worker and its small init manifest. This is placement headroom, not a claim that the worker disappears from live guest RAM. The shared production parser passes 452 shape/bounds checks; new native build qualification is pending.

### Retained-ISO BIOS failure

The version-2 runtime-module candidate passes UEFI install/restart/independent startup, original console tasks, both MSI previews, native MSI exports, the restored HKCU regression and machine-view rights/persistence. Its explicit BIOS test installs successfully but restarts into the retained ISO wizard. Generated live BIOS configurations have BIOS_CHAIN75=0 because historical feature detection searched host folder spellings that omit m14-native. This real failure is retained; BIOS qualification does not pass. The next builder passes the live-chain decision explicitly from the milestone identity, covering both CD and USB layouts independently of the host path. Installed BIOS stages retain their separate non-chain behavior.
