#include <stddef.h>
int _fltused=0;
void*memcpy(void*out,const void*in,size_t bytes){volatile unsigned char*d=out;const volatile unsigned char*s=in;for(size_t i=0;i<bytes;++i)d[i]=s[i];return out;}
#include "../../user/windows8/transform-math148.h"
__declspec(dllexport) unsigned __attribute__((target("sse2"))) rotate(float angle,float*out){return gp_rotation148(angle,out);}
__declspec(dllexport) unsigned combine(float*out,const float*operation,int order){return gp_matrix_combine148(out,operation,order);}
