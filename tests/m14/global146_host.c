/* Deterministic allocator-failure checks only; not a native ABI/heap substitute. */
#include <stdint.h>
#include <stddef.h>
#define MS
typedef struct {unsigned depth;} lock142;
static unsigned error146,live146,at146;
static int fail146=-1;
_Alignas(16) static unsigned char arena146[131072];
typedef struct {void*p;size_t bytes;} allocation146;
static allocation146 allocations146[256];
static void last8(unsigned e){error146=e;}
static void lock_enter142(lock142*p){++p->depth;}
static void lock_leave142(lock142*p){--p->depth;}
static void *memset(void*p,int value,size_t bytes){unsigned char*out=p;for(size_t i=0;i<bytes;++i)out[i]=(unsigned char)value;return p;}
static void *alloc8(size_t bytes){
 if(fail146==0)return 0;if(fail146>0)--fail146;
 bytes=(bytes+15)&~(size_t)15;if(!bytes)bytes=16;if(bytes>sizeof(arena146)-at146)return 0;
 unsigned i=0;while(i<256&&allocations146[i].p)++i;if(i==256)return 0;
 void*p=arena146+at146;at146+=(unsigned)bytes;allocations146[i]=(allocation146){p,bytes};++live146;memset(p,0x9b,bytes);return p;
}
static void *calloc8(size_t n,size_t bytes){if(n&&bytes>SIZE_MAX/n)return 0;void*p=alloc8(n*bytes);if(p)memset(p,0,n*bytes);return p;}
static void free8(void*p){if(!p)return;for(unsigned i=0;i<256;++i)if(allocations146[i].p==p){allocations146[i].p=0;if(!--live146)at146=0;return;}live146=999;}
static size_t allocation_size8(const void*p){for(unsigned i=0;i<256;++i)if(allocations146[i].p==p)return allocations146[i].bytes;return SIZE_MAX;}
#include "../../user/windows8/global-memory146.inc"
#define CHECK146(yes,code) do{if(!(yes))return code;}while(0)
__declspec(dllexport) int verify146(void){
 CHECK146(!global_count146&&!live146,1);
 fail146=0;CHECK146(!f_GlobalAlloc(2,17)&&error146==8&&!global_objects146&&!live146,2);
 fail146=1;CHECK146(!f_GlobalAlloc(2,17)&&error146==8&&!global_objects146&&!live146,3);
 fail146=-1;uint64_t h=f_GlobalAlloc(0x42,17);CHECK146(h&&global_count146==1&&live146==2,4);
 unsigned char*p=f_GlobalLock(h);CHECK146(p&&f_GlobalSize(h)==32&&f_GlobalHandle(p)==h,5);
 for(unsigned i=0;i<32;++i)CHECK146(!p[i],6);p[0]=71;
 CHECK146(f_GlobalFlags(h)==1&&global_contains146(p)&&global_contains146((void*)(uintptr_t)h),7);
 CHECK146(!f_GlobalUnlock(h)&&error146==0,8);
 fail146=0;CHECK146(!f_GlobalAlloc(2,99)&&error146==8&&global_count146==1&&p[0]==71,9);
 CHECK146(f_GlobalFree(h+1)==h+1&&error146==6&&global_count146==1,10);
 CHECK146(!f_GlobalHandle(p+1)&&error146==6,11);
 CHECK146(!f_GlobalFree(h)&&!global_objects146&&!global_count146&&!live146,12);
 fail146=-1;uint64_t next=f_GlobalAlloc(2,17);CHECK146(next&&next!=h&&!f_GlobalLock(h)&&error146==6,13);
 CHECK146(!f_GlobalFree(next)&&!live146&&!global_lock146.depth,14);
 unsigned saved_generation=global_generation146;global_generation146=UINT32_MAX;
 CHECK146(!f_GlobalAlloc(2,1)&&error146==1816&&!global_objects146&&!live146,15);global_generation146=saved_generation;
 return 0;
}
