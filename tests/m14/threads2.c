/* Synthetic Win64 scheduling probe; never executed on the host. */
typedef unsigned long long U;
typedef struct {U debug;int lock,recursion;U owner,semaphore,spin;} CRITICAL;
__declspec(dllimport) U CreateThread(void*,U,void*,void*,unsigned,unsigned*);
__declspec(dllimport) unsigned ResumeThread(U);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) int GetExitCodeThread(U,unsigned*);
__declspec(dllimport) unsigned GetCurrentThreadId(void);
__declspec(dllimport) unsigned GetLastError(void);
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
__declspec(dllimport) U CreateEventW(void*,int,int,const unsigned short*);
__declspec(dllimport) U OpenEventW(unsigned,int,const unsigned short*);
__declspec(dllimport) int SetEvent(U);
__declspec(dllimport) U CreateSemaphoreW(void*,int,int,const unsigned short*);
__declspec(dllimport) int ReleaseSemaphore(U,int,int*);
__declspec(dllimport) unsigned WaitForSingleObject(U,unsigned);
__declspec(dllimport) U CreateWaitableTimerW(void*,int,const unsigned short*);
__declspec(dllimport) int SetWaitableTimer(U,const long long*,int,void*,void*,int);
__declspec(dllimport) int CancelWaitableTimer(U);
static U wake_event;
static CRITICAL gate;
static unsigned tls,counter,ids[4];
static unsigned worker(void*arg){
 unsigned n=(unsigned)(U)arg;
 if(n==4){Sleep(30);if(!SetEvent(wake_event))ExitProcess(30);return 91;}
 if(TlsGetValue(tls))ExitProcess(31);ids[n]=GetCurrentThreadId();if(!TlsSetValue(tls,100+n))ExitProcess(11);
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
 unsigned join=WaitForMultipleObjects(4,threads,1,10000);if(join!=0){char debug[80]="M142_JOIN_DEBUG ";unsigned values[3]={join,GetLastError(),counter},at=16;for(unsigned i=0;i<3;++i){for(unsigned n=0;n<8;++n){unsigned digit=(values[i]>>(28-4*n))&15;debug[at++]=(char)(digit<10?'0'+digit:'a'+digit-10);}debug[at++]=' ';}debug[at++]='\n';unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),debug,at,&wrote,0);ExitProcess(5);}
 if(counter!=160||TlsGetValue(tls)!=42)ExitProcess(6);
 for(unsigned i=0;i<4;++i){unsigned code;if(!GetExitCodeThread(threads[i],&code)||code!=20+i||!ids[i]||ids[i]==main_id)ExitProcess(7);for(unsigned j=0;j<i;++j)if(ids[i]==ids[j])ExitProcess(8);if(!CloseHandle(threads[i]))ExitProcess(9);}
 for(unsigned repeat=0;repeat<24;++repeat){U h=CreateThread(0,0,worker,0,0,0);if(!h||WaitForSingleObject(h,10000)!=0||!CloseHandle(h)||CloseHandle(h))ExitProcess(32);}
 U events[2]={CreateEventW(0,0,1,0),CreateEventW(0,0,0,0)};
 if(!events[0]||!events[1]||WaitForMultipleObjects(2,events,1,0)!=258||WaitForSingleObject(events[0],0)!=0||WaitForSingleObject(events[0],0)!=258)ExitProcess(33);
 if(!SetEvent(events[1])||WaitForMultipleObjects(2,events,0,0)!=1)ExitProcess(34);
 static const unsigned short name[]={'M','1','4','2',0};U named=CreateEventW(0,1,0,name),opened=OpenEventW(0x100002,0,name);
 if(!named||!opened||named==opened||!CloseHandle(named)||!SetEvent(opened)||WaitForSingleObject(opened,0)!=0||WaitForSingleObject(opened,0)!=0||!CloseHandle(opened))ExitProcess(35);
 wake_event=events[1];U producer=CreateThread(0,0,worker,(void*)(U)4,0,0);
 if(!producer||WaitForSingleObject(wake_event,1000)!=0||WaitForSingleObject(producer,1000)!=0||!CloseHandle(producer))ExitProcess(36);
 U sem=CreateSemaphoreW(0,1,2,0);int previous=-1;
 if(!sem||WaitForSingleObject(sem,0)!=0||WaitForSingleObject(sem,0)!=258||!ReleaseSemaphore(sem,2,&previous)||previous||ReleaseSemaphore(sem,1,0)||WaitForSingleObject(sem,0)!=0||WaitForSingleObject(sem,0)!=0||WaitForSingleObject(sem,0)!=258||!CloseHandle(sem))ExitProcess(37);
 U timer=CreateWaitableTimerW(0,0,0);long long due=-200000;
 if(!timer||!SetWaitableTimer(timer,&due,0,0,0,0)||WaitForSingleObject(timer,1000)!=0||WaitForSingleObject(timer,0)!=258)ExitProcess(38);
 due=-100000;if(!SetWaitableTimer(timer,&due,10,0,0,0)||WaitForSingleObject(timer,1000)!=0||WaitForSingleObject(timer,1000)!=0||!CancelWaitableTimer(timer)||WaitForSingleObject(timer,30)!=258||!CloseHandle(timer))ExitProcess(39);
 if(!CloseHandle(events[0])||!CloseHandle(events[1]))ExitProcess(40);
 if(!TlsFree(tls))ExitProcess(10);
 static const char idle[]="M142_SLEEP_IDLE_BEGIN\n";unsigned idle_wrote;WriteFile(GetStdHandle((unsigned)-11),idle,sizeof(idle)-1,&idle_wrote,0);Sleep(1000);
 static const char ok[]="M142_THREADS_TLS_WAIT_SLEEP_LOCK_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);
}
