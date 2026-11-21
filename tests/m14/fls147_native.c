/* Own native FLS lifecycle caller. No original program executes on the host. */
#include <stdint.h>
#include <stddef.h>
__declspec(dllimport) unsigned FlsAlloc(void*);
__declspec(dllimport) int FlsFree(unsigned);
__declspec(dllimport) void*FlsGetValue(unsigned);
__declspec(dllimport) int FlsSetValue(unsigned,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void SetLastError(unsigned);
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
static unsigned index147,mode147,count147,bits147;
static uint64_t ready147[4],release147;
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
static void callback147(void*opaque){
 unsigned value=(unsigned)(uintptr_t)opaque;
 unsigned temporary=FlsAlloc(0);check147(temporary!=UINT32_MAX&&FlsFree(temporary),11);
 if(mode147==3){check147(value==99,12);static const char text[]="M147_NATIVE_FLS_THREADS_FREE_CALLBACKS_MAIN_EXIT_PASS\n";unsigned n=0;check147(WriteFile(GetStdHandle((unsigned)-11),text,sizeof(text)-1,&n,0)&&n==sizeof(text)-1,13);return;}
 check147(value>=1&&value<=5,14);__atomic_fetch_add(&count147,1,__ATOMIC_SEQ_CST);__atomic_fetch_or(&bits147,1u<<value,__ATOMIC_SEQ_CST);
}
static unsigned worker147(void*opaque){
 unsigned value=(unsigned)(uintptr_t)opaque;check147(!FlsGetValue(index147)&&GetLastError()==0,20);check147(FlsSetValue(index147,opaque)&&FlsGetValue(index147)==opaque,21);
 if(mode147==2){check147(SetEvent(ready147[value-1]),22);check147(WaitForSingleObject(release147,5000)==0,23);check147(!FlsGetValue(index147)&&GetLastError()==87,24);}
 return 0;
}
void entry(void);void*volatile anchor147=&entry;
void entry(void){
 unsigned indices[64];for(unsigned i=0;i<64;++i){indices[i]=FlsAlloc(0);check147(indices[i]!=UINT32_MAX,30);}check147(FlsAlloc(0)==UINT32_MAX,31);for(unsigned i=0;i<64;++i)check147(FlsFree(indices[i]),32);
 check147(!FlsFree(0)&&GetLastError()==87,33);check147(!FlsSetValue(UINT32_MAX,(void*)1)&&GetLastError()==87,34);
 for(mode147=1;mode147<=2;++mode147){
  count147=bits147=0;index147=FlsAlloc(callback147);check147(index147!=UINT32_MAX&&FlsSetValue(index147,(void*)5),35);
  if(mode147==2){release147=CreateEventW(0,1,0,0);check147(release147!=0,36);for(unsigned i=0;i<4;++i){ready147[i]=CreateEventW(0,1,0,0);check147(ready147[i]!=0,37);}}
  uint64_t threads[4];for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,worker147,(void*)(uintptr_t)(i+1),0,0);check147(threads[i]!=0,38);}
  if(mode147==2){check147(WaitForMultipleObjects(4,ready147,1,5000)==0,39);check147(FlsFree(index147)&&count147==5&&bits147==62,40);check147(SetEvent(release147),41);}
  check147(WaitForMultipleObjects(4,threads,1,5000)==0,42);
  for(unsigned i=0;i<4;++i){unsigned code=99;check147(GetExitCodeThread(threads[i],&code)&&code==0&&CloseHandle(threads[i]),43);}
  if(mode147==1){check147(count147==4&&bits147==30&&(uintptr_t)FlsGetValue(index147)==5,44);check147(FlsFree(index147)&&count147==5&&bits147==62,45);}
  else{for(unsigned i=0;i<4;++i)check147(CloseHandle(ready147[i]),46);check147(CloseHandle(release147),47);}
 }
 mode147=3;index147=FlsAlloc(callback147);check147(index147!=UINT32_MAX,48);SetLastError(999);check147(!FlsGetValue(index147)&&GetLastError()==0,49);check147(FlsSetValue(index147,(void*)99),50);ExitProcess(0);
}
