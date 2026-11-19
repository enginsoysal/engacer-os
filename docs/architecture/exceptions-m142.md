# M14.2 - Native x64 exception dispatch design

Status: vectored hardware-fault continuation has scoped native development proof. A first compiler-generated C structured-handler/finally profile also has native development proof below. Broader unwind coverage and full M14.2 release qualification remain incomplete. Existing child-process proofs remain separate.

## Capture and continuation boundary

Use a process-local registered runtime dispatch entry and a lazily mapped, guarded exception stack for each thread. Preserve the real trap registers, FXSAVE state, exception code, fault address and access direction in Windows-compatible records. Bound nested dispatch to four levels. Place a nested packet below the interrupted exception-stack pointer; never overwrite an active handler frame with a fixed per-depth buffer.

The kernel retains only bounded packet ownership/depth administration. Full contexts live on the process-owned exception stack, avoiding sixteen permanent copies of four 1,232-byte contexts in the kernel metadata slab. The dedicated exception-stack region must not overlap normal thread stacks, TEBs, PE images or virtual allocations. Release its resident pages with the owning thread.

Exception return accepts only the current thread's top owned packet. Validate readable records, executable user continuation, writable user stack, user segments, permitted flags and MXCSR before restoring FPU state. Never allow user-supplied FXSAVE bits to cause a kernel fault. An invalid packet, exhausted nested stack or unsupported context feature ends that protected process clearly.

## Windows ABI and unwind metadata

Use the actual AMD64 CONTEXT layout with compile-time size/offset assertions, including 512-byte FXSAVE state and nonvolatile integer/XMM registers. Populate EXCEPTION_RECORD and EXCEPTION_POINTERS from the real fault. Access violations distinguish read, write and execute faults. Vector-specific codes remain visible in retained process exit status when handling fails.

Read checked image-relative RUNTIME_FUNCTION entries and version-1 UNWIND_INFO. Validate sorted ranges, alignment, image bounds, prolog offsets, variable-length unwind-code slots, saved-register memory, chained records and executable language-handler targets. Bound chains and frame traversal. Implement supported nonvolatile pushes/saves, stack allocation, frame-pointer establishment and XMM saves with native compiler-generated fixtures. Leaf returns, partial prologs and epilogs require their own tests; blindly popping every frame is incorrect.

Start with vectored handlers and C structured handlers. Run filters and finally funclets using the Microsoft x64 ABI and preserve real continue/search/execute decisions. Generic C++ exception personalities, unsupported metadata versions and dynamic function registration require implemented contracts of their own. Do not substitute a successful handler return for actual context restoration or stack unwinding.

The compatibility runtime itself uses a different compiler ABI and currently lacks Windows unwind tables. A fault inside one of its frames must not be treated as an ordinary Windows leaf frame. Explicit RaiseException capture needs an assembly bridge to the actual Windows caller; unsupported cross-runtime unwinds must remain contained and clearly refused until metadata/bridges implement them.

## Native acceptance

Test real handled access violations with altered continuation, compiler-generated C try/except and try/finally, saved nonvolatile registers/XMM state, nested faults and invalid continuation. Check unhandled child faults leave their parent and desktop usable. Include malformed/chained metadata, callback faults, explicit cancellation and twenty close/reuse cycles with zero unexplained retained pages. Host structure/parser checks are only supporting evidence. Qualify the final frozen ISO independently after these native tasks pass.

