/* Own deepest legal native HWND tree: initial visibility, paint, quota and teardown. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {int left,top,right,bottom;} RECT;
typedef struct {H dc;int erase;RECT rect;int restore,increment;unsigned char reserved[32];unsigned pad;} PAINT;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) int IsWindow(H);
__declspec(dllimport) H BeginPaint(H,PAINT*);
__declspec(dllimport) int EndPaint(H,const PAINT*);
__declspec(dllimport) int FillRect(H,const RECT*,H);
__declspec(dllimport) H GetSysColorBrush(int);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static H windows[32];static unsigned shows,painted;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*why){if(!ok){say("M144_DEEP_FAIL ");say(why);say("\n");ExitProcess(1);}}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==0x18&&wp)++shows;
 if(m==15){PAINT paint;H dc=BeginPaint(h,&paint);check(dc!=0,"paint DC");check(FillRect(dc,&paint.rect,GetSysColorBrush(h==windows[31]?13:5)),"actual retained surface");check(EndPaint(h,&paint),"paint release");if(h==windows[31]&&!painted){painted=1;say("M144_DEEP_PAINTED\n");}return 0;}
 if(m==2&&h==windows[0]){check(painted&&shows==32,"deep surface and initial show callbacks");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){CLASS cls={0};cls.proc=anchor;cls.name=L"NativeDeep144";check(RegisterClassW(&cls),"register");
 windows[0]=CreateWindowExW(0,cls.name,L"Maximum native nesting",0x10cf0000,180,100,540,300,0,0,0,0);check(windows[0]!=0,"root");
 for(unsigned n=1;n<32;++n){windows[n]=CreateWindowExW(0,cls.name,L"Nested",0x50000000,0,0,400,200,windows[n-1],0,0,0);check(windows[n]!=0,"legal child depth");}
 check(shows==32,"initial visibility callbacks");H refused=CreateWindowExW(0,cls.name,L"Over quota",0x50000000,0,0,100,100,windows[31],0,0,0);check(!refused&&GetLastError()==1816,"descriptor quota");say("M144_DEEP_READY\n");MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);
 for(unsigned n=0;n<32;++n)check(!IsWindow(windows[n]),"recursive descriptor cleanup");say("M144_DEEP_LIFETIME_PASS\n");ExitProcess(0);}
