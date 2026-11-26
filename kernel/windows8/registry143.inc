/* Durable bounded HKCU records. Hashes locate records; full identities authorize them. */
#define REGISTRY_KEYS143 64u
#ifdef ENGINE_M14
/* Durable namespace capacity is independent of the lazy live-object budget. */
#define REGISTRY_PERSISTED_KEYS148 512u
#define REGISTRY_VALUES143 1024u
#else
#define REGISTRY_PERSISTED_KEYS148 REGISTRY_KEYS143
#define REGISTRY_VALUES143 128u
#endif
#define REGISTRY_KEY_MAGIC143 UINT64_C(0x314b52454734314d)
#define REGISTRY_VALUE_MAGIC143 UINT64_C(0x315652454734314d)
typedef struct {uint64_t magic,time;char user[256],canonical[768],display[768];} registry_key_record143;
typedef struct {uint64_t magic;uint32_t type,bytes;char user[256],key[768],name[256],display[256];uint8_t data[2048];} registry_value_record143;
typedef struct {registry_key_record143 record;char directory[256];
#ifdef ENGINE_M14
 char app_owner[65];
#endif
 unsigned refs,deleted;} registry_object143;
_Static_assert(sizeof(registry_object143)<=4096&&sizeof(registry_value_record143)<=4096,"Registry records exceed the scratch-page budget");
static registry_object143*registry_objects143[REGISTRY_KEYS143];
static unsigned registry_generation143;
static uint64_t registry_page143(void){if(registry_resident143>=REGISTRY_KEYS143+2)return 0;uint64_t page=page_alloc();if(page){memset((void*)(uintptr_t)page,0,4096);++registry_resident143;group_peak142();}return page;}
static void registry_free143(uint64_t page){page_free(page);--registry_resident143;}
#ifdef ENGINE_M14
/* Per-syscall namespace selection; syscall work does not yield between phases. */
static unsigned registry_machine147;
static const char*registry_owner147(void){return registry_machine147==1?"/Machine/64":registry_machine147==2?"/Machine/32":input8.user_root;}
static unsigned registry_hklm147(uint64_t h){return h==UINT64_C(0x80000002)||h==UINT64_C(0xffffffff80000002);}
#else
#define registry_owner147() input8.user_root
#endif
static unsigned registry_hkcu143(uint64_t handle){return handle==UINT64_C(0x80000001)||handle==UINT64_C(0xffffffff80000001)
#ifdef ENGINE_M14
 ||registry_hklm147(handle)
#endif
 ;}
