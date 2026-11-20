/* Registered clipboard formats must be global across real private processes. */
typedef unsigned long long H;
typedef unsigned short W;
typedef struct {unsigned size,pad;H reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;unsigned short show,bytes;unsigned pad2;H reserved2,input,output,error;} START;
typedef struct {H process,thread;unsigned pid,tid;} PROCESS;
__declspec(dllimport) unsigned RegisterClipboardFormatW(const W*);
__declspec(dllimport) int GetClipboardFormatNameW(unsigned,W*,int);
__declspec(dllimport) W*GetCommandLineW(void);
__declspec(dllimport) unsigned GetModuleFileNameW(H,W*,unsigned);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,START*,PROCESS*);
__declspec(dllimport) unsigned WaitForSingleObject(H,unsigned);
__declspec(dllimport) int GetExitCodeProcess(H,unsigned*);
__declspec(dllimport) int CloseHandle(H);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static const W*volatile anchor=L"Engacer.Clipboard.\u00c9tude";
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*message){if(!ok){say("M144_CLIPFORMAT_FAIL ");say(message);say("\n");ExitProcess(1);}}
static unsigned same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static unsigned child(void){const W*value=GetCommandLineW();const W*marker=L" --cf-child";for(unsigned i=0;value[i];++i){unsigned n=0;while(marker[n]&&value[i+n]==marker[n])++n;if(!marker[n])return 1;}return 0;}
void entry(void){
 if(child()){check(RegisterClipboardFormatW(L"Engacer.Clipboard.ChildFirst")>=0xc000,"child first format");ExitProcess(RegisterClipboardFormatW(L"engacer.clipboard.\u00e9TUDE"));}
 unsigned a=RegisterClipboardFormatW(anchor);check(a>=0xc000&&a<=0xffff,"registered range");check(RegisterClipboardFormatW(L"engacer.clipboard.\u00e9TUDE")==a,"case-insensitive Unicode identity");unsigned b=RegisterClipboardFormatW(L"Engacer.Clipboard.Second");check(b>=0xc000&&b!=a,"unique format name");W buffer[256];check(GetClipboardFormatNameW(a,buffer,256)>0&&same(buffer,anchor),"original name retained");check(GetClipboardFormatNameW(a,buffer,7)==6&&buffer[6]==0,"truncated format name");check(!GetClipboardFormatNameW(1,buffer,256)&&GetLastError()==87,"predefined format has no registered name");check(!RegisterClipboardFormatW(L"")&&GetLastError()==87,"empty format refused");W invalid[2]={0xd800,0};check(!RegisterClipboardFormatW(invalid)&&GetLastError()==1113,"invalid UTF16 refused");
 W path[512],command[600];unsigned length=GetModuleFileNameW(0,path,512);check(length&&length<512,"own original path");unsigned at=0;command[at++]='"';for(unsigned i=0;i<length;++i)command[at++]=path[i];command[at++]='"';const W*suffix=L" --cf-child";for(unsigned i=0;suffix[i];++i)command[at++]=suffix[i];command[at]=0;START startup={0};startup.size=104;PROCESS process={0};check(CreateProcessW(path,command,0,0,0,0,0,0,&startup,&process),"real private child process");check(WaitForSingleObject(process.process,30000)==0,"child process wait");unsigned code=0;check(GetExitCodeProcess(process.process,&code)&&code==a,"shared IDs across processes with different registration order");check(CloseHandle(process.thread)&&CloseHandle(process.process),"child handles closed");unsigned other=RegisterClipboardFormatW(L"Engacer.Clipboard.ChildFirst");check(other!=a&&other!=b&&GetClipboardFormatNameW(other,buffer,256)>0,"child's registration survives process exit");
 say("M144_CLIPFORMAT_SHARED_PASS\n");ExitProcess(0);
}
