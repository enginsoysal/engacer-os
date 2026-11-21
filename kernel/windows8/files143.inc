/* Shared file identities, per-process grants and bounded sparse dirty pages.
 * All callers run on the one Windows worker CPU with syscall serialization. */
#define FILE_OBJECTS143 128u
#define FILE_DIRTY_LIMIT143 2048u
typedef struct {uint32_t index,pad;uint64_t page;} file_dirty_entry143;
typedef struct file_dirty_chunk143 {uint64_t next;unsigned count,pad;file_dirty_entry143 entries[255];} file_dirty_chunk143;
_Static_assert(sizeof(file_dirty_chunk143)==4096,"Dirty directory must occupy one page");
typedef struct {uint64_t offset,length;unsigned owner,exclusive,live,reserved;} file_lock143;
typedef struct {char path[256];uint64_t size,backing_size,chunks;unsigned refs,dirty,existed,crc,delete_pending,staged,metadata_dirty;file_metadata143 metadata;file_lock143 locks[16];} file_object143;
_Static_assert(sizeof(file_object143)<=4096,"File identity exceeds one owned page");
static file_object143 *file_objects143[FILE_OBJECTS143];
static unsigned file_generation143,file_dirty_pages143;
static void file_refresh_waits143(void);
static unsigned file_overlap143(uint64_t a,uint64_t an,uint64_t b,uint64_t bn){return an&&bn&&a<b+bn&&b<a+an;}
static unsigned file_io_lock143(file_object143*object,unsigned owner,uint64_t offset,unsigned bytes,unsigned write){
 for(unsigned i=0;i<16;++i){file_lock143*lock=object->locks+i;if(lock->live&&file_overlap143(offset,bytes,lock->offset,lock->length)&&((lock->exclusive&&lock->owner!=owner)||(write&&!lock->exclusive)))return 33;}return 0;
}
static void file_account143(int delta){if(delta>0)file_resident143+=(unsigned)delta;else file_resident143-=(unsigned)-delta;group_peak142();}
static uint64_t file_page143(void){if(file_resident143>=FILE_DIRTY_LIMIT143+256||file_resident143-file_dirty_pages143>=256)return 0;uint64_t page=page_alloc();if(page){memset((void*)(uintptr_t)page,0,4096);file_account143(1);}return page;}
static void file_free_page143(uint64_t page){page_free(page);file_account143(-1);}
static void file_clear_dirty143(file_object143*object){
 uint64_t next=object->chunks;object->chunks=0;
 while(next){file_dirty_chunk143*chunk=(void*)(uintptr_t)next;uint64_t old=next;next=chunk->next;
  for(unsigned i=0;i<chunk->count;++i)if(chunk->entries[i].page){file_free_page143(chunk->entries[i].page);--file_dirty_pages143;}
  file_free_page143(old);
 }
}
static uint64_t file_dirty143(file_object143*object,unsigned index,unsigned create){
 file_dirty_chunk143*available=0;
 for(uint64_t at=object->chunks;at;){file_dirty_chunk143*chunk=(void*)(uintptr_t)at;
  for(unsigned i=0;i<chunk->count;++i){if(chunk->entries[i].page&&chunk->entries[i].index==index)return chunk->entries[i].page;if(!chunk->entries[i].page&&!available)available=chunk;}
  if(chunk->count<255&&!available)available=chunk;at=chunk->next;
 }
 if(!create||file_dirty_pages143==FILE_DIRTY_LIMIT143)return 0;
 uint64_t page=file_page143();if(!page)return 0;
 uint64_t offset=(uint64_t)index*4096;
 if(offset<object->backing_size){unsigned got=0,bytes=(unsigned)(object->backing_size-offset);if(bytes>4096)bytes=4096;
  if(v6_read(m6_volume(),object->path,offset,(void*)(uintptr_t)page,bytes,&got)||got!=bytes){file_free_page143(page);return 0;}}
 if(!available){uint64_t chunk_page=file_page143();if(!chunk_page){file_free_page143(page);return 0;}
  available=(void*)(uintptr_t)chunk_page;available->next=object->chunks;object->chunks=chunk_page;}
 unsigned slot=0;while(slot<available->count&&available->entries[slot].page)++slot;if(slot==available->count)++available->count;
 available->entries[slot]=(file_dirty_entry143){index,0,page};++file_dirty_pages143;return page;
}
static unsigned file_source143(void*context,uint64_t offset,void*out,unsigned bytes){
 file_object143*object=context;uint8_t*destination=out;
 while(bytes){unsigned part=4096-(unsigned)(offset&4095);if(part>bytes)part=bytes;
  uint64_t page=file_dirty143(object,(unsigned)(offset/4096),0);
  if(page)memcpy(destination,(void*)(uintptr_t)(page+(offset&4095)),part);
  else{memset(destination,0,part);if(offset<object->backing_size){unsigned got=0,read=(unsigned)(object->backing_size-offset);if(read>part)read=part;
    if(v6_read(m6_volume(),object->path,offset,destination,read,&got)||got!=read)return 1;}}
  offset+=part;destination+=part;bytes-=part;
 }return 0;
}
static unsigned file_flush_metadata143(file_object143*object){if(!object->metadata_dirty)return 0;unsigned error=metadata_save143(&object->metadata);if(!error)object->metadata_dirty=0;return error;}
static unsigned file_set_metadata143(file_object143*object,const w8_file_info*information){
 if(information->attributes&~0xa7u)return 50;file_metadata143 previous=object->metadata;unsigned dirty=object->metadata_dirty;
 if(!memcmp(previous.times,information->time,sizeof(previous.times))&&previous.attributes==information->attributes)return 0;
 memcpy(object->metadata.times,information->time,sizeof(object->metadata.times));object->metadata.attributes=information->attributes?information->attributes:128;object->metadata_dirty=1;
 unsigned error=file_flush_metadata143(object);if(error){object->metadata=previous;object->metadata_dirty=dirty;}return error;
}
static void file_modified143(file_object143*object){if(!prefix8(object->path,input8.user_root))return;uint64_t time=now8();unsigned attributes=(object->metadata.attributes&~128u)|32;if(time!=object->metadata.times[2]||attributes!=object->metadata.attributes){object->metadata.times[2]=time;object->metadata.attributes=attributes;object->metadata_dirty=1;}}
static unsigned file_flush143(file_object143*object){
 if(!object->dirty)return file_flush_metadata143(object);const v6_entry*entry=find8(object->path);
 if((entry&&!object->existed)||(!entry&&object->existed)||(entry&&(entry->kind!=1||entry->crc!=object->crc)))return 1117;
 if(v6_put(m6_volume(),object->path,object->size,file_source143,object))return 1117;
 entry=find8(object->path);if(!entry)return 1117;object->existed=1;object->crc=entry->crc;object->backing_size=object->size;object->dirty=0;object->staged=0;file_clear_dirty143(object);return file_flush_metadata143(object);
}
static unsigned file_object_slot143(const char*path){for(unsigned i=0;i<FILE_OBJECTS143;++i)if(file_objects143[i]&&equal8(file_objects143[i]->path,path))return i;return FILE_OBJECTS143;}
static unsigned file_sharing143(unsigned object,unsigned access,unsigned share){
 if(!(access&7))return 0;
 for(unsigned process=0;process<SPACES142;++process){if(!spaces142[process])continue;
  for(unsigned i=0;i<32;++i){file8*grant=spaces142[process]->files+i;
   if(grant->live&&(grant->access&7)&&grant->object==object&&(((access&7)&~grant->share)||((grant->access&7)&~share)))return 32;
  }
 }return 0;
}
static unsigned file_resize143(file_object143*object,uint64_t size){
 if(size>64*1024*1024)return 223;
 if(size<object->size){
  /* A zero tail is retained in a dirty page so later growth cannot expose data. */
  if(size&4095){uint64_t page=file_dirty143(object,(unsigned)(size/4096),1);if(!page)return 8;memset((void*)(uintptr_t)(page+(size&4095)),0,4096-(unsigned)(size&4095));}
  for(uint64_t at=object->chunks;at;){file_dirty_chunk143*chunk=(void*)(uintptr_t)at;
   for(unsigned i=0;i<chunk->count;++i)if(chunk->entries[i].page&&(uint64_t)chunk->entries[i].index*4096>=size){file_free_page143(chunk->entries[i].page);chunk->entries[i].page=0;--file_dirty_pages143;}at=chunk->next;}
  if(object->backing_size>size)object->backing_size=size;
 }object->size=size;object->dirty=1;file_modified143(object);return 0;
}
static int64_t file_open143(const char*path,unsigned access,unsigned share,unsigned creation,unsigned flags,unsigned legacy){
 if(access&~31u||share&~7u||creation<1||creation>5)return -87;
 if(!path8(path,0)||((access&22)&&!path8(path,1)))return -5;
 if(flags&~0x040000a7u)return -50;if((flags&0x04000000u)&&!(access&4))return -5;
 const v6_entry*entry=find8(path);unsigned object=file_object_slot143(path);file_object143*value=object<FILE_OBJECTS143?file_objects143[object]:0;
 unsigned exists=entry||value;
 if(value&&value->delete_pending)return -303;
 if(exists&&creation==1)return -80;if(!exists&&(creation==3||creation==5))return -2;
 if(entry&&entry->kind!=1)return -5;if((creation==2||creation==5)&&!(access&2))return -5;
 if(!exists){if(!path8(path,1))return -5;char parent[256];copy8(parent,path,256);unsigned n=length8(parent);while(n&&parent[n-1]!='/')--n;if(!n)return -3;parent[n-1]=0;const v6_entry*directory=find8(parent);if(!directory||directory->kind!=2)return -3;}
 if(legacy&&input8.command==W8_INSTALL&&exists&&access&2)return -80;
 if(value){unsigned error=file_sharing143(object,access,share);if(error)return -(int64_t)error;}
 unsigned slot=0;while(slot<32&&files8[slot].live)++slot;if(slot==32||file_generation143==0x7fffffu)return -4;
 unsigned allocated=0;if(!value){object=0;while(object<FILE_OBJECTS143&&file_objects143[object])++object;if(object==FILE_OBJECTS143)return -4;
  if(entry&&v6_verify(m6_volume(),path))return -23;
  uint64_t page=file_page143();if(!page)return -8;value=(void*)(uintptr_t)page;copy8(value->path,path,256);
  value->size=value->backing_size=entry?entry->size:0;value->existed=entry!=0;value->crc=entry?entry->crc:0;
  unsigned error=metadata_load143(path,1,&value->metadata);if(error&&entry){file_free_page143(page);return -(int64_t)error;}
  if(!entry){metadata_default143(path,1,&value->metadata);for(unsigned i=0;i<3;++i)value->metadata.times[i]=now8();unsigned attributes=flags&0xa7u;value->metadata.attributes=(attributes&~128u)?attributes&~128u:32;value->metadata_dirty=prefix8(path,input8.user_root);}
  if(entry&&((access&2)||(flags&0x04000000u))&&(value->metadata.attributes&1)){file_free_page143(page);return -5;}
  file_objects143[object]=value;allocated=1;
 }
 if(exists&&((access&2)||(flags&0x04000000u))&&(value->metadata.attributes&1))return -5;
 unsigned error=0;
 if(!exists){value->dirty=1;value->staged=legacy!=0;if(!legacy)error=file_flush143(value);}
 if(!error&&(creation==2||creation==5))error=file_resize143(value,0);
 if(error){if(allocated){if(!exists&&!legacy&&value->existed&&v6_remove(m6_volume(),path))error=1117;file_clear_dirty143(value);file_objects143[object]=0;file_free_page143((uint64_t)(uintptr_t)value);}return -(int64_t)error;}
 file8*grant=files8+slot;memset(grant,0,sizeof(*grant));grant->live=1;grant->write=(access&2)!=0;grant->access=access;grant->share=share;grant->object=object;grant->generation=++file_generation143;
 grant->size=value->size;grant->legacy=legacy;copy8(grant->path,path,256);++value->refs;if(flags&0x04000000u)value->delete_pending=1;
 return slot;
}
static uint64_t file_token143(unsigned slot){return W8_FILE_TAG143|((uint64_t)files8[slot].generation<<5)|slot;}
static int file_handle143(uint64_t handle){unsigned slot=(unsigned)(handle&31);return (handle&UINT64_C(0xfffffffff0000000))==W8_FILE_TAG143&&files8[slot].live&&!files8[slot].legacy&&files8[slot].generation==((handle&0x0fffffffu)>>5)?(int)slot:-1;}
static unsigned close8(unsigned slot,unsigned commit){
 if(slot>=32||!files8[slot].live)return 6;file8*grant=files8+slot;unsigned object=grant->object;file_object143*value=file_objects143[object];
 unsigned error=commit&&grant->write?file_flush143(value):0;if(error)return error;
 for(unsigned i=0;i<16;++i)if(value->locks[i].live&&value->locks[i].owner==grant->generation)memset(value->locks+i,0,sizeof(file_lock143));
 memset(grant,0,sizeof(*grant));if(--value->refs){file_refresh_waits143();return 0;}
 if(value->delete_pending&&value->existed){if(v6_remove(m6_volume(),value->path))error=1117;else error=metadata_remove143(value->path);}
 file_clear_dirty143(value);file_objects143[object]=0;file_free_page143((uint64_t)(uintptr_t)value);file_refresh_waits143();return error;
}
static void file_release143(void){for(unsigned i=0;i<32;++i)if(files8[i].live)(void)close8(i,0);}
static int64_t file_read143(unsigned slot,uint64_t output,unsigned bytes){
 if(slot>=32||!files8[slot].live)return -6;file8*grant=files8+slot;if(!(grant->access&1))return -5;if(bytes>4096)return -87;
 file_object143*value=file_objects143[grant->object];unsigned count=0;if(grant->position<value->size){uint64_t remaining=value->size-grant->position;count=remaining<bytes?(unsigned)remaining:bytes;}
 unsigned error=file_io_lock143(value,grant->generation,grant->position,count,0);if(error)return -(int64_t)error;
 if(file_source143(value,grant->position,io8,count))return -30;if(count&&user8(output,io8,count,1))return -998;grant->position+=count;return count;
}
static int64_t file_write143(unsigned slot,uint64_t input,unsigned bytes){
 if(slot>=32||!files8[slot].live)return -6;file8*grant=files8+slot;if(!(grant->access&2))return -5;
 if(bytes>4096)return -87;if(grant->position>64*1024*1024||bytes>64*1024*1024-grant->position)return -223;
 if(bytes&&user8(input,io8,bytes,0))return -998;if(!bytes)return 0;file_object143*value=file_objects143[grant->object];
 unsigned error=file_io_lock143(value,grant->generation,grant->position,bytes,1);if(error)return -(int64_t)error;
 /* At most two pages are touched. Reserve both before changing visible bytes. */
 unsigned first=(unsigned)(grant->position/4096),last=(unsigned)((grant->position+bytes-1)/4096);
 uint64_t pages[2];pages[0]=file_dirty143(value,first,1);pages[1]=last==first?pages[0]:file_dirty143(value,last,1);if(!pages[0]||!pages[1])return -8;
 unsigned offset=(unsigned)(grant->position&4095),part=4096-offset;if(part>bytes)part=bytes;
 memcpy((void*)(uintptr_t)(pages[0]+offset),io8,part);if(part<bytes)memcpy((void*)(uintptr_t)pages[1],io8+part,bytes-part);
 grant->position+=bytes;if(grant->position>value->size)value->size=grant->position;value->dirty=1;file_modified143(value);return bytes;
}
static int64_t file_seek143(unsigned slot,int64_t offset,unsigned method){
 if(slot>=32||!files8[slot].live)return -6;if(method>2)return -87;file8*grant=files8+slot;file_object143*value=file_objects143[grant->object];
 int64_t base=method==0?0:method==1?(int64_t)grant->position:(int64_t)value->size,position;
 if(__builtin_add_overflow(base,offset,&position)||position<0||position>64*1024*1024)return -87;grant->position=(uint64_t)position;return position;
}
static unsigned file_try_lock143(unsigned slot,uint64_t offset,uint64_t length,unsigned exclusive){
 file8*grant=files8+slot;if(!(grant->access&3))return 5;file_object143*object=file_objects143[grant->object];unsigned empty=16;
 for(unsigned i=0;i<16;++i){file_lock143*lock=object->locks+i;if(!lock->live){if(empty==16)empty=i;continue;}
  if(file_overlap143(offset,length,lock->offset,lock->length)&&(exclusive||(lock->exclusive&&lock->owner!=grant->generation)))return 33;}
 if(empty==16)return 8;object->locks[empty]=(file_lock143){offset,length,grant->generation,exclusive,1,0};return 0;
}
static void file_refresh_waits143(void){
 unsigned saved=active_space142;
 for(unsigned process=0;process<SPACES142;++process){if(!spaces142[process])continue;active_space142=process;
  for(unsigned i=0;i<THREADS142;++i){thread142*thread=threads142+i;if(thread->state!=T143_FILELOCK)continue;
   int slot=file_handle143(thread->wait_handles[0]);unsigned error=slot<0?6:file_try_lock143((unsigned)slot,thread->wait_handles[1],thread->wait_handles[2],thread->wait_all);
   if(error!=33){thread->state=T142_READY;thread->frame.rax=(uint64_t)-(int64_t)error;}
  }
 }active_space142=saved;
}
static int64_t file_lock_call143(trap_frame*frame,unsigned slot,uint64_t handle,uint64_t address,unsigned unlock){
 w8_file_lock_request143 request;if(user8(address,&request,sizeof(request),0))return -998;
 if(request.reserved||(request.flags&~3u)||!request.length||request.length>UINT64_MAX-request.offset)return -87;
 if(unlock){file_object143*object=file_objects143[files8[slot].object];unsigned selected=16;for(unsigned i=0;i<16;++i){file_lock143*lock=object->locks+i;
   if(lock->live&&lock->owner==files8[slot].generation&&lock->offset==request.offset&&lock->length==request.length){selected=i;if(lock->exclusive)break;}}
  if(selected==16)return -158;memset(object->locks+selected,0,sizeof(file_lock143));file_refresh_waits143();return 0;
 }
 unsigned error=file_try_lock143(slot,request.offset,request.length,(request.flags&2)!=0);if(error!=33||(request.flags&1))return -(int64_t)error;
 thread142*thread=threads142+current142;thread->wait_handles[0]=handle;thread->wait_handles[1]=request.offset;thread->wait_handles[2]=request.length;thread->wait_all=(request.flags&2)!=0;thread->state=T143_FILELOCK;thread->deadline=UINT64_MAX;
 context8=*frame;context8.rax=0;w8_active=0;w8_escape();
}
static unsigned file_delete143(const char*path){
 if(!path8(path,1))return 5;const v6_entry*entry=find8(path);if(!entry)return 2;
 unsigned object=file_object_slot143(path);
 file_metadata143 metadata;unsigned error=0;if(object<FILE_OBJECTS143)metadata=file_objects143[object]->metadata;else error=metadata_load143(path,entry->kind,&metadata);if(error)return error;if(entry->kind==1&&(metadata.attributes&1))return 5;
 if(object<FILE_OBJECTS143){file_object143*value=file_objects143[object];if(value->delete_pending)return 303;
  unsigned error=file_sharing143(object,4,7);if(error)return error;value->delete_pending=1;return 0;}
 if(entry->kind==2){for(unsigned i=0;i<FILE_OBJECTS143;++i)if(file_objects143[i]&&prefix8(file_objects143[i]->path,path))return 32;}
 if(v6_remove(m6_volume(),path))return 1117;return metadata_remove143(path);
}
static unsigned file_move143(const char*source,const char*destination,unsigned replace){
 if(replace>1)return 87;if(!path8(source,1)||!path8(destination,1))return 5;
 const v6_entry*entry=find8(source);if(!entry)return 2;if(equal8(source,destination))return 0;
 unsigned source_slot=file_object_slot143(source),target_slot=file_object_slot143(destination);
 if(source_slot<FILE_OBJECTS143){file_object143*value=file_objects143[source_slot];if(value->delete_pending)return 303;unsigned error=file_sharing143(source_slot,4,7);if(error)return error;}
 if(target_slot<FILE_OBJECTS143)return 32;
 if(find8(destination)&&!replace)return 183;
 if(entry->kind!=1)return 50;
 char parent[256];copy8(parent,destination,256);unsigned length=length8(parent);while(length&&parent[length-1]!='/')--length;if(!length)return 3;parent[length-1]=0;const v6_entry*directory=find8(parent);if(!directory||directory->kind!=2)return 3;
 if(source_slot<FILE_OBJECTS143){unsigned error=file_flush143(file_objects143[source_slot]);if(error)return error;}
 file_metadata143 metadata,old_target;unsigned error=metadata_load143(source,1,&metadata);if(error)return error;
 error=metadata_load143(destination,1,&old_target);if(error)return error;const v6_entry*target=find8(destination);if(target&&(old_target.attributes&1))return 5;
 char target_record[256];metadata_path143(destination,target_record);unsigned had_target_record=find8(target_record)!=0;copy8(metadata.path,destination,256);error=metadata_save143(&metadata);if(error)return error;
 if(v6_rename(m6_volume(),source,destination,replace)){unsigned restore=had_target_record?metadata_save143(&old_target):metadata_remove143(destination);return restore?restore:1117;}
 if(source_slot<FILE_OBJECTS143){copy8(file_objects143[source_slot]->path,destination,256);file_objects143[source_slot]->metadata=metadata;file_objects143[source_slot]->metadata_dirty=0;}
 for(unsigned process=0;process<SPACES142;++process){if(!spaces142[process])continue;
  for(unsigned i=0;i<32;++i)if(spaces142[process]->files[i].live&&equal8(spaces142[process]->files[i].path,source))copy8(spaces142[process]->files[i].path,destination,256);
 }return metadata_remove143(source);
}
static unsigned file_attributes143(const char*path,unsigned attributes){
 if(!path8(path,1))return 5;if(attributes&~0xb7u)return 50;const v6_entry*entry=find8(path);if(!entry)return 2;
 unsigned object=file_object_slot143(path);file_metadata143 record;unsigned error=0;if(object<FILE_OBJECTS143)record=file_objects143[object]->metadata;else error=metadata_load143(path,entry->kind,&record);if(error)return error;
 unsigned selected=attributes&0xa7u;if(!selected)selected=128;if((selected&~128u)||entry->kind==2)selected&=~128u;selected|=entry->kind==2?16u:0u;if(selected==record.attributes)return 0;record.attributes=selected;error=metadata_save143(&record);
 if(!error&&object<FILE_OBJECTS143){file_objects143[object]->metadata=record;file_objects143[object]->metadata_dirty=0;}return error;
}

