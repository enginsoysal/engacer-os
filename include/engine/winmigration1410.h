#ifndef ENGINE_WINMIGRATION1410_H
#define ENGINE_WINMIGRATION1410_H

#include <engine/wintxn147.h>

/* The current legacy value must still match the committed postimage. A
 * pre-existing identical value gives no evidence of a write by this app.
 * The caller separately excludes competing claims from other products.
 */
static inline unsigned win_migration_postimage1410(
 uint32_t type,const uint8_t *value,unsigned bytes,
 uint32_t after_type,const uint8_t *after,unsigned after_bytes,
 unsigned before_exists,uint32_t before_type,const uint8_t *before,unsigned before_bytes){
 if(type!=after_type||bytes!=after_bytes||memcmp(value,after,bytes))return 0;
 return !before_exists||before_type!=after_type||before_bytes!=after_bytes||
        memcmp(before,after,after_bytes);
}

static inline unsigned win_migration_same_value1410(
 unsigned root,unsigned view,const char *key,const char *name,
 const win_tx_reg147 *other,const char *other_key,const char *other_name){
 if(root!=other->root||(root==2&&view!=other->view))return 0;
 return win_tx_equal147(key,other_key)&&win_tx_equal147(name,other_name);
}

/* Read a bounded committed journal without reserving a contiguous kernel buffer. */
typedef unsigned (*win_migration_read1410)(void*,unsigned,void*,unsigned);
static inline unsigned win_migration_open1410(
 win_migration_read1410 read,void *context,unsigned bytes,
 const char *root,const char *user,win_tx_header147 *header){
 if(bytes<sizeof(*header)||bytes>WIN_TX_LIMIT147||
    read(context,0,header,sizeof(*header))||
    !win_tx_header_shape147(header,bytes)||!win_tx_bound147(header,root,user,0))return 0;
 engine_sha256_context hash;
 uint8_t block[512],digest[32];
 engine_sha256_init(&hash);
 for(unsigned offset=0;offset<bytes;){
  unsigned count=bytes-offset;if(count>sizeof(block))count=sizeof(block);
  if(read(context,offset,block,count))return 0;
  if(!offset)memset(block+72,0,32);
  if(!engine_sha256_update(&hash,block,count))return 0;
  offset+=count;
 }
 return engine_sha256_final(&hash,digest)&&!memcmp(digest,header->checksum,32);
}

typedef struct {
 win_tx_reg147 fields;
 char key[256],name[256];
 unsigned identical_preimage;
 uint8_t after[2048];
} win_migration_value1410;

/* Return one registry effect, none at end, or -1 for malformed input. */
static inline int win_migration_next1410(
 win_migration_read1410 read,void *context,unsigned bytes,
 unsigned *offset,win_migration_value1410 *value){
 while(*offset<bytes){
  win_tx_record147 record;
  if(bytes-*offset<sizeof(record)||read(context,*offset,&record,sizeof(record))||
     record.bytes<sizeof(record)||(record.bytes&7)||record.bytes>bytes-*offset||
     record.type<WIN_TX_FILE147||record.type>WIN_TX_PROPERTY147)return -1;
  unsigned start=*offset+sizeof(record);
  *offset+=record.bytes;
  if(record.type!=WIN_TX_REG147)continue;
  win_tx_reg147 *field=&value->fields;
  unsigned length=record.bytes-sizeof(record);
  if(length<sizeof(*field)||read(context,start,field,sizeof(*field)))return -1;
  if((field->root!=1&&field->root!=2)||(field->view!=32&&field->view!=64)||
     field->before_exists>1||field->reserved||
     (!field->before_exists&&(field->before_bytes||field->before_type))||
     !field->key_bytes||field->key_bytes>sizeof(value->key)||
     !field->name_bytes||field->name_bytes>sizeof(value->name)||
     field->after_bytes>sizeof(value->after)||field->before_bytes>sizeof(value->after))return -1;
  unsigned used=sizeof(*field)+field->key_bytes+field->name_bytes+field->after_bytes+field->before_bytes;
  if(used>length||length-used>7)return -1;
  unsigned at=start+sizeof(*field);
  if(read(context,at,value->key,field->key_bytes))return -1;
  at+=field->key_bytes;
  if(read(context,at,value->name,field->name_bytes))return -1;
  at+=field->name_bytes;
  if(!win_tx_reg_path147(value->key,field->key_bytes,0)||
     !win_tx_reg_path147(value->name,field->name_bytes,1)||
     read(context,at,value->after,field->after_bytes)||
     !win_tx_typed147(field->after_type,value->after,field->after_bytes))return -1;
  at+=field->after_bytes;
  value->identical_preimage=field->before_exists&&
    field->before_type==field->after_type&&field->before_bytes==field->after_bytes;
  if(value->identical_preimage){
   uint8_t block[256];
   for(unsigned offset=0;offset<field->before_bytes;){
    unsigned count=field->before_bytes-offset;
    if(count>sizeof(block))count=sizeof(block);
    if(read(context,at+offset,block,count))return -1;
    if(memcmp(block,value->after+offset,count)){value->identical_preimage=0;break;}
    offset+=count;
   }
  }
  at+=field->before_bytes;
  uint8_t padding[7];
  if(length>used&&(read(context,at,padding,length-used)||!win_tx_zero147(padding,length-used)))return -1;
  return 1;
 }
 return 0;
}

#endif
