#include "path-core143.inc"
static unsigned path_user_string143(uint64_t source,char*out,unsigned cap){
 unsigned at=0;
 for(unsigned i=0;i<1024;++i){uint16_t units[2];unsigned count=1;
  if(user8(source+(uint64_t)i*2,units,2,0))return 998;
  if(!units[0]){out[at]=0;return 0;}
  if(units[0]>=0xd800&&units[0]<=0xdbff){if(++i==1024)return 206;if(user8(source+(uint64_t)i*2,units+1,2,0))return 998;count=2;}
  unsigned position=0;uint32_t cp;if(!decode_utf16_143(units,count,&position,&cp))return 1113;
  if(!encode_utf8_143(cp,out,cap-1,&at))return 206;
 }return 206;
}
static int64_t path_syscall143(uint64_t name,uint64_t directory,uint64_t output,uint64_t flags){
 if(flags&~UINT64_C(7))return -87;
 char text[2048],cwd[1024];w8_path_result143 result;
 unsigned error=path_user_string143(name,text,sizeof(text));if(error)return -(int64_t)error;
 path_context143 context={input8.user_root,input8.product_root,input8.windows_root,m6_volume()->entries,V6_ENTRIES};
 if(directory)error=path_user_string143(directory,cwd,sizeof(cwd));
 else{error=path_user_alias143(&context,cwd,sizeof(cwd));if(!error)error=path_append143(cwd,"\\Documents",sizeof(cwd));}
 if(error)return -(int64_t)error;
 error=path_policy143(&context,text,cwd,(unsigned)flags,&result);if(error)return -(int64_t)error;
 if(!(flags&2)&&!path8(result.native,0))return -5;
 return user8(output,&result,sizeof(result),1)?-998:0;
}