#ifdef ENGINE_M14
/* Stream directly into one checked copy-on-write extent; no dirty-page growth. */
static int64_t file_copy148(unsigned destination,uint64_t source){
 int input=file_handle143(source);if(input<0||destination>=32||!files8[destination].live)return -6;
 file8*in=files8+input,*out=files8+destination;
 if(!(in->access&1)||!(out->access&2)||!path8(in->path,0)||!path8(out->path,1))return -5;
 if(in->object==out->object)return -32;
 file_object143*from=file_objects143[in->object],*to=file_objects143[out->object];
 if(from->size>64*1024*1024)return -223;
 unsigned error=file_io_lock143(from,in->generation,0,(unsigned)from->size,0);
 if(!error)error=file_io_lock143(to,out->generation,0,(unsigned)from->size,1);if(error)return -(int64_t)error;
 const v6_entry*previous=find8(to->path);
 if((previous&&!to->existed)||(!previous&&to->existed)||(previous&&(previous->kind!=1||previous->crc!=to->crc)))return -1117;
 unsigned status=v6_put(m6_volume(),to->path,from->size,file_source143,from);
 if(status)return status==V6_FULL?-112:status==V6_RO?-19:-1117;
 const v6_entry*entry=find8(to->path);if(!entry)return -1117;
 file_clear_dirty143(to);to->size=from->size;to->backing_size=from->size;to->crc=entry->crc;to->existed=1;to->dirty=0;to->staged=0;file_modified143(to);
 return -(int64_t)file_flush_metadata143(to);
}
#endif
