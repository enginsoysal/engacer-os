#include <engine/wintxn147.h>
void *memcpy(void*d,const void*s,size_t n){uint8_t*a=d;const uint8_t*b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void *memset(void*d,int c,size_t n){uint8_t*a=d;for(size_t i=0;i<n;++i)a[i]=(uint8_t)c;return d;}
int memcmp(const void*a,const void*b,size_t n){const uint8_t*x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]<y[i]?-1:1;return 0;}
__declspec(dllexport) int validate147(const void*p,unsigned n){return win_tx_validate147(p,n);}
__declspec(dllexport) int digest147(const void*p,unsigned n,void*out){return win_tx_digest147(p,n,out);}

#define W8_USER
#include <engine/windows8.h>
#define ENGINE_M8
#include <engine/storage/volume6.h>
static w8_mailbox input8,mailbox147;
static const uint8_t*test_data147;static unsigned test_bytes147,test_mode147,test_fail147;
static v6_entry test_entry147;
static unsigned length8(const char*s){return win_tx_length147(s,4096);}
static void copy8(char*out,const char*in,unsigned n){unsigned i=0;if(!n)return;while(i+1<n&&in[i]){out[i]=in[i];++i;}out[i]=0;}
static const v6_entry*find8(const char*path){unsigned n=length8(path);const char*leaf=test_mode147==1?"/.EngacerMSI/transaction.bin":"/product.bin";unsigned len=length8(leaf);if(!test_mode147||n<len||memcmp(path+n-len,leaf,len+1))return 0;test_entry147.kind=1;test_entry147.size=test_bytes147;return &test_entry147;}
static unsigned exact8(const char*path,uint64_t off,void*out,unsigned n){(void)path;if(off+n>test_bytes147||off==test_fail147)return 1;memcpy(out,test_data147+off,n);return 0;}
static unsigned string8(uint64_t address,char*out,unsigned cap){const char*text=(const void*)(uintptr_t)address;if(!text||win_tx_length147(text,cap)==cap)return 1;copy8(out,text,cap);return 0;}
static unsigned user8(uint64_t address,void*data,unsigned n,unsigned write){if(!write||address!=W8_MAILBOX+offsetof(w8_mailbox,windows_root)||n>256)return 1;memcpy(mailbox147.windows_root,data,n);return 0;}
static unsigned prefix8(const char*p,const char*root){unsigned n=length8(root);return length8(p)>=n&&!memcmp(p,root,n)&&(!p[n]||p[n]=='/');}
static unsigned installer_authority147(void){return 1;}
#define FILE_OBJECTS143 64u
static unsigned file_object_slot143(const char*p){(void)p;return FILE_OBJECTS143;}
static void metadata_path143(const char*p,char*out){(void)p;copy8(out,"/never-a-test-record",256);}
static v6_volume*m6_volume(void){return 0;}
unsigned v6_rename(v6_volume*v,const char*a,const char*b,unsigned replace){(void)v;(void)a;(void)b;(void)replace;return 0;}
#include "../../kernel/windows8/transaction147.inc"
__declspec(dllexport) unsigned keep147(const void*p,unsigned n,unsigned mode,unsigned fail,const char*root,const char*user){memset(&input8,0,sizeof(input8));copy8(input8.product_root,root,256);copy8(input8.user_root,user,256);test_data147=p;test_bytes147=n;test_mode147=mode;test_fail147=fail;return transaction_keep147();}
__declspec(dllexport) int64_t alias147(unsigned command,const char*alias){memset(&input8,0,sizeof(input8));memset(&mailbox147,0,sizeof(mailbox147));input8.command=command;copy8(input8.product_root,"/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}",256);int64_t status=alias_set147((uint64_t)(uintptr_t)alias,0,0,0,0);if(!status&&(memcmp(input8.windows_root,mailbox147.windows_root,256)||!win_product_root147(input8.product_root)))return -999;return status;}

__declspec(dllexport) unsigned grant147(const char*path,unsigned ancestor){copy8(input8.product_root,"/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}",256);copy8(input8.user_root,"/Users/Owner",256);return installer_user_grant147(path,ancestor);}
__declspec(dllexport) int64_t move147(const char*source,const char*target,unsigned command){input8.command=command;test_mode147=0;copy8(input8.product_root,"/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}",256);return staging_move147(source,target);}
