/* Admit a qualified original helper, never synthesize its deferred body. */
#include "msi-actions147.h"
#include "msi-files147.h"
#include "msi_db.h"
#include "msi-condition147.h"
static const uint8_t helper_sha147[32]={0x54,0xfe,0xbb,0xd1,0xf0,0xa3,0x87,0x5d,0xf1,0x6a,0x4b,0x88,0x62,0x1c,0xc0,0xa1,0x07,0x29,0xb3,0xc9,0x4b,0x9a,0x68,0x63,0x9a,0xab,0x27,0xd3,0x6f,0xe3,0x93,0x81};
static msi8_blob binary_actions147(const msia_action147*a){
 msi8_blob none={0};if(!msia_dll_type147(a->kind)||!equal8(a->target,"WixQuietExec")||len8(a->source)>63)return none;
 char stream[72];copy8(stream,"Binary.",sizeof(stream));append8(stream,a->source,sizeof(stream));msi8_blob blob=msi8_stream(stream,0);uint8_t sha[32];
 if(blob.size==423704){engine_sha256(blob.data,blob.size,sha);if(!memcmp(sha,helper_sha147,32))return blob;}
 if(blob.data)free8(blob.data);return none;
}
static unsigned argument_actions147(const char**cursor,char out[256],unsigned quote){
 const char*p=*cursor;while(*p==' ')++p;unsigned n=0;if(quote){if(*p++!='"')return 87;while(*p&&*p!='"'){unsigned c=(uint8_t)*p++;if(c<32||c>=127||c=='%'||c=='&'||c=='|'||c=='<'||c=='>'||c=='^'||n==255)return 87;out[n++]=(char)c;}if(*p++!='"')return 87;if(*p&&*p!=' ')return 87;}
 else{while(*p&&*p!=' '){if(n==255)return 87;out[n++]=*p++;}}
 out[n]=0;*cursor=p;return n?0:87;
}
static unsigned command_actions147(msia_plan147*p,msica_item147*item){
 const char*cursor=item->data;char executable[256],first[256],second[256],last[256],target[256];unsigned status=argument_actions147(&cursor,executable,1);if(status)return status;
 copy8(target,p->program_alias,256);if(len8(target)+sizeof("\\nativeLang.xml*")>256)return 206;append8(target,"\\nativeLang.xml",256);
 if(!case8(executable,"C:\\Windows\\System32\\xcopy.exe")||!case8(executable,"C:\\Windows\\SysWOW64\\xcopy.exe")){
  if(argument_actions147(&cursor,first,1)||argument_actions147(&cursor,second,1)||argument_actions147(&cursor,last,0)||case8(last,"/Y"))return 50;
  if(argument_actions147(&cursor,last,0)||case8(last,"/Q"))return 50;while(*cursor==' ')++cursor;if(*cursor)return 50;append8(target,"*",256);if(case8(second,target))return 50;
  for(unsigned i=0;i<p->file_count;++i)if(p->files[i].selected){char native[256],path[256];if(msia_file_path147(p,i,native))return 206;const char*relative=native+len8(p->product_root)+1;copy8(path,p->program_alias,256);if(len8(path)+1+len8(relative)>=256)return 206;append8(path,"\\",256);unsigned offset=len8(path);for(unsigned k=0;relative[k];++k)path[offset+k]=relative[k]=='/'?'\\':relative[k];path[offset+len8(relative)]=0;if(!case8(path,first)){item->operation=1;item->file=i;return 0;}}
  return 50;
 }
 if(!case8(executable,"C:\\Windows\\System32\\cmd.exe")||!case8(executable,"C:\\Windows\\SysWOW64\\cmd.exe")){
  static const char*const args[]={"/C","del","/F","/Q"};for(unsigned i=0;i<4;++i)if(argument_actions147(&cursor,last,0)||case8(last,args[i]))return 50;
  if(argument_actions147(&cursor,first,1)||case8(first,target))return 50;while(*cursor==' ')++cursor;if(*cursor)return 50;item->operation=2;return 0;
 }
 return 50;
}
void msica_close147(msica147*actions){if(actions){for(unsigned i=0;i<actions->count;++i)free8(actions->items[i]);free8(actions);}}
unsigned msica_prepare147(msia_plan147*p,msica147**out){
 if(!p||!p->costed||!out)return 87;*out=0;msica147*actions=0;unsigned status=0;
 for(unsigned i=0;i<p->action_count&&!status;++i){msia_action147*a=p->actions+i;int condition=msia_condition147(p,a->condition);if(condition==MSIC_ERROR147){status=87;break;}if(condition==MSIC_FALSE147)continue;
  if(a->kind==MSIA_PROPERTY147){unsigned captures=0;for(unsigned k=i+1;k<p->action_count;++k)if(msia_dll_type147(p->actions[k].kind)&&equal8(a->source,p->actions[k].name))captures=1;if(!captures){status=50;break;}status=msia_property_action147(p,i);continue;}if(!a->kind)continue;
  unsigned lower=0,upper=0;for(unsigned k=0;k<p->action_count;++k){msia_action147*b=p->actions+k;if(job8->command==W8_REMOVE){if(equal8(b->name,"RemoveRegistryValues")||equal8(b->name,"RemoveShortcuts")){if(b->sequence>lower)lower=b->sequence;}if(equal8(b->name,"RemoveFiles"))upper=b->sequence;}else{if(equal8(b->name,"InstallFiles"))lower=b->sequence;if(equal8(b->name,"InstallFinalize"))upper=b->sequence;}}if(!lower||!upper||a->sequence<=lower||a->sequence>=upper){status=50;break;}
  msi8_blob blob=binary_actions147(a);if(!blob.data){status=50;break;}free8(blob.data);
  if(!actions){actions=calloc8(1,sizeof(*actions));if(!actions){status=8;break;}}if(actions->count==16){status=1816;break;}
  msica_item147*item=calloc8(1,sizeof(*item));if(!item){status=8;break;}actions->items[actions->count++]=item;item->index=i;copy8(item->data,msip_get147(&p->properties,a->name),sizeof(item->data));status=command_actions147(p,item);
  if(!status&&((job8->command==W8_INSTALL&&item->operation!=1)||(job8->command==W8_REMOVE&&item->operation!=2)))status=50;
 }
 if(status){msica_close147(actions);return status;}*out=actions;return 0;
}
unsigned msica_records147(const msica147*actions,const msia_plan147*p,msij147*j){
 if(!actions)return 0;unsigned generated=0;for(unsigned i=0;i<actions->count;++i)if(actions->items[i]->operation==1){if(generated++)return 50;const msia_file147*f=p->files+actions->items[i]->file;unsigned status=msij_file147(j,WIN_TX_FILE147,"nativeLang.xml",f->size,f->sha256,WIN_TX_GENERATED147);if(status)return status;}return 0;
}
unsigned msi_current147(void);
unsigned msica_clean147(const msia_plan147*p,const char*path){
 if(!p||!p->file_count)return 2;unsigned known=0;for(unsigned i=0;i<p->action_count;++i)if(msia_dll_type147(p->actions[i].kind)){msi8_blob blob=binary_actions147(p->actions+i);if(blob.data){known=1;free8(blob.data);break;}}if(!known)return 2;
 w8_file_info info;uint8_t sha[32];if(stat8(path,&info)||info.kind!=1||info.size!=423704)return 2;unsigned status=msif_hash147(path,info.size,sha);if(status)return status;if(memcmp(sha,helper_sha147,32))return 2;return remove8(path)?1117:0;
}
unsigned msica_run147(const msica147*actions,msia_plan147*p,unsigned index,msia_custom_result147*out){
 if(!out)return 87;*out=(msia_custom_result147){0};if(!actions)return 50;const msica_item147*item=0;for(unsigned i=0;i<actions->count;++i)if(actions->items[i]->index==index)item=actions->items[i];if(!item)return 50;
 msi8_blob blob=binary_actions147(p->actions+index);if(!blob.data)return 23;char native[256],logical[256];copy8(native,p->product_root,256);append8(native,"/.EngacerMSI/stage/action.dll",256);copy8(logical,p->program_alias,256);if(len8(logical)+sizeof("\\.EngacerMSI\\stage\\action.dll")>256){free8(blob.data);return 206;}append8(logical,"\\.EngacerMSI\\stage\\action.dll",256);
 w8_file_info info;unsigned status=0;if(!stat8(native,&info)){uint8_t actual[32];status=msif_hash147(native,blob.size,actual);if(!status&&memcmp(actual,helper_sha147,32))status=23;}
 else{char directory[256];copy8(directory,p->product_root,256);append8(directory,"/.EngacerMSI/stage",256);status=msif_directory147(directory);int h=status?-1:open8(native,2);if(h<0){if(!status)status=5;}else{for(unsigned at=0;!status&&at<blob.size;){unsigned n=blob.size-at;if(n>4096)n=4096;if(write8(h,blob.data+at,n)!=(int)n)status=29;at+=n;sys8(W8_SYS_YIELD,0,0,0,0,0);}if(status)(void)sys8(W8_SYS_CLOSE,(unsigned)h,1,0,0,0);else if(close8(h))status=1117;}}
 free8(blob.data);uint8_t actual[32];if(!status)status=msif_hash147(native,423704,actual);if(!status&&memcmp(actual,helper_sha147,32))status=23;if(status)return status;
 WCHAR wide[256];unsigned n=len8(logical);for(unsigned i=0;i<=n;++i)wide[i]=(uint8_t)logical[i];unsigned session=msi_current147();if(!session)return 6;
 status=msia_deferred147(session,p->actions[index].kind,wide,p->actions[index].target,item->data,out);
 print8("M147_ORIGINAL_DEFERRED_BODY ");print8(p->actions[index].name);print8(" result=");number8(out->body_status);print8(" continued=");number8(out->continued);print8("\n");
 if(!status&&item->operation==1&&!out->body_status){char generated[256];copy8(generated,p->product_root,256);append8(generated,"/nativeLang.xml",256);const msia_file147*f=p->files+item->file;status=msif_hash147(generated,f->size,actual);if(!status&&memcmp(actual,f->sha256,32))status=23;}
 if(!status&&item->operation==2&&!out->body_status){uint64_t cursor=0;for(;;){w8_file_info entry;int64_t next=(int64_t)sys8(W8_SYS_ENUM,(uint64_t)(uintptr_t)p->product_root,(uint64_t)(uintptr_t)&entry,cursor,0,0);if(next<0){status=5;break;}if(!next)break;if((uint64_t)next<=cursor){status=13;break;}cursor=(uint64_t)next;if(!case8(entry.name,"nativeLang.xml")){status=23;break;}}}
 if(remove8(native)&&!status)status=1117;return status;
}
