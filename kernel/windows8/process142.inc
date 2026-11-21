/* Retained lifetime objects are distinct from live private address spaces. */
static int new_process_object142(void){
 if(process_id142==UINT32_MAX)return -1;for(unsigned i=0;i<32;++i)if(!process_objects142[i].used){process_objects142[i]=(process_object142){.used=1,.pid=process_id142++,.slot=UINT32_MAX};return (int)i;}return -1;
}
static void drop_process_object142(unsigned object){process_object142*o=process_objects142+object;if(o->used&&!o->live&&!o->refs)memset(o,0,sizeof(*o));}
static int process_handle_slot142(uint64_t handle){
 unsigned slot=(unsigned)(handle&63);if((handle&W8_HANDLE_TAG_MASK)!=W8_PROCESS_TAG||slot>=32)return -1;process_handle142*h=spaces142[active_space142]->handles+slot;
 return h->live&&h->generation==((handle&UINT64_C(0x1fffffff))>>6)&&h->object<32&&process_objects142[h->object].used?(int)slot:-1;
}
static uint64_t new_process_handle142(unsigned object,unsigned kind){
 if(process_handle_generation142>=0x7fffffu)return 0;unsigned slot=0;while(slot<32&&spaces142[active_space142]->handles[slot].live)++slot;if(slot==32)return 0;
 process_handle142*h=spaces142[active_space142]->handles+slot;*h=(process_handle142){1,++process_handle_generation142,object,kind,0x1fffffu};++process_objects142[object].refs;
 return W8_PROCESS_TAG|((uint64_t)h->generation<<6)|slot;
}
static int64_t close_process_handle142(uint64_t handle){int slot=process_handle_slot142(handle);if(slot<0)return -1;process_handle142*h=spaces142[active_space142]->handles+slot;unsigned object=h->object;h->live=0;--process_objects142[object].refs;drop_process_object142(object);return 0;}
#ifdef ENGINE_M14
static int64_t open_process148(unsigned pid,unsigned access,unsigned inherit){
 if(!pid)return -87;if(inherit||access&~0x101400u)return -50;
 for(unsigned i=0;i<SPACES142;++i){private_space142*p=spaces142[i];if(!p)continue;process_object142*o=process_objects142+p->object;if(o->pid!=pid||!o->live)continue;if(!equal8(p->input.user_root,input8.user_root))return -5;
  uint64_t handle=new_process_handle142(p->object,1);if(!handle)return -8;int slot=process_handle_slot142(handle);spaces142[active_space142]->handles[slot].access=access;return (int64_t)handle;
 }return -87;
}
static int64_t process_image148(uint64_t handle,uint64_t output){
 unsigned object=spaces142[active_space142]->object;if(handle!=UINT64_MAX){int slot=process_handle_slot142(handle);if(slot<0)return -6;process_handle142*h=spaces142[active_space142]->handles+slot;if(h->kind!=1)return -6;if(!(h->access&0x1400u))return -5;object=h->object;}
 process_object142*o=process_objects142+object;if(!o->live||o->slot>=SPACES142||!spaces142[o->slot])return -6;private_space142*target=spaces142[o->slot];const char*path=target->exe_context148&&o->slot==0?"/System/Windows/runtime8.elf":target->input.source;
 return user8(output,(void*)path,length8(path)+1,1)?-998:0;
}
#endif
static void release_grants142(void){for(unsigned i=0;i<32;++i){process_handle142*h=spaces142[active_space142]->handles+i;if(h->live){unsigned object=h->object;h->live=0;if(object<32&&process_objects142[object].used&&process_objects142[object].refs){--process_objects142[object].refs;drop_process_object142(object);}}}}
static void wake_process_waiters142(void){for(unsigned p=0;p<SPACES142;++p)if(spaces142[p]){++spaces142[p]->wait_epoch;for(unsigned i=0;i<THREADS142;++i){thread142*t=spaces142[p]->threads+i;if(t->state==T142_PARK){t->state=T142_READY;t->frame.rax=0;}}}refresh_sync_waits142();}
static int64_t process_status142(uint64_t handle,uint64_t output,unsigned required){
 process_object142*o;unsigned kind;if(handle==UINT64_MAX){if(required==2)return -1;o=process_objects142+spaces142[active_space142]->object;kind=1;}
 else{int slot=process_handle_slot142(handle);if(slot<0)return -1;process_handle142*h=spaces142[active_space142]->handles+slot;kind=h->kind;if(required&&kind!=required)return -1;if(!(h->access&(required?0x1400u:0x100000u)))return -5;o=process_objects142+h->object;}
 unsigned done=kind==1?!o->live:o->primary_done,code=kind==1?o->code:o->primary_code;if(output&&user8(output,&code,4,1))return -1;return done?0:259;
}
static int choose_space142(void){for(unsigned n=0;n<SPACES142;++n){unsigned slot=(space_cursor142+n)%SPACES142;if(!spaces142[slot])continue;active_space142=slot;reap_threads142();if(choose_thread142()){space_cursor142=(slot+1)%SPACES142;return 1;}}active_space142=0;return 0;}
static void finalize_group142(void){
 if(w8_pending())return;active_space142=0;timer_needed142=0;timer_claim142(1,0);
 if(root_terminal142){if(root_waiting142)copy8(root_info142->message,root_end_message142[0]?root_end_message142:"The main program and its child processes have finished.",sizeof(root_info142->message));root_info142->state=root_terminal142;serial_text(root_info142->status?"M8_JOB_FAILED code=":"M8_JOB_DONE code=");serial_hex(root_info142->status);serial_text("\n");++root_info142->revision;}
}
static void end_space142(unsigned slot,unsigned code){
 active_space142=slot;unsigned object=spaces142[slot]->object;process_object142*o=process_objects142+object;unsigned pid=o->pid;
 if(!slot){root_terminal142=info8.state;copy8(root_end_message142,root_info142->message,sizeof(root_end_message142));}
 o->code=code;o->live=0;o->slot=UINT32_MAX;if(!o->primary_done){o->primary_done=1;o->primary_code=code;}
#ifdef ENGINE_M14
 if(slot&&code&&spaces142[0]&&spaces142[0]->exe_context148)spaces142[0]->exe_child_error148=code;
#endif
 release8();drop_process_object142(object);wake_process_waiters142();
 serial_text(slot?"M142_CHILD_EXIT pid=":"M142_ROOT_EXIT pid=");serial_hex(pid);serial_text(" code=");serial_hex(code);serial_text("\n");
 if(!slot&&w8_pending()){root_waiting142=1;root_info142->state=1;copy8(root_info142->message,"The main program ended; waiting for child processes.",sizeof(root_info142->message));++root_info142->revision;}
 active_space142=0;finalize_group142();
}
static int64_t resume_process_thread142(uint64_t handle){
 int slot=process_handle_slot142(handle);if(slot<0)return -1;process_handle142*h=spaces142[active_space142]->handles+slot;process_object142*o=process_objects142+h->object;
 if(h->kind!=2||!o->live||o->primary_done||o->slot>=SPACES142||!spaces142[o->slot])return -1;
 thread142*t=spaces142[o->slot]->threads;unsigned suspended=t->state==T142_SUSPENDED;if(suspended)t->state=T142_READY;return suspended;
}
static int64_t terminate_process142(uint64_t handle,unsigned code){
 if(handle==UINT64_MAX){finish8(code);return -1;}
 int h=process_handle_slot142(handle);if(h<0)return -1;process_handle142*cap=spaces142[active_space142]->handles+h;process_object142*o=process_objects142+cap->object;
 if(!(cap->access&1u))return -5;
 if(cap->kind!=1||!o->live||o->slot>=SPACES142||!spaces142[o->slot])return -1;
 unsigned caller=active_space142,target=o->slot;active_space142=target;info8.status=code;info8.state=code?3:2;copy8(info8.message,"The Windows process was terminated without application cleanup.",sizeof(info8.message));end_space142(target,code);active_space142=caller;return 0;
}
static unsigned child_image142(const char*source){
 const v6_entry*e=find8(source);if(!e||e->kind!=1)return 2;if(e->size<256||e->size>32*1024*1024)return 193;
 uint8_t dos[64],pe[24],optional[72];if(exact8(source,0,dos,64)||memcmp(dos,"MZ",2))return 193;uint32_t at;memcpy(&at,dos+60,4);
 if(at>e->size-96||exact8(source,at,pe,24)||memcmp(pe,"PE\0\0",4))return 193;uint16_t machine,flags,magic,subsystem,bytes;memcpy(&machine,pe+4,2);memcpy(&bytes,pe+20,2);memcpy(&flags,pe+22,2);
 if(machine!=0x8664||(flags&0x2000)||bytes<72||exact8(source,(uint64_t)at+24,optional,72))return 193;memcpy(&magic,optional,2);memcpy(&subsystem,optional+68,2);if(magic!=0x20b)return 193;return subsystem==3||subsystem==2?0:50;
}
static unsigned environment_validate143(const w8_process_request*request){
 unsigned bytes=request->environment_bytes;
#ifdef ENGINE_M14
 if(request->error_mode148&~0x8003u)return 87;
#else
 if(request->error_mode148)return 87;
#endif
 if(!bytes)return request->environment?87:0;
 if(!request->environment||bytes<4||bytes>W8_ENVIRONMENT_LIMIT143||(bytes&1))return 87;
 if(bytes==4){uint16_t empty[2];if(user8(request->environment,empty,4,0))return 998;if(!empty[0]&&!empty[1])return 0;}
 unsigned ended=0,value=0,name_units=0,value_units=0,entries=0,surrogate=0;
 for(unsigned offset=0;offset<bytes;offset+=2){uint16_t unit;if(user8(request->environment+offset,&unit,2,0))return 998;
  if(!unit){if(surrogate)return 1113;if(ended)return offset+2==bytes?0:87;if(!value||!name_units)return 87;if(++entries>64)return 8;ended=1;value=name_units=value_units=0;continue;}
  ended=0;if(surrogate){if(unit<0xdc00||unit>0xdfff)return 1113;surrogate=0;}else if(unit>=0xd800&&unit<=0xdbff)surrogate=1;else if(unit>=0xdc00&&unit<=0xdfff)return 1113;
  if(unit=='='&&!value){if(!name_units)return 87;value=1;continue;}
  if(value){if(++value_units>2047)return 206;}else if(++name_units>255)return 206;
 }return 87;
}
static unsigned environment_copy143(const w8_process_request*request,unsigned caller,unsigned target){
 if(!request->environment_bytes)return 0;unsigned bytes=request->environment_bytes;active_space142=target;
 if(map8(W8_ENVIRONMENT143,(bytes+4095u)&~UINT64_C(4095),3)){active_space142=caller;return 8;}
 for(unsigned offset=0;offset<bytes;){unsigned count=bytes-offset;if(count>4096)count=4096;active_space142=caller;
  if(user8(request->environment+offset,io8,count,0))return 998;active_space142=target;if(user8(W8_ENVIRONMENT143+offset,io8,count,1)){active_space142=caller;return 998;}offset+=count;}
 input8.environment=W8_ENVIRONMENT143;input8.environment_bytes=bytes;
 unsigned error=user8(W8_MAILBOX,&input8,sizeof(input8),1)?998:0;active_space142=caller;return error;
}
static int64_t create_process142(uint64_t request_address,uint64_t result_address){
 w8_process_request request;w8_process_result result={0};if(user8(request_address,&request,sizeof(request),0)||user8(result_address,&result,sizeof(result),1))return -87;
 if(!terminated142(request.source,sizeof(request.source))||!terminated142(request.command,sizeof(request.command))||!terminated142(request.directory,sizeof(request.directory))||(request.flags&~W8_CREATE_FLAGS147))return -87;
 if(!path8(request.source,0)||!path8(request.directory,0))return -5;const v6_entry*directory=find8(request.directory);if(!directory||directory->kind!=2)return -3;unsigned error=environment_validate143(&request);if(error)return -(int64_t)error;error=child_image142(request.source);if(error)return -(int64_t)error;
#ifdef ENGINE_M14
 if(spaces142[active_space142]->exe_context148&&!equal8(request.source,"/System/Windows/Tools/cmd.exe")&&!equal8(request.source,"/System/Windows/Tools/xcopy.exe")){error=exe_hash_file148(request.source,EXE148_SOURCE_BYTES,EXE148_SOURCE_SHA);if(error)return -(int64_t)error;}
#endif
 unsigned caller=active_space142,target=1,free_handles=0;while(target<SPACES142&&spaces142[target])++target;for(unsigned i=0;i<32;++i)if(!spaces142[caller]->handles[i].live)++free_handles;if(target==SPACES142||free_handles<2)return -8;
 int object=new_process_object142();if(object<0)return -8;
 const w8_mailbox*parent=&spaces142[caller]->input;
 unsigned status=start_space142(W8_RUN,request.source,parent->product_root,parent->user_root,"",target,(unsigned)object,&request);active_space142=caller;
 if(status){drop_process_object142((unsigned)object);return -8;}
 process_objects142[object].parent_pid=spaces142[caller]->input.process_id;
#ifdef ENGINE_M14
 spaces142[target]->install_authority147=spaces142[caller]->install_authority147;
 spaces142[target]->exe_context148=spaces142[caller]->exe_context148;
 if(spaces142[target]->exe_context148){const v6_entry*image=find8(request.source);spaces142[target]->image_pin148=(unsigned)(image-m6_volume()->entries)+1;spaces142[target]->input.reserved147=spaces142[caller]->input.reserved147;spaces142[target]->input.profile147=W8_PROFILE_EXE148;}
 error=pipe_inherit147(caller,target,&request);if(error){active_space142=target;info8.status=error;info8.state=3;end_space142(target,error);active_space142=caller;return -(int64_t)error;}
 spaces142[target]->input.startup_flags147=request.startup_flags147;memcpy(spaces142[target]->input.std_handles147,request.std_handles147,sizeof(request.std_handles147));copy8(spaces142[target]->input.windows_root,spaces142[caller]->input.windows_root,256);
 spaces142[target]->input.error_mode148=(request.flags&0x04000000u)?0:request.error_mode148;
 active_space142=target;error=user8(W8_MAILBOX,&input8,sizeof(input8),1)?998:0;active_space142=caller;if(error){active_space142=target;info8.status=error;info8.state=3;end_space142(target,error);active_space142=caller;return -(int64_t)error;}
#endif
 error=environment_copy143(&request,caller,target);if(error){active_space142=target;info8.status=error;info8.state=3;end_space142(target,error);active_space142=caller;return -(int64_t)error;}
 result.process=new_process_handle142((unsigned)object,1);result.thread=new_process_handle142((unsigned)object,2);
 if(!result.process||!result.thread){if(result.process)close_process_handle142(result.process);if(result.thread)close_process_handle142(result.thread);active_space142=target;info8.status=8;info8.state=3;end_space142(target,8);active_space142=caller;return -8;}
 result.process_id=process_objects142[object].pid;result.thread_id=process_objects142[object].primary_id;
 if(user8(result_address,&result,sizeof(result),1))return -87;return 0;
}
unsigned w8_start(unsigned command,const char*source,const char*root,const char*user,const char*arguments){
#ifdef ENGINE_M14
 v6_set_guard148(exe_volume_guard148);
#endif
 if(w8_pending())return V6_INVALID;active_space142=0;root_terminal142=root_waiting142=0;root_end_message142[0]=0;space_cursor142=0;memset(root_info142,0,sizeof(*root_info142));int object=new_process_object142();if(object<0)return V6_INVALID;
 unsigned status=start_space142(command,source,root,user,arguments,0,(unsigned)object,0);active_space142=0;if(status)drop_process_object142((unsigned)object);
#ifdef ENGINE_M14
 if(!status&&command==W8_REMOVE&&equal8(root,EXE148_ROOT)){status=exe_admit148(command,0);if(status)w8_cancel();}
#endif
 return status;
}
unsigned w8_start_reviewed147(unsigned command,const char*source,const char*root,const char*user,const char*arguments,const uint8_t digest[32]){
 if(command!=W8_INSTALL||!digest)return V6_INVALID;unsigned nonzero=0;for(unsigned i=0;i<32;++i)nonzero|=digest[i];if(!nonzero)return V6_INVALID;
 unsigned status=w8_start(command,source,root,user,arguments);if(status)return status;
 memcpy(input8.source_sha147,digest,32);
#ifdef ENGINE_M14
 if(equal8(root,EXE148_ROOT)){status=exe_admit148(command,digest);if(status){w8_cancel();return status;}}
#endif
 if(user8(W8_MAILBOX+offsetof(w8_mailbox,source_sha147),input8.source_sha147,32,1)){w8_cancel();return V6_INVALID;}return 0;
}
void w8_cancel(void){
 if(!w8_pending())return;unsigned cleanup_failed=0,kept=0,damaged=0;
 for(unsigned slot=0;slot<SPACES142;++slot)if(spaces142[slot]){active_space142=slot;cancel8=1;info8.state=3;info8.status=1223;unsigned cleanup=rollback8();if(cleanup==2)kept=1;else if(cleanup==3)damaged=1;else if(cleanup)cleanup_failed=1;end_space142(slot,1223);}
 active_space142=0;root_terminal142=3;root_info142->state=3;root_info142->status=1;copy8(root_info142->message,damaged?"Cancelled. A recovery record needs inspection. Files were kept.":kept?"Cancelled. Its transaction was kept; choose Recover / remove.":cleanup_failed?"Cancelled. Disk cleanup was interrupted; use Recover / remove.":"Operation cancelled. Uncommitted file writes were discarded.",sizeof(root_info142->message));++root_info142->revision;timer_needed142=0;timer_claim142(1,0);
}
