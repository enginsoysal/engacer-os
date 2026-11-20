/* One checked common-dialog request; user pointers are copied only in caller context. */
#include <engine/winpicker146.h>
typedef struct {wpick_view146 view;wpick_ofn146 ofn;uint64_t address;unsigned space,thread,state,error;char result[256];} picker_request146;
_Static_assert(sizeof(picker_request146)<=4096,"One lazy common-dialog page");
static picker_request146*picker_request;
static uint64_t picker_generation146;
static void picker_free146(void){ui_free144(picker_request);picker_request=0;}
static unsigned picker_caller146(uint64_t generation){return picker_request&&picker_request->space==active_space142&&picker_request->thread==current142&&picker_request->view.generation==generation;}
static void picker_thread_release146(unsigned space,unsigned thread){if(picker_request&&picker_request->space==space&&picker_request->thread==thread)picker_free146();}
static void picker_owner_destroy146(uint64_t owner){if(picker_request&&(picker_request->view.owner==owner||picker_request->ofn.owner==owner)){picker_request->state=3;picker_request->error=0xffff;thread142*t=spaces142[picker_request->space]->threads+picker_request->thread;if(t->state==T144_GUI){t->state=T142_READY;t->frame.rax=0;}}}
static unsigned picker_string_limit146(uint64_t pointer,char*out,unsigned capacity,unsigned limit,unsigned*units){
 unsigned at=0;if(!pointer){out[0]=0;if(units)*units=0;return 0;}
 for(unsigned i=0;i<limit;++i){uint16_t pair[2];unsigned count=1;if(user8(pointer+(uint64_t)i*2,pair,2,0))return 998;
  if(!pair[0]){out[at]=0;if(units)*units=i+1;return 0;}
  if(pair[0]>=0xd800&&pair[0]<=0xdbff){if(++i==limit)return 206;if(user8(pointer+(uint64_t)i*2,pair+1,2,0))return 998;count=2;}
  unsigned position=0;uint32_t scalar;if(!decode_utf16_143(pair,count,&position,&scalar))return 1113;
  if(!encode_utf8_143(scalar,out,capacity-1,&at))return 206;
 }return 206;
}
static unsigned picker_string146(uint64_t pointer,char*out,unsigned capacity,unsigned*units){return picker_string_limit146(pointer,out,capacity,1024,units);}
static unsigned picker_probe146(uint64_t address,unsigned bytes){
 if(address<W8_BASE||address>=W8_LIMIT||bytes>W8_LIMIT-address)return 0;
 while(bytes){uint64_t*p=pte8(address,0);if(p&&!(*p&1)&&(*p&RESERVED141)&&commit141(address,1,0))return 0;if(!p||!(*p&1)||!(*p&2))return 0;unsigned n=4096-(unsigned)(address&4095);if(n>bytes)n=bytes;address+=n;bytes-=n;}return 1;
}
static unsigned picker_granted146(const wpick_view146*v,const char*path,unsigned write){return prefix8(path,v->user_root)||(!write&&prefix8(path,v->product_root));}
static unsigned picker_filter_valid146(const char*pattern){unsigned any=0;for(unsigned i=0;pattern[i];++i){unsigned c=(uint8_t)pattern[i];if(c==';'){if(!any)return 0;any=0;continue;}if(!(c=='*'||c=='?'||c=='.'||c=='-'||c=='_'||(c>='0'&&c<='9')||(c>='a'&&c<='z')||(c>='A'&&c<='Z')))return 0;any=1;}return any;}
static unsigned picker_filter_string146(picker_request146*r,uint64_t address,unsigned*used,unsigned limit,unsigned*units,uint16_t*offset){
 if(*used>=WPICK_FILTER_TEXT146)return 1816;unsigned capacity=WPICK_FILTER_TEXT146-*used;if(capacity>limit)capacity=limit;
 char*text=r->view.filter_text+*used;unsigned error=picker_string146(address,text,capacity,units);if(error)return error;*offset=(uint16_t)*used;*used+=length8(text)+1;return 0;
}
static unsigned picker_read_filters146(picker_request146*r){
 uint64_t address=r->ofn.filter;if(!address){r->view.filter_index=0;return 0;}unsigned used=0;
 for(unsigned i=0;i<WPICK_FILTERS146;++i){unsigned units=0;wpick_filter146*f=r->view.filters+i;uint16_t first;if(user8(address,&first,2,0))return 998;if(!first){r->view.filter_count=i;return 0;}
  unsigned error=picker_filter_string146(r,address,&used,64,&units,&f->label);if(error)return error;
  if(!r->view.filter_text[f->label]){r->view.filter_count=i;return 0;}address+=(uint64_t)units*2;
  error=picker_filter_string146(r,address,&used,WPICK_PATTERN146,&units,&f->pattern);if(error)return error;
  if(!picker_filter_valid146(r->view.filter_text+f->pattern))return 50;address+=(uint64_t)units*2;r->view.filter_count=i+1;
 }
 uint16_t end;if(user8(address,&end,2,0))return 998;return end?1816:0;
}
static unsigned picker_windows146(const wpick_view146*v,const char*native,uint16_t*out,unsigned*count){
 char path[512];const char*tail=0;path_context143 context={v->user_root,v->product_root,input8.windows_root,m6_volume()->entries,V6_ENTRIES};unsigned error;
 if(prefix8(native,v->user_root)){error=path_user_alias143(&context,path,sizeof(path));tail=native+length8(v->user_root);}
 else if(prefix8(native,v->product_root)){error=path_copy143(path,input8.windows_root,sizeof(path));tail=native+length8(v->product_root);}
 else return 5;
 if(error)return error;if(path_append143(path,tail,sizeof(path)))return 206;for(unsigned i=0;path[i];++i)if(path[i]=='/')path[i]='\\';
 w8_path_result143 resolved;error=path_policy143(&context,path,path,0,&resolved);if(error||!equal8(resolved.native,native))return error?error:123;
 unsigned at=0,used=0,n=length8(path);while(at<n){uint32_t scalar;if(!decode_utf8_143(path,n,&at,&scalar)||!encode_utf16_143(scalar,out,511,&used))return 1113;}out[used]=0;*count=used;return 0;
}
unsigned w8_picker_view146(wpick_view146*out){if(!picker_request||picker_request->state==3)return 0;if(out)*out=picker_request->view;return picker_request->state;}
unsigned w8_picker_display146(uint64_t generation){if(!picker_request||picker_request->view.generation!=generation||picker_request->state!=1)return 0;picker_request->state=2;return 1;}
unsigned w8_picker_allowed146(uint64_t generation,const char*path,unsigned write){return picker_request&&picker_request->view.generation==generation&&picker_request->state<3&&picker_granted146(&picker_request->view,path,write);}
unsigned w8_picker_matches146(uint64_t generation,const char*name,unsigned filter){
 if(!picker_request||picker_request->view.generation!=generation||picker_request->state==3)return 0;
 const wpick_view146*v=&picker_request->view;if(!v->filter_count)return 1;if(filter>=v->filter_count)return 0;
 const char*pattern=wpick_pattern146(v,filter);unsigned at=0;
 while(pattern[at]){char part[WPICK_PATTERN146];unsigned used=0;while(pattern[at]&&pattern[at]!=';')part[used++]=pattern[at++];part[used]=0;if(pattern[at])++at;
  unsigned matched=0;if(equal8(part,"*.*")||equal8(part,"*"))return 1;if(!find_match_core143(part,used,name,length8(name),&matched)&&matched)return 1;
 }return 0;
}
unsigned w8_picker_complete146(uint64_t generation,const char*path,unsigned filter,unsigned error){
 if(!picker_request||picker_request->view.generation!=generation||picker_request->state==3)return 0;
 if(path&&(!picker_granted146(&picker_request->view,path,picker_request->view.save)||length8(path)>=256))return 0;
 if(path)memcpy(picker_request->result,path,length8(path)+1);picker_request->view.filter_index=filter;picker_request->error=error;picker_request->state=3;
 thread142*t=spaces142[picker_request->space]->threads+picker_request->thread;if(t->state==T144_GUI){t->state=T142_READY;t->frame.rax=0;}return 1;
}

