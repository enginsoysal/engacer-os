/* M14.10 converts only attributable legacy registry effects. Legacy storage
 * is left intact. The staged tree becomes visible with one catalog commit. */
#include <engine/winmigration1410.h>

typedef struct {
 char root[256],journal[256];
 win_tx_header147 header;
} migration_msi1410;

static unsigned migration_read1410(void *path,unsigned offset,void *out,unsigned bytes){
 return exact8(path,offset,out,bytes);
}

static unsigned migration_msi_open1410(migration_msi1410 *msi,const char *root,
                                      const char *user){
 copy8(msi->root,root,sizeof(msi->root));
 copy8(msi->journal,root,sizeof(msi->journal));
 path_append143(msi->journal,"/product.bin",sizeof(msi->journal));
 const v6_entry *entry=find8(msi->journal);
 if(!entry)return V6_NOTFOUND;
 uint64_t magic=0;
 if(entry->kind!=1||entry->size<sizeof(magic)||entry->size>WIN_TX_LIMIT147||
    v6_verify(m6_volume(),msi->journal)||exact8(msi->journal,0,&magic,sizeof(magic)))return V6_INVALID;
 /* The old compact 7-Zip record predates journaled registry effects. */
 if(magic==UINT64_C(0x31494d38574f53))return V6_NOTFOUND;
 if(exact8(msi->journal,0,&msi->header,sizeof(msi->header))||
    !win_tx_header_shape147(&msi->header,(unsigned)entry->size))return V6_INVALID;
 char principal[256];
 copy8(principal,user?user:msi->header.user,sizeof(principal));
 return win_migration_open1410(migration_read1410,msi->journal,(unsigned)entry->size,
                               msi->root,principal,&msi->header)?V6_OK:V6_INVALID;
}

static unsigned migration_key_directory1410(char *directory,const char *base,
                                            const char *principal,const char *key){
 char principal_hash[33],key_hash[33];
 protected_hash143(principal,principal_hash);
 protected_hash143(key,key_hash);
 unsigned error=path_copy143(directory,base,256);
 if(!error)error=path_append143(directory,"/",256);
 if(!error)error=path_append143(directory,principal_hash,256);
 if(!error)error=path_append143(directory,"/k",256);
 if(!error)error=path_append143(directory,key_hash,256);
 return error?V6_LIMIT:V6_OK;
}

static unsigned migration_value_path1410(char *path,const char *directory,const char *name){
 char hash[33];protected_hash143(name,hash);
 unsigned error=path_copy143(path,directory,256);
 if(!error)error=path_append143(path,"/v",256);
 if(!error)error=path_append143(path,hash,256);
 return error?V6_LIMIT:V6_OK;
}

static unsigned migration_copy_value1410(const char *stage,const char *user,
                                         const win_migration_value1410 *claim){
 const win_tx_reg147 *effect=&claim->fields;
 const char *principal=effect->root==1?user:effect->view==32?"/Machine/32":"/Machine/64";
 char directory[256],value_path[256],key_path[256],legacy[256],principal_hash[33];
 char key[768],name[256];
 if(registry_fold143(claim->key,key,sizeof(key))||
    registry_fold143(claim->name,name,sizeof(name)))return V6_INVALID;
 protected_hash143(principal,principal_hash);
 copy8(legacy,"/Data/Windows/",sizeof(legacy));
 path_append143(legacy,principal_hash,sizeof(legacy));
 path_append143(legacy,"/Registry/k",sizeof(legacy));
 char key_hash[33];protected_hash143(key,key_hash);
 path_append143(legacy,key_hash,sizeof(legacy));
 if(migration_value_path1410(value_path,legacy,name))return V6_LIMIT;
 const v6_entry *entry=find8(value_path);
 if(!entry)return V6_OK;
 registry_value_record143 *value=(void*)io8;
 const unsigned fixed=offsetof(registry_value_record143,data);
 if(entry->kind!=1||entry->size<fixed||entry->size>sizeof(*value)||
    v6_verify(m6_volume(),value_path)||exact8(value_path,0,value,(unsigned)entry->size))return V6_INVALID;
 if(value->magic!=REGISTRY_VALUE_MAGIC143||value->bytes!=entry->size-fixed||
    !terminated142(value->user,sizeof(value->user))||
    !terminated142(value->key,sizeof(value->key))||
    !terminated142(value->name,sizeof(value->name))||
    !terminated142(value->display,sizeof(value->display))||
    !equal8(value->user,principal)||!equal8(value->key,key)||!equal8(value->name,name))
  return V6_INVALID;
 char folded[256];
 if(registry_fold143(value->display,folded,sizeof(folded))||!equal8(folded,name))return V6_INVALID;
 if(!win_migration_postimage1410(value->type,value->data,value->bytes,
      effect->after_type,claim->after,effect->after_bytes,
      effect->before_exists,effect->before_type,claim->before,effect->before_bytes))return V6_OK;

 unsigned status=migration_key_directory1410(directory,stage,principal,key);
 if(status)return status;
 copy8(key_path,directory,sizeof(key_path));
 if(path_append143(key_path,"/$key",sizeof(key_path)))return V6_LIMIT;
 if(!find8(key_path)){
  registry_key_record143 record;
  memset(&record,0,sizeof(record));
  record.magic=REGISTRY_KEY_MAGIC143;
  copy8(record.user,principal,sizeof(record.user));
  copy8(record.canonical,key,sizeof(record.canonical));
  copy8(record.display,claim->key,sizeof(record.display));
  if(protected_prepare143(directory))return V6_IO;
  status=v6_put(m6_volume(),key_path,sizeof(record),memory_source8,&record);
  if(status)return status;
 }
 status=migration_value_path1410(value_path,directory,name);
 if(status)return status;
 if(find8(value_path))return V6_INVALID;
 return v6_put(m6_volume(),value_path,fixed+value->bytes,memory_source8,value);
}

