# M14.8 native EXE installer design

M14.7 native and scoped public delivery pass. M14.8 is in development; original Sumatra installation and its reader remain unqualified.

## Execution and authority

Use the existing own kernel, x64 PE loader and ABI. The unchanged installer executes its actual instructions and required original helpers. A source review binds file hash, arguments, destination and installation authority. User mailbox fields cannot grant kernel permissions. Unsupported required operations fail clearly.

First use a labelled diagnostic clone to inspect entry, TLS, exception and actual API behavior. Replace private dispatch instrumentation with the ordinary shipped source-selection route before qualification. A frame, banner, manual extraction or replacement installer is insufficient.

The matching 3.6.1 source identifies self-copy, embedded LZMA extraction, native GUI controls, an installer thread and registry/shortcut effects. Check invocation against that version. Optional preview/search/update families remain separate.

## Resources and persistence

### Restricted Windows identity

Windows clients use the current native owner's restricted interactive profile.
The kernel's read-only W8_SYS_SECURITY148 query verifies the actual owner root
and reports authenticated/user/interactive categories without allocating token
objects or adding services. Existing syscall numbers remain unchanged; the new
query is appended. It changes no filesystem or registry grant.

CheckTokenMembership with a null token maps that profile to Everyone,
Authenticated Users, Builtin Users and Interactive well-known SIDs. It does not
map the process to Administrators, LocalSystem or a service account. A selected
product's installation review gives bounded broker authority, not Windows
administrator membership. This prevents an installer privilege query from
inventing broad OS access. Explicit token handles, impersonation and the full NT
token/ACL model remain unsupported; their calls must fail visibly.

SID allocation/serialization is ordinary caller-owned data. Neither constructing
an Administrators SID nor changing user-writable startup fields changes the
kernel-owned identity profile or authorization. This kernel query is preferred
over inferring membership from mutable environment strings or pretending that
every installation runs as administrator.

Allocate session state lazily and account image, heap, stack, kernel, framebuffer and caches separately. Stream OS-owned copies and hashes in bounded chunks. Preserve original allocation semantics and measure high-water/retained pages rather than silently expanding all quotas. Whole-system optimization remains M14.15.

Use an explicitly selected fresh destination and preserve personal files, modified app data and protected records. Original removal and required children must run. Independently inspect outputs and persistence after restarting. Later M14.11 repair/upgrade work does not waive the normal removal/reinstall chain or current data protection.

## Evidence

Record source/media/build identity, original hashes and architectures, API/fault traces, native windows/input, actual file/registry/shortcut effects, child executions, independent starts and resource limits. Preserve failures and distinguish private routing probes from shipped behavior.

[Stage gates](../milestones/m14-8.md), [vendor source](https://github.com/sumatrapdfreader/sumatrapdf/blob/3.6.1rel/src/Installer.cpp), [official command line](https://www.sumatrapdfreader.org/docs/Installer-cmd-line-arguments), [M14 requirements](windows-m14.md).