static int64_t picker_begin146(uint64_t address,uint64_t directory,unsigned save){
 if(picker_request||picker_generation146>=INT64_MAX)return -0xffff;
 unsigned size;if(user8(address,&size,4,0))return -0xffff;if(size!=136&&size!=152)return -1;
 picker_request146*r=ui_page144();if(!r)return -9;
 picker_request=r;r->address=address;r->space=active_space142;r->thread=current142;r->state=1;r->view.save=save;
 unsigned error=0;if(user8(address,&r->ofn,size,0)){error=0xffff;goto fail;}
 wpick_ofn146*ofn=&r->ofn;ui_window144*owner=ui_owned144(ofn->owner);
 if(!owner||owner->thread!=current142||!owner->view.description.visible){error=0xffff;goto fail;}
 uint64_t root=owner->view.handle;for(unsigned depth=0;owner->view.description.parent&&depth<WUI_WINDOWS144;++depth){owner=ui_owned144(owner->view.description.parent);if(!owner){error=0xffff;goto fail;}root=owner->view.handle;}
 r->view.owner=root;r->view.flags=ofn->flags;
 if((ofn->flags&~0x0088980eu)||ofn->custom_filter||ofn->flags_ex||ofn->reserved||ofn->reserved_pointer||!ofn->file||!ofn->file_capacity||ofn->file_capacity>32768){error=2;goto fail;}
 if(!picker_probe146(address,size)||!picker_probe146(ofn->file,2)){error=0xffff;goto fail;}
 memcpy(r->view.user_root,input8.user_root,256);memcpy(r->view.product_root,input8.product_root,256);
 if(picker_read_filters146(r)){error=2;goto fail;}
 r->view.filter_index=r->view.filter_count?ofn->filter_index?ofn->filter_index-1:0:0;
 if(r->view.filter_count&&r->view.filter_index>=r->view.filter_count)r->view.filter_index=0;
 if(picker_string146(ofn->title,r->view.title,sizeof(r->view.title),0)||picker_string146(ofn->default_extension,r->view.extension,sizeof(r->view.extension),0)){error=2;goto fail;}
 for(unsigned i=0;r->view.extension[i];++i){unsigned c=(uint8_t)r->view.extension[i];if(!(c=='_'||c=='-'||(c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9'))){error=2;goto fail;}}
 char file[512],initial[1024],cwd[1024];unsigned units;
 if(picker_string_limit146(ofn->file,file,sizeof(file),ofn->file_capacity<1024?ofn->file_capacity:1024,&units)||picker_string146(ofn->initial_directory,initial,sizeof(initial),0)||picker_string146(directory,cwd,sizeof(cwd),0)){error=2;goto fail;}
 path_context143 context={input8.user_root,input8.product_root,input8.windows_root,m6_volume()->entries,V6_ENTRIES};w8_path_result143 resolved;
 if(!cwd[0]){if(path_user_alias143(&context,cwd,sizeof(cwd))||path_append143(cwd,"\\Documents",sizeof(cwd))){error=2;goto fail;}}
 unsigned full=0;for(unsigned i=0;file[i];++i)if(file[i]=='/'||file[i]=='\\'||file[i]==':')full=1;
 const char*selected=full?file:initial[0]?initial:cwd;
 if(path_policy143(&context,selected,cwd,0,&resolved)||!path8(resolved.native,0)){error=2;goto fail;}
 memcpy(r->view.directory,resolved.native,256);
 if(full){unsigned end=length8(r->view.directory),begin=end;while(begin&&r->view.directory[begin-1]!='/')--begin;
  if(!begin){error=2;goto fail;}memcpy(r->view.name,r->view.directory+begin,end-begin+1);r->view.directory[begin-1]=0;
 }else if(path_copy143(r->view.name,file,256)){error=2;goto fail;}
 const v6_entry*entry=find8(r->view.directory);if(!entry||entry->kind!=2||!picker_granted146(&r->view,r->view.directory,0)){error=2;goto fail;}
 r->view.generation=++picker_generation146;return(int64_t)r->view.generation;
fail:picker_free146();return -(int64_t)(error?error:2);
}
static int64_t picker_result146(void){
 picker_request146*r=picker_request;if(r->state!=3)return 2;
 if(r->error){unsigned error=r->error;picker_free146();return -(int64_t)error;}
 if(!r->result[0]){picker_free146();return 0;}
 uint16_t path[512];unsigned units=0;unsigned error=picker_windows146(&r->view,r->result,path,&units);
 if(error||!path8(r->result,r->view.save)){picker_free146();return -0xffff;}
 const v6_entry*entry=find8(r->result);if((entry&&entry->kind!=1)||(!r->view.save&&!entry)){picker_free146();return -0xffff;}
 if(units+1>r->ofn.file_capacity){uint16_t required=(uint16_t)(units+1);if(!picker_probe146(r->ofn.file,2)||user8(r->ofn.file,&required,2,1)){picker_free146();return -0xffff;}picker_free146();return -0x3003;}
 unsigned offset=0,extension=0;for(unsigned i=0;i<units;++i){if(path[i]=='\\'){offset=i+1;extension=0;}else if(path[i]=='.')extension=i+1;}
 unsigned title_units=units-offset;
 if((r->ofn.file_title&&r->ofn.title_capacity&&title_units+1>r->ofn.title_capacity)||!picker_probe146(r->address,r->ofn.size)||!picker_probe146(r->ofn.file,(units+1)*2)||(r->ofn.file_title&&r->ofn.title_capacity&&!picker_probe146(r->ofn.file_title,(title_units+1)*2))){picker_free146();return -0xffff;}
 r->ofn.file_offset=(uint16_t)offset;r->ofn.file_extension=(uint16_t)extension;r->ofn.filter_index=r->view.filter_count?r->view.filter_index+1:0;
 error=user8(r->ofn.file,path,(units+1)*2,1);
 if(!error&&r->ofn.file_title&&r->ofn.title_capacity)error=user8(r->ofn.file_title,path+offset,(title_units+1)*2,1);
 if(!error)error=user8(r->address,&r->ofn,r->ofn.size,1);picker_free146();return error?-0xffff:1;
}
static int64_t picker_call146(uint64_t operation,uint64_t pointer,uint64_t argument,trap_frame*f){
 if(operation==WPICK_OPEN146||operation==WPICK_SAVE146)return picker_begin146(pointer,argument,operation==WPICK_SAVE146);
 if(pointer||!picker_caller146(argument))return -0xffff;
 if(operation==WPICK_RESULT146)return picker_result146();
 if(operation==WPICK_CANCEL146){picker_free146();return 0;}
 if(operation==WPICK_WAIT146){
  if(picker_request->state==3)return 0;wui_queue144*q=ui_queue144(active_space142,current142,1);if(!q)return -9;
  wui_filter144 filter={.remove=1};if(q->quit||ui_find144(q,&filter)>=0||ui_timer_peek144(&filter,0,1))return 0;
  q->waiting=filter;threads142[current142].deadline=ui_timer_deadline144(&filter);threads142[current142].state=T144_GUI;context8=*f;context8.rax=0;w8_active=0;w8_escape();
 }
 return -2;
}

const wpick_view146*w8_picker_native146(void){return picker_request&&picker_request->state<3?&picker_request->view:0;}
const v6_entry*w8_picker_existing146(uint64_t generation,const char*path){if(!w8_picker_allowed146(generation,path,0))return 0;const v6_entry*match=0;for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*e=m6_volume()->entries+i;if(e->kind&&equal_utf8_143(e->path,length8(e->path),path,length8(path))==1){if(match)return 0;match=e;}}return match;}
