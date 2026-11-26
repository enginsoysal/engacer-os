/* One owner of the existing V6 staged extent; no whole-file dirty allocation. */
static uint32_t stream_owner147,stream_phase147;
static uint64_t stream_expected147,stream_received147;
static void stream_release147(void){if(stream_owner147&&stream_owner147==input8.process_id){v6_stream_abort(m6_volume());stream_owner147=stream_phase147=0;stream_expected147=stream_received147=0;}}
static void maintenance_stage1410(char path[256]){
 copy8(path,input8.product_root,256);
 path_append143(path,W8_MAINTAIN_STAGE1410,256);
}
static unsigned maintenance_authority1410(void){
 return active_space142==0&&(input8.command==W8_REPAIR1410||input8.command==W8_UPDATE1410);
}
static int64_t maintain_call1410(uint64_t operation){
 unsigned removing=operation==1&&active_space142==0&&input8.command==W8_REMOVE&&
                   installer_authority147()&&!spaces142[0]->exe_context148;
 if((!maintenance_authority1410()&&!removing)||stream_owner147)return -5;
 char stage[256];maintenance_stage1410(stage);
 const v6_entry *directory=find8(stage);
 if(directory&&directory->kind!=2)return -13;
 if(operation==1){
  if(directory&&v6_remove_tree11(m6_volume(),stage))return -1117;
  return 0;
 }
 if(operation!=2||!directory)return -87;
 const v6_volume *volume=m6_volume();
 unsigned stage_bytes=length8(stage),control=0;
 for(unsigned i=0;i<V6_ENTRIES;++i){
  const v6_entry *entry=volume->entries+i;
  if(!entry->kind||!prefix8(entry->path,stage)||equal8(entry->path,stage))continue;
  const char *relative=entry->path+stage_bytes+1;
  char item[64];unsigned j=0;
  for(;relative[j]&&relative[j]!='/'&&j<sizeof(item)-1;++j)item[j]=relative[j];
  item[j]=0;
  if(!win_tx_relative147(relative,'/')||win_tx_equal147(item,".Engacer"))return -5;
  if(win_tx_equal147(item,".EngacerMSI")||win_tx_equal147(item,"product.bin")){
   if(input8.command!=W8_UPDATE1410)return -5;
   if(equal8(relative,"product.bin")&&entry->kind==1)control|=1;
   else if(equal8(relative,".EngacerMSI/source.msi")&&entry->kind==1)control|=2;
   else if(!equal8(relative,".EngacerMSI")||entry->kind!=2)return -5;
  }
  char target[256];copy8(target,input8.product_root,256);
  if(path_append143(target,entry->path+stage_bytes,256))return -206;
  if(file_object_slot143(target)<FILE_OBJECTS143)return -32;
 }
 if(input8.command==W8_UPDATE1410&&control!=3)return -13;
 return v6_overlay_tree1410(m6_volume(),stage,input8.product_root)?-1117:0;
}
static int64_t stream_call147(uint64_t operation,uint64_t address,uint64_t bytes,uint64_t d,uint64_t e){
 unsigned repairing=maintenance_authority1410();
 if(d||e||(!repairing&&(input8.command!=W8_INSTALL||!installer_authority147())))return -5;
 if(operation==1){
  if(stream_owner147)return -170;if(bytes>32u*1024u*1024u)return -1816;char path[256];if(string8(address,path,sizeof(path))||!path8(path,1))return -5;
  unsigned root=length8(input8.product_root);if(memcmp(path,input8.product_root,root)||path[root]!='/')return -5;
  const char*relative=path+root+1;unsigned prefix=sizeof(".EngacerMSI/stage/")-1;
  if(repairing){char stage[256];maintenance_stage1410(stage);if(!prefix8(path,stage)||equal8(path,stage))return -5;}
  else if((length8(relative)<=prefix||memcmp(relative,".EngacerMSI/stage/",prefix))&&!equal8(relative,".EngacerMSI/source.msi"))return -5;
  if(find8(path)||file_object_slot143(path)<FILE_OBJECTS143)return -80;
  unsigned status=v6_stream_begin(m6_volume(),path,bytes?bytes:1);if(status)return status==V6_LIMIT?-170:status==V6_FULL?-112:-1117;
  stream_owner147=input8.process_id;stream_phase147=0;stream_expected147=bytes;stream_received147=0;return 0;
 }
 if(!stream_owner147||stream_owner147!=input8.process_id)return -6;
 if(operation==2){
  if(stream_phase147||bytes>4096||bytes>stream_expected147-stream_received147)return -87;
  unsigned done=0;while(done<bytes){unsigned part=4096-(unsigned)(stream_received147&4095);if(part>bytes-done)part=(unsigned)bytes-done;
   if(user8(address+done,io8,part,0))return -998;
   if(v6_stream_append(m6_volume(),io8,part)){stream_release147();return -1117;}done+=part;stream_received147+=part;
  }return 0;
 }
 if(address||bytes)return -87;
 if(operation==6){stream_release147();return 0;}
 if(stream_received147!=stream_expected147)return -87;
 if(operation==3){if(stream_phase147)return -87;if(v6_stream_seal11(m6_volume())){stream_release147();return -1117;}stream_phase147=1;return 0;}
 if(operation==4){if(stream_phase147!=1)return -87;unsigned done=0;for(unsigned i=0;i<128&&!done;++i)if(v6_stream_check11(m6_volume(),&done)){stream_release147();return -1117;}if(done)stream_phase147=2;return done;}
 if(operation==5){if(stream_phase147!=2)return -87;unsigned status=v6_stream_finish(m6_volume());stream_owner147=stream_phase147=0;stream_expected147=stream_received147=0;return status?-1117:0;}
 return -87;
}
