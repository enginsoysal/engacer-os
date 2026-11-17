# System tray and quick settings — M12.12

Development guide: native M12.12 tests and downloads are pending. The completed
tested release remains [M12.11](install-m1211.md).

Open **System** at the right of the taskbar, or press **Windows+A**. On a wider
desktop, the network and sound icons open Quick settings, the USB icon opens
USB drives, and the date/time opens Calendar. The clock is shown in **UTC**.
Choose one of the three tabs. Tab/arrows choose a control; Enter activates it.
Escape, Close or a click outside closes the panel without closing your apps.

## Quick settings

- Network shows its actual local connection state. An IPv4 address does not
  guarantee Internet access. Retry is available when a supported connection
  failed/disconnected. Devices opens the real hardware inventory in Settings.
- Quieter, Louder and Mute control supported **software PCM playback**. They
  do not claim universal sound-card output or a hardware master mixer. Media
  Player shows playback/device failures. A level normally saves for restart.
- During a file operation or active file dialog, the level changes for this
  session and the panel explains that it has not saved. Finish/cancel that
  operation, then change the level again to save it.
- Settings opens the required base Settings app. Wi-Fi, Bluetooth and battery
  controls are unavailable because their providers are not implemented.

## USB drives

Connect a supported USB storage device. The list updates from real device
events; Refresh refreshes the known inventory. **Open** opens Files with the
same Back/Forward/Up/navigation controls as your native folders. Unsupported
formats remain a provider limitation; opening never formats or erases a disk.

Choose **Safe remove**, wait for **Safe to unplug**, then unplug. A failed
flush, disconnect or active transfer is not reported as a successful removal.
Finish/cancel transfers first. Reconnect an ejected drive to use it again.
The panel checks the particular connected device; it does not reuse a stale
selection after replacement. Other USB folder windows show the changed state.

## Calendar

The calendar uses the real UTC clock. Previous/Next browse 2000–2099; Today
returns to the real date. Clicking a day selects it. **Open Calendar** explicitly
opens the optional Calendar app for that date. If an optional app is removed,
the panel explains that it is not installed; reinstall it through Settings.
Removing Clock, Calendar or Media Player does not remove the base tray.

These controls do not add hardware drivers or broaden the documented device,
filesystem, GPU or Windows compatibility limits.
