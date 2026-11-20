# Required original-runtime follow-ups

The pinned Notepad++ 8.9.9.1 x64 MSI and SumatraPDF 3.6.1 x64 EXE/GUI remain mandatory M14 targets. This dependency record does not narrow the corpus or label their interfaces as supported. Required runtime work belongs to M14.10; full installation/use/save/restart/removal scenarios still block M14.12 and final M14.15.

## Native startup observation

Frozen development 06c8de63a527c32ad9ec73f4b9e333bc advances both original programs beyond their actual read-only VirtualProtect calls. Both then fail at kernel32!FlsAlloc, before any original window. Protected worker creation is not interface qualification.

The observer resolves the direct call through the original x64 import thunk, including its optional REX.W prefix, to the original IAT entry. No name is guessed for unsupported call shapes. The earlier unresolved diagnostic is preserved, alongside the later independent read-only decode.

## Required fiber-local storage contract

Implement real per-execution-context values, bounded allocation/free, callbacks on context/thread teardown and free, callback-driven repopulation rules, thread/context ownership, last-error behavior and cleanup ordering. A TLS alias with ignored destructors would not meet this requirement. Qualify original startup separately from owned concurrency, callback, quota and cleanup tests. Do not silently ignore required callbacks or return a fake slot to pass CRT initialization.

Continue inventorying the next actually reached dependencies. Optional updaters, plugins and helper architectures remain separate named profiles. A bound import, refused call or mapped image is not an implemented API or compatibility percentage.
