#ifndef ENGINE_WINTXN147_H
#define ENGINE_WINTXN147_H
#include <engine/base.h>
#include <engine/sha256.h>
#include <engine/winproduct147.h>
/* Immutable write-ahead ownership. Publication renames this same checked image. */
#define WIN_TX_MAGIC147 UINT64_C(0x314e58544d474e45)
#define WIN_TX_LIMIT147 (512u*1024u)
enum {WIN_TX_FILE147=1,WIN_TX_REG147=2,WIN_TX_LINK147=3,WIN_TX_KEY147=4,WIN_TX_PROPERTY147=5};
enum {WIN_TX_PAYLOAD147=1,WIN_TX_GENERATED147=2,WIN_TX_CACHE147=4};
typedef struct {
 uint64_t magic;
 uint32_t schema,bytes,records,files,registry,links,keys,properties;
 uint8_t source_sha[32],checksum[32];
 char code[40],user[256],alias[256],product[96],version[32],publisher[96],upgrade[40];
 uint8_t reserved[104];
} win_tx_header147;
typedef struct {uint32_t type,bytes;} win_tx_record147;
typedef struct {char path[256];uint8_t sha[32];uint64_t bytes;uint32_t flags,reserved;} win_tx_file147;
typedef struct {uint32_t root,view,after_type,before_type,after_bytes,before_bytes,key_bytes,name_bytes,before_exists,reserved;} win_tx_reg147;
typedef struct {uint32_t root,view,key_bytes,reserved;} win_tx_key147;
typedef struct {uint32_t name_bytes,value_bytes;} win_tx_property147;
_Static_assert(sizeof(win_tx_header147)==1024,"Stable transaction header");
_Static_assert(sizeof(win_tx_file147)==304,"Stable owned-file record");
static inline unsigned win_tx_length147(const char*s,unsigned cap){unsigned n=0;while(n<cap&&s[n])++n;return n;}
static inline int win_tx_zero147(const void*p,unsigned n){const uint8_t*s=p;for(unsigned i=0;i<n;++i)if(s[i])return 0;return 1;}
static inline int win_tx_text147(const char*s,unsigned cap,unsigned empty){unsigned n=win_tx_length147(s,cap);if(n==cap||(!empty&&!n))return 0;for(unsigned i=0;i<n;++i)if((uint8_t)s[i]<32)return 0;return 1;}
/* Selected native payload names remain ASCII, with the filesystem's 63-byte leaves. */
static inline int win_tx_relative147(const char*s,unsigned separator){
 unsigned n=win_tx_length147(s,256),leaf=0,begin=0;if(!n||n==256)return 0;
 for(unsigned i=0;i<=n;++i){unsigned c=(uint8_t)s[i];if(!c||c==separator){
   if(!leaf||leaf>63||(leaf==1&&s[begin]=='.')||(leaf==2&&s[begin]=='.'&&s[begin+1]=='.'))return 0;
   if(s[i-1]=='.'||s[i-1]==' ')return 0;leaf=0;begin=i+1;
  }else{if(c<32||c>=127||c=='/'||c=='\\'||c==':'||c=='*'||c=='?'||c=='"'||c=='<'||c=='>'||c=='|')return 0;++leaf;}}
 return 1;
}
static inline int win_tx_alias147(const char*s){
 const char*a="C:\\Program Files\\",*b="C:\\Program Files (x86)\\";unsigned an=17,bn=23;
 if(!s)return 0;unsigned n=win_tx_length147(s,256);if(n==256)return 0;
 if(n>an&&!memcmp(s,a,an))return win_tx_relative147(s+an,'\\');
 if(n>bn&&!memcmp(s,b,bn))return win_tx_relative147(s+bn,'\\');return 0;
}
static inline int win_tx_header_shape147(const win_tx_header147*h,unsigned bytes){
 if(!h||bytes<sizeof(*h)||bytes>WIN_TX_LIMIT147||h->magic!=WIN_TX_MAGIC147||h->schema!=1||h->bytes!=bytes||h->records>1024||h->files>258||h->registry>128||h->links>32||h->keys>128||h->properties>256||h->records!=h->files+h->registry+h->links+h->keys+h->properties)return 0;
 if(!win_product_guid147(h->code,1)||!win_tx_alias147(h->alias)||!win_tx_text147(h->user,256,0)||!win_tx_text147(h->product,96,0)||!win_tx_text147(h->version,32,0)||!win_tx_text147(h->publisher,96,0)||!win_tx_zero147(h->reserved,sizeof(h->reserved))||win_tx_zero147(h->source_sha,32))return 0;
 if(h->upgrade[0]&&!win_product_guid147(h->upgrade,1))return 0;
 return !memcmp(h->user,"/Users/",7)&&win_tx_relative147(h->user+7,'/');
}
static inline int win_tx_digest147(const void*data,unsigned bytes,uint8_t out[32]){
 if(!data||bytes<104||bytes>WIN_TX_LIMIT147||!out)return 0;engine_sha256_context c;uint8_t zero[32]={0};const uint8_t*p=data;engine_sha256_init(&c);
 return engine_sha256_update(&c,p,72)&&engine_sha256_update(&c,zero,32)&&engine_sha256_update(&c,p+104,bytes-104)&&engine_sha256_final(&c,out);
}
static inline int win_tx_bound147(const win_tx_header147*h,const char*root,const char*user,const uint8_t*source){
 char expected[256];if(!h||!root||!user||!win_product_make147(expected,sizeof(expected),h->code))return 0;
 unsigned n=win_tx_length147(root,256),u=win_tx_length147(user,256);if(n==256||u==256)return 0;
 return win_tx_length147(expected,256)==n&&!memcmp(expected,root,n+1)&&win_tx_length147(h->user,256)==u&&!memcmp(h->user,user,u+1)&&(!source||!memcmp(h->source_sha,source,32));
}
static inline int win_tx_reg_path147(const char*s,unsigned bytes,unsigned empty){
 if(!bytes||bytes>256||s[bytes-1]||win_tx_length147(s,bytes)!=bytes-1||(!empty&&bytes==1))return 0;
 for(unsigned i=0;i+1<bytes;++i)if((uint8_t)s[i]<32||s[i]=='/'||(s[i]=='\\'&&(!i||i+2==bytes||s[i-1]=='\\')))return 0;return 1;
}
static inline int win_tx_equal147(const char*a,const char*b){
 unsigned i=0;for(;a[i]&&b[i];++i){unsigned x=(uint8_t)a[i],y=(uint8_t)b[i];if(x>='A'&&x<='Z')x+=32;if(y>='A'&&y<='Z')y+=32;if(x!=y)return 0;}return a[i]==b[i];
}
static inline int win_tx_typed147(unsigned type,const uint8_t*p,unsigned n){
 if(type==3)return 1;if(type==4)return n==4;
 if(type!=1&&type!=2&&type!=7)return 0;
 if(n<2||(n&1)||p[n-1]||p[n-2])return 0;
 return type!=7||(n>=4&&!p[n-3]&&!p[n-4]);
}
static inline int win_tx_validate147(const void*data,unsigned bytes){
 if(!data||bytes<sizeof(win_tx_header147))return 0;const win_tx_header147*h=data;if(!win_tx_header_shape147(h,bytes))return 0;
 uint8_t digest[32];if(!win_tx_digest147(data,bytes,digest)||memcmp(digest,h->checksum,32))return 0;
 unsigned counts[6]={0},at=sizeof(*h);const uint8_t*p=data;
 for(unsigned i=0;i<h->records;++i){if(at>bytes||bytes-at<8)return 0;const win_tx_record147*r=(const void*)(p+at);if(r->type<1||r->type>5||r->bytes<8||(r->bytes&7)||r->bytes>bytes-at)return 0;const uint8_t*value=p+at+8;unsigned size=r->bytes-8,used=0;
  if(r->type==WIN_TX_FILE147||r->type==WIN_TX_LINK147){if(size!=sizeof(win_tx_file147))return 0;const win_tx_file147*f=(const void*)value;if(!win_tx_relative147(f->path,'/')||f->reserved||f->bytes>32u*1024u*1024u||win_tx_zero147(f->sha,32))return 0;
   if(r->type==WIN_TX_LINK147){if(f->flags>1)return 0;}else{
    if(f->flags!=WIN_TX_PAYLOAD147&&f->flags!=WIN_TX_GENERATED147&&f->flags!=WIN_TX_CACHE147)return 0;
    if(f->flags==WIN_TX_CACHE147){if(!win_tx_equal147(f->path,".EngacerMSI/source.msi")||f->bytes>8u*1024u*1024u||memcmp(f->sha,h->source_sha,32))return 0;}
    else{char first[256];unsigned n=0;while(f->path[n]&&f->path[n]!='/'){first[n]=f->path[n];++n;}first[n]=0;if(win_tx_equal147(first,".EngacerMSI")||win_tx_equal147(f->path,"product.bin"))return 0;}
   }
   for(unsigned previous=sizeof(*h);previous<at;){const win_tx_record147*q=(const void*)(p+previous);if(q->type==r->type){const win_tx_file147*g=(const void*)(p+previous+8);if(win_tx_equal147(f->path,g->path))return 0;}previous+=q->bytes;}used=size;
  }else if(r->type==WIN_TX_REG147){if(size<sizeof(win_tx_reg147))return 0;const win_tx_reg147*v=(const void*)value;
   if((v->root!=1&&v->root!=2)||(v->view!=32&&v->view!=64)||v->reserved||v->before_exists>1||v->after_bytes>2048||v->before_bytes>2048||(!v->before_exists&&(v->before_bytes||v->before_type))||v->key_bytes>256||v->name_bytes>256)return 0;
   if(v->after_type!=1&&v->after_type!=2&&v->after_type!=3&&v->after_type!=4&&v->after_type!=7)return 0;
   used=sizeof(*v)+v->key_bytes+v->name_bytes+v->after_bytes+v->before_bytes;if(used>size||!win_tx_reg_path147((const char*)value+sizeof(*v),v->key_bytes,0)||!win_tx_reg_path147((const char*)value+sizeof(*v)+v->key_bytes,v->name_bytes,1))return 0;
   const uint8_t*after=value+sizeof(*v)+v->key_bytes+v->name_bytes;
   if(!win_tx_typed147(v->after_type,after,v->after_bytes)||(v->before_exists&&!win_tx_typed147(v->before_type,after+v->after_bytes,v->before_bytes)))return 0;
   for(unsigned previous=sizeof(*h);previous<at;){const win_tx_record147*q=(const void*)(p+previous);if(q->type==r->type){const win_tx_reg147*g=(const void*)(p+previous+8);const char*a=(const char*)(v+1),*b=(const char*)(g+1);if(v->root==g->root&&v->view==g->view&&win_tx_equal147(a,b)&&win_tx_equal147(a+v->key_bytes,b+g->key_bytes))return 0;}previous+=q->bytes;}
  }else if(r->type==WIN_TX_KEY147){if(size<sizeof(win_tx_key147))return 0;const win_tx_key147*k=(const void*)value;if((k->root!=1&&k->root!=2)||(k->view!=32&&k->view!=64)||k->reserved||k->key_bytes>256)return 0;used=sizeof(*k)+k->key_bytes;if(used>size||!win_tx_reg_path147((const char*)value+sizeof(*k),k->key_bytes,0))return 0;
  }else{if(size<sizeof(win_tx_property147))return 0;const win_tx_property147*v=(const void*)value;used=sizeof(*v)+v->name_bytes+v->value_bytes;if(v->name_bytes<2||v->name_bytes>73||!v->value_bytes||v->value_bytes>4097||used>size)return 0;const char*name=(const char*)value+sizeof(*v),*text=name+v->name_bytes;if(name[v->name_bytes-1]||text[v->value_bytes-1]||win_tx_length147(name,v->name_bytes)!=v->name_bytes-1||win_tx_length147(text,v->value_bytes)!=v->value_bytes-1)return 0;
   for(unsigned j=0;j+1<v->name_bytes;++j){unsigned c=(uint8_t)name[j];if(!((c>='A'&&c<='Z')||(c>='a'&&c<='z')||c=='_'||(j&&((c>='0'&&c<='9')||c=='.'))))return 0;}
   for(unsigned previous=sizeof(*h);previous<at;){const win_tx_record147*q=(const void*)(p+previous);if(q->type==r->type){const win_tx_property147*g=(const void*)(p+previous+8);if(g->name_bytes==v->name_bytes&&!memcmp(g+1,name,v->name_bytes))return 0;}previous+=q->bytes;}
  }
  if(!win_tx_zero147(value+used,size-used))return 0;++counts[r->type];at+=r->bytes;
 }
 return at==bytes&&counts[1]==h->files&&counts[2]==h->registry&&counts[3]==h->links&&counts[4]==h->keys&&counts[5]==h->properties;
}
#endif
