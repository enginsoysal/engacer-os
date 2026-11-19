/* Lazy process-local Unicode environment. Kernel roots never come from these values. */
#define ENV_UNITS143 (W8_ENVIRONMENT_LIMIT143/2)
static lock142 environment_lock143;
static WCHAR*environment143;
static unsigned environment_units143,environment_capacity143;
static struct {void*pointer;unsigned kind;} environment_copies143[32];
static char*crt_environment_text143;static char*crt_environment143[65];
static unsigned environment_length143(const WCHAR*text,unsigned limit,unsigned*length){
 if(!text)return 87;for(unsigned i=0;i<limit;++i){unsigned unit=text[i];if(!unit){*length=i;return 0;}
  if(unit>=0xd800&&unit<=0xdbff){if(++i>=limit)return 206;if(text[i]<0xdc00||text[i]>0xdfff)return 1113;}else if(unit>=0xdc00&&unit<=0xdfff)return 1113;
 }return 206;
}
static int environment_compare143(const WCHAR*a,unsigned an,const WCHAR*b,unsigned bn){
 unsigned ascii=1;for(unsigned i=0;i<an;++i)if(a[i]>127)ascii=0;for(unsigned i=0;i<bn;++i)if(b[i]>127)ascii=0;
 if(ascii){unsigned n=an<bn?an:bn;for(unsigned i=0;i<n;++i){unsigned x=lower8(a[i]),y=lower8(b[i]);if(x!=y)return x<y?1:2;}return an==bn?0:an<bn?1:2;}
 WCHAR first[256],second[256];memcpy(first,a,an*2);first[an]=0;memcpy(second,b,bn*2);second[bn]=0;
 return (int)(int64_t)sys8(W8_SYS_TEXT143,1,(uint64_t)first,(uint64_t)second,0,0);
}
static int environment_find143(const WCHAR*name,unsigned name_units,unsigned*position,unsigned*entry_units,unsigned*count){
 unsigned at=0,entries=0;*entry_units=0;*position=0;
 while(environment143[at]){unsigned n=0;while(environment143[at+n]&&environment143[at+n]!='=')++n;unsigned bytes=wlen8(environment143+at)+1;
  int comparison=environment_compare143(name,name_units,environment143+at,n);if(comparison<0)return comparison;
  if(!comparison){*position=at;*entry_units=bytes;if(count)*count=entries;return 1;}if(comparison==1){*position=at;if(count)*count=entries;return 0;}at+=bytes;++entries;
 }*position=at;if(count)*count=entries;return 0;
}
static unsigned environment_reserve143(unsigned units){if(units>ENV_UNITS143)return 8;if(units<=environment_capacity143)return 0;unsigned cap=environment_capacity143?environment_capacity143:512;while(cap<units)cap*=2;
 WCHAR*replacement=realloc8(environment143,(size_t)cap*2);if(!replacement)return 8;environment143=replacement;environment_capacity143=cap;return 0;
}
static unsigned environment_set_locked143(const WCHAR*name,const WCHAR*value){
 unsigned nn=0,vn=0,error=environment_length143(name,256,&nn);if(error)return error;if(!nn)return 87;for(unsigned i=0;i<nn;++i)if(name[i]=='=')return 87;
 if(value&&(error=environment_length143(value,2048,&vn)))return error;
 WCHAR key[256],text[2048];memcpy(key,name,(nn+1)*2);if(value)memcpy(text,value,(vn+1)*2);
 unsigned position=0,old=0;int found=environment_find143(key,nn,&position,&old,0);if(found<0)return (unsigned)-found;if(!found&&!value)return 0;
 unsigned entries=0;for(unsigned i=0;environment143[i];i+=wlen8(environment143+i)+1)++entries;if(!found&&value&&entries==64)return 8;
 unsigned added=value?nn+1+vn+1:0,used=environment143[0]?environment_units143:1,needed=used-old+added;if(needed<2)needed=2;
 if((error=environment_reserve143(needed)))return error;
 memmove(environment143+position+added,environment143+position+old,(used-position-old)*2);
 if(value){memcpy(environment143+position,key,nn*2);environment143[position+nn]='=';memcpy(environment143+position+nn+1,text,(vn+1)*2);}
 environment_units143=needed;if(!environment143[0])environment143[1]=0;return 0;
}
static unsigned environment_ensure143(void){
 if(environment143)return 0;unsigned error=environment_reserve143(2);if(error)return error;environment143[0]=environment143[1]=0;environment_units143=2;
 if(job8->environment_bytes){
  if(job8->environment!=W8_ENVIRONMENT143||job8->environment_bytes>W8_ENVIRONMENT_LIMIT143||(job8->environment_bytes&1)){error=87;goto fail;}
  const WCHAR*source=(const WCHAR*)(uintptr_t)job8->environment;unsigned total=job8->environment_bytes/2,at=0,entries=0;
  while(at<total&&source[at]){unsigned n=0;while(at+n<total&&source[at+n]&&source[at+n]!='=')++n;if(!n||n>=256||at+n>=total||source[at+n]!='='||++entries>64){error=87;goto fail;}
   WCHAR key[256];memcpy(key,source+at,n*2);key[n]=0;unsigned value_units=0;error=environment_length143(source+at+n+1,total-at-n-1<2048?total-at-n-1:2048,&value_units);if(error)goto fail;
   error=environment_set_locked143(key,source+at+n+1);if(error)goto fail;at+=n+1+value_units+1;
  }
  if(total<2||at>=total||source[at]||source[total-1]||source[total-2]||(source[0]&&at!=total-1)){error=87;goto fail;}
  if(sys8(W8_SYS_UNMAP,job8->environment,(job8->environment_bytes+4095u)&~UINT64_C(4095),0,0,0)){error=87;goto fail;}job8->environment=0;job8->environment_bytes=0;return 0;
 }
 {char native[256],win[512];WCHAR profile[512],temporary[512],path[512],username[256];copy8(native,job8->user_root,256);winpath8(native,win,512);
  if(utf8_to16(win,profile,512)<0){error=1113;goto fail;}append8(win,"\\AppData\\Temp",512);if(utf8_to16(win,temporary,512)<0){error=1113;goto fail;}
  winpath8(job8->product_root,win,512);if(utf8_to16(win,path,512)<0){error=1113;goto fail;}const char*leaf=job8->user_root;for(unsigned i=0;job8->user_root[i];++i)if(job8->user_root[i]=='/')leaf=job8->user_root+i+1;if(utf8_to16(leaf,username,256)<0){error=1113;goto fail;}
  const WCHAR*names[]={u"USERPROFILE",u"USERNAME",u"TEMP",u"TMP",u"Path",u"PROCESSOR_ARCHITECTURE",u"NUMBER_OF_PROCESSORS"};
  const WCHAR*values[]={profile,username,temporary,temporary,path,u"AMD64",u"1"};
  for(unsigned i=0;i<7;++i)if((error=environment_set_locked143(names[i],values[i])))goto fail;
 }return 0;
 fail:free8(environment143);environment143=0;environment_units143=environment_capacity143=0;return error;
}
static unsigned MS f_GetEnvironmentVariableW(const WCHAR*name,WCHAR*out,unsigned capacity){
 unsigned n=0,error=environment_length143(name,256,&n);if(error||!n||(capacity&&!out)){last8(error?error:87);return 0;}
 lock_enter142(&environment_lock143);error=environment_ensure143();unsigned at=0,entry=0;int found=error?0:environment_find143(name,n,&at,&entry,0);
 if(error||found<=0){lock_leave142(&environment_lock143);last8(error?error:found<0?(unsigned)-found:203);return 0;}
 const WCHAR*value=environment143+at;while(*value!='=')++value;++value;unsigned length=wlen8(value);if(capacity>length)memcpy(out,value,(length+1)*2);lock_leave142(&environment_lock143);last8(0);return capacity>length?length:length+1;
}
static int MS f_SetEnvironmentVariableW(const WCHAR*name,const WCHAR*value){lock_enter142(&environment_lock143);unsigned error=environment_ensure143();if(!error)error=environment_set_locked143(name,value);lock_leave142(&environment_lock143);if(error){last8(error);return 0;}return 1;}
static unsigned MS f_GetEnvironmentVariableA(const char*name,char*out,unsigned capacity){
 if(!name||(capacity&&!out)||capacity>INT32_MAX){last8(87);return 0;}WCHAR key[256];int units=f_MultiByteToWideChar(65001,8,name,-1,key,256);if(!units)return 0;
 lock_enter142(&environment_lock143);unsigned error=environment_ensure143(),at=0,entry=0;int found=error?0:environment_find143(key,(unsigned)units-1,&at,&entry,0);
 if(error||found<=0){lock_leave142(&environment_lock143);last8(error?error:found<0?(unsigned)-found:203);return 0;}
 const WCHAR*value=environment143+at;while(*value!='=')++value;++value;int bytes=f_WideCharToMultiByte(65001,0,value,-1,0,0,0,0);if(bytes>0&&capacity>=(unsigned)bytes)f_WideCharToMultiByte(65001,0,value,-1,out,(int)capacity,0,0);
 lock_leave142(&environment_lock143);if(bytes<=0)return 0;last8(0);return capacity>=(unsigned)bytes?(unsigned)bytes-1:(unsigned)bytes;
}
static int MS f_SetEnvironmentVariableA(const char*name,const char*value){
 if(!name){last8(87);return 0;}WCHAR key[256],text[2048];if(!f_MultiByteToWideChar(65001,8,name,-1,key,256)||(value&&!f_MultiByteToWideChar(65001,8,value,-1,text,2048)))return 0;return f_SetEnvironmentVariableW(key,value?text:0);
}
static void*environment_copy_locked143(unsigned kind){
 unsigned error=environment_ensure143();if(error){last8(error);return 0;}unsigned slot=0;while(slot<32&&environment_copies143[slot].pointer)++slot;if(slot==32){last8(8);return 0;}
 unsigned bytes=environment_units143*2;if(kind==2){bytes=environment143[0]?1:2;for(unsigned at=0;environment143[at];at+=wlen8(environment143+at)+1){int n=f_WideCharToMultiByte(65001,0,environment143+at,-1,0,0,0,0);if(n<=0)return 0;bytes+=(unsigned)n;}}
 void*copy=alloc8(bytes);if(!copy){last8(8);return 0;}if(kind==1)memcpy(copy,environment143,bytes);else{unsigned offset=0;for(unsigned at=0;environment143[at];at+=wlen8(environment143+at)+1){int n=f_WideCharToMultiByte(65001,0,environment143+at,-1,(char*)copy+offset,(int)(bytes-offset),0,0);offset+=(unsigned)n;}((char*)copy)[offset]=0;if(!offset)((char*)copy)[1]=0;}
 environment_copies143[slot].pointer=copy;environment_copies143[slot].kind=kind;return copy;
}
static WCHAR*MS f_GetEnvironmentStringsW(void){lock_enter142(&environment_lock143);void*copy=environment_copy_locked143(1);lock_leave142(&environment_lock143);return copy;}
static char*MS f_GetEnvironmentStringsA(void){lock_enter142(&environment_lock143);void*copy=environment_copy_locked143(2);lock_leave142(&environment_lock143);return copy;}
static int environment_free_copy143(void*pointer,unsigned kind){lock_enter142(&environment_lock143);for(unsigned i=0;i<32;++i)if(environment_copies143[i].pointer==pointer&&pointer&&environment_copies143[i].kind==kind){environment_copies143[i].pointer=0;free8(pointer);lock_leave142(&environment_lock143);return 1;}lock_leave142(&environment_lock143);last8(87);return 0;}
static int MS f_FreeEnvironmentStringsW(WCHAR*pointer){return environment_free_copy143(pointer,1);}
static int MS f_FreeEnvironmentStringsA(char*pointer){return environment_free_copy143(pointer,2);}
static char**environment_crt143(void){
 lock_enter142(&environment_lock143);if(crt_environment_text143){lock_leave142(&environment_lock143);return crt_environment143;}
 char*copy=environment_copy_locked143(2);if(!copy){lock_leave142(&environment_lock143);return 0;}
 for(unsigned i=0;i<32;++i)if(environment_copies143[i].pointer==copy)environment_copies143[i].pointer=0;
 unsigned count=0,at=0;while(copy[at]&&count<64){crt_environment143[count++]=copy+at;at+=len8(copy+at)+1;}crt_environment143[count]=0;crt_environment_text143=copy;lock_leave142(&environment_lock143);return crt_environment143;
}
static WCHAR*environment_snapshot143(const void*explicit_block,unsigned flags,unsigned*bytes){
 if(!explicit_block){WCHAR*copy=f_GetEnvironmentStringsW();if(!copy)return 0;unsigned units=0;if(!copy[0])units=2;else{while(copy[units])units+=wlen8(copy+units)+1;++units;}*bytes=units*2;return copy;}
 WCHAR*copy=alloc8(W8_ENVIRONMENT_LIMIT143);if(!copy){last8(8);return 0;}unsigned used=0;
 if(flags&0x400){const WCHAR*source=explicit_block;for(;used<ENV_UNITS143;++used){copy[used]=source[used];if(used&& !copy[used]&&!copy[used-1]){++used;break;}}if(used==ENV_UNITS143&&copy[used-1]){free8(copy);last8(206);return 0;}}
 else{const char*source=explicit_block;unsigned at=0;while(source[at]){unsigned length=0;while(at+length<W8_ENVIRONMENT_LIMIT143&&source[at+length])++length;if(at+length==W8_ENVIRONMENT_LIMIT143){free8(copy);last8(206);return 0;}
   int n=f_MultiByteToWideChar(65001,8,source+at,(int)length+1,0,0);if(n<=0){free8(copy);return 0;}if((unsigned)n+used+1>ENV_UNITS143){free8(copy);last8(206);return 0;}
   if(!f_MultiByteToWideChar(65001,8,source+at,(int)length+1,copy+used,n)){free8(copy);return 0;}used+=(unsigned)n;at+=length+1;if(at>=W8_ENVIRONMENT_LIMIT143){free8(copy);last8(206);return 0;}}
  copy[used++]=0;if(used==1)copy[used++]=0;
 }
 if(used<2||used>ENV_UNITS143||copy[used-1]||copy[used-2]){free8(copy);last8(87);return 0;}*bytes=used*2;return copy;
}
static unsigned environment_expand_pass143(const WCHAR*source,unsigned count,WCHAR*out,unsigned*total){
 unsigned used=0;for(unsigned at=0;at<count;){const WCHAR*chosen=source+at;unsigned length=1,advance=1;
  if(source[at]=='%'){unsigned end=at+1;while(end<count&&source[end]!='%')++end;if(end<count&&end>at+1){unsigned nn=end-at-1;if(nn>255)return 206;WCHAR key[256];memcpy(key,source+at+1,nn*2);key[nn]=0;unsigned position=0,entry=0;int found=environment_find143(key,nn,&position,&entry,0);if(found<0)return (unsigned)-found;
    advance=end-at+1;if(found){chosen=environment143+position;while(*chosen!='=')++chosen;++chosen;length=wlen8(chosen);}else length=advance;}}
  if(length>ENV_UNITS143-1-used)return 206;if(out)memcpy(out+used,chosen,length*2);used+=length;at+=advance;
 }if(out)out[used]=0;*total=used+1;return 0;
}
static WCHAR*environment_expanded143(const WCHAR*source,unsigned*units){
 unsigned length=0,error=environment_length143(source,ENV_UNITS143,&length);if(error){last8(error);return 0;}lock_enter142(&environment_lock143);error=environment_ensure143();if(!error)error=environment_expand_pass143(source,length,0,units);
 WCHAR*result=error?0:alloc8((size_t)*units*2);if(!error&&!result)error=8;if(!error)error=environment_expand_pass143(source,length,result,units);lock_leave142(&environment_lock143);if(error){free8(result);last8(error);return 0;}return result;
}
static unsigned MS f_ExpandEnvironmentStringsW(const WCHAR*source,WCHAR*out,unsigned capacity){if(capacity&&!out){last8(87);return 0;}unsigned units=0;WCHAR*text=environment_expanded143(source,&units);if(!text)return 0;if(capacity>=units)memcpy(out,text,units*2);free8(text);return units;}
static unsigned MS f_ExpandEnvironmentStringsA(const char*source,char*out,unsigned capacity){
 if(!source||(capacity&&!out)||capacity>INT32_MAX){last8(87);return 0;}int needed=f_MultiByteToWideChar(65001,8,source,-1,0,0);if(needed<=0)return 0;if(needed>(int)ENV_UNITS143){last8(206);return 0;}
 WCHAR*input=alloc8((size_t)needed*2);if(!input){last8(8);return 0;}if(!f_MultiByteToWideChar(65001,8,source,-1,input,needed)){free8(input);return 0;}unsigned units=0;WCHAR*text=environment_expanded143(input,&units);free8(input);if(!text)return 0;
 int bytes=f_WideCharToMultiByte(65001,0,text,(int)units,0,0,0,0);if(bytes>0&&capacity>=(unsigned)bytes)f_WideCharToMultiByte(65001,0,text,(int)units,out,(int)capacity,0,0);free8(text);return bytes>0?(unsigned)bytes:0;
}
