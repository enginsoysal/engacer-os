/* Own API implementation with bounded data-only host file/heap adapters. */
#include "../../user/windows8/runtime.h"
__declspec(dllimport) void*GetProcessHeap(void);
__declspec(dllimport) void*HeapAlloc(void*,unsigned,size_t);
__declspec(dllimport) int HeapFree(void*,unsigned,void*);
static const uint8_t*input147;static uint64_t bytes147,offset147,live147,peak147;static unsigned error147,opens147;
static void last8(unsigned n){error147=n;}
void*memcpy(void*d,const void*s,size_t n){uint8_t*a=d;const uint8_t*b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void*memset(void*d,int value,size_t n){uint8_t*p=d;for(size_t i=0;i<n;++i)p[i]=(uint8_t)value;return d;}
unsigned len8(const char*s){unsigned n=0;while(s[n])++n;return n;}
void copy8(char*out,const char*in,unsigned cap){unsigned i=0;while(i+1<cap&&in[i]){out[i]=in[i];++i;}if(cap)out[i]=0;}
void*alloc8(size_t n){uint64_t*p=HeapAlloc(GetProcessHeap(),0,n+8);if(!p)return 0;*p=n;live147+=n;if(live147>peak147)peak147=live147;return p+1;}
void free8(void*p){if(p){uint64_t*base=(uint64_t*)p-1;live147-=*base;HeapFree(GetProcessHeap(),0,base);}}
int64_t seek8(int f,int64_t offset,unsigned method){if(f!=1||method||offset<0||(uint64_t)offset>bytes147)return -1;offset147=(uint64_t)offset;return offset;}
int read8(int f,void*out,unsigned n){if(f!=1||offset147>bytes147||n>bytes147-offset147)return -1;memcpy(out,input147+offset147,n);offset147+=n;return(int)n;}
int open8(const char*path,unsigned flags){(void)path;if(flags||opens147)return -1;opens147=1;offset147=0;return 1;}
int close8(int f){if(f!=1||!opens147)return 1;opens147=0;return 0;}
int stat8(const char*path,w8_file_info*out){(void)path;out->size=bytes147;out->kind=1;return 0;}
uint64_t sys8(uint64_t call,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){(void)a;(void)b;(void)c;(void)d;(void)e;return call==W8_SYS_ACCESS?0:UINT64_MAX;}
static int nativepath8(const WCHAR*name,char*out){if(!name||!name[0]){last8(87);return 0;}copy8(out,"input",256);return 1;}
static int f_WideCharToMultiByte(unsigned cp,unsigned flags,const WCHAR*in,int n,char*out,int cap,const char*def,int*used){(void)cp;(void)flags;(void)in;(void)n;(void)out;(void)cap;(void)def;(void)used;return 0;}
uint64_t pe8_module(const char*name){(void)name;return 0;}
const char*pe8_path(uint64_t h){(void)h;return 0;}
#include "../../user/windows8/version147.inc"
__declspec(dllexport) void source147(const void*data,unsigned bytes){input147=data;bytes147=bytes;offset147=0;error147=0;}
__declspec(dllexport) unsigned size147(unsigned*handle){return f_GetFileVersionInfoSizeW(L"input",handle);}
__declspec(dllexport) int info147(unsigned capacity,void*out){return f_GetFileVersionInfoW(L"input",0,capacity,out);}
__declspec(dllexport) int query147(const void*data,const WCHAR*path,void**out,unsigned*n){return f_VerQueryValueW(data,path,out,n);}
__declspec(dllexport) unsigned query_bound147(const void*data,unsigned bytes,const WCHAR*path,unsigned*offset,unsigned*n){return ver_query147(data,bytes,path,offset,n);}
__declspec(dllexport) unsigned error_get147(void){return error147;}
__declspec(dllexport) uint64_t live_get147(void){return live147;}
__declspec(dllexport) uint64_t peak_get147(void){return peak147;}
__declspec(dllexport) unsigned opens_get147(void){return opens147;}
