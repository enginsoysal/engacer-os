# Your first day with M14.2

Status: native qualification passes within M14-STAGE2-VM-v1. Actual website publication is being verified.

Start with the [matching VMware installation guide](install-m142.md) and [release limits](../releases/m142-v0.14.2.md). M14.2 retains the existing native desktop and adds native Windows processes, threads, TLS and selected C exception handling while retaining the optional Firefox installer download. This is development media for the named test profiles.

## Find your way around

Click an item once to select it; use the configured double-click or Enter to open it. Open Files for Home, Desktop, Documents and Downloads. Back, Forward and Up navigate folders. Start search finds installed native apps. Right-click or Shift+F10 opens the available context menu. The taskbar switches between open windows.

The retained desktop, Files and personalization controls are explained in the [desktop guide](desktop-m135.md), [Files guide](files-m137.md), [Start and taskbar guide](start-m136.md) and [Settings guide](settings-m1311.md). Their original qualification records remain historical; the matching M14.2 release records the new media's actual tests.

## Try the Windows changes

Open **Windows Apps** from Start. Install the included original 7-Zip console profile, run it and try the sample archive/extraction actions. **Check a Windows file** inspects an original AMD64 EXE/DLL without starting it. This helps explain loader compatibility; it does not mean every Windows installer or GUI works.

Open **Browser → Browser choices** for the original Firefox x64 installer download. Downloads shows progress and offers Cancel. A successful download is saved in Downloads; it does not run automatically. Firefox installation and execution remain unavailable. Follow the [Windows and browser tutorial](windows-m142.md) for the exact distinction.

## Keep your work

Save documents explicitly before shutdown and keep a separate backup of anything important. Use the [saved-work guide](stability-m1313.md) for retained recovery behavior and historical stability limits. M14.2 does not repeat the earlier long-duration observation or establish unlimited uptime, physical hardware, GPU gaming or general Windows compatibility. The [M14 plan](../milestones/m14.md) records the remaining runtime and optimization stages.
