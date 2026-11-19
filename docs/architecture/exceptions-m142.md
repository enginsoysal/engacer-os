# M14.2 - Native x64 exception dispatch design

Status: vectored hardware-fault continuation has scoped native development proof. Structured exception dispatch, x64 metadata unwinding and full M14.2 release qualification remain incomplete. Existing child-process proofs remain separate.

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
