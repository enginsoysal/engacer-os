/* Actual modal owner destruction, requesting-thread exit and process exit. */
#define W8_USER
#include <engine/winpicker146.h>
typedef uint64_t H;typedef int64_t I;typedef uint16_t W;typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) H SetTimer(H,H,unsigned,void*);
__declspec(dllimport) int KillTimer(H,H);
__declspec(dllimport) int GetOpenFileNameW(void*);
__declspec(dllimport) int GetSaveFileNameW(void*);
__declspec(dllimport) unsigned CommDlgExtendedError(void);
__declspec(dllimport) H CreateThread(void*,H,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForSingleObject(H,unsigned);
__declspec(dllimport) int GetExitCodeThread(H,unsigned*);
__declspec(dllimport) int CloseHandle(H);
__declspec(dllimport) void ExitThread(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int yes,const char*s){if(!yes){say("M146_LIFETIME_FAIL ");say(s);say("\n");ExitProcess(1);}}
static void init(wpick_ofn146*o,H owner,W*file){unsigned char*p=(void*)o;for(unsigned n=0;n<sizeof(*o);++n)p[n]=0;o->size=152;o->owner=owner;o->file=(H)file;o->file_capacity=64;o->initial_directory=(H)L"C:/Users/Owner/Documents";o->filter=(H)L"Text\0*.txt\0";o->filter_index=1;o->flags=0x8000c;}
static I procedure(H h,unsigned m,H w,I l){
 if(m==0x113){check(KillTimer(h,w),"retire timer before teardown");if(w==1){check(DestroyWindow(h),"destroy modal owner in callback");return 0;}if(w==2)ExitThread(17);if(w==3)ExitProcess(42);check(0,"unexpected timer identity");}
 return DefWindowProcW(h,m,w,l);
}
static PROC volatile anchor=procedure;
static W worker_file[64]={'K','E','E','P',0};
static H owner(unsigned timer){H h=CreateWindowExW(0,L"PickerLifetime146",L"Pending dialog teardown",0x10cf0000,160,100,540,240,0,0,0,0);check(h!=0,"live owner");check(SetTimer(h,timer,5000,0)!=0,"modal callback deadline");return h;}
static unsigned thread(void*unused){(void)unused;H h=owner(2);wpick_ofn146 o;init(&o,h,worker_file);say("M146_THREAD_EXIT_READY\n");GetSaveFileNameW(&o);check(0,"requesting thread unexpectedly returned after ExitThread");return 1;}
void entry(void){CLASS cls={0};cls.proc=anchor;cls.name=L"PickerLifetime146";check(RegisterClassW(&cls)!=0,"class");
 W file[64]={'K','E','E','P',0};H h=owner(1);wpick_ofn146 o;init(&o,h,file);say("M146_OWNER_DESTROY_READY\n");check(!GetOpenFileNameW(&o)&&CommDlgExtendedError()==0xffff,"destroyed owner refuses result");check(file[0]=='K'&&file[3]=='P'&&!file[4],"owner cancellation preserves output");say("M146_OWNER_RELEASE_PASS\n");
 H worker=CreateThread(0,0,thread,0,0,0);check(worker!=0&&WaitForSingleObject(worker,0xffffffffu)==0,"wait for requesting thread");unsigned code=0;check(GetExitCodeThread(worker,&code)&&code==17&&CloseHandle(worker),"thread exit and handle lifetime");check(worker_file[0]=='K'&&worker_file[3]=='P'&&!worker_file[4],"thread exit preserves abandoned output");say("M146_THREAD_RELEASE_PASS\n");
 h=owner(3);init(&o,h,file);say("M146_PROCESS_EXIT_READY\n");GetOpenFileNameW(&o);check(0,"process unexpectedly returned after ExitProcess");
}
