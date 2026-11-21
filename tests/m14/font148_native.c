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
__declspec(dllimport) int64_t SendMessageW(H,unsigned,uint64_t,int64_t);
__declspec(dllimport) int DestroyIcon(H);
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
__declspec(dllimport) unsigned GdiplusStartup(uint64_t*,const void*,void*);
__declspec(dllimport) void GdiplusShutdown(uint64_t);
__declspec(dllimport) unsigned GdipCreateFromHDC(H,void**);
__declspec(dllimport) unsigned GdipGraphicsClear(void*,unsigned);
__declspec(dllimport) unsigned GdipDeleteGraphics(void*);
__declspec(dllimport) unsigned GdipCreateSolidFill(unsigned,void**);
__declspec(dllimport) unsigned GdipDeleteBrush(void*);
__declspec(dllimport) unsigned GdipFillRectangleI(void*,void*,int,int,int,int);
__declspec(dllimport) unsigned GdipCreateBitmapFromScan0(int,int,int,unsigned,void*,void**);
__declspec(dllimport) unsigned GdipDrawImageI(void*,void*,int,int);
__declspec(dllimport) unsigned GdipDisposeImage(void*);
static uint32_t image_pixels148[80*60];
static H small,big,shield_button148;static unsigned paints;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int ok){if(!ok){say("M148_FONT_RASTER_FAIL\n");ExitProcess(1);}}
static int64_t procedure(H h,unsigned msg,uint64_t wp,int64_t lp){
 if(msg==15){PAINT paint;H dc=BeginPaint(h,&paint);check(dc!=0);check(FillRect(dc,&paint.rect,16));void*graphics=0;check(!GdipCreateFromHDC(dc,&graphics)&&graphics);check(!GdipGraphicsClear(graphics,0xffffffff));for(unsigned i=0;i<80*60;++i)image_pixels148[i]=i%80<40?0x80008000u:0xff0000ffu;void*image=0;check(!GdipCreateBitmapFromScan0(80,60,320,0xe200b,image_pixels148,&image)&&image&&!GdipDrawImageI(graphics,image,450,140)&&!GdipDisposeImage(image));for(unsigned i=0;i<80*60;++i)image_pixels148[i]=0xff000000;void*brush=0;check(!GdipCreateSolidFill(0xffff0000,&brush)&&brush&&!GdipFillRectangleI(graphics,brush,450,210,100,40)&&!GdipDeleteBrush(brush)&&!GdipDeleteGraphics(graphics));check(SetBkMode(dc,1));H old=SelectObject(dc,small);check(old!=0);SetTextColor(dc,0xff0000);check(TextOutW(dc,30,30,L"Native glyphs WWW iii",20));check(SelectObject(dc,big)==small);SetTextColor(dc,0x0000ff);check(TextOutW(dc,30,95,L"Native glyphs WWW iii",20));check(SelectObject(dc,old)==big);check(EndPaint(h,&paint));++paints;say("M148_FONT_RASTER_WAITING\n");return 0;}
 if(msg==0x102&&wp=='a'){H old=(H)SendMessageW(shield_button148,0x160c,0,0);check(old&&DestroyIcon(old));say("M148_SHIELD_CLEARED\n");return 0;}
 if(msg==2){PostQuitMessage(0);return 0;}return DefWindowProcW(h,msg,wp,lp);
}
static PROC volatile relocation=procedure;
void entry(void){struct{unsigned version,pad;uint64_t callback;int suppress_thread,suppress_codecs;} input={1,0,0,0,0};uint64_t token=0;check(!GdiplusStartup(&token,&input,0)&&token);FONT f={0};f.height=-14;f.weight=400;small=CreateFontIndirectW(&f);f.height=-28;f.weight=600;f.underline=1;big=CreateFontIndirectW(&f);check(small&&big);CLASS c={0};c.proc=relocation;c.name=L"EngacerFontRaster148";check(RegisterClassW(&c));H h=CreateWindowExW(0,c.name,L"Real native Inter glyphs: 14 and 28 pixels",0x10cf0000,180,120,700,350,0,0,0,0);check(h!=0);shield_button148=CreateWindowExW(0,L"Button",L"Approve",0x50000000,30,180,180,40,h,71,0,0);check(shield_button148!=0);SendMessageW(shield_button148,0x160c,0,1);MSG m;int state;while((state=GetMessageW(&m,0,0,0))>0){TranslateMessage(&m);DispatchMessageW(&m);}check(state==0&&paints&&DeleteObject(small)&&DeleteObject(big));GdiplusShutdown(token);say("M148_FONT_RASTER_LIFETIME_PASS\n");ExitProcess(0);}
