/* Own list implementation; the observer interoperates with public host APIs. */
#include "../../user/windows8/runtime.h"
#include "../../user/windows8/processor147.h"
static int f_IsProcessorFeaturePresent(unsigned feature){uint32_t a,b,c,d;__asm__ volatile("cpuid":"=a"(a),"=b"(b),"=c"(c),"=d"(d):"a"(1u),"c"(0));return feature==14&&(c&(1u<<13));}
NORETURN void fail8(const char*text){(void)text;__builtin_trap();}
#include "../../user/windows8/slist147.inc"
__declspec(dllexport) void initialize147(void*head){f_InitializeSListHead(head);}
__declspec(dllexport) void*flush147(void*head){return f_InterlockedFlushSList(head);}
__declspec(dllexport) int feature147(unsigned feature,uint32_t c,uint32_t d,uint32_t e){return processor_feature147(feature,c,d,e);}
