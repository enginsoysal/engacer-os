#include "../../user/windows8/msi-record147.h"
static msir_context147 context147;
__declspec(dllexport) void init147(msip_alloc147 a,msip_free147 f){msir_destroy147(&context147);context147.alloc=a;context147.release=f;}
__declspec(dllexport) unsigned create147(unsigned fields){return msir_create147(&context147,fields);}
__declspec(dllexport) unsigned close147(unsigned h){return msir_close147(&context147,h);}
__declspec(dllexport) unsigned clear147(unsigned h){return msir_clear147(&context147,h);}
__declspec(dllexport) unsigned set147(unsigned h,unsigned field,const char*s){return msir_string147(&context147,h,field,s);}
__declspec(dllexport) unsigned number147(unsigned h,unsigned field,int32_t v){return msir_integer147(&context147,h,field,v);}
__declspec(dllexport) int32_t getnumber147(unsigned h,unsigned field){return msir_number147(&context147,h,field);}
__declspec(dllexport) const char*get147(unsigned h,unsigned field){static char scratch[16];return msir_text147(&context147,h,field,scratch);}
__declspec(dllexport) unsigned bytes147(void){return context147.bytes;}
__declspec(dllexport) void destroy147(void){msir_destroy147(&context147);}
