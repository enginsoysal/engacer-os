#include "../../user/windows8/resource-core144.h"
__declspec(dllexport) unsigned lookup144(const uint8_t*data,unsigned bytes,unsigned directory,unsigned directory_bytes,const resource_key144*type,const resource_key144*name,unsigned language,unsigned exact,resource_result144*out){resource_image144 image={data,bytes,directory,directory_bytes};return resource_find144(&image,type,name,language,exact,out);}
__declspec(dllexport) unsigned string144(const uint8_t*data,unsigned bytes,unsigned slot,const uint16_t**text,unsigned*units){return resource_string144(data,bytes,slot,text,units);}
