/* Owned eager-text clipboard: private processes, real threads and byte limits. */
#define W8_USER
#include <engine/windows8.h>
#include <engine/winui144.h>
typedef unsigned long long H;typedef long long I;typedef unsigned short W;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
typedef struct {unsigned size,pad;H reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;unsigned short show,bytes;unsigned pad2;H reserved2,input,output,error;} START;
typedef struct {H process,thread;unsigned pid,tid;} PROCESS;
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) int PeekMessageW(MSG*,H,unsigned,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) int OpenClipboard(H);
__declspec(dllimport) int CloseClipboard(void);
__declspec(dllimport) int EmptyClipboard(void);
__declspec(dllimport) H SetClipboardData(unsigned,H);
__declspec(dllimport) H GetClipboardData(unsigned);
__declspec(dllimport) int IsClipboardFormatAvailable(unsigned);
__declspec(dllimport) unsigned CountClipboardFormats(void);
__declspec(dllimport) unsigned EnumClipboardFormats(unsigned);
__declspec(dllimport) H GetClipboardOwner(void);
__declspec(dllimport) H GetOpenClipboardWindow(void);
__declspec(dllimport) unsigned GetClipboardSequenceNumber(void);
__declspec(dllimport) H GlobalAlloc(unsigned,H);
__declspec(dllimport) H GlobalFree(H);
__declspec(dllimport) void*GlobalLock(H);
__declspec(dllimport) int GlobalUnlock(H);
__declspec(dllimport) unsigned GlobalFlags(H);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void SetLastError(unsigned);
__declspec(dllimport) W*GetCommandLineW(void);
__declspec(dllimport) unsigned GetModuleFileNameW(H,W*,unsigned);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,START*,PROCESS*);
__declspec(dllimport) H CreateThread(void*,H,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForSingleObject(H,unsigned);
__declspec(dllimport) int GetExitCodeProcess(H,unsigned*);
__declspec(dllimport) int GetExitCodeThread(H,unsigned*);
__declspec(dllimport) int CloseHandle(H);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static const W original[]=L"Native \u00e9 \u03a9 \U0001f600\r\n";
static const W child_text[]=L"Private child \u00e9 \U0001f600";
static const W thread_text[]=L"Exited thread \u00e9";
static W large146[8193];static unsigned destroyed146;
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int yes,const char*message){if(!yes){say("M146_CLIPBOARD_FAIL ");say(message);say("\n");ExitProcess(1);}}
static unsigned length(const W*s){unsigned n=0;while(s[n])++n;return n;}
static unsigned same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static unsigned contains(const W*s,const W*marker){for(unsigned i=0;s[i];++i){unsigned n=0;while(marker[n]&&s[i+n]==marker[n])++n;if(!marker[n])return 1;}return 0;}
static I procedure(H h,unsigned m,H w,I l){if(m==0x307){++destroyed146;return 0;}return DefWindowProcW(h,m,w,l);}
static PROC volatile anchor146=procedure;
static H owner(void){H h=CreateWindowExW(0,L"Clipboard146",L"Clipboard ABI",0,80,80,320,200,0,0,0,0);check(h!=0,"hidden owned window");return h;}
static H memory(const W*s){unsigned n=length(s)+1;H h=GlobalAlloc(0x42,n*2);check(h!=0,"movable allocation");W*p=GlobalLock(h);check(p!=0,"allocation lock");for(unsigned i=0;i<n;++i)p[i]=s[i];check(!GlobalUnlock(h)&&!GetLastError(),"allocation unlock");return h;}
static void read_equal(const W*expected){H h=GetClipboardData(13);check(h!=0,"read Unicode");W*p=GlobalLock(h);check(p&&same(p,expected),"exact Unicode bytes");check(!GlobalUnlock(h)&&!GetLastError(),"read unlock");}
static void publish(H window,const W*text){check(OpenClipboard(window)&&EmptyClipboard(),"open empty");H h=memory(text);check(SetClipboardData(13,h)==h,"publish Unicode");check(CloseClipboard(),"publish close");}
static void pump(void){MSG msg;unsigned n=0;while(PeekMessageW(&msg,0,0,0,1)){check(++n<128,"bounded notification drain");DispatchMessageW(&msg);}}
static void child_process(const W*mode){
 W path[512],command[600];unsigned n=GetModuleFileNameW(0,path,512);check(n&&n<512,"own path");unsigned at=0;command[at++]='"';for(unsigned i=0;i<n;++i)command[at++]=path[i];command[at++]='"';command[at++]=' ';for(unsigned i=0;mode[i];++i)command[at++]=mode[i];command[at]=0;
 START startup={0};startup.size=104;PROCESS p={0};check(CreateProcessW(path,command,0,0,0,0,0,0,&startup,&p),"private process creation");check(WaitForSingleObject(p.process,30000)==0,"private process wait");unsigned code=99;check(GetExitCodeProcess(p.process,&code)&&code==0,"private process result");check(CloseHandle(p.thread)&&CloseHandle(p.process),"private process handles");
}
static unsigned worker(void*argument){
 unsigned mode=(unsigned)(H)argument;
 if(!mode){if(OpenClipboard(0)||GetLastError()!=5)return 61;if(GetClipboardData(13)||GetLastError()!=1418)return 62;if(CloseClipboard()||GetLastError()!=1418)return 63;return 0;}
 if(mode==1){if(!OpenClipboard(0))return 64;read_equal(original);return CloseClipboard()?0:65;}
 H window=owner();check(OpenClipboard(window)&&EmptyClipboard(),"thread open");H h=memory(thread_text);check(SetClipboardData(13,h)==h,"thread publication");return 0;
}
static void thread_case(unsigned mode){unsigned id=0;H h=CreateThread(0,0,worker,(void*)(H)mode,0,&id);check(h&&WaitForSingleObject(h,30000)==0,"real thread wait");unsigned code=99;check(GetExitCodeThread(h,&code)&&code==0&&CloseHandle(h),"real thread result");}
static I raw(unsigned mode,void*pointer){
 register H r8 __asm__("r8")=0,r10 __asm__("r10")=0;H result=W8_SYS_UI144;
 __asm__ volatile("int $0x80":"+a"(result):"D"((H)WUI_CLIPBOARD146),"S"((H)mode),"d"((H)pointer),"r"(r10),"r"(r8):"memory","rcx","r11");return(I)result;
}
void entry(void){
 CLASS cls={0};cls.proc=anchor146;cls.name=L"Clipboard146";check(RegisterClassW(&cls)!=0,"window class");
 const W*command=GetCommandLineW();
 if(contains(command,L"--busy")){check(!OpenClipboard(0)&&GetLastError()==5,"private open exclusion");check(!GetClipboardData(13)&&GetLastError()==1418,"private data exclusion");ExitProcess(0);}
 if(contains(command,L"--reader")){H other=GetClipboardOwner();check(other&&!OpenClipboard(other)&&GetLastError()==1400,"foreign window is not caller owned");check(OpenClipboard(0),"private reader open");read_equal(original);check(CloseClipboard(),"private reader close");ExitProcess(0);}
 if(contains(command,L"--publish-exit")){H window=owner();check(OpenClipboard(window)&&EmptyClipboard(),"private source open");H h=memory(child_text);check(SetClipboardData(13,h)==h,"private source publication");ExitProcess(0);}
 H window=owner();check(!OpenClipboard(123)&&GetLastError()==1400,"invalid owner refusal");
 check(OpenClipboard(window)&&EmptyClipboard()&&CountClipboardFormats()==0,"empty state");check(GetClipboardOwner()==window&&GetOpenClipboardWindow()==window,"owner identities");
 H h=memory(original);check(SetClipboardData(13,h)==h&&GetClipboardData(13)==h,"transferred handle");check(GlobalFree(h)==h&&GetLastError()==5,"system ownership prevents caller free");
 read_equal(original);check(CountClipboardFormats()==3&&IsClipboardFormatAvailable(1)&&IsClipboardFormatAvailable(7)&&IsClipboardFormatAvailable(13)&&!IsClipboardFormatAvailable(0xc123),"actual synthesized text formats");
 check(EnumClipboardFormats(0)==13&&EnumClipboardFormats(13)==1&&EnumClipboardFormats(1)==7&&!EnumClipboardFormats(7)&&!GetLastError(),"format enumeration");
 H bytes=GetClipboardData(1);const char*text=GlobalLock(bytes);const char*expected="Native \xc3\xa9 \xce\xa9 \xf0\x9f\x98\x80\r\n";check(text!=0,"byte-text lock");for(unsigned i=0;expected[i]||text[i];++i)check(expected[i]==text[i],"UTF8 ACP synthesis");check(!GlobalUnlock(bytes)&&!GetLastError(),"byte-text unlock");
 check(GlobalLock(h)!=0&&!CloseClipboard()&&GetLastError()==212,"locked clipboard memory cannot close");check(!GlobalUnlock(h)&&!GetLastError(),"unlock before close");
 H bad=memory(L"unsupported");check(!SetClipboardData(1,bad)&&GetLastError()==50&&!GlobalFree(bad),"unsupported publication retains caller ownership");
 check(!SetClipboardData(13,0)&&GetLastError()==50,"delayed rendering refuses explicitly");W invalid[]={0xd800,0};bad=memory(invalid);check(!SetClipboardData(13,bad)&&GetLastError()==1113&&!GlobalFree(bad),"invalid UTF16 failure atomicity");read_equal(original);
 unsigned sequence=GetClipboardSequenceNumber();char invalid_utf8[]={ (char)0xc0,(char)0xaf,0 };wclip_transfer146 transfer={0,(H)invalid_utf8,sizeof(invalid_utf8),0};check(raw(WCLIP_WRITE146,&transfer)==-1113&&GetClipboardSequenceNumber()==sequence,"kernel rejects malformed UTF8 without mutation");
 transfer.buffer=W8_LIMIT-2;transfer.bytes=4;check(raw(WCLIP_WRITE146,&transfer)==-998&&GetClipboardSequenceNumber()==sequence,"kernel refuses invalid input without mutation");read_equal(original);
 transfer.revision=~(H)0;transfer.buffer=(H)invalid_utf8;transfer.bytes=sizeof(invalid_utf8);check(raw(WCLIP_READ146,&transfer)==-1237,"stale snapshot refusal");
 thread_case(0);child_process(L"--busy");check(CloseClipboard()&&!GetOpenClipboardWindow(),"close ownership");check(GlobalFlags(h)==0x8000&&GetLastError()==6,"borrowed handle expires after close");check(!GetClipboardData(13)&&GetLastError()==1418,"data requires open");
 thread_case(1);child_process(L"--reader");
 for(unsigned i=0;i<4095;++i)large146[i]='A';large146[4095]=0xe9;large146[4096]='B';large146[4097]=0;publish(window,large146);check(OpenClipboard(0),"boundary read open");read_equal(large146);check(CloseClipboard(),"boundary close");
 for(unsigned i=0;i<8191;++i)large146[i]='Z';large146[8191]=0;publish(window,large146);check(OpenClipboard(window),"maximum read open");read_equal(large146);
 large146[8191]='Z';large146[8192]=0;bad=memory(large146);check(!SetClipboardData(13,bad)&&GetLastError()==1816&&!GlobalFree(bad),"quota preserves previous publication");large146[8191]=0;read_equal(large146);check(CloseClipboard(),"maximum close");
 child_process(L"--publish-exit");check(!GetClipboardOwner()&&OpenClipboard(0),"source exit releases open lock and owner");read_equal(child_text);check(CloseClipboard(),"source-exit reader close");
 thread_case(2);check(!GetClipboardOwner()&&OpenClipboard(0),"thread exit releases open lock and owner");read_equal(thread_text);check(CloseClipboard(),"thread-exit reader close");
 check(OpenClipboard(0)&&EmptyClipboard(),"null owner empty");bad=memory(original);check(!SetClipboardData(13,bad)&&GetLastError()==1418&&!GlobalFree(bad),"null owner cannot publish");check(CloseClipboard(),"null owner close");
 pump();check(destroyed146!=0,"queued owner notifications delivered");check(DestroyWindow(window),"owner teardown");say("M146_CLIPBOARD_PRIVATE_PROCESS_THREADS_LIMITS_PASS\n");ExitProcess(0);
}
