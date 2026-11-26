/* The i386 gate uses the actual stdcall argument block, not the Win64
 * syscall register convention. Only known immutable stub return PCs enter. */
static unsigned pe32_error1410(unsigned error,uint32_t result){
 spaces142[active_space142]->compat_error=error;
 return result;
}
static uint32_t pe32_write1410(const uint32_t *args){
 uint32_t output=args[3],done=0;
 if(!output||args[4]||args[2]>32u*1024u*1024u)return pe32_error1410(87,0);
 if(user8(output,&done,sizeof(done),1))return pe32_error1410(998,0);
 if(args[2]&&!user_range8(args[1],args[2]))return pe32_error1410(998,0);
 unsigned console=args[0]==2||args[0]==3;
 int file=console?-1:file_handle143(args[0]);
 if(!console&&file<0)return pe32_error1410(6,0);
 while(done<args[2]){
  unsigned bytes=args[2]-done;
  if(bytes>4096)bytes=4096;
  if(console){
   if(user8(args[1]+done,io8,bytes,0))return pe32_error1410(998,0);
   output8((const char*)io8,bytes);
  }else{
   int64_t written=file_write143((unsigned)file,args[1]+done,bytes);
   if(written<0)return pe32_error1410((unsigned)-written,0);
   bytes=(unsigned)written;
   if(!bytes)break;
  }
  done+=bytes;
  if(user8(output,&done,sizeof(done),1))return pe32_error1410(998,0);
 }
 return 1;
}
static uint32_t dispatch_pe321410(trap_frame *frame){
 if(frame->cs!=0x3b||!app_context_current1410(spaces142[active_space142])){
  finish8(0xc0000005u);return 0;
 }
 uint32_t api=(uint32_t)frame->rax-PE32_GATE_FIRST1410;
 if(api>=sizeof(pe32_kernel1410)/sizeof(*pe32_kernel1410)||
    (frame->rip!=PE32_THUNKS1410+api*16u+7u&&
     (api!=X86_EXIT1410||frame->rip!=PE32_EXIT_RETURN1410+10u))){
  finish8(0xc000001du);return 0;
 }
 uint32_t args[9]={0};
 unsigned count=pe32_kernel1410[api].arguments;
 if(frame->rsp>UINT32_MAX-4||count>sizeof(args)/sizeof(*args)||
    (count&&user8(frame->rsp+4,args,count*sizeof(*args),0)))return pe32_error1410(998,0);
 switch(api){
 case X86_EXIT1410:finish8(args[0]);return 0;
 case X86_GET_ERROR1410:return spaces142[active_space142]->compat_error;
 case X86_SET_ERROR1410:return pe32_error1410(args[0],0);
 case X86_PID1410:return input8.process_id;
 case X86_STD_HANDLE1410:{
  unsigned index=args[0]==(uint32_t)-10?0:args[0]==(uint32_t)-11?1:args[0]==(uint32_t)-12?2:3;
  if(index==3)return pe32_error1410(87,UINT32_MAX);
  return input8.startup_flags147&0x100?(uint32_t)input8.std_handles147[index]:index+1;
 }
 case X86_WRITE1410:return pe32_write1410(args);
 default:return pe32_error1410(50,0);
 }
}
