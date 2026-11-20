/* Owned production CAB/SHA probe. Original archive data is never executed. */
#include <stddef.h>
#include <stdint.h>
#include <engine/sha256.h>
#include "../../user/windows8/cab147.h"
__declspec(dllimport) uint64_t GlobalAlloc(unsigned,uint64_t);
__declspec(dllimport) uint64_t GlobalFree(uint64_t);
__declspec(dllimport) uint64_t CreateFileW(const uint16_t *,unsigned,unsigned,void *,unsigned,unsigned,uint64_t);
__declspec(dllimport) unsigned GetFileSize(uint64_t,unsigned *);
__declspec(dllimport) int ReadFile(uint64_t,void *,unsigned,unsigned *,void *);
__declspec(dllimport) int CloseHandle(uint64_t);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void *,unsigned,unsigned *,void *);
__declspec(dllimport) void ExitProcess(unsigned);
void *memcpy(void *d,const void *s,size_t n){uint8_t *a=d;const uint8_t *b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void *memset(void *d,int value,size_t n){uint8_t *a=d;for(size_t i=0;i<n;++i)a[i]=(uint8_t)value;return d;}
int memcmp(const void *a,const void *b,size_t n){const uint8_t *x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]-y[i];return 0;}
void *alloc8(size_t n){return (void *)(uintptr_t)GlobalAlloc(0,n);}
void free8(void *p){if(p&&GlobalFree((uint64_t)(uintptr_t)p))ExitProcess(91);}
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
static int same147(const char *a,const char *b){unsigned i=0;while(a[i]&&a[i]==b[i])++i;return a[i]==b[i];}
typedef struct {const char *name;unsigned size;uint8_t hash[32];} expected147;
#include "cab147_expected.h"
typedef struct {const expected147 *expected;unsigned count,done,current;uint8_t seen[256];engine_sha256_context hash;} sink147_state;
static int sink147(void *opaque,const cab147_file *file,unsigned offset,const void *data,unsigned n){
 sink147_state *state=opaque;unsigned index=0;while(index<state->count&&!same147(file->name,state->expected[index].name))++index;
 if(index==state->count||file->size!=state->expected[index].size||state->seen[index])return 1;
 if(!offset){if(state->current)return 1;state->current=index+1;engine_sha256_init(&state->hash);}else if(state->current!=index+1)return 1;
 if(!engine_sha256_update(&state->hash,data,n))return 1;
 if(offset+n==file->size){uint8_t hash[32];if(!engine_sha256_final(&state->hash,hash)||memcmp(hash,state->expected[index].hash,32))return 1;state->seen[index]=1;state->current=0;++state->done;}return 0;
}
void entry(void);void *volatile anchor147=&entry;
void entry(void){
 for(unsigned item=0;item<2;++item){
  uint16_t path[96];static const char prefix[]="C:\\Users\\Owner\\Documents\\m147-cab-0.bin";unsigned i=0;for(;prefix[i];++i)path[i]=(uint8_t)prefix[i];path[i]=0;for(unsigned at=0;at<i;++at)if(path[at]=='0')path[at]=(uint16_t)('0'+item);
  uint64_t h=CreateFileW(path,0x80000000u,1,0,3,0,0);check147(h!=UINT64_MAX,10);unsigned high=0,size=GetFileSize(h,&high);check147(!high&&size==cab147_sizes[item],11);uint8_t *source=alloc8(size);check147(source!=0,12);unsigned got=0;check147(ReadFile(h,source,size,&got,0)&&got==size&&CloseHandle(h),13);
  uint8_t hash[32];engine_sha256(source,size,hash);check147(!memcmp(hash,cab147_hashes[item],32),14);
  cab147_archive *archive=0;check147(cab147_open((msi8_blob){source,size},&archive)==0,15);check147(archive->count==cab147_counts[item],16);
  sink147_state state={.expected=item?cab147_items1:cab147_items0,.count=cab147_counts[item]};check147(cab147_walk(archive,sink147,&state)==0&&state.done==state.count&&!state.current,17);cab147_close(archive);free8(source);
 }
 static const char message[]="M147_ORIGINAL_CAB_STREAM_ALL_323_SHA256_PASS\r\n";unsigned wrote=0;check147(WriteFile(GetStdHandle((unsigned)-11),message,sizeof(message)-1,&wrote,0)&&wrote==sizeof(message)-1,18);ExitProcess(0);
}
