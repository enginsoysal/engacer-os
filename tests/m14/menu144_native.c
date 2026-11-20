/* Owned menu semantics fixture; runs only inside Engacer OS. */
typedef unsigned long long H;
typedef unsigned short W;
typedef struct {unsigned size,mask,type,state,id,pad;H submenu,checked,unchecked,data;W*text;unsigned length,pad2;H bitmap;} INFO;
__declspec(dllimport) H CreateMenu(void);
typedef long long I;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned char flags,pad;W key,command;} ACCEL;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) H LoadAcceleratorsW(H,const W*);
__declspec(dllimport) H CreateAcceleratorTableW(const ACCEL*,int);
__declspec(dllimport) int CopyAcceleratorTableW(H,ACCEL*,int);
__declspec(dllimport) int DestroyAcceleratorTable(H);
__declspec(dllimport) int TranslateAcceleratorW(H,H,const MSG*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I SetWindowLongPtrW(H,int,I);
__declspec(dllimport) I CallWindowProcW(PROC,H,unsigned,H,I);
__declspec(dllimport) int DestroyWindow(H);

__declspec(dllimport) H LoadLibraryW(const W*);
__declspec(dllimport) int FreeLibrary(H);
__declspec(dllimport) H LoadMenuW(H,const W*);
__declspec(dllimport) H CreatePopupMenu(void);
__declspec(dllimport) int IsMenu(H);
__declspec(dllimport) int AppendMenuW(H,unsigned,H,const W*);
__declspec(dllimport) int InsertMenuItemW(H,unsigned,int,const INFO*);
__declspec(dllimport) int GetMenuItemInfoW(H,unsigned,int,INFO*);
__declspec(dllimport) int SetMenuItemInfoW(H,unsigned,int,const INFO*);
__declspec(dllimport) int GetMenuItemCount(H);
__declspec(dllimport) H GetSubMenu(H,int);
__declspec(dllimport) unsigned GetMenuItemID(H,int);
__declspec(dllimport) unsigned CheckMenuItem(H,unsigned,unsigned);
__declspec(dllimport) unsigned EnableMenuItem(H,unsigned,unsigned);
__declspec(dllimport) int RemoveMenu(H,unsigned,unsigned);
__declspec(dllimport) int DestroyMenu(H);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*why){if(!ok){say("M144_MENU_FAIL ");say(why);say("\n");ExitProcess(1);}}
static void(*volatile anchor)(const char*)=say;
static H received_command;static PROC previous_proc;
static I command_proc(H h,unsigned m,H wp,I lp){if(m==0x111){received_command=wp;return 0;}return CallWindowProcW(previous_proc,h,m,wp,lp);}
void entry(void){
 anchor("");H module=LoadLibraryW(L"menus144.dll");check(module!=0,"resource DLL");
 H loaded_accel=LoadAcceleratorsW(module,(const W*)1);ACCEL actual[2];check(loaded_accel&&LoadAcceleratorsW(module,(const W*)1)==loaded_accel&&CopyAcceleratorTableW(loaded_accel,0,0)==2&&CopyAcceleratorTableW(loaded_accel,actual,2)==2&&actual[0].key==0x75&&actual[0].command==77&&actual[1].flags==0&&actual[1].key=='g',"actual accelerator resource and shared identity");
 H command_window=CreateWindowExW(0,L"Static",L"Accelerator fixture",0,0,0,100,100,0,0,0,0);check(command_window!=0,"original accelerator command target");previous_proc=(PROC)SetWindowLongPtrW(command_window,-4,(I)command_proc);check(previous_proc!=0,"actual command subclass");ACCEL table[2]={{1,0,'Q',12},{9,0,'X',13}};H owned_accel=CreateAcceleratorTableW(table,2);check(owned_accel&&CopyAcceleratorTableW(owned_accel,actual,1)==1&&actual[0].key=='Q',"created table copy bound");MSG message={0};message.message=0x100;message.wp='Q';check(TranslateAcceleratorW(command_window,owned_accel,&message)&&received_command==0x1000c,"actual CPL3 accelerator command");message.wp='X';check(!TranslateAcceleratorW(command_window,owned_accel,&message),"required modifier absent");message.private_=0x800;check(TranslateAcceleratorW(command_window,owned_accel,&message)&&received_command==0x1000d,"explicit modifier context match");check(DestroyWindow(command_window)&&DestroyAcceleratorTable(owned_accel)&&!CopyAcceleratorTableW(owned_accel,0,0)&&GetLastError()==6,"owned table stale handle");
 H extended=LoadMenuW(module,(const W*)1),standard=LoadMenuW(module,(const W*)2);check(extended&&standard,"both resource versions");H nested=GetSubMenu(extended,0);check(nested&&GetMenuItemCount(nested)==2&&GetMenuItemID(nested,0)==41&&GetMenuItemID(nested,1)==42,"extended resource tree");check(GetMenuItemID(standard,0)==81,"standard resource ID");check(!LoadMenuW(module,(const W*)3)&&GetLastError()==1812,"truncated resource rejected");check(FreeLibrary(module)&&CopyAcceleratorTableW(loaded_accel,0,0)==2&&GetMenuItemCount(nested)==2,"copied menu outlives resource module");DestroyMenu(extended);DestroyMenu(standard);
 H root=CreateMenu(),sub=CreatePopupMenu();check(root&&sub&&root!=sub,"opaque handles");
 check(AppendMenuW(sub,0,41,L"Open")&&AppendMenuW(sub,0,42,L"Close"),"append commands");
 check(AppendMenuW(root,0x10,sub,L"&File")&&GetSubMenu(root,0)==sub,"submenu association");
 check(GetMenuItemCount(root)==1&&GetMenuItemCount(sub)==2&&GetMenuItemID(sub,1)==42&&GetMenuItemID(root,0)==~0u,"counts and IDs");
 INFO item={0};item.size=sizeof(item);item.mask=0x43;check(GetMenuItemInfoW(root,41,0,&item)&&item.length==4&&item.id==41,"recursive command lookup and size");
 W text[4];item.text=text;item.length=4;check(GetMenuItemInfoW(root,41,0,&item)&&item.length==3&&text[0]=='O'&&text[2]=='e'&&!text[3],"bounded label copy");
 item.mask=0x61;item.text=L"Changed";item.data=0x123456789abcULL;item.state=8;check(SetMenuItemInfoW(root,41,0,&item),"state label data change");
 item.mask=0x61;item.text=0;check(GetMenuItemInfoW(sub,0,1,&item)&&item.length==7&&item.state==8&&item.data==0x123456789abcULL,"state returned");
 check(CheckMenuItem(root,41,0)==8&&CheckMenuItem(sub,0,0x408)==0,"check state transitions");
 check(EnableMenuItem(root,41,3)==0&&EnableMenuItem(sub,0,0x400)==3,"enable state transitions");
 item.mask=4;item.submenu=root;check(!SetMenuItemInfoW(sub,0,1,&item)&&GetLastError()==87,"cycle refused");
 item.mask=0x42;item.text=L"First";item.id=40;check(InsertMenuItemW(sub,0,1,&item)&&GetMenuItemID(sub,0)==40,"positional insertion");
 check(RemoveMenu(root,0,0x400)&&IsMenu(sub)&&GetMenuItemCount(root)==0,"remove preserves submenu");
 check(DestroyMenu(root)&&!IsMenu(root)&&DestroyMenu(sub)&&!IsMenu(sub),"lifetime and stale handles");
 H next=CreateMenu();check(next&&next!=root&&next!=sub,"non-reused generation");DestroyMenu(next);
 say("M144_MENU_STATE_PASS\n");ExitProcess(0);
}
