# M11.6 qualification design

M11.6 qualifies one frozen final artifact, rather than combining passes from
different stage builds. [Matching native acceptance](../../evidence/M11/6/acceptance-results.json)
passes 36 report groups, including 14 enabled-device VMware controller/starter
profiles, on 562 compiled inputs and the exact final ISO/ZIP. Public release and
website verification are separate delivery gates. Accepted M11.1–M11.5 artifacts
remain unchanged.

## What must be exercised

| Area | Required evidence | Reason |
|---|---|---|
| Setup | Eight steps, saved choices, partition tools, explicit destructive consent, error quarantine, retry and boot repair | A final screen alone cannot establish safe installation |
| Installed startup | Real reset with matching ISO retained, then two independent boots with it disconnected | Firmware must discover the installation without a harness forcing disk priority |
| Files | Selection, context menus, clipboard, streamed copy/move, rename, recycling, restore, conflicts, protection, associations and preferences | Visible rows must refer to actual durable entries |
| Shell | Search, categories, app/folder/taskbar pins, removal, window admission and power review | Customization must not leave stale launch paths or lose work |
| Windows | Move/resize, snap, switcher, keyboard parity, saved appearance and actual 4K framebuffer | Screenshots and framebuffer copies cannot substitute for working input |
| Controllers | SATA, IDE, LSI Logic, SAS1068, PVSCSI and NVMe with BIOS and UEFI; BusLogic with BIOS | Qualification belongs to each implemented controller/firmware combination |
| Devices | Keyboard reconnect, layouts, wheel, device inventory, removable-media round trip, refusal and quota cleanup | Discovery must lead to useful bounded behavior and honest capability reporting |
| Original application | Original 7-Zip MSI install, console execution, archive/extract, removal and reinstall | Native sample applications do not establish Windows compatibility |
| Resources | Retained pages, peak pages, fixed desktop state, idle paints and halted CPUs | Configured guest RAM is not kernel consumption |

The exact distributed VMware starter is tested separately with every shipped
device enabled. Tests use owned disposable guests and ordinary keyboard/mouse
input. Guest memory is read only for observation; host-side fixture corruption
is restricted to owned test images. Existing user VMs must remain untouched.

## Final regression corrections

The first final candidate exposed a genuine interaction ordering defect:
Ctrl+Escape during Ctrl-drag reached Start before the Files cancellation handler.
Cancellation now consumes Escape and Ctrl+Escape while a menu or interaction is
captured, before ordinary Start dispatch. Ctrl+Escape with no captured interaction
still opens Start. This retains the standard shortcut while preventing a dangling
drag. Both the genuine file cancellation task and the normal USB/PS2 Start routes
must pass on the replacement artifact.

Older stage harnesses are adapted to the eight-step setup and current sorted
Files listings. Selected bits identify volume entries, not row numbers. The
regression observes the actual native listing-to-entry mapping; it does not
weaken selection checks or restore old ordering merely to satisfy a test.
The VMware folder task uses the normal Ctrl+Shift+N action after navigation.
M11's creation dialog no longer emits the legacy M72 creation marker. QEMU
checks the actual stored directory; VMware navigates to the new directory through
the normal address field and subsequently inspects the stopped disk independently.
A missing obsolete marker is retained as a harness diagnostic, not described as
a failed storage operation or fixed by weakening durable-byte verification.

Failed candidate reports are diagnostic evidence, never acceptance for later
bytes. Any change to a compiled input requires rebuilding and repeating the
affected complete final qualification; artifacts must remain frozen while guests
are using them.

## Boundaries and storage

This is named virtual-machine qualification. Physical devices, ARM, vendor GPU
3D, arbitrary Wi-Fi/audio hardware and universal Windows application support
remain outside it. A known 64-MiB OVMF topology with boot-attached USB storage is
retained as an unqualified condition; a late USB connection is a separate test.

Large temporary build and guest files live in the local application-data build
directory through the guarded `build/m11` junction, outside OneDrive. Source,
canonical evidence and accepted media are preserved. Publication must verify
source bytes, complete release asset hashes, English manuals and the fresh
public homepage/downloads before reporting completion.
