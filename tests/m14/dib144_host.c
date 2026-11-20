#include "../../user/windows8/dib-core144.h"
__declspec(dllexport) unsigned info144(const uint8_t*data,unsigned bytes,unsigned icon,dib_info144*out){return dib_info_read144(data,bytes,icon,out);}
__declspec(dllexport) unsigned decode144(const uint8_t*data,unsigned bytes,unsigned icon,uint32_t*out,unsigned pixels){return dib_decode144(data,bytes,icon,out,pixels);}
