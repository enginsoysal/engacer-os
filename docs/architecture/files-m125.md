# M12.5 one Files environment

Status: implementation and qualification in progress. M12.4 remains the current
qualified download. Host checks and compilation do not qualify a new ISO.

## One frame, different capabilities

Native folders, the USB drive collection, USB folders and disconnected/empty
locations use one frame: title, Back, Forward, Up, Refresh, address, Places,
toolbar and status. Native contents retain their checked filesystem operations.
USB retains its actual FAT32 browsing and one-file create-only copy support.
Unsupported view/sort/edit commands stay unavailable; a shared frame does not
invent provider capabilities. Provider metadata comes from real directory and
storage records, without invented dates or capacity values.

The sidebar is shown only when width and height fit all eight places. Smaller
windows retain a Places button in the toolbar. All four navigation controls stay
visible. The footer labels Prev page and Next page distinguish item pagination
from location history. Empty and unavailable locations retain navigation rather
than replacing the entire window. Empty-state layout adapts to short content
regions, including a real active transfer's progress strip. One shared row-count
function governs USB drawing, paging and keyboard selection.

## Bounded history and device identity

The existing eight slots per window now record provider, path, scroll offset,
disk, partition and the USB driver's generation-backed context lease. Reusing
that history adds 160 bytes per window, 1,280 bytes across eight window slots;
there is no second history, directory cache or heap allocation. Back/Forward
restore the actual prior location; a new visit replaces the forward branch.
Repeated visits to the same location update their offset rather than adding
duplicates. The oldest location leaves the bounded history when it fills.

History never obtains a fresh USB lease behind the user's back. An old location
remains unavailable after removal or replacement, with Back and Home still
working. Refresh checks that location. Choosing a drive in USB drives or entering
an explicit new USB address is the separate user action that binds its current
lease. Native missing folders similarly retain their location and explanation,
with creation unavailable. USB drive objects select once and open on double-click
or Enter; selected drive contexts and click identities include generation.
Ctrl+N copies the current provider location into a new independent window, not
the old hidden native folder. Each new window starts its own bounded history.

## Address safety and input ownership

Ordinary browsing needs no syntax. Optional editing accepts native paths, named
places and explicit locations such as `USB:2:/Games`. A relative USB folder stays
on the current lease. Invalid input preserves the prior location and leaves the
editor available for correction. The address buffer is 272 bytes so the original
255-byte provider path plus its USB prefix fits without silent truncation. This
adds 16 bytes per window; it does not expand either filesystem's path limits.

The shared text editor receives the actual buffer capacity. Native addresses
still reject paths beyond 255 bytes; USB validates the complete path before
copying it into a location record. Field measurement has sufficient bounded
scratch space for the prefix too. Selection, old scrollbar capture and keyboard
focus are reset on provider changes. Caption names describe the actual provider
rather than continuing to say Documents while USB is open.

## Verification and limits

Host checks exercise location/generation isolation, branching, offsets, 10,000
bounded transitions and short-window row geometry. Native qualification must
separately install and start matching media, traverse Documents/USB/folders and
Back/Forward/Home, test no-device/detach/replacement/refresh, address limits,
multiple window ownership, real 150%/4K rendering, idle and retained resources.
Exact VMware, BIOS and cached/full rendering checks remain separate gates before
release and complete website verification. No M12.5 native acceptance is claimed
by this development document.

Presentation/sort expansion remains M12.6; broader transfers M12.7; shared Open
and Save dialogs M12.8. The M12.4 shared-menu footer and HiDPI cursor observations
remain explicit M12.14/M12.16 follow-ups. Final controller/application regression
and the retained BIOS/AHCI observation remain M12.18.
