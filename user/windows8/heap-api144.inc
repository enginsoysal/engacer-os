/* The process heap is the bounded native runtime allocator, not a second heap. */
#define PROCESS_HEAP144 UINT64_C(0x50000001)
static HANDLE MS f_GetProcessHeap(void){return PROCESS_HEAP144;}
static void *MS process_heap_alloc144(HANDLE heap,unsigned flags,size_t bytes){if(heap!=PROCESS_HEAP144||(flags&~9u)){last8(heap!=PROCESS_HEAP144?6:50);return 0;}void*p=alloc8(bytes);if(!p){last8(8);return 0;}if(flags&8)memset(p,0,bytes);return p;}
static int MS process_heap_free144(HANDLE heap,unsigned flags,void*pointer){if(heap!=PROCESS_HEAP144||(flags&~1u)){last8(heap!=PROCESS_HEAP144?6:87);return 0;}if(!pointer)return 1;if(allocation_size8(pointer)==SIZE_MAX){last8(87);return 0;}free8(pointer);return 1;}
static size_t MS process_heap_size144(HANDLE heap,unsigned flags,const void*pointer){if(heap!=PROCESS_HEAP144||(flags&~1u)){last8(heap!=PROCESS_HEAP144?6:87);return SIZE_MAX;}size_t bytes=allocation_size8(pointer);if(bytes==SIZE_MAX)last8(87);return bytes;}
#ifdef ENGINE_M14
#include "private-heap148.inc"
#else
#define f_HeapAlloc process_heap_alloc144
#define f_HeapFree process_heap_free144
#define f_HeapSize process_heap_size144
#endif
static void*MS f_LocalAlloc(unsigned flags,size_t bytes){if(flags&~0x40u){last8(50);return 0;}void*p=flags&0x40?calloc8(1,bytes):alloc8(bytes);if(!p)last8(8);return p;}
static size_t MS f_wcslen(const WCHAR*text){return wlen8(text);}
static unsigned random144=1;static lock142 random_lock144;
static void MS f_srand(unsigned seed){lock_enter142(&random_lock144);random144=seed;lock_leave142(&random_lock144);}
static int MS f_rand(void){lock_enter142(&random_lock144);random144=random144*214013u+2531011u;unsigned result=(random144>>16)&32767;lock_leave142(&random_lock144);return(int)result;}
static unsigned MS f_lstrlenW(const WCHAR*text){return wlen8(text);}
static unsigned MS f_GetUserDefaultLangID(void){return 0x409;}
static unsigned MS f_GetSystemDefaultLangID(void){return 0x409;}
static void *MS f_CoTaskMemAlloc(size_t bytes){return alloc8(bytes);}
static void MS f_CoTaskMemFree(void*pointer){free8(pointer);}
static void *MS f_CoTaskMemRealloc(void*pointer,size_t bytes){return realloc8(pointer,bytes);}
