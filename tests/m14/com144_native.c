/* Owned COM apartment/target callbacks and normal GUI-thread teardown. */
typedef unsigned long long H;
typedef long long I64;
typedef unsigned short W;
typedef I64(*PROC)(H,unsigned,H,I64);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
__declspec(dllimport) int CoInitializeEx(void*,unsigned);
__declspec(dllimport) int CoInitialize(void*);
__declspec(dllimport) void CoUninitialize(void);
__declspec(dllimport) int OleInitialize(void*);
__declspec(dllimport) void OleUninitialize(void);
__declspec(dllimport) int RegisterDragDrop(H,void*);
__declspec(dllimport) int RevokeDragDrop(H);
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I64 DefWindowProcW(H,unsigned,H,I64);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) int IsWindow(H);
__declspec(dllimport) H CreateThread(void*,H,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForSingleObject(H,unsigned);
__declspec(dllimport) int GetExitCodeThread(H,unsigned*);
__declspec(dllimport) int CloseHandle(H);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static I64 procedure(H h,unsigned m,H w,I64 l){return DefWindowProcW(h,m,w,l);}
static unsigned refs=1,adds,releases;
static int query(void*self,void*iid,void**out){(void)self;(void)iid;if(out)*out=0;return(int)0x80004002;}
static unsigned add(void*self){(void)self;++adds;return ++refs;}
static unsigned release(void*self){(void)self;++releases;return --refs;}
static void*vtable[]={query,add,release};
static struct{void**vtable;}object={vtable};
static H thread_window;
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*message){if(!ok){say("M144_COM_FAIL ");say(message);say("\n");ExitProcess(1);}}
static H window(void){return CreateWindowExW(0,L"Apartment144",L"Owned apartment",0xcf0000,10,10,500,400,0,0,0,0);}
static unsigned thread(void*unused){(void)unused;check(CoInitializeEx(0,0)==0,"new thread apartment");check(CoInitializeEx(0,0)==1,"nested thread apartment");thread_window=window();check(thread_window!=0,"thread-owned hidden window");return 17;}
void entry(void){CLASS definition={0};definition.proc=procedure;definition.name=L"Apartment144";check(RegisterClassW(&definition)!=0,"window class");H root=window();check(root!=0,"window create");
 check(CoInitializeEx(0,0)==0,"MTA initial");check(CoInitializeEx(0,0)==1,"MTA nested");check(CoInitialize(0)==(int)0x80010106,"changed apartment refusal");check(OleInitialize(0)==(int)0x80010106,"OLE in MTA refusal");check(RegisterDragDrop(root,&object)==(int)0x8007000e&&refs==1,"OLE initialization required");CoUninitialize();CoUninitialize();
 check(OleInitialize(0)==0,"OLE initial STA");check(OleInitialize(0)==1,"OLE nested STA");check(RegisterDragDrop(root,&object)==0&&refs==2&&adds==1,"actual IUnknown AddRef");check(RegisterDragDrop(root,&object)==(int)0x80040101&&refs==2&&adds==1,"duplicate target refusal");check(RevokeDragDrop(root)==0&&refs==1&&releases==1,"actual IUnknown Release");check(RevokeDragDrop(root)==(int)0x80040100&&refs==1,"missing target refusal");
 check(RegisterDragDrop(root,&object)==0&&refs==2,"register again");check(DestroyWindow(root)&&refs==1&&releases==2,"window teardown releases target");OleUninitialize();OleUninitialize();check(CoInitializeEx(0,0)==0,"mode after balanced OLE shutdown");CoUninitialize();
 for(unsigned i=0;i<25;++i){unsigned id=0,code=0;H child=CreateThread(0,0,thread,0,0,&id);check(child&&id,"actual native thread");check(WaitForSingleObject(child,30000)==0&&GetExitCodeThread(child,&code)&&code==17,"thread completion");check(!IsWindow(thread_window),"thread-owned window destroyed");check(CloseHandle(child),"thread handle closed");}
 say("M144_COM_LIFETIME_PASS\n");ExitProcess(0);
}
