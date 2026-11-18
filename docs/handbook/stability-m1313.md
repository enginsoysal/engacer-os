# Stability, saved work and useful diagnostics

**M13.13 qualification is in progress. M13.12 remains the current testing download.** The eight-hour candidate run has started but has not passed yet. Do not use testing media as the only copy of important work.

## Keep your work

In Text Editor, use **Save** or **Ctrl+S**. An unsaved edit remains part of the open window until you save it; a VM reset cannot promise to recover unsaved work. During qualification, the test deliberately keeps a saved document and an unsaved suffix open for the full session, checks both independently, then explicitly saves and reopens the exact bytes after two ordinary disk-only starts.

The screensaver is optional and starts **Off**. Open **Start > Settings > Appearance > Screensaver** to choose a supported timeout and style, use **Preview**, then **Apply** to keep your choices or **Cancel changes** to restore them. Keyboard or mouse input wakes the screen; that first gesture is consumed so it cannot accidentally operate the covered desktop. A screensaver does not save a document, authenticate a user, repair a freeze or switch off the display.

## If the display stops responding

Allow an installation write to finish while its progress is advancing. If the clock, pointer and controls all stop changing, record the release/build, displayed step or open app, approximate elapsed time, and whether the problem follows a reset or a complete power-off/start. A paused VM, disconnected input and a frozen guest are different observations; do not assume which occurred without evidence.

Before a reset, retain any existing screenshot and available test logs. Resetting loses unsaved state and can remove useful evidence. The project does not require you to reboot your host laptop or change its system settings. Report whether you used the matching prepared VMware package or a custom VM, its RAM, firmware and disk controller, and which operation immediately preceded the failure. Never include VM memory dumps, credentials or private documents in a public issue.

## What the qualification actually measures

The frozen enabled-device VMware candidate must complete eight actual hours, starting with two uninterrupted hours without injected input and continuing with repeated real file, window, search, Settings and app tasks. The observer checks visible presentation as well as native events, retained dirty text, explicit saved bytes, bounded peak memory, no unexplained retained memory or new allocation refusals, and two independent ordinary starts without the ISO. Unexpected hangs, restarts, data loss or observation gaps above the declared limit block release.

Separate checks cover constrained-memory and physical 4K native tasks, screensaver preferences and wake behavior, and a clearly labelled simulated display-timeout recovery followed by three warm resets. Short feature checks do not replace eight elapsed hours. A simulated timeout does not prove the cause of the historical M13.7/M13.8 natural freezes. A successful named-VM workday would qualify that candidate and scenario, not every device, every VM configuration or unlimited uptime.

The [M13.13 milestone](../milestones/m13-13.md) records the acceptance contract and current state. The [current installation guide](install-m1312.md) remains the guide for the available M13.12 download until the new candidate passes and its exact media are published.
