/* Owned Win64 common-dialog task; original apps remain separate acceptance. */
#define W8_USER
#include <engine/winpicker146.h>
typedef uint64_t H;typedef int64_t I;typedef uint16_t W;typedef I(*PROC)(H,unsigned,H,I);
typedef struct {unsigned style;PROC proc;int cls_extra,win_extra;H instance,icon,cursor,background;const W*menu,*name;} CLASS;
__declspec(dllimport) H RegisterClassW(const CLASS*);
__declspec(dllimport) H CreateWindowExW(unsigned,const W*,const W*,unsigned,int,int,int,int,H,H,H,void*);
__declspec(dllimport) int DestroyWindow(H);
__declspec(dllimport) I DefWindowProcW(H,unsigned,H,I);
__declspec(dllimport) int GetOpenFileNameW(void*);
__declspec(dllimport) int GetSaveFileNameW(void*);
__declspec(dllimport) unsigned CommDlgExtendedError(void);
__declspec(dllimport) H CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,H);
__declspec(dllimport) int ReadFile(H,void*,unsigned,unsigned*,void*);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int CloseHandle(H);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) void* VirtualAlloc(void*,H,unsigned,unsigned);
__declspec(dllimport) int VirtualProtect(void*,H,unsigned,unsigned*);
__declspec(dllimport) int VirtualFree(void*,H,unsigned);
__declspec(dllimport) unsigned GetFileAttributesW(const W*);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(int yes,const char*s){if(!yes){say("M146_PICKER_FAIL ");say(s);say("\n");ExitProcess(1);}}
static void clear(void*p,unsigned n){unsigned char*b=p;for(unsigned i=0;i<n;++i)b[i]=0;}
static unsigned length(const W*s){unsigned n=0;while(s[n])++n;return n;}
static void copy(W*d,const W*s){unsigned i=0;do{d[i]=s[i];}while(s[i++]);}
static int same(const void*a,const void*b,unsigned n){const unsigned char*x=a,*y=b;for(unsigned i=0;i<n;++i)if(x[i]!=y[i])return 0;return 1;}
static W file[512],file_title[128];static H owner;
static void init(wpick_ofn146*p){clear(p,sizeof(*p));p->size=152;p->owner=owner;p->file=(H)file;p->file_capacity=512;p->file_title=(H)file_title;p->title_capacity=128;p->initial_directory=(H)L"C:/Users/Owner/Documents";p->filter=(H)L"Text files\0*.txt\0All files\0*.*\0";p->filter_index=1;p->flags=0x8000c;p->default_extension=(H)L"txt";file[0]=file_title[0]=0;}
static void verify_path(wpick_ofn146*p,const W*name){unsigned n=length(file),base=n;while(base&&file[base-1]!=0x5c)--base;unsigned extension=0;for(unsigned i=base;i<n;++i)if(file[i]=='.')extension=i+1;check(p->file_offset==base&&p->file_extension==extension,"UTF-16 offsets");check(length(file_title)==length(name)&&same(file_title,name,(length(name)+1)*2),"file title");check(same(file+base,name,(length(name)+1)*2)&&p->filter_index==1,"path and selected filter");}
static void read_exact(const W*path,const char*expected){H h=CreateFileW(path,0x80000000,3,0,3,0,0);check(h!=(H)-1,"open selected file");char text[128];unsigned n=0,wanted=0;while(expected[wanted])++wanted;check(ReadFile(h,text,sizeof(text),&n,0)&&n==wanted&&same(text,expected,wanted)&&CloseHandle(h),"actual selected file bytes");}
static void write_exact(const W*path,const char*text,unsigned creation){H h=CreateFileW(path,0x40000000,3,0,creation,0,0);check(h!=(H)-1,"app creates selected destination");unsigned n=0,wanted=0;while(text[wanted])++wanted;check(WriteFile(h,text,wanted,&n,0)&&n==wanted&&CloseHandle(h),"actual app write");}
static I procedure(H h,unsigned m,H w,I l){return DefWindowProcW(h,m,w,l);}
static PROC volatile anchor=procedure;
void entry(void){
 CLASS cls={0};cls.proc=anchor;cls.name=L"Picker146";check(RegisterClassW(&cls)!=0,"class");owner=CreateWindowExW(0,cls.name,L"Common dialog interoperability",0x10cf0000,180,100,560,360,0,0,0,0);check(owner!=0,"owner window");wpick_ofn146 ofn;
 if(GetFileAttributesW(L"C:/Users/Owner/Documents/m146-save-\u00e9.txt")!=(unsigned)-1)check(DeleteFileW(L"C:/Users/Owner/Documents/m146-save-\u00e9.txt"),"remove previous owned fixture output");
 check(!GetOpenFileNameW(0)&&CommDlgExtendedError()==0xffff,"invalid structure pointer");
 init(&ofn);ofn.file=1;check(!GetOpenFileNameW(&ofn)&&CommDlgExtendedError()==0xffff,"invalid output pointer");
 init(&ofn);ofn.flags|=0x200;check(!GetOpenFileNameW(&ofn)&&CommDlgExtendedError()!=0,"multiselection refused");
 init(&ofn);{static const W invalid[]={0xd800,0};ofn.title=(H)invalid;check(!GetOpenFileNameW(&ofn)&&CommDlgExtendedError()!=0,"invalid UTF-16 title refused");}
 init(&ofn);{unsigned old;wpick_ofn146*readonly=VirtualAlloc(0,4096,0x3000,4);check(readonly!=0,"readonly request allocation");for(unsigned i=0;i<sizeof(ofn);++i)((volatile unsigned char*)readonly)[i]=((const unsigned char*)&ofn)[i];check(VirtualProtect(readonly,4096,2,&old),"protect request");check(!GetOpenFileNameW(readonly)&&CommDlgExtendedError()==0xffff,"readonly structure refused without app fault");check(VirtualFree(readonly,0,0x8000),"readonly request release");}
 init(&ofn);ofn.size=1;check(!GetOpenFileNameW(&ofn)&&CommDlgExtendedError()==1,"invalid structure size");init(&ofn);ofn.flags|=0x20;check(!GetOpenFileNameW(&ofn)&&CommDlgExtendedError()!=0,"hooks explicitly refused");
 init(&ofn);copy(file,L"KEEP");say("M146_PICKER_CANCEL_READY\n");check(!GetOpenFileNameW(&ofn)&&!CommDlgExtendedError()&&same(file,L"KEEP",10),"cancel preserves buffer");
 init(&ofn);ofn.size=136;say("M146_PICKER_OPEN_READY\n");check(GetOpenFileNameW(&ofn),"open selection");verify_path(&ofn,L"m146-open-\u00e9.txt");read_exact(file,"original dialog source \xc3\xa9\n");
 init(&ofn);ofn.file_capacity=2;file[1]=0x4321;say("M146_PICKER_SHORT_READY\n");check(!GetOpenFileNameW(&ofn)&&CommDlgExtendedError()==0x3003&&file[0]>2&&file[1]==0x4321,"short buffer reports required UTF-16 units only");
 init(&ofn);copy(file,L"m146-save-\u00e9");say("M146_PICKER_SAVE_READY\n");check(GetSaveFileNameW(&ofn),"save destination");verify_path(&ofn,L"m146-save-\u00e9.txt");check(GetFileAttributesW(file)==(unsigned)-1,"dialog does not create a file");write_exact(file,"first dialog save \xc3\xa9\n",1);
 init(&ofn);copy(file,L"m146-save-\u00e9.txt");say("M146_PICKER_REPLACE_CANCEL_READY\n");check(!GetSaveFileNameW(&ofn)&&!CommDlgExtendedError(),"replacement cancel");read_exact(L"C:/Users/Owner/Documents/m146-save-\u00e9.txt","first dialog save \xc3\xa9\n");
 init(&ofn);copy(file,L"m146-save-\u00e9.txt");say("M146_PICKER_REPLACE_READY\n");check(GetSaveFileNameW(&ofn),"replacement consent");verify_path(&ofn,L"m146-save-\u00e9.txt");write_exact(file,"final dialog save \xc3\xa9\n",2);read_exact(file,"final dialog save \xc3\xa9\n");
 check(DestroyWindow(owner),"owner destroy");say("M146_COMMON_DIALOG_BYTES_CANCEL_REPLACE_PASS\n");ExitProcess(0);
}
