# M14.2 - Shared Windows synchronization

Status: implemented development profile with native checks; complete M14.2 release qualification remains pending. [Execution contract](runtime-m142.md), [child-process ownership](children-m142.md).

## Ownership and names

Events, semaphores and waitable timers live in a bounded supervisor-only registry. Each Windows process holds generation-checked grants with its own access mask; an integer copied from another process does not become an owned handle. Default security and explicit named opens are supported. Custom security descriptors, arbitrary inherited handles, mutexes and APC callbacks are separate unsupported profiles.

Names compare exact UTF-16 units. In the current single local-user/session profile, an unprefixed name and its Local-prefixed form identify the same object; the Global-prefixed form is distinct. Name prefixes are case sensitive. Registry ownership follows the protected native user-root grant. This does not implement multiple Windows sessions, service privileges, impersonation or general Windows ACLs.

Creating an existing same-kind named object returns another grant and reports already-exists without changing its original state. A different kind under that name fails. Open access masks control actual modify and synchronize operations; wait-only grants cannot signal events. Closing one grant leaves independent grants valid. The object survives its creator while another process retains a grant. Final close or process teardown releases it.

## Atomic waits and timers

WaitForSingleObject and WaitForMultipleObjects enter the kernel with a copied bounded handle list. Validation, signaled-state checks, auto-reset/semaphore consumption and entering a blocked state happen atomically on the protected Windows worker CPU. Wait-all never consumes only a subset. Lists may mix owned process/thread, event, semaphore and timer handles. Invalid/stale handles and duplicate object aliases refuse clearly.

Completion, signal and timer transitions reevaluate actual waiters. Each thread keeps its deadline and result independently; one process cannot clear another process's state. Active waited-on timers and finite timeouts share the existing PIT ownership lease with networking. Indefinite waits without an active timer need no Windows periodic poll; the normal desktop halt path remains available. Periodic timer catch-up is bounded arithmetic, not a loop for every missed tick.

## Bounded storage

| Component | First profile limit |
| --- | --- |
| Shared objects | 128 across live Windows processes |
| Objects created by one process | 32 while still retained |
| Synchronization grants | 64 per process |
| Handles in one wait | 32 |
| Object name | 95 UTF-16 units; longer names refuse |
| Shared registry pages | Eight 512-byte records per page; at most 16 pages |

Registry pages allocate only when used and return after their last live record disappears. No registry data pages are reserved while unused. Fixed registry administration is 264 component bytes, excluding linker padding; it is not total OS memory. Process wait/grant state belongs to the already lazy kernel metadata slab. [Compiler-derived layout](../../evidence/M14/2/development/metadata-layout-v12.json) separates these bounds from actual native memory measurements.

The earlier per-process user-mode object tables could not provide parent/child named sharing. Kernel ownership also makes mixed waits atomic and keeps another process from modifying raw synchronization records. This replaces those tables rather than maintaining a second implementation with diverging semantics.

## Native development evidence

Candidate `08c59243fbe774363546a5271575797c` passes [parent/child sharing](../../evidence/M14/2/development/named-sync-native-v12.json): Local/default aliases, separate Global names, existing-object state, independent grants, modify/wait access refusal, cross-kind refusal, shared semaphore/timer behavior, atomic mixed wait-all and real child exit codes. Twenty closes retain zero managed pages. A separate child retains and uses an object after its creator exits; its second run retains zero pages after four first-run transition pages.

[Named-event group cancellation](../../evidence/M14/2/development/named-cancel-native-v12.json) cancels four private processes blocked on one shared event 21 times. All observed blocked snapshots have both configured CPUs halted; after the first four transition pages, subsequent retention is zero. The [thread/synchronization regression](../../evidence/M14/2/development/threads-native-v12.json), [static TLS regression](../../evidence/M14/2/development/static-tls-native-v12.json), [original 7-Zip lifecycle and 106 hashes](../../evidence/M14/2/development/original-apps-native-v12.json) and [compact installation/startup](../../evidence/M14/2/development/compact-startup-v12.json) pass on the same compiled source. These checks are scoped development proof, not full M14.2 or universal Windows compatibility.

Sources: [Windows kernel-object namespaces](https://learn.microsoft.com/en-us/windows/win32/termserv/kernel-object-namespaces), [CreateEventW ownership and lifetime](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createeventw).
