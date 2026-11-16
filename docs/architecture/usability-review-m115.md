# M11.5 installation and first-desktop scenario review

Reviewed 16 November 2026 against actual ordinary 1280×800, 1920×1200 at 150%,
3840×2160 at automatic 200%, and the exact VMware SATA/UEFI starter. This is an
agent scenario/visual review, not a study with inexperienced children or adults.
Final acceptance and public publication remain separately gated.

The review asks of every ordinary step and error: is the next action clear,
convenient, friendly, visually consistent and readable? Screenshots are native
framebuffer data or the owned VMware guest, never a browser mockup or enlarged
low-resolution capture. [Native screenshots and reports](../../evidence/M11/5/README.md).

| Surface | Review and concrete behavior |
|---|---|
| Welcome | One highlighted Next, brief three-part explanation, optional recovery. No commands or account service to configure. |
| Keyboard / size | Two actual layouts, a typing box and Clear; visibly selected choices. Unsuitable scaling gives a reason and preserves the old size. English/UTC limits are explicit. |
| Disk selection | Bordered list, whole-row target, controller label/capacity and a visible selected state. Next stays unavailable before an eligible choice. |
| Existing contents | Ordinary installation does not silently erase. The disk-level erase choice is separate from final Review consent. Back clears consent. |
| Disk tools | Existing partition/free-space rows, explicit format/create/delete review and independent consent. Cancelling leaves bytes unchanged; unrelated data has independent hash checks. |
| Your apps | All, Essentials and No optional apps have real effects. Individual choices use bounded pages; Files/Settings/desktop remain base. |
| Your style | Owner is selected for replacement; correction uses normal selection/cursor keys. Accent, Light/Dark and labelled wallpaper choices map to saved desktop preferences. |
| Review | Named disk/controller, capacity, account, layout, app count, full appearance, scale and first-start choice. Install is the clear primary action; no writes before consent. |
| Installing | Real copying/readback stages and percentages. No decorative progress timer or fake cancellation after destructive work begins. |
| Ready | A single primary Restart to Engacer OS route. The normal UI no longer offers an immediate live-session desktop as an alternative completion shortcut. |
| First installed desktop | A short optional card offers actual Files, Start and Appearance actions, plus Go to my desktop/Escape. No second mandatory setup and no dependency on Help or Editor. |
| Missing/small disk | Clear explanation and disabled Next rather than an unusable installation offer. The release manual identifies supported capacity, sector and controller requirements. |
| Failed write | No success claim or activation. Back retains personal choices and clears consent. A quarantined controller remains blocked; the manual explicitly explains fixing the fault and restarting with the same disk/ISO. |
| Recovery | Matching UEFI media gives a visible two-second Escape opportunity. Recovery Review says existing personal settings/files stay rather than presenting unsaved installer choices as changes. |
| Minimal desktop | No optional executables are needed to open Files/Settings/Start. Calculator can be installed offline, run, reviewed for removal, removed, and Files still creates a persistent folder. |

The persistent frame and original Inter typography remain consistent across
ordinary Next/Back transitions. Setup uses sixteen-pixel body text, measured
controls, deliberate spacing and visible keyboard focus. Active controls are
bounded inside the wizard and at least 36 pixels high/wide. Display scaling
rasterizes the existing font at actual physical sizes rather than enlarging a
bitmap font. An actual size change legitimately recalculates the frame.

Every tested display profile includes an installed reset and two disk-only boots
with retained firmware variables. The guide dismissal and preferences are read
independently from checked on-disk metadata/payloads. Idle checks observe halted
CPUs and unchanged paints after startup work settles. The new fixed desktop
state is sixteen bytes above M11.4; the offline Calculator lifecycle retains no
managed pages. Shared framebuffer/font/kernel memory is separate from this delta.

Remaining boundaries include English/US layouts, UTC, ASCII account/path limits,
whole-disk OS installation, eight desktop windows and supported virtual hardware.
Selected-partition OS installation, resize/dual boot, physical hardware, vendor
GPU 3D and general Windows app compatibility are not established by this review.
The full new-artifact controller/device/original-app regression remains M11.6.
