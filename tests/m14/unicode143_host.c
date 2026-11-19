#include <stdint.h>
#include "../../kernel/windows8/unicode143.inc"
#define EXPORT __declspec(dllexport)
EXPORT uint32_t validate_fold143(const uint32_t*expected,uint32_t count){
 if(count!=0x110000)return UINT32_MAX;
 for(uint32_t cp=0;cp<count;++cp)if(fold143(cp)!=expected[cp])return cp+1;
 return 0;
}
EXPORT uint32_t validate_scalars143(void){
 for(uint32_t cp=0;cp<=0x10ffff;++cp){
  if(cp>=0xd800&&cp<=0xdfff)continue;
  char utf8[4];uint16_t utf16[2];unsigned n=0,m=0,at=0;uint32_t actual=0;
  if(!encode_utf8_143(cp,utf8,4,&n)||!decode_utf8_143(utf8,n,&at,&actual)||actual!=cp||at!=n)return 0x10000000|cp;
  at=0;if(!encode_utf16_143(cp,utf16,2,&m)||!decode_utf16_143(utf16,m,&at,&actual)||actual!=cp||at!=m)return 0x20000000|cp;
 }return 0;
}
EXPORT uint32_t decode8_host143(const char*text,unsigned bytes,unsigned*at,uint32_t*out){return decode_utf8_143(text,bytes,at,out);}
EXPORT uint32_t decode16_host143(const uint16_t*text,unsigned units,unsigned*at,uint32_t*out){return decode_utf16_143(text,units,at,out);}
EXPORT uint32_t encode8_host143(uint32_t cp,char*out,unsigned bytes,unsigned*at){return encode_utf8_143(cp,out,bytes,at);}
EXPORT uint32_t encode16_host143(uint32_t cp,uint16_t*out,unsigned units,unsigned*at){return encode_utf16_143(cp,out,units,at);}
EXPORT int equal_host143(const char*a,unsigned an,const char*b,unsigned bn){return equal_utf8_143(a,an,b,bn);}
