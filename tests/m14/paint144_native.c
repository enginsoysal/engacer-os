/* Own CPL3 painter, verified against actual native framebuffer pixels. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {int left,top,right,bottom;} RECT;
typedef struct {H dc;int erase;RECT rect;int restore,increment;unsigned char reserved[32];unsigned pad;} PAINT;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) int InvalidateRect(H,const RECT*,int);
__declspec(dllimport) int ValidateRect(H,const RECT*);
__declspec(dllimport) int GetUpdateRect(H,RECT*,int);
__declspec(dllimport) int UpdateWindow(H);
__declspec(dllimport) H BeginPaint(H,PAINT*);
__declspec(dllimport) int EndPaint(H,const PAINT*);
__declspec(dllimport) int FillRect(H,const RECT*,H);
__declspec(dllimport) H GetSysColorBrush(int);
__declspec(dllimport) int TextOutW(H,int,int,const W*,int);
__declspec(dllimport) int GetTextExtentPoint32W(H,const W*,int,int*);
__declspec(dllimport) int SetBkMode(H,int);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static unsigned paints;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*why){if(!ok){say("M144_PAINT_FAIL ");say(why);say("\n");ExitProcess(1);}}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==15){PAINT paint;H dc=BeginPaint(h,&paint);check(dc!=0,"real DC");check(FillRect(dc,&paint.rect,GetSysColorBrush(5)),"white background");RECT color={20,20,100,60};check(FillRect(dc,&color,GetSysColorBrush(13)),"colored primitive");int size[2];check(GetTextExtentPoint32W(dc,L"Native drawn text",17,size)&&size[0]>50&&size[1]==16,"actual native font measure");SetBkMode(dc,1);check(TextOutW(dc,10,80,L"Native drawn text",17),"native glyph command");check(EndPaint(h,&paint),"DC release");check(!GetUpdateRect(h,0,0),"validated paint");++paints;return 0;}
 if(m==0x102&&wp=='a'){for(unsigned n=0;n<20;++n){check(InvalidateRect(h,0,1)&&UpdateWindow(h),"repaint");}say("M144_PAINT_REPAINTED\n");return 0;}
 if(m==2){check(paints>=21,"paint callbacks");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){CLASS cls={0};cls.proc=anchor;cls.name=L"NativePaint144";check(RegisterClassW(&cls),"register");H h=CreateWindowExW(0,cls.name,L"Native CPL3 drawing",0x10cf0000,180,100,540,300,0,0,0,0);check(h!=0,"window");RECT region={5,6,30,40};check(InvalidateRect(h,&region,1),"invalidate");RECT got;check(GetUpdateRect(h,&got,0)&&got.left<=5&&got.right>=30,"damage bounds");check(UpdateWindow(h),"initial paint");say("M144_PAINT_READY\n");MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);say("M144_PAINT_LIFETIME_PASS\n");ExitProcess(0);}
