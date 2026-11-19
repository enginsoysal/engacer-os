/* Synthetic Win64 scheduling probe; never executed on the host. */
typedef unsigned long long U;
typedef struct {U debug;int lock,recursion;U owner,semaphore,spin;} CRITICAL;
__declspec(dllimport) U CreateThread(void*,U,void*,void*,unsigned,unsigned*);
__declspec(dllimport) unsigned ResumeThread(U);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) int GetExitCodeThread(U,unsigned*);
__declspec(dllimport) unsigned GetCurrentThreadId(void);
__declspec(dllimport) unsigned TlsAlloc(void);
__declspec(dllimport) int TlsSetValue(unsigned,U);
__declspec(dllimport) U TlsGetValue(unsigned);
__declspec(dllimport) int TlsFree(unsigned);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) void InitializeCriticalSection(CRITICAL*);
__declspec(dllimport) void EnterCriticalSection(CRITICAL*);
__declspec(dllimport) void LeaveCriticalSection(CRITICAL*);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
static CRITICAL gate;
static unsigned tls,counter,ids[4];
static unsigned worker(void*arg){
 unsigned n=(unsigned)(U)arg;
 ids[n]=GetCurrentThreadId();if(!TlsSetValue(tls,100+n))ExitProcess(11);
 for(unsigned i=0;i<40;++i){EnterCriticalSection(&gate);EnterCriticalSection(&gate);++counter;LeaveCriticalSection(&gate);LeaveCriticalSection(&gate);Sleep(10);if(TlsGetValue(tls)!=100+n)ExitProcess(12);}
 return 20+n;
}
void entry(void);
void* volatile relocation_anchor=&entry;
void entry(void){
 tls=TlsAlloc();if(tls==~0u)ExitProcess(1);
 InitializeCriticalSection(&gate);TlsSetValue(tls,42);
 U threads[4];unsigned main_id=GetCurrentThreadId();
 for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,worker,(void*)(U)i,4,0);if(!threads[i])ExitProcess(2);}
 if(WaitForMultipleObjects(4,threads,1,0)!=258)ExitProcess(3);
 for(unsigned i=0;i<4;++i)if(ResumeThread(threads[i])!=1)ExitProcess(4);
 if(WaitForMultipleObjects(4,threads,1,10000)!=0)ExitProcess(5);
 if(counter!=160||TlsGetValue(tls)!=42)ExitProcess(6);
 for(unsigned i=0;i<4;++i){unsigned code;if(!GetExitCodeThread(threads[i],&code)||code!=20+i||!ids[i]||ids[i]==main_id)ExitProcess(7);for(unsigned j=0;j<i;++j)if(ids[i]==ids[j])ExitProcess(8);if(!CloseHandle(threads[i]))ExitProcess(9);}
 if(!TlsFree(tls))ExitProcess(10);
 static const char ok[]="M142_THREADS_TLS_WAIT_SLEEP_LOCK_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);
}
