/* Pure bounded path policy; syscall copying and authorization stay in the kernel. */
#include "unicode143.inc"
typedef struct {const char*user,*product,*windows;const v6_entry*entries;unsigned count;} path_context143;

static unsigned path_length143(const char*s,unsigned cap){unsigned n=0;while(n<cap&&s[n])++n;return n;}
static unsigned path_copy143(char*out,const char*in,unsigned cap){unsigned n=path_length143(in,cap);if(n==cap)return 206;memcpy(out,in,n+1);return 0;}
static unsigned path_append143(char*out,const char*in,unsigned cap){unsigned n=path_length143(out,cap);if(n==cap)return 206;return path_copy143(out+n,in,cap-n);}
static unsigned path_prefix143(const char*path,const char*prefix,unsigned*consumed){
 unsigned a=0,b=0,an=path_length143(path,2048),bn=path_length143(prefix,512);
 while(b<bn){uint32_t x,y;if(!decode_utf8_143(path,an,&a,&x)||!decode_utf8_143(prefix,bn,&b,&y)||fold143(x)!=fold143(y))return 0;}
 if(path[a]&&path[a]!='\\')return 0;*consumed=a;return 1;
}
static unsigned path_user_alias143(const path_context143*ctx,char*out,unsigned cap){
 const char*name=ctx->user;for(unsigned i=0;ctx->user[i];++i)if(ctx->user[i]=='/')name=ctx->user+i+1;
 unsigned e=path_copy143(out,"C:\\Users\\",cap);return e?e:path_append143(out,name,cap);
}
static unsigned path_reserved143(const char*name,unsigned bytes){
 char base[16];unsigned n=0;while(n<bytes&&name[n]!='.'&&n+1<sizeof(base)){unsigned ch=(uint8_t)name[n];base[n]=(char)(ch>='a'&&ch<='z'?ch-32:ch);++n;}base[n]=0;
 const char*fixed[]={"CON","PRN","AUX","NUL","CLOCK$","CONIN$","CONOUT$"};
 for(unsigned i=0;i<sizeof(fixed)/sizeof(fixed[0]);++i){unsigned len=path_length143(fixed[i],16);if(n==len&&!memcmp(base,fixed[i],n))return 1;}
 if(n>=4&&(!memcmp(base,"COM",3)||!memcmp(base,"LPT",3))){if(n==4&&base[3]>='1'&&base[3]<='9')return 1;
  if(n==5&&(uint8_t)base[3]==0xc2&&((uint8_t)base[4]==0xb9||(uint8_t)base[4]==0xb2||(uint8_t)base[4]==0xb3))return 1;}
 return 0;
}
static unsigned path_normalize143(const char*input,const char*cwd,unsigned flags,char*out){
 char raw[2048];unsigned error=path_copy143(raw,input,sizeof(raw));if(error)return error;
 if(!raw[0])return flags&2?87:3;unsigned extended=0;
 if(!memcmp(raw,"\\\\?\\",4)){extended=1;unsigned n=path_length143(raw,sizeof(raw));memmove(raw,raw+4,n-3);
  if((raw[0]!='C'&&raw[0]!='c')||raw[1]!=':'||raw[2]!='\\')return 50;
  for(unsigned i=0;raw[i];++i)if(raw[i]=='/')return 123;
 }else{
  if((raw[0]=='\\'||raw[0]=='/')&&(raw[1]=='\\'||raw[1]=='/'))return 50;
  for(unsigned i=0;raw[i];++i)if(raw[i]=='/')raw[i]='\\';
 }
 unsigned absolute=raw[0]&&raw[1]==':'&&raw[2]=='\\';
 if(raw[0]&&raw[1]==':'&&raw[0]!='C'&&raw[0]!='c')return 15;
 if(!absolute){
  if(raw[0]=='\\'){unsigned n=path_length143(raw,sizeof(raw));if(n+2>=sizeof(raw))return 206;memmove(raw+2,raw,n+1);raw[0]='C';raw[1]=':';}
  else{if(!cwd||(cwd[0]!='C'&&cwd[0]!='c')||cwd[1]!=':'||cwd[2]!='\\')return 87;
   unsigned skip=raw[0]&&raw[1]==':'?2:0,n=path_length143(raw+skip,sizeof(raw)),base=path_length143(cwd,1024);
   unsigned slash=base&&cwd[base-1]!='\\';if(base==1024||base+slash+n>=sizeof(raw))return 206;
   memmove(raw+base+slash,raw+skip,n+1);memcpy(raw,cwd,base);if(slash)raw[base]='\\';}
 }
 if((raw[0]!='C'&&raw[0]!='c')||raw[1]!=':'||raw[2]!='\\')return 123;
 out[0]='C';out[1]=':';out[2]='\\';unsigned used=3,at=3;
 while(raw[at]){
  if(raw[at]=='\\'){if(extended)return 123;++at;continue;}
  unsigned begin=at;while(raw[at]&&raw[at]!='\\')++at;unsigned bytes=at-begin,last=at;while(raw[last]=='\\')++last;unsigned final=!raw[last];
  if(!extended){while(bytes&&raw[begin+bytes-1]==' ')--bytes;
   if(bytes==1&&raw[begin]=='.')continue;
   if(bytes==2&&raw[begin]=='.'&&raw[begin+1]=='.'){if(used>3){while(used>3&&out[used-1]!='\\')--used;if(used>3)--used;}continue;}
   while(bytes&&raw[begin+bytes-1]=='.')--bytes;
  }else if((bytes==1&&raw[begin]=='.')||(bytes==2&&raw[begin]=='.'&&raw[begin+1]=='.'))return 50;
  if(!bytes)return 123;if(bytes>63)return 206;unsigned pos=0;
  while(pos<bytes){uint32_t cp;if(!decode_utf8_143(raw+begin,bytes,&pos,&cp))return 1113;
   if(cp<32||cp=='<'||cp=='>'||cp=='"'||cp=='|')return 123;
   if(cp==':')return 50;if((cp=='*'||cp=='?')&&(!(flags&1)||!final))return 123;
  }
  if(!extended&&path_reserved143(raw+begin,bytes))return 50;
  unsigned slash=used>3;if(used+slash+bytes>=1024)return 206;if(slash)out[used++]='\\';memcpy(out+used,raw+begin,bytes);used+=bytes;
  if(extended&&raw[at]=='\\')++at;
 }
 out[used]=0;return 0;
}
static unsigned path_resolve143(const path_context143*ctx,const char*root,const char*tail,unsigned flags,char*out){
 unsigned error=path_copy143(out,root,256);if(error)return error;unsigned at=0,missing=0;
 while(tail[at]){if(tail[at]!='\\')return 123;++at;unsigned first=at;while(tail[at]&&tail[at]!='\\')++at;unsigned n=at-first;
  unsigned prefix=path_length143(out,256);if(prefix+n+1>=256)return 206;const v6_entry*match=0;unsigned matches=0;
  unsigned wildcard=0;for(unsigned i=0;i<n;++i)if(tail[first+i]=='*'||tail[first+i]=='?')wildcard=1;
  if(!missing&&!wildcard&&!((flags&4)&&!tail[at]))for(unsigned i=0;i<ctx->count;++i){const v6_entry*entry=ctx->entries+i;
   if(!entry->kind||memcmp(entry->path,out,prefix)||entry->path[prefix]!='/')continue;
   const char*name=entry->path+prefix+1;unsigned len=path_length143(name,256-prefix-1),direct=1;
   for(unsigned j=0;j<len;++j)if(name[j]=='/')direct=0;
   if(direct&&equal_utf8_143(name,len,tail+first,n)==1){match=entry;++matches;}
  }
  if(matches>1)return 123;
  if(match){if(tail[at]&&match->kind!=2)return 3;error=path_copy143(out,match->path,256);if(error)return error;}
  else{out[prefix++]='/';memcpy(out+prefix,tail+first,n);out[prefix+n]=0;missing=1;}
 }return 0;
}
static unsigned path_policy143(const path_context143*ctx,const char*input,const char*cwd,unsigned flags,w8_path_result143*out){
 if(flags&~7u)return 87;memset(out,0,sizeof(*out));char clean[1024];unsigned error=path_normalize143(input,cwd,flags,clean);if(error)return error;
 unsigned pos=0,wide=0,bytes=path_length143(clean,sizeof(clean));
 while(pos<bytes){uint32_t cp;if(!decode_utf8_143(clean,bytes,&pos,&cp))return 1113;if(!encode_utf16_143(cp,out->windows,511,&wide))return 206;}out->windows[wide]=0;
 if(flags&2)return 0;
 char user[512];if(path_user_alias143(ctx,user,sizeof(user)))return 206;
 unsigned skip=0;const char*root=0;
 if(path_prefix143(clean,ctx->windows,&skip))root=ctx->product;
 else if(path_prefix143(clean,user,&skip))root=ctx->user;
 if(!root)return 5;return path_resolve143(ctx,root,clean+skip,flags,out->native);
}
