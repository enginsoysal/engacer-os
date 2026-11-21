/* Real kernel atoms cross process lifetime; own executables only. */
#include <stdint.h>
__declspec(dllimport) unsigned short GlobalAddAtomW(const uint16_t*);
__declspec(dllimport) unsigned short GlobalFindAtomW(const uint16_t*);
__declspec(dllimport) unsigned short GlobalDeleteAtom(unsigned short);
__declspec(dllimport) unsigned GlobalGetAtomNameW(unsigned short,uint16_t*,int);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void SetLastError(unsigned);
__declspec(dllimport) const uint16_t*GetCommandLineW(void);
__declspec(dllimport) int CreateProcessW(const uint16_t*,uint16_t*,void*,void*,int,unsigned,void*,const uint16_t*,void*,void*);
__declspec(dllimport) unsigned WaitForSingleObject(uint64_t,unsigned);
__declspec(dllimport) int GetExitCodeProcess(uint64_t,unsigned*);
__declspec(dllimport) int CloseHandle(uint64_t);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
void entry(void);void*volatile anchor147=&entry;
static void check147(int value,unsigned code){if(!value)ExitProcess(code);}
void entry(void){
 const uint16_t*line=GetCommandLineW();unsigned child=0;for(unsigned i=0;line&&line[i];++i)if(line[i]==' '&&line[i+1]=='c'&&line[i+2]=='h'&&line[i+3]=='i'&&line[i+4]=='l'&&line[i+5]=='d'&&!line[i+6])child=1;
 if(child){check147(GlobalAddAtomW(L"ENGACER.NATIVE.ATOM147")>=0xc000,201);ExitProcess(0);}
 check147(!GlobalFindAtomW(L"Engacer.Native.Atom147"),202);unsigned short atom=GlobalAddAtomW(L"Engacer.Native.Atom147");check147(atom>=0xc000&&GlobalFindAtomW(L"engacer.native.atom147")==atom,203);
 uint8_t startup[104]={0};*(uint32_t*)startup=104;struct{uint64_t process,thread;uint32_t pid,tid;} process={0};uint16_t command[]=L"\"C:\\Program Files\\7-Zip\\atom-child147.exe\" child";
 check147(CreateProcessW(0,command,0,0,0,0x08000000u,0,0,startup,&process),204);check147(WaitForSingleObject(process.process,30000)==0,205);unsigned result=99;check147(GetExitCodeProcess(process.process,&result)&&!result,206);check147(CloseHandle(process.thread)&&CloseHandle(process.process),207);
 check147(GlobalFindAtomW(L"ENGACER.NATIVE.ATOM147")==atom,208);SetLastError(0);check147(GlobalDeleteAtom(atom)==0&&!GetLastError()&&GlobalFindAtomW(L"Engacer.Native.Atom147")==atom,209);
 uint16_t name[256];check147(GlobalGetAtomNameW(atom,name,256)==22,210);const uint16_t expected[]=L"Engacer.Native.Atom147";for(unsigned i=0;i<23;++i)check147(name[i]==expected[i],211);
 check147(GlobalDeleteAtom(atom)==0&&!GlobalFindAtomW(L"Engacer.Native.Atom147"),212);check147(GlobalAddAtomW(L"#37")==37&&GlobalFindAtomW((const uint16_t*)(uintptr_t)37)==37,213);SetLastError(0);check147(!GlobalDeleteAtom(37)&&!GlobalDeleteAtom(0)&&!GetLastError(),214);
 for(unsigned i=0;i<8;++i)name[i]=0x9b9b;check147(GlobalGetAtomNameW(7,name,2)==2&&name[0]=='#'&&name[1]=='7'&&name[2]==0x9b9b,215);check147(GlobalGetAtomNameW(7,name,3)==2&&!name[2],216);check147(!GlobalFindAtomW(L"#49152")&&GetLastError()==87,217);
 static const char output[]="M147_NATIVE_GLOBAL_ATOM_CREATOR_EXIT_REFERENCES_PASS\n";unsigned n=0;check147(WriteFile(GetStdHandle((unsigned)-11),output,sizeof(output)-1,&n,0)&&n==sizeof(output)-1,218);ExitProcess(0);
}
