# Stability, saved work and useful diagnostics

**M13.13 is complete within the owner-revised ninety-minute observation scope.** The actual candidate observation reached 108.78 minutes. The original eight-hour/two-hour idle gate was stopped at explicit owner direction and did not pass. Do not use testing media as the only copy of important work.

## Keep your work

In Text Editor, use **Save** or **Ctrl+S**. An unsaved edit remains part of the open window until you save it; a VM reset cannot promise to recover unsaved work. During qualification, the test deliberately keeps a saved document and an unsaved suffix open during observed tasks, checks both independently, then explicitly saves and reopens the exact bytes after two ordinary disk-only starts.

The screensaver is optional and starts **Off**. Open **Start > Settings > Appearance > Screensaver** to choose a supported timeout and style, use **Preview**, then **Apply** to keep your choices or **Cancel changes** to restore them. Keyboard or mouse input wakes the screen; that first gesture is consumed so it cannot accidentally operate the covered desktop. A screensaver does not save a document, authenticate a user, repair a freeze or switch off the display.

## If the display stops responding

Allow an installation write to finish while its progress is advancing. If the clock, pointer and controls all stop changing, record the release/build, displayed step or open app, approximate elapsed time, and whether the problem follows a reset or a complete power-off/start. A paused VM, disconnected input and a frozen guest are different observations; do not assume which occurred without evidence.

Before a reset, retain any existing screenshot and available test logs. Resetting loses unsaved state and can remove useful evidence. The project does not require you to reboot your host laptop or change its system settings. Report whether you used the matching prepared VMware package or a custom VM, its RAM, firmware and disk controller, and which operation immediately preceded the failure. Never include VM memory dumps, credentials or private documents in a public issue.

## What the qualification actually measures

The owner accepted ninety minutes instead of the earlier eight-hour requirement. The frozen enabled-device VMware candidate reached 108.78 observed minutes with no injected input during its idle observation. Separate fresh tasks complete real file, window, search, Settings, app and saved-data/startup checks. The observer checks visible presentation as well as native events, retained dirty text, explicit saved bytes, bounded peak memory, no unexplained retained memory or new allocation refusals, and two independent ordinary starts without the ISO. Unexpected hangs, restarts, data loss or unexplained observation gaps block the corresponding qualification claim.

Separate checks cover constrained-memory and physical 4K native tasks, screensaver preferences and wake behavior, and a clearly labelled simulated display-timeout recovery followed by three warm resets. The original eight-hour and two-hour idle gates did not complete; no short check is presented as their replacement or pass. A simulated timeout does not prove the cause of the historical M13.7/M13.8 natural freezes. Successful revised-scope checks qualify that candidate and scenario, not every device, every VM configuration or unlimited uptime.

The [M13.13 milestone](../milestones/m13-13.md) records the acceptance contract and current state. The [current installation guide](install-m1313.md) describes the matching M13.13 media; use it after that exact release is published.
