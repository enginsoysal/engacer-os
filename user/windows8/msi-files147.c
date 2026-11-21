/* One LZX pass, bounded disk streaming, and extent promotion after journaling. */
#include "msi-files147.h"
#include "cab147.h"
static unsigned stream_status147(unsigned op,const void*data,uint64_t bytes){int64_t status=(int64_t)sys8(W8_SYS_STREAM147,op,(uint64_t)(uintptr_t)data,bytes,0,0);return status<0?(unsigned)-status:0;}
static unsigned stream_write147(const void*data,unsigned bytes){const uint8_t*p=data;while(bytes){unsigned n=bytes>4096?4096:bytes;unsigned status=stream_status147(2,p,n);if(status)return status;p+=n;bytes-=n;}return 0;}
static unsigned stream_finish147(void){
 unsigned status=stream_status147(3,0,0);if(status)return status;
 for(;;){int64_t done=(int64_t)sys8(W8_SYS_STREAM147,4,0,0,0,0);if(done<0)return (unsigned)-done;if(done)break;sys8(W8_SYS_YIELD,0,0,0,0,0);}
 return stream_status147(5,0,0);
}
static unsigned make_path147(char out[256],const char*root,const char*tail){unsigned a=len8(root),b=len8(tail);if(a+b>=256)return 206;memcpy(out,root,a);memcpy(out+a,tail,b+1);return 0;}
static unsigned stage_path147(const msia_plan147*p,unsigned index,char out[256]){
 if(index>=256)return 87;char tail[]="/.EngacerMSI/stage/f000";unsigned n=sizeof(tail)-2;tail[n]=(char)('0'+index%10);tail[n-1]=(char)('0'+index/10%10);tail[n-2]=(char)('0'+index/100);return make_path147(out,p->product_root,tail);
}
unsigned msif_directory147(const char*path){
 if(!path||path[0]!='/'||len8(path)>=256)return 87;char part[256];copy8(part,path,sizeof(part));
 for(unsigned i=1;;++i)if(!part[i]||part[i]=='/'){char saved=part[i];part[i]=0;w8_file_info info;unsigned status=stat8(part,&info)?(mkdir8(part)?1117:0):info.kind==2?0:183;part[i]=saved;if(status)return status;if(!saved)break;}
 return 0;
}
unsigned msif_hash147(const char*path,uint64_t bytes,uint8_t hash[32]){
 w8_file_info info;if(stat8(path,&info)||info.kind!=1||info.size!=bytes||bytes>32u*1024u*1024u)return 2;
 int handle=open8(path,0);if(handle<0)return 5;uint8_t buffer[4096];engine_sha256_context context;engine_sha256_init(&context);unsigned status=0;
 while(bytes){unsigned n=bytes>sizeof(buffer)?sizeof(buffer):(unsigned)bytes;if(read8(handle,buffer,n)!=(int)n||!engine_sha256_update(&context,buffer,n)){status=23;break;}bytes-=n;}
 if(close8(handle))status=1117;if(!status&&!engine_sha256_final(&context,hash))status=87;return status;
}
typedef struct {msia_plan147*plan;msij147*journal;const cab147_archive*archive;uint16_t map[256];unsigned active,current,offset,completed,status;engine_sha256_context hash;} stage147;
static unsigned finish_file147(stage147*s){
 if(!s->active)return 0;msia_file147*f=s->plan->files+s->current;if(s->offset!=f->size)return 23;
 unsigned status=stream_finish147();if(status)return status;if(!engine_sha256_final(&s->hash,f->sha256))return 87;
 char path[256];status=msia_file_path147(s->plan,s->current,path);if(status)return status;
 status=msij_file147(s->journal,WIN_TX_FILE147,path+len8(s->plan->product_root)+1,f->size,f->sha256,WIN_TX_PAYLOAD147);if(status)return status;
 s->active=0;++s->completed;progress8(15+s->completed*50/s->plan->selected_files,"Staging and checking original application files.");return 0;
}
static int stage_sink147(void*opaque,const cab147_file*file,unsigned offset,const void*data,unsigned bytes){
 stage147*s=opaque;unsigned index=(unsigned)(file-s->archive->files);if(index>=s->archive->count){s->status=87;return 1;}unsigned current=s->map[index];msia_file147*f=s->plan->files+current;
 if(!f->selected)return 0;
 if(!s->active||s->current!=current){
  s->status=finish_file147(s);if(s->status||offset)return 1;char path[256];s->status=stage_path147(s->plan,current,path);if(!s->status)s->status=stream_status147(1,path,f->size);if(s->status)return 1;
  s->active=1;s->current=current;s->offset=0;engine_sha256_init(&s->hash);
 }
 if(offset!=s->offset||bytes>f->size-s->offset){s->status=23;return 1;}
 s->status=stream_write147(data,bytes);if(s->status)return 1;if(!engine_sha256_update(&s->hash,data,bytes)){s->status=87;return 1;}s->offset+=bytes;return 0;
}
unsigned msif_stage147(msia_plan147*p,msij147*j,const void*source,unsigned bytes){
 if(!p||!p->costed||!j||!source||bytes!=p->source_bytes||!p->selected_files||job8->command!=W8_INSTALL||!equal8(p->product_root,job8->product_root)||memcmp(p->source_sha256,job8->source_sha147,32))return 87;
 w8_file_info existing;if(!stat8(p->product_root,&existing))return 183;
 uint64_t free_entries=sys8(W8_SYS_INFO,5,0,0,0,0);if(free_entries<p->selected_files+p->directory_count+8)return 1816;
 if(sys8(W8_SYS_INFO,3,0,0,0,0)<(uint64_t)bytes+p->selected_bytes+2u*WIN_TX_LIMIT147+1024u*1024u)return 112;
 for(unsigned i=0;i<p->file_count;++i)if(p->files[i].selected){char path[256];unsigned status=msia_file_path147(p,i,path);if(status)return status;const char*relative=path+len8(p->product_root)+1;if(!win_tx_relative147(relative,'/')||win_tx_equal147(relative,"product.bin"))return 50;char first[256];unsigned n=0;while(relative[n]&&relative[n]!='/'){first[n]=relative[n];++n;}first[n]=0;if(win_tx_equal147(first,".EngacerMSI"))return 50;}
 msi8_blob blob=msi8_stream(p->cabinet,0);cab147_archive*archive=0;unsigned status=cab147_open(blob,&archive);if(status){if(blob.data)free8(blob.data);return 13;}
 stage147*s=calloc8(1,sizeof(*s));if(!s){cab147_close(archive);free8(blob.data);return 8;}s->plan=p;s->journal=j;s->archive=archive;
 if(archive->count!=p->file_count)status=13;
 for(unsigned i=0;!status&&i<archive->count;++i){unsigned match=0;while(match<p->file_count&&!equal8(archive->files[i].name,p->files[match].id))++match;if(match==p->file_count||archive->files[i].size!=p->files[match].size)status=13;else{s->map[i]=(uint16_t)match;for(unsigned k=0;k<i;++k)if(s->map[k]==match)status=13;}}
 if(!status){int64_t made=(int64_t)sys8(W8_SYS_MKDIR,(uint64_t)(uintptr_t)p->product_root,1,0,0,0);if(made)status=183;}
 char path[256];if(!status)status=make_path147(path,p->product_root,"/.EngacerMSI");if(!status&&mkdir8(path))status=1117;
 if(!status)status=make_path147(path,p->product_root,"/.EngacerMSI/stage");if(!status&&mkdir8(path))status=1117;
 if(!status)status=make_path147(path,p->product_root,"/.EngacerMSI/source.msi");if(!status)status=stream_status147(1,path,bytes);if(!status)status=stream_write147(source,bytes);if(!status)status=stream_finish147();
 if(!status)status=msij_file147(j,WIN_TX_FILE147,".EngacerMSI/source.msi",bytes,p->source_sha256,WIN_TX_CACHE147);
 if(!status){unsigned walk=cab147_walk(archive,stage_sink147,s);status=s->status?s->status:walk?13:finish_file147(s);}
 if(!status&&s->completed!=p->selected_files)status=13;
 if(status)(void)stream_status147(6,0,0);free8(s);cab147_close(archive);free8(blob.data);return status;
}
unsigned msif_promote147(const msia_plan147*p){
 if(!p||!p->costed)return 87;
 for(unsigned i=0;i<p->file_count;++i)if(p->files[i].selected){char from[256],to[256],parent[256];unsigned status=stage_path147(p,i,from);if(!status)status=msia_file_path147(p,i,to);if(status)return status;copy8(parent,to,sizeof(parent));unsigned n=len8(parent);while(n&&parent[n-1]!='/')--n;if(!n)return 87;parent[n-1]=0;status=msif_directory147(parent);if(status)return status;
  int64_t moved=(int64_t)sys8(W8_SYS_MOVE,(uint64_t)(uintptr_t)from,(uint64_t)(uintptr_t)to,2,0,0);if(moved<0)return (unsigned)-moved;
 }
 return 0;
}
unsigned msif_verify147(const msij147*j){
 if(!j||!win_tx_validate147(j->data,j->bytes))return 87;const win_tx_header147*h=(const void*)j->data;char root[256];if(!win_product_make147(root,sizeof(root),h->code))return 87;
 unsigned checked=0;for(unsigned at=sizeof(*h);at<j->bytes;){const win_tx_record147*r=(const void*)(j->data+at);
  if(r->type==WIN_TX_FILE147||r->type==WIN_TX_LINK147){const win_tx_file147*f=(const void*)(r+1);char path[256];const char*base=r->type==WIN_TX_FILE147?root:f->flags?"/Data/Windows/Common/Programs":h->user;unsigned a=len8(base),b=len8(f->path);if(a+b+1>=sizeof(path))return 206;copy8(path,base,sizeof(path));path[a++]='/';memcpy(path+a,f->path,b+1);uint8_t hash[32];unsigned status=msif_hash147(path,f->bytes,hash);if(status||memcmp(hash,f->sha,32))return status?status:23;++checked;progress8(85+checked*10/(h->files+h->links),"Verifying installed application ownership.");}
  at+=r->bytes;
 }return 0;
}
