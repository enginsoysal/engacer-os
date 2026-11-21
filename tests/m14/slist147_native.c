/* Native independent inline producers race the production atomic-flush API. */
#include <stdint.h>
#include <stddef.h>
__declspec(dllimport) void InitializeSListHead(void*);
__declspec(dllimport) void*InterlockedFlushSList(void*);
__declspec(dllimport) int IsProcessorFeaturePresent(unsigned);
__declspec(dllimport) uint64_t CreateThread(void*,size_t,void*,void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const uint64_t*,int,unsigned);
__declspec(dllimport) unsigned WaitForSingleObject(uint64_t,unsigned);
__declspec(dllimport) uint64_t CreateEventW(void*,int,int,const uint16_t*);
__declspec(dllimport) int SetEvent(uint64_t);
__declspec(dllimport) int GetExitCodeThread(uint64_t,unsigned*);
__declspec(dllimport) int CloseHandle(uint64_t);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
typedef struct {uint64_t low,high;} head147;
typedef struct {uint64_t next,id;} node147;
static _Alignas(16) head147 list147;
static _Alignas(16) node147 nodes147[256];
static unsigned char seen147[256];
static uint64_t start147,notify147;
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
static unsigned producer147(void*opaque){
 unsigned worker=(unsigned)(uintptr_t)opaque;check147(WaitForSingleObject(start147,5000)==0,10);
 for(unsigned i=0;i<64;++i){
  node147*node=nodes147+worker*64+i;node->id=worker*64+i;
  uint64_t old_low=__atomic_load_n(&list147.low,__ATOMIC_ACQUIRE),old_high=__atomic_load_n(&list147.high,__ATOMIC_ACQUIRE);
  for(;;){
   node->next=old_high&~UINT64_C(15);uint64_t next_low=((old_low+65536)&~UINT64_C(65535))|((old_low+1)&65535),next_high=(uint64_t)(uintptr_t)node|(old_high&15);unsigned char ok;
   __asm__ volatile("lock cmpxchg16b %1; sete %0":"=qm"(ok),"+m"(list147),"+a"(old_low),"+d"(old_high):"b"(next_low),"c"(next_high):"cc","memory");if(ok)break;
  }
  if(i%8==7)check147(SetEvent(notify147),11);
 }
 return 0;
}
void entry(void);void*volatile anchor147=&entry;
void entry(void){
 uint32_t a,b,c,d;__asm__ volatile("cpuid":"=a"(a),"=b"(b),"=c"(c),"=d"(d):"a"(1u),"c"(0));
 check147(IsProcessorFeaturePresent(6)==!!(d&(1u<<25))&&IsProcessorFeaturePresent(10)==!!(d&(1u<<26)),20);
 check147(IsProcessorFeaturePresent(13)==!!(c&1)&&IsProcessorFeaturePresent(14)==!!(c&(1u<<13))&&(c&(1u<<13)),21);
 check147(!IsProcessorFeaturePresent(17)&&!IsProcessorFeaturePresent(23)&&!IsProcessorFeaturePresent(39)&&!IsProcessorFeaturePresent(40)&&!IsProcessorFeaturePresent(41)&&!IsProcessorFeaturePresent(UINT32_MAX),22);
 InitializeSListHead(&list147);check147(!list147.low&&!list147.high&&!InterlockedFlushSList(&list147),23);
 start147=CreateEventW(0,1,0,0);notify147=CreateEventW(0,0,0,0);check147(start147&&notify147,24);uint64_t threads[4];
 for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,producer147,(void*)(uintptr_t)i,0,0);check147(threads[i]!=0,25);}check147(SetEvent(start147),26);
 unsigned count=0;while(count<256){
  check147(WaitForSingleObject(notify147,5000)==0,27);node147*node=InterlockedFlushSList(&list147);
  while(node){uintptr_t at=(uintptr_t)node,base=(uintptr_t)nodes147;check147(at>=base&&at<base+sizeof(nodes147)&&!((at-base)&15),28);unsigned index=(unsigned)((at-base)/16);check147(node->id==index&&!seen147[index],29);seen147[index]=1;check147(++count<=256,30);node=(void*)(uintptr_t)node->next;}
 }
 check147(WaitForMultipleObjects(4,threads,1,5000)==0,31);for(unsigned i=0;i<4;++i){unsigned code=99;check147(GetExitCodeThread(threads[i],&code)&&!code&&CloseHandle(threads[i]),32);}check147(!(list147.low&65535)&&!InterlockedFlushSList(&list147)&&CloseHandle(start147)&&CloseHandle(notify147),33);
 static const char text[]="M147_NATIVE_SLIST_ATOMIC_PRODUCERS_CPU_POLICY_PASS\n";unsigned n=0;check147(WriteFile(GetStdHandle((unsigned)-11),text,sizeof(text)-1,&n,0)&&n==sizeof(text)-1,40);ExitProcess(0);
}
