/* Owned clone only: seed a pre-existing language preference through real APIs. */
#include "../../user/windows8/runtime.h"
void msi8_execute(void){
 if(job8->command!=W8_PREVIEW&&job8->command!=W8_INSTALL&&job8->command!=W8_REMOVE)fail8("The language fixture requires an ordinary MSI operation.");
 init_win8();
 if(job8->command==W8_INSTALL){
  if(!equal8(job8->product_root,"/Applications/Windows/{A23B657D-838B-4C9B-8F9D-386E50C1A76B}"))fail8("The owned language fixture requires the original Notepad++ product.");
  typedef int (MS *create147)(HANDLE,const WCHAR*,unsigned,WCHAR*,unsigned,unsigned,void*,HANDLE*,unsigned*);
  typedef int (MS *set147)(HANDLE,const WCHAR*,unsigned,unsigned,const void*,unsigned);
  typedef int (MS *close147)(HANDLE);
  create147 create=(create147)resolve8("advapi32.dll","RegCreateKeyExW",0);set147 set=(set147)resolve8("advapi32.dll","RegSetValueExW",0);close147 close=(close147)resolve8("advapi32.dll","RegCloseKey",0);
  HANDLE key=0;unsigned disposition=0;static const WCHAR path[]={'S','o','f','t','w','a','r','e','\\','N','o','t','e','p','a','d','+','+','\\','L','a','n','g',0},name[]={'a','c','t','i','v','e',0},value[]={'f','r','e','n','c','h',0};
  if(!create||!set||!close||create(UINT64_C(0xffffffff80000002),path,0,0,0,0x10003u,0,&key,&disposition)||!key)fail8("The owned pre-existing language preference could not be opened.");
  unsigned status=set(key,name,0,1,value,sizeof(value));if(close(key)||status)fail8("The owned language preference could not be saved.");print8("M147_OWNED_EXISTING_FRENCH_PREFERENCE_SEEDED\n");
 }
 pe8_run("/System/Windows/Installer/msiexec.exe","");
}
