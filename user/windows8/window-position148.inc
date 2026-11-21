/* Geometry-only positioning retains the existing activation and stacking order. */
typedef struct {HANDLE window,after;int x,y,width,height;unsigned flags,pad;} window_position148;
_Static_assert(sizeof(window_position148)==40,"AMD64 WINDOWPOS ABI");
static unsigned position_flags148(unsigned flags){return !(flags&~0x617u)&&(flags&0x14u)==0x14u;}
static int64_t position_changed148(HANDLE handle,int64_t parameter){
 if(!parameter||sys8(W8_SYS_ACCESS,(uint64_t)parameter,sizeof(window_position148),1,0,0)){last8(87);return 0;}window_position148 position=*(const window_position148*)(uintptr_t)parameter;wui_view144 view;if(!window_view144(handle,&view))return 0;
 if(!(position.flags&2u)){int x,y;if(view.description.parent){int border=view.description.style&0x00800000u?1:0;x=view.description.bounds.x+border;y=view.description.bounds.y+border;}else if(!window_origin144(handle,&x,&y))return 0;f_SendMessageW(handle,3,0,(x&65535)|((int64_t)(y&65535)<<16));}
 if(!(position.flags&1u)){win_rect144 client;if(f_GetClientRect(handle,&client)){unsigned kind=view.description.style&0x20000000u?1:view.description.style&0x01000000u?2:0;f_SendMessageW(handle,5,kind,(client.right&65535)|((int64_t)(client.bottom&65535)<<16));}}
 return 0;
}
static int MS f_SetWindowPos(HANDLE handle,HANDLE after,int x,int y,int width,int height,unsigned flags){
 if(handle==DESKTOP_HANDLE148){last8(5);return 0;}if(!position_flags148(flags)){last8(50);return 0;}
 lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);if(!w||w->thread!=tid142()){lock_leave142(&ui_lock144);last8(w?5:1400);return 0;}if(!ui_refresh144(w)){lock_leave142(&ui_lock144);return 0;}wui_rect144 current=w->description.bounds;
 window_position148 position={handle,after,flags&2?current.x:x,flags&2?current.y:y,flags&1?current.width:width,flags&1?current.height:height,flags,0};lock_leave142(&ui_lock144);
 if(position.width<0||position.height<0||position.width>16384||position.height>16384||position.x< -32768||position.x>32767||position.y< -32768||position.y>32767){last8(87);return 0;}
 if(!(flags&0x400u))f_SendMessageW(handle,0x46,0,(int64_t)(uintptr_t)&position);
 if(position.window!=handle){last8(87);return 0;}if(!position_flags148(position.flags)){last8(50);return 0;}
 lock_enter142(&ui_lock144);w=ui_window_lookup144(handle);if(!w||w->thread!=tid142()){lock_leave142(&ui_lock144);last8(w?5:1400);return 0;}if(!ui_refresh144(w)){lock_leave142(&ui_lock144);return 0;}wui_description144 previous=w->description;wui_rect144 normal=w->normal_bounds;current=previous.bounds;
 if(position.flags&2){position.x=current.x;position.y=current.y;}if(position.flags&1){position.width=current.width;position.height=current.height;}
 if(position.width<0||position.height<0||position.width>16384||position.height>16384||position.x< -32768||position.x>32767||position.y< -32768||position.y>32767){lock_leave142(&ui_lock144);last8(87);return 0;}
 if(position.x==current.x&&position.y==current.y)position.flags|=2;if(position.width==current.width&&position.height==current.height)position.flags|=1;
 w->description.bounds=(wui_rect144){position.x,position.y,position.width,position.height};if(!(w->description.style&0x21000000u))w->normal_bounds=w->description.bounds;unsigned ok=ui_sync144(w);if(!ok){w->description=previous;w->normal_bounds=normal;}lock_leave142(&ui_lock144);if(!ok)return 0;
 f_SendMessageW(handle,0x47,0,(int64_t)(uintptr_t)&position);return 1;
}
