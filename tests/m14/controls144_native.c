/* Owned control registration, geometry and state fixture. */
typedef unsigned long long H;
typedef long long I64;
typedef unsigned short W;
typedef I64(*PROC)(H,unsigned,H,I64);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {int left,top,right,bottom;} RECT;
__declspec(dllimport) int InitCommonControlsEx(const unsigned*);
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I64 DefWindowProcW(H,unsigned,H,I64);
__declspec(dllimport) I64 SendMessageW(H,unsigned,H,I64);
__declspec(dllimport) int GetWindowRect(H,RECT*);
__declspec(dllimport) int GetClientRect(H,RECT*);
__declspec(dllimport) int ClientToScreen(H,int*);
__declspec(dllimport) int ScreenToClient(H,int*);
__declspec(dllimport) int MoveWindow(H,int,int,int,int,int);
__declspec(dllimport) H GetDlgItem(H,int);
__declspec(dllimport) int EnableWindow(H,int);
__declspec(dllimport) int IsWindowEnabled(H);
__declspec(dllimport) int ShowWindow(H,int);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) int SetWindowTextW(H,const W*);
__declspec(dllimport) int GetWindowTextW(H,W*,int);
__declspec(dllimport) int GetWindowTextLengthW(H);
__declspec(dllimport) unsigned GetDialogBaseUnits(void);
__declspec(dllimport) int SystemParametersInfoW(unsigned,unsigned,void*,unsigned);
__declspec(dllimport) H MonitorFromWindow(H,unsigned);
__declspec(dllimport) int GetMonitorInfoA(H,void*);
__declspec(dllimport) H LoadCursorW(H,const W*);
__declspec(dllimport) H SetCursor(H);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static I64 procedure(H window,unsigned message,H wp,I64 lp){return DefWindowProcW(window,message,wp,lp);}
static PROC volatile anchor=procedure;
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*message){if(!ok){say("M144_CONTROLS_FAIL ");say(message);say("\n");ExitProcess(1);}}
void entry(void){
 const unsigned classes[2]={8,0xff};check(InitCommonControlsEx(classes),"actual class registration");CLASS definition={0};definition.proc=anchor;definition.name=L"Controls144Root";check(RegisterClassW(&definition),"root class");H root=CreateWindowExW(0,definition.name,L"Control API fixture",0xcf0000,180,120,700,430,0,0,0,0);check(root!=0,"root create");RECT rect;check(GetClientRect(root,&rect)&&rect.right==698&&rect.bottom==389,"logical client bounds");
 H child=CreateWindowExW(0,L"Static",L"actual child",0x40000000,10,20,100,40,root,7,0,0);check(child!=0&&GetDlgItem(root,7)==child,"standard child lookup");check(GetWindowRect(child,&rect)&&rect.left==191&&rect.top==180&&rect.right==291&&rect.bottom==220,"child to screen bounds");int point[2]={0,0};check(ClientToScreen(child,point)&&point[0]==191&&point[1]==180,"client to screen");check(ScreenToClient(child,point)&&point[0]==0&&point[1]==0,"screen to client");check(MoveWindow(child,30,40,110,50,1),"move child");check(GetWindowRect(child,&rect)&&rect.left==211&&rect.top==200,"child geometry persisted");check(!EnableWindow(child,0)&&!IsWindowEnabled(child),"disable child");check(EnableWindow(child,1)&&IsWindowEnabled(child),"enable child");
 H edit=CreateWindowExW(0,L"Edit",L"",0x40000000,10,70,200,30,root,8,0,0);check(edit!=0,"edit create");check(SetWindowTextW(edit,L"Actual edit text"),"edit text mutation");W text[64];check(GetWindowTextLengthW(edit)==16&&GetWindowTextW(edit,text,64)==16&&text[0]=='A'&&text[15]=='t'&&text[16]==0,"edit text returned by its procedure");SendMessageW(edit,0xb1,2,7);unsigned first=0,last=0;check(SendMessageW(edit,0xb0,(H)&first,(I64)&last)==0x70002&&first==2&&last==7,"edit selection state");
 H status=CreateWindowExW(0,L"msctls_statusbar32",L"",0x40000000,0,330,600,24,root,9,0,0);check(status!=0,"status create");const int edges[3]={100,200,-1};check(SendMessageW(status,0x404,3,(I64)edges)==1&&SendMessageW(status,0x406,0,0)==3,"status parts");check(SendMessageW(status,0x40b,1,(I64)L"Actual status")==1,"status text");check(SendMessageW(status,0x40d,1,(I64)text)==13&&text[0]=='A'&&text[12]=='s'&&text[13]==0,"status text retrieved");
 RECT work;check(SystemParametersInfoW(0x30,0,&work,0)&&work.left==0&&work.top==0&&work.right>=1024&&work.bottom>600,"actual native work area");struct{unsigned size;RECT screen,work;unsigned flags;}monitor={0};monitor.size=40;check(GetMonitorInfoA(MonitorFromWindow(root,2),&monitor)&&monitor.flags==1&&monitor.work.right==work.right&&monitor.work.bottom==work.bottom,"actual monitor");unsigned units=GetDialogBaseUnits();check((units&65535)>0&&(units>>16)==16,"native base font metrics");
 H arrow=LoadCursorW(0,(const W*)32512),resize=LoadCursorW(0,(const W*)32644);check(arrow&&resize,"native cursor handles");SetCursor(arrow);check(SetCursor(resize)==arrow,"native cursor state");check(SetCursor(arrow)==resize,"native cursor restored");
 ShowWindow(root,1);check(ShowWindow(root,2),"minimize previous visibility");check(GetClientRect(root,&rect)&&!rect.right&&!rect.bottom,"minimized client size");ShowWindow(root,1);check(GetClientRect(root,&rect)&&rect.right==698&&rect.bottom==389,"restored client size");ShowWindow(root,0);ShowWindow(root,1);check(DestroyWindow(root),"recursive control destruction");say("M144_CONTROLS_GEOMETRY_PASS\n");ExitProcess(0);
}
