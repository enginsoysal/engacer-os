/* Eager text formats in the declared UTF-8 ACP/OEM profile. */
static lock142 clipboard_api146;
static uint64_t clipboard_handles146[3],clipboard_epoch146;
static unsigned clipboard_local_thread146,clipboard_local_open146;
static int64_t clipboard_call146(unsigned operation,uint64_t pointer,uint64_t argument){return(int64_t)sys8(W8_SYS_UI144,WUI_CLIPBOARD146,operation,pointer,argument,0);}
static int clipboard_state146(wclip_state146*state,unsigned opened){int64_t status=clipboard_call146(WCLIP_STATE146,(uint64_t)(uintptr_t)state,opened);if(status<0){last8((unsigned)-status);return 0;}return 1;}
static int clipboard_index146(unsigned format){return format==1?0:format==7?1:format==13?2:-1;}
static unsigned clipboard_locked146(void){
 if(global_objects146)for(unsigned i=0;i<GLOBAL_SLOTS146;++i)if((global_objects146[i].flags&GLOBAL_SYSTEM146)&&global_objects146[i].locks)return 1;return 0;
}
static void clipboard_clear146(uint64_t keep){
 if(global_objects146)for(unsigned i=0;i<GLOBAL_SLOTS146;++i){global_object146*object=global_objects146+i;if(object->handle!=keep&&(object->flags&GLOBAL_SYSTEM146)){free8(object->pointer);memset(object,0,sizeof(*object));--global_count146;}}
 if(!global_count146){free8(global_objects146);global_objects146=0;}
 memset(clipboard_handles146,0,sizeof(clipboard_handles146));clipboard_epoch146=0;
}
static int MS f_OpenClipboard(uint64_t window){
 lock_enter142(&clipboard_api146);int64_t status=clipboard_call146(WCLIP_OPEN146,window,0);
 if(status<0){lock_leave142(&clipboard_api146);last8((unsigned)-status);return 0;}
 if(status>0||!clipboard_local_open146||clipboard_local_thread146!=tid142()){lock_enter142(&global_lock146);clipboard_clear146(0);lock_leave142(&global_lock146);}
 clipboard_local_open146=1;clipboard_local_thread146=tid142();lock_leave142(&clipboard_api146);return 1;
}
static int MS f_CloseClipboard(void){
 lock_enter142(&clipboard_api146);wclip_state146 state;if(!clipboard_state146(&state,1)){lock_leave142(&clipboard_api146);return 0;}
 lock_enter142(&global_lock146);if(clipboard_locked146()){lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);last8(212);return 0;}
 int64_t status=clipboard_call146(WCLIP_CLOSE146,0,0);if(status>=0){clipboard_clear146(0);clipboard_local_open146=0;}
 lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);if(status<0)last8((unsigned)-status);return status>=0;
}
static int MS f_EmptyClipboard(void){
 lock_enter142(&clipboard_api146);wclip_state146 state;if(!clipboard_state146(&state,1)){lock_leave142(&clipboard_api146);return 0;}
 lock_enter142(&global_lock146);if(clipboard_locked146()){lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);last8(212);return 0;}
 int64_t status=clipboard_call146(WCLIP_EMPTY146,0,0);if(status>=0)clipboard_clear146(0);
 lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);if(status<0)last8((unsigned)-status);return status>=0;
}
static uint64_t MS f_SetClipboardData(unsigned format,uint64_t handle){
 /* This development slice publishes eager Unicode; other formats refuse. */
 int index=clipboard_index146(format);if(format!=13||!handle){last8(50);return 0;}
 lock_enter142(&clipboard_api146);wclip_state146 state;if(!clipboard_state146(&state,1)){lock_leave142(&clipboard_api146);return 0;}
 lock_enter142(&global_lock146);global_object146*object=global_find146(handle);unsigned error=0;char*text=0;int needed=0;
 if(!object)error=6;else if(!(object->flags&2)||!object->pointer)error=87;else if(object->flags&GLOBAL_SYSTEM146)error=5;else if(clipboard_locked146())error=212;
 if(error)goto failed;
 const WCHAR*wide=object->pointer;unsigned limit=(unsigned)(object->bytes/2);if(limit>8192)limit=8192;unsigned units=0;while(units<limit&&wide[units])++units;
 if(units==limit){error=object->bytes>16384?1816:13;goto failed;}
 needed=f_WideCharToMultiByte(65001,0,wide,(int)units+1,0,0,0,0);if(!needed){error=*(volatile uint32_t*)(uintptr_t)(teb142()+0x68);goto failed;}
 if(needed>8192){error=1816;goto failed;}text=alloc8((unsigned)needed);if(!text){error=8;goto failed;}
 if(f_WideCharToMultiByte(65001,0,wide,(int)units+1,text,needed,0,0)!=needed){error=1113;goto failed;}
 {wclip_transfer146 transfer={0,(uint64_t)(uintptr_t)text,(unsigned)needed,0};int64_t result=clipboard_call146(WCLIP_WRITE146,(uint64_t)(uintptr_t)&transfer,0);
  if(result<0){error=(unsigned)-result;goto failed;}
  clipboard_clear146(handle);object=global_find146(handle);object->flags|=GLOBAL_SYSTEM146;clipboard_handles146[index]=handle;clipboard_epoch146=(uint64_t)result;
 }
 free8(text);lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);return handle;
