/* Deterministic metadata/allocation rollback only; not native mapping evidence. */
#define _CRT_SECURE_NO_WARNINGS
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#define W8_USER
#include <engine/windows8.h>
#define SPACES142 4u
#define SYNC_OBJECTS142 128u
#define VIRTUAL141_PAGES 32768u
#define NX (UINT64_C(1)<<63)
static unsigned active_space142,mapping_resident146;
static uint64_t virtual_pages141;
static w8_mailbox input8;
static int fail_allocate=-1,fail_write=-1;
static unsigned live;
static void*allocations[500];
static uint64_t page_alloc(void){if(!fail_allocate)return 0;if(fail_allocate>0)--fail_allocate;unsigned i=0;while(i<500&&allocations[i])++i;if(i==500)return 0;void*p=_aligned_malloc(4096,4096);if(!p)return 0;memset(p,0x9b,4096);allocations[i]=p;++live;return(uint64_t)(uintptr_t)p;}
static void page_free(uint64_t page){for(unsigned i=0;i<500;++i)if(allocations[i]==(void*)(uintptr_t)page){_aligned_free(allocations[i]);allocations[i]=0;--live;return;}abort();}
static void group_peak142(void){}
static unsigned length8(const char*s){return(unsigned)strlen(s);}
static int equal8(const char*a,const char*b){return!strcmp(a,b);}
static unsigned user8(uint64_t address,void*buffer,unsigned bytes,unsigned write){if(address<4096||!buffer)return 1;if(write){if(!fail_write)return 1;if(fail_write>0)--fail_write;memcpy((void*)(uintptr_t)address,buffer,bytes);}else memcpy(buffer,(const void*)(uintptr_t)address,bytes);return 0;}
static uint64_t*pte8(uint64_t address,unsigned create){(void)address;(void)create;return 0;}
typedef struct {char owner[256];uint16_t name[96];} sync_object142;
static unsigned char sync_used142[SYNC_OBJECTS142];
static sync_object142 sync_objects[SYNC_OBJECTS142];
static sync_object142*sync_object_at142(unsigned i){return sync_objects+i;}
static unsigned sync_name142(uint16_t*name){for(unsigned i=0;i<96;++i)if(!name[i]){memset(name+i,0,(96-i)*2);return 0;}return 206;}
#include "../../kernel/windows8/mapping146.inc"
#define CHECK(x) do{if(!(x)){fprintf(stderr,"Failed line %d\n",__LINE__);return 1;}}while(0)
static void request(wmap_create146*r,uint64_t bytes){memset(r,0,sizeof(*r));r->file=UINT64_MAX;r->bytes=bytes;r->protection=4;r->name[0]='T';}
static int64_t create(wmap_create146*r,wmap_result146*out,unsigned open){return mapping_create146((uint64_t)(uintptr_t)r,(uint64_t)(uintptr_t)out,open);}
static void clean(void){for(unsigned i=0;i<SPACES142;++i){active_space142=i;mapping_release146();}active_space142=0;}
int main(void){
 strcpy(input8.user_root,"/Users/Owner");wmap_create146 r;wmap_result146 out;
 for(int fail=0;fail<5;++fail){request(&r,8193);fail_allocate=fail;CHECK(create(&r,&out,0)==-8&&!live&&!mapping_resident146&&!mapping_processes146[0]);}
 fail_allocate=-1;request(&r,8193);CHECK(!create(&r,&out,0)&&out.handle&&out.bytes==8193&&!out.existed&&live==5);uint64_t first=out.handle;mapping_object146*object=mapping_objects146[0];for(unsigned page=0;page<3;++page)for(unsigned i=0;i<4096;++i)CHECK(!((unsigned char*)(uintptr_t)object->pages[page])[i]);((unsigned char*)(uintptr_t)object->pages[0])[0]=0x51;
 request(&r,0);r.protection=2;CHECK(!create(&r,&out,0)&&out.existed&&out.bytes==8193&&live==5);uint64_t second=out.handle;CHECK(((unsigned char*)(uintptr_t)object->pages[0])[0]==0x51);
 active_space142=1;memset(&r,0,sizeof(r));r.name[0]='T';r.access=4;CHECK(mapping_close146(first)==-6);CHECK(!create(&r,&out,1)&&out.handle!=first&&live==6);uint64_t child=out.handle;
 active_space142=0;CHECK(!mapping_close146(first)&&!mapping_close146(second)&&live==5&&!mapping_processes146[0]);active_space142=1;CHECK(((unsigned char*)(uintptr_t)mapping_objects146[0]->pages[0])[0]==0x51);CHECK(!mapping_close146(child)&&!live&&!mapping_resident146);active_space142=0;
 request(&r,1);fail_write=1;CHECK(create(&r,&out,0)==-998&&!live&&!mapping_resident146);fail_write=-1;
 request(&r,4096);CHECK(!create(&r,&out,0));uint64_t handles[64];handles[0]=out.handle;memset(&r,0,sizeof(r));r.name[0]='T';r.access=4;for(unsigned i=1;i<64;++i){CHECK(!create(&r,&out,1));handles[i]=out.handle;}CHECK(create(&r,&out,1)==-8&&live==3);CHECK(!mapping_close146(handles[0]));CHECK(!create(&r,&out,1)&&out.handle!=handles[0]);CHECK(mapping_close146(handles[0])==-6);handles[0]=out.handle;for(unsigned i=0;i<64;++i)CHECK(!mapping_close146(handles[i]));CHECK(!live&&!mapping_resident146);
 for(unsigned i=0;i<MAP_OBJECTS146;++i){request(&r,1);r.name[0]=0;CHECK(!create(&r,&out,0));handles[i]=out.handle;}CHECK(create(&r,&out,0)==-1816&&live==33);for(unsigned i=0;i<MAP_OBJECTS146;++i)CHECK(!mapping_close146(handles[i]));CHECK(!live&&!mapping_resident146);
 request(&r,4096);sync_used142[0]=1;strcpy(sync_objects[0].owner,input8.user_root);sync_objects[0].name[0]='T';CHECK(create(&r,&out,0)==-6&&!live);sync_used142[0]=0;
 mapping_generation146=0x7fffff;request(&r,1);CHECK(create(&r,&out,0)==-8&&!live&&!mapping_resident146);clean();CHECK(!live);
 puts("{\"passed\":true,\"scope\":\"Supporting hosted production metadata and deterministic allocator rollback; no native PTE/shared-process claim\",\"allocation_failure_positions\":5,\"zero_initialization\":true,\"private_grants_and_source_lifetime\":true,\"stale_handles\":true,\"handle_and_object_quotas\":true,\"output_copy_rollback\":true,\"generation_exhaustion\":true,\"retained_pages\":0}");return 0;
}
