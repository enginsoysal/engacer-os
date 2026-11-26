#include <stdint.h>
#include <stddef.h>
__declspec(dllimport) void __stdcall ExitProcess(unsigned);
__declspec(dllimport) unsigned __stdcall GetCurrentProcessId(void);
__declspec(dllimport) unsigned __stdcall GetLastError(void);
__declspec(dllimport) void __stdcall SetLastError(unsigned);
__declspec(dllimport) uint32_t __stdcall GetStdHandle(int);
__declspec(dllimport) int __stdcall WriteFile(uint32_t,const void*,unsigned,unsigned*,void*);

#ifdef TEST_VIEWS
#include "engine/winexception32_1410.h"
__declspec(dllimport) uint32_t __stdcall CreateFileW(const wchar_t*,unsigned,unsigned,void*,unsigned,unsigned,uint32_t);
__declspec(dllimport) int __stdcall ReadFile(uint32_t,void*,unsigned,unsigned*,void*);
__declspec(dllimport) int __stdcall CloseHandle(uint32_t);
__declspec(dllimport) int __stdcall RegOpenKeyExW(uint32_t,const wchar_t*,unsigned,unsigned,uint32_t*);
__declspec(dllimport) int __stdcall RegQueryValueExW(uint32_t,const wchar_t*,void*,unsigned*,void*,unsigned*);
__declspec(dllimport) int __stdcall RegCloseKey(uint32_t);
typedef int (__stdcall *exception_filter)(win_exception_pointers321410*);
__declspec(dllimport) exception_filter __stdcall SetUnhandledExceptionFilter(exception_filter);
static volatile unsigned recovered;
static int __stdcall recover(win_exception_pointers321410 *p){
 win_exception_record321410 *record=(void*)(uintptr_t)p->record;
 win_context321410 *context=(void*)(uintptr_t)p->context;
 if(record->code!=0xc000001d||record->address!=context->eip)return 0;
 recovered=1;
 context->eip+=2;
 return -1;
}
static void check_view(unsigned view,unsigned expected){
 uint32_t key=0;
 unsigned type=0,value=0,size=sizeof(value);
 if(RegOpenKeyExW(0x80000002,L"Software\\EngineProbe",0,view|1,&key))ExitProcess(83+view/256);
 if(RegQueryValueExW(key,L"Payload",0,&type,&value,&size)||type!=4||value!=expected||
    size!=sizeof(value)||RegCloseKey(key))ExitProcess(85+view/256);
}
static void check_views(void){
 char payload=0;
 unsigned count=0;
 uint32_t file=CreateFileW(L"C:\\Windows\\System32\\view.dat",0x80000000,1,0,3,0,0);
 if(file==UINT32_MAX||!ReadFile(file,&payload,1,&count,0)||count!=1||payload!='x'||
    !CloseHandle(file))ExitProcess(87);
 check_view(0,32);
 check_view(0x100,64);
 if(SetUnhandledExceptionFilter(recover))ExitProcess(88);
 __asm__ volatile("ud2");
 if(!recovered||SetUnhandledExceptionFilter(0)!=recover)ExitProcess(89);
}
#endif

void entry(void){
#ifdef TEST_VIEWS
 check_views();
#endif
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
