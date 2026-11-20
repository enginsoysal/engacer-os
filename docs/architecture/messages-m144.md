# M14.4 Windows window and message ownership

Status: implementation in progress, not native GUI qualification. M14.3 remains the current tested download.

## Execution boundary

An original PE application registers its own window procedure in its private address space. Creation, synchronous messages and dispatch call that procedure in CPL3 using the Windows x64 ABI. The kernel never calls an application procedure. The native compositor consumes checked window descriptions and supplies queued input, not executable callbacks.

Window handles carry a generation. Every operation checks process and thread ownership; a reused slot cannot redirect an old message to a native app. Top-level windows use existing native movement, sizing, minimization and caption handling. Child controls retain their own hierarchy. Owner relationships and parent relationships are distinct. Cross-process synchronous messages are initially refused, not reported as successful.

## Event-driven queues

A GUI thread acquires one bounded queue page on first use. Windows also acquire bounded lazy records; console processes allocate neither. Posted messages retain FIFO order, including repeated keyboard input. Mouse-move coalescing is permitted only when it does not reorder intervening events. Queue exhaustion returns an error to the caller. Native close/input admission reserves capacity separately from application posts. Filtered retrieval preserves unrelated messages, and WM_QUIT remains retrievable regardless of the message range. A blocking retrieval parks atomically after checking the queue again; actual matching input wakes it. No recurring compatibility polling worker is introduced.

Normal exit, thread exit, faults and cancellation must release windows, queues and later drawing resources. Resource peaks include supervisor records and queue pages. Twenty repeated original-app lifetimes must leave no unexplained retained pages before acceptance.

## Creation and reentrancy

WM_NCCREATE precedes WM_CREATE and visibility. A false WM_NCCREATE or minus-one WM_CREATE aborts creation and returns a null handle. Original procedures may create children, update GWLP_USERDATA and send messages while processing creation. Callback pointers remain in the original process; exceptions use the existing contained exception dispatcher.

## Verification and scope

Host tests establish queue contracts only. Owned synthetic AMD64 fixtures establish native ABI, creation, dispatch, invalid-handle, saturation, thread and cleanup behavior. The separate blocking acceptance is the unmodified original 7-Zip file manager, its actual message loop and visibly working window interactions. Synthetic fixtures, resolved import names and a recreated native interface do not replace it. Drawing and common-control prerequisites needed for that first original window must be implemented honestly; broader GDI/control qualification continues in M14.5.

References: [window creation](https://learn.microsoft.com/en-us/windows/win32/winmsg/about-windows), [WM_CREATE failure](https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-create), [application state during creation](https://learn.microsoft.com/windows/win32/learnwin32/managing-application-state-), [virtual list-view ownership](https://learn.microsoft.com/en-us/windows/win32/controls/list-view-controls-overview).

[WM_QUIT](https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-quit) ends retrieval without dispatching to a window procedure. Its separately retained quit request cannot be lost when application posts exhaust the bounded queue. [Why PostQuitMessage is distinct](https://devblogs.microsoft.com/oldnewthing/20051104-33/?p=33453).
