/* Owned Windows reference executable. No UI and no third-party program body. */
#include <stdint.h>
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
void entry(void);void*volatile image_reference_anchor148=&entry;
void entry(void){unsigned written=0;WriteFile(GetStdHandle((unsigned)-11),"READY\n",6,&written,0);Sleep(2000);ExitProcess(0);}
