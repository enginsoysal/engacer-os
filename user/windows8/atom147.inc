/* Wide global atom API uses the kernel's session table, never a process cache. */
#include <engine/winatom147.h>
#include <engine/winui144.h>
static unsigned MS f_RegisterWindowMessageW(const WCHAR*name){int64_t result=(int64_t)sys8(W8_SYS_UI144,WUI_MESSAGE148,0,(uint64_t)(uintptr_t)name,0,0);if(result<0){last8((unsigned)-result);return 0;}return(unsigned)result;}
static unsigned MS f_RegisterWindowMessageA(const char*name){
 if(!name){last8(87);return 0;}unsigned bytes=0;while(bytes<1021){uint64_t address=(uint64_t)(uintptr_t)(name+bytes);unsigned chunk=4096-(unsigned)(address&4095);if(chunk>1021-bytes)chunk=1021-bytes;if(sys8(W8_SYS_ACCESS,address,chunk,1,0,0)){last8(998);return 0;}unsigned end=bytes+chunk;while(bytes<end&&name[bytes])++bytes;if(bytes<end)break;}
 if(bytes==1021){last8(87);return 0;}WCHAR wide[256];int units=f_MultiByteToWideChar(0,8,name,(int)bytes+1,wide,256);if(!units)return 0;return f_RegisterWindowMessageW(wide);
}
static unsigned atom_result147(int64_t result){if(result<0){last8((unsigned)-result);return 0;}return(unsigned)result;}
static unsigned MS f_GlobalFindAtomW(const WCHAR*name){return atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_FIND147,(uint64_t)(uintptr_t)name,0,0));}
static unsigned MS f_GlobalAddAtomW(const WCHAR*name){return atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_ADD147,(uint64_t)(uintptr_t)name,0,0));}
static unsigned MS f_GlobalDeleteAtom(uint16_t atom){(void)atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_DELETE147,atom,0,0));return 0;}
static unsigned MS f_GlobalGetAtomNameW(uint16_t atom,WCHAR*out,int capacity){if(capacity<0){last8(87);return 0;}watom_name147 request={(uint64_t)(uintptr_t)out,atom,(unsigned)capacity};return atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_NAME147,(uint64_t)(uintptr_t)&request,0,0));}
