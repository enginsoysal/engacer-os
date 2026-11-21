/* Owned real GDI raster/lifetime task, separate from original-app acceptance. */
#include <stdint.h>
typedef uint64_t H;typedef uint16_t W;typedef int64_t(*PROC)(H,unsigned,uint64_t,int64_t);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;uint64_t wp;int64_t lp;unsigned time;int x,y;unsigned private_;} MSG;
typedef struct {int left,top,right,bottom;} RECT;
typedef struct {H dc;int erase;RECT rect;int restore,increment;uint8_t reserved[32];unsigned pad;} PAINT;
typedef struct {int height,width,escapement,orientation,weight;uint8_t italic,underline,strike,charset,out_precision,clip_precision,quality,pitch;W face[32];} FONT;
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) int64_t DefWindowProcW(H,unsigned,uint64_t,int64_t);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) int TranslateMessage(const MSG*);
__declspec(dllimport) int64_t DispatchMessageW(const MSG*);
__declspec(dllimport) H BeginPaint(H,PAINT*);
__declspec(dllimport) int EndPaint(H,const PAINT*);
__declspec(dllimport) int FillRect(H,const RECT*,H);
__declspec(dllimport) H CreateFontIndirectW(const FONT*);
__declspec(dllimport) H SelectObject(H,H);
__declspec(dllimport) int DeleteObject(H);
__declspec(dllimport) unsigned SetTextColor(H,unsigned);
__declspec(dllimport) int SetBkMode(H,int);
__declspec(dllimport) int TextOutW(H,int,int,const W*,int);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static H small,big;static unsigned paints;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int ok){if(!ok){say("M148_FONT_RASTER_FAIL\n");ExitProcess(1);}}
static int64_t procedure(H h,unsigned msg,uint64_t wp,int64_t lp){
 if(msg==15){PAINT paint;H dc=BeginPaint(h,&paint);check(dc!=0);check(FillRect(dc,&paint.rect,6));check(SetBkMode(dc,1));H old=SelectObject(dc,small);check(old!=0);SetTextColor(dc,0xff0000);check(TextOutW(dc,30,30,L"Native glyphs WWW iii",20));check(SelectObject(dc,big)==small);SetTextColor(dc,0x0000ff);check(TextOutW(dc,30,95,L"Native glyphs WWW iii",20));check(SelectObject(dc,old)==big);check(EndPaint(h,&paint));++paints;say("M148_FONT_RASTER_WAITING\n");return 0;}
 if(msg==2){PostQuitMessage(0);return 0;}return DefWindowProcW(h,msg,wp,lp);
}
static PROC volatile relocation=procedure;
void entry(void){FONT f={0};f.height=-14;f.weight=400;small=CreateFontIndirectW(&f);f.height=-28;f.weight=600;f.underline=1;big=CreateFontIndirectW(&f);check(small&&big);CLASS c={0};c.proc=relocation;c.name=L"EngacerFontRaster148";check(RegisterClassW(&c));H h=CreateWindowExW(0,c.name,L"Real native Inter glyphs: 14 and 28 pixels",0x10cf0000,180,120,700,350,0,0,0,0);check(h!=0);MSG m;int state;while((state=GetMessageW(&m,0,0,0))>0){TranslateMessage(&m);DispatchMessageW(&m);}check(state==0&&paints&&DeleteObject(small)&&DeleteObject(big));say("M148_FONT_RASTER_LIFETIME_PASS\n");ExitProcess(0);}