Sources: [Microsoft x64 exception handling](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64), [AMD64 CONTEXT](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context), [prolog and epilog rules](https://learn.microsoft.com/en-us/cpp/build/prolog-and-epilog), [vectored handler order](https://learn.microsoft.com/en-us/windows/win32/debug/vectored-exception-handling).

## Initial native implementation

Candidate `d5bf58b38587bffa8e78e90a72e11593` implements process-local exception/continue-handler registration, ordered bounded handler snapshots, a top-level filter, real AMD64 fault/context packets and checked kernel exception return. Its dedicated 32-KiB stack is allocated only for a thread that actually dispatches a fault; nested depth is capped at four. The handler table has 64 generation-checked records shared between exception and continue handlers. Closed registrations reject stale tokens.

[Native vectored continuation proof](../../evidence/M14/2/development/vectored-faults-native-v8.json) exercises 24 actual access violations and 24 illegal instructions per execution, handler order, access-direction/address/register fields, changed continuation RIP, continue callbacks and 128 registration-reuse cycles. Twenty repeated process closes retain zero managed pages. This is actual CPL3 execution, not a host parser check. [Compact installation and independent starts](../../evidence/M14/2/development/compact-startup-v8.json) and [the original 7-Zip lifecycle](../../evidence/M14/2/development/original-apps-native-v8.json) also pass on this candidate.

No Windows structured language handler, C++ personality, RaiseException bridge, dynamic unwind table or x64 stack-unwind compatibility is inferred from these tests. The existing structured-unwind guard remains explicit until implemented. [Native invalid-context checks](../../evidence/M14/2/development/invalid-exception-context-native-v8.json) reject a privileged continuation RIP and unsupported MXCSR bits with status `0xc0000028`, preserve a responsive desktop and retain zero pages on the second run after four one-time transition pages. Full nested-handler, secondary-thread fault and original unhandled-fault regressions remain separate required checks.

## Compiler-generated C structured dispatch development

Candidate `6a21b5cac2e7d5fef97aa466e2a67c32` adds checked ordered PE runtime-function tables, version-1 unwind operations, bounded virtual frame walks, C scope filters and finally funclets. Handler calls use the Microsoft ABI. Search preserves the actual interrupted context; a selected C scope restores the target frame and runs termination handlers for frames it leaves. Unsupported metadata and dispositions remain explicit refusals. This does not implement C++ exception personalities or the RaiseException bridge.

[Native C exception/finally proof](../../evidence/M14/2/development/c-seh-unwind-native-v9.json) runs twelve real fault-to-catch traversals with finally cleanup per execution, then twenty process closes with zero retained managed pages. [Child-process regression](../../evidence/M14/2/development/processes-native-v9.json) and [compact installation/startup](../../evidence/M14/2/development/compact-startup-v9.json) pass on the same compiled source. The first fixture omitted unwind tables for a helper that actually pushes a local value. Its [honest failed attempt and diagnosis](../../evidence/M14/2/development/unwind-fixture-metadata-failure-v9.json) are preserved; explicit compiler unwind-table generation fixes the fixture rather than weakening the runtime.

This is a scoped development pass. Before release, resolve zero-code metadata access, distinguish E-handler search from U-handler cleanup eligibility, complete epilog/chained metadata cases, test real filter callbacks and nested/secondary-thread exceptions, and repeat the full frozen-media regression. Make exception-stack resident pages demand-backed as well as thread-lazy. Do not infer these pending cases from the constant-filter/finally fixture.

## Threaded filters, nested faults and metadata bounds

Candidate `d0e249c637fcaca90a407bee9cadf7fb` changes the dedicated exception stack to demand-backed reservations: only touched pages become resident, and all owned pages are released with the thread/process. Zero-code unwind records are valid, and E-handler search eligibility is separate from U-handler cleanup eligibility.

[Real C filters/finally on five thread stacks](../../evidence/M14/2/development/c-filters-threads-native-v11.json) pass sixty actual fault-to-catch traversals per execution. [Four-level nested faults](../../evidence/M14/2/development/nested-faults-native-v11.json) pass 480 actual handled faults per execution across five independent Windows threads. Both repeat twenty closes with zero retained managed pages. [Valid chained/zero-code metadata](../../evidence/M14/2/development/chained-unwind-native-v11.json) also passes the threaded C corpus and twenty zero-retention closes.

[Malformed metadata](../../evidence/M14/2/development/malformed-unwind-native-v11.json) refuses cyclic chains, unsupported operands, oversized C scopes and invalid directory sizes without losing the desktop. [Invalid-context/depth probes](../../evidence/M14/2/development/invalid-exception-context-native-v11.json) reject privileged RIP, invalid MXCSR and a fifth nested fault; each second run retains zero pages after the first four transition pages. These remain scoped development proofs. General C++ personalities, dynamic function tables, the RaiseException bridge and unqualified epilog forms are not inferred from this corpus.
