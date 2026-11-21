/* Actual stream gateway and V6 storage; host-only syscall-copy/role adapter. */
#define W8_USER
#include <engine/windows8.h>
#include <engine/storage/volume6.h>
static v6_volume*volume_host147;
static w8_mailbox input8;
static unsigned authority147;
static uint8_t io8[4096];
void *memcpy(void*d,const void*s,size_t n){uint8_t*a=d;const uint8_t*b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
int memcmp(const void*a,const void*b,size_t n){const uint8_t*x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]<y[i]?-1:1;return 0;}
static unsigned length8(const char*s){unsigned n=0;while(s[n])++n;return n;}
static unsigned equal8(const char*a,const char*b){unsigned i=0;while(a[i]&&a[i]==b[i])++i;return a[i]==b[i];}
static unsigned string8(uint64_t address,char*out,unsigned cap){if(!address)return 1;const char*s=(const void*)(uintptr_t)address;unsigned n=0;while(n<cap&&s[n])++n;if(n==cap)return 1;memcpy(out,s,n+1);return 0;}
static unsigned user8(uint64_t address,void*out,unsigned n,unsigned write){if(!address||write)return 1;memcpy(out,(const void*)(uintptr_t)address,n);return 0;}
static v6_volume*m6_volume(void){return volume_host147;}
static unsigned installer_authority147(void){return authority147;}
static unsigned path8(const char*p,unsigned write){(void)write;unsigned n=length8(input8.product_root);return length8(p)>n&&!memcmp(p,input8.product_root,n)&&p[n]=='/';}
#define FILE_OBJECTS143 64u
static unsigned file_object_slot143(const char*p){(void)p;return FILE_OBJECTS143;}
static const v6_entry*find8(const char*p){for(unsigned i=0;i<V6_ENTRIES;++i)if(volume_host147->entries[i].kind&&equal8(p,volume_host147->entries[i].path))return volume_host147->entries+i;return 0;}
#include "../../kernel/windows8/stream147.inc"
__declspec(dllexport) void init147(v6_volume*v,unsigned command,unsigned pid,unsigned authority){volume_host147=v;input8.command=command;input8.process_id=pid;authority147=authority;const char*root="/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}";memcpy(input8.product_root,root,length8(root)+1);}
__declspec(dllexport) int64_t call147(uint64_t op,uint64_t address,uint64_t bytes){return stream_call147(op,address,bytes,0,0);}
__declspec(dllexport) void release147(void){stream_release147();}
__declspec(dllexport) unsigned owner147(void){return stream_owner147;}
