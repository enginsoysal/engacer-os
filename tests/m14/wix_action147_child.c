/* Own executable child used to verify the original action's pipe/exit path. */
#include <stdint.h>
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
void entry(void);void*volatile anchor147=&entry;
void entry(void){static const char output[]="M147_REAL_WIX_CAPTURED_CHILD_OUTPUT\r\n";unsigned n=0;if(!WriteFile(GetStdHandle((unsigned)-11),output,sizeof(output)-1,&n,0)||n!=sizeof(output)-1)ExitProcess(91);ExitProcess(0);}
