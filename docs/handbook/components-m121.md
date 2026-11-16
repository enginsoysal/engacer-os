# Use the M12.1 desktop controls

M12.1 refreshes the shared native controls. App icons and the larger Files/Start/
taskbar redesign follow in later M12 stages. Use the matching release and
[installation guide](install-m121.md).

- Click a button once. If you press it and release outside it, the click is
  cancelled. A muted button is unavailable; select a file before Copy or Cut.
- Use Tab and Shift+Tab to move keyboard focus, then Enter to activate. The
  outline shows focus; selecting a file does not open it.
- Text fields show a caret and selected text. Their input stays with the field.
- In a long native Files list, drag the scrollbar thumb, use the wheel or click
  above/below the thumb to page. Escape or Ctrl+Escape during a thumb drag restores
  the starting position. With the scrollbar focused, arrows scroll and Home/End
  jump to the beginning/end. USB and address fields keep their own keyboard input.
- Search Start for **Settings** to preview Light/Dark and display size. Choose
  **Save preferences** to retain changes. Unsupported sizes preserve the usable
  setting. A 4K screen can use Auto or 200%; suitable larger screens also support
  150%. The control layout and font masks use the actual selected scale.

The included Documents/Welcome.txt matches this distribution. Optional apps
remain independently removable through Software Manager. The desktop and base
Settings do not depend on Calculator. Existing file operations, erasure reviews
and USB capability limits remain in force.

[Implementation and decisions](../architecture/components-m121.md) explain the
resource and test scope. Named VM qualification is separate from physical
hardware, vendor GPU 3D and general Windows compatibility.
