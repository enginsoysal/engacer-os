/* Host-only I/O fault adapter around the unchanged production journal builder. */
#include "plan147_host.c"
#include "../../user/windows8/msi-journal147.h"
typedef size_t (*size_callback147)(const void*);
static size_callback147 size_host147;
static w8_mailbox job_host147;
w8_mailbox*const job8=&job_host147;
static msij147*journal_host147;
static uint8_t image_host147[WIN_TX_LIMIT147];
static unsigned image_bytes147,io_fault147,io_live147,io_exists147;
void *realloc8(void*old,size_t n){if(!old)return alloc8(n);if(!n){free8(old);return 0;}size_t before=size_host147(old);void*next=alloc8(n);if(next){memcpy(next,old,before<n?before:n);free8(old);}return next;}
int open8(const char*path,unsigned flags){(void)path;if(flags!=2||io_fault147==1||io_exists147||io_live147)return -1;io_live147=1;image_bytes147=0;return 7;}
int write8(int handle,const void*data,unsigned bytes){if(handle!=7||!io_live147||bytes>sizeof(image_host147))return -1;if(io_fault147==2)return (int)bytes-1;memcpy(image_host147,data,bytes);image_bytes147=bytes;return (int)bytes;}
int close8(int handle){if(handle!=7||!io_live147)return -1;io_live147=0;if(io_fault147==3)return -1;io_exists147=1;return 0;}
uint64_t sys8(uint64_t call,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){(void)c;(void)d;(void)e;if(call!=W8_SYS_CLOSE||a!=7||b!=1)return UINT64_MAX;io_live147=image_bytes147=0;return 0;}
unsigned load8(const char*path,void**out,unsigned cap){(void)path;if(!io_exists147||io_fault147==4||image_bytes147>cap)return 0;void*p=alloc8(image_bytes147+1);if(!p)return 0;memcpy(p,image_host147,image_bytes147);((uint8_t*)p)[image_bytes147]=0;if(io_fault147==5)((uint8_t*)p)[0]^=1;*out=p;return image_bytes147;}
__declspec(dllexport) void journal_init147(size_callback147 callback){size_host147=callback;copy8(job_host147.user_root,"/Users/Owner",256);}
__declspec(dllexport) unsigned journal_create147(void){journal_host147=msij_create147(plan147);return journal_host147!=0;}
__declspec(dllexport) unsigned journal_file147(const char*path,uint64_t bytes,const uint8_t*hash,unsigned flags){return msij_file147(journal_host147,WIN_TX_FILE147,path,bytes,hash,flags);}
__declspec(dllexport) unsigned journal_properties147(void){return msij_properties147(journal_host147,&plan147->properties);}
__declspec(dllexport) unsigned journal_seal147(void){return msij_seal147(journal_host147);}
__declspec(dllexport) const void*journal_data147(void){return journal_host147?journal_host147->data:0;}
__declspec(dllexport) unsigned journal_bytes147(void){return journal_host147?journal_host147->bytes:0;}
__declspec(dllexport) unsigned journal_write147(unsigned fault){io_fault147=fault;io_live147=io_exists147=image_bytes147=0;return msij_write147(journal_host147,"/owned-test/journal.bin");}
__declspec(dllexport) unsigned journal_read147(unsigned wrong_user){io_fault147=0;msij147*j=msij_read147("/owned-test/journal.bin",plan147->product_root,wrong_user?"/Users/Other":"/Users/Owner");unsigned good=j&&j->bytes==journal_host147->bytes&&!memcmp(j->data,journal_host147->data,j->bytes);msij_close147(j);return good;}
__declspec(dllexport) void journal_close147(void){msij_close147(journal_host147);journal_host147=0;}
