/* Product-specific admission metadata is separate from shared Windows APIs.
 * The first original EXE profile is deliberately bounded and independently
 * checks effects; later general installation work must replace its admission
 * inventory without weakening the kernel-owned authority boundary. */
static void exe_record_path148(const char*owner,char*out){char hash[33];protected_hash143(owner,hash);copy8(out,"/Data/Windows/",256);path_append143(out,hash,256);path_append143(out,"/EXE",256);path_append143(out,EXE148_CODE ".bin",256);}
static unsigned exe_record_load148(const char*owner,exe_record148*r){
 char path[256];exe_record_path148(owner,path);const v6_entry*e=find8(path);unsigned got=0;
 if(!e)return 2;if(e->kind!=1||e->size!=sizeof(*r)||v6_verify(m6_volume(),path)||v6_read(m6_volume(),path,0,r,sizeof(*r),&got)||got!=sizeof(*r))return 13;
 if(r->magic!=EXE148_RECORD_MAGIC||r->schema!=1||r->bytes!=sizeof(*r)||r->state<1||r->state>5||!terminated142(r->user,256)||!terminated142(r->root,256)||!terminated142(r->alias,256)||!terminated142(r->source,256)||!terminated142(r->temporary,256)||!equal8(r->user,owner)||!equal8(r->root,EXE148_ROOT)||!equal8(r->alias,EXE148_ALIAS)||!exe_digest148(r->source_sha,EXE148_SOURCE_SHA))return 13;
 uint8_t expected[32],digest[32];memcpy(expected,r->checksum,32);memset(r->checksum,0,32);engine_sha256(r,sizeof(*r),digest);memcpy(r->checksum,expected,32);return memcmp(digest,expected,32)?13:0;
}
unsigned w8_exe_record148(const char*owner,exe_record148*out){if(!owner||!out||!prefix8(owner,"/Users"))return 0;return !exe_record_load148(owner,out);}
static unsigned exe_record_save148(exe_record148*r){char path[256],directory[256];exe_record_path148(r->user,path);copy8(directory,path,256);unsigned n=length8(directory);while(n&&directory[n-1]!='/')--n;directory[n-1]=0;unsigned error=protected_prepare143(directory);if(error)return error;memset(r->checksum,0,32);engine_sha256(r,sizeof(*r),r->checksum);return v6_put(m6_volume(),path,sizeof(*r),memory_source8,r)?1117:0;}
static unsigned exe_hash_file148(const char*path,uint64_t bytes,const char*expected){
 const v6_entry*e=find8(path);if(!e||e->kind!=1||e->size!=bytes)return 13;engine_sha256_context hash;engine_sha256_init(&hash);uint8_t digest[32];
 for(uint64_t at=0;at<bytes;){unsigned count=bytes-at>sizeof(io8)?sizeof(io8):(unsigned)(bytes-at);if(exact8(path,at,io8,count)||!engine_sha256_update(&hash,io8,count))return 23;at+=count;}
 return engine_sha256_final(&hash,digest)&&exe_digest148(digest,expected)?0:23;
}
static unsigned exe_payloads_check148(void){
 unsigned files=0;v6_volume*v=m6_volume();for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*e=v->entries+i;if(!e->kind||equal8(e->path,EXE148_ROOT)||!prefix8(e->path,EXE148_ROOT))continue;unsigned found=0;
  for(unsigned j=0;j<4;++j){char path[256];copy8(path,EXE148_ROOT,256);path_append143(path,"/",256);path_append143(path,exe_payloads148[j].name,256);if(equal8(path,e->path)){if(exe_hash_file148(path,exe_payloads148[j].bytes,exe_payloads148[j].sha))return 23;found=1;++files;break;}}
  if(!found)return 5;
 }return files==4?0:13;
}
static void exe_leaf148(unsigned which,char*out){copy8(out,input8.user_root,256);path_append143(out,which?"/AppData/Roaming/Microsoft/Windows/Start Menu/SumatraPDF.lnk":"/Desktop/SumatraPDF.lnk",256);}
static unsigned exe_link_check148(const char*path){const v6_entry*e=find8(path);uint8_t header[20];static const uint8_t clsid[]={1,0x14,2,0,0,0,0,0,0xc0,0,0,0,0,0,0,0x46};if(!e||e->kind!=1||e->size<76||e->size>4096||exact8(path,0,header,20)||header[0]!=76||memcmp(header+4,clsid,16)||v6_verify(m6_volume(),path))return 13;return 0;}
static unsigned exe_user_grant148(const char*path,unsigned ancestor){
 char leaf[256];for(unsigned i=0;i<2;++i){exe_leaf148(i,leaf);if(equal8(path,leaf)||(ancestor&&prefix8(leaf,path)))return 1;}
 char temporary[256];copy8(temporary,input8.user_root,256);path_append143(temporary,"/AppData/Temp/EXE-",256);path_append143(temporary,EXE148_CODE,256);char number[16],reverse[16];unsigned n=0,at=0,value=input8.reserved147;do{reverse[n++]=(char)('0'+value%10);value/=10;}while(value);number[at++]='-';while(n)number[at++]=reverse[--n];number[at]=0;path_append143(temporary,number,256);
 return prefix8(path,temporary)||(ancestor&&prefix8(temporary,path));
}
static void exe_temporary148(char*out){copy8(out,input8.user_root,256);path_append143(out,"/AppData/Temp/EXE-",256);path_append143(out,EXE148_CODE,256);char number[16],reverse[16];unsigned n=0,at=0,value=input8.reserved147;do{reverse[n++]=(char)('0'+value%10);value/=10;}while(value);number[at++]='-';while(n)number[at++]=reverse[--n];number[at]=0;path_append143(out,number,256);}
static const char*exe_shared_key148(unsigned i){return i?"software\\classes\\mime\\database\\content type\\application/pdf":"software\\classes\\.pdf";}
static const char*exe_shared_name148(unsigned i){return i?"extension":"content type";}
static void exe_shared_path148(unsigned i,registry_value_record143*v,char*out){memset(v,0,sizeof(*v));v->magic=REGISTRY_VALUE_MAGIC143;copy8(v->user,input8.user_root,256);copy8(v->key,exe_shared_key148(i),768);copy8(v->name,exe_shared_name148(i),256);copy8(v->display,i?"Extension":"Content Type",256);registry_directory143(v->key,out);char hash[33];registry_hash143(v->name,hash);path_append143(out,"/v",256);path_append143(out,hash,256);}
static unsigned exe_shared_capture148(exe_record148*r){registry_machine147=0;registry_value_record143*v=(void*)io8;
 for(unsigned i=0;i<2;++i){char path[256],dir[256];exe_shared_path148(i,v,path);registry_directory143(v->key,dir);path_append143(dir,"/$key",256);r->shared[i].key_present=find8(dir)!=0;unsigned error=registry_load_value143(path,v);if(error==2)continue;if(error)return error;if(v->bytes>512)return 234;r->shared[i].present=1;r->shared[i].type=v->type;r->shared[i].bytes=v->bytes;memcpy(r->shared[i].data,v->data,v->bytes);}
 return 0;
}
static unsigned exe_shared_restore148(exe_record148*r){registry_machine147=0;registry_value_record143*v=(void*)io8;
 for(unsigned i=0;i<2;++i){char path[256];exe_shared_path148(i,v,path);unsigned error=registry_load_value143(path,v);if(error!=2&&error)return error;
  /* Do not overwrite a newer user's value. Restore only the value installed by
   * this profile or an absent value removed by the original uninstaller. */
  static const uint16_t mime[]={ 'a','p','p','l','i','c','a','t','i','o','n','/','p','d','f',0 },ext[]={'.','p','d','f',0};const void*expected=i?(const void*)ext:(const void*)mime;unsigned bytes=i?sizeof(ext):sizeof(mime);
  if(!error&&(v->type!=1||v->bytes!=bytes||memcmp(v->data,expected,bytes)))continue;
  if(r->shared[i].present){if(r->shared[i].bytes>512)return 13;exe_shared_path148(i,v,path);v->type=r->shared[i].type;v->bytes=r->shared[i].bytes;memcpy(v->data,r->shared[i].data,v->bytes);if(v6_put(m6_volume(),path,offsetof(registry_value_record143,data)+v->bytes,memory_source8,v))return 1117;}
  else if(!error&&v6_remove(m6_volume(),path))return 1117;
 }return 0;
}
static unsigned exe_admit148(unsigned command,const uint8_t*digest){
 if(active_space142||!equal8(input8.product_root,EXE148_ROOT)||command!=W8_INSTALL&&command!=W8_REMOVE)return 87;
 uint64_t page=page_alloc();if(!page)return 8;exe_record148*r=(void*)(uintptr_t)page;unsigned error=exe_record_load148(input8.user_root,r);
 if(command==W8_INSTALL){if(!digest||!exe_digest148(digest,EXE148_SOURCE_SHA)||find8(EXE148_ROOT)||error!=2&&error||!error&&r->state!=EXE148_REMOVED){error=5;goto done;}error=exe_hash_file148(input8.source,EXE148_SOURCE_BYTES,EXE148_SOURCE_SHA);}
 else{if(error||r->state!=EXE148_INSTALLED||!equal8(input8.source,EXE148_ROOT "/SumatraPDF.exe")){error=5;goto done;}error=exe_payloads_check148();}
 if(error)goto done;
 spaces142[0]->exe_context148=command==W8_INSTALL?1:2;input8.reserved147=input8.process_id;input8.profile147=W8_PROFILE_EXE148;copy8(input8.windows_root,EXE148_ALIAS,256);
 if(command==W8_INSTALL){const v6_entry*e=find8(input8.source);spaces142[0]->image_pin148=(unsigned)(e-m6_volume()->entries)+1;}
 if(user8(W8_MAILBOX,&input8,sizeof(input8),1))error=998;
 done:page_free(page);return error;
}
static int64_t exe_syscall148(trap_frame*frame,uint64_t op,uint64_t b,uint64_t c,uint64_t d,uint64_t e){
 if(b||c||d||e||active_space142||!spaces142[0]->exe_context148)return -5;
 if(op==0)return spaces142[0]->exe_context148;
 if(op==4){for(unsigned i=1;i<SPACES142;++i)if(spaces142[i]&&process_objects142[spaces142[i]->object].live){thread142*t=threads142+current142;t->state=T142_PARK;t->deadline=UINT64_MAX;context8=*frame;context8.rax=0;w8_active=0;w8_escape();}return 1;}
 uint64_t page=page_alloc();if(!page)return -8;exe_record148*r=(void*)(uintptr_t)page;unsigned error=0;
 if(op==1){unsigned loaded=exe_record_load148(input8.user_root,r);if(spaces142[0]->exe_context148==1){if(loaded!=2&&(loaded||r->state!=EXE148_REMOVED)){error=5;goto done;}memset(r,0,sizeof(*r));r->magic=EXE148_RECORD_MAGIC;r->schema=1;r->bytes=sizeof(*r);r->state=EXE148_INSTALLING;r->nonce=input8.reserved147;copy8(r->user,input8.user_root,256);copy8(r->root,EXE148_ROOT,256);copy8(r->alias,EXE148_ALIAS,256);copy8(r->source,input8.source,256);memcpy(r->source_sha,input8.source_sha147,32);exe_temporary148(r->temporary);
   for(unsigned i=0;i<2;++i){char path[256];exe_leaf148(i,path);if(find8(path)){error=80;goto done;}}error=exe_shared_capture148(r);if(error)goto done;
  }else{if(loaded||r->state!=EXE148_INSTALLED){error=5;goto done;}r->state=EXE148_REMOVING;r->nonce=input8.reserved147;exe_temporary148(r->temporary);}
  if(find8(r->temporary)){error=80;goto done;}error=exe_record_save148(r);if(!error)error=protected_prepare143(r->temporary);
 }else if(op==2||op==3){error=exe_record_load148(input8.user_root,r);if(error||r->nonce!=input8.reserved147){error=13;goto done;}if(spaces142[0]->exe_child_error148){error=spaces142[0]->exe_child_error148;goto done;}
  if(op==2){if(r->state!=EXE148_INSTALLING){error=5;goto done;}error=exe_payloads_check148();for(unsigned i=0;!error&&i<2;++i){char path[256];exe_leaf148(i,path);error=exe_link_check148(path);}if(!error){r->state=EXE148_INSTALLED;error=exe_record_save148(r);}}
  else{if(r->state!=EXE148_REMOVING||find8(EXE148_ROOT)){error=5;goto done;}for(unsigned i=0;i<2;++i){char path[256];exe_leaf148(i,path);if(find8(path)){error=5;goto done;}}error=exe_shared_restore148(r);if(!error){r->state=EXE148_REMOVED;error=exe_record_save148(r);}}
 }else error=87;
 done:page_free(page);return -(int64_t)error;
}
