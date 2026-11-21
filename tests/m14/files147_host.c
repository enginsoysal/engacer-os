/* Real file engine, journal, stream gateway and V6; host syscall/handle adapter. */
#include "plan147_host.c"
#include "../../user/windows8/msi-files147.h"
#include "../../user/windows8/msi-shortcuts147.h"
#include "../../user/windows8/msi-text147.h"
#include <engine/storage/volume6.h>
typedef size_t (*size_callback147)(const void*);
static size_callback147 size_host147;
static v6_volume*volume147;
static w8_mailbox input8;
w8_mailbox*const job8=&input8;
static uint8_t io8[4096];
static msij147*journal147;static msil_plan147*links147;
static const void*source147;static unsigned source_bytes147;
static struct {char path[256];uint8_t*data;unsigned live,write,bytes,capacity,offset;} handles147[8];
void *realloc8(void*p,size_t n){if(!p)return alloc8(n);void*next=alloc8(n);if(next){size_t before=size_host147(p);memcpy(next,p,before<n?before:n);free8(p);}return next;}
void *memmove(void*d,const void*s,size_t n){uint8_t*a=d;const uint8_t*b=s;if(a<b)for(size_t i=0;i<n;++i)a[i]=b[i];else while(n){--n;a[n]=b[n];}return d;}
static unsigned length8(const char*s){return len8(s);}
static void copy_kernel147(char*out,const char*s,unsigned cap){copy8(out,s,cap);}
static unsigned prefix8(const char*p,const char*root){unsigned n=len8(root);return len8(p)>=n&&!memcmp(p,root,n)&&(!p[n]||p[n]=='/');}
static unsigned string8(uint64_t address,char*out,unsigned cap){if(!address)return 1;const char*p=(const void*)(uintptr_t)address;if(win_tx_length147(p,cap)==cap)return 1;copy8(out,p,cap);return 0;}
static unsigned user8(uint64_t address,void*data,unsigned n,unsigned write){if(write){if(address!=W8_MAILBOX+offsetof(w8_mailbox,windows_root)||n>256)return 1;memcpy(input8.windows_root,data,n);return 0;}if(!address)return 1;memcpy(data,(const void*)(uintptr_t)address,n);return 0;}
static const v6_entry*find8(const char*p){for(unsigned i=0;i<V6_ENTRIES;++i)if(volume147->entries[i].kind&&equal8(p,volume147->entries[i].path))return volume147->entries+i;return 0;}
static unsigned exact8(const char*p,uint64_t off,void*out,unsigned n){unsigned got=0;return v6_read(volume147,p,off,out,n,&got)||got!=n;}
static unsigned installer_authority147(void){return input8.command==W8_INSTALL;}
static v6_volume*m6_volume(void){return volume147;}
#define FILE_OBJECTS143 64u
static unsigned file_object_slot143(const char*p){(void)p;return FILE_OBJECTS143;}
static void metadata_path143(const char*p,char*out){(void)p;copy_kernel147(out,"/not-a-host-adapter-metadata-record",256);}
#define copy8 copy_kernel147
#include "../../kernel/windows8/transaction147.inc"
#undef copy8
static unsigned path8(const char*p,unsigned write){return prefix8(p,input8.product_root)||(!write&&(prefix8(p,input8.user_root)||prefix8(p,"/Data/Windows/Common/Programs")))||(write&&installer_user_grant147(p,0));}
#include "../../kernel/windows8/stream147.inc"
#include "../../kernel/windows8/path-core143.inc"
int stat8(const char*p,w8_file_info*out){if(!path8(p,0))return -1;const v6_entry*e=find8(p);if(!e)return -1;memset(out,0,sizeof(*out));out->kind=e->kind;out->size=e->size;return 0;}
int mkdir8(const char*p){unsigned status=v6_mkdir(volume147,p);return status&&status!=V6_EXISTS?-1:0;}
int open8(const char*p,unsigned flags){if(flags!=0&&flags!=2)return -1;const v6_entry*e=find8(p);if((flags==0&&(!e||e->kind!=1))||(flags==2&&e))return -1;unsigned i=0;while(i<8&&handles147[i].live)++i;if(i==8)return -1;memset(handles147+i,0,sizeof(handles147[i]));handles147[i].live=1;handles147[i].write=flags!=0;copy8(handles147[i].path,p,256);return (int)i;}
int read8(int h,void*out,unsigned n){if(h<0||h>=8||!handles147[h].live||handles147[h].write)return -1;unsigned got=0;if(v6_read(volume147,handles147[h].path,handles147[h].offset,out,n,&got))return -1;handles147[h].offset+=got;return (int)got;}
int write8(int h,const void*data,unsigned n){if(h<0||h>=8||!handles147[h].live||!handles147[h].write||n>WIN_TX_LIMIT147-handles147[h].bytes)return -1;unsigned total=handles147[h].bytes+n;if(total>handles147[h].capacity){void*p=realloc8(handles147[h].data,total);if(!p)return -1;handles147[h].data=p;handles147[h].capacity=total;}memcpy(handles147[h].data+handles147[h].bytes,data,n);handles147[h].bytes=total;return (int)n;}
static unsigned write_source147(void*context,uint64_t offset,void*out,unsigned n){memcpy(out,(uint8_t*)context+offset,n);return 0;}
static int close_handle147(unsigned h,unsigned commit){if(h>=8||!handles147[h].live)return -1;unsigned status=0;if(commit&&handles147[h].write)status=v6_put(volume147,handles147[h].path,handles147[h].bytes,write_source147,handles147[h].data);if(handles147[h].data)free8(handles147[h].data);memset(handles147+h,0,sizeof(handles147[h]));return status?-1:0;}
int close8(int h){return close_handle147((unsigned)h,1);}
unsigned load8(const char*p,void**out,unsigned cap){const v6_entry*e=find8(p);if(!e||e->kind!=1||e->size>cap)return 0;void*data=alloc8((size_t)e->size+1);if(!data)return 0;unsigned got=0;if(v6_read(volume147,p,0,data,(unsigned)e->size,&got)||got!=e->size){free8(data);return 0;}((uint8_t*)data)[got]=0;*out=data;return got;}
void progress8(unsigned percent,const char*text){input8.percent=percent;copy8(input8.message,text,sizeof(input8.message));}
uint64_t sys8(uint64_t call,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){
 if(call==W8_SYS_PATH143){char text[2048],cwd[1024];unsigned code=msit_fromwide147((const void*)(uintptr_t)a,text,sizeof(text));if(!code)code=msit_fromwide147((const void*)(uintptr_t)b,cwd,sizeof(cwd));if(code)return (uint64_t)-(int64_t)code;path_context143 context={input8.user_root,input8.product_root,input8.windows_root,volume147->entries,V6_ENTRIES};return (uint64_t)-(int64_t)path_policy143(&context,text,cwd,(unsigned)d,(void*)(uintptr_t)c);}
 if(call==W8_SYS_STREAM147)return (uint64_t)stream_call147(a,b,c,d,e);
 if(call==W8_SYS_ALIAS147)return (uint64_t)alias_set147(a,b,c,d,e);
 if(call==W8_SYS_INFO){if(a==3)return v6_capacity(volume147)-v6_used(volume147);if(a==5){unsigned free=0;for(unsigned i=0;i<V6_ENTRIES;++i)if(!volume147->entries[i].kind)++free;return free;}}
 if(call==W8_SYS_YIELD)return 0;
 if(call==W8_SYS_MKDIR){const char*path=(const void*)(uintptr_t)a;if(!path8(path,1)&&!installer_user_grant147(path,1))return UINT64_MAX;unsigned status=v6_mkdir(volume147,(const char*)(uintptr_t)a);return status&&!(status==V6_EXISTS&&!b)?UINT64_MAX:0;}
 if(call==W8_SYS_MOVE&&c==2)return (uint64_t)staging_move147((const char*)(uintptr_t)a,(const char*)(uintptr_t)b);
 if(call==W8_SYS_CLOSE)return (uint64_t)close_handle147((unsigned)a,!b);
 return UINT64_MAX;
}
__declspec(dllexport) void files_init147(v6_volume*v,size_callback147 size,const void*data,unsigned bytes){volume147=v;size_host147=size;source147=data;source_bytes147=bytes;memset(&input8,0,sizeof(input8));input8.command=W8_INSTALL;input8.process_id=147;copy8(input8.product_root,plan147->product_root,256);copy8(input8.windows_root,plan147->program_alias,256);copy8(input8.user_root,"/Users/Owner",256);memcpy(input8.source_sha147,plan147->source_sha256,32);}
__declspec(dllexport) unsigned stage147(void){journal147=msij_create147(plan147);if(!journal147)return 8;unsigned status=msij_properties147(journal147,&plan147->properties);if(!status)status=msil_prepare147(plan147,journal147,&links147);if(!status)status=msif_stage147(plan147,journal147,source147,source_bytes147);if(!status)status=msil_stage147(plan147,links147);return status;}
__declspec(dllexport) unsigned pending147(void){char path[256];copy8(path,plan147->product_root,256);append8(path,"/.EngacerMSI/transaction.bin",256);return msij_write147(journal147,path);}
__declspec(dllexport) unsigned promote147(void){unsigned status=msif_promote147(plan147);return status?status:msil_apply147(plan147,links147);}
__declspec(dllexport) unsigned verify147(void){return msif_verify147(journal147);}
__declspec(dllexport) unsigned keep147(void){return transaction_pending147()?transaction_keep147():0;}
__declspec(dllexport) const void*journal_data147(void){return journal147->data;}
__declspec(dllexport) unsigned journal_bytes147(void){return journal147->bytes;}
__declspec(dllexport) void files_close147(void){stream_release147();for(unsigned i=0;i<8;++i)if(handles147[i].live)(void)close_handle147(i,0);msij_close147(journal147);journal147=0;msil_close147(links147);links147=0;}

__declspec(dllexport) unsigned links_collision147(void){msij147*j=msij_create147(plan147);if(!j)return 8;msil_plan147*links=0;unsigned status=msil_prepare147(plan147,j,&links);msil_close147(links);msij_close147(j);return status;}
