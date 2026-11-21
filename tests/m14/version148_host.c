#include "../../user/windows8/version-mask148.h"
#include "../../user/windows8/version-compare148.h"
__declspec(dllexport) uint64_t condition148(uint64_t mask,uint32_t type,uint8_t condition){return version_mask148(mask,type,condition);}
__declspec(dllexport) unsigned compare148(const uint32_t*current,const uint32_t*requested,unsigned types,uint64_t mask){return version_compare148(current,requested,types,mask);}
