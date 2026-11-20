/* Bounded MSI condition profile. No allocation, host service or hidden state.
 * Lookup returns a NUL-terminated UTF-8 value, at most 4096 bytes. Missing is "".
 * Prefixes: property=0, environment='%', component='$'/'?', feature='&'/'!'.
 * ASCII insensitive/ordered comparisons only; unsupported comparisons fail.
 */
#ifndef ENGINE_MSI_CONDITION147_H
#define ENGINE_MSI_CONDITION147_H
#include <stdint.h>
#include <stddef.h>
typedef const char *(*msic_lookup147)(void *,unsigned,const char *);
enum {MSIC_FALSE147=0,MSIC_TRUE147=1,MSIC_NONE147=2,MSIC_ERROR147=3};
enum {MC_END147=0,MC_VALUE147=256,MC_AND147,MC_OR147,MC_XOR147,MC_EQV147,MC_IMP147,MC_NOT147};
typedef struct {const char *s;unsigned n;int number;int32_t integer;} msic_value147;
typedef struct {const char *text;unsigned at,length,steps,depth,error,token;msic_value147 value;msic_lookup147 lookup;void *context;} msic_parser147;
static unsigned msic_fold147(unsigned c){return c>='a'&&c<='z'?c-32:c;}
static int msic_word147(const char *s,unsigned n,const char *word){unsigned i=0;while(word[i]){if(i==n||msic_fold147((unsigned char)s[i])!=(unsigned char)word[i])return 0;++i;}return i==n;}
static int msic_integer147(const char *s,unsigned n,int32_t *out){
 unsigned i=0,negative=0;uint64_t value=0;if(!n)return 0;
 if(s[i]=='-'||s[i]=='+'){negative=s[i]=='-';if(++i==n)return 0;}
 for(;i<n;++i){unsigned c=(unsigned char)s[i];if(c<'0'||c>'9')return 0;value=value*10+c-'0';if(value>(negative?UINT64_C(2147483648):UINT64_C(2147483647)))return 0;}
 *out=negative?(int32_t)-(int64_t)value:(int32_t)value;return 1;
}
static int msic_name147(unsigned c){return (c>='A'&&c<='Z')||(c>='a'&&c<='z')||c=='_'||(c>='0'&&c<='9')||c=='.';}
static void msic_next147(msic_parser147 *p){
 if(p->error||++p->steps>2048){p->error=1;p->token=MC_END147;return;}
 while(p->at<p->length&&(p->text[p->at]==' '||p->text[p->at]=='\t'||p->text[p->at]=='\r'||p->text[p->at]=='\n'))++p->at;
 if(p->at==p->length){p->token=MC_END147;return;}
 unsigned start=p->at,c=(unsigned char)p->text[p->at++];p->token=c;
 if(c=='('||c==')'||c=='='||c=='<'||c=='>'||c=='~')return;
 if(c=='"'){
  start=p->at;while(p->at<p->length&&p->text[p->at]!='"')++p->at;
  if(p->at==p->length){p->error=1;return;}p->value=(msic_value147){p->text+start,p->at-start,0,0};++p->at;p->token=MC_VALUE147;return;
 }
 if((c>='0'&&c<='9')||c=='-'||c=='+'){
  while(p->at<p->length&&p->text[p->at]>='0'&&p->text[p->at]<='9')++p->at;
  p->value=(msic_value147){p->text+start,p->at-start,1,0};if(!msic_integer147(p->value.s,p->value.n,&p->value.integer))p->error=1;p->token=MC_VALUE147;return;
 }
 unsigned prefix=0;if(c=='%'||c=='$'||c=='?'||c=='&'||c=='!'){prefix=c;start=p->at;if(start==p->length){p->error=1;return;}c=(unsigned char)p->text[p->at++];}
 if(!msic_name147(c)||(c>='0'&&c<='9')||c=='.'){p->error=1;return;}
 while(p->at<p->length&&msic_name147((unsigned char)p->text[p->at]))++p->at;
 unsigned n=p->at-start;if(n>72){p->error=1;return;}
 if(!prefix){
  static const char *const words[]={"AND","OR","XOR","EQV","IMP","NOT"};
  for(unsigned i=0;i<6;++i)if(msic_word147(p->text+start,n,words[i])){p->token=MC_AND147+i;return;}
 }
 char name[73];for(unsigned i=0;i<n;++i)name[i]=p->text[start+i];name[n]=0;
 const char *s=p->lookup?p->lookup(p->context,prefix,name):"";if(!s)s="";n=0;while(n<=4096&&s[n])++n;if(n>4096){p->error=1;return;}
 p->value=(msic_value147){s,n,prefix&&prefix!='%',0};if(p->value.number&&!msic_integer147(s,n,&p->value.integer))p->error=1;p->token=MC_VALUE147;
}
static int msic_ascii147(msic_value147 v){for(unsigned i=0;i<v.n;++i)if((unsigned char)v.s[i]>=128)return 0;return 1;}
static int msic_equal_span147(const char *a,const char *b,unsigned n,unsigned fold){for(unsigned i=0;i<n;++i){unsigned x=(unsigned char)a[i],y=(unsigned char)b[i];if(fold){x=msic_fold147(x);y=msic_fold147(y);}if(x!=y)return 0;}return 1;}
/* Operators are encoded as their one/two ASCII characters in little endian. */
static int msic_compare147(msic_parser147 *p,msic_value147 a,msic_value147 b,unsigned op,unsigned fold){
 const unsigned ne='<'|('>'<<8),contains='>'|('<'<<8),prefix='<'|('<'<<8),suffix='>'|('>'<<8);
 if(!(op=='='||op==ne||op=='<'||op=='>'||op==('<'|('='<<8))||op==('>'|('='<<8))||op==contains||op==prefix||op==suffix)){p->error=1;return 0;}
 int comparison=0;
 if(a.number||b.number){
  int32_t x=a.integer,y=b.integer;
  if((!a.number&&!msic_integer147(a.s,a.n,&x))||(!b.number&&!msic_integer147(b.s,b.n,&y)))return op==ne;
  if(op==contains)return ((uint32_t)x&(uint32_t)y)!=0;
  if(op==prefix)return (int32_t)((uint32_t)x>>16)==y;
  if(op==suffix)return (int32_t)((uint32_t)x&65535)==y;
  comparison=x<y?-1:x>y?1:0;
 }else{
  unsigned ascii=msic_ascii147(a)&&msic_ascii147(b);
  if((fold||!(op=='='||op==ne||op==contains||op==prefix||op==suffix))&&!ascii){p->error=1;return 0;}
  if(op==contains){if(b.n>a.n)return 0;for(unsigned i=0;i<=a.n-b.n;++i)if(msic_equal_span147(a.s+i,b.s,b.n,fold))return 1;return 0;}
  if(op==prefix||op==suffix)return b.n<=a.n&&msic_equal_span147(a.s+(op==suffix?a.n-b.n:0),b.s,b.n,fold);
  unsigned n=a.n<b.n?a.n:b.n;for(unsigned i=0;i<n;++i){unsigned x=(unsigned char)a.s[i],y=(unsigned char)b.s[i];if(fold){x=msic_fold147(x);y=msic_fold147(y);}if(x!=y){comparison=x<y?-1:1;break;}}if(!comparison)comparison=a.n<b.n?-1:a.n>b.n?1:0;
 }
 if(op=='=')return comparison==0;if(op==ne)return comparison!=0;if(op=='<')return comparison<0;if(op=='>')return comparison>0;if(op==('<'|('='<<8)))return comparison<=0;if(op==('>'|('='<<8)))return comparison>=0;p->error=1;return 0;
}
static int msic_expression147(msic_parser147 *,unsigned);
static int msic_unary147(msic_parser147 *p){
 if(++p->depth>32){p->error=1;--p->depth;return 0;}int result=0;
 if(p->token==MC_NOT147){msic_next147(p);result=!msic_unary147(p);}
 else if(p->token=='('){msic_next147(p);result=msic_expression147(p,1);if(p->token!=')')p->error=1;else msic_next147(p);}
 else if(p->token==MC_VALUE147){
  msic_value147 a=p->value;msic_next147(p);unsigned fold=0,op=0;
  if(p->token=='~'){fold=1;msic_next147(p);}
  if(p->token=='='||p->token=='<'||p->token=='>'){
   op=p->token;unsigned end=p->at;msic_next147(p);
   if(p->at==end+1&&(p->token=='='||p->token=='<'||p->token=='>')){op|=p->token<<8;msic_next147(p);}
   if(p->token!=MC_VALUE147)p->error=1;else{msic_value147 b=p->value;msic_next147(p);result=msic_compare147(p,a,b,op,fold);}
  }else if(fold)p->error=1;else result=a.number?a.integer!=0:a.n!=0;
 }else p->error=1;
 --p->depth;return result;
}
static unsigned msic_precedence147(unsigned t){switch(t){case MC_AND147:return 6;case MC_OR147:return 5;case MC_XOR147:return 4;case MC_EQV147:return 3;case MC_IMP147:return 2;default:return 0;}}
static int msic_expression147(msic_parser147 *p,unsigned minimum){
 int left=msic_unary147(p);while(!p->error){unsigned op=p->token,precedence=msic_precedence147(op);if(!precedence||precedence<minimum)break;msic_next147(p);int right=msic_expression147(p,precedence+1);switch(op){case MC_AND147:left=left&&right;break;case MC_OR147:left=left||right;break;case MC_XOR147:left=left!=right;break;case MC_EQV147:left=left==right;break;case MC_IMP147:left=!left||right;break;}}return left;
}
static int msic_evaluate147(const char *text,msic_lookup147 lookup,void *context){
 if(!text)return MSIC_NONE147;msic_parser147 p={0};p.text=text;p.lookup=lookup;p.context=context;while(p.length<=4096&&text[p.length])++p.length;if(p.length>4096)return MSIC_ERROR147;msic_next147(&p);if(p.token==MC_END147)return p.error?MSIC_ERROR147:MSIC_NONE147;int value=msic_expression147(&p,1);return p.error||p.token!=MC_END147?MSIC_ERROR147:value?MSIC_TRUE147:MSIC_FALSE147;
}
#endif
