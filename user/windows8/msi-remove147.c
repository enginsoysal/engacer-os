/* Replayable ownership undo. Changed files survive outside the product root. */
#include "msi-remove147.h"
#include "msi-registry147.h"
#include "msi-condition147.h"
#include "msi-actions147.h"
static unsigned remove_path147(char out[256],const char*base,const char*tail){unsigned n=len8(base),m=len8(tail);if(n+m>=256)return 206;memcpy(out,base,n);memcpy(out+n,tail,m+1);return 0;}
static void hex_remove147(char*out,const uint8_t*bytes,unsigned n){const char*hex="0123456789abcdef";for(unsigned i=0;i<n;++i){out[i*2]=hex[bytes[i]>>4];out[i*2+1]=hex[bytes[i]&15];}out[n*2]=0;}
static void decimal_remove147(char out[24],uint64_t n){char reverse[24];unsigned count=0,at=0;do{reverse[count++]=(char)('0'+n%10);n/=10;}while(n);while(count)out[at++]=reverse[--count];out[at]=0;}
static unsigned preserve_remove147(const msia_plan147*p,const char*source,unsigned*kept){
 w8_file_info info;if(stat8(source,&info))return 0;if(info.kind!=1)return 87;uint64_t source_bytes=info.size;uint8_t sha[32],path_sha[32];unsigned status=msif_hash147(source,info.size,sha);if(status)return status;engine_sha256(source,len8(source),path_sha);
 char directory[256],target[256],buddy[256],leaf[64],full_sha[65],size[24];status=remove_path147(directory,job8->user_root,"/Documents/Recovered applications/");if(status)return status;if(len8(directory)+len8(p->code)>=256)return 206;append8(directory,p->code,256);status=msif_directory147(directory);if(status)return status;
 hex_remove147(leaf,path_sha,8);leaf[16]='-';hex_remove147(leaf+17,sha,12);leaf[41]='-';const char*name=source;for(unsigned i=0;source[i];++i)if(source[i]=='/')name=source+i+1;unsigned safe=name[0]!=0;for(unsigned i=0;name[i];++i){unsigned c=(uint8_t)name[i];if(!((c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='.'||c=='_'||c=='-'))safe=0;}copy8(leaf+42,safe?name:"saved-file.dat",17);unsigned length=len8(leaf);if(leaf[length-1]=='.')leaf[length-1]='_';
 status=remove_path147(target,directory,"/");if(status||len8(target)+len8(leaf)>=256)return 206;append8(target,leaf,256);status=remove_path147(buddy,target,".txt");if(status)return status;
 hex_remove147(full_sha,sha,32);decimal_remove147(size,info.size);char description[1024];copy8(description,"Preserved application file\nProduct: ",sizeof(description));append8(description,p->code,sizeof(description));append8(description,"\nOriginal path: ",sizeof(description));append8(description,source,sizeof(description));append8(description,"\nBytes: ",sizeof(description));append8(description,size,sizeof(description));append8(description,"\nSHA-256: ",sizeof(description));append8(description,full_sha,sizeof(description));append8(description,"\n",sizeof(description));unsigned bytes=len8(description);
 if(!stat8(buddy,&info)){void*existing=0;unsigned n=load8(buddy,&existing,sizeof(description));unsigned equal=n==bytes&&!memcmp(existing,description,bytes);if(existing)free8(existing);if(!equal)return 183;}
 else{int handle=open8(buddy,2);if(handle<0)return 5;if(write8(handle,description,bytes)!=(int)bytes){(void)sys8(W8_SYS_CLOSE,(unsigned)handle,1,0,0,0);return 29;}if(close8(handle))return 1117;void*check=0;unsigned n=load8(buddy,&check,sizeof(description));unsigned equal=n==bytes&&!memcmp(check,description,bytes);if(check)free8(check);if(!equal)return 1117;}
 if(!stat8(target,&info)){uint8_t existing[32];status=msif_hash147(target,info.size,existing);if(status||info.size!=source_bytes||memcmp(existing,sha,32))return status?status:183;if(remove8(source))return 1117;}
 else{int64_t result=(int64_t)sys8(W8_SYS_MOVE,(uint64_t)(uintptr_t)source,(uint64_t)(uintptr_t)target,0,0,0);if(result<0)return 1117;uint8_t actual[32];if(stat8(target,&info))return 1117;status=msif_hash147(target,info.size,actual);if(status||info.size!=source_bytes||memcmp(actual,sha,32))return status?status:23;}
 ++*kept;return 0;
}
static unsigned owned_remove147(const msia_plan147*p,const win_tx_file147*f,unsigned link,unsigned*kept){
 const char*base=link?(f->flags?"/Data/Windows/Common/Programs":job8->user_root):p->product_root;char path[256],tail[257];tail[0]='/';copy8(tail+1,f->path,256);unsigned status=remove_path147(path,base,tail);if(status)return status;w8_file_info info;if(stat8(path,&info))return 0;if(info.kind!=1)return 183;
 uint8_t sha[32];if(info.size==f->bytes){status=msif_hash147(path,info.size,sha);if(status)return status;if(!memcmp(sha,f->sha,32))return remove8(path)?1117:0;}
 return preserve_remove147(p,path,kept);
}
static const win_tx_file147*record_file_remove147(const msij147*j,const char*relative){for(unsigned at=1024;at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==WIN_TX_FILE147){const win_tx_file147*f=(const void*)(r+1);if(win_tx_equal147(f->path,relative))return f;}at+=r->bytes;}return 0;}
static const win_tx_file147*stage_remove147(const msia_plan147*p,const msij147*j,const char*relative){
 const char*prefix=".EngacerMSI/stage/";unsigned n=len8(prefix);if(len8(relative)!=n+4||memcmp(relative,prefix,n))return 0;const char*name=relative+n;if((name[0]!='f'&&name[0]!='s')||name[1]<'0'||name[1]>'9'||name[2]<'0'||name[2]>'9'||name[3]<'0'||name[3]>'9')return 0;unsigned index=(name[1]-'0')*100+(name[2]-'0')*10+name[3]-'0';
 if(name[0]=='f'){if(index>=p->file_count||!p->files[index].selected)return 0;char path[256];if(msia_file_path147(p,index,path))return 0;return record_file_remove147(j,path+len8(p->product_root)+1);}
 for(unsigned at=1024;at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==WIN_TX_LINK147){if(!index)return(const void*)(r+1);--index;}at+=r->bytes;}return 0;
}
static unsigned tree_remove147(const msia_plan147*p,const msij147*j,const char*directory,unsigned depth,unsigned*kept){
 if(depth>32)return 206;uint64_t cursor=0;unsigned root=len8(p->product_root);for(;;){w8_file_info entry;int64_t next=(int64_t)sys8(W8_SYS_ENUM,(uint64_t)(uintptr_t)directory,(uint64_t)(uintptr_t)&entry,cursor,0,0);if(next<0)return 5;if(!next)return 0;if((uint64_t)next<=cursor)return 13;cursor=(uint64_t)next;char tail[257],path[256];tail[0]='/';copy8(tail+1,entry.name,256);unsigned status=remove_path147(path,directory,tail);if(status)return status;const char*relative=path+root+1;
  if(entry.kind==2){status=tree_remove147(p,j,path,depth+1,kept);if(status)return status;if(!equal8(relative,".EngacerMSI")&&remove8(path))return 1117;}
  else if(entry.kind==1){if(equal8(relative,".EngacerMSI/stage/action.dll")){status=msica_clean147(p,path);if(status==2)status=preserve_remove147(p,path,kept);if(status)return status;continue;}if(equal8(relative,".EngacerMSI/transaction.bin")||equal8(relative,".EngacerMSI/source.msi"))continue;const win_tx_file147*f=stage_remove147(p,j,relative);if(f&&entry.size==f->bytes){uint8_t sha[32];status=msif_hash147(path,entry.size,sha);if(status)return status;if(!memcmp(sha,f->sha,32)){if(remove8(path))return 1117;continue;}}status=preserve_remove147(p,path,kept);if(status)return status;}
  else return 50;
 }
}
static unsigned link_parents_remove147(const msij147*j){
 for(unsigned at=1024;at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==WIN_TX_LINK147){const win_tx_file147*f=(const void*)(r+1);char floor[256],path[256],tail[257];copy8(floor,f->flags?"/Data/Windows/Common/Programs":job8->user_root,256);if(!f->flags){if(len8(floor)+sizeof("/AppData/Roaming/Microsoft/Windows/Start Menu/Programs")>256)return 206;append8(floor,"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs",256);}const char*base=f->flags?floor:job8->user_root;tail[0]='/';copy8(tail+1,f->path,256);unsigned status=remove_path147(path,base,tail);if(status)return status;unsigned boundary=len8(floor);if(len8(path)<=boundary||memcmp(path,floor,boundary)||path[boundary]!='/')return 87;
  for(;;){unsigned n=len8(path);while(n&&path[n-1]!='/')--n;if(!n)break;path[n-1]=0;if(len8(path)<=len8(floor))break;w8_file_info child;int64_t next=(int64_t)sys8(W8_SYS_ENUM,(uint64_t)(uintptr_t)path,(uint64_t)(uintptr_t)&child,0,0,0);if(next<0)return 5;if(next)break;w8_file_info info;if(!stat8(path,&info)&&remove8(path))return 1117;}
 }at+=r->bytes;}return 0;
}
static unsigned property_flag_remove147(const msij147*j,const char*requested){for(unsigned at=1024;at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==WIN_TX_PROPERTY147){const win_tx_property147*q=(const void*)(r+1);const char*name=(const void*)(q+1);if(equal8(name,requested))return equal8(name+q->name_bytes,"1")?1:2;}at+=r->bytes;}return 0;}
static unsigned flag_remove147(const msij147*j){return property_flag_remove147(j,"_EngacerRemove147");}
static unsigned append_flag_remove147(msij147*j,const char*name){unsigned prior=property_flag_remove147(j,name);if(prior)return prior==1?0:13;struct {win_tx_property147 header;char data[80];}record={0};unsigned n=len8(name)+1;if(n>73)return 87;record.header.name_bytes=n;record.header.value_bytes=2;memcpy(record.data,name,n);memcpy(record.data+n,"1",2);return msij_append147(j,WIN_TX_PROPERTY147,&record,8+n+2);}
unsigned msir_finish147(unsigned*kept){
 if(!kept||(job8->command!=W8_REMOVE&&job8->command!=W8_INSTALL))return 87;char done[256];if(!win_product_completion147(done,sizeof(done),job8->product_root))return 87;w8_file_info info;if(stat8(done,&info))return 2;
 msij147*j=msij_read147(done,job8->product_root,job8->user_root);if(!j)return 13;if(property_flag_remove147(j,"_EngacerRemoveDone147")!=1){msij_close147(j);return 13;}
 const win_tx_header147*h=(const void*)j->data;msia_plan147*p=calloc8(1,sizeof(*p));if(!p){msij_close147(j);return 8;}copy8(p->product_root,job8->product_root,256);copy8(p->code,h->code,40);copy8(job8->product,h->product,sizeof(job8->product));copy8(job8->version,h->version,sizeof(job8->version));copy8(job8->publisher,h->publisher,sizeof(job8->publisher));copy8(job8->code,h->code,sizeof(job8->code));memcpy(job8->source_sha147,h->source_sha,32);
 unsigned extra=0,status=0;if(!stat8(p->product_root,&info)){
  if(info.kind!=2)status=183;else status=tree_remove147(p,j,p->product_root,0,&extra);
  char cache[256],pending[256],private_dir[256];if(!status)status=remove_path147(cache,p->product_root,"/.EngacerMSI/source.msi");if(!status)status=remove_path147(pending,p->product_root,"/.EngacerMSI/transaction.bin");if(!status)status=remove_path147(private_dir,p->product_root,"/.EngacerMSI");
  if(!status&&!stat8(cache,&info)){const win_tx_file147*f=record_file_remove147(j,".EngacerMSI/source.msi");uint8_t sha[32];unsigned match=0;if(f&&f->flags==WIN_TX_CACHE147&&info.kind==1&&info.size==f->bytes){status=msif_hash147(cache,info.size,sha);if(!status)match=!memcmp(sha,f->sha,32);}if(!status)status=match?(remove8(cache)?1117:0):preserve_remove147(p,cache,&extra);}
  if(!status&&!stat8(pending,&info)){msij147*old=msij_read147(pending,p->product_root,job8->user_root);unsigned match=old&&win_tx_bound147((const void*)old->data,p->product_root,job8->user_root,h->source_sha);msij_close147(old);status=match?(remove8(pending)?1117:0):preserve_remove147(p,pending,&extra);}
  if(!status&&!stat8(private_dir,&info)&&remove8(private_dir))status=1117;
  if(!status&&remove8(p->product_root))status=1117;
 }
 if(!status&&remove8(done))status=1117;if(!status)*kept+=extra;free8(p);msij_close147(j);return status;
}
static unsigned execute_remove147(msia_plan147*p,msij147*j,unsigned*kept,msica147**actions){
 if(!p||!p->costed||!j||!kept||job8->command!=W8_REMOVE||!equal8(p->product_root,job8->product_root)||!win_tx_validate147(j->data,j->bytes)||!win_tx_bound147((const void*)j->data,p->product_root,job8->user_root,p->source_sha256))return 87;*kept=0;unsigned completed=msir_finish147(kept);if(completed!=2)return completed;if(property_flag_remove147(j,"_EngacerRemoveDone147"))return 13;
 char pending[256],product[256],cache[256];unsigned status=remove_path147(pending,p->product_root,"/.EngacerMSI/transaction.bin");if(!status)status=remove_path147(product,p->product_root,"/product.bin");if(!status)status=remove_path147(cache,p->product_root,"/.EngacerMSI/source.msi");if(status)return status;w8_file_info info;unsigned has_pending=!stat8(pending,&info),installed=!stat8(product,&info)||flag_remove147(j)==1;if(flag_remove147(j)==2)return 13;
 if(has_pending&&!stat8(product,&info)){msij147*registered=msij_read147(product,p->product_root,job8->user_root);if(!registered)return 13;const win_tx_header147*header=(const void*)registered->data;unsigned valid=win_tx_bound147(header,p->product_root,job8->user_root,p->source_sha256)&&equal8(header->alias,p->program_alias);msij_close147(registered);if(!valid)return 13;}
 uint8_t source_sha[32];if(stat8(cache,&info)||info.kind!=1)return 2;status=msif_hash147(cache,info.size,source_sha);if(status||memcmp(source_sha,p->source_sha256,32))return status?status:23;
 if(installed)status=msip_set147(&p->properties,"Installed","1");if(!status)status=msip_set147(&p->properties,"REMOVE","ALL");if(status)return status;
 unsigned file_action=0,link_action=0,registry_action=0;for(unsigned i=0;i<p->action_count;++i){msia_action147*a=p->actions+i;int condition=msia_condition147(p,a->condition);if(condition==MSIC_ERROR147)return 87;if(installed&&a->kind==MSIA_PROPERTY147){status=msia_property_action147(p,i);if(status)return status;}else if(installed&&a->kind&&!msia_dll_type147(a->kind)&&condition!=MSIC_FALSE147)return 50;if(condition==MSIC_FALSE147)continue;if(equal8(a->name,"RemoveFiles"))file_action=1;if(equal8(a->name,"RemoveShortcuts"))link_action=1;if(equal8(a->name,"RemoveRegistryValues"))registry_action=1;}
 const win_tx_header147*h=(const void*)j->data;if(!file_action||(h->links&&!link_action)||(h->registry&&!registry_action))return 50;
 if(installed){status=msica_prepare147(p,actions);if(status)return status;}
 if(!has_pending){if(installed&&!flag_remove147(j)){status=append_flag_remove147(j,"_EngacerRemove147");if(status)return status;}status=msij_write147(j,pending);if(status)return status;}
 if(!stat8(product,&info)&&remove8(product))return 1117;
 unsigned files_done=0,links_done=0,registry_done=0;for(unsigned i=0;i<p->action_count&&!status;++i){msia_action147*a=p->actions+i;int condition=msia_condition147(p,a->condition);if(condition==MSIC_FALSE147)continue;
  if(installed&&msia_dll_type147(a->kind)){
   for(unsigned at=1024;at<j->bytes&&!status;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==WIN_TX_FILE147){const win_tx_file147*f=(const void*)(r+1);if(f->flags==WIN_TX_GENERATED147){char path[256],tail[257];tail[0]='/';copy8(tail+1,f->path,256);status=remove_path147(path,p->product_root,tail);w8_file_info info;if(!status&&!stat8(path,&info)){uint8_t hash[32];if(info.kind!=1)status=183;else{unsigned same=0;if(info.size==f->bytes){status=msif_hash147(path,info.size,hash);same=!status&&!memcmp(hash,f->sha,32);}if(!status&&!same)status=preserve_remove147(p,path,kept);}}}}at+=r->bytes;}
   if(!status){msia_custom_result147 result;status=msica_run147(*actions,p,i,&result);}
  }
  else if(equal8(a->name,"RemoveRegistryValues")){status=msireg_undo147(j);registry_done=!status;}
  else if(equal8(a->name,"RemoveShortcuts")||equal8(a->name,"RemoveFiles")){unsigned link=equal8(a->name,"RemoveShortcuts");for(unsigned at=1024;at<j->bytes&&!status;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==(link?WIN_TX_LINK147:WIN_TX_FILE147)){const win_tx_file147*f=(const void*)(r+1);if(link||f->flags!=WIN_TX_CACHE147)status=owned_remove147(p,f,link,kept);}at+=r->bytes;}if(link)links_done=!status;else files_done=!status;}
  sys8(W8_SYS_YIELD,0,0,0,0,0);
 }
 h=(const void*)j->data;if(status)return status;if(!files_done||(h->links&&!links_done)||(h->registry&&!registry_done))return 50;status=link_parents_remove147(j);if(status)return status;status=tree_remove147(p,j,p->product_root,0,kept);if(status)return status;
 if(stat8(cache,&info)||info.kind!=1)return 2;status=msif_hash147(cache,info.size,source_sha);if(status||memcmp(source_sha,p->source_sha256,32))return status?status:23;
 char done[256],parent[256];if(!win_product_completion147(done,sizeof(done),p->product_root))return 87;copy8(parent,done,256);unsigned n=len8(parent);while(n&&parent[n-1]!='/')--n;if(!n)return 87;parent[n-1]=0;status=msif_directory147(parent);if(status)return status;status=append_flag_remove147(j,"_EngacerRemoveDone147");if(!status)status=msij_write147(j,done);if(status)return status;
 return msir_finish147(kept);
}

unsigned msir_remove147(msia_plan147*p,msij147*j,unsigned*kept){msica147*actions=0;unsigned status=execute_remove147(p,j,kept,&actions);msica_close147(actions);return status;}
