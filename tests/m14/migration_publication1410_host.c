/* Interrupt the exact volume operation that publishes a migrated registry. */
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <engine/storage/volume6.h>

enum {PAGE=4096,BLOCKS=4096};
#define DATA "/Data"
#define BUNDLE DATA "/Bundle"
#define STAGED BUNDLE "/Migration"
#define VISIBLE BUNDLE "/Registry"
#define OLD DATA "/Old"

typedef struct {
 unsigned char *bytes;
 unsigned calls,fail,torn;
} disk1410;

static unsigned read1410(void *context,uint64_t block,void *out,unsigned bytes){
 disk1410 *disk=context;
 if(block>=BLOCKS||bytes!=PAGE)return 1;
 memcpy(out,disk->bytes+block*PAGE,bytes);
 return 0;
}
static unsigned write1410(void *context,uint64_t block,void *data,unsigned bytes){
 disk1410 *disk=context;
 if(block>=BLOCKS||bytes!=PAGE)return 1;
 if(++disk->calls==disk->fail){
  if(disk->torn)memcpy(disk->bytes+block*PAGE,data,bytes/2);
  return 1;
 }
 memcpy(disk->bytes+block*PAGE,data,bytes);
 return 0;
}
static unsigned flush1410(void *context){
 disk1410 *disk=context;
 return ++disk->calls==disk->fail;
}
static unsigned source1410(void *context,uint64_t start,void *out,unsigned bytes){
 memcpy(out,(const char*)context+start,bytes);
 return 0;
}
static void attach1410(v6_volume *volume,disk1410 *disk){
 memset(volume,0,sizeof(*volume));
 volume->context=disk;volume->read=read1410;volume->write=write1410;
 volume->flush=flush1410;volume->blocks=BLOCKS;
}
static void put1410(v6_volume *volume,const char *path,const char *value){
 assert(v6_put(volume,path,strlen(value),source1410,(void*)value)==V6_OK);
}
static void check1410(v6_volume *volume,const char *path,const char *value){
 char bytes[32];unsigned read;
 assert(v6_verify(volume,path)==V6_OK);
 assert(v6_read(volume,path,0,bytes,sizeof(bytes),&read)==V6_OK);
 assert(read==strlen(value)&&!memcmp(bytes,value,read));
}
static void publication1410(v6_volume *volume){
 assert(v6_verify(volume,STAGED "/value")==V6_NOTFOUND);
 check1410(volume,VISIBLE "/value","owned");
 check1410(volume,VISIBLE "/receipt","verified");
 check1410(volume,OLD "/value","legacy");
}

int main(void){
 const size_t size=(size_t)BLOCKS*PAGE;
 disk1410 disk={.bytes=calloc(BLOCKS,PAGE)};
 unsigned char *initial=malloc(size);
 v6_volume *volume=malloc(sizeof(*volume));
 assert(disk.bytes&&volume&&initial);
 attach1410(volume,&disk);
 assert(v6_format(volume)==V6_OK);
 assert(v6_mkdir(volume,DATA)==V6_OK);
 assert(v6_mkdir(volume,BUNDLE)==V6_OK);
 assert(v6_mkdir(volume,STAGED)==V6_OK);
 assert(v6_mkdir(volume,OLD)==V6_OK);
 put1410(volume,STAGED "/value","owned");
 put1410(volume,STAGED "/receipt","verified");
 put1410(volume,OLD "/value","legacy");
 memcpy(initial,disk.bytes,size);
 disk.calls=0;
 assert(v6_move_tree11(volume,STAGED,VISIBLE,0)==V6_OK);
 unsigned boundaries=disk.calls;
 assert(boundaries>2);
 publication1410(volume);

 for(unsigned torn=0;torn<=1;++torn)for(unsigned operation=1;operation<=boundaries;++operation){
  memcpy(disk.bytes,initial,size);
  attach1410(volume,&disk);
  assert(v6_mount(volume)==V6_OK);
  disk.calls=0;disk.fail=operation;disk.torn=torn;
  assert(v6_move_tree11(volume,STAGED,VISIBLE,0)!=V6_OK);

  disk.fail=0;
  attach1410(volume,&disk);
  assert(v6_mount(volume)==V6_OK);
  check1410(volume,OLD "/value","legacy");
  if(v6_verify(volume,VISIBLE "/receipt")==V6_NOTFOUND){
   assert(v6_verify(volume,VISIBLE "/value")==V6_NOTFOUND);
   check1410(volume,STAGED "/value","owned");
   check1410(volume,STAGED "/receipt","verified");
   assert(v6_move_tree11(volume,STAGED,VISIBLE,0)==V6_OK);
  }
  publication1410(volume);
 }
 free(volume);free(initial);free(disk.bytes);
 return 0;
}
