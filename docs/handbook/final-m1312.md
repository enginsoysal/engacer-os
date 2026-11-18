# Your first day with Engacer OS M13.12

Status: final integration candidate, qualification pending. Use the matching release only after publication. Stability remains unqualified until M13.13; this is controlled testing, not an everyday system recommendation.

## Start with the prepared VMware package

Extract the whole ZIP, open EngacerOS.vmx and start it. Keep its included disk and devices. Follow the [eight-step installation guide](install-m1312.md). The disk list is a bordered list: click the intended row, review its capacity, and continue. Disk tools are optional; whole-disk replacement requires its own erasure confirmation. Ready means verification finished. Choose **Restart to Engacer OS** and keep the installed hard disk attached. The ISO may remain connected.

## Find your way around

Dismiss the first-start guide with Escape. Click an object once to select it; double-click or press Enter to open it. Right-click for available actions. Buttons need one click. Start finds installed apps and pinned folders. Its Pinned, All apps and Categories views are separate. The taskbar switches windows; a group badge lets you choose among multiple windows of an app.

Files provides Back, Forward, Up, Refresh and Address. Small windows use Places for the same folder destinations. Open Documents, Downloads or USB drives; Back returns to where you came from. Ctrl+F filters names in the current native folder, not all subfolders; USB filtering is unavailable. Clear the filter to see every item again. [Detailed Files guide](files-m137.md).

## Keep your work

Text Editor opens and saves supported native text files. **Save as** lets you choose a folder and name; replacement needs a review. Cancel preserves your work. Closing a dirty document asks first. Copy, Cut, Paste and transfers show actual supported operations and conflicts. Completed files stay when a transfer is cancelled. USB supports the documented FAT32, create-only one-file operations; use Eject before disconnecting. [File dialogs](dialogs-m1310.md), [transfers and conflicts](transfers-m137.md).

## Make it yours

Settings has Appearance, Display, Input, System and Accessibility. Input contains mouse and keyboard choices. Type in **Find a setting**, or press Ctrl+F. Results describe implemented categories; searching itself changes nothing. Appearance/Display preview choices. **Apply and save** keeps them; Cancel preview, Escape or closing the owner restores the previous choices. Input and accessibility save separately. System leads to Devices, optional Applications, Start/taskbar and Quick settings.

Appearance > Screensaver offers Off/On, one/five/ten minutes, Engacer logo, Clock and Blank. Preview never saves. **Apply and save** keeps choices; **Cancel changes** or leaving restores saved choices. Move the mouse or press a key to return; that wake gesture is consumed so it cannot activate something underneath. Reduced motion keeps the logo still. This is neither a password lock nor display power management. Clock saver does not depend on the optional Clock app. [Full personalization instructions](personalization-m1311.md).

## Change apps without breaking the desktop

System > Applications lists independently removable optional apps. Removing Calculator does not remove Files or Settings. Some standard frontends intentionally explain unsupported capabilities. The supported Windows profile remains the original pinned 7-Zip console MSI/executable lifecycle; general Windows GUI, Steam/DirectX and arbitrary MSI packages are not supported. Hardware support remains the explicitly named virtual controller/device profiles.

## Keyboard essentials

Tab / Shift+Tab move focus; Enter activates a focused control. Escape dismisses menus or cancels a supported preview. Alt+Tab switches windows. Alt+F4 closes the active window, retaining dirty-document confirmation. F6 changes panes and F1 explains the focused control. High contrast and Reduced motion are in Accessibility. The installed Welcome guide remains available offline.

## If something goes wrong

Read the message before changing a disk. A failed install is not successful completion. Keep the ISO for same-build recovery. Record the release, action and visible message; historical M13.7/M13.8 freezes remain open for M13.13. Do not assume the screensaver establishes stability. Automated novice scenarios and visual checks do not substitute for a participant usability study.

[Current status](../roadmap/status.md) | [M13.12 contract](../milestones/m13-12.md) | [Exact release scope](../releases/m1312-v0.13.12.md)
