/* Bounded Unicode conversion and MSI output-buffer sizing, in UTF-16 units. */
#ifndef ENGINE_MSI_TEXT147_H
#define ENGINE_MSI_TEXT147_H
#include <stddef.h>
#include <stdint.h>
static inline unsigned msit_fromwide147(const uint16_t*s,char*out,unsigned cap){
 if(!s||!out||!cap)return 87;unsigned at=0;out[0]=0;
 for(unsigned i=0;i<=4096;++i){uint32_t c=s[i];if(!c){out[at]=0;return 0;}if(i==4096)return 1816;
  if(c>=0xd800&&c<=0xdbff){if(++i==4096)return 1113;uint32_t lo=s[i];if(lo<0xdc00||lo>0xdfff)return 1113;c=0x10000+((c-0xd800)<<10)+lo-0xdc00;}else if(c>=0xdc00&&c<=0xdfff)return 1113;
  unsigned n=c<128?1:c<2048?2:c<65536?3:4;if(n>=cap-at)return 1816;
  if(n==1)out[at++]=(char)c;else{out[at++]=(char)((n==2?0xc0:n==3?0xe0:0xf0)|(c>>(6*(n-1))));for(unsigned j=n-1;j;--j)out[at++]=(char)(0x80|((c>>(6*(j-1)))&63));}
 }return 1816;
}
static inline unsigned msit_next147(const char*s,unsigned length,unsigned*at,uint32_t*out){
 if(*at>=length)return 0;uint32_t c=(uint8_t)s[(*at)++],minimum=0;unsigned n=0;
 if(c<128){}else if(c>=0xc2&&c<=0xdf){c&=31;n=1;minimum=128;}else if(c>=0xe0&&c<=0xef){c&=15;n=2;minimum=2048;}else if(c>=0xf0&&c<=0xf4){c&=7;n=3;minimum=65536;}else return 0;
 if(n>length-*at)return 0;for(unsigned i=0;i<n;++i){unsigned v=(uint8_t)s[(*at)++];if((v&0xc0)!=0x80)return 0;c=(c<<6)|(v&63);}if(c<minimum||c>0x10ffff||(c>=0xd800&&c<=0xdfff))return 0;*out=c;return 1;
}
static inline unsigned msit_outwide147(const char*s,uint16_t*out,unsigned*capacity){
 if(!s||!capacity||!out)return 87;unsigned bytes=0;while(bytes<=4096&&s[bytes])++bytes;if(bytes>4096)return 1816;
 unsigned at=0,units=0;uint32_t cp;while(at<bytes){if(!msit_next147(s,bytes,&at,&cp))return 1113;units+=cp>65535?2:1;}
 unsigned cap=*capacity;*capacity=units;at=0;unsigned used=0;while(at<bytes){if(!msit_next147(s,bytes,&at,&cp))return 1113;unsigned n=cp>65535?2:1;if(used+n>=cap)break;if(n==1)out[used++]=(uint16_t)cp;else{cp-=0x10000;out[used++]=(uint16_t)(0xd800+(cp>>10));out[used++]=(uint16_t)(0xdc00+(cp&1023));}}
 if(cap)out[used]=0;return cap>units?0:234;
}
static inline unsigned msit_outansi147(const char*s,char*out,unsigned*capacity){if(!s||!out||!capacity)return 87;unsigned n=0;while(n<=4096&&s[n])++n;if(n>4096)return 1816;unsigned cap=*capacity;*capacity=n;if(cap){unsigned count=n<cap?n:cap-1;for(unsigned i=0;i<count;++i)out[i]=s[i];out[count]=0;}return cap>n?0:234;}
#endif
