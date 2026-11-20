/* Host-only adapter. Original database bytes are parsed, never executed. */
#include "../../user/windows8/msi-plan147.h"
typedef void *(*allocator147)(void *,size_t);
typedef void (*releaser147)(void *,void *);
typedef void (*failure147)(const char *);
static allocator147 allocate_host147;
static releaser147 release_host147;
static failure147 fail_host147;
static msia_plan147 *plan147;
void *memcpy(void *d,const void *s,size_t n){uint8_t *a=d;const uint8_t *b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void *memset(void *d,int value,size_t n){uint8_t *a=d;for(size_t i=0;i<n;++i)a[i]=(uint8_t)value;return d;}
int memcmp(const void *a,const void *b,size_t n){const uint8_t *x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]-y[i];return 0;}
void *alloc8(size_t n){return allocate_host147?allocate_host147(0,n):0;}
void free8(void *p){if(p&&release_host147)release_host147(0,p);}
void *calloc8(size_t count,size_t size){if(size&&count>SIZE_MAX/size)return 0;void *p=alloc8(count*size);if(p)memset(p,0,count*size);return p;}
NORETURN void fail8(const char *message){fail_host147(message);__builtin_trap();}
unsigned len8(const char *s){unsigned n=0;while(s[n])++n;return n;}
int equal8(const char *a,const char *b){unsigned i=0;while(a[i]&&a[i]==b[i])++i;return a[i]==b[i];}
void copy8(char *out,const char *in,unsigned capacity){unsigned i=0;while(i+1<capacity&&in[i]){out[i]=in[i];++i;}if(capacity)out[i]=0;}
void append8(char *out,const char *in,unsigned capacity){unsigned at=len8(out);if(at<capacity)copy8(out+at,in,capacity-at);}
__declspec(dllexport) void init147(allocator147 allocate,releaser147 release,failure147 failure){allocate_host147=allocate;release_host147=release;fail_host147=failure;}
__declspec(dllexport) unsigned open147(const void *data,unsigned bytes){plan147=msia_prepare147(data,bytes);return plan147->action_count;}
__declspec(dllexport) const msia_action147 *action147(unsigned index){return plan147&&index<plan147->action_count?plan147->actions+index:0;}
__declspec(dllexport) const char *get147(const char *name){return msip_get147(&plan147->properties,name);}
__declspec(dllexport) unsigned set147(const char *name,const char *value){return msip_set147(&plan147->properties,name,value);}
__declspec(dllexport) unsigned property147(unsigned index){return msia_property_action147(plan147,index);}
__declspec(dllexport) int condition147(const char *text){return msia_condition147(plan147,text);}
__declspec(dllexport) void close147(void){msia_close147(plan147);plan147=0;}
