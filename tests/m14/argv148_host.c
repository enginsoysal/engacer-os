#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
typedef uint16_t WCHAR;
#define MS
#define W8_SYS_ACCESS 1
static uint64_t sys8(uint64_t n,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){(void)n;(void)a;(void)b;(void)c;(void)d;(void)e;return 0;}
static void last8(unsigned value){(void)value;}
static void*alloc8(size_t bytes){return malloc(bytes);}
static void free8(void*p){free(p);}
static unsigned f_GetModuleFileNameW(uint64_t module,WCHAR*out,unsigned cap){(void)module;(void)cap;static const WCHAR name[]={'p','r','o','b','e','.','e','x','e',0};memcpy(out,name,sizeof(name));return 9;}
#include "../../user/windows8/argv148.inc"
__declspec(dllexport) WCHAR**parse148(const WCHAR*input,int*count){return f_CommandLineToArgvW(input,count);}
__declspec(dllexport) void release148(void*pointer){free8(pointer);}
