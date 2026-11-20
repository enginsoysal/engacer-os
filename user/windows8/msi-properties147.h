/* Lazy, privately owned MSI properties. Caller owns the session lifetime. */
#ifndef ENGINE_MSI_PROPERTIES147_H
#define ENGINE_MSI_PROPERTIES147_H
#include <stddef.h>
#include <stdint.h>
typedef void *(*msip_alloc147)(void *,size_t);
typedef void (*msip_free147)(void *,void *);
typedef struct {char *block,*value;unsigned bytes;} msip_item147;
typedef struct {msip_item147 *items;unsigned count,capacity,bytes;msip_alloc147 alloc;msip_free147 release;void *context;} msip_session147;
enum {MSIP_OK147=0,MSIP_MEMORY147=8,MSIP_PARAMETER147=87,MSIP_QUOTA147=1816};
#define MSIP_BUDGET147 131072u
static int msip_name147(const char *name,unsigned *length){
 if(!name)return 0;unsigned n=0;for(;name[n]&&n<=72;++n){unsigned c=(unsigned char)name[n];if(!((c>='A'&&c<='Z')||(c>='a'&&c<='z')||c=='_'||(n&&((c>='0'&&c<='9')||c=='.'))))return 0;}*length=n;return n&&n<=72;
}
static int msip_same147(const char *a,const char *b){unsigned i=0;while(a[i]&&a[i]==b[i])++i;return a[i]==b[i];}
static const char *msip_get147(const msip_session147 *s,const char *name){if(!s||!name)return "";for(unsigned i=0;i<s->count;++i)if(msip_same147(s->items[i].block,name))return s->items[i].value;return "";}
static unsigned msip_set147(msip_session147 *s,const char *name,const char *value){
 unsigned names=0,values=0;if(!s||!s->alloc||!s->release||!msip_name147(name,&names))return MSIP_PARAMETER147;
 if(value){while(values<=4096&&value[values])++values;if(values>4096)return MSIP_QUOTA147;}
 unsigned at=0;while(at<s->count&&!msip_same147(s->items[at].block,name))++at;
 if(!values){if(at<s->count){s->bytes-=s->items[at].bytes;s->release(s->context,s->items[at].block);--s->count;s->items[at]=s->items[s->count];}return MSIP_OK147;}
 if(at==s->count&&s->count==256)return MSIP_QUOTA147;
 unsigned bytes=names+values+2;if(bytes>MSIP_BUDGET147-s->bytes)return MSIP_QUOTA147;
 char *block=s->alloc(s->context,bytes);if(!block)return MSIP_MEMORY147;
 for(unsigned i=0;i<=names;++i)block[i]=name[i];for(unsigned i=0;i<=values;++i)block[names+1+i]=value[i];
 if(at==s->count&&s->count==s->capacity){
  unsigned cap=s->capacity?s->capacity*2:16,new_bytes=cap*(unsigned)sizeof(msip_item147);
  if(new_bytes>MSIP_BUDGET147-s->bytes-bytes){s->release(s->context,block);return MSIP_QUOTA147;}
  msip_item147 *next=s->alloc(s->context,new_bytes);if(!next){s->release(s->context,block);return MSIP_MEMORY147;}
  for(unsigned i=0;i<s->count;++i)next[i]=s->items[i];if(s->items)s->release(s->context,s->items);s->bytes-=s->capacity*(unsigned)sizeof(msip_item147);s->items=next;s->capacity=cap;s->bytes+=new_bytes;
 }
 if(at<s->count){s->bytes-=s->items[at].bytes;s->release(s->context,s->items[at].block);}else ++s->count;
 s->items[at]=(msip_item147){block,block+names+1,bytes};s->bytes+=bytes;return MSIP_OK147;
}
static void msip_destroy147(msip_session147 *s){if(!s)return;if(s->release){for(unsigned i=0;i<s->count;++i)s->release(s->context,s->items[i].block);if(s->items)s->release(s->context,s->items);}s->items=0;s->count=s->capacity=s->bytes=0;}
/* Selected scalar Formatted fields. Unknown properties resolve to blank.
 * Non-property references use the caller's costed file/component/env resolver.
 * Nested keys and optional {...} groups deliberately refuse until implemented;
 * [~] needs a binary registry formatter and must never truncate a command.
 */
typedef const char *(*msip_resolve147)(void *,unsigned,const char *);
static unsigned msip_format_inner147(const msip_session147 *s,const char *text,char *out,unsigned capacity,msip_resolve147 resolve,void *context){
 if(!s||!text||!out||!capacity)return MSIP_PARAMETER147;unsigned length=0;while(length<=4096&&text[length])++length;if(length>4096)return MSIP_QUOTA147;
 unsigned used=0;out[0]=0;
 for(unsigned at=0;at<length;){
  if(text[at]=='{'||text[at]=='}'){unsigned end=at+1;while(end<length&&text[end]!='}')++end;if(text[at]=='{'&&end<length){for(unsigned i=at+1;i<end;++i)if(text[i]=='[')return MSIP_PARAMETER147;}}
  if(text[at]=='['){
   unsigned end=at+1;if(end<length&&text[end]=='\\'&&end+1<length)end+=2;while(end<length&&text[end]!=']')++end;
   if(end<length){
    const char *value="";char name[73],escaped[2]={0,0};unsigned first=at+1,prefix=0;
    if(first<end&&text[first]=='\\'){if(first+1<end){escaped[0]=text[first+1];value=escaped;}}
    else{
     if(first<end&&(text[first]=='%'||text[first]=='#'||text[first]=='$'||text[first]=='!'))prefix=(unsigned char)text[first++];
     unsigned n=end-first;if(n>72)return MSIP_QUOTA147;for(unsigned i=0;i<n;++i){if(text[first+i]=='['||text[first+i]=='~')return MSIP_PARAMETER147;name[i]=text[first+i];}name[n]=0;
     value=prefix?(resolve?resolve(context,prefix,name):0):msip_get147(s,name);if(prefix&&!resolve)return MSIP_PARAMETER147;if(!value)value="";
    }
    unsigned n=0;while(n<=4096&&value[n])++n;if(n>4096||n>=capacity-used)return MSIP_QUOTA147;for(unsigned i=0;i<n;++i)out[used++]=value[i];at=end+1;continue;
   }
  }
  if(used+1>=capacity)return MSIP_QUOTA147;out[used++]=text[at++];
 }
 out[used]=0;return MSIP_OK147;
}
static unsigned msip_format147(const msip_session147 *s,const char *text,char *out,unsigned capacity,msip_resolve147 resolve,void *context){unsigned result=msip_format_inner147(s,text,out,capacity,resolve,context);if(result&&out&&capacity)out[0]=0;return result;}
#endif
