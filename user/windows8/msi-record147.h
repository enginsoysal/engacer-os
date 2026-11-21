/* Bounded MSI record ownership. The service serializes access to this context. */
#ifndef ENGINE_MSI_RECORD147_H
#define ENGINE_MSI_RECORD147_H
#include "msi-properties147.h"
#define MSIR_BUDGET147 262144u
#define MSIR_NULL147 INT32_MIN
typedef struct {char *text;int32_t integer;unsigned kind,bytes;} msir_field147;
typedef struct {unsigned handle,fields,bytes;msir_field147 values[];} msir_record147;
typedef struct {msir_record147 *slots[64];unsigned generation,bytes;msip_alloc147 alloc;msip_free147 release;void *context;} msir_context147;
static inline msir_record147 *msir_find147(msir_context147*c,unsigned h){unsigned slot=(h&127u);if(!c||!slot||slot>64)return 0;msir_record147*r=c->slots[slot-1];return r&&r->handle==h?r:0;}
static inline unsigned msir_create147(msir_context147*c,unsigned fields){
 if(!c||!c->alloc||!c->release||fields>32||c->generation>=0xfffffu)return 0;
 unsigned slot=0;while(slot<64&&c->slots[slot])++slot;if(slot==64)return 0;
 unsigned bytes=(unsigned)sizeof(msir_record147)+(fields+1)*(unsigned)sizeof(msir_field147);if(bytes>MSIR_BUDGET147-c->bytes)return 0;
 msir_record147*r=c->alloc(c->context,bytes);if(!r)return 0;unsigned char*p=(void*)r;for(unsigned i=0;i<bytes;++i)p[i]=0;
 r->fields=fields;r->bytes=bytes;r->handle=0x70000000u|(++c->generation<<7)|(slot+1);c->slots[slot]=r;c->bytes+=bytes;return r->handle;
}
static inline void msir_clear_field147(msir_context147*c,msir_record147*r,unsigned at){msir_field147*f=r->values+at;if(f->text){c->release(c->context,f->text);c->bytes-=f->bytes;r->bytes-=f->bytes;}*f=(msir_field147){0};}
static inline unsigned msir_clear147(msir_context147*c,unsigned h){msir_record147*r=msir_find147(c,h);if(!r)return 6;for(unsigned i=0;i<=r->fields;++i)msir_clear_field147(c,r,i);return 0;}
static inline unsigned msir_close147(msir_context147*c,unsigned h){msir_record147*r=msir_find147(c,h);if(!r)return 6;msir_clear147(c,h);c->bytes-=r->bytes;c->slots[(h&127u)-1]=0;c->release(c->context,r);return 0;}
static inline void msir_destroy147(msir_context147*c){if(!c)return;for(unsigned i=0;i<64;++i)if(c->slots[i])msir_close147(c,c->slots[i]->handle);}
static inline unsigned msir_string147(msir_context147*c,unsigned h,unsigned at,const char*value){
 msir_record147*r=msir_find147(c,h);if(!r)return 6;if(at>r->fields)return 87;
 unsigned n=0;if(value){while(n<=4096&&value[n])++n;if(n>4096)return 1816;}if(!n){msir_clear_field147(c,r,at);return 0;}
 if(n+1>MSIR_BUDGET147-c->bytes)return 1816;char*p=c->alloc(c->context,n+1);if(!p)return 8;for(unsigned i=0;i<=n;++i)p[i]=value[i];msir_clear_field147(c,r,at);r->values[at]=(msir_field147){.text=p,.bytes=n+1,.kind=1};c->bytes+=n+1;r->bytes+=n+1;return 0;
}
static inline unsigned msir_integer147(msir_context147*c,unsigned h,unsigned at,int32_t value){msir_record147*r=msir_find147(c,h);if(!r)return 6;if(at>r->fields)return 87;msir_clear_field147(c,r,at);if(value!=MSIR_NULL147)r->values[at]=(msir_field147){.kind=2,.integer=value};return 0;}
static inline const char *msir_text147(msir_context147*c,unsigned h,unsigned at,char scratch[16]){msir_record147*r=msir_find147(c,h);if(!r||at>r->fields)return 0;msir_field147*f=r->values+at;if(f->kind!=2)return f->text?f->text:"";char reverse[16];unsigned n=0,used=0;uint32_t v=f->integer<0?(uint32_t)-(int64_t)f->integer:(uint32_t)f->integer;if(f->integer<0)scratch[used++]='-';do{reverse[n++]=(char)('0'+v%10);v/=10;}while(v);while(n)scratch[used++]=reverse[--n];scratch[used]=0;return scratch;}
static inline int32_t msir_number147(msir_context147*c,unsigned h,unsigned at){msir_record147*r=msir_find147(c,h);if(!r||at>r->fields)return MSIR_NULL147;msir_field147*f=r->values+at;if(f->kind==2)return f->integer;if(f->kind!=1)return MSIR_NULL147;const char*s=f->text;unsigned i=0,negative=0;if(s[0]=='-'){negative=1;++i;}if(!s[i])return MSIR_NULL147;uint64_t n=0;for(;s[i];++i){if(s[i]<'0'||s[i]>'9')return MSIR_NULL147;n=n*10+(unsigned)(s[i]-'0');if(n>INT32_MAX)return MSIR_NULL147;}return negative?-(int32_t)n:(int32_t)n;}
#endif