static unsigned registry_fold143(const char*source,char*out,unsigned cap){
 unsigned bytes=length8(source),at=0,used=0;while(at<bytes){uint32_t scalar;if(!decode_utf8_143(source,bytes,&at,&scalar)||!encode_utf8_143(fold143(scalar),out,cap-1,&used))return 206;}out[used]=0;return 0;
}
#define registry_hash143 protected_hash143
#define registry_prepare143 protected_prepare143
static void registry_root143(char*out){
#ifdef ENGINE_M14
 char hash[33];protected_hash143(registry_owner147(),hash);copy8(out,"/Data/Windows/",256);path_append143(out,hash,256);path_append143(out,"/Registry",256);
#else
 protected_root143("Registry",out);
#endif
}
static void registry_directory143(const char*canonical,char*out){char hash[33];registry_hash143(canonical,hash);registry_root143(out);path_append143(out,"/k",256);path_append143(out,hash,256);}
static unsigned registry_load_key143(const char*canonical,const char*directory,registry_key_record143*out){
 char path[256];copy8(path,directory,256);path_append143(path,"/$key",256);const v6_entry*entry=find8(path);if(!entry)return 2;
 unsigned got=0;if(entry->kind!=1||entry->size!=sizeof(*out)||v6_verify(m6_volume(),path)||v6_read(m6_volume(),path,0,out,sizeof(*out),&got)||got!=sizeof(*out))return 13;
 if(out->magic!=REGISTRY_KEY_MAGIC143||!terminated142(out->user,256)||!terminated142(out->canonical,768)||!terminated142(out->display,768)||!equal8(out->user,registry_owner147())||!equal8(out->canonical,canonical))return 13;
 char folded[768];if(registry_fold143(out->display,folded,sizeof(folded))||!equal8(folded,canonical))return 13;return 0;
}
static unsigned registry_count143(unsigned values){char root[256];registry_root143(root);unsigned count=0;v6_volume*volume=m6_volume();
 for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*entry=volume->entries+i;if(entry->kind!=1||!prefix8(entry->path,root))continue;const char*leaf=entry->path;for(unsigned n=0;entry->path[n];++n)if(entry->path[n]=='/')leaf=entry->path+n+1;
  if(values?leaf[0]=='v':equal8(leaf,"$key"))++count;
 }return count;
}
static unsigned registry_ensure_key143(const char*canonical,const char*display,registry_key_record143*scratch){
 char directory[256],path[256];registry_directory143(canonical,directory);unsigned error=registry_load_key143(canonical,directory,scratch);if(!error)return 0;if(error!=2)return error;
 if(registry_count143(0)>=REGISTRY_PERSISTED_KEYS148)return 1450;error=registry_prepare143(directory);if(error)return error;
 memset(scratch,0,sizeof(*scratch));scratch->magic=REGISTRY_KEY_MAGIC143;scratch->time=now8();copy8(scratch->user,registry_owner147(),256);copy8(scratch->canonical,canonical,768);copy8(scratch->display,display,768);
 copy8(path,directory,256);path_append143(path,"/$key",256);return v6_put(m6_volume(),path,sizeof(*scratch),memory_source8,scratch)?1117:0;
}
static unsigned registry_object_owned143(const registry_object143*object){
#ifdef ENGINE_M14
 return object&&equal8(object->app_owner,W8_NAMED_OWNER);
#else
 return object!=0;
#endif
}
static int registry_slot143(uint64_t handle){unsigned slot=(unsigned)(handle&31);registry_cap143*cap=spaces142[active_space142]->registry_handles+slot;
 return (handle&W8_HANDLE_TAG_MASK)==W8_REGISTRY_TAG143&&cap->live&&cap->generation==((handle&UINT64_C(0x1fffffff))>>5)&&cap->object<REGISTRY_KEYS143&&registry_object_owned143(registry_objects143[cap->object])?(int)slot:-1;
}
static unsigned registry_close143(uint64_t handle){if(registry_hkcu143(handle))return 0;int slot=registry_slot143(handle);if(slot<0)return 6;registry_cap143*cap=spaces142[active_space142]->registry_handles+slot;unsigned object=cap->object;cap->live=0;
 if(!--registry_objects143[object]->refs){registry_free143((uint64_t)(uintptr_t)registry_objects143[object]);registry_objects143[object]=0;}return 0;
}
static void registry_release143(void){for(unsigned i=0;i<32;++i){registry_cap143*cap=spaces142[active_space142]->registry_handles+i;if(cap->live){uint64_t handle=W8_REGISTRY_TAG143|((uint64_t)cap->generation<<5)|i;(void)registry_close143(handle);}}}
static unsigned registry_full_key143(uint64_t root,uint64_t name,unsigned access,unsigned create,char*display,char*canonical){
 if(access&~0xf003fu)return 50;display[0]=0;
 if(!registry_hkcu143(root)){int slot=registry_slot143(root);if(slot<0)return 6;registry_cap143*cap=spaces142[active_space142]->registry_handles+slot;registry_object143*object=registry_objects143[cap->object];if(object->deleted)return 1018;
  if((access&~cap->access)||(create&&!(cap->access&4)))return 5;copy8(display,object->record.display,768);
 }
 char relative[768];relative[0]=0;unsigned error=name?path_user_string143(name,relative,sizeof(relative)):0;if(error)return error;
 if(relative[0]){if(display[0]&&(error=path_append143(display,"\\",768)))return error;if((error=path_append143(display,relative,768)))return error;}
 unsigned depth=display[0]?1:0;for(unsigned i=0;display[i];++i)if(display[i]=='\\'){if(!i||!display[i+1]||display[i-1]=='\\')return 161;if(++depth>32)return 206;}
 return registry_fold143(display,canonical,768);
}
static unsigned registry_open143(const w8_registry_request143*request,unsigned create,w8_registry_result143*result){
 if(request->flags)return 50;char display[768],canonical[768];unsigned error=registry_full_key143(request->root,request->name,request->access,create,display,canonical);if(error)return error;
 unsigned cap_slot=0;while(cap_slot<32&&spaces142[active_space142]->registry_handles[cap_slot].live)++cap_slot;if(cap_slot==32||registry_generation143==0x7fffffu)return 8;
 unsigned object_slot=0;while(object_slot<REGISTRY_KEYS143){registry_object143*object=registry_objects143[object_slot];if(registry_object_owned143(object)&&!object->deleted&&equal8(object->record.user,registry_owner147())&&equal8(object->record.canonical,canonical))break;++object_slot;}
 unsigned existing_object=object_slot<REGISTRY_KEYS143;if(!existing_object){object_slot=0;while(object_slot<REGISTRY_KEYS143&&registry_objects143[object_slot])++object_slot;if(object_slot==REGISTRY_KEYS143)return 8;}
 uint64_t page=registry_page143();if(!page)return 8;registry_object143*loaded=(void*)(uintptr_t)page;registry_directory143(canonical,loaded->directory);
 error=registry_load_key143(canonical,loaded->directory,&loaded->record);unsigned existed=!error||!canonical[0];
 if(error==2&&create){
  /* Create each selected ancestor, retaining the first stored display spelling. */
  for(unsigned i=0;;++i){if(display[i]&&display[i]!='\\')continue;char save=display[i];display[i]=0;char folded[768];error=registry_fold143(display,folded,sizeof(folded));if(!error)error=registry_ensure_key143(folded,display,&loaded->record);display[i]=save;if(error||!save)break;}
  if(!error)error=registry_load_key143(canonical,loaded->directory,&loaded->record);
 }
 if(error==2&&!canonical[0]){error=0;loaded->record.magic=REGISTRY_KEY_MAGIC143;copy8(loaded->record.user,registry_owner147(),256);}
 if(error){registry_free143(page);return error;}
 if(existing_object)registry_free143(page);else{
#ifdef ENGINE_M14
  copy8(loaded->app_owner,W8_NAMED_OWNER,sizeof(loaded->app_owner));
#endif
  registry_objects143[object_slot]=loaded;
 }
 registry_cap143*cap=spaces142[active_space142]->registry_handles+cap_slot;*cap=(registry_cap143){1,++registry_generation143,object_slot,request->access};++registry_objects143[object_slot]->refs;
 result->handle=W8_REGISTRY_TAG143|((uint64_t)cap->generation<<5)|cap_slot;result->disposition=existed?2:1;return 0;
}
static unsigned registry_value_name143(registry_object143*object,uint64_t name,registry_value_record143*record,char*path){
 memset(record,0,sizeof(*record));record->magic=REGISTRY_VALUE_MAGIC143;copy8(record->user,registry_owner147(),256);copy8(record->key,object->record.canonical,768);
 unsigned error=name?path_user_string143(name,record->display,sizeof(record->display)):0;if(error)return error;if((error=registry_fold143(record->display,record->name,sizeof(record->name))))return error;
 char hash[33];registry_hash143(record->name,hash);copy8(path,object->directory,256);path_append143(path,"/v",256);path_append143(path,hash,256);return 0;
}
static unsigned registry_load_value143(const char*path,registry_value_record143*record){
 const v6_entry*entry=find8(path);if(!entry)return 2;if(entry->kind!=1||entry->size<offsetof(registry_value_record143,data)||entry->size>sizeof(*record)||v6_verify(m6_volume(),path))return 13;
 char expected_name[256];copy8(expected_name,record->name,256);char expected_key[768];copy8(expected_key,record->key,768);
 unsigned got=0;if(v6_read(m6_volume(),path,0,record,(unsigned)entry->size,&got)||got!=entry->size)return 13;
 if(record->magic!=REGISTRY_VALUE_MAGIC143||record->bytes>sizeof(record->data)||entry->size!=offsetof(registry_value_record143,data)+record->bytes||!terminated142(record->user,256)||!terminated142(record->key,768)||!terminated142(record->name,256)||!terminated142(record->display,256)||!equal8(record->user,registry_owner147())||!equal8(record->key,expected_key)||!equal8(record->name,expected_name))return 13;
 char folded[256];if(registry_fold143(record->display,folded,256)||!equal8(folded,record->name))return 13;return 0;
}
static unsigned registry_key_entry143(const v6_entry*entry,registry_key_record143*record){
 unsigned got=0;if(entry->kind!=1||entry->size!=sizeof(*record)||v6_verify(m6_volume(),entry->path)||v6_read(m6_volume(),entry->path,0,record,sizeof(*record),&got)||got!=sizeof(*record))return 13;
 if(record->magic!=REGISTRY_KEY_MAGIC143||!terminated142(record->user,256)||!terminated142(record->canonical,768)||!terminated142(record->display,768)||!equal8(record->user,registry_owner147()))return 13;
 char directory[256],folded[768];registry_directory143(record->canonical,directory);path_append143(directory,"/$key",256);
 if(!equal8(directory,entry->path)||registry_fold143(record->display,folded,768)||!equal8(folded,record->canonical))return 13;return 0;
}
static unsigned registry_child143(const registry_key_record143*parent,const registry_key_record143*child){
 unsigned n=length8(parent->canonical);const char*relative=child->canonical;
 if(n){if(memcmp(relative,parent->canonical,n)||relative[n]!='\\')return 0;relative+=n+1;}
 if(!*relative)return 0;for(unsigned i=0;relative[i];++i)if(relative[i]=='\\')return 0;return 1;
}
static unsigned registry_name_output143(const char*name,const w8_registry_request143*request,w8_registry_result143*result){
 uint16_t text[768];unsigned at=0,used=0,bytes=length8(name);while(at<bytes){uint32_t scalar;if(!decode_utf8_143(name,bytes,&at,&scalar)||!encode_utf16_143(scalar,text,767,&used))return 13;}text[used]=0;result->name_units=used;
 if(request->name_capacity<=used)return 234;if(!request->name_output)return 87;return user8(request->name_output,text,(used+1)*2,1)?998:0;
}
static unsigned registry_enum143(unsigned operation,registry_object143*object,const w8_registry_request143*request,w8_registry_result143*result,void*scratch){
 char root[256];registry_root143(root);unsigned selected=0;v6_volume*volume=m6_volume();
 for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*entry=volume->entries+i;if(entry->kind!=1)continue;
  const char*leaf=entry->path;for(unsigned n=0;entry->path[n];++n)if(entry->path[n]=='/')leaf=entry->path+n+1;
  if(operation==9){if(!prefix8(entry->path,root)||!equal8(leaf,"$key"))continue;registry_key_record143*key=scratch;unsigned error=registry_key_entry143(entry,key);if(error)return error;if(!registry_child143(&object->record,key))continue;if(selected++!=request->index)continue;
   const char*name=key->display;for(unsigned n=0;key->display[n];++n)if(key->display[n]=='\\')name=key->display+n+1;result->time=key->time;return registry_name_output143(name,request,result);
  }
  if(!prefix8(entry->path,object->directory)||leaf[0]!='v')continue;registry_value_record143*value=scratch;unsigned got=0;
  if(entry->size>sizeof(*value)||entry->size<offsetof(registry_value_record143,data)||v6_read(volume,entry->path,0,value,(unsigned)entry->size,&got)||got!=entry->size||!terminated142(value->name,256)||!terminated142(value->key,768)||!equal8(value->key,object->record.canonical))return 13;
  char expected[256],hash[33];registry_hash143(value->name,hash);copy8(expected,object->directory,256);path_append143(expected,"/v",256);path_append143(expected,hash,256);if(!equal8(expected,entry->path))return 13;
  unsigned error=registry_load_value143(entry->path,value);if(error)return error;if(selected++!=request->index)continue;result->type=value->type;result->bytes=value->bytes;
  error=registry_name_output143(value->display,request,result);if(error)return error;if(request->data){if(request->bytes<value->bytes)return 234;if(value->bytes&&user8(request->data,value->data,value->bytes,1))return 998;}return 0;
 }return 259;
}
static unsigned registry_delete_key143(const w8_registry_request143*request,void*scratch){
 char display[768],canonical[768];unsigned error=registry_full_key143(request->root,request->name,0,0,display,canonical);if(error)return error;if(!canonical[0])return 5;
 if(!registry_hkcu143(request->root)){int slot=registry_slot143(request->root);if(slot<0)return 6;if(!(spaces142[active_space142]->registry_handles[slot].access&0x10000u))return 5;}
 char directory[256],path[256];registry_directory143(canonical,directory);registry_key_record143*record=scratch;error=registry_load_key143(canonical,directory,record);if(error)return error;
 char root[256];registry_root143(root);v6_volume*volume=m6_volume();
 for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*entry=volume->entries+i;if(entry->kind!=1||!prefix8(entry->path,root))continue;const char*leaf=entry->path;for(unsigned n=0;entry->path[n];++n)if(entry->path[n]=='/')leaf=entry->path+n+1;if(!equal8(leaf,"$key"))continue;
  error=registry_key_entry143(entry,record);if(error)return error;unsigned n=length8(canonical);if(!memcmp(record->canonical,canonical,n)&&record->canonical[n]=='\\')return 5;
 }
 for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*entry=volume->entries+i;if(entry->kind==1&&prefix8(entry->path,directory)){const char*leaf=entry->path;for(unsigned n=0;entry->path[n];++n)if(entry->path[n]=='/')leaf=entry->path+n+1;if(equal8(leaf,"$key"))continue;if(leaf[0]!='v')return 13;copy8(path,entry->path,256);if(v6_remove(volume,path))return 1117;}}
 copy8(path,directory,256);path_append143(path,"/$key",256);if(v6_remove(volume,path))return 1117;
 for(unsigned i=0;i<REGISTRY_KEYS143;++i){registry_object143*object=registry_objects143[i];if(registry_object_owned143(object)&&equal8(object->record.user,registry_owner147())&&equal8(object->record.canonical,canonical))object->deleted=1;}
 return v6_remove(volume,directory)?1117:0;
}
#include "registry-info148.inc"
static int64_t registry_syscall143(uint64_t operation,uint64_t address){
 w8_registry_request143 request;w8_registry_result143 result={0};if(user8(address,&request,sizeof(request),0))return -998;
#ifdef ENGINE_M14
 registry_machine147=0;unsigned view=request.access&0x300u;if(view==0x300u)return -87;request.access&=~0x300u;
 if(registry_hklm147(request.root))registry_machine147=view==0x200u?2:1;
 else if(registry_hkcu143(request.root)){if(view)return -50;}
 else {int selected=registry_slot143(request.root);if(selected<0)return -6;const char*owner=registry_objects143[spaces142[active_space142]->registry_handles[selected].object]->record.user;
  if(equal8(owner,"/Machine/64"))registry_machine147=1;else if(equal8(owner,"/Machine/32"))registry_machine147=2;
  if(view&&registry_machine147&&registry_machine147!=(view==0x200u?2u:1u))return -50;
 }
 /* Machine writes require the owner-confirmed install/remove worker context.
  * Ordinary applications can read both views but cannot obtain write grants. */
 if(registry_machine147&&(!installer_authority147()||spaces142[active_space142]->exe_context148)){
  if(operation==2||operation==3||operation==6||operation==10||((operation==1)&&(request.access&~0x20019u)))return -5;
 }
#endif
 if(operation==11){if(request.flags||request.name||request.data||!request.result)return -87;result.type=registry_count143(0);result.bytes=registry_count143(1);result.name_units=REGISTRY_PERSISTED_KEYS148;result.disposition=REGISTRY_VALUES143;return user8(request.result,&result,sizeof(result),1)?-998:0;}
 if(operation==1||operation==2){if(!request.result)return -87;if(user8(request.result,&result,sizeof(result),1))return -998;unsigned error=registry_open143(&request,operation==2,&result);if(error)return -(int64_t)error;if(user8(request.result,&result,sizeof(result),1)){(void)registry_close143(result.handle);return -998;}return 0;}
 if(request.flags)return -87;
 if(operation==5)return -(int64_t)registry_close143(request.root);
 if(operation==10){uint64_t temporary=registry_page143();if(!temporary)return -8;unsigned error=registry_delete_key143(&request,(void*)(uintptr_t)temporary);registry_free143(temporary);return -(int64_t)error;}
 int slot=registry_slot143(request.root);if(slot<0)return -6;registry_cap143*cap=spaces142[active_space142]->registry_handles+slot;registry_object143*object=registry_objects143[cap->object];if(object->deleted)return -1018;
 if(operation==8)return cap->access&1?0:-5;
 if(operation==12){if(!(cap->access&1))return -5;if(request.bytes!=sizeof(w8_registry_info148)||!request.data||request.name||request.result)return -87;uint64_t page=registry_page143();if(!page)return -8;w8_registry_info148 info;unsigned error=registry_info148(object,&info,(void*)(uintptr_t)page);registry_free143(page);if(!error&&user8(request.data,&info,sizeof(info),1))error=998;return -(int64_t)error;}
 if(operation==7||operation==9){if(!(cap->access&(operation==7?1u:8u)))return -5;uint64_t temporary=registry_page143();if(!temporary)return -8;unsigned error=registry_enum143((unsigned)operation,object,&request,&result,(void*)(uintptr_t)temporary);if(request.result&&user8(request.result,&result,sizeof(result),1))error=998;registry_free143(temporary);return -(int64_t)error;}
 if(operation!=3&&operation!=4&&operation!=6)return -50;
 if(!(cap->access&(operation==4?1u:2u)))return -5;
 uint64_t page=registry_page143();if(!page)return -8;registry_value_record143*value=(void*)(uintptr_t)page;char path[256];unsigned error=registry_value_name143(object,request.name,value,path);
 if(!error&&operation==3){
  if(request.flags||(!request.data&&request.bytes))error=87;else if(request.bytes>sizeof(value->data))error=1450;
  else{const v6_entry*entry=find8(path);if(entry){error=registry_load_value143(path,value);if(!error)error=registry_value_name143(object,request.name,value,path);}else if(registry_count143(1)>=REGISTRY_VALUES143)error=1450;
   if(!error&&request.bytes&&user8(request.data,value->data,request.bytes,0))error=998;
   if(!error){value->type=request.type;value->bytes=request.bytes;error=registry_ensure_key143(object->record.canonical,object->record.display,(void*)value);
    /* Key serialization used the scratch page; rebuild value identity and bytes. */
    if(!error)error=registry_value_name143(object,request.name,value,path);if(!error&&request.bytes&&user8(request.data,value->data,request.bytes,0))error=998;
    if(!error){value->type=request.type;value->bytes=request.bytes;if(v6_put(m6_volume(),path,offsetof(registry_value_record143,data)+value->bytes,memory_source8,value))error=1117;}}
  }
 }else if(!error){error=registry_load_value143(path,value);if(!error&&operation==6){if(v6_remove(m6_volume(),path))error=1117;}
  else if(!error){result.type=value->type;result.bytes=value->bytes;if(request.result&&user8(request.result,&result,sizeof(result),1))error=998;
   if(!error&&request.data){if(request.bytes<value->bytes)error=234;else if(value->bytes&&user8(request.data,value->data,value->bytes,1))error=998;}}
 }
 registry_free143(page);return -(int64_t)error;
}
