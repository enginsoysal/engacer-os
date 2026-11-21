#ifndef ENGACER_UI_PREMULTIPLIED148_H
#define ENGACER_UI_PREMULTIPLIED148_H
#include <stdint.h>
/* Windows-compatible integer channel rounding, verified against owned GDI+ pixels. */
static inline unsigned pargb_pack148(unsigned channel,unsigned alpha){return(channel*alpha+127u)/255u;}
static inline unsigned pargb_unpack148(unsigned channel,unsigned alpha){if(!alpha)return 0;unsigned value=(channel*((255u<<16)/alpha))>>16;return value>255?255:value;}
static inline uint32_t pargb_color148(uint32_t color){unsigned a=color>>24;return(a<<24)|(pargb_pack148((color>>16)&255,a)<<16)|(pargb_pack148((color>>8)&255,a)<<8)|pargb_pack148(color&255,a);}
/* Both operands are premultiplied. Constant source conversion belongs outside loops. */
static inline uint32_t pargb_over148(uint32_t source,uint32_t destination){unsigned inverse=255-(source>>24);uint32_t out=0;for(unsigned shift=0;shift<32;shift+=8){unsigned value=((source>>shift)&255)+((((destination>>shift)&255)*inverse+127)/255);if(value>255)value=255;out|=value<<shift;}return out;}
#endif
