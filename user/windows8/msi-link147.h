#ifndef ENGINE_MSI_LINK147_H
#define ENGINE_MSI_LINK147_H
#include <stddef.h>
#include <stdint.h>
#include "msi-text147.h"
/* MS-SHLLINK local LinkInfo and Unicode StringData, not a text shortcut stub. */
static inline void msil_u32147(uint8_t*p,uint32_t n){for(unsigned i=0;i<4;++i)p[i]=(uint8_t)(n>>(i*8));}
static inline unsigned msil_length147(const char*s,unsigned cap){unsigned n=0;if(s)while(n<cap&&s[n])++n;return n;}
static inline unsigned msil_string147(uint8_t*out,const uint16_t*text,unsigned units){out[0]=(uint8_t)units;out[1]=(uint8_t)(units>>8);for(unsigned i=0;i<units;++i){out[2+i*2]=(uint8_t)text[i];out[3+i*2]=(uint8_t)(text[i]>>8);}return 2+units*2;}
static inline unsigned msil_encode147(const char*target,const char*working,const char*arguments,const char*description,unsigned show,unsigned file_bytes,uint8_t*out,unsigned capacity,unsigned*bytes){
 if(!bytes)return 87;*bytes=0;if(!target||!working||!arguments||!description||!out||(show!=1&&show!=3&&show!=7))return 87;
 unsigned n=msil_length147(target,256);if(n<4||n==256||(target[0]!='C'&&target[0]!='c')||target[1]!=':'||target[2]!='\\')return 87;
 for(unsigned i=0;i<n;++i)if((uint8_t)target[i]<32||(uint8_t)target[i]>=127||target[i]=='/'||target[i]=='"'||target[i]=='*'||target[i]=='?'||target[i]=='%')return 50;
 uint16_t w[260],a[260],d[260];unsigned wn=260,an=260,dn=260;
 unsigned status=msit_outwide147(working,w,&wn);if(!status)status=msit_outwide147(arguments,a,&an);if(!status)status=msit_outwide147(description,d,&dn);if(status)return status;
 unsigned volume=24,base=36+volume,suffix=base+n+1,wide=suffix+1,wide_suffix=wide+(n+1)*2,info=wide_suffix+2;
 unsigned total=76+info+(wn?2+wn*2:0)+(an?2+an*2:0)+(dn?2+dn*2:0)+788+4;if(total>capacity)return 234;
 for(unsigned i=0;i<total;++i)out[i]=0;
 static const uint8_t clsid[16]={1,0x14,2,0,0,0,0,0,0xc0,0,0,0,0,0,0,0x46};
 msil_u32147(out,76);for(unsigned i=0;i<16;++i)out[4+i]=clsid[i];msil_u32147(out+20,0x02000282u|(dn?4u:0)|(wn?16u:0)|(an?32u:0));msil_u32147(out+24,32);msil_u32147(out+52,file_bytes);msil_u32147(out+60,show);
 uint8_t*link=out+76;msil_u32147(link,info);msil_u32147(link+4,36);msil_u32147(link+8,1);msil_u32147(link+12,36);msil_u32147(link+16,base);msil_u32147(link+24,suffix);msil_u32147(link+28,wide);msil_u32147(link+32,wide_suffix);
 msil_u32147(link+36,volume);msil_u32147(link+40,3);msil_u32147(link+48,16);const char*label="Engacer";for(unsigned i=0;i<7;++i)link[52+i]=(uint8_t)label[i];
 for(unsigned i=0;i<n;++i){link[base+i]=(uint8_t)target[i];link[wide+i*2]=(uint8_t)target[i];}
 unsigned at=76+info;if(dn)at+=msil_string147(out+at,d,dn);if(wn)at+=msil_string147(out+at,w,wn);if(an)at+=msil_string147(out+at,a,an);
 /* An explicit standard target block supports GetPath without an ItemIDList. */
 msil_u32147(out+at,788);msil_u32147(out+at+4,0xa0000001u);for(unsigned i=0;i<n;++i){out[at+8+i]=(uint8_t)target[i];out[at+268+i*2]=(uint8_t)target[i];}at+=788;*bytes=at+4;return 0;
}
#endif
