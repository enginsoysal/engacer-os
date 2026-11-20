# M14.4 resource and image prerequisites

Development implementation, not accepted original GUI compatibility. These prerequisites are required by the pinned original 7-Zip startup; broader drawing/control qualification still belongs to M14.5.

## Checked module resources

The runtime traverses three bounded PE resource-directory levels and checks every table, UTF-16 name, data entry and image range before exposing bytes. FindResourceW/ExW, LoadResource, LockResource, SizeofResource and LoadStringW refer to the immutable existing image mapping. Counted strings can be copied with termination or viewed without another allocation. Numeric identifiers and their #decimal representation are supported. The selected default is English-US, then neutral/first available; exact-language requests refuse absent languages. Full MUI/locale fallback is not claimed.

Resource capabilities carry a generation independent of DLL attachment order. FreeLibrary removes descriptors before unmapping a module; reusing its image address does not revive old handles. Resource-only DLLs and descriptor reuse are bounded to 256 live descriptors. Normal process teardown, faults and cancellation retain kernel ownership as the final cleanup boundary.

## Original image data

The DIB decoder supports bounded uncompressed 1/4/8/24/32-bit bitmap data, palettes, row padding/orientation and icon AND/alpha masks. Unsupported compression/format variants fail rather than return invented pixels. Icon groups select an original resource, and image lists copy pixels so the source icon/bitmap can be destroyed independently. Create/append/replace/masked-strip/count/destroy semantics retain bounded ownership and stale-handle refusal. Predefined/custom cursors, PNG-compressed icons and general GDI drawing are separate remaining work. Initial resize uses nearest-neighbour sampling; it is not final HiDPI quality qualification.

Image allocations are lazy and bounded to 16 MiB per process, 256 image objects and 512 images per list. This limit includes object and list-pointer storage as well as pixels. Console processes acquire none of this image storage. The process heap APIs use the existing bounded native allocator, with zero initialization, exact allocation validation and an allocation-size query; no second allocator is introduced.

## Honest unsupported calls

Known static imports needed to investigate original startup can resolve to explicit fail-at-call diagnostics. Those functions terminate the protected task with their exact DLL/symbol name. They are not implemented API behavior and do not count as compatibility. Optional GetProcAddress discovery returns null for these diagnostic-only entries so the application's own fallback remains possible. Unknown imports remain refused. Data exports such as _acmdln point to actual process storage and are never function guards. The native fixture verifies implemented-versus-unsupported dynamic discovery.

## Development verification

The independent host resource walk checks all 88 resources/688 string slots in original 7-Zip, 2,487 resources in Notepad++ and 46 in SumatraPDF, plus 20,000 malformed-table mutations. A separate decoder comparison matches all 19 original 7-Zip bitmap/icon resources against Pillow and checks 10,000 malformed bitmap inputs. These host tests do not execute original apps.

The native owned PE fixture passes 21 process lifetimes with 25 real resource-DLL loads/unloads each: 525 cycles. It checks generation invalidation, exact/missing languages, string copying/truncation/zero-copy Unicode, actual icon/bitmap/image-list operations, stale objects, heap zeroing/size/interior-pointer refusal and dynamic API discovery. After the existing four-page first-use transition-stack warmup, subsequent complete process lifetimes retain zero managed pages. The original MSI/console lifecycle and 106 payload hashes also pass on that candidate.

The unmodified 7zFM.exe now executes its own code and reaches the common-control initialization call (ordinal 17). This is progress beyond the prior unresolved import, not a working original file-manager interface. M14.4 remains unaccepted.

References: [FindResourceW](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-findresourcew), [resource lifetime](https://learn.microsoft.com/en-us/windows/win32/menurc/finding-and-loading-resources), [icon groups](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-lookupiconidfromdirectoryex).
