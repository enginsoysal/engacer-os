# M14.1 loader design and qualification

Status: native M14-STAGE1-VM-v1 qualification passes. The matching GitHub release is published; actual website verification remains the final closing gate.

## Mapping and resource ownership

The original AMD64 PE32+ file is read section by section into a private user address space. It is not copied wholesale into a second heap buffer. Each file and image has a 32-MiB bound; the module table has 32 reusable slots. First-fit 64-KiB-aligned image reservations replace fixed 16-MiB slots, which would overlap larger originals. Each module retains an unmapped guard range.

Image reservations use non-present software-marked page-table entries. Physical zeroed pages are committed only when the loader copies real file bytes, checked kernel copies access a page, or the process touches a permitted reserved page. Read-only and non-executable reservations retain their permissions before their first physical commit. Guard pages are never eligible for demand commitment. The virtual budget is 128 MiB and the physical ownership table remains bounded at 10,000 pages, including page tables and process allocations. Exhaustion stops the task; it never grants access to unrelated physical memory.

After relocations and import binding, headers and image gaps become read-only and non-executable. Individual sections receive their final read/write/execute permissions. Writable executable sections are refused. A process fault or cancellation releases its data pages, reservations and owned page tables. The existing four-page kernel transition stack is initialized once and shared sequentially between workers; it is fixed runtime infrastructure, not per-task retention.

## Dependencies and module lifetime

Direct imports resolve against the existing independently implemented API providers or explicit application-local DLLs. Search is bounded to the importing module's directory and the main executable's directory. Current-directory or arbitrary system-directory search is not added. Case-insensitive application filenames are found by the bounded native directory enumerator. Conflicting explicit paths for an already loaded module name are refused.

Exports support names, ordinals and bounded forwarded exports. A forwarder chain deeper than 32 is refused. Module dependencies are tracked as a 32-bit graph. External library references are tracked separately. Freeing an external reference preserves modules reachable from the main image or another external reference and releases unreachable dependency groups, including cycles. DLL attachment follows completed import mapping; detach runs in reverse recorded attachment order before unmapping.

RVA delay-import descriptors and their arrays are validated while original delay thunks remain intact. The application's delay helper must use LoadLibrary/GetProcAddress when it actually needs the module. Optional delayed modules are not loaded eagerly. This does not claim every compiler's delay-unload hook is supported. Static TLS execution remains M14.2; inspection does not execute TLS callbacks or DLL entry points.

## User-facing file checks

Windows Apps offers a shared file picker for checking an original EXE or DLL. The protected worker maps and relocates it and inspects direct and delayed imports without binding or executing foreign code. The result explicitly says that the app was not installed or started. A matching mapped-byte fingerprint is test evidence of the original headers and section bytes; it is not a digital signature or a security endorsement. Original test packages have separate SHA-256 provenance.

## Browser download choice

The basic static-page reader exposes Browser choices. Firefox is the first target; Chrome, Brave and Microsoft Edge remain candidates. The optional download points directly to Mozilla's original Windows x64 English MSI. It does not run automatically, change the default browser or imply that Firefox can execute. Actual modern-browser execution needs later process/thread, graphical, network and installation compatibility.

The pinned choice is Firefox 160.0.1, 95,924,224 bytes, SHA-256 `6dc28633cbd77cb1d044f339185cd467dda39397e4bcca942bfb0ddb2360c681`. These were read from Mozilla's release server on 19 November 2026. M14 permits a maximum 128-MiB streamed download instead of 64 MiB; the transfer still uses bounded chunks and create-only publication. Static browser pages retain their separate 128-KiB source limit. Other existing archive/USB/file-copy limits are unchanged.

Sources: [Mozilla release metadata](https://product-details.mozilla.org/1.0/firefox_versions.json), [Mozilla SHA-256 list](https://archive.mozilla.org/pub/firefox/releases/160.0.1/SHA256SUMS), [full offline installer guidance](https://support.mozilla.org/en-US/kb/custom-installation-firefox-on-windows).

## Qualification and remaining publication gates

The exact candidate passes original-image inspection, original 7-Zip lifecycle, real DLL forwarding/delay/reference/reuse fixtures, actual protection faults, repeated retention checks, native Firefox download/cancellation and independent stored hashes. Ordinary/compact/physical-4K installation and independent starts pass; the exact VMware package is also qualified. See [acceptance](../../evidence/M14/1/acceptance-results.json), [resources](../../evidence/M14/1/resources.json) and the [stage record](../milestones/m14-1.md). GitHub release and actual complete website publication remain separate closing gates. Normal process-detach callbacks and static TLS remain M14.2; this stage does not provide general Windows GUI, reusable MSI or Firefox execution.
