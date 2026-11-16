# M12.2 — original scalable shell icons

Native qualification passes M12-STAGE2-VM-v1 on build
`704df6a9802e5ba98e2062fec7922f57`.
[Acceptance](../../evidence/M12/2/acceptance-results.json) records 573 verified
compiled inputs, 114 app and twelve file/USB comparisons, plus twelve cached/full
comparisons. The host geometry check is separate from native execution; public
downloads and website closure remain independent required gates.

## Artwork and identities

The [catalog](figures/m12-icons/catalog.json) contains 57 original MIT geometric
icons, including all nineteen stable application identities, folders, supported
file types, shortcut overlay, devices and common actions. The artwork is defined
once in `tools/design/icons12.py`, which emits both native geometry and review
SVGs. No Windows artwork, external icon pack or icon font is included.

Examples: [Calculator](figures/m12-icons/calculator.svg),
[Text Editor](figures/m12-icons/editor.svg), [USB](figures/m12-icons/usb.svg),
[folder](figures/m12-icons/folder.svg), [copy](figures/m12-icons/copy.svg).
Color supports identification; silhouettes and retained text labels supply meaning.
Light and dark palettes keep foreground shapes visible on their own tiles.
Custom accent changes do not replace the icon set or erase app identities.

Start uses the real application or pinned-folder identity. Taskbar pins, running
windows and title bars share application IDs. Files details/icon views, desktop
items and USB file rows use the same folder/file classifications. Native
application directories match the installed package's stable name. Unknown file
types use a generic fallback; a shortcut keeps a visible overlay. Drawing an icon
does not execute or read an untrusted file. It does not imply that an unsupported
file format has gained a decoder or application handler.

Device icons identify a category. Ready/Limited/Unavailable text remains the
authority for verified capability. A GPU icon does not imply 3D acceleration,
nor does a network icon mean its link is configured. The larger Files/USB frame,
desktop shortcuts and taskbar layouts remain their later ordered stages.

## Physical rendering and resource choice

`icons12.h` supplies bounded integer shape coverage and premultiplied row
composition. Rounded geometry and capped strokes are sampled at the actual
physical density, rather than enlarging a fixed bitmap. The compositor clips
against the real screen and active window using signed coordinates; partially
off-screen windows retain safe bounds.

The renderer uses one **512-byte temporary row**, up to 128 physical pixels
for a 64-logical-pixel icon at 200%. Its raster cache is **zero bytes**. Shared
read-only geometry avoids a large atlas, runtime font parser, per-window image
buffers and allocation on hover. This also avoids expanding the fixed low-memory
UEFI kernel allocation with a large static raster cache. Existing dirty-region
and cached-window movement rules remain in force. Idle adds no animation or
polling. Fixed code/data, transient row state, managed pages and framebuffers
are reported separately.

The linked installed map contains one copy of the geometry (2,191 bytes), offsets
(116) and palettes (136), totaling **2,443 bytes**. Icon telemetry has 28 bytes of
fields in a 32-byte aligned storage span. Fixed desktop BSS/data remains 544,164
bytes, unchanged from M12.1; fonts remain 251,248 coverage bytes. Native Start
previews retain no pages, and measured current/peak pages remain at the existing
ordinary/150%/4K costs. [Resources](../../evidence/M12/2/resources.json).

The generator's review SVGs and host contact sheets are artwork/host evidence,
not VM captures. The host checks compare production shape containment with an
independent floating-point closest-point reference, exercise all icons at
fourteen physical extents in both themes, check premultiplied channels and row
guards, and require distinct identities for all nineteen apps and safe fallback.
The first binary export observer used Windows text stdout; binary mode fixes
that observer's byte translation, without changing the kernel renderer.

Standalone colored strokes use separate adaptive blue/violet/orange inks.
Saturated app tiles retain their own fills and contrasting white internal
symbols. An initial candidate used tile colors directly for standalone marks
on dark paper, measuring 2.55–2.88 contrast, below the 3:1 graphical requirement.
The corrected palette lightens those standalone inks without washing out app
tiles. Host tests now enforce both standalone graphic contrast and white-on-tile
contrast, alongside native pixel verification of the rebuilt media.

## Native verification and retained limits

The candidate must install and reboot with its ISO retained, then start twice
with only its disk using the same firmware variables. Actual Start icon crops
are compared with production raster rows across ordinary, 150% and real 4K
light/dark profiles. Previewing icons must not launch app processes or retain
managed pages. Files/provider focus, real scrolling, signed clipping and idle
must still work. The exact enabled-device VMware starter and BIOS are separate
journeys. Failed observations are retained with the final results; no historical
M11/M12.1 test pass qualifies the new bytes automatically.

The completed host run covers 1,322,425 independent geometry samples and 1,596
icon/theme/extent cases. All 114 native app and twelve file/USB comparisons have
zero channel difference. Text, BMP, WAV, ZIP, MSI and actual unknown-file routing
are checked without executing a file; independent file CRCs remain valid. The
feature image is from the actual owned QEMU SATA/UEFI installed guest. Host
contact sheets are labeled separately.

An earlier M12.2 candidate (`93d8dc6597cbc948062274e4fb29eeff`) had an initial
concurrent BIOS installation reach the pre-existing AHCI timeout and fail.
A fresh repeat of that candidate passed its complete journey. The corrected
palette candidate has separate matching installation and disk-boot evidence.
The trigger has not been isolated; preserve the
failed report and revisit load sensitivity in final qualification. A successful
repeat is not a storage-driver fix or a stress-reliability claim. Test-observer
preconditions were also corrected: open Settings before a helper that closes it,
and include the real bundled MSI alongside ZIP in Downloads. These corrections
do not alter the kernel or hide the failed observer reports.
