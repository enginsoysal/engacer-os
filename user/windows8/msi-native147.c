/* Native Win64 installer service adaptation, not a second operating system. */
#include "runtime.h"
#include <engine/product.h>
__declspec(dllimport) HANDLE GetProcessHeap(void);
__declspec(dllimport) void *HeapAlloc(HANDLE,unsigned,size_t);
__declspec(dllimport) int HeapFree(HANDLE,unsigned,void *);
__declspec(dllimport) size_t HeapSize(HANDLE,unsigned,const void *);
__declspec(dllimport) void ExitProcess(unsigned);
w8_mailbox *const job8=(void *)(uintptr_t)W8_MAILBOX;
uint64_t sys8(uint64_t n,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){
 register uint64_t r8 __asm__("r8")=e;register uint64_t r10 __asm__("r10")=d;
 __asm__ volatile("int $0x80":"+a"(n):"D"(a),"S"(b),"d"(c),"r"(r10),"r"(r8):"memory","rcx","r11");return n;
}
unsigned len8(const char *s){unsigned n=0;if(s)while(s[n])++n;return n;}
unsigned wlen8(const WCHAR *s){unsigned n=0;if(s)while(s[n])++n;return n;}
int equal8(const char *a,const char *b){unsigned i=0;while(a[i]&&a[i]==b[i])++i;return a[i]==b[i];}
int case8(const char *a,const char *b){while(*a&&*b){unsigned x=(uint8_t)*a++,y=(uint8_t)*b++;if(x>='A'&&x<='Z')x+=32;if(y>='A'&&y<='Z')y+=32;if(x!=y)return (int)x-(int)y;}return (uint8_t)*a-(uint8_t)*b;}
void copy8(char *out,const char *in,unsigned cap){if(!cap)return;unsigned i=0;while(i+1<cap&&in[i]){out[i]=in[i];++i;}out[i]=0;}
void append8(char *out,const char *in,unsigned cap){unsigned n=len8(out);if(n<cap)copy8(out+n,in,cap-n);}
void *memcpy(void *out,const void *in,size_t n){uint8_t *d=out;const uint8_t *s=in;for(size_t i=0;i<n;++i)d[i]=s[i];return out;}
void *memset(void *out,int value,size_t n){uint8_t *d=out;for(size_t i=0;i<n;++i)d[i]=(uint8_t)value;return out;}
void *memmove(void *out,const void *in,size_t n){uint8_t *d=out;const uint8_t *s=in;if(d<s)for(size_t i=0;i<n;++i)d[i]=s[i];else while(n){--n;d[n]=s[n];}return out;}
int memcmp(const void *a,const void *b,size_t n){const uint8_t *x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]-y[i];return 0;}
size_t strlen(const char *s){return len8(s);}
void *alloc8(size_t n){return HeapAlloc(GetProcessHeap(),0,n?n:1);}
void free8(void *p){if(p&&!HeapFree(GetProcessHeap(),0,p))ExitProcess(87);}
void *calloc8(size_t count,size_t bytes){if(bytes&&count>SIZE_MAX/bytes)return 0;void *p=alloc8(count*bytes);if(p)memset(p,0,count*bytes);return p;}
size_t allocation_size8(const void *p){return HeapSize(GetProcessHeap(),0,p);}
void *realloc8(void *old,size_t bytes){if(!old)return alloc8(bytes);if(!bytes){free8(old);return 0;}size_t before=allocation_size8(old);if(before==SIZE_MAX)return 0;void *next=alloc8(bytes);if(next){memcpy(next,old,before<bytes?before:bytes);free8(old);}return next;}
void print8(const char *text){unsigned n=len8(text);while(n){unsigned part=n>4096?4096:n;if((int64_t)sys8(W8_SYS_OUTPUT,(uint64_t)(uintptr_t)text,part,0,0,0)<0)ExitProcess(29);text+=part;n-=part;}}
void number8(uint64_t value){char text[24],reverse[24];unsigned n=0,at=0;do{reverse[n++]=(char)('0'+value%10);value/=10;}while(value);while(n)text[at++]=reverse[--n];text[at]=0;print8(text);}
NORETURN void exit8(unsigned code){ExitProcess(code);__builtin_unreachable();}
NORETURN void fail8(const char *text){copy8(job8->message,text,sizeof(job8->message));print8("\n" ENGINE_PRODUCT_NAME ": ");print8(text);print8("\n");exit8(1);}
int open8(const char *path,unsigned flags){return (int)sys8(W8_SYS_OPEN,(uint64_t)(uintptr_t)path,flags,0,0,0);}
int read8(int handle,void *out,unsigned n){unsigned done=0;while(n){unsigned part=n>4096?4096:n;int got=(int)sys8(W8_SYS_READ,(unsigned)handle,(uint64_t)(uintptr_t)out,part,0,0);if(got<0)return -1;done+=(unsigned)got;if((unsigned)got<part)break;out=(uint8_t *)out+got;n-=(unsigned)got;}return (int)done;}
int write8(int handle,const void *data,unsigned n){unsigned done=0;while(n){unsigned part=n>4096?4096:n;int got=(int)sys8(W8_SYS_WRITE,(unsigned)handle,(uint64_t)(uintptr_t)data,part,0,0);if(got<0)return -1;done+=(unsigned)got;if((unsigned)got!=part)break;data=(const uint8_t *)data+got;n-=(unsigned)got;}return (int)done;}
int64_t seek8(int handle,int64_t offset,unsigned method){return (int64_t)sys8(W8_SYS_SEEK,(unsigned)handle,(uint64_t)offset,method,0,0);}
int close8(int handle){return (int)sys8(W8_SYS_CLOSE,(unsigned)handle,0,0,0,0);}
int stat8(const char *path,w8_file_info *info){return (int)sys8(W8_SYS_STAT,(uint64_t)(uintptr_t)path,(uint64_t)(uintptr_t)info,0,0,0);}
unsigned load8(const char *path,void **out,unsigned maximum){w8_file_info info;if(stat8(path,&info)||info.kind!=1||info.size>maximum)return 0;void *data=alloc8((size_t)info.size+1);if(!data)return 0;int handle=open8(path,0);if(handle<0){free8(data);return 0;}int got=read8(handle,data,(unsigned)info.size);close8(handle);if(got<0||(unsigned)got!=info.size){free8(data);return 0;}((char *)data)[info.size]=0;*out=data;return (unsigned)info.size;}
int save8(const char *path,const void *data,unsigned n){int handle=open8(path,1);if(handle<0)return 1;if(write8(handle,data,n)!=(int)n){(void)sys8(W8_SYS_CLOSE,(unsigned)handle,1,0,0,0);return 1;}return close8(handle)!=0;}
int mkdir8(const char *path){return (int)sys8(W8_SYS_MKDIR,(uint64_t)(uintptr_t)path,0,0,0,0);}
int remove8(const char *path){return (int)sys8(W8_SYS_DELETE,(uint64_t)(uintptr_t)path,0,0,0,0);}
void progress8(unsigned percent,const char *text){job8->percent=percent;copy8(job8->message,text,sizeof(job8->message));sys8(W8_SYS_YIELD,0,0,0,0,0);}
