/* Own real-deadline timer fixture. The host only compiles this executable. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) H SetTimer(H,H,unsigned,void*);
__declspec(dllimport) int KillTimer(H,H);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) int PeekMessageW(MSG*,H,unsigned,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) unsigned GetTickCount(void);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static unsigned delivered,callbacks;static H callback_id;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*why){if(!ok){say("M144_TIMER_FAIL ");say(why);say("\n");ExitProcess(1);}}
static I procedure(H h,unsigned m,H wp,I lp){if(m==0x113){check(wp==53,"original timer identity");++delivered;if(delivered==1)check(SetTimer(h,53,40,0)==53,"timer replacement");if(delivered==3)check(KillTimer(h,53),"timer cancellation");return 0;}return DefWindowProcW(h,m,wp,lp);}
static void callback(H h,unsigned message,H id,unsigned time){(void)time;check(!h&&message==0x113&&id==callback_id,"actual CPL3 callback identity");if(++callbacks==2){check(KillTimer(0,id),"thread callback cancellation");PostQuitMessage(0);}}
static PROC volatile anchor=procedure;
void entry(void){CLASS cls={0};cls.proc=anchor;cls.name=L"NativeTimer144";check(RegisterClassW(&cls),"register");H window=CreateWindowExW(0,cls.name,L"Timer fixture",0xcf0000,180,120,400,240,0,0,0,0);check(window!=0,"hidden window");unsigned start=GetTickCount();check(SetTimer(window,53,1000,0)==53,"real timer creation");say("M144_TIMER_WAITING\n");MSG msg;while(delivered<3){check(GetMessageW(&msg,window,0x113,0x113)>0,"filtered deadline wait");DispatchMessageW(&msg);}check(GetTickCount()-start>=1080,"actual elapsed deadlines");check(!PeekMessageW(&msg,window,0x113,0x113,1),"no cancelled timer message");
 for(unsigned i=0;i<64;++i)check(SetTimer(window,1000+i,60000,0)==1000+i,"bounded timer table");check(!SetTimer(window,2000,60000,0)&&GetLastError()==1816,"quota refusal");for(unsigned i=0;i<63;++i)check(KillTimer(window,1000+i),"timer slot release");check(DestroyWindow(window),"remaining timer follows window lifetime");
 callback_id=SetTimer(0,0,40,callback);check(callback_id!=0,"thread callback timer");while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);check(callbacks==2,"original callback executed");say("M144_TIMER_LIFETIME_PASS\n");ExitProcess(0);}