static unsigned migration_exe_claim1410(const exe_record148 *record,unsigned index,
                                        win_migration_value1410 *claim){
 if(record->state!=EXE148_INSTALLED||index>=2)return 0;
 const exe_shared148 *prior=&record->shared[index];
 if(prior->present>1||prior->bytes>sizeof(prior->data))return 0;
 memset(claim,0,sizeof(*claim));
 claim->fields.root=1;claim->fields.view=64;claim->fields.after_type=1;
 copy8(claim->key,exe_shared_key148(index),sizeof(claim->key));
 copy8(claim->name,exe_shared_name148(index),sizeof(claim->name));
 /* The reviewed EXE profile inventories exactly these two shared effects. */
 static const uint16_t mime[]={'a','p','p','l','i','c','a','t','i','o','n','/','p','d','f',0};
 static const uint16_t extension[]={'.','p','d','f',0};
 const void *after=index?(const void*)extension:(const void*)mime;
 claim->fields.after_bytes=index?sizeof(extension):sizeof(mime);
 memcpy(claim->after,after,claim->fields.after_bytes);
 claim->fields.before_exists=prior->present;
 claim->fields.before_type=prior->type;
 claim->fields.before_bytes=prior->bytes;
 memcpy(claim->before,prior->data,prior->bytes);
 return 1;
}

static unsigned migration_name_equal1410(const char *a,const char *b){
 return equal_utf8_143(a,length8(a),b,length8(b))==1;
}

/* Competing ownership only needs the registry coordinates, not the data. */
static unsigned migration_msi_conflict1410(migration_msi1410 *msi,
 const win_migration_value1410 *claim){
 const win_tx_reg147 *effect=&claim->fields;
 unsigned at=sizeof(msi->header),count=0;
 while(at<msi->header.bytes){
  win_tx_record147 record;
  unsigned remaining=msi->header.bytes-at;
  if(remaining<sizeof(record)||exact8(msi->journal,at,&record,sizeof(record))||
     record.bytes<sizeof(record)||(record.bytes&7)||record.bytes>remaining||
     record.type<WIN_TX_FILE147||record.type>WIN_TX_PROPERTY147)return 1;
  unsigned start=at+sizeof(record);
  at+=record.bytes;
  if(record.type!=WIN_TX_REG147)continue;
  ++count;
  win_tx_reg147 other;
  if(record.bytes<sizeof(record)+sizeof(other)||
     exact8(msi->journal,start,&other,sizeof(other))||
     (other.root!=1&&other.root!=2)||(other.view!=32&&other.view!=64)||
     !other.key_bytes||other.key_bytes>256||!other.name_bytes||other.name_bytes>256||
     other.key_bytes+other.name_bytes>record.bytes-sizeof(record)-sizeof(other))return 1;
  if(effect->root!=other.root||(effect->root==2&&effect->view!=other.view))continue;
  char key[256],name[256];start+=sizeof(other);
  if(exact8(msi->journal,start,key,other.key_bytes)||
     exact8(msi->journal,start+other.key_bytes,name,other.name_bytes)||
     !win_tx_reg_path147(key,other.key_bytes,0)||
     !win_tx_reg_path147(name,other.name_bytes,1))return 1;
  if(migration_name_equal1410(key,claim->key)&&migration_name_equal1410(name,claim->name))return 1;
 }
 return count!=msi->header.registry;
}

