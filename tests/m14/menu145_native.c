/* Owned real-menu/input/callback/coordinate fixture, not an original app. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
typedef struct {int left,top,right,bottom;} RECT;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) H CreateMenu(void);
__declspec(dllimport) H CreatePopupMenu(void);
__declspec(dllimport) int AppendMenuW(H,unsigned,H,const W*);
__declspec(dllimport) int SetMenu(H,H);
__declspec(dllimport) H GetMenu(H);
__declspec(dllimport) int DrawMenuBar(H);
__declspec(dllimport) unsigned EnableMenuItem(H,unsigned,unsigned);
__declspec(dllimport) int GetClientRect(H,RECT*);
__declspec(dllimport) int GetWindowRect(H,RECT*);
__declspec(dllimport) int ClientToScreen(H,void*);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static H root,file_menu;static unsigned commands,nested,entered,exited,initialized,uninitialized;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int ok,const char*s){if(!ok){say("M145_MENU_FAIL ");say(s);say("\n");ExitProcess(1);}}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==0x211){++entered;return 0;}if(m==0x212){++exited;say("M145_MENU_EXIT\n");return 0;}
 if(m==0x117){++initialized;EnableMenuItem(file_menu,203,3);return 0;}if(m==0x125){++uninitialized;return 0;}
 if(m==0x111){check(lp==0,"menu command source");if((wp&65535)==201){++commands;say("M145_MENU_ACCEPT\n");}else if((wp&65535)==301){++nested;say("M145_MENU_NESTED\n");}else check(0,"disabled or unknown menu command");return 0;}
 if(m==2){check(commands&&nested&&entered==exited&&initialized==uninitialized,"menu callback balance and real commands");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){CLASS cls={0};cls.proc=anchor;cls.name=L"Menu145";check(RegisterClassW(&cls)!=0,"class");root=CreateWindowExW(0,cls.name,L"Native application menus",0x10cf0000,180,100,560,360,0,0,0,0);check(root!=0,"root");RECT before,after;check(GetClientRect(root,&before),"initial client");
 H menu=CreateMenu();file_menu=CreatePopupMenu();H sub=CreatePopupMenu();check(menu&&file_menu&&sub,"menus");check(AppendMenuW(sub,0,301,L"Nested command"),"nested item");
 check(AppendMenuW(file_menu,0,201,L"&Enabled command")&&AppendMenuW(file_menu,3,203,L"Disabled command")&&AppendMenuW(file_menu,0x10,sub,L"More")&&AppendMenuW(menu,0x10,file_menu,L"&File"),"menu tree");
 check(SetMenu(root,menu)&&GetMenu(root)==menu&&DrawMenuBar(root),"attach/paint");check(GetClientRect(root,&after)&&before.bottom-after.bottom==24&&before.right==after.right,"menu reserves client height");int origin[2]={0,0};check(ClientToScreen(root,origin)&&origin[0]==181&&origin[1]==164,"client origin below menu");
 H child=CreateWindowExW(0,L"Static",L"Client content stays below its menu",0x50000000,10,12,380,24,root,10,0,0);RECT bounds;check(child&&GetWindowRect(child,&bounds)&&bounds.left==191&&bounds.top==176,"child screen origin");
 say("M145_MENU_READY\n");MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);say("M145_MENU_LIFETIME_PASS\n");ExitProcess(0);}
