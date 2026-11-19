# M14.3 - Windows files and settings ownership

Status: implementation design, **not native qualification**. [Stage acceptance](../milestones/m14-3.md). Existing M14.2 media remain the current qualified download.

## Path boundary

Normalize Windows names using trusted kernel startup roots, not a writable user mailbox. Keep Windows spelling separate from the native UTF-8 storage name. Convert well-formed UTF-16 explicitly, preserve stored spelling and reject over-budget names without truncation. Resolve existing path components with a defined invariant case mapping; reject ambiguous native names instead of selecting an unrelated file.

Support the selected C-drive absolute, current-directory-relative and root-relative forms. Canonicalize dot components before authorization. Device/UNC/unsupported extended forms must not accidentally become native paths. The existing native volume bounds whole paths and components; the Windows adapter must report those limits honestly rather than pretend to implement arbitrary NT long paths. Native storage stays case sensitive for native apps.

Use a shared, pinned case-mapping definition for file and registry identity; do not make security depend on the host compiler locale or a running user's locale. This provides a reproducible selected profile, not a claim of identical NLS tables across every Windows version. Literal Unicode identity and case matching are distinct from Unicode normalization.

The selected data is Unicode 17.0.0 simple case folding, C/S records only. A generated arithmetic-range table stores 1,512 mappings in 3,344 read-only component bytes. Full expansion and locale-specific Turkic folds are excluded. The [source, generator and license](../../third_party/unicode/README.md) are pinned. Host checks compare every code point to the independent official data, round-trip every valid scalar through the compiled codecs, and reject malformed/truncated input and undersized output. These are supporting checks, not native Windows file qualification. [Host evidence](../../evidence/M14/3/development/unicode-host.json).

## File objects and grants

The path foundation now routes the runtime adapter through a checked kernel syscall. It snapshots the process current directory under its existing blocking lock, reads bounded UTF-16 through checked user memory, and resolves existing native components with the shared Unicode table. GetFullPathNameW/A provide lexical full-name and required-capacity results without granting file access. A separate target-leaf mode preserves requested spelling for the later rename implementation while canonicalizing parent components. Existing file sharing, persistence and registry gaps below remain open; this foundation does not close M14.3.

The compiled policy passes explicit boundary cases and 5,000 deterministic mutations, including native case ambiguity, extended paths, malformed Unicode and protected-root traversal. The original extended-separator test failure and corrected supporting result are retained in [development evidence](../../evidence/M14/3/development/path-host.json). On development build `a9544396469dda7a62b514c651db6869`, [compact installation and independent starts](../../evidence/M14/3/development/compact-path-candidate.json) and the [original supported 7-Zip lifecycle and all 106 payload hashes](../../evidence/M14/3/development/original-apps-path-candidate.json) pass. A [synthetic Windows PE probe](../../evidence/M14/3/development/path-native.json) exercises the real native syscall, Unicode/UTF-8 names, lexical traversal, required capacities and malformed/unmapped input; twenty repeated executions retain zero managed pages after initialization. Its first fixture lacked a relocation directory and was correctly refused; that observation is retained separately rather than weakening the loader. These remain development observations rather than final stage qualification.

The kernel owns live file identity, pending data/deletion, access/share rules and byte locks. Process grants own independent positions and generation-checked handles. Validate an open against every existing grant in both directions before admitting it. All processes using the same file must observe the same pending object; a separate user-mode table per process would miss conflicts and lose changes.

Reuse native COW/CRC storage for durable publication. Keep dirty data bounded and allocate it only when touched; read untouched bytes from the committed file instead of copying a whole file into RAM on open. Flush must actually commit its acknowledged state. Failed writes cannot publish a successful partial result. Document the selected delayed-write/cancellation behavior separately from Windows cache-manager or universal power-loss semantics.

Internal loader/MSI reads and writes must not become a sharing bypass. Preserve existing product-ownership rollback and original payload checks. Rename/delete must consult actual open grants and preserve live file identity where supported. Unsupported asynchronous/mapped/device semantics fail clearly. Range-lock state belongs to file grants and disappears on close/process teardown; a failed lock cannot secretly acquire or consume another owner's range.

## Persistent registry

Writable user preferences are separate from the installed product's machine-registration view. Use the trusted user root for the backing namespace and validate every access, key/value identity and buffer size at the kernel boundary. A request for an unsupported registry view/security/volatile feature must be refused instead of ignored.

Prefer bounded independent key/value records over rewriting a large duplicated hive on every small update. Reuse native CRC and durable COW publication; record identity must be validated even if a name hash is used to keep storage paths short. A hash collision cannot alias another setting. Avoid a permanently loaded full-registry cache and unsolicited idle writes.

Preserve value type and exact data bytes. Size queries and short-buffer results differ from copying a string: queried registry strings are not guaranteed to include a terminator. Enumerate supported children/values with explicit name/data capacities. Generation-checked key grants retain their access masks and refuse stale or foreign handles. Independent disk-only starts must verify acknowledged settings.

## Environment and lifetime

An environment block belongs to its process. Seed implemented defaults, support real lookup/set/delete/expansion, and snapshot the parent's current block when creating a child unless the caller supplies a supported explicit block. A later parent mutation must not alter a running child's variables. Strings exposed by GetEnvironmentStrings require their own owned copy and release route.

Keep environment allocation bounded and lazy. User-selected TEMP, PATH or USERPROFILE values are data; they must never alter kernel authorization. Reuse the existing process/thread lifecycle and blocking locks, then prove fault/cancellation cleanup of every added resource.

## Sources and verification boundary

Microsoft documents the required interfaces: [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew), [file names and namespaces](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file), [LockFileEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex), [RegSetValueExW](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regsetvalueexw), [RegQueryValueExW](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regqueryvalueexw), [process environments](https://learn.microsoft.com/en-us/windows/win32/procthread/environment-variables). These describe Windows behavior; only matching Engacer native tests can qualify our implementation.
