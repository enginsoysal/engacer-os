/* Extend the existing independently Windows-readable link encoder with an icon.
 * The MSI encoder and its accepted binary output remain unchanged. */
#ifndef ENGINE_SHELL_LINK_FORMAT148_H
#define ENGINE_SHELL_LINK_FORMAT148_H
#include "msi-link147.h"
static inline unsigned shell_link_encode148(const char*target,const char*working,const char*arguments,const char*description,const char*icon,int icon_index,unsigned show,unsigned file_bytes,uint8_t*out,unsigned capacity,unsigned*bytes){
 if(!bytes)return 87;*bytes=0;unsigned length=0;
 unsigned status=msil_encode147(target,working,arguments,description,show,file_bytes,out,capacity,&length);if(status)return status;
 if(icon&&icon[0]){
  uint16_t wide[260];unsigned units=260;status=msit_outwide147(icon,wide,&units);if(status)return status;
  unsigned extra=2+units*2;if(extra>capacity-length)return 234;
  unsigned at=length-792;for(unsigned i=length;i>at;--i)out[i-1+extra]=out[i-1];msil_string147(out+at,wide,units);
  uint32_t flags=(uint32_t)out[20]|((uint32_t)out[21]<<8)|((uint32_t)out[22]<<16)|((uint32_t)out[23]<<24);msil_u32147(out+20,flags|64u);msil_u32147(out+56,(uint32_t)icon_index);length+=extra;
 }
 *bytes=length;return 0;
}
#endif
