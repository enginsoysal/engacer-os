# M14.4 resource and image prerequisites

Current qualification: exact-source M14.4 passes its bounded original-window/message and supporting resource/drawing profiles, with 47 native and eight supporting host groups. [Acceptance](../../evidence/M14/4/acceptance-results.json), [resources](../../evidence/M14/4/resources.json). Earlier diagnostic observations below are preserved as history. Full common-control/application task coverage remains M14.5 and later work.

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

## Menu resource development

The Windows runtime now parses standard and extended menu templates from the actual checked module resource bytes. The pinned original 7-Zip file manager uses MENUEX, including aligned items, nested popups and counted resource bounds. Parsing is limited to sixteen nested popup levels, 2,048 items and 256 process-owned menus. Truncated resource templates fail and release the partially built tree.

Menu objects copy labels and remain valid after the source DLL is unloaded. Opaque monotonic handles prevent stale-handle revival. Item insertion, retrieval, mutation, check/enable state and submenu association operate on the actual process-owned tree; cyclic associations are refused. Removing an item preserves its detached submenu, while destroying a menu destroys its associated subtree. Class menu resources load before the original WM_CREATE callback. Resource loading releases the class lock before taking loader/resource locks.

An owned native fixture checks both resource template versions, nested IDs, malformed input, copied resource lifetime, label truncation, recursive command lookup, item state, submenu detachment and stale handles. These observations use an explicitly identified new user runtime with a previously frozen owned kernel; they are diagnostic evidence, not stage/ISO acceptance. [Menu observations](../../evidence/M14/4/development/mixed-menu-controls/menu-resource-fixture.json).

Menu painting and interaction remain separate compositor work: DrawMenuBar explicitly reports unsupported behavior in this development implementation. No invisible menu is advertised as working graphical menu interaction.

## List and toolbar state development

The list model stores original application rows, images, callback markers, per-cell labels, selection states and up to 32 columns. It never substitutes native Files data for the original application's data. Rows allocate lazily with a 2,048-row initial implementation ceiling; unsupported owner-data callbacks and layout/drawing operations remain explicit limitations. Toolbar buttons copy temporary original labels, preserve command/state/data values and reference actual image lists. The initial toolbar ceiling is 64 buttons. Recursive control teardown frees copied labels and row storage.

The owned control fixture checks copied toolbar labels, disabled-button state, measured toolbar content, list row/subitem data, selection, teardown and transactional coordinate-overflow refusal. [Diagnostic observations](../../evidence/M14/4/development/mixed-menu-controls/list-toolbar-fixture.json). The original 7-Zip startup proceeds through menu and toolbar construction into its list window, then stops at InvalidateRect. It is still not a qualified graphical application.

## Initial native drawing path

A checked copied IPC path retains rectangle and text primitives for native Windows client surfaces. The broker owns every retained byte and validates process/window/thread identity, geometry, UTF-8 and quotas; no original callback or user pointer enters the compositor. The desktop clips each surface through its parent chain and renders with Engacer's existing native font/compositor. Original application drawing remains CPL3 code.

Each surface retains at most 224 primitives, allocated lazily in seven-record pages. The session ceiling is 128 pages (512 KiB); pages are reused on repaint and freed on window destruction. This avoids a separate full-resolution bitmap for every child window. The initial BeginPaint path promotes damage to the whole client surface, resets its retained primitives and returns the expanded paint bounds. Partial-region preservation, richer GDI operations and final typography remain further work; this is not complete GDI compatibility.

The owned painting fixture passes 21 process lifetimes, each with at least 21 real paint callbacks. It independently checks physical framebuffer RGB pixels, 573 visible native text pixels in the named capture, stable one-page drawing storage through repeated repaints, and zero retained GUI/drawing pages after closing. [Exact native observations](../../evidence/M14/4/development/58a58f96d2827eeae3f1253fa39633c3/paint-native.json), [actual framebuffer](../../evidence/M14/4/development/58a58f96d2827eeae3f1253fa39633c3/native-painted-window.png). This is our own fixture, not an original-app GUI acceptance result.

## Composite controls and own system artwork

A subsequent diagnostic supplies real nested combo/edit windows, copied combo items/data, selection, editable-text forwarding, rebar band parenting/layout and native toolbar/status creation helpers. The owned fixture checks these APIs and actual generic file/folder image lists, original stock-view-toolbar button data and image-list teardown. The OS-generated file/folder/view artwork is separate from original application resources. It does not establish a Windows shell namespace or shell extension service. Unsupported PIDL queries still fail explicitly. [Native diagnostic](../../evidence/M14/4/development/composite-diagnostics/controls.json).

The original file-manager startup reaches its SetTimer call after constructing these controls. [Observed stop](../../evidence/M14/4/development/composite-diagnostics/original-settimer-stop.json). These are explicitly mixed-runtime diagnostics against the recorded immutable kernel; they are not original GUI acceptance or a public ISO qualification.

## Timer and input ownership candidate

The next full candidate adds a lazy 64-slot timer page per protected process, window/thread-bound IDs, coalesced deadlines, cancellation and teardown. GUI waits join the existing scheduler deadline ownership; a process with no due input or timer sleeps. Timer callbacks are opaque values in the broker and execute only through the original protected user dispatcher. A separate native fixture must qualify actual elapsed deadlines, filtered waits, callback execution, idle halt, quota refusal and repeated cleanup before this behavior is accepted.

The candidate also stores focus/capture as checked window capabilities, with thread checks, disabled-ancestor refusal and stale-window cleanup. Original focus/capture notifications execute in CPL3. Keyboard routing follows the focused descendant; pointer routing hit-tests child windows and translates coordinates, with capture extending pointer delivery outside the native client surface. These routes still require their full native event tests and do not establish complete modality or multi-thread input attachment.

## List sorting, placement and accelerator development

Column order is stored as a checked permutation with insertion/removal reflow. The non-owner-data item-count message reserves capacity without inventing rows. Stable list sorting compares original item parameters by invoking the original CPL3 comparator. Two bounded index arrays and one row temporary avoid allocating a second complete row model. Row mutations during a sort are refused; callback-driven window destruction is checked before continuing.

The window runtime now stores normal placement, applies work-area maximization and tracks minimized/maximized restore intent. Native caption state synchronization remains a separate pending consistency test. The accelerator layer loads real resource records, copies bounded tables and sends commands through the original procedure. Physical modifier/scancode coverage and complete menu activation semantics are not established by these initial table tests.

The original file manager's first functional diagnostic runs its own loop, renders its own root-folder data, accepts text input and closes normally. [Scope and actual capture](../milestones/m14-4.md#first-original-gui-functional-diagnostic). The generic system-image service does not add networking, a Windows shell namespace or universal application compatibility.
