/* Owned ABI/lifetime fixture. This is not an original-app compatibility claim. */
typedef unsigned long long U64;
typedef long long I64;
typedef unsigned short W;
typedef U64 H;
typedef I64 (*PROC)(H,unsigned,U64,I64);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;U64 wp;I64 lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) unsigned RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I64 DefWindowProcW(H,unsigned,U64,I64);
__declspec(dllimport) I64 SendMessageW(H,unsigned,U64,I64);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) int ShowWindow(H,int);
__declspec(dllimport) int PostMessageW(H,unsigned,U64,I64);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) int PeekMessageW(MSG*,H,unsigned,unsigned,unsigned);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) int TranslateMessage(const MSG*);
__declspec(dllimport) I64 DispatchMessageW(const MSG*);
__declspec(dllimport) I64 GetWindowLongPtrW(H,int);
__declspec(dllimport) I64 SetWindowLongPtrW(H,int,I64);
__declspec(dllimport) int SetWindowTextW(H,const W*);
__declspec(dllimport) int IsWindow(H);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) unsigned GetLastError(void);
static unsigned mode,nccreate,create,destroy,ncdestroy,characters,moves,sizes,callbacks;
static H root;
static void say(const char*s){unsigned n=0,written=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&written,0);}
static void check(unsigned ok,const char*name){if(!ok){say("M144_FAIL ");say(name);say("\n");ExitProcess(1);}}
static I64 procedure(H h,unsigned m,U64 wp,I64 lp){
 ++callbacks;
 if(m==0x81){++nccreate;check(*(U64*)(U64)lp==0x12345678,"CREATESTRUCT parameter");SetWindowLongPtrW(h,-21,0x778899);return mode==1?0:1;}
 if(m==1){++create;check(GetWindowLongPtrW(h,-21)==0x778899,"GWLP_USERDATA during creation");return mode==2?-1:0;}
 if(m==2){++destroy;if(h==root)PostQuitMessage(23);return 0;}
 if(m==0x82){++ncdestroy;check(GetWindowLongPtrW(h,-21)==0x778899,"userdata through NCDESTROY");return 0;}
 if(m==0x8001)return (I64)wp+lp;
 if(m==0x8002)return SendMessageW(h,0x8001,wp,lp)+1;
 if(m==0x102){++characters;SetWindowTextW(h,L"Original procedure received keyboard input");say("M144_CHARACTER_RECEIVED\n");return 0;}
 if(m==3){++moves;say("M144_MOVE_RECEIVED\n");return 0;}
 if(m==5){++sizes;say("M144_SIZE_RECEIVED\n");return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile relocation144=procedure;
static H window(unsigned visible){return CreateWindowExW(0,L"EngacerOwnedWindow144",L"Native Win64 window procedure",0x00cf0000u|(visible?0x10000000u:0),180,120,700,430,0,0,0,(void*)0x12345678);}
void entry(void){
 CLASS cls={0};cls.proc=relocation144;cls.win_extra=16;cls.name=L"EngacerOwnedWindow144";check(RegisterClassW(&cls)!=0,"RegisterClassW");
 mode=1;check(!window(0),"NCCREATE refusal");check(nccreate==1&&create==0&&destroy==0&&ncdestroy==1,"NCCREATE refusal sequence");
 mode=2;check(!window(0),"CREATE refusal");check(nccreate==2&&create==1&&destroy==1&&ncdestroy==2,"CREATE refusal sequence");
 mode=0;
 for(unsigned i=0;i<20;++i){H h=window(0);check(h!=0,"temporary create");check(SetWindowLongPtrW(h,0,0x123abc)==0,"extra storage initial");check(GetWindowLongPtrW(h,0)==0x123abc,"extra storage read");check(SendMessageW(h,0x8002,10,20)==31,"reentrant SendMessageW");check(DestroyWindow(h),"temporary destroy");check(!IsWindow(h),"stale IsWindow");check(!SendMessageW(h,0x8001,1,2)&&GetLastError()==1400,"stale SendMessageW");}
 root=window(0);check(root!=0,"root create");MSG m;
 H child=CreateWindowExW(0,L"EngacerOwnedWindow144",L"Child",0x40000000u,10,10,100,100,root,7,0,(void*)0x12345678);check(child!=0,"child create");
 check(PostMessageW(child,0x8800,87,88),"child post");check(PeekMessageW(&m,root,0x8800,0x8800,1)&&m.window==child&&m.wp==87,"parent-filter child retrieval");check(DestroyWindow(child),"child destroy");
 for(unsigned i=0;i<56;++i)check(PostMessageW(root,0x8001,i,0),"bounded queue fill");
 check(!PostMessageW(root,0x8001,56,0)&&GetLastError()==1816,"bounded queue refusal");PostQuitMessage(29);
 check(PeekMessageW(&m,0,0x9000,0x9001,0)&&m.message==0x12&&m.wp==29,"quit bypasses filter without removal");
 check(GetMessageW(&m,0,0x9000,0x9001)==0&&m.wp==29,"quit survives full queue");
 for(unsigned i=0;i<56;++i)check(PeekMessageW(&m,root,0,0,1)&&m.wp==i,"overflow preserves prior order");
 check(PostMessageW(root,0x8001,11,22),"post first");check(PostMessageW(root,0x8002,33,44),"post second");
 check(PeekMessageW(&m,root,0x8002,0x8002,0)&&m.wp==33,"filtered nonremoving peek");
 check(PeekMessageW(&m,root,0x8002,0x8002,1)&&m.wp==33,"filtered remove");
 check(PeekMessageW(&m,root,0,0,1)&&m.message==0x8001&&m.wp==11,"unmatched message preserved");
 ShowWindow(root,1);say("M144_NATIVE_WINDOW_WAITING\n");int status;
 while((status=GetMessageW(&m,0,0,0))>0){TranslateMessage(&m);DispatchMessageW(&m);}
 check(status==0&&m.wp==23,"WM_QUIT status");check(!IsWindow(root),"root destroyed");check(characters>0&&moves>0&&sizes>0,"real native input and geometry");check(nccreate==24&&create==23&&destroy==23&&ncdestroy==24,"exact lifecycle callbacks");say("M144_WINDOW_LIFETIME_PASS\n");ExitProcess(0);
}
