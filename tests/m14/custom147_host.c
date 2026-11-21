/* Own control-flow/fault adapters only. No original DLL is loaded on the host. */
#define __declspec(x)
#include "../../user/windows8/msi-custom147.c"
#undef __declspec
static unsigned failures147,body_status147,phase147,thread_status147,events147[32],event_count147,loads147,frees147,begins147,ends147,threads147,callbacks147,closes147,joined147,error147,bad147;
static void(*fatal147)(const char*);
static void event147(unsigned e){if(event_count147<32)events147[event_count147++]=e;}
unsigned len8(const char*s){unsigned n=0;while(s[n])++n;return n;}
void*memset(void*out,int value,size_t n){uint8_t*p=out;for(size_t i=0;i<n;++i)p[i]=(uint8_t)value;return out;}
unsigned msi_immediate147(unsigned h){return h==0x14700001u&&!(failures147&256u)&&!phase147;}
unsigned msi_begin_deferred147(const char*data){(void)data;++begins147;event147(3);if(failures147&4u)return 8;phase147=1;return 0;}
void msi_end_deferred147(void){++ends147;event147(9);if(!phase147)++bad147;phase147=0;}
static unsigned body147(unsigned h){++callbacks147;event147(5);if(h!=0x14700001u||!phase147)++bad147;return body_status147;}
HANDLE LoadLibraryW(const WCHAR*path){(void)path;++loads147;event147(1);if(failures147&1u){error147=126;return 0;}return 0x1234;}
void*GetProcAddress(HANDLE h,const char*name){(void)name;event147(2);if(h!=0x1234)++bad147;if(failures147&2u){error147=127;return 0;}return body147;}
int FreeLibrary(HANDLE h){++frees147;event147(10);if(h!=0x1234||phase147||(threads147&&!joined147))++bad147;if(failures147&64u){error147=6;return 0;}return 1;}
HANDLE CreateThread(void*security,size_t stack,unsigned(*callback)(void*),void*context,unsigned flags,unsigned*id){(void)security;(void)stack;(void)flags;++threads147;event147(4);if(failures147&8u){--threads147;error147=8;return 0;}*id=2;if(!(failures147&512u))thread_status147=callback(context);return 0x2345;}
unsigned WaitForSingleObject(HANDLE h,unsigned timeout){event147(6);if(h!=0x2345||timeout!=UINT32_MAX)++bad147;if(failures147&128u){error147=6;return UINT32_MAX;}joined147=1;return 0;}
int GetExitCodeThread(HANDLE h,unsigned*out){event147(7);if(h!=0x2345||!joined147)++bad147;if(failures147&16u){error147=6;return 0;}*out=thread_status147;return 1;}
int CloseHandle(HANDLE h){++closes147;event147(8);if(h!=0x2345||!joined147)++bad147;if(failures147&32u){error147=6;return 0;}return 1;}
unsigned GetLastError(void){return error147;}
NORETURN void fail8(const char*text){if(fatal147)fatal147(text);__builtin_trap();}
__declspec(dllexport) void fatal_hook147(void(*hook)(const char*)){fatal147=hook;}
__declspec(dllexport) unsigned stat147(unsigned i){unsigned values[]={loads147,frees147,begins147,ends147,threads147,callbacks147,closes147,joined147,error147,phase147,bad147,event_count147};return i<12?values[i]:i<44?events147[i-12]:0;}
__declspec(dllexport) unsigned invoke147(unsigned type,unsigned body,unsigned failures,msia_custom_result147*out){failures147=failures;body_status147=body;phase147=thread_status147=event_count147=loads147=frees147=begins147=ends147=threads147=callbacks147=closes147=joined147=error147=bad147=0;for(unsigned i=0;i<32;++i)events147[i]=0;return msia_deferred147(0x14700001u,type,L"fixture.dll","Action","payload",out);}