static unsigned migration_conflict1410(const char *root,const char *user,
                                       const win_migration_value1410 *claim){
 const win_tx_reg147 *effect=&claim->fields;
 migration_msi1410 other;
 v6_volume *volume=m6_volume();
 for(unsigned i=0;i<V6_ENTRIES;++i){
  const v6_entry *entry=volume->entries+i;
  if(entry->kind!=2||!win_product_root147(entry->path)||equal8(entry->path,root))continue;
  unsigned status=migration_msi_open1410(&other,entry->path,0);
  if(status==V6_NOTFOUND)continue;
  if(status)return 1;
  if(effect->root==1&&!equal8(user,other.header.user))continue;
  if(migration_msi_conflict1410(&other,claim))return 1;
 }
 if(effect->root==1&&!equal8(root,EXE148_ROOT)&&find8(EXE148_ROOT)){
  exe_record148 record;
  unsigned status=exe_record_load148(user,&record);
  if(status!=2&&status)return 1;
  if(!status&&record.state==EXE148_INSTALLED)for(unsigned i=0;i<2;++i)
   if(migration_name_equal1410(claim->key,exe_shared_key148(i))&&
      migration_name_equal1410(claim->name,exe_shared_name148(i)))return 1;
 }
 return 0;
}

static unsigned migrate_registry1410(const char *root,const char *user){
 uint64_t generation=0;
 unsigned status=app_generation1410(root,0,&generation);
 if(status||generation||!find8(root))return status;
 migration_msi1410 msi;
 exe_record148 exe;
 unsigned is_exe=equal8(root,EXE148_ROOT);
 const uint8_t *digest;
 if(is_exe){
  unsigned loaded=exe_record_load148(user,&exe);
  if(loaded==2)return V6_OK;
  if(loaded)return V6_INVALID;
  if(exe.state!=EXE148_INSTALLED)return V6_OK;
  digest=exe.checksum;
 }else{
  status=migration_msi_open1410(&msi,root,user);
  if(status==V6_NOTFOUND)return V6_OK;
  if(status)return status;
  digest=msi.header.checksum;
 }
 char stage[256],target[256],receipt[256];
 copy8(stage,root,sizeof(stage));
 path_append143(stage,"/.Engacer/Migration",sizeof(stage));
 copy8(target,root,sizeof(target));
 path_append143(target,"/.Engacer/Registry",sizeof(target));
 copy8(receipt,target,sizeof(receipt));
 path_append143(receipt,"/$legacy-migration",sizeof(receipt));
 if(find8(target)){
  uint8_t checked[32];
  const v6_entry *stored=find8(receipt);
  return stored&&stored->kind==1&&stored->size==sizeof(checked)&&
         !v6_verify(m6_volume(),receipt)&&!exact8(receipt,0,checked,sizeof(checked))&&
         !memcmp(checked,digest,sizeof(checked))?V6_OK:V6_EXISTS;
 }
 /* An interrupted staging pass is never visible to registry lookup. */
 if(find8(stage)&&(status=v6_remove_tree11(m6_volume(),stage)))return status;
 if(protected_prepare143(stage))return V6_IO;
 win_migration_value1410 claim;
 unsigned offset=sizeof(msi.header),count=0;
 for(;;){
  int next=is_exe?(count<2?(migration_exe_claim1410(&exe,count,&claim)?1:-1):0):
                   win_migration_next1410(migration_read1410,msi.journal,msi.header.bytes,&offset,&claim);
  if(next<0)return V6_INVALID;
  if(!next)break;
  ++count;
  if(migration_conflict1410(root,user,&claim))continue;
  status=migration_copy_value1410(stage,user,&claim);
  if(status)return status;
 }
 if(!is_exe&&count!=msi.header.registry)return V6_INVALID;
 copy8(receipt,stage,sizeof(receipt));
 path_append143(receipt,"/$legacy-migration",sizeof(receipt));
 if((status=v6_put(m6_volume(),receipt,32,memory_source8,(void*)digest)))return status;
 return v6_move_tree11(m6_volume(),stage,target,0);
}
