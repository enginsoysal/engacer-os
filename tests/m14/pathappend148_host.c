#include <stdint.h>
#include <string.h>
#define MS
typedef uint16_t WCHAR;
static unsigned error;
static void last8(unsigned value){error=value;}
#include "../../user/windows8/pathappend148.inc"
__declspec(dllexport) int append148(WCHAR*path,const WCHAR*more){return f_PathAppendW(path,more);}
