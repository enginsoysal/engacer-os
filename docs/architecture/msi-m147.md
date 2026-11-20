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
