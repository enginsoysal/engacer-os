/* Shared Windows objects across private parent/child address spaces. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned size,pad;U reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;W show,reserved_bytes;unsigned pad2;U reserved_data,input,output,error;} SI;
typedef struct {U process,thread;unsigned pid,tid;} PI;
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,SI*,PI*);
__declspec(dllimport) U CreateEventW(void*,int,int,const W*);
__declspec(dllimport) U OpenEventW(unsigned,int,const W*);
__declspec(dllimport) U CreateSemaphoreW(void*,int,int,const W*);
__declspec(dllimport) U OpenSemaphoreW(unsigned,int,const W*);
__declspec(dllimport) U CreateWaitableTimerW(void*,int,const W*);
__declspec(dllimport) U OpenWaitableTimerW(unsigned,int,const W*);
__declspec(dllimport) int SetWaitableTimer(U,const long long*,int,void*,void*,int);
__declspec(dllimport) int SetEvent(U);
__declspec(dllimport) int ResetEvent(U);
__declspec(dllimport) int ReleaseSemaphore(U,int,int*);
__declspec(dllimport) unsigned WaitForSingleObject(U,unsigned);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) int GetExitCodeProcess(U,unsigned*);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) W* GetCommandLineW(void);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
static int same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static void print(const char*s,unsigned n){unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),s,n,&wrote,0);}
static PI spawn(const W*text){SI si={0};PI pi;W command[64];unsigned i=0;while(text[i]){command[i]=text[i];++i;}command[i]=0;si.size=sizeof(si);if(!CreateProcessW(L"C:\\Program Files\\7-Zip\\child.exe",command,0,0,0,0,0,0,&si,&pi))ExitProcess(51);return pi;}
static void close_pi(PI pi){if(!CloseHandle(pi.process)||!CloseHandle(pi.thread))ExitProcess(52);}
static void quotas(void){W names[32][24];U original[32],opened[32];for(unsigned i=0;i<32;++i){const W*prefix=L"Engacer142Quota";unsigned n=0;while(prefix[n]){names[i][n]=prefix[n];++n;}names[i][n++]=(W)('0'+i/10);names[i][n++]=(W)('0'+i%10);names[i][n]=0;original[i]=CreateEventW(0,1,i&1,names[i]);if(!original[i])ExitProcess(74);}for(unsigned i=0;i<32;++i){opened[i]=OpenEventW(0x1f0003,0,names[i]);if(!opened[i])ExitProcess(75);}if(OpenEventW(0x1f0003,0,names[0])||GetLastError()!=8||CreateEventW(0,1,0,L"Engacer142Overflow")||GetLastError()!=8)ExitProcess(76);U stale=opened[0];if(!CloseHandle(stale))ExitProcess(77);if(CreateEventW(0,1,0,L"Engacer142Overflow")||GetLastError()!=8)ExitProcess(78);opened[0]=OpenEventW(0x1f0003,0,names[0]);if(!opened[0]||opened[0]==stale||WaitForSingleObject(stale,0)!=~0u||GetLastError()!=6||CloseHandle(stale))ExitProcess(79);for(unsigned i=0;i<32;++i)if(!CloseHandle(original[i]))ExitProcess(80);for(unsigned i=0;i<32;++i)if(WaitForSingleObject(opened[i],0)!=(i&1?0:258)||!CloseHandle(opened[i]))ExitProcess(81);}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){W*command=GetCommandLineW();
 if(same(command,L"named-child")){U event=OpenEventW(0x1f0003,0,L"Engacer142Event"),sem=OpenSemaphoreW(0x1f0003,0,L"Engacer142Semaphore"),timer=OpenWaitableTimerW(0x1f0003,0,L"Engacer142Timer");int previous;if(!event||!sem||!timer||WaitForSingleObject(sem,0)||!ReleaseSemaphore(sem,1,&previous)||previous!=0||WaitForSingleObject(timer,~0u)||!SetEvent(event))ExitProcess(53);if(!CloseHandle(event)||!CloseHandle(sem)||!CloseHandle(timer))ExitProcess(54);ExitProcess(17);}
 if(same(command,L"named-sleeper")){Sleep(200);ExitProcess(19);}
 if(same(command,L"named-survivor")){U ready=OpenEventW(0x1f0003,0,L"Engacer142Ready"),keep=OpenEventW(0x1f0003,0,L"Engacer142Keep");if(!ready||!keep||!SetEvent(ready))ExitProcess(55);Sleep(200);if(!SetEvent(keep)||WaitForSingleObject(keep,0)||!CloseHandle(ready)||!CloseHandle(keep))ExitProcess(56);static const char done[]="M142_NAMED_OBJECT_SURVIVED_CREATOR_PASS\n";print(done,sizeof(done)-1);ExitProcess(0);}
 if(same(command,L"named-block")){U event=OpenEventW(0x100000,0,L"Engacer142Block");if(!event)ExitProcess(57);static const char ready[]="M142_NAMED_CHILD_WAITING\n";print(ready,sizeof(ready)-1);WaitForSingleObject(event,~0u);ExitProcess(58);}
#ifdef NAMED_CANCEL142
 U block=CreateEventW(0,1,0,L"Local\\Engacer142Block");if(!block)ExitProcess(59);for(unsigned i=0;i<3;++i){PI child=spawn(L"named-block");(void)child;}static const char ready[]="M142_NAMED_GROUP_CANCEL_READY\n";print(ready,sizeof(ready)-1);WaitForSingleObject(block,~0u);ExitProcess(60);
#endif
#ifdef NAMED_PARENT_EXITS142
 U ready=CreateEventW(0,1,0,L"Local\\Engacer142Ready"),keep=CreateEventW(0,1,0,L"Local\\Engacer142Keep");if(!ready||!keep)ExitProcess(61);PI surviving=spawn(L"named-survivor");(void)surviving;if(WaitForSingleObject(ready,15000)||!CloseHandle(ready)||!CloseHandle(keep))ExitProcess(62);static const char leaving[]="M142_NAMED_CREATOR_EXIT_BEGIN\n";print(leaving,sizeof(leaving)-1);ExitProcess(0);
#endif
 U event=CreateEventW(0,1,0,L"Local\\Engacer142Event");if(!event||GetLastError())ExitProcess(63);U alias=CreateEventW(0,0,1,L"Engacer142Event");if(!alias||GetLastError()!=183||WaitForSingleObject(event,0)!=258)ExitProcess(64);U duplicates[2]={event,alias};if(WaitForMultipleObjects(2,duplicates,1,0)!=~0u||GetLastError()!=87||!CloseHandle(alias))ExitProcess(65);
 U wait_only=OpenEventW(0x100000,0,L"Engacer142Event"),modify_only=OpenEventW(2,0,L"Engacer142Event");if(!wait_only||!modify_only||SetEvent(wait_only)||GetLastError()!=5||WaitForSingleObject(modify_only,0)!=~0u||GetLastError()!=5||!CloseHandle(wait_only)||!CloseHandle(modify_only))ExitProcess(66);if(CreateSemaphoreW(0,0,1,L"Engacer142Event")||GetLastError()!=6)ExitProcess(67);
 U global=CreateEventW(0,1,1,L"Global\\Engacer142Event");if(!global||WaitForSingleObject(global,0)||WaitForSingleObject(event,0)!=258||!CloseHandle(global))ExitProcess(68);
 U sem=CreateSemaphoreW(0,1,2,L"Local\\Engacer142Semaphore"),timer=CreateWaitableTimerW(0,0,L"Local\\Engacer142Timer");long long due=-1000000;if(!sem||!timer||!SetWaitableTimer(timer,&due,0,0,0,0))ExitProcess(69);PI child=spawn(L"named-child");U waits[3]={child.process,event,sem};if(WaitForMultipleObjects(3,waits,1,15000))ExitProcess(70);unsigned code;if(!GetExitCodeProcess(child.process,&code)||code!=17||WaitForSingleObject(sem,0)!=258||WaitForSingleObject(event,0)||WaitForSingleObject(event,0)||!ResetEvent(event)||WaitForSingleObject(event,0)!=258)ExitProcess(71);close_pi(child);if(!CloseHandle(event)||CloseHandle(event)||GetLastError()!=6||!CloseHandle(sem)||!CloseHandle(timer))ExitProcess(72);
 PI sleeper=spawn(L"named-sleeper");if(WaitForSingleObject(sleeper.process,~0u)||!GetExitCodeProcess(sleeper.process,&code)||code!=19)ExitProcess(73);close_pi(sleeper);quotas();static const char ok[]="M142_NAMED_SYNC_CHILD_AND_ATOMIC_WAIT_PASS\n";print(ok,sizeof(ok)-1);ExitProcess(0);
}
