/* Process-local GDI+ lifetime gate for the native display/event backend. This
 * does not implement unregistered image/font/drawing APIs or create idle workers. */
typedef struct {uint32_t version,pad;uint64_t callback;int32_t suppress_thread,suppress_codecs;} gp_input148;
typedef struct {uint64_t token,callback;uint32_t width,height,scale,version;} gp_runtime148;
_Static_assert(sizeof(gp_input148)==24,"AMD64 GdiplusStartupInput ABI");
static gp_runtime148 gp_runtimes148[8];static unsigned gp_generation148,gp_references148;static lock142 gp_lock148;
static unsigned MS f_GdiplusStartup(uint64_t*token,const gp_input148*input,void*output){
 if(!token||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)token,8,2,0,0))return 2;
 if(!input||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,sizeof(*input),1,0,0)){*token=0;return 2;}
 gp_input148 options=*input;*token=0;if(options.version!=1)return 17;
 if(options.callback&&sys8(W8_SYS_ACCESS,options.callback,1,5,0,0))return 2;
 if(options.suppress_thread){print8("GDI+ notification hooks are not implemented.\n");return output?6u:2u;}
 /* Version 1 ignores external codec suppression. Release builds do not emit
  * debug assertions. Display changes are serviced by the existing native broker. */
 wui_metrics144 metrics;if(!window_metrics144(&metrics)||!metrics.width||!metrics.height||!metrics.scale)return 7;
 lock_enter142(&gp_lock148);unsigned slot=0;while(slot<8&&gp_runtimes148[slot].token)++slot;
 if(slot==8||gp_generation148==0xffffff){lock_leave142(&gp_lock148);return 3;}
 uint64_t value=UINT64_C(0xc8000000)|((uint64_t)(++gp_generation148)<<3)|slot;
 gp_runtimes148[slot]=(gp_runtime148){value,options.callback,metrics.width,metrics.height,metrics.scale,1};++gp_references148;lock_leave142(&gp_lock148);*token=value;return 0;
}
static void MS f_GdiplusShutdown(uint64_t token){
 unsigned slot=(unsigned)(token&7u);lock_enter142(&gp_lock148);
 if(!token||gp_runtimes148[slot].token!=token||!gp_references148){lock_leave142(&gp_lock148);fail8("The GDI+ startup token is invalid or already released.");}
 memset(gp_runtimes148+slot,0,sizeof(*gp_runtimes148));--gp_references148;lock_leave142(&gp_lock148);
}
