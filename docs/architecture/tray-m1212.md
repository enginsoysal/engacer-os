# M12.12 — provider-backed system tray

Status: M12-STAGE12-VM-v1 native qualification passes for build `93839018f852f6b6ba79643004d5f101`. The complete public delivery passes: twenty downloads, 364 pages and 2,513 HTTP links, native homepage Save and actual desktop/mobile verification. M12.13 follows in order.

## How and why

One native flyout supplies Quick settings, USB drives and Calendar. It uses the
existing control registry, original icons, semantic typography and kernel
providers. It consumes no application-window slot, pixel cache or worker.
Small desktops reserve 64 logical pixels for a visible System button; wider
desktops retain the existing 180-pixel clock area with network/USB/audio entries.
Production taskbar arithmetic reserves this area before calculating app overflow.
Supported logical desktops start at 800x600; smaller modes refuse the panel with
a reason rather than registering unreachable controls.

Network labels derive from `net7_current`: no interface, disconnected,
configuring, connected or failed. Connected means local DHCP configuration,
not proof of Internet access. Retry operates only on a disconnected/failed
provider. Devices opens required Settings and its real hardware inventory.
Wi-Fi, Bluetooth and battery controls remain explicitly unavailable.

Audio labels derive from actual playback state. Quieter/Louder/Mute call the
existing software PCM gain provider; they are not universal hardware master
volume controls. Hardware output is still checked when playback starts. The
existing validated eight-byte audio preference format is retained. A file
transfer, active file review/picker or Windows job allows a session-level gain
change but prevents competing preference writes; the panel explains how to
save after the operation. Optional Media Player removal does not remove this
base provider or falsely report hardware readiness.

USB lists only readable registered USB transports, never the installation
disk. Four rows per page bound the sixteen-device inventory. Open uses the
common Files environment. Safe remove uses `usb10_eject` and reports success
only after its checked flush/removal result. Active transfers refuse removal.
Every row's control owner includes its full provider context and disk index;
the pointer broker compares it across press/release, and dispatch revalidates
it. Detach/replacement cannot silently retarget an earlier click. Successful
ejection invalidates other USB Files windows and preserves their navigation.
Opening or refreshing never formats or erases storage.

The calendar uses the real UTC clock and existing Gregorian calendar helpers.
Month navigation is bounded to 2000–2099. Selecting a day previews it; opening
the optional Calendar is explicit. Removing Calendar or Clock does not remove
the base date/time display. No timezone database, DST, NTP or missing clock
value is invented by this flyout.

Windows+A uses both supported USB and PS/2 shortcut paths. Tab/arrows choose
registered enabled controls, Enter activates, Escape/Alt+F4 closes only the
flyout, and Alt+Tab/Start dismiss it before normal shell handling. Opening
cancels captured drag/scroll gestures while preserving unsaved work and file
dialog ownership. Clicking outside dismisses without activating a hidden app.

## Updates and bounds

Only existing network/audio revisions, USB events and clock-minute changes
invalidate the tray/panel. There is no idle scanner, per-second animation or
new polling task. Flyout state is bounded to a small fixed record and shared
controls; actual compiled fixed bytes, peak and retained pages are measured
separately. Configured VM RAM is not measured OS consumption.

## Verification contract and retained scope

Freeze matching media through native install, ordinary disk starts, actual
provider status/controls, independent preference bytes, late USB open/eject/
detach/replacement and keyboard/owner checks. Test compact light/dark, actual
150% and physical 3840x2160, exact enabled-device VMware, separate BIOS,
movement equivalence and actual boot repair. Host bounds tests do not replace
these native tasks. Agent review is not a human usability study.

M12.14 retains transfer/modal arbitration and feedback refinements; M12.16
retains cursor/scale/focus work; M12.17 retains measured renderer work; M12.18
retains the earlier BIOS/AHCI observation and full controller/original-app
matrix. No universal hardware, physical/ARM, GPU 3D or general Windows support
is qualified by drawing tray controls.

## Measured receipt

11 native task/profile checks, four real display profiles, separate BIOS and exact enabled-device VMware pass. Fixed shell state is 553,196 bytes (+239); completed UI journeys retain zero pages. [Acceptance](../../evidence/M12/12/acceptance-results.json).
