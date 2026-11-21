/* Process-local GDI+ lifetime gate for the native display/event backend. This
 * does not implement unregistered image/font/drawing APIs or create idle workers. */
typedef struct {uint32_t version,pad;uint64_t callback;int32_t suppress_thread,suppress_codecs;} gp_input148;
typedef struct {uint64_t token,callback;uint32_t width,height,scale,version,suppressed,reserved;} gp_runtime148;
typedef struct {uint64_t token;unsigned thread,reserved;} gp_hook148;
_Static_assert(sizeof(gp_input148)==24,"AMD64 GdiplusStartupInput ABI");
static gp_runtime148 gp_runtimes148[8];static unsigned gp_generation148,gp_references148;static lock142 gp_lock148;
static gp_hook148 gp_hooks148[8];static unsigned gp_hook_generation148;
static unsigned MS gp_hook_create148(uint64_t*token){
 if(!token||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)token,8,2,0,0))return 2;*token=0;
 lock_enter142(&gp_lock148);unsigned active=gp_references148;lock_leave142(&gp_lock148);if(!active)return 18;
 wui_filter144 filter={0,0,0,0,0};wui_message144 ignored;int64_t result=ui_call144(WUI_PEEK144,0,&ignored,(uint64_t)(uintptr_t)&filter);if(result<0)return 7;
 lock_enter142(&gp_lock148);if(!gp_references148){lock_leave142(&gp_lock148);return 18;}unsigned slot=0;while(slot<8&&gp_hooks148[slot].token)++slot;
 if(slot==8||gp_hook_generation148==0xffffff){lock_leave142(&gp_lock148);return 3;}
 uint64_t value=UINT64_C(0xd8000000)|((uint64_t)(++gp_hook_generation148)<<3)|slot;gp_hooks148[slot]=(gp_hook148){value,tid142(),0};lock_leave142(&gp_lock148);*token=value;return 0;
}
static void MS gp_hook_remove148(uint64_t token){unsigned slot=(unsigned)(token&7u);lock_enter142(&gp_lock148);if(!token||gp_hooks148[slot].token!=token||gp_hooks148[slot].thread!=tid142()){lock_leave142(&gp_lock148);fail8("The GDI+ notification token or owning thread is invalid.");}memset(gp_hooks148+slot,0,sizeof(*gp_hooks148));lock_leave142(&gp_lock148);}
static void gp_message148(unsigned message){
 if(message!=5&&message!=0x1a&&message!=0x1d&&message!=0x7e&&message!=0x2e0)return;
 lock_enter142(&gp_lock148);unsigned enabled=0,thread=tid142();
 if(gp_references148){for(unsigned i=0;i<8;++i){if(gp_runtimes148[i].token&&!gp_runtimes148[i].suppressed)enabled=1;if(gp_hooks148[i].token&&gp_hooks148[i].thread==thread)enabled=1;}}
 lock_leave142(&gp_lock148);if(!enabled)return;wui_metrics144 metrics;if(!window_metrics144(&metrics))return;
 lock_enter142(&gp_lock148);for(unsigned i=0;i<8;++i)if(gp_runtimes148[i].token){gp_runtimes148[i].width=metrics.width;gp_runtimes148[i].height=metrics.height;gp_runtimes148[i].scale=metrics.scale;}lock_leave142(&gp_lock148);
}
static unsigned MS f_GdiplusStartup(uint64_t*token,const gp_input148*input,void*output){
 if(!token||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)token,8,2,0,0))return 2;
 if(!input||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,sizeof(*input),1,0,0)){*token=0;return 2;}
 gp_input148 options=*input;*token=0;if(options.version!=1)return 17;
 if(options.callback&&sys8(W8_SYS_ACCESS,options.callback,1,5,0,0))return 2;
 if(options.suppress_thread&&(!output||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)output,16,2,0,0)))return 2;
 /* Version 1 ignores external codec suppression. Release builds do not emit
  * debug assertions. Display changes are serviced by the existing native broker. */
 wui_metrics144 metrics;if(!window_metrics144(&metrics)||!metrics.width||!metrics.height||!metrics.scale)return 7;
 lock_enter142(&gp_lock148);unsigned slot=0;while(slot<8&&gp_runtimes148[slot].token)++slot;
 if(slot==8||gp_generation148==0xffffff){lock_leave142(&gp_lock148);return 3;}
 uint64_t value=UINT64_C(0xc8000000)|((uint64_t)(++gp_generation148)<<3)|slot;
 gp_runtimes148[slot]=(gp_runtime148){value,options.callback,metrics.width,metrics.height,metrics.scale,1,options.suppress_thread!=0,0};++gp_references148;lock_leave142(&gp_lock148);
 if(options.suppress_thread){uint64_t hooks[2]={(uint64_t)(uintptr_t)gp_hook_create148,(uint64_t)(uintptr_t)gp_hook_remove148};memcpy(output,hooks,sizeof(hooks));}*token=value;return 0;
}
static void MS f_GdiplusShutdown(uint64_t token){
 unsigned slot=(unsigned)(token&7u);lock_enter142(&gp_lock148);
 if(!token||gp_runtimes148[slot].token!=token||!gp_references148){lock_leave142(&gp_lock148);fail8("The GDI+ startup token is invalid or already released.");}
 memset(gp_runtimes148+slot,0,sizeof(*gp_runtimes148));if(!--gp_references148)memset(gp_hooks148,0,sizeof(gp_hooks148));lock_leave142(&gp_lock148);
}
