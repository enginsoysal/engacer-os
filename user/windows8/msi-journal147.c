/* One immutable, bounded write-ahead image; no growing per-file disk rewrites. */
#include "msi-journal147.h"
static unsigned reserve_journal147(msij147*j,unsigned bytes){
 if(bytes>WIN_TX_LIMIT147)return 1816;if(bytes<=j->capacity)return 0;
 unsigned capacity=j->capacity?j->capacity:4096;while(capacity<bytes)capacity*=2;
 uint8_t*next=realloc8(j->data,capacity);if(!next)return 8;j->data=next;j->capacity=capacity;return 0;
}
msij147 *msij_create147(const msia_plan147*p){
 if(!p||!p->costed||!win_product_guid147(p->code,1)||!win_tx_alias147(p->program_alias))return 0;
 msij147*j=calloc8(1,sizeof(*j));if(!j)return 0;
 if(reserve_journal147(j,sizeof(win_tx_header147))){msij_close147(j);return 0;}
 memset(j->data,0,sizeof(win_tx_header147));j->bytes=sizeof(win_tx_header147);win_tx_header147*h=(void*)j->data;
 h->magic=WIN_TX_MAGIC147;h->schema=1;h->bytes=j->bytes;memcpy(h->source_sha,p->source_sha256,32);
 copy8(h->code,p->code,sizeof(h->code));copy8(h->user,job8->user_root,sizeof(h->user));copy8(h->alias,p->program_alias,sizeof(h->alias));copy8(h->product,p->product,sizeof(h->product));copy8(h->version,p->version,sizeof(h->version));copy8(h->publisher,p->publisher,sizeof(h->publisher));
 const char*upgrade=msip_get147(&p->properties,"UpgradeCode");if(upgrade[0]){if(!win_product_guid147(upgrade,0)){msij_close147(j);return 0;}copy8(h->upgrade,upgrade,sizeof(h->upgrade));for(unsigned i=0;h->upgrade[i];++i)if(h->upgrade[i]>='a'&&h->upgrade[i]<='f')h->upgrade[i]-=32;}
 if(!win_tx_header_shape147(h,j->bytes)){msij_close147(j);return 0;}return j;
}
void msij_close147(msij147*j){if(j){if(j->data)free8(j->data);free8(j);}}
unsigned msij_append147(msij147*j,unsigned kind,const void*value,unsigned bytes){
 if(!j||!j->data||kind<1||kind>5||(!value&&bytes)||bytes>WIN_TX_LIMIT147-8)return 87;
 unsigned total=(bytes+15)&~7u;if(j->bytes>WIN_TX_LIMIT147-total)return 1816;
 const win_tx_header147*old=(const void*)j->data;unsigned count=kind==1?old->files:kind==2?old->registry:kind==3?old->links:kind==4?old->keys:old->properties;
 unsigned limit=kind==1?258:kind==2?128:kind==3?32:kind==4?128:256;if(count==limit||old->records==1024)return 1816;
 unsigned result=reserve_journal147(j,j->bytes+total);if(result)return result;
 win_tx_record147*r=(void*)(j->data+j->bytes);memset(r,0,total);r->type=kind;r->bytes=total;if(bytes)memcpy(r+1,value,bytes);j->bytes+=total;
 win_tx_header147*h=(void*)j->data;h->bytes=j->bytes;++h->records;
 if(kind==1)++h->files;else if(kind==2)++h->registry;else if(kind==3)++h->links;else if(kind==4)++h->keys;else ++h->properties;
 memset(h->checksum,0,32);return 0;
}
unsigned msij_file147(msij147*j,unsigned kind,const char*path,uint64_t bytes,const uint8_t hash[32],unsigned flags){
 if(!path||!hash||(kind!=1&&kind!=3)||len8(path)>=256)return 87;win_tx_file147 file={0};copy8(file.path,path,sizeof(file.path));file.bytes=bytes;file.flags=flags;memcpy(file.sha,hash,32);return msij_append147(j,kind,&file,sizeof(file));
}
unsigned msij_properties147(msij147*j,const msip_session147*s){
 if(!j||!s)return 87;uint8_t*buffer=alloc8(8+73+4097);if(!buffer)return 8;unsigned status=0;
 for(unsigned i=0;i<s->count;++i){const msip_item147*item=s->items+i;unsigned name=len8(item->block)+1,value=len8(item->value)+1;if(name<2||name>73||value>4097){status=87;break;}
  msij147*owner=j;win_tx_property147*p=(void*)buffer;p->name_bytes=name;p->value_bytes=value;memcpy(buffer+8,item->block,name);memcpy(buffer+8+name,item->value,value);status=msij_append147(owner,WIN_TX_PROPERTY147,buffer,8+name+value);if(status)break;
 }
 free8(buffer);return status;
}
unsigned msij_seal147(msij147*j){if(!j||!j->data||j->bytes<1024)return 87;win_tx_header147*h=(void*)j->data;if(!win_tx_digest147(j->data,j->bytes,h->checksum)||!win_tx_validate147(j->data,j->bytes))return 87;return 0;}
unsigned msij_write147(msij147*j,const char*path){
 unsigned status=msij_seal147(j);if(status)return status;
 /* Exclusive creation makes a stale/replaced recovery record a refusal. */
 int handle=open8(path,2);if(handle<0)return 5;
 if(write8(handle,j->data,j->bytes)!=(int)j->bytes){(void)sys8(W8_SYS_CLOSE,(unsigned)handle,1,0,0,0);return 29;}
 if(close8(handle))return 1117;
 void*check=0;unsigned bytes=load8(path,&check,WIN_TX_LIMIT147);if(!bytes)return 1117;
 status=bytes!=j->bytes||memcmp(check,j->data,bytes)||!win_tx_validate147(check,bytes)?1117:0;free8(check);return status;
}
msij147 *msij_read147(const char*path,const char*root,const char*user){
 void*data=0;unsigned bytes=load8(path,&data,WIN_TX_LIMIT147);if(!bytes)return 0;
 if(!win_tx_validate147(data,bytes)||!win_tx_bound147(data,root,user,0)){free8(data);return 0;}
 msij147*j=calloc8(1,sizeof(*j));if(!j){free8(data);return 0;}j->data=data;j->bytes=bytes;j->capacity=bytes;return j;
}
