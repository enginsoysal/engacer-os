#ifndef ENGACER_RESOURCE_CORE144_H
#define ENGACER_RESOURCE_CORE144_H
#include <stdint.h>
#include <stddef.h>
typedef struct {uint32_t numeric,id,units;uint16_t text[128];} resource_key144;
typedef struct {const uint8_t*image;uint32_t image_bytes,directory,directory_bytes;} resource_image144;
typedef struct {uint32_t entry,data,bytes,language;} resource_result144;
static inline uint16_t resource_u16_144(const uint8_t*p){return(uint16_t)(p[0]|((uint16_t)p[1]<<8));}
static inline uint32_t resource_u32_144(const uint8_t*p){return(uint32_t)p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24);}
static inline unsigned resource_span144(uint64_t at,uint64_t bytes,uint64_t size){return at<=size&&bytes<=size-at;}
static inline const uint8_t *resource_at144(const resource_image144*i,uint32_t at,unsigned bytes){if(!resource_span144(i->directory,i->directory_bytes,i->image_bytes)||!resource_span144(at,bytes,i->directory_bytes))return 0;return i->image+i->directory+at;}
static inline unsigned resource_name144(const resource_image144*i,uint32_t encoded,const resource_key144*k){
 if(k->numeric)return !(encoded&0x80000000u)&&encoded==k->id;
 if(!(encoded&0x80000000u))return 0;uint32_t offset=encoded&0x7fffffffu;const uint8_t*s=resource_at144(i,offset,2);if(!s)return 0;unsigned n=resource_u16_144(s);s=resource_at144(i,offset,2u+(uint64_t)n*2);if(!s||n!=k->units)return 0;
 for(unsigned c=0;c<n;++c)if(resource_u16_144(s+2+c*2)!=k->text[c])return 0;return 1;
}
/* Three explicit levels prevent cyclic resource graphs from causing recursion. */
static inline unsigned resource_find144(const resource_image144*i,const resource_key144*type,const resource_key144*name,unsigned language,unsigned exact,resource_result144*out){
 if(!i||!i->image||!out||!type||!name||type->units>128||name->units>128||type->numeric>1||name->numeric>1||language>65535)return 87;
 if(!i->directory||!i->directory_bytes)return 1812;uint32_t table=0;
 for(unsigned level=0;level<3;++level){const uint8_t*h=resource_at144(i,table,16);if(!h)return 193;unsigned count=(unsigned)resource_u16_144(h+12)+resource_u16_144(h+14);if(count>4096||!resource_span144(table,(uint64_t)16+count*8,i->directory_bytes))return 193;
  const uint8_t*chosen=0;unsigned chosen_rank=4;
  for(unsigned n=0;n<count;++n){const uint8_t*e=h+16+n*8;uint32_t key=resource_u32_144(e);if(level<2){if(resource_name144(i,key,level?name:type)){chosen=e;break;}}
   else if(!(key&0xffff0000u)){unsigned rank=key==language?0:key==0?1:2;if(exact&&key!=language)continue;if(rank<chosen_rank){chosen=e;chosen_rank=rank;}}
  }
  if(!chosen)return level==0?1813:level==1?1814:1815;uint32_t child=resource_u32_144(chosen+4);
  if(level<2){if(!(child&0x80000000u))return 193;table=child&0x7fffffffu;}
  else{if(child&0x80000000u)return 193;const uint8_t*entry=resource_at144(i,child,16);if(!entry)return 193;uint32_t data=resource_u32_144(entry),bytes=resource_u32_144(entry+4);if(!resource_span144(data,bytes,i->image_bytes))return 193;*out=(resource_result144){i->directory+child,data,bytes,resource_u32_144(chosen)};return 0;}
 }return 193;
}
static inline unsigned resource_string144(const uint8_t*data,unsigned bytes,unsigned slot,const uint16_t**text,unsigned*units){if(!data||!text||!units||slot>=16)return 87;unsigned at=0;for(unsigned n=0;n<=slot;++n){if(!resource_span144(at,2,bytes))return 193;unsigned length=resource_u16_144(data+at);at+=2;if(!resource_span144(at,(uint64_t)length*2,bytes))return 193;if(n==slot){*text=(const uint16_t*)(const void*)(data+at);*units=length;return 0;}at+=length*2;}return 193;}
#endif
