/* Test-only session owner for the unchanged original deferred WiX action. */
#include "../../user/windows8/msi-plan147.h"
__declspec(dllimport) uint64_t LoadLibraryW(const WCHAR*);
__declspec(dllimport) void *GetProcAddress(uint64_t,const char*);
__declspec(dllimport) int FreeLibrary(uint64_t);
unsigned msi_bind147(msia_plan147*);
void msi_unbind147(void);
unsigned msi_begin_deferred147(const char*);
void msi_end_deferred147(void);
__declspec(dllexport) unsigned TestOriginalAction147(void){
 void*source=0;unsigned bytes=load8("/Users/Owner/Downloads/npp.8.9.9.1.Installer.x64.msi",&source,8u*1024u*1024u);if(!bytes)fail8("Original package fixture is missing.");
 msia_plan147*p=msia_prepare147(source,bytes);if(msip_set147(&p->properties,"Privileged","1")||msip_set147(&p->properties,"ALLUSERS","1"))fail8("Test property session failed.");msia_cost147(p,"C:\\Users\\Owner");unsigned h=msi_bind147(p);if(!h)fail8("Test MSI session could not bind.");
 uint64_t module=LoadLibraryW(L"C:\\Program Files\\7-Zip\\wix147.dll");if(!module)fail8("The original WiX DLL could not load.");unsigned(*action)(unsigned)=GetProcAddress(module,"WixQuietExec");if(!action)fail8("Original WiX export is missing.");
 if(msi_begin_deferred147("\"C:\\Program Files\\7-Zip\\quiet-child147.exe\""))fail8("Test deferred phase failed.");print8("M147_ORIGINAL_WIX_ACTION_BEGIN\n");unsigned result=action(h);print8("M147_ORIGINAL_WIX_ACTION_RESULT=");number8(result);print8("\n");msi_end_deferred147();
 if(!FreeLibrary(module))fail8("The original action DLL could not unload.");msi_unbind147();msia_close147(p);free8(source);return result;
}
