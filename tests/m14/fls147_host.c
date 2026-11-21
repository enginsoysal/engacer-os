/* Host-only own-code adapter; original DLLs never execute here. */
#include "../../user/windows8/runtime.h"
static void *(*allocate147)(size_t);
static void (*release147)(void*);
static unsigned row147,error147;
void *memset(void*d,int c,size_t n){unsigned char*p=d;for(size_t i=0;i<n;++i)p[i]=(unsigned char)c;return d;}
void *calloc8(size_t n,size_t size){if(size&&n>SIZE_MAX/size)return 0;void*p=allocate147(n*size);if(p)memset(p,0,n*size);return p;}
void free8(void*p){if(p)release147(p);}
unsigned tid142(void){return row147;}
void lock_enter142(lock142*l){while(__atomic_exchange_n(&l->owner,1,__ATOMIC_ACQUIRE)){} }
void lock_leave142(lock142*l){__atomic_store_n(&l->owner,0,__ATOMIC_RELEASE);}
static void last8(unsigned code){error147=code;}
NORETURN void fail8(const char*text){(void)text;__builtin_trap();}
#include "../../user/windows8/fls147.inc"
__declspec(dllexport) void init147(void*(*a)(size_t),void(*r)(void*)){allocate147=a;release147=r;}
__declspec(dllexport) void row_set147(unsigned row){row147=row;}
__declspec(dllexport) unsigned error_get147(void){return error147;}
__declspec(dllexport) unsigned allocate_fls147(uint64_t cb){return f_FlsAlloc(cb);}
__declspec(dllexport) int free_fls147(unsigned i){return f_FlsFree(i);}
__declspec(dllexport) uint64_t get_fls147(unsigned i){return f_FlsGetValue(i);}
__declspec(dllexport) int set_fls147(unsigned i,uint64_t v){return f_FlsSetValue(i,v);}
__declspec(dllexport) void exit_fls147(void){fls_thread_exit147();}
