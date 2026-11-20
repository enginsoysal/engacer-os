/* Own native ownership, modality, visible-root admission and capture fixture. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) H GetParent(H);
__declspec(dllimport) int IsWindow(H);
__declspec(dllimport) int EnableWindow(H,int);
__declspec(dllimport) int IsWindowEnabled(H);
__declspec(dllimport) H SetFocus(H);
__declspec(dllimport) H GetFocus(void);
__declspec(dllimport) H SetCapture(H);
__declspec(dllimport) H GetCapture(void);
__declspec(dllimport) int ReleaseCapture(void);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static H owner,modal,owned;static unsigned forbidden_close,captured_outside;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*why){if(!ok){say("M144_OWNER_FAIL ");say(why);say("\n");ExitProcess(1);}}
static H create(const W*title,int x,int y,H parent){return CreateWindowExW(0,L"NativeOwner144",title,0x10cf0000,x,y,400,260,parent,0,0,0);}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==0x10&&h==owner){if(!IsWindowEnabled(owner)){++forbidden_close;check(0,"disabled owner received native close");}DestroyWindow(owner);return 0;}
 if(m==0x10&&h==modal){EnableWindow(owner,1);DestroyWindow(modal);modal=0;say("M144_MODAL_CLOSED\n");return 0;}
 if(m==0x201&&h==owner){SetFocus(owner);SetCapture(owner);check(GetCapture()==owner,"native capture set");say("M144_CAPTURE_READY\n");return 0;}
 if(m==0x200&&h==owner&&GetCapture()==owner){int x=(short)(lp&65535),y=(short)((lp>>16)&65535);if(x<0||y<0||x>=398||y>=219){captured_outside=1;say("M144_CAPTURE_OUTSIDE\n");}return 0;}
 if(m==0x202&&h==owner){check(ReleaseCapture()&&!GetCapture(),"capture release");say("M144_CAPTURE_RELEASED\n");return 0;}
 if(m==0x102&&wp=='m'){check(h==modal,"keyboard remains with enabled modal");say("M144_MODAL_KEYBOARD_PASS\n");return 0;}
 if(m==0x102&&h==owner&&wp=='p'){check(!modal&&IsWindowEnabled(owner),"owner resumed after modal close");say("M144_OWNER_RESPONSIVE\n");return 0;}
 if(m==0x102&&h==owner&&wp=='c'){owned=create(L"Owned palette",650,440,owner);check(owned&&GetParent(owned)==owner,"actual owner capability");say("M144_OWNED_VISIBLE\n");return 0;}
 if(m==2&&h==owner){check(!forbidden_close&&captured_outside,"native modal/capture checks");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){CLASS cls={0};cls.proc=anchor;cls.name=L"NativeOwner144";cls.background=6;check(RegisterClassW(&cls),"register");owner=create(L"Disabled owner",80,80,0);check(owner!=0,"owner create");SetFocus(owner);SetCapture(owner);check(GetFocus()==owner&&GetCapture()==owner,"initial input ownership");EnableWindow(owner,0);check(!GetFocus()&&!GetCapture(),"disabling owner releases input ownership");modal=create(L"Owned modal",650,140,owner);check(modal&&GetParent(modal)==owner,"modal owner relationship");H extra[5];for(unsigned i=0;i<5;++i){extra[i]=create(L"Admission fixture",120+(int)i*12,100,0);check(extra[i]!=0,"visible root reservation");}H refused=create(L"Must not be invisible",120,100,0);check(!refused&&GetLastError()==1816,"visible root quota is explicit");for(unsigned i=0;i<5;++i)check(DestroyWindow(extra[i]),"admission fixture release");say("M144_MODAL_READY\n");MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);check(owned&&!IsWindow(owned)&&!IsWindow(owner),"owner destruction removes owned windows");say("M144_OWNER_LIFETIME_PASS\n");ExitProcess(0);}
