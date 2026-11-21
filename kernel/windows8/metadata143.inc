/* File-owned metadata records do not live in an application's install directory. */
#define FILE_METADATA_MAGIC143 UINT64_C(0x314d464e4534314d)
typedef struct {uint64_t magic;char user[256],path[256];uint64_t times[3];uint32_t attributes,reserved;} file_metadata143;
static unsigned metadata_scope148(const char*path){
 if(prefix8(path,input8.user_root))return 1;
#ifdef ENGINE_M14
 /* This scope stores metadata only; file effects still require path8 grants. */
 if(input8.product_root[0]&&prefix8(path,input8.product_root))return 1;
#endif
 return 0;
}
static void metadata_path143(const char*path,char*out){char hash[33];protected_root143("Files",out);protected_hash143(path,hash);path_append143(out,"/m",256);path_append143(out,hash,256);}
static void metadata_default143(const char*path,unsigned kind,file_metadata143*out){memset(out,0,sizeof(*out));out->magic=FILE_METADATA_MAGIC143;copy8(out->user,input8.user_root,256);copy8(out->path,path,256);out->attributes=kind==2?16:32;for(unsigned i=0;i<3;++i)out->times[i]=UINT64_C(119600064000000000);}
static unsigned metadata_load143(const char*path,unsigned kind,file_metadata143*out){
 metadata_default143(path,kind,out);if(!metadata_scope148(path))return 0;char source[256];metadata_path143(path,source);const v6_entry*entry=find8(source);if(!entry)return 0;
 unsigned got=0;if(entry->kind!=1||entry->size!=sizeof(*out)||v6_verify(m6_volume(),source)||v6_read(m6_volume(),source,0,out,sizeof(*out),&got)||got!=sizeof(*out))return 13;
 if(out->magic!=FILE_METADATA_MAGIC143||out->reserved||!terminated142(out->user,256)||!terminated142(out->path,256)||!equal8(out->user,input8.user_root)||!equal8(out->path,path)||(out->attributes&~0xb7u)||(kind&&((out->attributes&16)!=0)!=(kind==2)))return 13;return 0;
}
static unsigned metadata_save143(const file_metadata143*record){
 if(!metadata_scope148(record->path))return 5;char directory[256],path[256];protected_root143("Files",directory);unsigned error=protected_prepare143(directory);if(error)return error;
 metadata_path143(record->path,path);const v6_entry*existing=find8(path);if(existing){file_metadata143 check;error=metadata_load143(record->path,(record->attributes&16)?2:1,&check);if(error)return error;}
 return v6_put(m6_volume(),path,sizeof(*record),memory_source8,(void*)record)?1117:0;
}
static unsigned metadata_remove143(const char*path){if(!metadata_scope148(path))return 0;char source[256];metadata_path143(path,source);if(!find8(source))return 0;file_metadata143 check;unsigned error=metadata_load143(path,0,&check);if(error)return error;return v6_remove(m6_volume(),source)?1117:0;}
