# M14.4 Windows window and message ownership

Status: exact-source M14.4 native qualification passes for the bounded original-window/message profile. All 47 native and eight supporting host groups pass on build `eafa19ad1e60ef524888e94dbb5af01e`. Matching public media and independent downloads pass; complete actual website closure is being verified. [Acceptance](../../evidence/M14/4/acceptance-results.json), [resource observations](../../evidence/M14/4/resources.json). Complete original GUI application tasks remain later blocking gates.

## Execution boundary

An original PE application registers its own window procedure in its private address space. Creation, synchronous messages and dispatch call that procedure in CPL3 using the Windows x64 ABI. The kernel never calls an application procedure. The native compositor consumes checked window descriptions and supplies queued input, not executable callbacks.

Window handles carry a generation. Every operation checks process and thread ownership; a reused slot cannot redirect an old message to a native app. Top-level windows use existing native movement, sizing, minimization and caption handling. Child controls retain their own hierarchy. Owner relationships and parent relationships are distinct. Cross-process synchronous messages are initially refused, not reported as successful.

## Event-driven queues

A GUI thread acquires one bounded queue page on first use. Windows also acquire bounded lazy records; console processes allocate neither. Posted messages retain FIFO order, including repeated keyboard input. Mouse-move coalescing is permitted only when it does not reorder intervening events. Queue exhaustion returns an error to the caller. Native close/input admission reserves capacity separately from application posts. Filtered retrieval includes a requested parent's descendants and preserves unrelated messages, and WM_QUIT remains retrievable regardless of the message range. A blocking retrieval parks atomically after checking the queue again; actual matching input wakes it. No recurring compatibility polling worker is introduced.

Normal exit, thread exit, faults and cancellation must release windows, queues and later drawing resources. Resource peaks include supervisor records and queue pages. Twenty repeated original-app lifetimes must leave no unexplained retained pages before acceptance.

## Creation and reentrancy

WM_NCCREATE precedes WM_CREATE and visibility. A false WM_NCCREATE or minus-one WM_CREATE aborts creation and returns a null handle. Original procedures may create children, update GWLP_USERDATA and send messages while processing creation. Callback pointers remain in the original process; exceptions use the existing contained exception dispatcher.

## Verification and scope

Host tests establish queue contracts only. Owned synthetic AMD64 fixtures establish native ABI, creation, dispatch, invalid-handle, saturation, thread and cleanup behavior. The separate blocking acceptance is the unmodified original 7-Zip file manager, its actual message loop and visibly working window interactions. Synthetic fixtures, resolved import names and a recreated native interface do not replace it. Drawing and common-control prerequisites needed for that first original window must be implemented honestly; broader GDI/control qualification continues in M14.5.

References: [window creation](https://learn.microsoft.com/en-us/windows/win32/winmsg/about-windows), [WM_CREATE failure](https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-create), [application state during creation](https://learn.microsoft.com/windows/win32/learnwin32/managing-application-state-), [virtual list-view ownership](https://learn.microsoft.com/en-us/windows/win32/controls/list-view-controls-overview).

[WM_QUIT](https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-quit) ends retrieval without dispatching to a window procedure. Its separately retained quit request cannot be lost when application posts exhaust the bounded queue. [Why PostQuitMessage is distinct](https://devblogs.microsoft.com/oldnewthing/20051104-33/?p=33453).

## Native admission, modality and placement decisions

Visible original top-level windows reserve the same eight native desktop slots used by native applications. The broker separately bounds all Windows descriptors, including children and hidden windows, to 32. A failed visible-root reservation returns quota error 1816 and a null creation result; it must not report an invisible successful window. Native application launch observes the same reservations. Disabled owners lose keyboard focus and pointer capture, cannot receive native caption actions, and remain below their enabled owned modal. Closing a modal can restore the original owner's input. Owner destruction releases owned windows as well as child descendants.

Normal bounds and maximized restore intent live in the checked broker so native caption actions and original USER32 queries share state. GetWindowPlacement always returns zero flags; SetWindowPlacement's restore-to-maximized flag is retained internally for minimized restoration. The unsupported custom minimum-position flag returns ERROR_NOT_SUPPORTED instead of silently succeeding. The native compositor traverses child surfaces using one bounded iterative stack, avoiding kernel-stack growth with legal HWND nesting. Initial visible creation sends the original procedure WM_SHOWWINDOW and invalidates its surface through the normal paint path.

The alternative of maintaining independent desktop/runtime placement state caused contradictory restore behavior; the broker is the common authority. Recursive rendering was simpler, but multiplied large drawing/view temporaries by 32 levels. The explicit traversal preserves child paint order and clipping with bounded stack use. Physical max-depth drawing and repeated teardown must pass on the final candidate before acceptance.

Development candidate d7d1a07ab90e36f7cd396d09dc60aedb passes 21 original file-manager window lifetimes, 21 ownership/modality/capture lifetimes and 21 contained GUI instruction-fault runs. These observations precede the final placement-output and iterative-renderer corrections and are not stage acceptance. [Preserved development scope](../../evidence/M14/4/development/d7d1a07ab90e36f7cd396d09dc60aedb/scope.json). Original-app window testing is separate from the complete original-app functional corpus required by M14.12.

API references: [GetWindowPlacement output flags](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowplacement), [WINDOWPLACEMENT flags](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-windowplacement).

The maximum-depth native fixture passes 21 lifetimes on candidate af750de50bd84d5ad45401164569fdb6, independently checking the deepest child pixel, 32 initial visibility callbacks, descriptor-quota refusal and zero retained pages. Its placement edge fixture correctly fails when a normal-bounds move overwrites requested minimized restore intent. The correction applies that intent after geometry synchronization; the unchanged fixture then passes a separately labelled mixed-runtime diagnostic. A new complete build remains required. [Preserved failure and correction](../../evidence/M14/4/development/af750de50bd84d5ad45401164569fdb6/scope.json).

Disabled-owner pointer targets are consumed before native desktop selection/focus dispatch. Merely suppressing caption actions was insufficient: the generic background path could still change desktop selection. The strengthened native fixture separately checks retained desktop focus/selection, modal keyboard delivery and context-menu refusal. This is a blocking correctness correction, not broader control appearance qualification.
