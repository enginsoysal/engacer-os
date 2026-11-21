/* The measured zero-handle GUI wait; mixed object/message arrays refuse. */
static unsigned MS f_MsgWaitForMultipleObjects(unsigned count,const HANDLE*handles,int all,unsigned timeout,unsigned mask){
 (void)handles;(void)all;if(count){last8(count>31?87:50);return UINT32_MAX;}if(mask&~0x1dffu){last8(87);return UINT32_MAX;}
 if(mask&32u){lock_enter142(&ui_lock144);unsigned ready=0;for(ui_window_runtime144*w=ui_runtime_windows144;w;w=w->next)if(w->thread==tid142()&&w->description.visible&&w->invalid&&!w->paint_seen148){ready=1;break;}lock_leave142(&ui_lock144);if(ready)return 0;}
 w8_wait_request142 request={.all=2,.timeout=timeout,.pad=mask};int64_t result=(int64_t)sys8(W8_SYS_WAIT_OBJECTS,(uint64_t)(uintptr_t)&request,0,0,0,0);if(result<0){last8((unsigned)-result);return UINT32_MAX;}return(unsigned)result;
}
