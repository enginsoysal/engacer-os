#ifndef ENGACER_DIB_CORE144_H
#define ENGACER_DIB_CORE144_H
#include "resource-core144.h"
typedef struct {unsigned width,height,bits,stride,palette,pixels,mask,mask_stride,top,icon;} dib_info144;
static inline unsigned dib_info_read144(const uint8_t*data,unsigned bytes,unsigned icon,dib_info144*out){
 if(!data||!out||bytes<40||icon>1)return 87;unsigned header=resource_u32_144(data);if(header<40||header>bytes)return 193;
 int32_t w=(int32_t)resource_u32_144(data+4),h=(int32_t)resource_u32_144(data+8);unsigned bits=resource_u16_144(data+14),compression=resource_u32_144(data+16);if(w<=0||w>4096||!h||h==INT32_MIN||resource_u16_144(data+12)!=1)return 193;
 unsigned height=(unsigned)(h<0?-h:h);if(icon){if(height&1)return 193;height/=2;}if(!height||height>4096)return 193;
 if(compression||!(bits==1||bits==4||bits==8||bits==24||bits==32))return 50;
 unsigned colors=bits<=8?resource_u32_144(data+32):0;if(bits<=8){if(!colors)colors=1u<<bits;if(colors>(1u<<bits))return 193;}
 uint64_t offset=(uint64_t)header+colors*4,stride=(((uint64_t)(unsigned)w*bits+31)/32)*4,span=stride*height,mask_stride=(((uint64_t)(unsigned)w+31)/32)*4,mask=offset+span;
 if(!resource_span144(offset,span,bytes)||(icon&&!resource_span144(mask,mask_stride*height,bytes)))return 193;
 *out=(dib_info144){(unsigned)w,height,bits,(unsigned)stride,header,(unsigned)offset,(unsigned)mask,(unsigned)mask_stride,h<0,icon};return 0;
}
static inline unsigned dib_decode144(const uint8_t*data,unsigned bytes,unsigned icon,uint32_t*out,unsigned pixels){
 dib_info144 info;unsigned error=dib_info_read144(data,bytes,icon,&info);if(error)return error;if(!out||(uint64_t)info.width*info.height>pixels)return 122;
 unsigned colors=info.bits<=8?(info.pixels-info.palette)/4:0,has_alpha=0;
 if(info.bits==32&&icon)for(unsigned y=0;y<info.height&&!has_alpha;++y)for(unsigned x=0;x<info.width;++x)if(data[info.pixels+y*info.stride+x*4+3]){has_alpha=1;break;}
 for(unsigned y=0;y<info.height;++y){unsigned row=info.top?y:info.height-1-y;const uint8_t*source=data+info.pixels+row*info.stride;const uint8_t*mask=icon?data+info.mask+row*info.mask_stride:0;
  for(unsigned x=0;x<info.width;++x){uint32_t color;
   if(info.bits<=8){unsigned index=info.bits==8?source[x]:info.bits==4?(source[x/2]>>(x&1?0:4))&15:(source[x/8]>>(7-(x&7)))&1;if(index>=colors)return 193;const uint8_t*p=data+info.palette+index*4;color=0xff000000u|((uint32_t)p[2]<<16)|((uint32_t)p[1]<<8)|p[0];}
   else{const uint8_t*p=source+x*(info.bits/8);color=((uint32_t)p[2]<<16)|((uint32_t)p[1]<<8)|p[0];color|=(uint32_t)(info.bits==32&&has_alpha?p[3]:255)<<24;}
   if(mask&&(mask[x/8]&(0x80u>>(x&7))))color&=0xffffffu;out[y*info.width+x]=color;
  }
 }return 0;
}
#endif
