# Windows apps: what works now and what M14 adds

**Historical M14.0 research record:** its qualified download was M13.13; the research did not provide a new ISO. For current native behavior use the [M14.2 Windows guide](windows-m142.md). Existing native Windows support covers one pinned original 7-Zip x64 console/MSI profile. The original GUI File Manager, Notepad++ and SumatraPDF are M14 targets; this research does not claim they currently install or run.

## The intended normal experience

Open a supported original installer from Files, review it, install through readable graphical steps and launch the real Windows app from Start. Work with your own files, save, restart Engacer OS and reopen them. Remove the app from the normal app-management route without deleting personal documents or breaking the desktop. Portable originals are useful diagnostic checks, not substitutes for required installation.

## Why the exact download matters

The measured Notepad++ 8.9.9.1 x64 EXE installer is itself 32-bit. Its original x64 MSI is the planned M14 route, with required custom actions still to implement. SumatraPDF 3.6.1 has an actual x64 EXE installer. 7-Zip 26.06 has the pinned original x64 MSI. Names alone never establish the architecture of helpers or plugins. M15 will add x86 and mixed installation chains; M16 covers Win16/DOS routes.

## Speed and resource use

CPU, RAM and storage traffic are core requirements for the whole OS. Every implementation stage measures its resource effects. M14.15 blocks final release until the same real app tasks, correctness and optimization checks pass. Current research contains no invented performance figures for unsupported apps. [Architecture and measurement protocol](../architecture/windows-m14.md).

Read the [sixteen-stage plan](../milestones/m14.md), [M14.0 findings](../milestones/m14-0.md) and [exact target inventory](../roadmap/m14-targets.json). Use the [current install guide](install-m1313.md) for the available native media.

The [corrected M14.0 research release](https://github.com/enginsoysal/engacer-os/releases/tag/m140-v0.14.0-research.2) provides the plan, inspection tools and reports. It contains no new OS image or downloaded third-party app binaries.
