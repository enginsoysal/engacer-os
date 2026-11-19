/* Strict bounded codecs and the selected invariant identity profile. */
#include "unicode-table143.inc"

static inline uint32_t fold143(uint32_t value){
 unsigned low=0,high=sizeof(unicode_runs143)/sizeof(unicode_runs143[0]);
 while(low<high){unsigned middle=low+(high-low)/2;const unicode_run143*r=unicode_runs143+middle;
  if(value<r->first)high=middle;else if(value>r->last)low=middle+1;
  else return (value-r->first)%r->stride?value:(uint32_t)((int64_t)value+r->delta);
 }return value;
}
static inline unsigned decode_utf8_143(const char*text,unsigned bytes,unsigned*position,uint32_t*out){
 unsigned at=*position;if(at>=bytes)return 0;unsigned value=(uint8_t)text[at++],count=0,minimum=0;
 if(value<128){}else if(value>=0xc2&&value<=0xdf){value&=31;count=1;minimum=128;}
 else if(value>=0xe0&&value<=0xef){value&=15;count=2;minimum=2048;}
 else if(value>=0xf0&&value<=0xf4){value&=7;count=3;minimum=65536;}else return 0;
 if(count>bytes-at)return 0;
 for(unsigned i=0;i<count;++i){unsigned byte=(uint8_t)text[at++];if((byte&0xc0)!=0x80)return 0;value=(value<<6)|(byte&63);}
 if(value<minimum||value>0x10ffff||(value>=0xd800&&value<=0xdfff))return 0;
 *out=value;*position=at;return 1;
}
static inline unsigned encode_utf8_143(uint32_t value,char*out,unsigned bytes,unsigned*position){
 if(value>0x10ffff||(value>=0xd800&&value<=0xdfff))return 0;
 unsigned count=value<128?1:value<2048?2:value<65536?3:4,at=*position;
 if(at>bytes||count>bytes-at)return 0;
 if(count==1)out[at++]=(char)value;
 else{out[at++]=(char)((count==2?0xc0:count==3?0xe0:0xf0)|(value>>(6*(count-1))));
  for(unsigned i=count-1;i;--i)out[at++]=(char)(0x80|((value>>(6*(i-1)))&63));}
 *position=at;return 1;
}
static inline unsigned decode_utf16_143(const uint16_t*text,unsigned units,unsigned*position,uint32_t*out){
 unsigned at=*position;if(at>=units)return 0;uint32_t value=text[at++];
 if(value>=0xd800&&value<=0xdbff){if(at==units||text[at]<0xdc00||text[at]>0xdfff)return 0;
  value=0x10000+((value-0xd800)<<10)+(text[at++]-0xdc00);
 }else if(value>=0xdc00&&value<=0xdfff)return 0;
 *position=at;*out=value;return 1;
}
static inline unsigned encode_utf16_143(uint32_t value,uint16_t*out,unsigned units,unsigned*position){
 if(value>0x10ffff||(value>=0xd800&&value<=0xdfff))return 0;
 unsigned count=value>65535?2:1,at=*position;if(at>units||count>units-at)return 0;
 if(count==1)out[at++]=(uint16_t)value;
 else{value-=0x10000;out[at++]=(uint16_t)(0xd800+(value>>10));out[at++]=(uint16_t)(0xdc00+(value&1023));}
 *position=at;return 1;
}
static inline int equal_utf8_143(const char*a,unsigned a_bytes,const char*b,unsigned b_bytes){
 unsigned x=0,y=0;while(x<a_bytes&&y<b_bytes){uint32_t left,right;
  if(!decode_utf8_143(a,a_bytes,&x,&left)||!decode_utf8_143(b,b_bytes,&y,&right))return -1;
  if(fold143(left)!=fold143(right))return 0;
 }return x==a_bytes&&y==b_bytes;
}
