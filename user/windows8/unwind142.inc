/* Checked version-1 AMD64 virtual unwinding and C scope dispatch. */
typedef struct {uint64_t control_pc,image_base,function,establisher,target_ip,context,handler,handler_data,history;uint32_t scope_index,pad;} dispatcher_context142;
_Static_assert(sizeof(dispatcher_context142)==80,"Windows dispatcher context ABI");
typedef struct {module141*module;uint8_t*function;uint64_t pc,establisher,handler,data;unsigned handler_flags;} unwind_frame142;
typedef struct seh_state142 {struct seh_state142*previous;w8_context142*original;uint64_t target,frame,function;w8_context142 selected;unsigned chosen;} seh_state142;
static seh_state142*seh_states142[16];
static NORETURN void unwind_fail142(const char*message){print8(message);print8("\n");exit8(0xc0000027u);}
static void checked_unwind_read142(uint64_t address,void*out,unsigned bytes){if(!bytes||sys8(W8_SYS_ACCESS,address,bytes,1,0,0))unwind_fail142("The Windows unwind stack or metadata is unreadable.");memcpy(out,(void*)(uintptr_t)address,bytes);}
static uint64_t stack_word142(uint64_t address){uint64_t value;checked_unwind_read142(address,&value,8);return value;}
static unsigned nonvolatile142(unsigned reg){return reg==3||reg==5||reg==6||reg==7||reg>=12;}
static uint64_t*context_register142(w8_context142*c,unsigned reg){if(reg>15)unwind_fail142("The unwind register index is invalid.");return &c->rax+reg;}
static uint8_t*unwind_data142(module141*m,uint64_t rva,unsigned bytes){if(!range141(rva,bytes,m->size)||(bytes&&sys8(W8_SYS_ACCESS,(uint64_t)m->base+rva,bytes,1,0,0)))unwind_fail142("Windows unwind data is outside readable image pages.");return m->base+rva;}
static module141*unwind_image142(uint64_t pc){for(unsigned i=0;i<MODULES141;++i){module141*m=modules141+i;uint64_t base=(uint64_t)m->base;if(m->state==2&&pc>=base&&pc-base<m->size)return m;}return 0;}
static uint8_t*unwind_function142(module141*m,uint64_t pc){unsigned low=0,high=m->unwind_bytes/12;uint32_t offset=(uint32_t)(pc-(uint64_t)m->base);while(low<high){unsigned at=low+(high-low)/2;uint8_t*f=unwind_data142(m,(uint64_t)m->unwind_rva+at*12,12);if(offset<u32(f))high=at;else if(offset>=u32(f+4))low=at+1;else return f;}return 0;}
static unsigned epilog_unwind142(module141*m,uint64_t pc,w8_context142*c){
 uint64_t rva=pc-(uint64_t)m->base;if(!range141(rva,1,m->size))return 0;w8_context142 work=*c;unsigned bytes=0,pops=0;
 for(unsigned step=0;step<18;++step){if(!range141(rva+bytes,8,m->size))return 0;uint8_t*b=unwind_data142(m,rva+bytes,8);unsigned used=0;
  if(!step&&b[0]==0x48&&b[1]==0x83&&b[2]==0xc4){work.rsp+=(uint8_t)b[3];used=4;}
  else if(!step&&b[0]==0x48&&b[1]==0x81&&b[2]==0xc4){work.rsp+=u32(b+3);used=7;}
  else if(!step&&(b[0]==0x48||b[0]==0x49)&&b[1]==0x8d&&(b[2]&0x38)==0x20&&(b[2]&7)!=4&&(b[2]>>6==1||b[2]>>6==2)){unsigned reg=(b[2]&7)|((b[0]&1)?8:0);int64_t offset=b[2]>>6==1?(int8_t)b[3]:(int32_t)u32(b+3);work.rsp=*context_register142(&work,reg)+offset;used=b[2]>>6==1?4:7;}
  else if(b[0]>=0x58&&b[0]<=0x5f){unsigned reg=b[0]-0x58;if(!nonvolatile142(reg))return 0;*context_register142(&work,reg)=stack_word142(work.rsp);work.rsp+=8;used=1;++pops;}
  else if(b[0]==0x41&&b[1]>=0x58&&b[1]<=0x5f){unsigned reg=b[1]-0x58+8;if(!nonvolatile142(reg))return 0;*context_register142(&work,reg)=stack_word142(work.rsp);work.rsp+=8;used=2;++pops;}
  else if(b[0]==0xc3){work.rip=stack_word142(work.rsp);work.rsp+=8;*c=work;return 1;}
  else return 0;
  bytes+=used;if(bytes>64||pops>8)return 0;
 }return 0;
}
static void virtual_unwind142(w8_context142*c,uint64_t pc,unwind_frame142*out){
 memset(out,0,sizeof(*out));module141*m=unwind_image142(pc);if(!m)unwind_fail142("Unwinding through an unsupported compatibility-runtime frame is unavailable.");out->module=m;out->pc=pc;uint8_t*function=unwind_function142(m,pc);out->function=function;out->establisher=c->rsp;
 if(!function){c->rip=stack_word142(c->rsp);c->rsp+=8;return;}
 uint32_t data=u32(function+8);uint8_t*initial=unwind_data142(m,data,4);if((initial[0]&7)!=1)unwind_fail142("This Windows unwind metadata version is unsupported.");
 /* A caller walk names the pre-return call site; its epilog has not run. */
 if(pc==c->rip&&pc-(uint64_t)m->base-u32(function)>=initial[1]&&epilog_unwind142(m,pc,c))return;
 for(unsigned chain=0;chain<32;++chain){uint8_t*info=unwind_data142(m,data,4);unsigned version=info[0]&7,flags=info[0]>>3,count=info[2],frame=info[3]&15,frame_offset=info[3]>>4;if(version!=1||(flags&~7u)||((flags&4)&&(flags&3))||(frame&&!nonvolatile142(frame)))unwind_fail142("Windows unwind flags or frame register are invalid.");
  uint8_t*codes=unwind_data142(m,(uint64_t)data+4,((count+1)&~1u)*2+((flags&4)?12:(flags&3)?4:0));uint64_t control=pc-(uint64_t)m->base-u32(function);unsigned previous=256;
  if(frame){unsigned established=control>=info[1];for(unsigned i=0;i<count;){unsigned op=codes[i*2+1]&15,reg=codes[i*2+1]>>4,slots=op==1?(reg==0?2:reg==1?3:0):(op==4||op==8)?2:(op==5||op==9)?3:1;if(!slots||slots>count-i)unwind_fail142("Invalid frame-pointer unwind operands.");if(op==3&&codes[i*2]<=control)established=1;i+=slots;}if(established)out->establisher=*context_register142(c,frame)-frame_offset*16u;}
  for(unsigned i=0;i<count;){unsigned offset=codes[i*2],op=codes[i*2+1]&15,reg=codes[i*2+1]>>4,slots=1;if(offset>previous||offset>info[1])unwind_fail142("Windows unwind codes are not ordered within the prolog.");previous=offset;
   if(op==1)slots=reg==0?2:reg==1?3:0;else if(op==4||op==8)slots=2;else if(op==5||op==9)slots=3;else if(op!=0&&op!=2&&op!=3)slots=0;if(!slots||slots>count-i)unwind_fail142("The Windows unwind operation or operand is unsupported.");
   if(offset<=control){uint64_t operand=slots==2?u16(codes+(i+1)*2):slots==3?u32(codes+(i+1)*2):0;
    if(op==0){if(!nonvolatile142(reg))unwind_fail142("Invalid saved nonvolatile register.");*context_register142(c,reg)=stack_word142(c->rsp);c->rsp+=8;}
    else if(op==1)c->rsp+=reg?operand:operand*8;
    else if(op==2)c->rsp+=reg*8+8;
    else if(op==3){if(reg||!frame)unwind_fail142("Invalid frame establishment operation.");c->rsp=*context_register142(c,frame)-frame_offset*16u;}
    else if(op==4||op==5){if(!nonvolatile142(reg))unwind_fail142("Invalid nonvolatile save operation.");*context_register142(c,reg)=stack_word142(c->rsp+operand*(op==4?8:1));}
    else{if(reg<6)unwind_fail142("Invalid saved nonvolatile XMM register.");checked_unwind_read142(c->rsp+operand*(op==8?16:1),c->fx+160+reg*16,16);}
   }i+=slots;
  }
  unsigned padded=((count+1)&~1u)*2;if(flags&4){function=codes+padded;data=u32(function+8);continue;}
  if((flags&3)&&control>=info[1]){uint32_t handler=u32(codes+padded);if(!range141(handler,1,m->size)||sys8(W8_SYS_ACCESS,(uint64_t)m->base+handler,1,5,0,0))unwind_fail142("The Windows language handler is not executable.");out->handler_flags=flags&3;out->handler=(uint64_t)m->base+handler;out->data=(uint64_t)(codes+padded+4);}
  c->rip=stack_word142(c->rsp);c->rsp+=8;return;
 }unwind_fail142("The Windows chained unwind metadata is cyclic or too deep.");
}
static dispatcher_context142 dispatcher142(unwind_frame142*f,w8_context142*c,uint64_t target){return (dispatcher_context142){f->pc,(uint64_t)f->module->base,(uint64_t)f->function,f->establisher,target,(uint64_t)c,f->handler,f->data,0,0,0};}
int seh_c_specific142(w8_exception_record142*record,uint64_t frame,w8_context142*context,void*dispatcher){
 (void)context;dispatcher_context142*d=dispatcher;seh_state142*state=seh_states142[tid142()&255u];if(!state)unwind_fail142("The C scope handler has no owned dispatcher.");uint32_t count;checked_unwind_read142(d->handler_data,&count,4);if(count>4096)unwind_fail142("The C exception scope quota was exceeded.");uint64_t relative=d->control_pc-d->image_base;
 for(unsigned i=d->scope_index;i<count;++i){uint32_t row[4];checked_unwind_read142(d->handler_data+4+(uint64_t)i*16,row,16);module141*m=unwind_image142(d->control_pc);if(!m||row[0]>=row[1]||row[1]>m->size||row[2]>=m->size||row[3]>=m->size)unwind_fail142("The C exception scope table is invalid.");if(relative<row[0]||relative>=row[1])continue;
  if(record->flags&2){if(row[3])continue;uint64_t target=d->target_ip-d->image_base;if((record->flags&32)&&target>=row[0]&&target<row[1])continue;uint64_t callback=d->image_base+row[2];if(sys8(W8_SYS_ACCESS,callback,1,5,0,0))unwind_fail142("The C finally callback is not executable.");d->scope_index=i+1;((void(MS*)(unsigned,uint64_t))(uintptr_t)callback)(1,frame);continue;}
  if(!row[3])continue;int filter=1;if(row[2]!=1){uint64_t callback=d->image_base+row[2];if(sys8(W8_SYS_ACCESS,callback,1,5,0,0))unwind_fail142("The C exception filter is not executable.");w8_exception_pointers142 pointers={(uint64_t)record,(uint64_t)state->original};filter=((int(MS*)(w8_exception_pointers142*,uint64_t))(uintptr_t)callback)(&pointers,frame);}
  if(filter<0)return 0;if(filter>0){state->chosen=1;state->target=d->image_base+row[3];state->frame=frame;state->function=d->function;state->selected=*(w8_context142*)(uintptr_t)d->context;return 1;}
 }return 1;
}
unsigned pe8_exception_dispatch(w8_exception_record142*record,w8_context142*context){
 unsigned thread=tid142()&255u;if(thread>=16)return 0;seh_state142 state={.previous=seh_states142[thread],.original=context};seh_states142[thread]=&state;w8_context142 walk=*context;unsigned caller=0;
 for(unsigned depth=0;depth<256;++depth){if(!walk.rip)break;uint64_t pc=walk.rip-(caller?1:0);if(!unwind_image142(pc))break;w8_context142 before=walk;unwind_frame142 frame;virtual_unwind142(&walk,pc,&frame);if(frame.handler&&(frame.handler_flags&1)){dispatcher_context142 d=dispatcher142(&frame,&before,0);int result=((int(MS*)(w8_exception_record142*,uint64_t,w8_context142*,dispatcher_context142*))(uintptr_t)frame.handler)(record,frame.establisher,context,&d);if(!result){seh_states142[thread]=state.previous;return 1;}if(result!=1)unwind_fail142("The exception language-handler disposition is unsupported.");if(state.chosen)break;}if(walk.rsp<=before.rsp||walk.rsp-before.rsp>8*1024*1024)unwind_fail142("The Windows virtual unwind did not advance its stack.");caller=1;}
 if(!state.chosen){seh_states142[thread]=state.previous;return 0;}walk=*context;caller=0;unsigned old_flags=record->flags;
 for(unsigned depth=0;depth<256;++depth){uint64_t pc=walk.rip-(caller?1:0);w8_context142 before=walk;unwind_frame142 frame;virtual_unwind142(&walk,pc,&frame);unsigned target=frame.establisher==state.frame&&(uint64_t)frame.function==state.function;record->flags=old_flags|2|(target?32u:0u);
  if(frame.handler&&(frame.handler_flags&2)){dispatcher_context142 d=dispatcher142(&frame,&before,state.target);int result=((int(MS*)(w8_exception_record142*,uint64_t,w8_context142*,dispatcher_context142*))(uintptr_t)frame.handler)(record,frame.establisher,context,&d);if(result!=1)unwind_fail142("The unwind language-handler disposition is unsupported.");}
  if(target){*context=state.selected;context->rsp=state.frame;context->rip=state.target;context->rax=record->code;record->flags=old_flags;seh_states142[thread]=state.previous;return 1;}caller=1;
 }unwind_fail142("The selected Windows unwind target was not reached.");
}
