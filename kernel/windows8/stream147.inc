/* One owner of the existing V6 staged extent; no whole-file dirty allocation. */
static uint32_t stream_owner147,stream_phase147;
static uint64_t stream_expected147,stream_received147;
static void stream_release147(void){if(stream_owner147&&stream_owner147==input8.process_id){v6_stream_abort(m6_volume());stream_owner147=stream_phase147=0;stream_expected147=stream_received147=0;}}
static int64_t stream_call147(uint64_t operation,uint64_t address,uint64_t bytes,uint64_t d,uint64_t e){
 if(d||e||input8.command!=W8_INSTALL||!installer_authority147())return -5;
 if(operation==1){
  if(stream_owner147)return -170;if(bytes>32u*1024u*1024u)return -1816;char path[256];if(string8(address,path,sizeof(path))||!path8(path,1))return -5;
  unsigned root=length8(input8.product_root);if(memcmp(path,input8.product_root,root)||path[root]!='/')return -5;
  const char*relative=path+root+1;unsigned prefix=sizeof(".EngacerMSI/stage/")-1;
  if((length8(relative)<=prefix||memcmp(relative,".EngacerMSI/stage/",prefix))&&!equal8(relative,".EngacerMSI/source.msi"))return -5;
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
