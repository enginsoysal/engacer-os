/* Owned raster/toolbar fixture: expected pixels are checked outside the guest. */
typedef unsigned long long H;
typedef long long I;
typedef unsigned short W;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {int left,top,right,bottom;} RECT;
typedef struct {H dc;int erase;RECT rect;int restore,incremental;unsigned char reserved[32];} PAINT;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
typedef struct {int bitmap,command;unsigned char state,style,reserved[6];H data;I string;} BUTTON;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) H BeginPaint(H,PAINT*);
__declspec(dllimport) int EndPaint(H,const PAINT*);
__declspec(dllimport) int FillRect(H,const RECT*,H);
__declspec(dllimport) int TextOutW(H,int,int,const W*,int);
__declspec(dllimport) int DrawIconEx(H,int,int,H,int,int,unsigned,H,unsigned);
__declspec(dllimport) int ImageList_Draw(H,int,H,int,int,unsigned);
__declspec(dllimport) H ImageList_Create(int,int,unsigned,int,int);
__declspec(dllimport) int ImageList_ReplaceIcon(H,int,H);
__declspec(dllimport) int ImageList_Destroy(H);
__declspec(dllimport) H LoadLibraryW(const W*);
__declspec(dllimport) int FreeLibrary(H);
__declspec(dllimport) H LoadImageW(H,const W*,unsigned,int,int,unsigned);
__declspec(dllimport) int DestroyIcon(H);
__declspec(dllimport) I SendMessageW(H,unsigned,H,I);
__declspec(dllimport) H GetDC(H);
__declspec(dllimport) int GetClientRect(H,RECT*);
__declspec(dllimport) int ReleaseDC(H,H);
__declspec(dllimport) int GetTextExtentPoint32W(H,const W*,int,int*);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static H root,child,images,icon,resource;
static unsigned painted,commands;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int ok,const char*why){if(!ok){say("M145_RASTER_FAIL ");say(why);say("\n");ExitProcess(1);}}
static void number(unsigned value){char b[16];unsigned n=0;do{b[n++]=(char)('0'+value%10);value/=10;}while(value);while(n){char c=b[--n];unsigned written;WriteFile(GetStdHandle((unsigned)-11),&c,1,&written,0);}}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==15){PAINT p;H dc=BeginPaint(h,&p);check(dc!=0,"paint DC");check(FillRect(dc,&p.rect,14),"blue surface");
  if(h==child)check(DrawIconEx(dc,-2,0,icon,4,2,0,0,3),"signed child clip");
  else{check(DrawIconEx(dc,20,20,icon,0,0,0,0,3),"original icon pixels");check(DrawIconEx(dc,40,20,icon,8,4,0,0,3),"scaled icon pixels");check(ImageList_Draw(images,0,dc,72,20,1),"copied list pixels");check(!ImageList_Draw(images,0,dc,1,1,0x8000)&&GetLastError()==50,"unsupported flag refusal");check(!DrawIconEx(dc,1,1,icon,-1,4,0,0,3)&&GetLastError()==87,"invalid size refusal");RECT reference={20,180,120,196};check(FillRect(dc,&reference,6)&&TextOutW(dc,20,180,L"gjpqy",5),"independent short-label reference");++painted;}
  check(EndPaint(h,&p),"DC release");return 0;}
 if(m==0x111){check((wp&65535)==201,"disabled or separator invoked a command");++commands;say("M145_TOOLBAR_COMMAND_PASS\n");return 0;}
 if(m==2&&h==root){check(painted&&commands,"real painting and ordinary-input command");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){
 resource=LoadLibraryW(L"resources144.dll");check(resource!=0,"owned resource DLL");icon=LoadImageW(resource,(const W*)1,1,0,0,0);check(icon!=0,"resource icon");
 images=ImageList_Create(4,2,1,1,1);check(images&&ImageList_ReplaceIcon(images,-1,icon)==0,"copy image list");
 H stale=icon;check(DestroyIcon(icon),"release copied source");icon=LoadImageW(resource,(const W*)1,1,0,0,0);check(icon&&icon!=stale,"reload native-sized icon");
 CLASS cls={0};cls.proc=anchor;cls.name=L"Raster145";check(RegisterClassW(&cls)!=0,"class");
 root=CreateWindowExW(0,cls.name,L"Native image and measured toolbar",0x10cf0000,180,100,560,320,0,0,0,0);check(root!=0,"root");
 child=CreateWindowExW(0,cls.name,L"",0x50000000,100,20,2,8,root,90,0,0);check(child!=0,"clipped child");
 unsigned static_styles[4]={0x50000803,0x50000003,0x50000a03,0x50000843};int static_x[4]={200,220,270,320};
 for(unsigned n=0;n<4;++n){int width=n==3?8:40,height=n==3?4:40;H image_control=CreateWindowExW(0,L"Static",(const W*)1,static_styles[n],static_x[n],20,width,height,root,100+n,resource,0);RECT bounds;
  check(image_control&&GetClientRect(image_control,&bounds),"real static resource icon creation");
  check(bounds.right==(n==0?4:n==1?32:width)&&bounds.bottom==(n==0?2:n==1?32:height),"static native/default/center/stretch dimensions");
  H current=(H)SendMessageW(image_control,0x171,0,0);check(current!=0&&(H)SendMessageW(image_control,0x173,1,0)==current,"static image getter identity");
  if(n==0){check((H)SendMessageW(image_control,0x170,icon,0)==current,"static image replacement returns previous handle");check((H)SendMessageW(image_control,0x171,0,0)==icon,"static image replacement identity");}
 }
 H empty_icon=CreateWindowExW(0,L"Static",L"",0x50000803,380,20,40,40,root,110,resource,0);RECT empty_bounds;check(empty_icon&&!SendMessageW(empty_icon,0x171,0,0)&&GetClientRect(empty_icon,&empty_bounds)&&empty_bounds.right==40&&empty_bounds.bottom==40,"empty icon control does not load a resource");SendMessageW(empty_icon,0x172,1,(I)icon);check((H)SendMessageW(empty_icon,0x171,0,0)==icon&&GetClientRect(empty_icon,&empty_bounds)&&empty_bounds.right==4&&empty_bounds.bottom==2,"deferred icon assignment resizes");
 check(CreateWindowExW(0,L"Static",L"gjpqy",0x50000000,200,180,100,16,root,111,0,0)!=0,"short native label");
 H bar=CreateWindowExW(0,L"ToolbarWindow32",L"",0x50001000,10,80,500,64,root,77,0,0);check(bar!=0,"toolbar");SendMessageW(bar,0x41e,32,0);SendMessageW(bar,0x430,0,(I)images);
 BUTTON buttons[4]={{0}};const W*labels[4]={L"WWW",L"iii",L"",L"Longer measured title"};
 for(unsigned n=0;n<4;++n){buttons[n].bitmap=0;buttons[n].command=201+(int)n;buttons[n].state=n==1?0:4;buttons[n].style=n==2?1:16;buttons[n].string=(I)labels[n];}
 check(SendMessageW(bar,0x444,4,(I)buttons)==1,"toolbar insert");RECT a,b,by_command;check(SendMessageW(bar,0x41d,0,(I)&a)&&SendMessageW(bar,0x41d,1,(I)&b),"item rectangles");check(a.right<=b.left,"nonoverlap");check(SendMessageW(bar,0x433,201,(I)&by_command)&&by_command.left==a.left&&by_command.right==a.right,"command rectangle matches");
 H dc=GetDC(root);int wide[2],narrow[2];check(dc&&GetTextExtentPoint32W(dc,labels[0],3,wide)&&GetTextExtentPoint32W(dc,labels[1],3,narrow),"native metrics");check(wide[0]>narrow[0]&&a.right-a.left>=wide[0]+16&&a.right-a.left>b.right-b.left,"proportional font geometry");check(ReleaseDC(root,dc),"measure release");
 say("M145_BUTTON_CENTER ");number((unsigned)(10+(a.left+a.right)/2));say(" ");number((unsigned)(80+(a.top+a.bottom)/2));say("\nM145_DISABLED_CENTER ");number((unsigned)(10+(b.left+b.right)/2));say(" ");number((unsigned)(80+(b.top+b.bottom)/2));say("\nM145_RASTER_READY\n");
 MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);
 check(ImageList_Destroy(images)&&DestroyIcon(icon)&&FreeLibrary(resource),"image teardown");say("M145_RASTER_LIFETIME_PASS\n");ExitProcess(0);
}
