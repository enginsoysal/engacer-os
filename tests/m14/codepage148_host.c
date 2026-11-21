#include <assert.h>
#include <stdint.h>
#include <string.h>
#define MS
#define ENGINE_M14
typedef uint16_t WCHAR;
static unsigned error;
static void last8(unsigned value){error=value;}
static unsigned len8(const char*s){return(unsigned)strlen(s);}
static unsigned wlen8(const WCHAR*s){unsigned n=0;while(s[n])++n;return n;}
#include "../../user/windows8/codepage147.inc"
int main(void){
 assert(f_GetACP()==65001&&f_GetOEMCP()==65001);
 unsigned pages[]={0,1,3,1252,65001};
 for(unsigned byte=0;byte<256;++byte){
  error=123;assert(!f_IsDBCSLeadByte((uint8_t)byte)&&error==123);
  for(unsigned i=0;i<5;++i){error=123;assert(!f_IsDBCSLeadByteEx(pages[i],(uint8_t)byte)&&error==123);}
 }
 error=0;assert(!f_IsDBCSLeadByteEx(932,0x81)&&error==87);
 unsigned char info[20];assert(f_GetCPInfo(65001,info));
 for(unsigned i=6;i<18;++i)assert(!info[i]);
 return 0;
}
