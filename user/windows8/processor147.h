#ifndef ENGACER_PROCESSOR147_H
#define ENGACER_PROCESSOR147_H
/* Only instruction state supported by the current x87/FXSAVE kernel profile.
 * Hardware AVX/XSAVE bits alone cannot authorize unsaved extended state. */
static inline int processor_feature147(unsigned feature,uint32_t ecx,uint32_t edx,uint32_t extended_edx){
 switch(feature){
 case 2:return !!(edx&(1u<<8));
 case 3:return !!(edx&(1u<<23));
 case 6:return !!(edx&(1u<<25));
 case 8:return !!(edx&(1u<<4));
 case 9:return 1; /* This runtime executes in AMD64 long mode with PAE. */
 case 10:return !!(edx&(1u<<26));
 case 12:return !!(extended_edx&(1u<<20));
 case 13:return !!(ecx&1u);
 case 14:return !!(ecx&(1u<<13));
 case 36:return !!(ecx&(1u<<9));
 case 37:return !!(ecx&(1u<<19));
 case 38:return !!(ecx&(1u<<20));
 default:return 0; /* In particular: XSAVE, AVX and Windows fast-fail. */
 }
}
#endif
