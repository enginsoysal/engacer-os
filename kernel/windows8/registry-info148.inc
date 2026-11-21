/* Query real key/value metadata in one bounded directory-table traversal. */
static unsigned registry_units148(const char*text){unsigned bytes=length8(text),at=0,units=0;while(at<bytes){uint32_t scalar;if(!decode_utf8_143(text,bytes,&at,&scalar))return UINT32_MAX;units+=scalar>0xffff?2:1;}return units;}
static unsigned registry_info148(registry_object143*object,w8_registry_info148*out,void*scratch){
 memset(out,0,sizeof(*out));char root[256];registry_root143(root);v6_volume*volume=m6_volume();
 for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*entry=volume->entries+i;if(entry->kind!=1||!prefix8(entry->path,root))continue;const char*leaf=entry->path;for(unsigned n=0;entry->path[n];++n)if(entry->path[n]=='/')leaf=entry->path+n+1;
  if(equal8(leaf,"$key")){registry_key_record143*key=scratch;unsigned error=registry_key_entry143(entry,key);if(error)return error;if(!registry_child143(&object->record,key))continue;const char*name=key->display;for(unsigned n=0;key->display[n];++n)if(key->display[n]=='\\')name=key->display+n+1;unsigned units=registry_units148(name);if(units==UINT32_MAX)return 13;++out->subkeys;if(units>out->max_subkey_units)out->max_subkey_units=units;}
  else if(prefix8(entry->path,object->directory)&&leaf[0]=='v'){registry_value_record143*value=scratch;unsigned got=0;if(entry->size>sizeof(*value)||entry->size<offsetof(registry_value_record143,data)||v6_read(volume,entry->path,0,value,(unsigned)entry->size,&got)||got!=entry->size||!terminated142(value->key,768)||!terminated142(value->name,256)||!equal8(value->key,object->record.canonical))return 13;
   char expected[256],hash[33];registry_hash143(value->name,hash);copy8(expected,object->directory,256);path_append143(expected,"/v",256);path_append143(expected,hash,256);if(!equal8(expected,entry->path))return 13;unsigned error=registry_load_value143(entry->path,value);if(error)return error;unsigned units=registry_units148(value->display);if(units==UINT32_MAX)return 13;++out->values;if(units>out->max_value_name_units)out->max_value_name_units=units;if(value->bytes>out->max_value_bytes)out->max_value_bytes=value->bytes;
  }
 }return 0;
}
