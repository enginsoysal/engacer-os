/* Physical control-letter identity must not collapse into special keys. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) short GetKeyState(int);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static unsigned seen146;static const unsigned wanted146[]={0x43,0x48,0x49,0x4a,8,9,13};
static const char*const markers146[]={"M146_CHORD_C\n","M146_CHORD_H\n","M146_CHORD_I\n","M146_CHORD_J\n","M146_CHORD_BACKSPACE\n","M146_CHORD_TAB\n","M146_CHORD_ENTER\n"};
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int yes,const char*s){if(!yes){say("M146_CHORD_FAIL ");say(s);say("\n");ExitProcess(1);}}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==0x100&&wp!=0x11&&wp!=0xa2&&wp!=0xa3){check(seen146<7&&wp==wanted146[seen146],"virtual key identity/order");check(GetKeyState(0x11)<0,"consumed Control snapshot");say(markers146[seen146++]);return 0;}
 if(m==0x101&&wp==0x11&&seen146==7){check(GetKeyState(0x11)>=0,"physical release after consumed input");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor146=procedure;
void entry(void){CLASS cls={0};cls.proc=anchor146;cls.name=L"Chords146";check(RegisterClassW(&cls)!=0,"class");H window=CreateWindowExW(0,cls.name,L"Control shortcut identity",0x10cf0000,180,100,560,360,0,0,0,0);check(window!=0,"window");say("M146_CHORD_READY\n");Sleep(400);MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);check(seen146==7&&DestroyWindow(window),"complete and destroy");say("M146_CHORD_IDENTITY_PASS\n");ExitProcess(0);}
