#include "path143_host.c"
#include "../../kernel/windows8/find-core143.inc"
__declspec(dllexport) unsigned find_host143(const char*pattern,unsigned pattern_bytes,const char*name,unsigned name_bytes,unsigned*matched){return find_match_core143(pattern,pattern_bytes,name,name_bytes,matched);}
