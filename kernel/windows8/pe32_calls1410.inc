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
static uint32_t pe32_create_file1410(const uint32_t *args){
 unsigned access=args[1],share=args[2],creation=args[4],flags=args[5];
 if(args[3]||args[6]||(flags&~0x040000a7u))return pe32_error1410(50,UINT32_MAX);
 if(access&~0xc0010180u||share&~7u)return pe32_error1410(87,UINT32_MAX);
 unsigned grant=((access&0x80000000u)?9u:0u)|((access&0x40000000u)?18u:0u)|
                ((access&0x10000u)?4u:0u)|((access&0x80u)?8u:0u)|((access&0x100u)?16u:0u);
 w8_path_result143 path;
 int64_t status=path_user_resolve1410(args[0],0,&path,0);
 if(status)return pe32_error1410((unsigned)-status,UINT32_MAX);
 unsigned existed=find8(path.native)!=0;
 status=file_open143(path.native,grant,share,creation,flags,0);
 if(status<0)return pe32_error1410((unsigned)-status,UINT32_MAX);
 return pe32_error1410(existed&&(creation==2||creation==4)?183:0,
                       (uint32_t)file_token143((unsigned)status));
}

static uint32_t pe32_read1410(const uint32_t *args){
 uint32_t output=args[3],done=0;
 if(!output||args[4]||args[2]>32u*1024u*1024u)return pe32_error1410(87,0);
 if(user8(output,&done,sizeof(done),1))return pe32_error1410(998,0);
 if(args[2]&&!user_range8(args[1],args[2]))return pe32_error1410(998,0);
 int file=file_handle143(args[0]);
 if(file<0)return pe32_error1410(6,0);
 while(done<args[2]){
  unsigned requested=args[2]-done;
  if(requested>4096)requested=4096;
  int64_t count=file_read143((unsigned)file,args[1]+done,requested);
  if(count<0)return pe32_error1410((unsigned)-count,0);
  done+=(uint32_t)count;
  if(user8(output,&done,sizeof(done),1))return pe32_error1410(998,0);
  if((unsigned)count<requested)break;
 }
 return 1;
}

static uint32_t pe32_registry1410(unsigned api,const uint32_t *args){
 w8_registry_request143 request={.root=args[0],.name=args[1]};
 w8_registry_result143 result={0};
 int64_t status;
 switch(api){
 case X86_REG_OPEN1410:case X86_REG_CREATE1410:{
  unsigned create=api==X86_REG_CREATE1410;
  uint32_t handle=args[create?7:4],disposition=create?args[8]:0;
  if(args[2]||(create&&(args[3]||args[4]||args[6]))||!handle)return 87;
  unsigned zero=0;
  if(user8(handle,&zero,sizeof(zero),1)||
     (disposition&&user8(disposition,&zero,sizeof(zero),1)))return 998;
  request.access=args[create?5:3];
  status=registry_request1410(create?2:1,request,&result);
  if(status)return (uint32_t)-status;
  uint32_t value=(uint32_t)result.handle;
  if(user8(handle,&value,sizeof(value),1)||
     (disposition&&user8(disposition,&result.disposition,sizeof(result.disposition),1))){
   (void)registry_close143(result.handle);return 998;
  }
  return 0;
 }
 case X86_REG_QUERY1410:
  if(args[2]||(args[4]&&!args[5]))return 87;
  if(args[5]&&user8(args[5],&request.bytes,sizeof(request.bytes),0))return 998;
  request.data=args[4];status=registry_request1410(4,request,&result);
  if(status&&status!=-234)return (uint32_t)-status;
  if((args[3]&&user8(args[3],&result.type,sizeof(result.type),1))||
     (args[5]&&user8(args[5],&result.bytes,sizeof(result.bytes),1)))return 998;
  return (uint32_t)-status;
 case X86_REG_SET1410:
  if(args[2])return 87;
  request.type=args[3];request.data=args[4];request.bytes=args[5];
  return (uint32_t)-registry_request1410(3,request,0);
 case X86_REG_CLOSE1410:return (uint32_t)-registry_request1410(5,request,0);
 default:return 50;
 }
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
 case X86_CREATE_FILE1410:return pe32_create_file1410(args);
 case X86_READ1410:return pe32_read1410(args);
 case X86_CLOSE_HANDLE1410:{
  int file=file_handle143(args[0]);
  if(file<0)return pe32_error1410(6,0);
  unsigned status=close8((unsigned)file,1);
  return status?pe32_error1410(status,0):1;
 }
 case X86_COMMAND1410:return PE32_COMMAND1410;
 case X86_REG_OPEN1410:case X86_REG_CREATE1410:case X86_REG_QUERY1410:
 case X86_REG_SET1410:case X86_REG_CLOSE1410:return pe32_registry1410(api,args);
 default:return pe32_error1410(50,0);
 }
}
