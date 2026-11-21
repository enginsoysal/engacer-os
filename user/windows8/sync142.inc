/* Kernel-backed objects and atomic mixed waits across private processes. */
static HANDLE sync_create_api142(unsigned kind,int count,int maximum,unsigned manual,const WCHAR*name,unsigned access,unsigned open_only){
 if(name&&wlen8(name)>95){last8(206);return 0;}w8_sync_request142 request={.kind=kind,.manual=manual,.count=count,.maximum=maximum,.access=access};widecopy8(request.name,name,96);w8_sync_result142 result={0};int64_t status=(int64_t)sys8(W8_SYS_SYNC_CREATE,(uint64_t)&request,(uint64_t)&result,open_only,0,0);if(status<0){last8((unsigned)-status);return 0;}if(!open_only)last8(result.existed?183:0);return result.handle;
}
static int sync_operate_api142(HANDLE handle,unsigned operation,uint64_t value,uint64_t argument){int64_t result=(int64_t)sys8(W8_SYS_SYNC_OPERATION,handle,operation,value,argument,0);if(result<0){last8((unsigned)-result);return 0;}return 1;}
static HANDLE MS f_CreateEventW(void*security,int manual,int initial,const WCHAR*name){if(security){last8(50);return 0;}return sync_create_api142(1,initial!=0,1,manual!=0,name,0,0);}
static HANDLE MS f_CreateSemaphoreW(void*security,int initial,int maximum,const WCHAR*name){if(security){last8(50);return 0;}if(initial<0||maximum<=0||initial>maximum){last8(87);return 0;}return sync_create_api142(2,initial,maximum,0,name,0,0);}
static HANDLE MS f_CreateWaitableTimerW(void*security,int manual,const WCHAR*name){if(security){last8(50);return 0;}return sync_create_api142(3,0,1,manual!=0,name,0,0);}
static HANDLE sync_open_api142(unsigned kind,unsigned access,int inherit,const WCHAR*name){if(!name||!name[0]||inherit||(access&~0x1f0003u)){last8(87);return 0;}return sync_create_api142(kind,0,1,0,name,access,1);}
static HANDLE MS f_OpenEventW(unsigned access,int inherit,const WCHAR*name){return sync_open_api142(1,access,inherit,name);}
static HANDLE MS f_OpenSemaphoreW(unsigned access,int inherit,const WCHAR*name){return sync_open_api142(2,access,inherit,name);}
static HANDLE MS f_OpenWaitableTimerW(unsigned access,int inherit,const WCHAR*name){return sync_open_api142(3,access,inherit,name);}
static int MS f_SetEvent(HANDLE handle){return sync_operate_api142(handle,1,0,0);}
static int MS f_ResetEvent(HANDLE handle){return sync_operate_api142(handle,2,0,0);}
static int MS f_ReleaseSemaphore(HANDLE handle,int count,int*previous){return sync_operate_api142(handle,3,(uint64_t)(int64_t)count,(uint64_t)previous);}
static int MS f_SetWaitableTimer(HANDLE handle,const int64_t*due,int period,void*callback,void*argument,int resume){
 (void)argument;if(!due||period<0){last8(87);return 0;}if(callback||resume){last8(50);return 0;}int64_t value=*due;uint64_t now=sys8(W8_SYS_TIME,0,0,0,0,0),delay;
 if(value<0){uint64_t units=(uint64_t)(-(value+1))+1;delay=units/10000+(units%10000!=0);}else{uint64_t clock=sys8(W8_SYS_TIME,1,0,0,0,0),units=(uint64_t)value>clock?(uint64_t)value-clock:0;delay=units/10000+(units%10000!=0);}if(delay>UINT64_MAX-now){last8(87);return 0;}return sync_operate_api142(handle,4,now+delay,(unsigned)period);
}
static int MS f_CancelWaitableTimer(HANDLE handle){return sync_operate_api142(handle,5,0,0);}
static unsigned MS f_WaitForMultipleObjects(unsigned count,const HANDLE*handles,int all,unsigned timeout){
 if(!count||count>32||!handles){last8(87);return UINT32_MAX;}w8_wait_request142 request={.count=count,.all=all!=0,.timeout=timeout};memcpy(request.handles,handles,count*8);int64_t result=(int64_t)sys8(W8_SYS_WAIT_OBJECTS,(uint64_t)&request,0,0,0,0);if(result<0){last8((unsigned)-result);return UINT32_MAX;}return (unsigned)result;
}
static unsigned MS f_WaitForSingleObject(HANDLE handle,unsigned timeout){return f_WaitForMultipleObjects(1,&handle,0,timeout);}
static int MS f_CloseHandle(HANDLE handle){
#ifdef ENGINE_M14
 if(snapshot_handle148(handle))return snapshot_close148(handle);
 if(pipe_handle147(handle))return pipe_api147(WPIPE_CLOSE147,handle,0,0)>=0;
#endif
 if((handle&W8_HANDLE_TAG_MASK)==WMAP_TAG146){int64_t result=(int64_t)sys8(W8_SYS_MAPPING146,WMAP_CLOSE146,handle,0,0,0);if(result<0){last8((unsigned)-result);return 0;}return 1;}
 if((handle&UINT64_C(0xfffffffff0000000))==W8_FILE_TAG143){int64_t result=(int64_t)sys8(W8_SYS_FILE_OP143,handle,7,0,0,0);if(result<0){last8((unsigned)-result);return 0;}return 1;}
 if((handle&W8_HANDLE_TAG_MASK)==UINT64_C(0x20000000)){int64_t result=(int64_t)sys8(W8_SYS_SYNC_CLOSE,handle,0,0,0,0);if(result<0){last8((unsigned)-result);return 0;}return 1;}
 if((handle&W8_HANDLE_TAG_MASK)==W8_PROCESS_TAG){if((int64_t)sys8(W8_SYS_PROCESS_CLOSE,handle,0,0,0,0)<0){last8(6);return 0;}return 1;}
 if((handle&UINT64_C(0xffffffffc0000000))==UINT64_C(0x40000000)){if((int64_t)sys8(W8_SYS_THREAD_CLOSE,handle,0,0,0,0)<0){last8(6);return 0;}return 1;}
 if(handle>=256&&handle<288){if(close8((int)(handle-256))){last8(29);return 0;}return 1;}last8(6);return 0;
}
