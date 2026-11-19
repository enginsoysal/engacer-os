#define W8_USER
#include <engine/windows8.h>
#include <engine/storage/volume6.h>
void *memcpy(void*d,const void*s,size_t n){unsigned char*a=d;const unsigned char*b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void *memset(void*d,int c,size_t n){unsigned char*a=d;for(size_t i=0;i<n;++i)a[i]=(unsigned char)c;return d;}
void *memmove(void*d,const void*s,size_t n){unsigned char*a=d;const unsigned char*b=s;if(a<b){for(size_t i=0;i<n;++i)a[i]=b[i];}else while(n){--n;a[n]=b[n];}return d;}
int memcmp(const void*a,const void*b,size_t n){const unsigned char*x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]-y[i];return 0;}
#include "../../kernel/windows8/path-core143.inc"
__declspec(dllexport) unsigned normalize_host143(const char*input,const char*cwd,unsigned flags,
 const char*user,const char*product,const char*windows,const v6_entry*entries,unsigned count,w8_path_result143*out){
 path_context143 context={user,product,windows,entries,count};return path_policy143(&context,input,cwd,flags,out);
}
