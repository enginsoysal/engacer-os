/* Production condition parser through a host-only checked lookup adapter. */
#include <stddef.h>
#include <stdint.h>
void *memset(void *out,int value,size_t n){unsigned char *p=out;for(size_t i=0;i<n;++i)p[i]=(unsigned char)value;return out;}
void *memcpy(void *out,const void *in,size_t n){unsigned char *p=out;const unsigned char *s=in;for(size_t i=0;i<n;++i)p[i]=s[i];return out;}
#include "../../user/windows8/msi-condition147.h"
typedef struct {const char *name,*value;unsigned prefix;} pair147;
typedef struct {const pair147 *pairs;unsigned count;} table147;
static const char *lookup147(void *opaque,unsigned prefix,const char *name){
 table147 *table=opaque;for(unsigned i=0;i<table->count;++i){const pair147 *p=table->pairs+i;if(!p->name||!p->value||p->prefix!=prefix)continue;unsigned j=0;while(name[j]&&p->name[j]&&(prefix=='%'?msic_fold147((unsigned char)name[j])==msic_fold147((unsigned char)p->name[j]):name[j]==p->name[j]))++j;if(!name[j]&&!p->name[j])return p->value;}return "";
}
__declspec(dllexport) int evaluate147(const char *text,const pair147 *pairs,unsigned count){if(count>256||(!pairs&&count))return MSIC_ERROR147;table147 table={pairs,count};return msic_evaluate147(text,lookup147,&table);}
