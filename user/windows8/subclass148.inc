/* Same-thread common-control subclasses: live ordered callbacks, bounded metadata. */
typedef int64_t(MS*subclass_proc148)(HANDLE,unsigned,uint64_t,int64_t,uint64_t,uint64_t);
typedef struct subclass_node148 {struct subclass_node148*next;HANDLE window;subclass_proc148 proc;uint64_t id,data,sequence;} subclass_node148;
typedef struct subclass_frame148 {struct subclass_frame148*next;HANDLE window;unsigned thread,depth;uint64_t before;ui_proc144 base;} subclass_frame148;
static subclass_node148*subclasses148;static subclass_frame148*subclass_frames148;static unsigned subclass_count148;static uint64_t subclass_sequence148;
static unsigned subclass_window148(HANDLE h){ui_window_runtime144*w=ui_window_lookup144(h);if(!w||w->thread!=tid142()){last8(w?50:1400);return 0;}return 1;}
static int MS f_SetWindowSubclass(HANDLE h,subclass_proc148 proc,uint64_t id,uint64_t data){
 lock_enter142(&ui_lock144);if(!subclass_window148(h)||!proc){lock_leave142(&ui_lock144);if(!proc)last8(87);return 0;}unsigned count=0;
 for(subclass_node148*n=subclasses148;n;n=n->next)if(n->window==h){++count;if(n->proc==proc&&n->id==id){n->data=data;lock_leave142(&ui_lock144);return 1;}}
 if(count==16||subclass_count148==128||subclass_sequence148==UINT64_MAX-1){lock_leave142(&ui_lock144);last8(1816);return 0;}subclass_node148*n=alloc8(sizeof(*n));if(!n){lock_leave142(&ui_lock144);last8(8);return 0;}*n=(subclass_node148){subclasses148,h,proc,id,data,++subclass_sequence148};subclasses148=n;++subclass_count148;lock_leave142(&ui_lock144);return 1;
}
static int MS f_GetWindowSubclass(HANDLE h,subclass_proc148 proc,uint64_t id,uint64_t*out){
 lock_enter142(&ui_lock144);if(!subclass_window148(h)){lock_leave142(&ui_lock144);return 0;}if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,8,2,0,0)){lock_leave142(&ui_lock144);last8(998);return 0;}for(subclass_node148*n=subclasses148;n;n=n->next)if(n->window==h&&n->proc==proc&&n->id==id){*out=n->data;lock_leave142(&ui_lock144);return 1;}lock_leave142(&ui_lock144);return 0;
}
static int MS f_RemoveWindowSubclass(HANDLE h,subclass_proc148 proc,uint64_t id){
 lock_enter142(&ui_lock144);if(!subclass_window148(h)){lock_leave142(&ui_lock144);return 0;}subclass_node148**link=&subclasses148;while(*link){subclass_node148*n=*link;if(n->window==h&&n->proc==proc&&n->id==id){*link=n->next;--subclass_count148;free8(n);lock_leave142(&ui_lock144);return 1;}link=&n->next;}lock_leave142(&ui_lock144);return 0;
}
static void subclass_release148(HANDLE h){lock_enter142(&ui_lock144);subclass_node148**link=&subclasses148;while(*link){subclass_node148*n=*link;if(n->window==h){*link=n->next;--subclass_count148;free8(n);}else link=&n->next;}lock_leave142(&ui_lock144);}
static int64_t subclass_next148(subclass_frame148*frame,HANDLE h,unsigned message,uint64_t wp,int64_t lp){
 lock_enter142(&ui_lock144);if(!ui_window_lookup144(h)){lock_leave142(&ui_lock144);last8(1400);return 0;}subclass_node148*chosen=0;for(subclass_node148*n=subclasses148;n;n=n->next)if(n->window==h&&n->sequence<frame->before&&(!chosen||n->sequence>chosen->sequence))chosen=n;
 if(chosen){subclass_proc148 proc=chosen->proc;uint64_t id=chosen->id,data=chosen->data;frame->before=chosen->sequence;lock_leave142(&ui_lock144);return proc(h,message,wp,lp,id,data);}
 ui_proc144 base=frame->base;lock_leave142(&ui_lock144);return base(h,message,wp,lp);
}
static int64_t MS f_DefSubclassProc(HANDLE h,unsigned message,uint64_t wp,int64_t lp){
 lock_enter142(&ui_lock144);unsigned thread=tid142();subclass_frame148*frame=subclass_frames148;while(frame&&(frame->window!=h||frame->thread!=thread))frame=frame->next;lock_leave142(&ui_lock144);
 if(frame){uint64_t saved=frame->before;int64_t result=subclass_next148(frame,h,message,wp,lp);frame->before=saved;return result;}
 lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(h);ui_proc144 base=w?w->proc:0;unsigned valid=w&&w->thread==thread;lock_leave142(&ui_lock144);if(!valid){last8(w?50:1400);return 0;}return base(h,message,wp,lp);
}
static int64_t subclass_dispatch148(ui_proc144 base,HANDLE h,unsigned message,uint64_t wp,int64_t lp){
 lock_enter142(&ui_lock144);unsigned present=0,depth=0,thread=tid142();for(subclass_node148*n=subclasses148;n;n=n->next)if(n->window==h){present=1;break;}if(!present){lock_leave142(&ui_lock144);return base(h,message,wp,lp);}for(subclass_frame148*f=subclass_frames148;f;f=f->next)if(f->thread==thread)++depth;if(depth==32){lock_leave142(&ui_lock144);last8(50);return 0;}
 subclass_frame148 frame={subclass_frames148,h,thread,depth,subclass_sequence148+1,base};subclass_frames148=&frame;lock_leave142(&ui_lock144);int64_t result=subclass_next148(&frame,h,message,wp,lp);
 lock_enter142(&ui_lock144);subclass_frame148**link=&subclass_frames148;while(*link!=&frame)link=&(*link)->next;*link=frame.next;lock_leave142(&ui_lock144);return result;
}
