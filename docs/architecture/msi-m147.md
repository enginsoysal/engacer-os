# M14.7 MSI execution contract

## How and why

Retain the checked CFB/MSI reader, pinned cabinet decoder and native protected worker. Replace hard-coded product identity/destination/action behavior with a checked database-derived session. Package hashes identify reproducible qualification inputs; they must not substitute for parsing required behavior. No host Windows Installer service or embedded guest implements the installation.

Properties, conditions and formatted fields form a bounded reusable engine shared by standard and custom actions. Evaluate actual sequence conditions against installation state; required actions that evaluate true must run. Validate the entire selected plan before target mutation. Directory grants remain within the selected product root and explicitly authorized per-user settings, never arbitrary host paths.

Install through a durable recovery plan and bounded staged writes, verify exact payload bytes, and publish product registration only after success. Cancellation/failure must be recoverable without removing unrelated documents or altered product files. Component ownership and registry/shortcut effects require independent verification rather than retaining tables as if their effects were implemented.

The original Notepad++ package contains an AMD64 WiX custom-action DLL and formatted xcopy/cmd operations. Its real export must execute with native MSI services and real child-operation semantics. A synthetic substitute, unconditional skip or manually copied installation is not acceptance. The x86 Notepad++ EXE remains M15; its x64 MSI is mandatory in M14.

## Verification boundaries

Hosted parser/condition/malformed-input tests support native qualification. They do not establish original MSI installation. Native tests must independently inspect installed bytes and registration, restart, remove/reinstall, exercise language conditions and required custom actions, and inject cancellation/write failure against owned disposable media. Preserve failures and evidence; do not waive the required original task corpus.
