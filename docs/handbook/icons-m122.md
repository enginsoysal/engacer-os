# Recognize apps and files in M12.2

M12.2 gives the native shell original icons instead of app-initial badges. Use
the [matching release](../releases/m122-v0.12.2.md) and
[installation guide](install-m122.md). Native qualification is scoped; public
release and website proof are separate gates. Later M12 stages continue the
larger desktop and Files redesign.

- Open Start for your pinned apps, or choose **All apps**. Each app keeps its
  icon and name. The Calculator keypad, Terminal prompt, Clock face and Calendar
  grid make similar names easier to distinguish.
- The same identity appears on the taskbar and in the app's title bar. Narrow
  taskbar captions can still shorten; Start and the window title identify the app.
- Folders, text, BMP images, WAV audio, ZIP archives, MSI packages and executables
  have distinct file symbols. A shortcut has an arrow overlay. A generic file
  icon means its type has no specific shell artwork; it does not damage the file.
- One click still selects a desktop/file item. Double-click or Enter opens it.
  Start entries and ordinary buttons activate with one click. The icons do not
  change file permissions or destructive-operation confirmations.
- Switch Light/Dark or display size in Settings and save your preference to keep
  it. Icons render at the actual selected density, including 150% and 200%.
- In Devices, read the capability text beside the icon. Detected hardware is
  not automatically fully supported. Unsupported GPU 3D and arbitrary Windows
  applications do not become supported because an icon is present.

Optional app packages remain separate from the shell. The icon library does not
load Calculator or another optional app just to draw its identity.
[Implementation and resource decisions](../architecture/icons-m122.md).
