/* Process-local vectored fault dispatch; structured unwinding is separate. */
typedef struct {uint64_t callback;unsigned generation,kind,live;} exception_handler142;
static exception_handler142 exception_handlers142[64];static unsigned exception_generation142;static uint64_t unhandled_filter142;static lock142 exception_lock142;
static void* add_exception_handler142(unsigned first,uint64_t callback,unsigned kind){
 if(!callback||sys8(W8_SYS_ACCESS,callback,1,5,0,0)){last8(87);return 0;}lock_enter142(&exception_lock142);unsigned at=0;while(at<64&&exception_handlers142[at].live)++at;
 if(at==64||exception_generation142>=0x7fffff){lock_leave142(&exception_lock142);last8(8);return 0;}
 /* Sequence is independent of the recycled storage slot. */
 unsigned generation=++exception_generation142;exception_handlers142[at]=(exception_handler142){callback,generation,kind|(first?4u:0u),1};lock_leave142(&exception_lock142);return (void*)(uintptr_t)(UINT64_C(0xa0000000)|((uint64_t)generation<<6)|at);
}
static unsigned remove_exception_handler142(void*handle,unsigned kind){
 uint64_t value=(uint64_t)(uintptr_t)handle;unsigned at=value&63,generation=(value&0x1fffffff)>>6;if((value&UINT64_C(0xffffffffe0000000))!=0xa0000000)return 0;
 lock_enter142(&exception_lock142);exception_handler142*h=exception_handlers142+at;unsigned valid=h->live&&(h->kind&3)==kind&&h->generation==generation;if(valid)h->live=0;lock_leave142(&exception_lock142);return valid;
}
static void* MS f_AddVectoredExceptionHandler(unsigned first,uint64_t callback){return add_exception_handler142(first,callback,1);}
static void* MS f_AddVectoredContinueHandler(unsigned first,uint64_t callback){return add_exception_handler142(first,callback,2);}
static unsigned MS f_RemoveVectoredExceptionHandler(void*handle){return remove_exception_handler142(handle,1);}
static unsigned MS f_RemoveVectoredContinueHandler(void*handle){return remove_exception_handler142(handle,2);}
static uint64_t MS f_SetUnhandledExceptionFilter(uint64_t callback){if(callback&&sys8(W8_SYS_ACCESS,callback,1,5,0,0)){last8(87);return 0;}lock_enter142(&exception_lock142);uint64_t old=unhandled_filter142;unhandled_filter142=callback;lock_leave142(&exception_lock142);return old;}
static unsigned snapshot_exception_handlers142(unsigned kind,exception_handler142*out){
 unsigned count=0;lock_enter142(&exception_lock142);for(unsigned i=0;i<64;++i)if(exception_handlers142[i].live&&(exception_handlers142[i].kind&3)==kind)out[count++]=exception_handlers142[i];lock_leave142(&exception_lock142);
 for(unsigned i=1;i<count;++i){exception_handler142 value=out[i];unsigned j=i;while(j){exception_handler142 previous=out[j-1];unsigned before=(value.kind&4)?(!(previous.kind&4)||value.generation>previous.generation):(!(previous.kind&4)&&value.generation<previous.generation);if(!before)break;out[j]=previous;--j;}out[j]=value;}return count;
}
static NORETURN void exception_entry142(w8_exception_packet142*packet){
 exception_handler142 handlers[64];unsigned count=snapshot_exception_handlers142(1,handlers);int handled=0;
 for(unsigned i=0;i<count;++i){int result=((int(MS*)(w8_exception_pointers142*))(uintptr_t)handlers[i].callback)(&packet->pointers);if(result==-1){handled=1;break;}if(result!=0)break;}
 if(!handled){lock_enter142(&exception_lock142);uint64_t filter=unhandled_filter142;lock_leave142(&exception_lock142);if(filter&&((int(MS*)(w8_exception_pointers142*))(uintptr_t)filter)(&packet->pointers)==-1)handled=1;}
 if(handled&&!(packet->record.flags&1)){count=snapshot_exception_handlers142(2,handlers);for(unsigned i=0;i<count;++i)((int(MS*)(w8_exception_pointers142*))(uintptr_t)handlers[i].callback)(&packet->pointers);sys8(W8_SYS_EXCEPTION_RETURN,(uint64_t)(uintptr_t)packet,0,0,0,0);exit8(0xc0000028u);}
 print8("The Windows process ended after an unhandled native exception. Structured unwinding remains unavailable in this development profile.\n");exit8(packet->record.code);
}
