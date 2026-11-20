/* Owned consumed-input state, no-remove peeking, posted-key and snapshot checks. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) H LoadCursorW(H,const W*);
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) short GetKeyState(int);
__declspec(dllimport) unsigned MapVirtualKeyW(unsigned,unsigned);
__declspec(dllimport) int GetKeyboardState(unsigned char*);
__declspec(dllimport) int PeekMessageW(MSG*,H,unsigned,unsigned,unsigned);
__declspec(dllimport) int PostMessageW(H,unsigned,H,I);
__declspec(dllimport) int GetCursorPos(int*);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static H root;static unsigned key_checked,posted_checked,snapshot_checked,released,shifted_key;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int ok,const char*s){if(!ok){say("M145_KEYS_FAIL ");say(s);say("\n");ExitProcess(1);}}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==0x100&&wp=='1'){check(((H)lp>>16&255)==MapVirtualKeyW('1',0),"shifted digit scan code");shifted_key=1;return 0;}
 if(m==0x102&&wp=='!'){check(shifted_key,"shifted character uses digit virtual key");shifted_key=2;say("M145_KEYS_SHIFTED_PASS\n");return 0;}
 if(m==0x100&&wp=='A'){
  if(!key_checked){check(GetKeyState('A')&0x8000,"consumed real key down");check(((H)lp>>16&255)==MapVirtualKeyW('A',0),"native key message carries the matching scan code");Sleep(150);MSG next;check(PeekMessageW(&next,h,0x101,0x101,0)&&next.wp=='A'&&(GetKeyState('A')&0x8000),"no-remove peek preserves down state");check(PeekMessageW(&next,h,0x101,0x101,1)&&!(GetKeyState('A')&0x8000),"removing real key up changes state");key_checked=1;check(PostMessageW(h,0x100,'A',1),"post ordinary key message");}
  else{check(!(GetKeyState('A')&0x8000),"posted message cannot fabricate native key state");posted_checked=1;say("M145_KEYS_QUEUE_PASS\n");}return 0;
 }
 if(m==0x200){int point[2];for(unsigned n=0;n<20;++n)check(GetCursorPos(point)&&point[0]>=0&&point[1]>=0,"pure cursor query under input");return 0;}
 if(m==0x201){check(key_checked&&posted_checked&&(GetKeyState(0x11)&0x8000)&&(GetKeyState(1)&0x8000),"actual control and mouse down");Sleep(900);unsigned char keys[256];check(GetKeyboardState(keys)&&(keys[0x11]&0x80)&&(keys[0xa2]&0x80)&&(keys[1]&0x80)&&(GetKeyState(0x11)&0x8000),"queued snapshot survives physical release before callback read");snapshot_checked=1;say("M145_KEYS_SNAPSHOT_PASS\n");return 0;}
 if(m==0x101&&wp==0x11&&snapshot_checked){check(!(GetKeyState(0x11)&0x8000),"native modifier release is delivered");released=1;say("M145_KEYS_RELEASE_PASS\n");return 0;}
 if(m==2){check(key_checked&&posted_checked&&snapshot_checked&&released&&shifted_key==2,"complete native key lifetime");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){check(MapVirtualKeyW(8,0)==14&&MapVirtualKeyW(0xa3,4)==0xe01d&&MapVirtualKeyW(0xe01d,3)==0xa3,"real scan and virtual-key mappings");CLASS cls={0};cls.proc=anchor;cls.cursor=LoadCursorW(0,(const W*)32512);cls.name=L"Keys145";cls.background=6;check(RegisterClassW(&cls)!=0,"class");root=CreateWindowExW(0,cls.name,L"Native consumed input state",0x10cf0000,180,100,560,360,0,0,0,0);check(root!=0,"root");check(CreateWindowExW(0,L"Edit",L"Cursor target",0x50800000,280,40,200,60,root,11,0,0)!=0,"native edit cursor target");say("M145_KEYS_READY\n");MSG msg;while(GetMessageW(&msg,0,0,0)>0)DispatchMessageW(&msg);say("M145_KEYS_LIFETIME_PASS\n");ExitProcess(0);}
