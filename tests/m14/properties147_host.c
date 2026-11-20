/* Host-only session adapter. Production owns allocation and parsing behavior. */
#include <stddef.h>
#include <stdint.h>
void *memset(void *out,int value,size_t n){unsigned char *p=out;for(size_t i=0;i<n;++i)p[i]=(unsigned char)value;return out;}
void *memcpy(void *out,const void *in,size_t n){unsigned char *p=out;const unsigned char *s=in;for(size_t i=0;i<n;++i)p[i]=s[i];return out;}
#include "../../user/windows8/msi-properties147.h"
static msip_session147 session147;
__declspec(dllexport) void init147(msip_alloc147 alloc,msip_free147 release,void *context){msip_destroy147(&session147);session147=(msip_session147){.alloc=alloc,.release=release,.context=context};}
__declspec(dllexport) unsigned set147(const char *name,const char *value){return msip_set147(&session147,name,value);}
__declspec(dllexport) const char *get147(const char *name){return msip_get147(&session147,name);}
__declspec(dllexport) unsigned count147(void){return session147.count;}
__declspec(dllexport) unsigned bytes147(void){return session147.bytes;}
__declspec(dllexport) void destroy147(void){msip_destroy147(&session147);}
__declspec(dllexport) unsigned format147(const char *text,char *out,unsigned capacity){return msip_format147(&session147,text,out,capacity,0,0);}
