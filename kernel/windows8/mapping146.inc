/* Shared RAM-backed committed sections, with process-owned grants and views. */
#include <engine/winmap146.h>
#ifndef W8_NAMED_OWNER
#define W8_NAMED_OWNER (input8.user_root)
#endif
#define MAP_OBJECTS146 16u
#define MAP_PAGES146 256u
#define MAP_VIEWS146 16u
#define MAP_SHARED146 UINT64_C(0x400)
typedef struct {uint64_t bytes,pages[MAP_PAGES146];unsigned refs,protection;char owner[256];uint16_t name[96];} mapping_object146;
typedef struct {unsigned live,generation,object,access;} mapping_cap146;
typedef struct {uint64_t base,bytes,offset;unsigned live,object,writable,reserved;} mapping_view146;
typedef struct {mapping_cap146 handles[64];mapping_view146 views[MAP_VIEWS146];} mapping_process146;
_Static_assert(sizeof(mapping_object146)<=4096,"One section metadata page");
_Static_assert(sizeof(mapping_process146)<=4096,"One lazy process grant/view page");
static mapping_object146*mapping_objects146[MAP_OBJECTS146];
static mapping_process146*mapping_processes146[SPACES142];
static unsigned mapping_generation146;
static void*mapping_page146(void){uint64_t p=page_alloc();if(!p)return 0;memset((void*)(uintptr_t)p,0,4096);++mapping_resident146;group_peak142();return(void*)(uintptr_t)p;}
static void mapping_free_page146(void*p){if(p){page_free((uint64_t)(uintptr_t)p);--mapping_resident146;}}
static mapping_process146*mapping_process_get146(unsigned create){if(!mapping_processes146[active_space142]&&create)mapping_processes146[active_space142]=mapping_page146();return mapping_processes146[active_space142];}
static void mapping_process_trim146(void){mapping_process146*p=mapping_process_get146(0);if(!p)return;for(unsigned i=0;i<64;++i)if(p->handles[i].live)return;for(unsigned i=0;i<MAP_VIEWS146;++i)if(p->views[i].live)return;mapping_processes146[active_space142]=0;mapping_free_page146(p);}
static void mapping_drop146(unsigned index){mapping_object146*o=mapping_objects146[index];if(!o||o->refs)return;for(unsigned i=0;i<MAP_PAGES146;++i)if(o->pages[i])mapping_free_page146((void*)(uintptr_t)o->pages[i]);mapping_objects146[index]=0;mapping_free_page146(o);}
static int mapping_slot146(uint64_t h){if((h&W8_HANDLE_TAG_MASK)!=WMAP_TAG146)return -1;mapping_process146*p=mapping_process_get146(0);if(!p)return -1;unsigned slot=(unsigned)(h&63);mapping_cap146*c=p->handles+slot;return c->live&&c->generation==((h&0x1fffffffu)>>6)&&c->object<MAP_OBJECTS146&&mapping_objects146[c->object]?(int)slot:-1;}
static uint64_t mapping_reference146(unsigned object,unsigned access){
 if(mapping_generation146>=0x7fffffu)return 0;mapping_process146*p=mapping_process_get146(1);if(!p)return 0;unsigned slot=0;while(slot<64&&p->handles[slot].live)++slot;if(slot==64)return 0;
 p->handles[slot]=(mapping_cap146){1,++mapping_generation146,object,access};++mapping_objects146[object]->refs;return WMAP_TAG146|((uint64_t)mapping_generation146<<6)|slot;
}
static int64_t mapping_close146(uint64_t h){int slot=mapping_slot146(h);if(slot<0)return -6;mapping_cap146*c=mapping_process_get146(0)->handles+slot;unsigned index=c->object;c->live=0;--mapping_objects146[index]->refs;mapping_drop146(index);mapping_process_trim146();return 0;}
static unsigned mapping_name_taken146(const uint16_t*name){if(!name[0])return 0;for(unsigned i=0;i<MAP_OBJECTS146;++i){mapping_object146*o=mapping_objects146[i];if(o&&equal8(o->owner,W8_NAMED_OWNER)&&!memcmp(o->name,name,192))return 1;}return 0;}
static unsigned mapping_access146(unsigned value){return value==2||value==4||value==6||value==0xf001f;}
static int64_t mapping_create146(uint64_t input,uint64_t output,unsigned open){
 wmap_create146 r;wmap_result146 result={0};if(user8(input,&r,sizeof(r),0)||user8(output,&result,sizeof(result),1))return -998;
 if(r.reserved[0]||r.reserved[1])return -87;unsigned error=sync_name142(r.name);if(error)return -(int64_t)error;
 if(open){if(!r.name[0]||r.file||r.bytes||r.protection||!mapping_access146(r.access))return -87;}
 else if(r.file!=UINT64_MAX||((r.protection&~0x08000000u)!=2&&(r.protection&~0x08000000u)!=4)||r.access)return -50;
 for(unsigned i=0;i<SYNC_OBJECTS142;++i)if(sync_used142[i]){sync_object142*o=sync_object_at142(i);if(r.name[0]&&equal8(o->owner,W8_NAMED_OWNER)&&!memcmp(o->name,r.name,192))return -6;}
 unsigned index=MAP_OBJECTS146,created=0;
 for(unsigned i=0;i<MAP_OBJECTS146;++i){mapping_object146*o=mapping_objects146[i];if(o&&r.name[0]&&equal8(o->owner,W8_NAMED_OWNER)&&!memcmp(o->name,r.name,192)){index=i;result.existed=1;break;}}
 if(index==MAP_OBJECTS146){
  if(open)return -2;if(!r.bytes)return -87;if(r.bytes>MAP_PAGES146*UINT64_C(4096))return -1816;
  for(unsigned i=0;i<MAP_OBJECTS146;++i)if(!mapping_objects146[i]){index=i;break;}if(index==MAP_OBJECTS146)return -1816;
  mapping_object146*o=mapping_page146();if(!o)return -8;mapping_objects146[index]=o;o->bytes=r.bytes;o->protection=r.protection&255;memcpy(o->owner,W8_NAMED_OWNER,256);memcpy(o->name,r.name,192);created=1;
  for(unsigned i=0;i<(r.bytes+4095)/4096;++i){void*page=mapping_page146();if(!page){mapping_drop146(index);return -8;}o->pages[i]=(uint64_t)(uintptr_t)page;}
 }
 mapping_object146*o=mapping_objects146[index];unsigned access=open?r.access:6;
 if(open&&(access&2)&&o->protection!=4)return -5;
 result.handle=mapping_reference146(index,access);result.bytes=o->bytes;
 if(!result.handle){if(created)mapping_drop146(index);mapping_process_trim146();return -8;}
 if(user8(output,&result,sizeof(result),1)){mapping_close146(result.handle);return -998;}return 0;
}
static int64_t mapping_unmap146(uint64_t);
static unsigned mapping_free_range146(uint64_t base,uint64_t bytes){for(uint64_t at=base;at<base+bytes;at+=4096){uint64_t*p=pte8(at,0);if(p&&*p)return 0;}return 1;}
static int64_t mapping_view146_call(uint64_t input,uint64_t output){
 wmap_view146 r;wmap_result146 result={0};if(user8(input,&r,sizeof(r),0)||user8(output,&result,sizeof(result),1))return -998;if(r.reserved)return -87;if(!mapping_access146(r.access))return -50;
 int slot=mapping_slot146(r.handle);if(slot<0)return -6;mapping_process146*p=mapping_process_get146(0);mapping_cap146*c=p->handles+slot;mapping_object146*o=mapping_objects146[c->object];unsigned writable=(r.access&2)!=0;
 if(writable?(!(c->access&2)||o->protection!=4):!(c->access&4))return -5;if(r.offset&65535)return -1132;if(r.offset>=o->bytes)return -87;
 uint64_t bytes=r.bytes?r.bytes:o->bytes-r.offset;if(bytes>o->bytes-r.offset)return -87;bytes=(bytes+4095)&~UINT64_C(4095);if(bytes/4096>VIRTUAL141_PAGES-virtual_pages141)return -8;
 unsigned view=0;while(view<MAP_VIEWS146&&p->views[view].live)++view;if(view==MAP_VIEWS146)return -1816;
 uint64_t base=r.base;if(base){if((base&65535)||base<W8_BASE||base>=W8_LIMIT||bytes>W8_LIMIT-base)return -487;if(!mapping_free_range146(base,bytes))return -487;}
 else{for(base=UINT64_C(0x130000000);base+bytes<=UINT64_C(0x138000000);base+=65536)if(mapping_free_range146(base,bytes))break;if(base+bytes>UINT64_C(0x138000000))return -8;}
 for(uint64_t at=base;at<base+bytes;at+=4096)if(!pte8(at,1))return -8;
 for(uint64_t at=0;at<bytes;at+=4096){uint64_t*entry=pte8(base+at,0);*entry=o->pages[(r.offset+at)/4096]|5|NX|MAP_SHARED146|(writable?2:0);__asm__ volatile("invlpg (%0)"::"r"(base+at):"memory");}
 p->views[view]=(mapping_view146){base,bytes,r.offset,1,c->object,writable,0};++o->refs;virtual_pages141+=bytes/4096;result.handle=base;result.bytes=bytes;
 if(user8(output,&result,sizeof(result),1)){mapping_unmap146(base);return -998;}return 0;
}
static int64_t mapping_unmap146(uint64_t base){
 mapping_process146*p=mapping_process_get146(0);if(!p)return -487;unsigned index=0;while(index<MAP_VIEWS146&&(!p->views[index].live||p->views[index].base!=base))++index;if(index==MAP_VIEWS146)return -487;
 mapping_view146*v=p->views+index;for(uint64_t at=v->base;at<v->base+v->bytes;at+=4096){uint64_t*entry=pte8(at,0);if(entry)*entry=0;__asm__ volatile("invlpg (%0)"::"r"(at):"memory");}virtual_pages141-=v->bytes/4096;unsigned object=v->object;memset(v,0,sizeof(*v));--mapping_objects146[object]->refs;mapping_drop146(object);mapping_process_trim146();return 0;
}
static unsigned mapping_protect146(uint64_t address,unsigned permission){mapping_process146*p=mapping_process_get146(0);if(!p)return 0;for(unsigned i=0;i<MAP_VIEWS146;++i){mapping_view146*v=p->views+i;if(v->live&&address>=v->base&&address-v->base<v->bytes)return !(permission&4)&&(!(permission&2)||v->writable);}return 0;}
static uint64_t mapping_skip146(uint64_t base,uint64_t bytes){mapping_process146*p=mapping_process_get146(0);if(!p)return base;for(unsigned round=0;round<MAP_VIEWS146;++round){unsigned moved=0;for(unsigned i=0;i<MAP_VIEWS146;++i){mapping_view146*v=p->views+i;if(v->live&&base<v->base+v->bytes&&base+bytes>v->base){base=(v->base+v->bytes+65535)&~UINT64_C(65535);moved=1;}}if(!moved)return base;}return base;}
static void mapping_release146(void){
 mapping_process146*p=mapping_process_get146(0);if(!p)return;for(unsigned i=0;i<MAP_VIEWS146;++i)if(p->views[i].live){uint64_t base=p->views[i].base;(void)mapping_unmap146(base);p=mapping_process_get146(0);if(!p)return;}
 for(unsigned i=0;i<64;++i)if(p->handles[i].live){uint64_t h=WMAP_TAG146|((uint64_t)p->handles[i].generation<<6)|i;(void)mapping_close146(h);p=mapping_process_get146(0);if(!p)return;}mapping_process_trim146();
}
static int64_t mapping_call146(uint64_t operation,uint64_t value,uint64_t result,uint64_t extra){
 if(extra)return -87;if(operation==WMAP_QUERY146){if(!result||value<W8_BASE||value>=W8_LIMIT||result>W8_LIMIT-value)return -87;mapping_process146*p=mapping_process_get146(0);if(!p)return 0;for(unsigned i=0;i<MAP_VIEWS146;++i){mapping_view146*v=p->views+i;if(v->live&&value>=v->base&&value-v->base<v->bytes&&result<=v->bytes-(value-v->base))return v->writable?3:1;}return 0;}if(operation==WMAP_CREATE146||operation==WMAP_OPEN146)return mapping_create146(value,result,operation==WMAP_OPEN146);
 if(operation==WMAP_VIEW146)return mapping_view146_call(value,result);
 if(operation==WMAP_SKIP146){if(!result||result>24*1024*1024||value<W8_BASE||value>=W8_LIMIT||result>W8_LIMIT-value)return -87;uint64_t base=mapping_skip146(value,result);return base<W8_LIMIT&&result<=W8_LIMIT-base?(int64_t)base:-487;}
 if(result)return -87;if(operation==WMAP_CLOSE146)return mapping_close146(value);if(operation==WMAP_UNMAP146)return mapping_unmap146(value);return -87;
}
