/* Owned dialog resource/callback/keyboard/cancellation fixture. */
typedef unsigned long long H;typedef long long I;typedef unsigned short W;
typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
typedef struct {H window;unsigned message,pad;H wp;I lp;unsigned time;int x,y;unsigned private_;} MSG;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) I DialogBoxParamW(H,const W*,H,PROC,I);
__declspec(dllimport) int EndDialog(H,I);
__declspec(dllimport) int IsWindowEnabled(H);
__declspec(dllimport) H GetDlgItem(H,int);
__declspec(dllimport) int GetDlgCtrlID(H);
__declspec(dllimport) int SetDlgItemTextW(H,int,const W*);
__declspec(dllimport) unsigned GetDlgItemTextW(H,int,W*,int);
__declspec(dllimport) I SetWindowLongPtrW(H,int,I);
__declspec(dllimport) I GetWindowLongPtrW(H,int);
__declspec(dllimport) int GetMessageW(MSG*,H,unsigned,unsigned);
__declspec(dllimport) I DispatchMessageW(const MSG*);
__declspec(dllimport) void PostQuitMessage(int);
__declspec(dllimport) H LoadLibraryW(const W*);
__declspec(dllimport) int FreeLibrary(H);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
static H root,module;static unsigned standard_done,extended_done,immediate_done;
static void say(const char*s){unsigned n=0,w;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int ok,const char*why){if(!ok){say("M145_DIALOG_FAIL ");say(why);say("\n");ExitProcess(1);}}
static I dialog(H h,unsigned m,H wp,I lp){
 if(m==0x110){check(!IsWindowEnabled(root),"owner disabled before initialization");check((H)lp==0x1122334455667788ull||(H)lp==0x8877665544332211ull,"64-bit initialization data");
  check(GetDlgCtrlID(GetDlgItem(h,11))==11,"real child IDs");check(SetDlgItemTextW(h,11,L"Editable value"),"set edit");W text[64];check(GetDlgItemTextW(h,11,text,64)==14&&text[0]=='E',"get edit");
  SetWindowLongPtrW(h,16,0x1234567812345678ll);check(GetWindowLongPtrW(h,16)==0x1234567812345678ll,"DWLP_USER independent from runtime context");
  if((H)lp==0x8877665544332211ull){++immediate_done;check(EndDialog(h,123),"EndDialog during initialization");return 0;}
  say("M145_MODAL_INITIALIZED\n");return 1;
 }
 if(m==0x111&&(wp&65535)==1){W text[64];check(GetDlgItemTextW(h,11,text,64)==15&&text[0]=='x',"native edit keyboard data");check(EndDialog(h,321),"accept modal");return 1;}
 if(m==0x111&&(wp&65535)==2){check(EndDialog(h,-2),"cancel modal");return 1;}
 return 0;
}
static I procedure(H h,unsigned m,H wp,I lp){
 if(m==0x102&&wp=='a'){check(DialogBoxParamW(module,(const W*)100,h,dialog,0x1122334455667788ll)==321,"standard result");check(IsWindowEnabled(h),"owner restored after accept");standard_done=1;say("M145_STANDARD_DIALOG_PASS\n");return 0;}
 if(m==0x102&&wp=='b'){check(DialogBoxParamW(module,(const W*)101,h,dialog,0x1122334455667788ll)==-2,"extended signed result");check(IsWindowEnabled(h),"owner restored after cancel");extended_done=1;say("M145_EXTENDED_DIALOG_PASS\n");return 0;}
 if(m==2){check(standard_done&&extended_done&&immediate_done==1,"complete modal lifetimes");PostQuitMessage(0);return 0;}
 return DefWindowProcW(h,m,wp,lp);
}
static PROC volatile anchor=procedure;
void entry(void){
 module=LoadLibraryW(L"dialogs145.dll");check(module!=0,"resource DLL");CLASS cls={0};cls.proc=anchor;cls.name=L"NativeModal145";check(RegisterClassW(&cls)!=0,"class");root=CreateWindowExW(0,cls.name,L"Original dialog procedure fixture",0x10cf0000,180,100,560,320,0,0,0,0);check(root!=0,"owner");
 check(DialogBoxParamW(module,(const W*)103,root,dialog,0)==-1&&GetLastError()==193&&IsWindowEnabled(root),"truncated template refusal");
 check(DialogBoxParamW(module,(const W*)104,root,dialog,0)==-1&&GetLastError()==1816&&IsWindowEnabled(root),"template quota refusal");
 check(DialogBoxParamW(module,(const W*)105,root,dialog,0)==-1&&GetLastError()==1816&&IsWindowEnabled(root),"partial child creation rollback");
 check(DialogBoxParamW(module,(const W*)102,root,dialog,(I)0x8877665544332211ull)==123&&IsWindowEnabled(root),"initialization-time EndDialog and owner restore");
 say("M145_DIALOG_READY\n");MSG message;while(GetMessageW(&message,0,0,0)>0)DispatchMessageW(&message);
 check(FreeLibrary(module),"resource unload");say("M145_DIALOG_LIFETIME_PASS\n");ExitProcess(0);
}