failed:free8(text);lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);last8(error);return 0;
}
static uint64_t MS f_GetClipboardData(unsigned format){
 int index=clipboard_index146(format);if(index<0){last8(50);return 0;}
 lock_enter142(&clipboard_api146);wclip_state146 state;if(!clipboard_state146(&state,1)){lock_leave142(&clipboard_api146);return 0;}
 if(!state.bytes||state.bytes>8192){lock_leave142(&clipboard_api146);last8(state.bytes?1816:1168);return 0;}
 lock_enter142(&global_lock146);uint64_t handle=0;char*text=0;unsigned error=0;
 if(clipboard_epoch146!=state.revision){if(clipboard_locked146()){error=212;goto failed;}clipboard_clear146(0);}
 if(clipboard_handles146[index]){handle=clipboard_handles146[index];lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);return handle;}
 text=alloc8(state.bytes);if(!text){error=8;goto failed;}
 {wclip_transfer146 transfer={state.revision,(uint64_t)(uintptr_t)text,state.bytes,0};int64_t status=clipboard_call146(WCLIP_READ146,(uint64_t)(uintptr_t)&transfer,0);if(status<0){error=(unsigned)-status;goto failed;}}
 int units=format==13?f_MultiByteToWideChar(65001,8,text,(int)state.bytes,0,0):(int)state.bytes;
 if(!units){error=1113;goto failed;}
 handle=f_GlobalAlloc(0x42,(size_t)units*(format==13?2:1));if(!handle){error=8;goto failed;}global_object146*object=global_find146(handle);
 if(format==13){if(f_MultiByteToWideChar(65001,8,text,(int)state.bytes,object->pointer,units)!=units){error=1113;goto failed;}}
 else memcpy(object->pointer,text,state.bytes);
 object->flags|=GLOBAL_SYSTEM146;clipboard_handles146[index]=handle;clipboard_epoch146=state.revision;
 free8(text);lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);return handle;
failed:free8(text);if(handle)f_GlobalFree(handle);lock_leave142(&global_lock146);lock_leave142(&clipboard_api146);last8(error);return 0;
}
static int MS f_IsClipboardFormatAvailable(unsigned format){wclip_state146 state;return clipboard_index146(format)>=0&&clipboard_state146(&state,0)&&state.bytes!=0;}
static unsigned MS f_CountClipboardFormats(void){wclip_state146 state;return clipboard_state146(&state,0)&&state.bytes?3:0;}
static unsigned MS f_EnumClipboardFormats(unsigned format){
 wclip_state146 state;if(!clipboard_state146(&state,1))return 0;if(!state.bytes){last8(0);return 0;}
 if(!format)return 13;if(format==13)return 1;if(format==1)return 7;if(format==7){last8(0);return 0;}last8(87);return 0;
}
static uint64_t MS f_GetClipboardOwner(void){wclip_state146 state;return clipboard_state146(&state,0)?state.owner:0;}
static uint64_t MS f_GetOpenClipboardWindow(void){int64_t status=clipboard_call146(WCLIP_OPEN_WINDOW146,0,0);if(status<0){last8((unsigned)-status);return 0;}return(uint64_t)status;}
static unsigned MS f_GetClipboardSequenceNumber(void){wclip_state146 state;return clipboard_state146(&state,0)?(unsigned)state.revision:0;}
