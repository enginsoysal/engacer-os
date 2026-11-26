#include "path-core143.inc"
#include "find-core143.inc"
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
#ifdef ENGINE_M14
 if(app_temp_enabled1410()){
  char temporary[256];app_temp_root1410(temporary);
  error=path_policy_with_temp1410(&context,text,cwd,(unsigned)flags,&result,temporary);
  if(!error&&!(flags&2)&&app_temp_grant1410(result.native)&&!find8(temporary)){
   const v6_entry *bundle=find8(input8.product_root);
   if(!bundle||bundle->kind!=2)return -3;
   error=protected_prepare143(temporary);
  }
 }else
#endif
 error=path_policy143(&context,text,cwd,(unsigned)flags,&result);
 if(error)return -(int64_t)error;
 if(!(flags&2)&&!path8(result.native,0))return -5;
 return user8(output,&result,sizeof(result),1)?-998:0;
}
static int64_t text_compare143(uint64_t first,uint64_t second){
 char a[1024],b[1024];unsigned error=path_user_string143(first,a,sizeof(a));if(!error)error=path_user_string143(second,b,sizeof(b));if(error)return -(int64_t)error;
 unsigned at=0,bt=0,an=length8(a),bn=length8(b);
 while(at<an&&bt<bn){uint32_t x,y;if(!decode_utf8_143(a,an,&at,&x)||!decode_utf8_143(b,bn,&bt,&y))return -1113;x=fold143(x);y=fold143(y);if(x!=y)return x<y?1:2;}
 return at==an&&bt==bn?0:at==an?1:2;
}
static int64_t text_find143(uint64_t pattern_address,uint64_t name_address){
 char pattern[256],name[256];char*outputs[]={pattern,name};uint64_t inputs[]={pattern_address,name_address};unsigned lengths[2]={0};
 for(unsigned item=0;item<2;++item){unsigned at=0;for(;at<256;++at){if(user8(inputs[item]+at,outputs[item]+at,1,0))return -998;if(!outputs[item][at])break;}if(at==256)return -206;lengths[item]=at;}
 unsigned matched=0,error=find_match_core143(pattern,lengths[0],name,lengths[1],&matched);return error?-(int64_t)error:matched;
}
