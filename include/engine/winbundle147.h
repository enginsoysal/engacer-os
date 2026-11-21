#ifndef ENGINE_WINBUNDLE147_H
#define ENGINE_WINBUNDLE147_H
#include <engine/base.h>
/* Borrowed slices remain owned by the reserved init boot module. */
typedef struct {const uint8_t *msi,*dll,*exe,*runtime,*dll_hash,*exe_hash,*runtime_hash;unsigned msi_size,dll_size,exe_size,runtime_size;} winbundle147;
static inline uint32_t bundle32_147(const uint8_t*p){return (uint32_t)p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;}
static inline int winbundle_parse147(const void*data,size_t n,winbundle147*out){
 const uint8_t*p=data;winbundle147 v={0};
 if(!p||!out||n<96||n>4*1024*1024||memcmp(p+48,"ENGMSI81",8))return 0;
 uint32_t m=bundle32_147(p+56);if(bundle32_147(p+60)||!m||m>n-96)return 0;
 v.msi=p+96;v.msi_size=m;size_t off=96+(size_t)m;
 if(off!=n){
  if(n-off<16||memcmp(p+off,"ENGMS147",8))return 0;
  unsigned version=bundle32_147(p+off+8),count=bundle32_147(p+off+12),header=0,hashes=0;
  if(version==1&&count==2){header=88;hashes=24;}else if(version==2&&count==3){header=124;hashes=28;}else return 0;
  if(n-off<header)return 0;v.dll_size=bundle32_147(p+off+16);v.exe_size=bundle32_147(p+off+20);
  if(version==2)v.runtime_size=bundle32_147(p+off+24);
  if(!v.dll_size||!v.exe_size||v.dll_size>1024*1024||v.exe_size>1024*1024||v.runtime_size>1024*1024||(version==2&&!v.runtime_size)||n-off-header!=(size_t)v.dll_size+v.exe_size+v.runtime_size)return 0;
  v.dll_hash=p+off+hashes;v.exe_hash=v.dll_hash+32;v.dll=p+off+header;v.exe=v.dll+v.dll_size;
  if(version==2){v.runtime_hash=v.exe_hash+32;v.runtime=v.exe+v.exe_size;}
 }
 *out=v;return 1;
}
#endif
