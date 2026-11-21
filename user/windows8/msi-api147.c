/* Real bounded session/property/record exports for native MSI custom actions. */
#include "msi-plan147.h"
#include "msi_db.h"
#include "msi-record147.h"
#include "msi-text147.h"
__declspec(dllimport) void InitializeCriticalSection(void*);
__declspec(dllimport) void EnterCriticalSection(void*);
__declspec(dllimport) void LeaveCriticalSection(void*);
__declspec(dllimport) void DeleteCriticalSection(void*);
static uint64_t api_lock147[5];static unsigned initialized147,session147,epoch147;
static unsigned deferred147,reboot147,database_generation147,database_handles147[16];
static msia_plan147 *api_plan147;static msir_context147 records147;
static void *api_alloc147(void*c,size_t n){(void)c;return alloc8(n);}
static void api_free147(void*c,void*p){(void)c;free8(p);}
int EngacerMsiDllEntry147(void*module,unsigned reason,void*reserved){(void)module;(void)reserved;if(reason==1){InitializeCriticalSection(api_lock147);records147.alloc=api_alloc147;records147.release=api_free147;initialized147=1;}else if(reason==0&&initialized147){msir_destroy147(&records147);memset(database_handles147,0,sizeof(database_handles147));api_plan147=0;session147=0;initialized147=0;DeleteCriticalSection(api_lock147);}return 1;}
unsigned msi_bind147(msia_plan147*p){if(!initialized147||!p||api_plan147||epoch147==0xffffu)return 0;api_plan147=p;session147=0x14700000u|++epoch147;return session147;}
void msi_unbind147(void){if(!api_plan147)return;EnterCriticalSection(api_lock147);msir_destroy147(&records147);memset(database_handles147,0,sizeof(database_handles147));session147=0;api_plan147=0;deferred147=reboot147=0;LeaveCriticalSection(api_lock147);}
/* The engine changes phase only after all prior custom-action threads finish. */
unsigned msi_begin_deferred147(const char*data){if(!api_plan147||deferred147)return 6;unsigned code=msip_set147(&api_plan147->properties,"CustomActionData",data);if(!code){memset(database_handles147,0,sizeof(database_handles147));deferred147=1;}return code;}
void msi_end_deferred147(void){if(api_plan147)msip_set147(&api_plan147->properties,"CustomActionData",0);deferred147=0;}
static const char*api_property147(const char*name){if(deferred147&&!equal8(name,"CustomActionData")&&!equal8(name,"ProductCode")&&!equal8(name,"UserSID"))return "";if(!deferred147&&equal8(name,"CustomActionData"))return "";return msip_get147(&api_plan147->properties,name);}
static int api_enter147(void){if(!initialized147)return 0;EnterCriticalSection(api_lock147);return 1;}
static void api_leave147(void){LeaveCriticalSection(api_lock147);}
unsigned msi_immediate147(unsigned h){if(!api_enter147())return 0;unsigned valid=api_plan147&&h&&h==session147&&!deferred147;api_leave147();return valid;}
unsigned msi_current147(void){if(!api_enter147())return 0;unsigned h=api_plan147&&!deferred147?session147:0;api_leave147();return h;}
#define MSI_EXPORT147 __declspec(dllexport)
static msia_plan147 *api_database147(unsigned handle){unsigned slot=handle&15;return api_plan147&&handle&&database_handles147[slot]==handle?api_plan147:0;}
/* Internal engine table access still checks the real database capability.
 * Deferred custom actions cannot obtain or reuse immediate database handles. */
