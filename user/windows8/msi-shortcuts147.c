/* Selected non-advertised links are real MS-SHLLINK files with owned hashes. */
#include "msi-shortcuts147.h"
#include "msi_db.h"
#include "msi-link147.h"
static unsigned link_component147(const msia_plan147*p,const char*id){for(unsigned i=0;i<p->component_count;++i)if(equal8(p->components[i].id,id))return i;return UINT32_MAX;}
static unsigned link_directory147(const msia_plan147*p,const char*id){for(unsigned i=0;i<p->directory_count;++i)if(equal8(p->directories[i].id,id))return i;return UINT32_MAX;}
static unsigned link_prefix147(const char*s,const char*prefix){unsigned n=len8(prefix);if(len8(s)<n)return 0;for(unsigned i=0;i<n;++i){unsigned a=(uint8_t)s[i],b=(uint8_t)prefix[i];if(a>='A'&&a<='Z')a+=32;if(b>='A'&&b<='Z')b+=32;if(a!=b)return 0;}return n;}
static unsigned link_native147(const char*windows,char native[256]){
 uint16_t wide[512],cwd[]={'C',':','\\',0};unsigned capacity=512,code=msit_outwide147(windows,wide,&capacity);if(code)return code;w8_path_result143 result;int64_t status=(int64_t)sys8(W8_SYS_PATH143,(uint64_t)(uintptr_t)wide,(uint64_t)(uintptr_t)cwd,(uint64_t)(uintptr_t)&result,0,0);if(status<0)return (unsigned)-status;memcpy(native,result.native,256);return 0;
}
static unsigned link_target147(msia_plan147*p,const char*target,unsigned*bytes){
 for(unsigned i=0;i<p->file_count;++i)if(p->files[i].selected){char query[80],actual[256];copy8(query,"[#",sizeof(query));if(len8(p->files[i].id)+4>sizeof(query))return 87;append8(query,p->files[i].id,sizeof(query));append8(query,"]",sizeof(query));unsigned code=msia_format147(p,query,actual,sizeof(actual));if(code)return code;if(win_tx_equal147(actual,target)){*bytes=p->files[i].size;return 0;}}
 return 50;
}
static unsigned link_stage_path147(const msia_plan147*p,unsigned i,char out[256]){
 if(i>=32)return 87;copy8(out,p->product_root,256);const char*tail="/.EngacerMSI/stage/s";if(len8(out)+len8(tail)+4>=256)return 206;append8(out,tail,256);unsigned n=len8(out);out[n]=(char)('0'+i/100);out[n+1]=(char)('0'+i/10%10);out[n+2]=(char)('0'+i%10);out[n+3]=0;return 0;
}
void msil_close147(msil_plan147*p){if(p){for(unsigned i=0;i<p->count;++i)free8(p->entries[i]);free8(p);}}
unsigned msil_prepare147(msia_plan147*p,msij147*j,msil_plan147**out){
 if(!p||!p->costed||!j||!out)return 87;*out=0;msi8_table table=msi8_table_open("Shortcut");if(table.rows>32||(table.rows&&(table.columns<12||table.columns>16))){if(table.data.data)free8(table.data.data);return 50;}
 msil_plan147*plan=calloc8(1,sizeof(*plan));uint8_t*binary=alloc8(4096);if(!plan||!binary){if(plan)free8(plan);if(binary)free8(binary);if(table.data.data)free8(table.data.data);return 8;}unsigned status=0;
 for(unsigned row=0;row<table.rows&&!status;++row){unsigned component=link_component147(p,msi8_text(&table,row,3)),directory=link_directory147(p,msi8_text(&table,row,1));if(component==UINT32_MAX||directory==UINT32_MAX){status=87;break;}if(!p->components[component].selected)continue;
  if(msi8_text(&table,row,8)[0]){status=50;break;}int hotkey=msi8_integer(&table,row,7),icon=msi8_integer(&table,row,9);if((hotkey!=INT32_MIN&&hotkey)||(icon!=INT32_MIN&&icon)){status=50;break;}
  for(unsigned column=12;column<table.columns;++column){if(table.column[column].type&0x800){if(msi8_text(&table,row,column)[0])status=50;}else{int n=msi8_integer(&table,row,column);if(n!=INT32_MIN&&n)status=50;}}if(status)break;
  const char*authored=msi8_text(&table,row,2),*name=authored;for(unsigned i=0;authored[i];++i)if(authored[i]=='|'){if(name!=authored){status=87;break;}name=authored+i+1;}if(status)break;char leaf[128];if(len8(name)+5>=sizeof(leaf)){status=206;break;}copy8(leaf,name,sizeof(leaf));append8(leaf,".lnk",sizeof(leaf));if(!msia_leaf147(leaf,len8(leaf))){status=50;break;}
  char windows[512],native[256],target[256],working[256]={0},arguments[4097];copy8(windows,p->directories[directory].windows,sizeof(windows));if(len8(windows)+len8(leaf)>=sizeof(windows)){status=206;break;}append8(windows,leaf,sizeof(windows));status=link_native147(windows,native);if(status)break;
  const char*common="/Data/Windows/Common/Programs/";unsigned skip=link_prefix147(native,common),flags=skip?1:0;if(!skip){char user[256];copy8(user,job8->user_root,256);append8(user,"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/",256);if(!link_prefix147(native,user)){status=50;break;}skip=len8(job8->user_root)+1;}const char*relative=native+skip;
  if(!win_tx_relative147(relative,'/')){status=50;break;}w8_file_info existing;if(!stat8(native,&existing)){status=183;break;}
  const char*raw_target=msi8_text(&table,row,4);unsigned formatted=0;for(unsigned i=0;raw_target[i];++i)if(raw_target[i]=='[')formatted=1;if(!formatted){status=50;break;}
  status=msia_format147(p,raw_target,target,sizeof(target));if(!status)status=msia_format147(p,msi8_text(&table,row,5),arguments,sizeof(arguments));unsigned file_bytes=0;if(!status)status=link_target147(p,target,&file_bytes);if(status)break;
  const char*work=msi8_text(&table,row,11);if(work[0]){unsigned id=link_directory147(p,work);if(id==UINT32_MAX){status=87;break;}copy8(working,p->directories[id].windows,sizeof(working));}
  int show=msi8_integer(&table,row,10);if(show==INT32_MIN)show=1;unsigned bytes=0;status=msil_encode147(target,working,arguments,msi8_text(&table,row,6),(unsigned)show,file_bytes,binary,4096,&bytes);if(status)break;
  msil_entry147*entry=alloc8(sizeof(*entry)+bytes);if(!entry){status=8;break;}entry->flags=flags;entry->bytes=bytes;copy8(entry->relative,relative,sizeof(entry->relative));memcpy(entry->data,binary,bytes);plan->entries[plan->count++]=entry;uint8_t hash[32];engine_sha256(binary,bytes,hash);status=msij_file147(j,WIN_TX_LINK147,relative,bytes,hash,flags);
 }
 free8(binary);if(table.data.data)free8(table.data.data);if(!status)status=msij_seal147(j);if(status){msil_close147(plan);return status;}*out=plan;return 0;
}
unsigned msil_stage147(const msia_plan147*p,const msil_plan147*plan){
 if(!p||!plan)return 87;for(unsigned i=0;i<plan->count;++i){char path[256];unsigned code=link_stage_path147(p,i,path);if(code)return code;int handle=open8(path,2);if(handle<0)return 5;if(write8(handle,plan->entries[i]->data,plan->entries[i]->bytes)!=(int)plan->entries[i]->bytes){(void)sys8(W8_SYS_CLOSE,(unsigned)handle,1,0,0,0);return 29;}if(close8(handle))return 1117;}return 0;
}
unsigned msil_apply147(const msia_plan147*p,const msil_plan147*plan){
 if(!p||!plan)return 87;for(unsigned i=0;i<plan->count;++i){const msil_entry147*entry=plan->entries[i];const char*base=entry->flags?"/Data/Windows/Common/Programs":job8->user_root;char source[256],target[256],parent[256];unsigned code=link_stage_path147(p,i,source);if(code)return code;unsigned a=len8(base),b=len8(entry->relative);if(a+b+1>=sizeof(target))return 206;copy8(target,base,sizeof(target));target[a++]='/';memcpy(target+a,entry->relative,b+1);copy8(parent,target,sizeof(parent));unsigned n=len8(parent);while(n&&parent[n-1]!='/')--n;if(!n)return 87;parent[n-1]=0;code=msif_directory147(parent);if(code)return code;int64_t status=(int64_t)sys8(W8_SYS_MOVE,(uint64_t)(uintptr_t)source,(uint64_t)(uintptr_t)target,2,0,0);if(status<0)return (unsigned)-status;}
 return 0;
}
