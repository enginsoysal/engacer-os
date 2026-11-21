#ifndef ENGACER_PARGB148_H
#define ENGACER_PARGB148_H
#include <stdint.h>
/* Windows-compatible integer channel rounding, verified against owned GDI+ pixels. */
static inline unsigned pargb_pack148(unsigned channel,unsigned alpha){return(channel*alpha+127u)/255u;}
static inline unsigned pargb_unpack148(unsigned channel,unsigned alpha){if(!alpha)return 0;unsigned value=(channel*((255u<<16)/alpha))>>16;return value>255?255:value;}
#endif
