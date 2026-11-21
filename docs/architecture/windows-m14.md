# M14 Windows x64 runtime and efficiency contract

## Execution and trust boundary

The owner approved the [eight consolidated M14.9-M14.16 work packages](../milestones/m14-consolidated.md)
on 21 November 2026. They supersede older future-stage numbering in historical
research below. Scope is the full original Windows 7/8/8.1/10/11 x64 application
landscape, including necessary mixed-architecture helpers, runtimes, services
and drivers. The pinned three originals remain regression fixtures, not the
compatibility scope or an application whitelist. M14.16 is the final integrated
optimization/release gate; efficiency is measured throughout. Current work must
finish M14.8 and then stop before M14.9 implementation.

Extend the existing direct AMD64 PE execution in a private native CPL3 address space. Original app code calls original Engacer API/NT-compatible implementations, which use the native kernel, storage, compositor and drivers. Do not replace a named app with a native imitation. This plan adopts neither a Windows/Linux kernel nor a Wine runtime. Reuse of any third-party implementation requires an explicit dependency/port/provenance/license decision and actual task qualification; it cannot be slipped in as a compatibility claim.

Separate loader, Win64 process/thread/exception model, file/registry/environment, USER/GDI/control/dialog and installation services. Stable internal interfaces must support later x86 and Win16 adapters without assuming identical pointer widths or semantics. App resources belong to processes/windows/generations; cancellation or faults cannot publish stale work into another owner. Compatibility services load lazily and are independently bounded. Standard apps remain optional.

## Research baseline and remaining gaps

The M14.0 baseline loader admitted at most eight modules and eight MiB per loaded file/image; actual Notepad++ SizeOfImage is 8,613,888 bytes and SumatraPDF is 20,840,448 bytes. M14.1 subsequently qualified checked demand-backed mapping and explicit per-process quotas. M14.2 qualified the documented native process/thread/TLS, shared synchronization and selected hardware-fault/C unwind profile. M14.3 retains those tests and qualifies bounded Unicode paths/search, shared files/locks, persistent user settings, inherited environments and file metadata independent of app removal. [File/settings scope](files-m143.md), [native acceptance](../../evidence/M14/3/acceptance-results.json). General GUI messages/controls, broader runtime families, COM and a reusable MSI engine remain unqualified. Read the retained [process/runtime contract](runtime-m142.md) and current file/settings scope instead of treating the original research gaps as current implementation status. Registry and security operations have scoped/refusal semantics. A matching function name is not correctness proof.

Notepad++'s x64-labelled EXE bootstrap is x86. Its original x64 MSI has x64 template metadata and an independently inspected x64 WiX DLL stream, but also required command strings invoking xcopy.exe/cmd.exe. Those operations need genuine compatible behavior in M14.7; skipping the actions or substituting a hand-copied install is not acceptance. 7-Zip carries optional x86 extension/SFX files: preserve payload presence while distinguishing unsupported execution. Static inspection cannot prove the complete dynamic dependency closure.

M14.1 now qualifies checked 32-MiB image/file mapping, 32 reusable module slots and bounded demand-backed image memory. Original Notepad++/Sumatra inspection does not execute their GUI or establish their complete runtime dependencies. See the [M14.1 loader contract](loader-m141.md) and [native evidence](../../evidence/M14/1/acceptance-results.json). M14.2 subsequently qualified static TLS, normal process-detach callbacks and the selected broader process/thread/exception profile; matching M14.3 regressions pass.

## Reproducible resource protocol

Reference profiles are the same named virtual hardware/controller/firmware, two CPUs, 512 MiB at 1920x1080 and 1024 MiB at physical 3840x2160. A separate 128-MiB/1024x768 capability/refusal profile preserves the lightweight OS goal without promising all applications fit. Record emulator/hypervisor, device settings, storage/cache backing, release/app hashes and actual surface dimensions. Host configured RAM is not kernel consumption. Do not use a native screenshot or host parser as app compatibility or GPU proof.

Use seven independent cold starts and seven warm starts per target after the first functional baseline exists. Cold means a fresh owned VM process and restored stopped test-disk snapshot; name separately any host/page/disk caches that cannot be flushed safely. Never claim physically cold storage from a fresh guest alone. Keep the same fixtures and scripted workload. Publish raw samples, median and p95, with observer cost/gaps and warmup recorded separately.

Measure wall start-to-interactive time and real app work, process and total guest CPU time, input-to-visible latency, private/committed/resident/shared memory, fixed reservations, managed peak, retained bytes and cache/surface budgets. Count file-level reads/writes, block/device bytes/requests, temporary files, flushes and eventual drained writeback. Sparse disk allocation or compressed archive bytes are not actual I/O traffic. Installed footprint is a separate metric. Aggregate shared pages once and include compatibility/kernel work, not only the app process.

## Initial budgets and release decisions

After completed app tasks, unexplained managed retention must be zero across twenty start/use/close cycles; explicitly shared caches require a separately declared cap and repeatable steady state. No new periodic compatibility polling worker is permitted; idle work must be event-driven and explainable (including app-originated timers). No unsolicited recurring disk writes are allowed in the registered quiescent scenario. Drained I/O and durable file hashes must agree after independent starts and controlled interrupted-write tests.

Before each first native app implementation is qualified, freeze that app's absolute CPU/time/memory/I/O bounds from the declared profile and observed working baseline. Those currently unsupported GUI metrics are explicitly unmeasured, not zero. From that point a >5% median start/CPU/I/O regression, >10% p95 input latency regression, increased retained memory or fixed-state growth blocks the stage until corrected or a quantified necessary tradeoff is explicitly documented before acceptance. Repeat when sample spread makes a threshold inconclusive; never select only the best run. An app's own computation imposes a floor; optimize avoidable OS/runtime overhead and total system cost.

M14.15 repeats the whole exact corpus on final frozen bytes and compares with the M14.12/M14.14 working candidates. Where a comparable Windows guest is already available, record the same original app/workload/profile as a reference, without taking over the owner's host or inventing Windows reference measurements. A faster-than-Windows claim needs actual comparable evidence. No speed result may sacrifice saved data, API semantics, visual correctness, security boundaries or user friendliness.

## Baselines and scope

M14.0 makes no native runtime changes. Its research baseline pinned M13.13 media and 613 compiled inputs; this is not the current native release. Existing [resource evidence](../../evidence/M13/13/resources.json) records fixed desktop 557,516 bytes, installer 48,412 bytes, font masks 251,248 bytes and the specific measured task peaks/retention. These are historical native tasks, not timings of the proposed GUI apps. M14.15 is a mandatory final gate; M14.14 remains a labelled candidate.

Sources: [Microsoft PE format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format), [x64 ABI](https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions), [64-bit MSI](https://learn.microsoft.com/en-us/windows/win32/msi/using-64-bit-windows-installer-packages), [read-only MSI stream interpretation](https://learn.microsoft.com/en-us/windows/win32/msi/record-readstream).