unsigned msi_table147(unsigned handle,const char*name,msi8_table*out){
 if(!name||!out)return 87;if(!api_enter147())return 6;unsigned code=6;
 if(!deferred147&&api_database147(handle)){*out=msi8_table_open(name);code=0;}api_leave147();return code;
}
MSI_EXPORT147 unsigned MsiGetActiveDatabase(unsigned install){
 if(!api_enter147())return 0;unsigned handle=0;
 if(install&&install==session147&&!deferred147&&database_generation147<0xffffu)for(unsigned i=0;i<16;++i)if(!database_handles147[i]){handle=0x14900000u|(++database_generation147<<4)|i;database_handles147[i]=handle;break;}
 api_leave147();return handle;
}
MSI_EXPORT147 unsigned MsiCreateRecord(unsigned fields){if(!api_enter147())return 0;unsigned h=msir_create147(&records147,fields);api_leave147();return h;}
MSI_EXPORT147 unsigned MsiCloseHandle(unsigned h){if(!api_enter147())return 6;unsigned code;if(h&&h==session147){session147=0;code=0;}else if(api_database147(h)){database_handles147[h&15]=0;code=0;}else code=msir_close147(&records147,h);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiRecordGetFieldCount(unsigned h){if(!api_enter147())return 0;msir_record147*r=msir_find147(&records147,h);unsigned n=r?r->fields:0;api_leave147();return n;}
MSI_EXPORT147 unsigned MsiRecordClearData(unsigned h){if(!api_enter147())return 6;unsigned code=msir_clear147(&records147,h);api_leave147();return code;}
MSI_EXPORT147 int MsiRecordIsNull(unsigned h,unsigned field){if(!api_enter147())return 1;msir_record147*r=msir_find147(&records147,h);int result=!r||field>r->fields||!r->values[field].kind;api_leave147();return result;}
MSI_EXPORT147 unsigned MsiRecordSetInteger(unsigned h,unsigned field,int32_t value){if(!api_enter147())return 6;unsigned code=msir_integer147(&records147,h,field,value);api_leave147();return code;}
MSI_EXPORT147 int32_t MsiRecordGetInteger(unsigned h,unsigned field){if(!api_enter147())return INT32_MIN;int32_t value=msir_number147(&records147,h,field);api_leave147();return value;}
MSI_EXPORT147 unsigned MsiRecordSetStringA(unsigned h,unsigned field,const char*value){if(!api_enter147())return 6;unsigned code=msir_string147(&records147,h,field,value);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiRecordSetStringW(unsigned h,unsigned field,const WCHAR*value){if(!value)return MsiRecordSetStringA(h,field,0);char text[4097];unsigned code=msit_fromwide147(value,text,sizeof(text));return code?code:MsiRecordSetStringA(h,field,text);}
MSI_EXPORT147 unsigned MsiRecordGetStringW(unsigned h,unsigned field,WCHAR*out,unsigned*capacity){if(!api_enter147())return 6;char scratch[16];const char*s=msir_text147(&records147,h,field,scratch);unsigned code=s?msit_outwide147(s,out,capacity):msir_find147(&records147,h)?87:6;api_leave147();return code;}
MSI_EXPORT147 unsigned MsiRecordGetStringA(unsigned h,unsigned field,char*out,unsigned*capacity){if(!api_enter147())return 6;char scratch[16];const char*s=msir_text147(&records147,h,field,scratch);unsigned code=s?msit_outansi147(s,out,capacity):msir_find147(&records147,h)?87:6;api_leave147();return code;}
MSI_EXPORT147 unsigned MsiRecordDataSize(unsigned h,unsigned field){if(!api_enter147())return 0;msir_record147*r=msir_find147(&records147,h);unsigned result=0;if(r&&field<=r->fields){msir_field147*f=r->values+field;if(f->kind==2)result=4;else if(f->kind==1){unsigned at=0,n=len8(f->text);uint32_t cp;while(at<n){if(!msit_next147(f->text,n,&at,&cp)){result=0;break;}result+=cp>65535?2:1;}}}api_leave147();return result;}
MSI_EXPORT147 unsigned MsiGetPropertyA(unsigned h,const char*name,char*out,unsigned*capacity){if(!api_enter147())return 6;unsigned n=0,code=h!=session147||!h?6:!msip_name147(name,&n)?87:msit_outansi147(api_property147(name),out,capacity);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiGetPropertyW(unsigned h,const WCHAR*name,WCHAR*out,unsigned*capacity){char key[73];unsigned code=msit_fromwide147(name,key,sizeof(key));if(code)return code;if(!api_enter147())return 6;unsigned n=0;code=h!=session147||!h?6:!msip_name147(key,&n)?87:msit_outwide147(api_property147(key),out,capacity);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiSetPropertyA(unsigned h,const char*name,const char*value){if(!api_enter147())return 6;unsigned code=h!=session147||!h||deferred147?6:msip_set147(&api_plan147->properties,name,value);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiSetPropertyW(unsigned h,const WCHAR*name,const WCHAR*value){char key[73],text[4097];unsigned code=msit_fromwide147(name,key,sizeof(key));if(!code&&value)code=msit_fromwide147(value,text,sizeof(text));return code?code:MsiSetPropertyA(h,key,value?text:0);}
MSI_EXPORT147 int MsiEvaluateConditionW(unsigned h,const WCHAR*condition){char text[4097];if(!condition)text[0]=0;else if(msit_fromwide147(condition,text,sizeof(text)))return 3;if(!api_enter147())return 3;int result=h!=session147||!h||deferred147?3:msia_condition147(api_plan147,text);api_leave147();return result;}
/* MSI first substitutes numeric fields, then resolves property/file fields. */
static unsigned api_format147(unsigned install,unsigned record,char result[4097]){
 msir_record147*r=msir_find147(&records147,record);if(!r||(install&&install!=session147))return 6;
 char scratch[16],first[4097];const char*text=msir_text147(&records147,record,0,scratch);unsigned n=len8(text),used=0;
 for(unsigned at=0;at<n;){const char*value=0;unsigned end=at;
  if(text[at]=='['&&at+1<n&&text[at+1]>='0'&&text[at+1]<='9'){
   unsigned field=0;end=at+1;while(end<n&&text[end]>='0'&&text[end]<='9'){if(field>4096)return 87;field=field*10+(unsigned)(text[end++]-'0');}
   if(end<n&&text[end]==']'){value=msir_text147(&records147,record,field,scratch);if(!value)value="";++end;}
  }
  if(value){unsigned count=len8(value);if(count>4096-used)return 1816;memcpy(first+used,value,count);used+=count;at=end;}
  else{if(used==4096)return 1816;first[used++]=text[at++];}
 }first[used]=0;
 if(install){if(!deferred147)return msia_format147(api_plan147,first,result,4097);
  msip_session147 restricted={.alloc=api_alloc147,.release=api_free147};unsigned code=msip_set147(&restricted,"CustomActionData",api_property147("CustomActionData"));if(!code)code=msip_set147(&restricted,"ProductCode",api_property147("ProductCode"));if(!code)code=msip_format147(&restricted,first,result,4097,0,0);msip_destroy147(&restricted);return code;}
 msip_session147 empty={0};return msip_format147(&empty,first,result,4097,0,0);
}
MSI_EXPORT147 unsigned MsiFormatRecordW(unsigned install,unsigned record,WCHAR*out,unsigned*capacity){if(!api_enter147())return 6;char result[4097];unsigned code=api_format147(install,record,result);if(!code)code=msit_outwide147(result,out,capacity);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiFormatRecordA(unsigned install,unsigned record,char*out,unsigned*capacity){if(!api_enter147())return 6;char result[4097];unsigned code=api_format147(install,record,result);if(!code)code=msit_outansi147(result,out,capacity);api_leave147();return code;}
MSI_EXPORT147 int MsiProcessMessage(unsigned h,unsigned type,unsigned record){if(!api_enter147())return -1;msir_record147*r=msir_find147(&records147,record);if(h!=session147||!h||!r){api_leave147();return -1;}unsigned kind=type&0xff000000u;if(kind!=0x04000000u&&kind!=0x03000000u&&kind!=0x02000000u&&kind!=0x01000000u){api_leave147();return -1;}char result[4097];if(api_format147(h,record,result)){api_leave147();return -1;}print8("MSI: ");print8(result);print8("\n");api_leave147();return 0;}

MSI_EXPORT147 int MsiGetMode(unsigned h,unsigned mode){if(!api_enter147())return 0;int value=0;if(h&&h==session147){if(deferred147)value=mode==16;else if(mode==6||mode==7)value=(reboot147>>(mode-6))&1;else if(mode==2)value=api_property147("Installed")[0]!=0;}api_leave147();return value;}
MSI_EXPORT147 unsigned MsiSetMode(unsigned h,unsigned mode,int state){if(!api_enter147())return 6;unsigned code=0;if(!h||h!=session147)code=6;else if(mode!=6&&mode!=7)code=87;else if(state)reboot147|=1u<<(mode-6);else reboot147&=~(1u<<(mode-6));api_leave147();return code;}
MSI_EXPORT147 unsigned MsiGetTargetPathW(unsigned h,const WCHAR*name,WCHAR*out,unsigned*capacity){char key[73];unsigned code=msit_fromwide147(name,key,sizeof(key));if(code)return code;if(!api_enter147())return 6;code=6;if(h&&h==session147&&!deferred147){code=267;if(api_plan147->costed)for(unsigned i=0;i<api_plan147->directory_count;++i)if(equal8(key,api_plan147->directories[i].id)){code=msit_outwide147(api_plan147->directories[i].windows,out,capacity);break;}}api_leave147();return code;}
