/* Synthetic process ownership probe, plus concurrent original 7-Zip children. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned size,pad;U reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;W show,reserved_bytes;unsigned pad2;U reserved_data,input,output,error;} SI;
typedef struct {U process,thread;unsigned pid,tid;} PI;
_Static_assert(sizeof(SI)==104,"Win64 startup ABI");
_Static_assert(sizeof(PI)==24,"Win64 result ABI");
__declspec(dllimport) U CreateThread(void*,U,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) void ExitThread(unsigned);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,SI*,PI*);
__declspec(dllimport) unsigned GetCurrentProcessId(void);
__declspec(dllimport) U GetCurrentProcess(void);
__declspec(dllimport) unsigned GetProcessId(U);
__declspec(dllimport) unsigned GetThreadId(U);
__declspec(dllimport) int GetExitCodeProcess(U,unsigned*);
__declspec(dllimport) int GetExitCodeThread(U,unsigned*);
__declspec(dllimport) unsigned WaitForSingleObject(U,unsigned);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) unsigned ResumeThread(U);
__declspec(dllimport) int TerminateProcess(U,unsigned);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) U CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,U);
__declspec(dllimport) W* GetCommandLineW(void);
__declspec(dllimport) unsigned TlsAlloc(void);
__declspec(dllimport) int TlsSetValue(unsigned,U);
__declspec(dllimport) U TlsGetValue(unsigned);
static volatile unsigned private_value=17;
static void print(const char*s,unsigned n){unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),s,n,&wrote,0);}
static int same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static void line(W*out,const W*in){unsigned i=0;while(in[i]&&i<255){out[i]=in[i];++i;}out[i]=0;}
static PI spawn(const W*app,const W*text,unsigned flags){SI si={0};PI pi={0};W command[256];si.size=sizeof(si);line(command,text);if(!CreateProcessW(app,command,0,0,0,flags,0,0,&si,&pi)){char debug[]="M142_CREATE_ERROR 00000000\n";unsigned value=GetLastError();for(unsigned i=0;i<8;++i){unsigned digit=(value>>(28-i*4))&15;debug[18+i]=(char)(digit<10?'0'+digit:'a'+digit-10);}print(debug,sizeof(debug)-1);ExitProcess(81);}if(!pi.process||!pi.thread||!pi.pid||!pi.tid||pi.pid==GetCurrentProcessId()||GetProcessId(pi.process)!=pi.pid||GetThreadId(pi.thread)!=pi.tid)ExitProcess(82);return pi;}
static void close_pi(PI p){if(!CloseHandle(p.process)||!CloseHandle(p.thread))ExitProcess(83);unsigned code;if(GetExitCodeProcess(p.process,&code)||WaitForSingleObject(p.process,0)!=~0u)ExitProcess(84);}
static unsigned worker(void*unused){(void)unused;Sleep(500);return 23;}
void entry(void);
void* volatile relocation_anchor=&entry;
void entry(void){
 W*command=GetCommandLineW();unsigned own=GetCurrentProcessId();if(!own||GetProcessId(GetCurrentProcess())!=own)ExitProcess(85);
 if(same(command,L"child.exe fault")){volatile U address=1;*(volatile unsigned*)(U)address=1;ExitProcess(96);}
 if(same(command,L"child.exe worker")){U thread=CreateThread(0,0,worker,0,0,0);if(!thread||!CloseHandle(thread))ExitProcess(97);ExitThread(5);}
 if(same(command,L"child.exe alpha")||same(command,L"child.exe beta")||same(command,L"child.exe survivor")){
  if(private_value!=17||TlsAlloc()!=0||TlsGetValue(0))ExitProcess(86);private_value=100;TlsSetValue(0,100);
  if(same(command,L"child.exe survivor")){Sleep(500);U file=CreateFileW(L"child-survivor.txt",0x40000000u,0,0,2,0x80,0);static const char data[]="The child continued after its parent exited.\n";unsigned wrote;if(file==~(U)0||!WriteFile(file,data,sizeof(data)-1,&wrote,0)||wrote!=sizeof(data)-1||!CloseHandle(file))ExitProcess(87);static const char ok[]="M142_CHILD_SURVIVED_PARENT_PASS\n";print(ok,sizeof(ok)-1);ExitProcess(0);}
  unsigned code=same(command,L"child.exe alpha")?13:14;Sleep(code==13?150:250);if(private_value!=100||TlsGetValue(0)!=100)ExitProcess(88);ExitProcess(code);
 }
 if(private_value!=17||TlsAlloc()!=0)ExitProcess(89);private_value=42;TlsSetValue(0,42);
#ifdef PARENT_EXITS142
 PI survivor=spawn(L"C:\\Program Files\\7-Zip\\child.exe",L"child.exe survivor",0);(void)survivor;static const char parent[]="M142_PARENT_EXIT_BEGIN\n";print(parent,sizeof(parent)-1);ExitProcess(0);
#endif
 PI a=spawn(L"C:\\Program Files\\7-Zip\\child.exe",L"child.exe alpha",4),b=spawn(L"C:\\Program Files\\7-Zip\\child.exe",L"child.exe beta",4);
 if(a.pid==b.pid||a.tid==b.tid||WaitForSingleObject(a.process,0)!=258||WaitForSingleObject(a.thread,0)!=258||ResumeThread(a.thread)!=1||ResumeThread(b.thread)!=1)ExitProcess(90);
 U processes[2]={a.process,b.process};if(WaitForMultipleObjects(2,processes,1,10000)!=0)ExitProcess(91);
 unsigned ca,cb,ta,tb;if(!GetExitCodeProcess(a.process,&ca)||!GetExitCodeProcess(b.process,&cb)||!GetExitCodeThread(a.thread,&ta)||!GetExitCodeThread(b.thread,&tb)||ca!=13||cb!=14||ta!=13||tb!=14||private_value!=42||TlsGetValue(0)!=42)ExitProcess(92);close_pi(a);close_pi(b);
 PI terminated=spawn(L"C:\\Program Files\\7-Zip\\child.exe",L"child.exe alpha",4);if(!TerminateProcess(terminated.process,77)||WaitForSingleObject(terminated.process,1000)!=0||!GetExitCodeProcess(terminated.process,&ca)||ca!=77)ExitProcess(93);close_pi(terminated);
 PI faulted=spawn(L"C:\\Program Files\\7-Zip\\child.exe",L"child.exe fault",0);
 if(WaitForSingleObject(faulted.process,10000)!=0||!GetExitCodeProcess(faulted.process,&ca)||ca!=0xc0000005u||private_value!=42||TlsGetValue(0)!=42)ExitProcess(98);close_pi(faulted);
 PI worker_child=spawn(L"C:\\Program Files\\7-Zip\\child.exe",L"child.exe worker",0);
 if(WaitForSingleObject(worker_child.thread,10000)!=0||!GetExitCodeThread(worker_child.thread,&ta)||ta!=5||WaitForSingleObject(worker_child.process,0)!=258||!GetExitCodeProcess(worker_child.process,&ca)||ca!=259||WaitForSingleObject(worker_child.process,10000)!=0||!GetExitCodeProcess(worker_child.process,&ca)||ca!=23)ExitProcess(99);close_pi(worker_child);
 DeleteFileW(L"child-a.zip");DeleteFileW(L"child-b.zip");
 PI archive_a=spawn(L"C:\\Program Files\\7-Zip\\original7z.exe",L"original7z.exe a -tzip -mx=1 -mmt=off -y child-a.zip child-input.txt",0);
 PI archive_b=spawn(L"C:\\Program Files\\7-Zip\\original7z.exe",L"original7z.exe a -tzip -mx=1 -mmt=off -y child-b.zip child-input.txt",0);
 if(!CloseHandle(archive_a.thread)||!CloseHandle(archive_b.thread))ExitProcess(94);processes[0]=archive_a.process;processes[1]=archive_b.process;
 if(WaitForMultipleObjects(2,processes,1,30000)!=0||!GetExitCodeProcess(archive_a.process,&ca)||!GetExitCodeProcess(archive_b.process,&cb)||ca||cb||!CloseHandle(archive_a.process)||!CloseHandle(archive_b.process)||private_value!=42||TlsGetValue(0)!=42)ExitProcess(95);
 static const char ok[]="M142_PROCESSES_ISOLATION_ORIGINAL_CHILDREN_PASS\n";print(ok,sizeof(ok)-1);ExitProcess(0);
}
