/* Owned selection/activation/veto/reentrant-model fixture. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
typedef struct {unsigned mask;int item,subitem;unsigned state,state_mask,pad;W*text;int capacity,image;I parameter;int indent,group;unsigned columns,pad2;unsigned*column_ids;int*formats;int group_index,pad3;} ITEM;
typedef struct {unsigned mask;int format,width,pad;W*text;int capacity,subitem,image,order,min_width,default_width,ideal_width,pad2;} COLUMN;
typedef struct {H window,id;unsigned code,pad;int item,subitem;unsigned next,old,changed;int x,y,pad2;I parameter;unsigned keys,pad3;} NOTICE;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) I SendMessageW(H,unsigned,H,I);
__declspec(dllimport) int SHGetSpecialFolderPathW(H,W*,int,int);
__declspec(dllimport) unsigned GetFileAttributesW(const W*);
__declspec(dllimport) int RemoveDirectoryW(const W*);
__declspec(dllimport) H FindFirstChangeNotificationW(const W*,int,unsigned);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) H SHGetFileInfoW(const W*,unsigned,void*,unsigned,unsigned);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static H root,list;static unsigned activated,changed,armed,mutated,safe,text_calls,cache_text,replace_text;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int ok,const char*s){if(!ok){say("M145_LIST_FAIL ");say(s);say("\n");ExitProcess(1);}}
static void fill(unsigned base){const W*labels[3]={L"First folder",L"Selection veto",L"Last folder"};for(unsigned n=0;n<3;++n){ITEM item={0};item.mask=7;item.item=(int)n;item.text=(W*)labels[n];item.image=1;item.parameter=base+n;check(SendMessageW(list,0x104d,0,(I)&item)==(I)n,"insert original row");}}
static I procedure(H h,unsigned m,H wp,I lp){(void)wp;
 if(m==0x4e){NOTICE*n=(void*)lp;if(n->code==(unsigned)-177){ITEM*item=(void*)((unsigned char*)n+24);++text_calls;const W*value=item->subitem?L"Callback size":L"Callback name";unsigned at=0;while(at+1<(unsigned)item->capacity&&value[at]){item->text[at]=value[at];++at;}item->text[at]=0;if(cache_text)item->mask|=0x1000;if(replace_text){replace_text=0;SendMessageW(list,0x1009,0,0);fill(200);}return 0;}if(n->code==(unsigned)-155){unsigned key=*(W*)((unsigned char*)n+24);if(key=='R'){armed=1;say("M145_LIST_ARMED\n");}if(key=='V'){check(mutated&&SendMessageW(list,0x1032,0,0)==0,"no stale selection after callback replaced equal-sized model");safe=1;say("M145_LIST_REENTRANT_SAFE\n");}return 0;}
  if(n->code==(unsigned)-100){check(n->changed==8&&n->item>=0&&n->item<3,"changing ABI");if(armed){armed=0;mutated=1;SendMessageW(list,0x1009,0,0);fill(200);say("M145_LIST_MUTATED\n");return 0;}if(n->item==1&&(n->next&3)){say("M145_LIST_VETO\n");return 1;}return 0;}
  if(n->code==(unsigned)-101){++changed;return 0;}
  if(n->code==(unsigned)-2){if(!activated&&n->item==0){check(SendMessageW(list,0x1032,0,0)==1&&SendMessageW(list,0x102c,0,3)==3,"single click selects and focuses");say("M145_LIST_SELECT_ONLY\n");}if(n->item==1){check(SendMessageW(list,0x1032,0,0)==1&&SendMessageW(list,0x102c,0,3)==3,"veto preserves previous selection and still reports click");say("M145_LIST_VETO_PRESERVED\n");}return 0;}
  if(n->code==(unsigned)-114){check(!mutated&&n->parameter==100+n->item&&(n->item==0||n->item==2),"activation carries current row identity");++activated;say(activated==1?"M145_LIST_DOUBLE_ACTIVATE\n":"M145_LIST_ENTER_ACTIVATE\n");return 0;}
 }
 if(m==2){check(activated==2&&changed&&mutated&&safe,"real activation and reentrant lifetime checks");PostQuitMessage(0);return 0;}return DefWindowProcW(h,m,wp,lp);
}
static void text_checks(void){W buffer[80];ITEM get={0};get.subitem=1;get.text=buffer;get.capacity=80;unsigned before=text_calls;check(SendMessageW(list,0x1073,0,(I)&get)==13&&text_calls==before+1,"absent subitem requests actual parent text");cache_text=1;check(SendMessageW(list,0x1073,0,(I)&get)==13,"cache callback-supplied text");cache_text=0;before=text_calls;check(SendMessageW(list,0x1073,0,(I)&get)==13&&text_calls==before,"DI_SETITEM avoids repeated callbacks");ITEM set={0};set.subitem=1;set.text=L"";check(SendMessageW(list,0x1074,0,(I)&set),"set explicit empty subitem");check(SendMessageW(list,0x1073,0,(I)&get)==0&&!buffer[0]&&text_calls==before,"explicit empty suppresses default callback");replace_text=1;check(SendMessageW(list,0x1073,2,(I)&get)==0&&!replace_text,"callback model replacement cancels stale text result");SendMessageW(list,0x1009,0,0);fill(100);}
static void folders(void){W path[260],returned[260];check(SHGetSpecialFolderPathW(0,path,40,0),"real user profile");check(FindFirstChangeNotificationW(path,0,3)==~(H)0&&GetLastError()==50,"unsupported watch returns failure without inventing a handle");check(FindFirstChangeNotificationW(0,0,3)==~(H)0&&GetLastError()==87,"invalid watch input refused");unsigned n=0;while(path[n])++n;check(n+7<260,"fixture path capacity");const W*tail=L"\\Music";for(unsigned j=0;j<=6;++j)path[n+j]=tail[j];unsigned before=GetFileAttributesW(path);if(before==0xffffffffu){check(!SHGetSpecialFolderPathW(0,returned,13,0)&&GetFileAttributesW(path)==0xffffffffu,"false create flag leaves missing folder absent");check(SHGetSpecialFolderPathW(0,returned,13,1)&&GetFileAttributesW(path)!=0xffffffffu&&(GetFileAttributesW(path)&16),"true create flag creates actual granted folder");check(RemoveDirectoryW(path)&&GetFileAttributesW(path)==0xffffffffu,"remove only fixture-created folder");}else if(before&16)check(SHGetSpecialFolderPathW(0,returned,13,0),"existing physical user folder");}
static PROC volatile anchor=procedure;
void entry(void){folders();_Static_assert(sizeof(ITEM)==88,"LVITEMW");_Static_assert(sizeof(COLUMN)==56,"LVCOLUMNW");CLASS cls={0};cls.proc=anchor;cls.name=L"List145";check(RegisterClassW(&cls)!=0,"class");root=CreateWindowExW(0,cls.name,L"Native Windows list input",0x10cf0000,180,100,560,360,0,0,0,0);check(root!=0,"root");list=CreateWindowExW(0,L"SysListView32",L"",0x50800045,10,12,500,260,root,11,0,0);check(list!=0,"list");COLUMN column={0};column.mask=6;column.width=300;column.text=L"Name";check(SendMessageW(list,0x1061,0,(I)&column)==0,"column");column.text=L"Size";column.width=140;check(SendMessageW(list,0x1061,1,(I)&column)==1,"size column");struct{H icon;int index;unsigned attributes;W name[260],type[80];}info;info.icon=0;info.index=-1;info.attributes=0;H images=SHGetFileInfoW(L"__DIR__",16,&info,sizeof(info),0x4011);check(images&&info.index==1,"actual small folder image list");check(SendMessageW(list,0x1003,1,(I)images)==0&&(H)SendMessageW(list,0x1002,1,0)==images,"published set/get image-list messages");W documents[260];check(SHGetSpecialFolderPathW(0,documents,5,0)&&GetFileAttributesW(documents)!=0xffffffffu&&(GetFileAttributesW(documents)&16),"real granted Documents folder");check(!SHGetSpecialFolderPathW(0,documents,17,0)&&!documents[0],"virtual folder is not a physical path");check(!SHGetSpecialFolderPathW(0,0,5,0),"null folder output refused");fill(100);text_checks();say("M145_LIST_READY\n");MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);say("M145_LIST_LIFETIME_PASS\n");ExitProcess(0);}
