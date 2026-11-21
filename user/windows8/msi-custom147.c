/* Execute the real DLL export on its own native action thread, then join it. */
#include "msi-custom147.h"
__declspec(dllimport) HANDLE LoadLibraryW(const WCHAR*);
__declspec(dllimport) void*GetProcAddress(HANDLE,const char*);
__declspec(dllimport) int FreeLibrary(HANDLE);
__declspec(dllimport) HANDLE CreateThread(void*,size_t,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForSingleObject(HANDLE,unsigned);
__declspec(dllimport) int GetExitCodeThread(HANDLE,unsigned*);
__declspec(dllimport) int CloseHandle(HANDLE);
__declspec(dllimport) unsigned GetLastError(void);
unsigned msi_begin_deferred147(const char*);
unsigned msi_immediate147(unsigned);
void msi_end_deferred147(void);
typedef struct {unsigned(*body)(unsigned);unsigned session,invoked;} msia_thread147;
static unsigned custom_thread147(void*parameter){msia_thread147*call=parameter;__atomic_store_n(&call->invoked,1,__ATOMIC_RELEASE);return call->body(call->session);}
unsigned msia_deferred147(unsigned session,unsigned type,const WCHAR*dll,const char*target,const char*data,msia_custom_result147*out){
 if(!out)return 87;*out=(msia_custom_result147){0};if(!msia_dll_type147(type)){out->engine_error=50;return 50;}if(!session||!dll||!dll[0]||!target||!target[0]||len8(target)>72||!data||len8(data)>4096){out->engine_error=87;return 87;}
 if(!msi_immediate147(session)){out->engine_error=6;return 1603;}HANDLE module=LoadLibraryW(dll);if(!module){out->engine_error=GetLastError();return 1603;}void*body=GetProcAddress(module,target);if(!body){out->engine_error=GetLastError();(void)FreeLibrary(module);return 1603;}
 unsigned error=msi_begin_deferred147(data);if(error){out->engine_error=error;(void)FreeLibrary(module);return 1603;}msia_thread147 call={body,session,0};unsigned thread_id=0;HANDLE thread=CreateThread(0,0,custom_thread147,&call,0,&thread_id);
 if(!thread){out->engine_error=GetLastError();msi_end_deferred147();(void)FreeLibrary(module);return 1603;}
 /* A failed join cannot release executable code while it may still run.
  * ExitProcess quiesces all owned threads; the durable installer journal stays. */
 if(WaitForSingleObject(thread,UINT32_MAX)!=0)fail8("The custom-action thread could not be joined. Installation recovery is required.");
 out->invoked=__atomic_load_n(&call.invoked,__ATOMIC_ACQUIRE);if(!GetExitCodeThread(thread,&out->body_status))out->engine_error=GetLastError();if(!CloseHandle(thread)&&!out->engine_error)out->engine_error=GetLastError();msi_end_deferred147();if(!FreeLibrary(module)&&!out->engine_error)out->engine_error=GetLastError();
 if(!out->invoked&&!out->engine_error)out->engine_error=31;if(out->engine_error)return 1603;if(out->body_status&&(type&0x40u)){out->continued=1;return 0;}return out->body_status;
}
