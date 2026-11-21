#ifndef ENGINE_WINBUNDLE147_H
#define ENGINE_WINBUNDLE147_H
#include <engine/base.h>
/* Borrowed slices remain owned by the reserved init boot module. */
typedef struct {const uint8_t *msi,*dll,*exe,*dll_hash,*exe_hash;unsigned msi_size,dll_size,exe_size;} winbundle147;
static inline uint32_t bundle32_147(const uint8_t*p){return (uint32_t)p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;}
static inline int winbundle_parse147(const void*data,size_t n,winbundle147*out){
 const uint8_t*p=data;winbundle147 v={0};
 if(!p||!out||n<96||n>4*1024*1024||memcmp(p+48,"ENGMSI81",8))return 0;
 uint32_t m=bundle32_147(p+56);if(bundle32_147(p+60)||!m||m>n-96)return 0;
 v.msi=p+96;v.msi_size=m;size_t off=96+(size_t)m;
 if(off!=n){
  if(n-off<88||memcmp(p+off,"ENGMS147",8)||bundle32_147(p+off+8)!=1||bundle32_147(p+off+12)!=2)return 0;
  v.dll_size=bundle32_147(p+off+16);v.exe_size=bundle32_147(p+off+20);
  if(!v.dll_size||!v.exe_size||v.dll_size>1024*1024||v.exe_size>1024*1024||n-off-88!=(size_t)v.dll_size+v.exe_size)return 0;
  v.dll_hash=p+off+24;v.exe_hash=p+off+56;v.dll=p+off+88;v.exe=v.dll+v.dll_size;
 }
 *out=v;return 1;
}
#endif
