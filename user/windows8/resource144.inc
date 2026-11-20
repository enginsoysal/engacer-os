/* Resource descriptors refer to immutable mapped image bytes, not extra copies. */
#include "resource-core144.h"
typedef struct resource_ref144 {struct resource_ref144*next;uint64_t handle,base;unsigned generation;resource_result144 result;} resource_ref144;
static resource_ref144*resource_refs144;static uint64_t resource_generation144;static unsigned resource_count144,module_generation144;
static void resource_release144(uint64_t base){resource_ref144**link=&resource_refs144;while(*link){resource_ref144*r=*link;if(r->base==base){*link=r->next;free8(r);--resource_count144;}else link=&r->next;}}
static unsigned resource_key_from144(const WCHAR*name,resource_key144*out){memset(out,0,sizeof(*out));uintptr_t value=(uintptr_t)name;if(value<=65535){out->numeric=1;out->id=(unsigned)value;return 0;}if(name[0]=='#'){unsigned id=0,n=1;for(;name[n];++n){if(n>5||name[n]<'0'||name[n]>'9'||id>(65535u-(name[n]-'0'))/10)return 87;id=id*10+name[n]-'0';}if(n==1)return 87;out->numeric=1;out->id=id;return 0;}for(unsigned n=0;n<128;++n){if(!name[n]){out->units=n;return 0;}out->text[n]=name[n];}return 206;}
uint64_t pe8_find_resource(uint64_t base,const WCHAR*type,const WCHAR*name,unsigned language,unsigned exact,unsigned*error){
 *error=0;lock_enter142(&loader_lock142);int slot=slot141(base?base:pe8_main());if(slot<0){*error=126;lock_leave142(&loader_lock142);return 0;}module141*m=modules141+slot;resource_key144 a,b;unsigned status=resource_key_from144(type,&a);if(!status)status=resource_key_from144(name,&b);resource_result144 result;
 if(!status){resource_image144 image={m->base,m->size,m->resources,m->resource_bytes};status=resource_find144(&image,&a,&b,language,exact,&result);}if(status){*error=status;lock_leave142(&loader_lock142);return 0;}
 for(resource_ref144*r=resource_refs144;r;r=r->next)if(r->base==(uint64_t)(uintptr_t)m->base&&r->generation==m->generation&&r->result.entry==result.entry){uint64_t handle=r->handle;lock_leave142(&loader_lock142);return handle;}
 if(resource_count144==256||resource_generation144==UINT32_MAX){*error=1816;lock_leave142(&loader_lock142);return 0;}resource_ref144*r=alloc8(sizeof(*r));if(!r){*error=8;lock_leave142(&loader_lock142);return 0;}
 *r=(resource_ref144){resource_refs144,UINT64_C(0x5253000000000000)|++resource_generation144,(uint64_t)(uintptr_t)m->base,m->generation,result};resource_refs144=r;++resource_count144;uint64_t handle=r->handle;lock_leave142(&loader_lock142);return handle;
}
unsigned pe8_resource_data(uint64_t base,uint64_t handle,const void**data,unsigned*bytes){
 unsigned error=1814;lock_enter142(&loader_lock142);for(resource_ref144*r=resource_refs144;r;r=r->next)if(r->handle==handle){int slot=slot141(r->base);if(slot<0||modules141[slot].generation!=r->generation)break;if(base&&base!=r->base){error=6;break;}module141*m=modules141+slot;if(!range141(r->result.data,r->result.bytes,m->size)){error=193;break;}*data=m->base+r->result.data;*bytes=r->result.bytes;error=0;break;}lock_leave142(&loader_lock142);return error;
}
