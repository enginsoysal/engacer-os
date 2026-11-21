#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "../../include/engine/windows8.h"
typedef uint64_t HANDLE;
#define MS
static unsigned error148;
static uint64_t sys8(uint64_t n,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){(void)n;(void)a;(void)b;(void)c;(void)d;(void)e;return 0;}
static void last8(unsigned value){error148=value;}
static void*alloc8(size_t bytes){return malloc(bytes);}
static void free8(void*p){free(p);}
static size_t allocation_size8(const void*p){return p?64:SIZE_MAX;}
#include "../../user/windows8/sid148.inc"
__declspec(dllexport) int sid148(const uint8_t*authority,uint8_t count,const unsigned*values,void**out){return f_AllocateAndInitializeSid(authority,count,values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],out);}
__declspec(dllexport) unsigned size148(const void*p){return f_GetLengthSid(p);}
__declspec(dllexport) int valid148(const void*p){return f_IsValidSid(p);}
__declspec(dllexport) int equal148(const void*a,const void*b){return f_EqualSid(a,b);}
__declspec(dllexport) void release148(void*p){f_FreeSid(p);}
/* The Windows-reference driver exercises serialization only, not this shim. */
__declspec(dllexport) int membership148(HANDLE token,const void*p,int*out){return f_CheckTokenMembership(token,p,out);}
