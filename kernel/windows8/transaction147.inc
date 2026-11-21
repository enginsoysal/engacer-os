/* Retain valid or damaged undo/completion records across process failure. */
static unsigned transaction_pending147(void){char path[256];copy8(path,input8.product_root,sizeof(path));unsigned n=length8(path);const char*tail="/.EngacerMSI/transaction.bin";if(n+length8(tail)>=sizeof(path))return 0;copy8(path+n,tail,sizeof(path)-n);if(find8(path))return 1;return win_product_completion147(path,sizeof(path),input8.product_root)&&find8(path)!=0;}
static unsigned transaction_keep147(void){
 char path[256];copy8(path,input8.product_root,sizeof(path));unsigned n=length8(path);
 const char*names[]={"","/.EngacerMSI/transaction.bin","/product.bin"};
 for(unsigned i=0;i<3;++i){
  if(i==0){if(!win_product_completion147(path,sizeof(path),input8.product_root))return 3;}
  else{if(n+length8(names[i])>=sizeof(path))return 3;copy8(path,input8.product_root,sizeof(path));copy8(path+n,names[i],sizeof(path)-n);}
  const v6_entry*e=find8(path);if(!e)continue;
  win_tx_header147 header;
  if(i==2){uint64_t magic=0;if(e->kind!=1||e->size<8||exact8(path,0,&magic,8))return 3;
   if(magic==UINT64_C(0x31494d38574f53))continue;
   if(magic!=WIN_TX_MAGIC147)return 3;
  }
  /* Even a damaged pending record is retained for inspection, never erased. */
  if(e->kind!=1||e->size<sizeof(header)||e->size>WIN_TX_LIMIT147||exact8(path,0,&header,sizeof(header))||!win_tx_header_shape147(&header,(unsigned)e->size)||!win_tx_bound147(&header,input8.product_root,input8.user_root,0))return 3;
  engine_sha256_context hash;engine_sha256_init(&hash);uint8_t block[4096],digest[32];
  for(unsigned at=0;at<e->size;){unsigned bytes=(unsigned)e->size-at;if(bytes>sizeof(block))bytes=sizeof(block);
   if(exact8(path,at,block,bytes))return 3;if(!at)memset(block+72,0,32);
   if(!engine_sha256_update(&hash,block,bytes))return 3;at+=bytes;
  }
  if(!engine_sha256_final(&hash,digest)||memcmp(digest,header.checksum,32))return 3;
  return 2;
 }
 return 0;
}
static int64_t alias_set147(uint64_t address,uint64_t b,uint64_t c,uint64_t d,uint64_t e){
 if(b||c||d||e)return -87;
 if(input8.command!=W8_INSTALL&&input8.command!=W8_REMOVE&&input8.command!=W8_PREVIEW)return -5;
 char alias[256];if(string8(address,alias,sizeof(alias))||!win_tx_alias147(alias))return -87;
 /* Only the logical alias changes. The canonical physical grant never moves. */
 if(user8(W8_MAILBOX+offsetof(w8_mailbox,windows_root),alias,length8(alias)+1,1))return -87;
 copy8(input8.windows_root,alias,sizeof(input8.windows_root));return 0;
}
static unsigned installer_user_grant147(const char*path,unsigned ancestor){
 if(!path||path[0]!='/'||!win_tx_relative147(path+1,'/')||!win_product_root147(input8.product_root))return 0;
 char completion[256];if(win_product_completion147(completion,sizeof(completion),input8.product_root)){if(equal8(path,completion))return 1;if(ancestor&&prefix8(completion,path))return 1;}
 const char*common="/Data/Windows/Common/Programs";
 if(prefix8(path,common))return 1;
 if(ancestor&&prefix8(common,path))return 1;
 unsigned user=length8(input8.user_root);if(user>=128||length8(path)<=user||memcmp(path,input8.user_root,user)||path[user]!='/')return 0;
 char programs[256],recovery[256];copy8(programs,input8.user_root,256);copy8(recovery,input8.user_root,256);
 copy8(programs+user,"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs",256-user);
 copy8(recovery+user,"/Documents/Recovered applications/",256-user);unsigned n=length8(recovery);
 copy8(recovery+n,input8.product_root+sizeof(WIN_PRODUCT_BASE147)-1,256-n);
 if(prefix8(path,programs)||prefix8(path,recovery))return 1;
 return ancestor&&(prefix8(programs,path)||prefix8(recovery,path));
}
static int64_t staging_move147(const char*source,const char*target){
 if(input8.command!=W8_INSTALL||!installer_authority147())return -5;
 unsigned root=length8(input8.product_root);const char*private_name="/.EngacerMSI/";unsigned private_bytes=sizeof("/.EngacerMSI/")-1;
 if(!prefix8(source,input8.product_root)||(!prefix8(target,input8.product_root)&&!installer_user_grant147(target,0))||length8(source)<=root+private_bytes||memcmp(source+root,private_name,private_bytes))return -5;
 const v6_entry*from=find8(source);if(!from||from->kind!=1)return -2;if(find8(target))return -80;
 if(file_object_slot143(source)<FILE_OBJECTS143||file_object_slot143(target)<FILE_OBJECTS143)return -32;
 /* This path is for untouched native staging files, never Windows file objects. */
 char record[256];metadata_path143(source,record);if(find8(record))return -50;metadata_path143(target,record);if(find8(record))return -50;
 return v6_rename(m6_volume(),source,target,0)?-1117:0;
}
