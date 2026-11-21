/* Host registry adapter: every effect is confined to one owned HKCU fixture. */
#include "plan147_host.c"
#include "../../user/windows8/msi-registry147.h"
typedef int64_t (*registry_callback147)(unsigned,uint64_t);
typedef size_t (*size_callback147)(const void*);
static registry_callback147 registry_host147;static size_callback147 size_host147;
static unsigned free_entries147=1024;
static w8_mailbox mailbox147;
w8_mailbox*const job8=&mailbox147;
static msij147*journal147;
void *memmove(void*d,const void*s,size_t n){uint8_t*a=d;const uint8_t*b=s;if(a<b)for(size_t i=0;i<n;++i)a[i]=b[i];else while(n){--n;a[n]=b[n];}return d;}
void *realloc8(void*p,size_t n){if(!p)return alloc8(n);void*next=alloc8(n);if(next){size_t old=size_host147(p);memcpy(next,p,old<n?old:n);free8(p);}return next;}
uint64_t sys8(uint64_t op,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){(void)c;(void)d;(void)e;if(op==W8_SYS_REGISTRY143)return (uint64_t)registry_host147((unsigned)a,b);if(op==W8_SYS_INFO&&a==5)return free_entries147;return UINT64_MAX;}
int open8(const char*p,unsigned flags){(void)p;(void)flags;return -1;}
int write8(int h,const void*p,unsigned n){(void)h;(void)p;(void)n;return -1;}
int close8(int h){(void)h;return -1;}
unsigned load8(const char*p,void**out,unsigned cap){(void)p;(void)out;(void)cap;return 0;}
__declspec(dllexport) void registry_init147(registry_callback147 callback,size_callback147 size,unsigned entries){registry_host147=callback;size_host147=size;free_entries147=entries;copy8(mailbox147.user_root,"/Users/Owner",256);mailbox147.command=W8_INSTALL;}
__declspec(dllexport) unsigned registry_snapshot147(void){journal147=msij_create147(plan147);if(!journal147)return 8;unsigned code=msij_properties147(journal147,&plan147->properties);return code?code:msireg_snapshot147(plan147,journal147);}
__declspec(dllexport) unsigned registry_apply147(void){return msireg_apply147(journal147);}
__declspec(dllexport) unsigned registry_undo147(void){return msireg_undo147(journal147);}
__declspec(dllexport) unsigned registry_search147(void){return msireg_appsearch147(plan147);}
__declspec(dllexport) const void*registry_data147(void){return journal147->data;}
__declspec(dllexport) unsigned registry_bytes147(void){return journal147->bytes;}
__declspec(dllexport) void registry_close147(void){msij_close147(journal147);journal147=0;}
