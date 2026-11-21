/* Pure condition-mask encoding, independently compared with original Windows.
 * Single documented type bits select three-bit fields; existing fields are ORed.
 * Keep the original marker bit and defined x64 shift behavior for other inputs. */
#ifndef ENGINE_VERSION_MASK148_H
#define ENGINE_VERSION_MASK148_H
#include <stdint.h>
static inline uint64_t version_mask148(uint64_t mask,uint32_t type,uint8_t condition){
 if(!type)return 0;
 unsigned bit=0;while(type>>1){type>>=1;++bit;}
 return mask|UINT64_C(0x8000000000000000)|((uint64_t)(condition&7u)<<((bit*3u)&63u));
}
#endif
