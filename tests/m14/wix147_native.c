/* Own admission caller; the unchanged original DLL executes only in Engacer. */
#include <stdint.h>
#include <stddef.h>
__declspec(dllimport) uint64_t LoadLibraryW(const uint16_t*);
__declspec(dllimport) void *GetProcAddress(uint64_t,const char*);
__declspec(dllimport) int FreeLibrary(uint64_t);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
void entry(void);void*volatile anchor147=&entry;
void entry(void){uint64_t module=LoadLibraryW(L"C:\\Program Files\\7-Zip\\wix147.dll");if(!module||!GetProcAddress(module,"WixQuietExec"))ExitProcess(87);if(!FreeLibrary(module))ExitProcess(88);static const char text[]="M147_ORIGINAL_WIX_NATIVE_LOAD_EXPORT_UNLOAD_PASS\n";unsigned n=0;if(!WriteFile(GetStdHandle((unsigned)-11),text,sizeof(text)-1,&n,0)||n!=sizeof(text)-1)ExitProcess(89);ExitProcess(0);}
