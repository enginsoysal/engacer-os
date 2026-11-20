/* Host-only allocation/sink adapter; all CAB validation/decoding is production. */
#include <stddef.h>
#include <stdint.h>
#include "../../user/windows8/cab147.h"
typedef void *(*allocator147)(void *,size_t);
typedef void (*releaser147)(void *,void *);
static allocator147 allocate_host147;
static releaser147 release_host147;
static cab147_archive *archive147;
void *memcpy(void *d,const void *s,size_t n){uint8_t *a=d;const uint8_t *b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void *memset(void *d,int value,size_t n){uint8_t *a=d;for(size_t i=0;i<n;++i)a[i]=(uint8_t)value;return d;}
int memcmp(const void *a,const void *b,size_t n){const uint8_t *x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]-y[i];return 0;}
void *alloc8(size_t n){return allocate_host147?allocate_host147(0,n):0;}
void free8(void *p){if(p&&release_host147)release_host147(0,p);}
__declspec(dllexport) void init147(allocator147 allocate,releaser147 release){cab147_close(archive147);archive147=0;allocate_host147=allocate;release_host147=release;}
__declspec(dllexport) unsigned open147(void *data,unsigned size){cab147_close(archive147);archive147=0;return cab147_open((msi8_blob){data,size},&archive147);}
__declspec(dllexport) unsigned walk147(cab147_sink sink,void *context){return cab147_walk(archive147,sink,context);}
__declspec(dllexport) void close147(void){cab147_close(archive147);archive147=0;}
__declspec(dllexport) unsigned count147(void){return archive147?archive147->count:0;}
__declspec(dllexport) unsigned bytes147(void){return archive147?archive147->bytes:0;}
__declspec(dllexport) const cab147_file *file147(unsigned i){return archive147&&i<archive147->count?archive147->files+i:0;}
