/* Own negative fixture: missing static API fails, optional discovery stays null. */
typedef unsigned long long H;typedef unsigned short W;
__declspec(dllimport) H GetModuleHandleW(const W*);
__declspec(dllimport) void*GetProcAddress(H,const char*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int PathIsRelativeW(const W*);
__declspec(dllimport) void ExitProcess(unsigned);
static const W*volatile relative145=L"relative.txt";
void entry(void){H module=GetModuleHandleW(L"SHLWAPI.dll");if(!module||GetProcAddress(module,"PathIsRelativeW")||GetLastError()!=127)ExitProcess(2);const char*message="M145_GUARD_DISCOVERY_PASS\n";unsigned written;WriteFile(GetStdHandle((unsigned)-11),message,26,&written,0);PathIsRelativeW(relative145);ExitProcess(3);}
