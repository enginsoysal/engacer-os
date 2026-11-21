/* Shared pure version predicate. The caller supplies its explicit ABI profile;
 * successful comparisons do not advertise implementation of every OS feature. */
#ifndef ENGINE_VERSION_COMPARE148_H
#define ENGINE_VERSION_COMPARE148_H
#include <stdint.h>
static inline unsigned version_relation148(uint32_t a,uint32_t b,unsigned op){
 switch(op){case 1:return a==b;case 2:return a>b;case 3:return a>=b;case 4:return a<b;case 5:return a<=b;default:return 0;}
}
static inline unsigned version_compare148(const uint32_t current[8],const uint32_t requested[8],unsigned types,uint64_t mask){
 if(!types||(types&~255u))return 87;
 for(unsigned i=0;i<8;++i)if(types&(1u<<i)){
  unsigned op=(unsigned)(mask>>(3*i))&7u;
  if(i==6){if(op!=6&&op!=7)return 87;}
  else if(op<1||op>5)return 87;
 }
 for(unsigned i=2;i<8;++i)if(i!=4&&i!=5&&(types&(1u<<i))){
  unsigned op=(unsigned)(mask>>(3*i))&7u;
  if(i==6){if(op==6?((current[i]&requested[i])!=requested[i]):!(current[i]&requested[i]))return 1150;}
  else if(!version_relation148(current[i],requested[i],op))return 1150;
 }
 const unsigned order[]={1,0,5,4};unsigned inherited=0;
 for(unsigned at=0;at<4;++at){unsigned i=order[at];if(!(types&(1u<<i)))continue;
  unsigned op=(unsigned)(mask>>(3*i))&7u;
  if(inherited)op=inherited;
  if(op!=1)inherited=op;
  if(current[i]!=requested[i])return version_relation148(current[i],requested[i],op)?0:1150;
 }
 return (types&0x10u)&&(inherited==2||inherited==4)?1150:0;
}
#endif
