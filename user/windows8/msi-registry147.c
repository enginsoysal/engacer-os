/* Actual registry effects with immutable before/after ownership and guarded undo. */
#include "msi-registry147.h"
#include "msi_db.h"
#include "msi-text147.h"
static unsigned reg_call147(unsigned op,w8_registry_request143*q,w8_registry_result143*r){q->result=(uint64_t)(uintptr_t)r;int64_t code=(int64_t)sys8(W8_SYS_REGISTRY143,op,(uint64_t)(uintptr_t)q,0,0,0);return code<0?(unsigned)-code:0;}
static unsigned reg_wide147(const char*s,uint16_t*out,unsigned cap){unsigned n=cap;return msit_outwide147(s,out,&n);}
static unsigned reg_open147(unsigned root,unsigned view,const char*key,unsigned write,uint64_t*out){
 uint16_t wide[256];unsigned code=reg_wide147(key,wide,256);if(code)return code;
 unsigned flags=root==2?(view==32?0x200u:0x100u):0;
 w8_registry_request143 q={.root=UINT64_C(0x80000000)+root,.name=(uint64_t)(uintptr_t)wide,.access=(write?0x2001fu:0x20019u)|flags};w8_registry_result143 r={0};code=reg_call147(write==1?2:1,&q,&r);if(!code)*out=r.handle;return code;
}
static unsigned reg_close147(uint64_t handle){w8_registry_request143 q={.root=handle};return reg_call147(5,&q,0);}
static unsigned reg_query147(unsigned root,unsigned view,const char*key,const char*name,unsigned*type,uint8_t data[2048],unsigned*bytes){
 uint64_t handle=0;unsigned code=reg_open147(root,view,key,0,&handle);if(code)return code;uint16_t wide[256];code=reg_wide147(name,wide,256);
 if(!code){w8_registry_request143 q={.root=handle,.name=(uint64_t)(uintptr_t)wide,.data=(uint64_t)(uintptr_t)data,.bytes=2048};w8_registry_result143 r={0};code=reg_call147(4,&q,&r);if(!code){*type=r.type;*bytes=r.bytes;}}
 unsigned closed=reg_close147(handle);return code?code:closed;
}
static unsigned reg_write147(unsigned root,unsigned view,const char*key,const char*name,unsigned type,const uint8_t*data,unsigned bytes,unsigned remove){
 uint64_t handle=0;unsigned code=reg_open147(root,view,key,remove?2:1,&handle);if(code)return remove&&code==2?0:code;uint16_t wide[256];code=reg_wide147(name,wide,256);
 if(!code){w8_registry_request143 q={.root=handle,.name=(uint64_t)(uintptr_t)wide,.type=type,.data=(uint64_t)(uintptr_t)data,.bytes=bytes};code=reg_call147(remove?6:3,&q,0);if(remove&&code==2)code=0;}
 unsigned closed=reg_close147(handle);return code?code:closed;
}
static unsigned reg_empty_key147(unsigned root,unsigned view,const char*key){
 uint64_t handle=0;unsigned code=reg_open147(root,view,key,0,&handle);if(code)return code==2?0:code;unsigned empty=1;uint16_t name[256];
 for(unsigned op=7;op<=9;op+=2){w8_registry_request143 q={.root=handle,.name_output=(uint64_t)(uintptr_t)name,.name_capacity=256};w8_registry_result143 r={0};unsigned status=reg_call147(op,&q,&r);if(status==0||status==234)empty=0;else if(status!=259){code=status;break;}}
 unsigned closed=reg_close147(handle);if(code||closed)return code?code:closed;if(!empty)return 0;uint16_t wide[256];code=reg_wide147(key,wide,256);if(code)return code;
 w8_registry_request143 q={.root=UINT64_C(0x80000000)+root,.name=(uint64_t)(uintptr_t)wide,.access=root==2?(view==32?0x200u:0x100u):0};code=reg_call147(10,&q,0);return code==2?0:code;
}
static unsigned ascii_reg147(const char*s){for(unsigned i=0;s[i];++i)if((uint8_t)s[i]>=127)return 0;return 1;}
static unsigned component_reg147(const msia_plan147*p,const char*name){for(unsigned i=0;i<p->component_count;++i)if(equal8(p->components[i].id,name))return i;return UINT32_MAX;}
static unsigned destination_reg147(const msia_plan147*p,int authored,unsigned component,const char*key,unsigned*root,unsigned*view,char out[256]){
 if(authored < -1||authored>2||component>=p->component_count||len8(key)>=256||!ascii_reg147(key))return 50;
 unsigned machine=equal8(msip_get147(&p->properties,"ALLUSERS"),"1");*root=authored<=0?(machine?2:1):(unsigned)authored;*view=(p->components[component].attributes&256)?64:32;
 copy8(out,authored==0?"Software\\Classes\\":"",256);if(len8(out)+len8(key)>=256)return 206;append8(out,key,256);
 /* Selected ordinary HKCU software keys share one view. Per-user Classes redirection is deferred. */
 if(*root==1){const char*classes="Software\\Classes";unsigned n=len8(classes);if(len8(out)>=n){char first[17];memcpy(first,out,n);first[n]=0;if(win_tx_equal147(first,classes)&&(!out[n]||out[n]=='\\'))return 50;}*view=64;}
 return win_tx_reg_path147(out,len8(out)+1,0)?0:87;
}
static int hex_reg147(unsigned c){return c>='0'&&c<='9'?(int)(c-'0'):c>='a'&&c<='f'?(int)(c-'a'+10):c>='A'&&c<='F'?(int)(c-'A'+10):-1;}
static unsigned typed_reg147(const char*text,unsigned*type,uint8_t data[2048],unsigned*bytes){
 *type=1;if(text[0]=='#'&&text[1]=='#')++text;
 else if(text[0]=='#'&&text[1]=='x'){unsigned n=len8(text+2);if((n&1)||n>4096)return 87;*type=3;*bytes=n/2;for(unsigned i=0;i<n;i+=2){int a=hex_reg147((uint8_t)text[i+2]),b=hex_reg147((uint8_t)text[i+3]);if(a<0||b<0)return 87;data[i/2]=(uint8_t)(a*16+b);}return 0;}
 else if(text[0]=='#'&&text[1]=='%'){*type=2;text+=2;}
 else if(text[0]=='#'){const char*p=text+1;unsigned negative=*p=='-';if(*p=='-'||*p=='+')++p;if(!*p)return 87;uint64_t number=0;for(unsigned i=0;p[i];++i){if(p[i]<'0'||p[i]>'9'||number>UINT32_MAX/10u)return 87;number=number*10u+(unsigned)(p[i]-'0');if(number>(negative?UINT64_C(2147483648):UINT32_MAX))return 87;}uint32_t value=negative?(uint32_t)(0u-(uint32_t)number):(uint32_t)number;memcpy(data,&value,4);*type=4;*bytes=4;return 0;}
 uint16_t wide[1024];unsigned cap=1024;unsigned code=msit_outwide147(text,wide,&cap);if(code)return code;*bytes=(cap+1)*2;memcpy(data,wide,*bytes);return 0;
}
static unsigned has_key_reg147(const msij147*j,unsigned root,unsigned view,const char*key){for(unsigned at=1024;at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==WIN_TX_KEY147){const win_tx_key147*k=(const void*)(r+1);if(k->root==root&&k->view==view&&win_tx_equal147((const char*)(k+1),key))return 1;}at+=r->bytes;}return 0;}
static unsigned snapshot_keys147(msij147*j,unsigned root,unsigned view,const char*key){
 char prefix[256];copy8(prefix,key,sizeof(prefix));for(unsigned at=0;;++at){if(!prefix[at]||prefix[at]=='\\'){char saved=prefix[at];prefix[at]=0;uint64_t h=0;unsigned code=reg_open147(root,view,prefix,0,&h);if(!code)code=reg_close147(h);else if(code==2){code=0;if(!has_key_reg147(j,root,view,prefix)){uint8_t record[sizeof(win_tx_key147)+256];win_tx_key147*k=(void*)record;*k=(win_tx_key147){root,view,len8(prefix)+1,0};memcpy(k+1,prefix,k->key_bytes);code=msij_append147(j,WIN_TX_KEY147,record,sizeof(*k)+k->key_bytes);}}
  prefix[at]=saved;if(code)return code;if(!saved)break;
 }}
 return 0;
}
static unsigned quota_reg147(const msia_plan147*p,const msij147*j){
 unsigned keys[3]={0},values[3]={0};for(unsigned at=1024;at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);unsigned root=0,view=0,add=0;if(r->type==WIN_TX_KEY147){const win_tx_key147*k=(const void*)(r+1);root=k->root;view=k->view;add=1;}else if(r->type==WIN_TX_REG147){const win_tx_reg147*v=(const void*)(r+1);root=v->root;view=v->view;add=!v->before_exists;}if(add){unsigned slot=root==1?0:view==32?1:2;if(r->type==WIN_TX_KEY147)++keys[slot];else ++values[slot];}at+=r->bytes;}
 unsigned entries=0;for(unsigned i=0;i<3;++i){if(!keys[i]&&!values[i])continue;w8_registry_request143 q={.root=UINT64_C(0x80000000)+(i?2:1),.access=i?(i==1?0x200u:0x100u):0};w8_registry_result143 r={0};unsigned code=reg_call147(11,&q,&r);if(code)return code;if(r.type>r.name_units||r.bytes>r.disposition||keys[i]>r.name_units-r.type||values[i]>r.disposition-r.bytes)return 1450;entries+=keys[i]*2+values[i]+8;}
 msi8_table links=msi8_table_open("Shortcut");unsigned shortcuts=links.rows;if(links.data.data)free8(links.data.data);if(shortcuts>32)return 1816;entries+=p->selected_files+p->directory_count+shortcuts*2+24;return sys8(W8_SYS_INFO,5,0,0,0,0)<entries?1816:0;
}
unsigned msireg_snapshot147(msia_plan147*p,msij147*j){
 if(!p||!p->costed||!j)return 87;msi8_table table=msi8_table_open("Registry");if(table.rows>128||(table.rows&&table.columns!=6)){if(table.data.data)free8(table.data.data);return 50;}
 uint8_t*record=alloc8(sizeof(win_tx_reg147)+512+4096);if(!record){if(table.data.data)free8(table.data.data);return 8;}unsigned status=0;
 for(unsigned row=0;row<table.rows&&!status;++row){unsigned component=component_reg147(p,msi8_text(&table,row,5));if(component==UINT32_MAX){status=87;break;}if(!p->components[component].selected)continue;
  char key[256],physical[256],name[256],formatted[4097];status=msia_format147(p,msi8_text(&table,row,2),key,sizeof(key));if(!status)status=msia_format147(p,msi8_text(&table,row,3),name,sizeof(name));if(!status)status=msia_format147(p,msi8_text(&table,row,4),formatted,sizeof(formatted));if(status)break;
  if(!ascii_reg147(name)||!win_tx_reg_path147(name,len8(name)+1,1)||equal8(name,"+")||equal8(name,"-")||equal8(name,"*")){status=50;break;}
  unsigned root=0,view=0;status=destination_reg147(p,msi8_integer(&table,row,1),component,key,&root,&view,physical);if(status)break;status=snapshot_keys147(j,root,view,physical);if(status)break;
  win_tx_reg147*v=(void*)record;memset(v,0,sizeof(*v));v->root=root;v->view=view;v->key_bytes=len8(physical)+1;v->name_bytes=len8(name)+1;uint8_t*after=record+sizeof(*v)+v->key_bytes+v->name_bytes;memcpy(v+1,physical,v->key_bytes);memcpy(record+sizeof(*v)+v->key_bytes,name,v->name_bytes);
  status=typed_reg147(formatted,&v->after_type,after,&v->after_bytes);if(status)break;unsigned prior_type=0,prior_bytes=0;status=reg_query147(root,view,physical,name,&prior_type,after+v->after_bytes,&prior_bytes);if(!status){v->before_exists=1;v->before_type=prior_type;v->before_bytes=prior_bytes;}else if(status==2)status=0;if(status)break;
  status=msij_append147(j,WIN_TX_REG147,record,sizeof(*v)+v->key_bytes+v->name_bytes+v->after_bytes+v->before_bytes);
 }
 free8(record);if(table.data.data)free8(table.data.data);if(!status)status=quota_reg147(p,j);if(!status)status=msij_seal147(j);return status;
}
static unsigned record_reg147(const win_tx_reg147*v,unsigned undo){
 const char*key=(const char*)(v+1),*name=key+v->key_bytes;const uint8_t*after=(const uint8_t*)name+v->name_bytes,*before=after+v->after_bytes;uint8_t actual[2048];unsigned type=0,bytes=0;unsigned code=reg_query147(v->root,v->view,key,name,&type,actual,&bytes);if(code&&code!=2)return code;
 unsigned matches_after=!code&&type==v->after_type&&bytes==v->after_bytes&&!memcmp(actual,after,bytes);
 unsigned matches_before=v->before_exists?!code&&type==v->before_type&&bytes==v->before_bytes&&!memcmp(actual,before,bytes):code==2;
 if(undo){if(matches_before||!matches_after)return 0;return reg_write147(v->root,v->view,key,name,v->before_type,before,v->before_bytes,!v->before_exists);}
 if(matches_after)return 0;if(!matches_before)return 1018;return reg_write147(v->root,v->view,key,name,v->after_type,after,v->after_bytes,0);
}
unsigned msireg_apply147(const msij147*j){if(!j||!win_tx_validate147(j->data,j->bytes))return 87;for(unsigned at=1024;at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);if(r->type==WIN_TX_REG147){unsigned code=record_reg147((const void*)(r+1),0);if(code)return code;}at+=r->bytes;}return 0;}
unsigned msireg_undo147(const msij147*j){
 if(!j||!win_tx_validate147(j->data,j->bytes))return 87;uint32_t*offsets=alloc8(1024*sizeof(uint32_t));if(!offsets)return 8;unsigned count=0,status=0;for(unsigned at=1024;at<j->bytes;){offsets[count++]=at;const win_tx_record147*r=(const void*)(j->data+at);at+=r->bytes;}
 while(count&&!status){const win_tx_record147*r=(const void*)(j->data+offsets[--count]);if(r->type==WIN_TX_REG147)status=record_reg147((const void*)(r+1),1);else if(r->type==WIN_TX_KEY147){const win_tx_key147*k=(const void*)(r+1);status=reg_empty_key147(k->root,k->view,(const char*)(k+1));}}
 free8(offsets);return status;
}
unsigned msireg_appsearch147(msia_plan147*p){
 if(!p||p->costed)return 87;msi8_table search=msi8_table_open("AppSearch"),locator=msi8_table_open("RegLocator"),signatures=msi8_table_open("Signature");unsigned status=0;
 if(search.rows>64||locator.rows>64||(search.rows&&search.columns!=2)||(locator.rows&&locator.columns!=5)||signatures.rows)status=50;
 for(unsigned row=0;row<search.rows&&!status;++row){const char*property=msi8_text(&search,row,0),*signature=msi8_text(&search,row,1);unsigned found=0;
  for(unsigned i=0;i<locator.rows&&!status;++i)if(equal8(signature,msi8_text(&locator,i,0))){found=1;int root=msi8_integer(&locator,i,1),kind=msi8_integer(&locator,i,4);if((root!=1&&root!=2)||(kind!=2&&kind!=18)){status=50;break;}char key[256],name[256];status=msia_format147(p,msi8_text(&locator,i,2),key,sizeof(key));if(!status)status=msia_format147(p,msi8_text(&locator,i,3),name,sizeof(name));if(status)break;uint8_t data[2048];unsigned type=0,bytes=0;status=reg_query147((unsigned)root,kind&16?64:32,key,name,&type,data,&bytes);if(status==2){status=0;continue;}if(status)break;
   char text[4097];if(type==1){if(bytes<2||(bytes&1)||data[bytes-1]||data[bytes-2]){status=13;break;}status=msit_fromwide147((const uint16_t*)(const void*)data,text+1,sizeof(text)-1);if(status)break;if(text[1]=='#')text[0]='#';else memmove(text,text+1,len8(text+1)+1);}
   else if(type==4&&bytes==4){uint32_t n;memcpy(&n,data,4);char reversed[16];unsigned digits=0,at=1;do{reversed[digits++]=(char)('0'+n%10);n/=10;}while(n);text[0]='#';while(digits)text[at++]=reversed[--digits];text[at]=0;}
   else if(type==3){if(bytes>2047){status=1816;break;}text[0]='#';text[1]='x';const char*hex="0123456789ABCDEF";for(unsigned k=0;k<bytes;++k){text[2+k*2]=hex[data[k]>>4];text[3+k*2]=hex[data[k]&15];}text[2+bytes*2]=0;}
   else{status=50;break;}
   status=msip_set147(&p->properties,property,text);
  }
  if(!found)status=50;
 }
 if(search.data.data)free8(search.data.data);if(locator.data.data)free8(locator.data.data);if(signatures.data.data)free8(signatures.data.data);return status;
}
