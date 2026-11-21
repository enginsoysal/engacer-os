/* Wide global atom API uses the kernel's session table, never a process cache. */
#include <engine/winatom147.h>
#include <engine/winui144.h>
static unsigned MS f_RegisterWindowMessageW(const WCHAR*name){int64_t result=(int64_t)sys8(W8_SYS_UI144,WUI_MESSAGE148,0,(uint64_t)(uintptr_t)name,0,0);if(result<0){last8((unsigned)-result);return 0;}return(unsigned)result;}
static unsigned atom_result147(int64_t result){if(result<0){last8((unsigned)-result);return 0;}return(unsigned)result;}
static unsigned MS f_GlobalFindAtomW(const WCHAR*name){return atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_FIND147,(uint64_t)(uintptr_t)name,0,0));}
static unsigned MS f_GlobalAddAtomW(const WCHAR*name){return atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_ADD147,(uint64_t)(uintptr_t)name,0,0));}
static unsigned MS f_GlobalDeleteAtom(uint16_t atom){(void)atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_DELETE147,atom,0,0));return 0;}
static unsigned MS f_GlobalGetAtomNameW(uint16_t atom,WCHAR*out,int capacity){if(capacity<0){last8(87);return 0;}watom_name147 request={(uint64_t)(uintptr_t)out,atom,(unsigned)capacity};return atom_result147((int64_t)sys8(W8_SYS_UI144,WUI_ATOM147,WATOM_NAME147,(uint64_t)(uintptr_t)&request,0,0));}
