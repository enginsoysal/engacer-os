/* Synthetic all-sleeping Windows process for native cancellation checks. */
typedef unsigned long long U;
__declspec(dllimport) U CreateThread(void*,U,void*,void*,unsigned,unsigned*);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
static unsigned sleeper(void*unused){(void)unused;Sleep(~0u);ExitProcess(98);return 98;}
void entry(void);
void* volatile relocation_anchor=&entry;
void entry(void){for(unsigned i=0;i<3;++i)if(!CreateThread(0,0,sleeper,0,0,0))ExitProcess(97);Sleep(~0u);ExitProcess(99);}
