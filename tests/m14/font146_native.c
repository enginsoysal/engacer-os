/* Owned GDI-to-native Unicode pixels, independently checked outside the guest. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {int left,top,right,bottom;} RECT;
typedef struct {H dc;int erase;RECT rect;int restore,incremental;unsigned char reserved[32];} PAINT;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) H BeginPaint(H,PAINT*);
__declspec(dllimport) int EndPaint(H,const PAINT*);
__declspec(dllimport) int FillRect(H,const RECT*,H);
__declspec(dllimport) int TextOutW(H,int,int,const W*,int);
__declspec(dllimport) unsigned SetTextColor(H,unsigned);
__declspec(dllimport) int SetBkMode(H,int);
__declspec(dllimport) int GetTextExtentPoint32W(H,const W*,int,int*);
__declspec(dllimport) H GetDC(H);
__declspec(dllimport) int ReleaseDC(H,H);
__declspec(dllimport) int SystemParametersInfoW(unsigned,unsigned,void*,unsigned);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static const W sample[]={65,0xe9,0x20ac,0x11e,0x131,0x15e,0xc6,63,0};
static const W fallback[]={0xd83d,0xde00,32,65,0};
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void number(unsigned value){char text[16],reverse[16];unsigned n=0,at=0;do{reverse[n++]=(char)('0'+value%10);value/=10;}while(value);while(n)text[at++]=reverse[--n];text[at]=0;say(text);}
static void check(int yes,const char*why){if(!yes){say("M146_FONT_FAIL ");say(why);say("\n");ExitProcess(1);}}
static I procedure(H h,unsigned message,H wp,I lp){
 if(message==0xf){PAINT paint;H dc=BeginPaint(h,&paint);check(dc&&FillRect(dc,&paint.rect,6),"paint white surface");SetTextColor(dc,0);check(SetBkMode(dc,1)!=0,"transparent text");check(TextOutW(dc,20,20,sample,8)&&TextOutW(dc,20,60,fallback,4),"original UTF-16 to native glyph bridge");check(EndPaint(h,&paint),"end paint");return 0;}
 if(message==2){PostQuitMessage(0);return 0;}return DefWindowProcW(h,message,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){CLASS cls={0};cls.proc=anchor;cls.name=L"UnicodePixels146";cls.background=6;check(RegisterClassW(&cls)!=0,"class");H root=CreateWindowExW(0,cls.name,L"Unicode: \u00e9 \u20ac",0x10cf0000,180,100,700,300,0,0,0,0);check(root!=0,"window");H dc=GetDC(root);int size[2];check(dc&&GetTextExtentPoint32W(dc,sample,8,size),"Unicode metrics");say("M146_FONT_METRICS ");number((unsigned)size[0]);say(" ");number((unsigned)size[1]);say("\n");check(ReleaseDC(root,dc),"release metrics DC");RECT work;check(SystemParametersInfoW(0x30,0,&work,0)&&!work.left&&!work.top,"logical work area query");say("M146_WORK_AREA ");number((unsigned)work.right);say(" ");number((unsigned)work.bottom);say("\nM146_FONT_READY\n");MSG message;while(GetMessageW(&message,0,0,0)>0)DispatchMessageW(&message);say("M146_FONT_LIFETIME_PASS\n");ExitProcess(0);}
