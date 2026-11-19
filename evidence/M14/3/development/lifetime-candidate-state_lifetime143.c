/* Own Windows PE checks exit/cancel/fault ownership; never run on the host. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {U internal,high;unsigned offset,offset_high;U event;} OV;
__declspec(dllimport) U CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,U);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int ReadFile(U,void*,unsigned,unsigned*,void*);
__declspec(dllimport) int LockFileEx(U,unsigned,unsigned,unsigned,unsigned,OV*);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) int RegCreateKeyExW(U,const W*,unsigned,W*,unsigned,unsigned,void*,U*,unsigned*);
__declspec(dllimport) int RegSetValueExW(U,const W*,unsigned,unsigned,const void*,unsigned);
__declspec(dllimport) int RegOpenKeyExW(U,const W*,unsigned,unsigned,U*);
__declspec(dllimport) int RegQueryValueExW(U,const W*,unsigned*,unsigned*,void*,unsigned*);
static void require(int good,unsigned code){if(!good)ExitProcess(code);}
static void print(const char*text){unsigned n=0,wrote=0;while(text[n])++n;require(WriteFile(GetStdHandle((unsigned)-11),text,n,&wrote,0)&&wrote==n,99);}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){
 U key=0;unsigned disposition=0,value=14303,wrote=0;OV lock={0};
#if MODE143==3
 (void)disposition;(void)wrote;(void)lock;
 unsigned type=0,bytes=4,read_value=0;
 require(!RegOpenKeyExW(0xffffffff80000001ULL,L"Software\\M143Lifecycle",0,1,&key),30);
 require(!RegQueryValueExW(key,L"durable",0,&type,&read_value,&bytes)&&type==4&&bytes==4&&read_value==value,31);
 print("M143_STATE_RESTART_REGISTRY_PASS\n");ExitProcess(0);
#else
 U file=CreateFileW(L"m143-lifecycle.bin",0xc0000000u,0,0,3,128,0);require(file!=~(U)0,10);
 require(LockFileEx(file,3,0,64,0,&lock),11);
 require(WriteFile(file,"changed ",8,&wrote,0)&&wrote==8,12);
 U temporary=CreateFileW(L"m143-lifecycle-temp.bin",0xc0010000u,0,0,2,0x04000080u,0);require(temporary!=~(U)0,13);
 require(WriteFile(temporary,"scratch",7,&wrote,0)&&wrote==7,14);
 require(!RegCreateKeyExW(0xffffffff80000001ULL,L"Software\\M143Lifecycle",0,0,0,3,0,&key,&disposition),15);
 require(!RegSetValueExW(key,L"durable",0,4,&value,4),16);
 print("M143_STATE_HELD_READY\n");
#if MODE143==1
 Sleep(0xffffffffu);
#elif MODE143==2
 *(volatile U*)0xffff800000000000ULL=14303;
#else
 print("M143_STATE_EXIT_PASS\n");
#endif
 ExitProcess(0);
#endif
}
