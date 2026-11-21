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
 static const char*commands[]={
 "\"C:\\Program Files\\7-Zip\\xcopy147.exe\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\" \"C:\\Users\\Owner\\Documents\\nativeLang.xml*\" /Y /Q",
 "\"C:\\Program Files\\7-Zip\\xcopy147.exe\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\" \"C:\\Users\\Owner\\Documents\\Delete & test.xml*\" /Y /Q",
 "\"C:\\Program Files\\7-Zip\\cmd147.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\\Delete & test.xml\"",
 "\"C:\\Program Files\\7-Zip\\cmd147.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\\Delete & test.xml\"",
 "\"C:\\Program Files\\7-Zip\\xcopy147.exe\" \"C:\\Users\\Owner\\Documents\\missing147.xml\" \"C:\\Users\\Owner\\Documents\\Must not exist.xml*\" /Y /Q",
 "\"C:\\Program Files\\7-Zip\\xcopy147.exe\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml*\" /Y /Q",
 "\"C:\\Program Files\\7-Zip\\cmd147.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\"",
 "\"C:\\Program Files\\7-Zip\\cmd147.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\\nativeLang.xml\" & del \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\""};
 for(unsigned i=0;i<8;++i){if(msi_begin_deferred147(commands[i]))fail8("The test deferred phase could not begin.");print8("M147_ORIGINAL_WIX_FILE_ACTION_BEGIN=");number8(i);print8("\n");unsigned result=action(h);print8("M147_ORIGINAL_WIX_FILE_ACTION_RESULT=");number8(result);print8("\n");msi_end_deferred147();if(result!=(i>=4?1603u:0u))fail8("The original file action did not return the expected status.");}
 print8("M147_ORIGINAL_WIX_COPY_DELETE_FAILURE_PROPAGATION_PASS\n");unsigned result=0;
 if(!FreeLibrary(module))fail8("The original action DLL could not unload.");msi_unbind147();msia_close147(p);free8(source);return result;
}
