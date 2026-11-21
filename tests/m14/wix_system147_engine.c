/* Test-only session owner for the unchanged original deferred WiX action. */
#include "../../user/windows8/msi-plan147.h"
#include "../../user/windows8/msi-custom147.h"
__declspec(dllimport) uint64_t LoadLibraryW(const WCHAR*);
__declspec(dllimport) void *GetProcAddress(uint64_t,const char*);
__declspec(dllimport) int FreeLibrary(uint64_t);
unsigned msi_bind147(msia_plan147*);
void msi_unbind147(void);
unsigned msi_begin_deferred147(const char*);
void msi_end_deferred147(void);
__declspec(dllexport) unsigned TestOriginalAction147(void){
 const char*tools[]={"/System/Windows/Tools/cmd.exe","/System/Windows/Tools/xcopy.exe"};
 for(unsigned i=0;i<2;++i){w8_file_info info;if(stat8(tools[i],&info)||!info.size||open8(tools[i],1)>=0)fail8("Protected system helper missing or writable.");}
 void*source=0;unsigned bytes=load8("/Users/Owner/Downloads/npp.8.9.9.1.Installer.x64.msi",&source,8u*1024u*1024u);if(!bytes)fail8("Original package fixture is missing.");
 msia_plan147*p=msia_prepare147(source,bytes);if(msip_set147(&p->properties,"Privileged","1")||msip_set147(&p->properties,"ALLUSERS","1"))fail8("Test property session failed.");msia_cost147(p,"C:\\Users\\Owner");unsigned h=msi_bind147(p);if(!h)fail8("Test MSI session could not bind.");
 static const char*commands[]={
 "\"C:\\Windows\\SysWOW64\\xcopy.exe\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\" \"C:\\Users\\Owner\\Documents\\nativeLang.xml*\" /Y /Q",
 "\"C:\\Windows\\SysWOW64\\xcopy.exe\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\" \"C:\\Users\\Owner\\Documents\\Delete & test.xml*\" /Y /Q",
 "\"C:\\Windows\\System32\\cmd.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\\Delete & test.xml\"",
 "\"C:\\Windows\\System32\\cmd.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\\Delete & test.xml\"",
 "\"C:\\Windows\\SysWOW64\\xcopy.exe\" \"C:\\Users\\Owner\\Documents\\missing147.xml\" \"C:\\Users\\Owner\\Documents\\Must not exist.xml*\" /Y /Q",
 "\"C:\\Windows\\SysWOW64\\xcopy.exe\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\" \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml*\" /Y /Q",
 "\"C:\\Windows\\System32\\cmd.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\"",
 "\"C:\\Windows\\System32\\cmd.exe\" /C del /F /Q \"C:\\Users\\Owner\\Documents\\nativeLang.xml\" & del \"C:\\Users\\Owner\\Documents\\source-\xc3\xa9.xml\""};
 for(unsigned i=0;i<9;++i){unsigned type=i>=4&&i<8?MSIA_DEFERRED_CHECKED147:MSIA_DEFERRED_DLL147;msia_custom_result147 call;unsigned result=msia_deferred147(h,type,L"C:\\Program Files\\7-Zip\\wix147.dll","WixQuietExec",commands[i<8?i:4],&call);print8("M147_THREADED_ORIGINAL_WIX_ACTION=");number8(i);print8(" result=");number8(result);print8(" body=");number8(call.body_status);print8(" continued=");number8(call.continued);print8("\n");if(call.engine_error||!call.invoked||call.body_status!=(i>=4?1603u:0u)||result!=(i>=4&&i<8?1603u:0u)||call.continued!=(i==8))fail8("Native action thread or authored return handling failed.");}
 print8("M147_THREADED_ORIGINAL_WIX_COPY_DELETE_CONTINUE_PASS\n");msi_unbind147();msia_close147(p);free8(source);return 0;
}
