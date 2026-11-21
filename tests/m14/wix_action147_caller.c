/* Own caller only; the real WiX implementation is not replaced. */
#include <stdint.h>
__declspec(dllimport) uint64_t LoadLibraryW(const uint16_t*);
__declspec(dllimport) void *GetProcAddress(uint64_t,const char*);
__declspec(dllimport) int FreeLibrary(uint64_t);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
void entry(void);void*volatile anchor147=&entry;
void entry(void){uint64_t dll=LoadLibraryW(L"C:\\Program Files\\7-Zip\\msi.dll");if(!dll)ExitProcess(87);unsigned(*run)(void)=GetProcAddress(dll,"TestOriginalAction147");if(!run)ExitProcess(88);unsigned status=run();if(status)ExitProcess(status);if(!FreeLibrary(dll))ExitProcess(89);static const char text[]="M147_ORIGINAL_WIX_DEFERRED_CHILD_OUTPUT_PASS\n";unsigned bytes=0;if(!WriteFile(GetStdHandle((unsigned)-11),text,sizeof(text)-1,&bytes,0)||bytes!=sizeof(text)-1)ExitProcess(90);ExitProcess(0);}
