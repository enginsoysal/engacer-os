/* Owned control registration, geometry and state fixture. */
typedef unsigned long long H;
typedef long long I64;
typedef unsigned short W;
typedef I64(*PROC)(H,unsigned,H,I64);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {int left,top,right,bottom;} RECT;
__declspec(dllimport) int InitCommonControlsEx(const unsigned*);
__declspec(dllimport) H SHGetFileInfoW(const W*,unsigned,void*,unsigned,unsigned);
__declspec(dllimport) int ImageList_GetImageCount(H);
__declspec(dllimport) int DestroyIcon(H);
__declspec(dllimport) H CreateToolbarEx(H,unsigned,unsigned,int,H,unsigned,const void*,int,int,int,int,int,unsigned);
__declspec(dllimport) H CreateStatusWindowW(unsigned,const W*,H,unsigned);
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
__declspec(dllimport) H GetParent(H);
__declspec(dllimport) H GetFocus(void);
__declspec(dllimport) H SetFocus(H);
__declspec(dllimport) H GetCapture(void);
__declspec(dllimport) H SetCapture(H);
__declspec(dllimport) int ReleaseCapture(void);
__declspec(dllimport) int EnableWindow(H,int);
__declspec(dllimport) int IsWindowEnabled(H);
__declspec(dllimport) int ShowWindow(H,int);
__declspec(dllimport) int IsZoomed(H);
__declspec(dllimport) int GetWindowPlacement(H,void*);
__declspec(dllimport) int SetWindowPlacement(H,const void*);
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
static H sorting_list;static unsigned comparisons;
static int compare_rows(I64 first,I64 second,I64 data){check(data==0xabc&&SendMessageW(sorting_list,0x1004,0,0)==3,"original comparator context and query");if(!comparisons++)check(!SendMessageW(sorting_list,0x1009,0,0)&&GetLastError()==87,"sort mutation refused");return first<second?-1:first>second?1:0;}
void entry(void){
 const unsigned classes[2]={8,0xff};check(InitCommonControlsEx(classes),"actual class registration");CLASS definition={0};definition.proc=anchor;definition.name=L"Controls144Root";check(RegisterClassW(&definition),"root class");H root=CreateWindowExW(0,definition.name,L"Control API fixture",0xcf0000,180,120,700,430,0,0,0,0);check(root!=0,"root create");RECT rect;check(GetClientRect(root,&rect)&&rect.right==698&&rect.bottom==389,"logical client bounds");
 H child=CreateWindowExW(0,L"Static",L"actual child",0x40000000,10,20,100,40,root,7,0,0);check(child!=0&&GetDlgItem(root,7)==child,"standard child lookup");check(GetWindowRect(child,&rect)&&rect.left==191&&rect.top==180&&rect.right==291&&rect.bottom==220,"child to screen bounds");int point[2]={0,0};check(ClientToScreen(child,point)&&point[0]==191&&point[1]==180,"client to screen");check(ScreenToClient(child,point)&&point[0]==0&&point[1]==0,"screen to client");check(MoveWindow(child,30,40,110,50,1),"move child");check(GetWindowRect(child,&rect)&&rect.left==211&&rect.top==200,"child geometry persisted");check(!EnableWindow(child,0)&&!IsWindowEnabled(child),"disable child");check(EnableWindow(child,1)&&IsWindowEnabled(child),"enable child");
 H edit=CreateWindowExW(0,L"Edit",L"",0x40000000,10,70,200,30,root,8,0,0);check(edit!=0,"edit create");check(SetWindowTextW(edit,L"Actual edit text"),"edit text mutation");W text[64];check(GetWindowTextLengthW(edit)==16&&GetWindowTextW(edit,text,64)==16&&text[0]=='A'&&text[15]=='t'&&text[16]==0,"edit text returned by its procedure");SendMessageW(edit,0xb1,2,7);unsigned first=0,last=0;check(SendMessageW(edit,0xb0,(H)&first,(I64)&last)==0x70002&&first==2&&last==7,"edit selection state");
 H status=CreateWindowExW(0,L"msctls_statusbar32",L"",0x40000000,0,330,600,24,root,9,0,0);check(status!=0,"status create");const int edges[3]={100,200,-1};check(SendMessageW(status,0x404,3,(I64)edges)==1&&SendMessageW(status,0x406,0,0)==3,"status parts");check(SendMessageW(status,0x40b,1,(I64)L"Actual status")==1,"status text");check(SendMessageW(status,0x40d,1,(I64)text)==13&&text[0]=='A'&&text[12]=='s'&&text[13]==0,"status text retrieved");

 H toolbar=CreateWindowExW(0,L"ToolbarWindow32",L"",0x40000000,0,0,200,30,root,10,0,0);check(toolbar!=0,"toolbar create");struct{int bitmap,command;unsigned char state,style,reserved[6];H data;I64 string;}button={0};button.command=91;button.state=4;W label[]=L"Copied";button.string=(I64)label;SendMessageW(toolbar,0x41e,32,0);check(SendMessageW(toolbar,0x444,1,(I64)&button)==1,"toolbar insert");label[0]='X';check(SendMessageW(toolbar,0x418,0,0)==1,"toolbar count");check(SendMessageW(toolbar,0x417,0,(I64)&button)&&((W*)button.string)[0]=='C',"toolbar copied label");check(SendMessageW(toolbar,0x401,91,0)&&SendMessageW(toolbar,0x412,91,0)==0,"toolbar disable");int size[2];check(SendMessageW(toolbar,0x453,0,(I64)size)&&size[0]>=48&&size[1]>=24,"toolbar measured content");
 H list=CreateWindowExW(0,L"SysListView32",L"",0x40000000,0,0,300,200,root,11,0,0);check(list!=0,"list create");struct{unsigned mask;int item,subitem;unsigned state,state_mask,pad;W*text;int capacity,image;I64 parameter;int indent,group;unsigned columns,pad2;unsigned*column_ids;int*formats;int group_index,pad3;}row={0};row.mask=15;row.text=L"Actual row";row.image=3;row.parameter=0x123456789abcLL;row.state=3;row.state_mask=3;check(SendMessageW(list,0x104d,0,(I64)&row)==0,"list insert");check(SendMessageW(list,0x1004,0,0)==1&&SendMessageW(list,0x1032,0,0)==1,"list count selected");row.text=text;row.capacity=64;check(SendMessageW(list,0x104b,0,(I64)&row)&&text[0]=='A'&&text[9]=='w'&&!text[10]&&row.parameter==0x123456789abcLL&&row.image==3,"list actual row data");row.mask=1;row.item=0;row.subitem=1;row.text=L"Second cell";check(SendMessageW(list,0x104c,0,(I64)&row),"subitem mutation");row.text=text;check(SendMessageW(list,0x104b,0,(I64)&row)&&text[0]=='S',"subitem retained");check(SendMessageW(list,0x1009,0,0)&&SendMessageW(list,0x1004,0,0)==0,"list teardown");


 check(SendMessageW(list,0x102f,3,0)&&SendMessageW(list,0x1004,0,0)==0,"non-owner count hint preserves row count");struct{unsigned mask;int format,width,pad;W*text;int capacity,subitem,image,order,min_width,default_width,ideal_width,pad2;}column={0};column.mask=0x2f;column.text=L"Column";for(unsigned n=0;n<3;++n){column.order=(int)n;column.subitem=(int)n;column.width=100+(int)n*20;check(SendMessageW(list,0x1061,n,(I64)&column)==n,"real column insertion");}int ordering[3]={2,0,1},got_order[3]={0};check(SendMessageW(list,0x1039,3,(I64)ordering)&&SendMessageW(list,0x103a,3,(I64)got_order)&&got_order[0]==2&&got_order[1]==0&&got_order[2]==1,"column permutation");column.mask=0x22;check(SendMessageW(list,0x105f,2,(I64)&column)&&column.order==0&&column.width==140,"column data retrieval");int invalid_order[3]={1,1,2};check(!SendMessageW(list,0x1039,3,(I64)invalid_order)&&GetLastError()==87,"duplicate permutation refused");column.mask=32;column.order=2;check(SendMessageW(list,0x1060,0,(I64)&column)&&SendMessageW(list,0x103a,3,(I64)got_order)&&got_order[0]==2&&got_order[1]==1&&got_order[2]==0,"individual column order mutation");check(SendMessageW(list,0x101c,0,0)&&SendMessageW(list,0x103a,2,(I64)got_order)&&got_order[0]==1&&got_order[1]==0,"deleted column order reflow");
 const I64 params[3]={30,10,20};for(unsigned n=0;n<3;++n){row.mask=5;row.item=(int)n;row.subitem=0;row.text=L"Sortable";row.parameter=params[n];check(SendMessageW(list,0x104d,0,(I64)&row)==n,"sortable row insert");}sorting_list=list;check(SendMessageW(list,0x1030,0xabc,(I64)compare_rows)&&comparisons>=2,"actual CPL3 comparator execution");for(unsigned n=0;n<3;++n){row.mask=4;row.item=(int)n;check(SendMessageW(list,0x104b,0,(I64)&row)&&row.parameter==(I64)(n+1)*10,"actual sorted row order");}check(SendMessageW(list,0x1009,0,0),"sorted row teardown");
 H combo=CreateWindowExW(0,L"ComboBoxEx32",L"",0x40000002,10,120,250,620,root,12,0,0);check(combo!=0,"composite combo create");H combo_child=(H)SendMessageW(combo,0x406,0,0),combo_edit=(H)SendMessageW(combo,0x407,0,0);check(combo_child&&combo_edit&&GetParent(combo_child)==combo&&GetParent(combo_edit)==combo_child,"real combo/edit child chain");check(GetWindowRect(combo,&rect)&&rect.bottom-rect.top==24,"closed combo height");check(SetWindowTextW(combo,L"Actual path")&&GetWindowTextW(combo_edit,text,64)==11&&text[0]=='A',"combo forwards editable text");struct{unsigned mask,pad;I64 index;W*text;int capacity,image,selected_image,overlay,indent,pad2;I64 data;}combo_item={0};combo_item.mask=33;combo_item.index=-1;combo_item.text=L"Chosen path";combo_item.data=0x1234abcd;check(SendMessageW(combo,0x40b,0,(I64)&combo_item)==0,"combo item insert");check(SendMessageW(combo,0x146,0,0)==1&&SendMessageW(combo,0x14e,0,0)==0&&GetWindowTextW(combo_edit,text,64)==11&&text[0]=='C'&&SendMessageW(combo,0x150,0,0)==0x1234abcd,"combo real selection and item data");
 H rebar=CreateWindowExW(0,L"ReBarWindow32",L"",0x40000000,0,0,400,0,root,13,0,0);check(rebar!=0,"rebar create");struct{unsigned size,mask,style,foreground,background,pad;W*text;unsigned capacity;int image;H child;unsigned min_width,min_height,width,pad2;H bitmap;unsigned id,height,max_height,integral,ideal,pad3;I64 data;unsigned header;int chevron[4];unsigned chevron_state;}band={0};band.size=sizeof(band);band.mask=0x71;band.child=toolbar;band.min_width=80;band.min_height=28;band.width=100;band.height=28;check(SendMessageW(rebar,0x40a,(H)-1,(I64)&band)==1&&GetParent(toolbar)==rebar,"rebar real child parenting");check(SendMessageW(rebar,0x40c,0,0)==1&&SendMessageW(rebar,0x41b,0,0)>=28,"rebar retained layout");check(SendMessageW(rebar,0x402,0,0)&&SendMessageW(rebar,0x40c,0,0)==0&&GetParent(toolbar)==rebar,"remove band preserves child");
 check(!GetFocus()&&!SetFocus(combo_edit)&&GetFocus()==combo_edit,"real per-thread focus");check(SetFocus(edit)==combo_edit&&GetFocus()==edit,"focus transfer");check(!GetCapture()&&!SetCapture(edit)&&GetCapture()==edit&&ReleaseCapture()&&!GetCapture(),"capture lifetime");check(SetFocus(0)==edit&&!GetFocus(),"focus clear");
 int overflow_point[2]={0x7fffffff,0};check(!ClientToScreen(child,overflow_point)&&overflow_point[0]==0x7fffffff&&overflow_point[1]==0&&GetLastError()==87,"coordinate overflow transactional refusal");

 struct{H icon;int index;unsigned attributes;W name[260],type[80];}shell_info={0};H shell_images=SHGetFileInfoW(L"__DIR__",16,&shell_info,sizeof(shell_info),0x4411);check(shell_images&&shell_info.index==1&&ImageList_GetImageCount(shell_images)==2&&shell_info.type[0]=='F',"own actual generic system image list");check(SHGetFileInfoW(L"file.txt",0,&shell_info,sizeof(shell_info),0x111)&&shell_info.icon&&shell_info.index==0&&DestroyIcon(shell_info.icon),"owned generic file icon");check(!SHGetFileInfoW(L"__DIR__",16,&shell_info,sizeof(shell_info),0x4018)&&GetLastError()==50,"unsupported PIDL query typed refusal");
 button.bitmap=8;button.command=92;button.state=4;button.string=0;H stock_toolbar=CreateToolbarEx(root,0x40000000,14,11,(H)-1,4,&button,1,0,0,0,0,32);check(stock_toolbar!=0,"stock view toolbar creation");H stock_images=(H)SendMessageW(stock_toolbar,0x431,0,0);check(stock_images&&ImageList_GetImageCount(stock_images)==11&&SendMessageW(stock_toolbar,0x418,0,0)==1,"actual stock toolbar images and button");check(DestroyWindow(stock_toolbar)&&ImageList_GetImageCount(stock_images)==0,"stock toolbar owned image teardown");H made_status=CreateStatusWindowW(0x40000000,L"Status wrapper",root,15);check(made_status&&GetParent(made_status)==root,"actual status wrapper window");
 RECT work;check(SystemParametersInfoW(0x30,0,&work,0)&&work.left==0&&work.top==0&&work.right>=1024&&work.bottom>600,"actual native work area");struct{unsigned size;RECT screen,work;unsigned flags;}monitor={0};monitor.size=40;check(GetMonitorInfoA(MonitorFromWindow(root,2),&monitor)&&monitor.flags==1&&monitor.work.right==work.right&&monitor.work.bottom==work.bottom,"actual monitor");unsigned units=GetDialogBaseUnits();check((units&65535)>0&&(units>>16)==16,"native base font metrics");
 H arrow=LoadCursorW(0,(const W*)32512),resize=LoadCursorW(0,(const W*)32644);check(arrow&&resize,"native cursor handles");SetCursor(arrow);check(SetCursor(resize)==arrow,"native cursor state");check(SetCursor(arrow)==resize,"native cursor restored");
 ShowWindow(root,1);check(ShowWindow(root,2),"minimize previous visibility");check(GetClientRect(root,&rect)&&!rect.right&&!rect.bottom,"minimized client size");ShowWindow(root,1);check(GetClientRect(root,&rect)&&rect.right==698&&rect.bottom==389,"restored client size");ShowWindow(root,0);ShowWindow(root,1);struct{unsigned length,flags,show;int min_x,min_y,max_x,max_y;RECT normal;}placement={0};placement.length=44;check(GetWindowPlacement(root,&placement)&&placement.normal.left==180&&placement.normal.top==120&&placement.normal.right==880&&placement.normal.bottom==550,"actual normal placement");ShowWindow(root,3);check(IsZoomed(root)&&GetWindowRect(root,&rect)&&rect.left==0&&rect.top==0&&rect.right==work.right&&rect.bottom==work.bottom,"actual maximized work area");ShowWindow(root,2);ShowWindow(root,9);check(IsZoomed(root),"minimized-maximized restore state");ShowWindow(root,1);check(!IsZoomed(root)&&GetWindowRect(root,&rect)&&rect.left==180&&rect.right==880,"normal restore");placement.normal=(RECT){280,200,920,620};placement.show=1;check(SetWindowPlacement(root,&placement)&&GetWindowRect(root,&rect)&&rect.left==280&&rect.top==200&&rect.right==920&&rect.bottom==620,"placement applies actual geometry");placement.flags=1;check(!SetWindowPlacement(root,&placement)&&GetLastError()==50,"unsupported minimum-position flag refused");placement.flags=2;placement.show=2;check(SetWindowPlacement(root,&placement),"explicit restore-to-maximized input");check(GetWindowPlacement(root,&placement)&&placement.flags==0&&placement.show==2,"placement output flags remain zero");ShowWindow(root,9);check(IsZoomed(root),"explicit minimized restore intent");ShowWindow(root,1);placement.show=1;placement.normal.right=100;check(!SetWindowPlacement(root,&placement)&&GetLastError()==87&&GetWindowRect(root,&rect)&&rect.left==280&&rect.right==920,"bad placement rejected");check(DestroyWindow(root),"recursive control destruction");say("M144_CONTROLS_GEOMETRY_PASS\n");ExitProcess(0);
}

void*memset(void*out,int value,unsigned long long count){unsigned char*p=out;for(unsigned long long i=0;i<count;++i)p[i]=(unsigned char)value;return out;}
