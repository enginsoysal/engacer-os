/* Owned native callers; unchanged original installers are tested separately. */
#include <stdint.h>
#include <engine/windows8.h>
__declspec(dllimport) unsigned RegisterWindowMessageW(const uint16_t*);
__declspec(dllimport) unsigned short GlobalAddAtomW(const uint16_t*);
__declspec(dllimport) unsigned short GlobalDeleteAtom(unsigned short);
__declspec(dllimport) const uint16_t*GetCommandLineW(void);
__declspec(dllimport) unsigned GetModuleFileNameW(uint64_t,uint16_t*,unsigned);
__declspec(dllimport) int CreateProcessW(const uint16_t*,uint16_t*,void*,void*,int,unsigned,void*,const uint16_t*,void*,void*);
__declspec(dllimport) unsigned WaitForSingleObject(uint64_t,unsigned);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const uint64_t*,int,unsigned);
__declspec(dllimport) int GetExitCodeProcess(uint64_t,unsigned*);
__declspec(dllimport) uint64_t CreateThread(void*,uint64_t,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) int CloseHandle(uint64_t);
__declspec(dllimport) void InitializeSRWLock(uint64_t*);
__declspec(dllimport) void AcquireSRWLockExclusive(uint64_t*);
__declspec(dllimport) void AcquireSRWLockShared(uint64_t*);
__declspec(dllimport) void ReleaseSRWLockExclusive(uint64_t*);
__declspec(dllimport) void ReleaseSRWLockShared(uint64_t*);
__declspec(dllimport) uint8_t TryAcquireSRWLockExclusive(uint64_t*);
__declspec(dllimport) uint8_t TryAcquireSRWLockShared(uint64_t*);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) uint64_t LoadLibraryExA(const char*,uint64_t,unsigned);
__declspec(dllimport) uint64_t GetModuleHandleW(const uint16_t*);
__declspec(dllimport) int FreeLibrary(uint64_t);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void*GetProcAddress(uint64_t,const char*);
__declspec(dllimport) unsigned GetSystemDirectoryW(uint16_t*,unsigned);
__declspec(dllimport) uint64_t HeapCreate(unsigned,uint64_t,uint64_t);
__declspec(dllimport) int HeapDestroy(uint64_t);
__declspec(dllimport) void*HeapAlloc(uint64_t,unsigned,uint64_t);
__declspec(dllimport) int HeapFree(uint64_t,unsigned,void*);
__declspec(dllimport) uint64_t HeapSize(uint64_t,unsigned,const void*);
__declspec(dllimport) void*HeapReAlloc(uint64_t,unsigned,void*,uint64_t);
static void check(int ok,unsigned error){if(!ok)ExitProcess(error);}
static uint64_t lock,left,right;
void entry(void);void*volatile relocation_anchor148=&entry;
static uint64_t owned_pages148(void){uint64_t values[4];register uint64_t r8 __asm__("r8")=0;register uint64_t r10 __asm__("r10")=0;uint64_t result=W8_SYS_VMINFO;__asm__ volatile("int $0x80":"+a"(result):"D"((uint64_t)(uintptr_t)values),"S"(UINT64_C(0)),"d"(UINT64_C(0)),"r"(r10),"r"(r8):"memory","rcx","r11");check(!result,260);return values[1];}
static unsigned worker(void*kind){
 for(unsigned i=0;i<1000;++i){
  if((uintptr_t)kind<4){AcquireSRWLockExclusive(&lock);++left;right=left*3;ReleaseSRWLockExclusive(&lock);}
  else{AcquireSRWLockShared(&lock);check(right==left*3,241);ReleaseSRWLockShared(&lock);}
 }return 0;
}
void entry(void){
 const uint16_t*line=GetCommandLineW();unsigned child=0;
 for(unsigned i=0;line&&line[i];++i)if(line[i]==' '&&line[i+1]=='!'&&!line[i+2])child=1;
 if(child){check(RegisterWindowMessageW(L"Engacer.Message148.ChildFirst")>=0xc000,221);ExitProcess(RegisterWindowMessageW(L"Engacer.Message148.Parent"));}
 unsigned id=RegisterWindowMessageW(L"Engacer.Message148.Parent");check(id>=0xc000&&id<=0xffff,222);
 for(unsigned i=0;i<70000;++i)check(RegisterWindowMessageW(L"engacer.message148.parent")==id,223);
 uint16_t path[512],command[520];unsigned n=GetModuleFileNameW(0,path,512);check(n&&n<512,224);
 command[0]='"';for(unsigned i=0;i<n;++i)command[i+1]=path[i];command[n+1]='"';command[n+2]=' ';command[n+3]='!';command[n+4]=0;
 uint8_t startup[104]={0};*(unsigned*)startup=104;struct{uint64_t process,thread;unsigned pid,tid;} process={0};
 check(CreateProcessW(path,command,0,0,0,0,0,0,startup,&process),225);check(WaitForSingleObject(process.process,30000)==0,226);
 unsigned result=0;check(GetExitCodeProcess(process.process,&result)&&result==id,227);check(CloseHandle(process.thread)&&CloseHandle(process.process),228);
 unsigned other=RegisterWindowMessageW(L"Engacer.Message148.ChildFirst");check(other>=0xc000&&other!=id,229);
 uint64_t module=LoadLibraryExA("kernel32.dll",0,0);check(module&&module==GetModuleHandleW(L"kernel32.dll")&&FreeLibrary(module),238);
 check(!LoadLibraryExA(0,0,0)&&GetLastError()==87,239);
 check(!LoadLibraryExA("\xff",0,0)&&GetLastError()==1113,240);
 check(!LoadLibraryExA("kernel32.dll",1,0)&&GetLastError()==50,242);
 uint16_t system[260];check(GetSystemDirectoryW(system,260)==19,243);
 uint64_t shell=LoadLibraryExA("SHLWAPI.dll",0,0);int(*append)(uint16_t*,const uint16_t*)=GetProcAddress(shell,"PathAppendW");
 check(shell&&append&&append(system,L"own.dll"),244);const uint16_t expected[]=L"C:\\Windows\\System32\\own.dll";for(unsigned i=0;i<sizeof(expected)/2;++i)check(system[i]==expected[i],245);check(FreeLibrary(shell),246);
 unsigned short atom=GlobalAddAtomW(L"Engacer.Message148.Parent");check(atom>=0xc000&&!GlobalDeleteAtom(atom)&&RegisterWindowMessageW(L"Engacer.Message148.Parent")==id,230);
 InitializeSRWLock(&lock);check(TryAcquireSRWLockExclusive(&lock)&&!TryAcquireSRWLockExclusive(&lock)&&!TryAcquireSRWLockShared(&lock),231);ReleaseSRWLockExclusive(&lock);
 check(TryAcquireSRWLockShared(&lock)&&TryAcquireSRWLockShared(&lock)&&!TryAcquireSRWLockExclusive(&lock),232);ReleaseSRWLockShared(&lock);ReleaseSRWLockShared(&lock);
 uint64_t threads[8];for(unsigned i=0;i<8;++i){threads[i]=CreateThread(0,0,worker,(void*)(uintptr_t)i,0,0);check(threads[i]!=0,233);}
 check(WaitForMultipleObjects(8,threads,1,30000)==0,234);for(unsigned i=0;i<8;++i)check(CloseHandle(threads[i]),235);
 check(left==4000&&right==12000&&!lock,236);
 uint64_t warm=HeapCreate(0,0,0);check(warm&&HeapDestroy(warm),247);uint64_t pages=owned_pages148();
 uint64_t h=HeapCreate(0,131072,0),other_heap=HeapCreate(0,0,0);check(h&&other_heap&&h!=other_heap,248);
 uint8_t*data=HeapAlloc(h,0,1);check(data&&!((uintptr_t)data&15)&&HeapSize(h,0,data)>=1,249);data[0]=0x3f;
 check(!HeapFree(other_heap,0,data)&&data[0]==0x3f,250);
 data=HeapReAlloc(h,8,data,70000);check(data&&data[0]==0x3f,251);for(unsigned i=1;i<70000;++i)check(data[i]==0,252);
 check(!HeapReAlloc(h,16,data,1024*1024)&&data[0]==0x3f,253);
 uint8_t*small=HeapReAlloc(h,0,data,32);check(small==data&&HeapFree(h,0,small),254);
 check(HeapAlloc(other_heap,8,16000)!=0,255);check(HeapDestroy(h)&&HeapDestroy(other_heap),256);
 check(!HeapAlloc(h,0,1)&&!HeapDestroy(h),257);check(owned_pages148()==pages,258);
 static const char text[]="M148_NATIVE_SESSION_MESSAGES_SRW_PASS\n";unsigned written=0;
 check(WriteFile(GetStdHandle((unsigned)-11),text,sizeof(text)-1,&written,0)&&written==sizeof(text)-1,237);ExitProcess(0);
}
