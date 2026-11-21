/* Own production codec only; reference data is compared by the host observer. */
#include "../../user/windows8/runtime.h"
static unsigned error147;
static void last8(unsigned n){error147=n;}
unsigned len8(const char*s){unsigned n=0;if(s)while(s[n])++n;return n;}
unsigned wlen8(const WCHAR*s){unsigned n=0;if(s)while(s[n])++n;return n;}
void*memcpy(void*d,const void*s,size_t n){unsigned char*a=d;const unsigned char*b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
#include "../../user/windows8/codepage147.inc"
__declspec(dllexport) unsigned acp147(void){return f_GetACP();}
__declspec(dllexport) unsigned oem147(void){return f_GetOEMCP();}
__declspec(dllexport) int valid147(unsigned cp){return f_IsValidCodePage(cp);}
__declspec(dllexport) int info147(unsigned cp,void*out){return f_GetCPInfo(cp,out);}
__declspec(dllexport) unsigned error_get147(void){return error147;}
__declspec(dllexport) int mb147(unsigned cp,unsigned flags,const char*src,int n,WCHAR*out,int cap){return f_MultiByteToWideChar(cp,flags,src,n,out,cap);}
__declspec(dllexport) int wc147(unsigned cp,unsigned flags,const WCHAR*src,int n,char*out,int cap,const char*def,int*used){return f_WideCharToMultiByte(cp,flags,src,n,out,cap,def,used);}
