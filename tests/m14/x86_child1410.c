#include <stdint.h>
__declspec(dllimport) void __stdcall ExitProcess(unsigned);
__declspec(dllimport) unsigned __stdcall GetCurrentProcessId(void);
__declspec(dllimport) unsigned __stdcall GetLastError(void);
__declspec(dllimport) void __stdcall SetLastError(unsigned);
__declspec(dllimport) uint32_t __stdcall GetStdHandle(int);
__declspec(dllimport) int __stdcall WriteFile(uint32_t,const void*,unsigned,unsigned*,void*);

void entry(void){
#ifdef TEST_FAULT
 __asm__ volatile("ud2");
#endif
 SetLastError(1410);
 if(!GetCurrentProcessId()||GetLastError()!=1410)ExitProcess(81);
 static const char text[]="M1410_NATIVE_I386_THUNK_PASS\n";
 unsigned bytes=0;
 if(!WriteFile(GetStdHandle(-11),text,sizeof(text)-1,&bytes,0)||bytes!=sizeof(text)-1)ExitProcess(82);
 ExitProcess(0);
}
