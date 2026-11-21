/* Real bounded session/property/record exports for native MSI custom actions. */
#include "msi-plan147.h"
#include "msi-record147.h"
#include "msi-text147.h"
__declspec(dllimport) void InitializeCriticalSection(void*);
__declspec(dllimport) void EnterCriticalSection(void*);
__declspec(dllimport) void LeaveCriticalSection(void*);
__declspec(dllimport) void DeleteCriticalSection(void*);
static uint64_t api_lock147[5];static unsigned initialized147,session147,epoch147;
static msia_plan147 *api_plan147;static msir_context147 records147;
static void *api_alloc147(void*c,size_t n){(void)c;return alloc8(n);}
static void api_free147(void*c,void*p){(void)c;free8(p);}
int EngacerMsiDllEntry147(void*module,unsigned reason,void*reserved){(void)module;(void)reserved;if(reason==1){InitializeCriticalSection(api_lock147);records147.alloc=api_alloc147;records147.release=api_free147;initialized147=1;}else if(reason==0&&initialized147){msir_destroy147(&records147);api_plan147=0;session147=0;initialized147=0;DeleteCriticalSection(api_lock147);}return 1;}
unsigned msi_bind147(msia_plan147*p){if(!initialized147||!p||api_plan147||epoch147==0xffffu)return 0;api_plan147=p;session147=0x14700000u|++epoch147;return session147;}
void msi_unbind147(void){if(!api_plan147)return;EnterCriticalSection(api_lock147);msir_destroy147(&records147);session147=0;api_plan147=0;LeaveCriticalSection(api_lock147);}
static int api_enter147(void){if(!initialized147)return 0;EnterCriticalSection(api_lock147);return 1;}
static void api_leave147(void){LeaveCriticalSection(api_lock147);}
#define MSI_EXPORT147 __declspec(dllexport)
MSI_EXPORT147 unsigned MsiCreateRecord(unsigned fields){if(!api_enter147())return 0;unsigned h=msir_create147(&records147,fields);api_leave147();return h;}
MSI_EXPORT147 unsigned MsiCloseHandle(unsigned h){if(!api_enter147())return 6;unsigned code;if(h&&h==session147){session147=0;code=0;}else code=msir_close147(&records147,h);api_leave147();return code;}
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
MSI_EXPORT147 unsigned MsiGetPropertyA(unsigned h,const char*name,char*out,unsigned*capacity){if(!api_enter147())return 6;unsigned n=0,code=h!=session147||!h?6:!msip_name147(name,&n)?87:msit_outansi147(msip_get147(&api_plan147->properties,name),out,capacity);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiGetPropertyW(unsigned h,const WCHAR*name,WCHAR*out,unsigned*capacity){char key[73];unsigned code=msit_fromwide147(name,key,sizeof(key));if(code)return code;if(!api_enter147())return 6;unsigned n=0;code=h!=session147||!h?6:!msip_name147(key,&n)?87:msit_outwide147(msip_get147(&api_plan147->properties,key),out,capacity);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiSetPropertyA(unsigned h,const char*name,const char*value){if(!api_enter147())return 6;unsigned code=h!=session147||!h?6:msip_set147(&api_plan147->properties,name,value);api_leave147();return code;}
MSI_EXPORT147 unsigned MsiSetPropertyW(unsigned h,const WCHAR*name,const WCHAR*value){char key[73],text[4097];unsigned code=msit_fromwide147(name,key,sizeof(key));if(!code&&value)code=msit_fromwide147(value,text,sizeof(text));return code?code:MsiSetPropertyA(h,key,value?text:0);}
MSI_EXPORT147 int MsiEvaluateConditionW(unsigned h,const WCHAR*condition){char text[4097];if(!condition)text[0]=0;else if(msit_fromwide147(condition,text,sizeof(text)))return 3;if(!api_enter147())return 3;int result=h!=session147||!h?3:msia_condition147(api_plan147,text);api_leave147();return result;}
MSI_EXPORT147 int MsiProcessMessage(unsigned h,unsigned type,unsigned record){if(!api_enter147())return -1;msir_record147*r=msir_find147(&records147,record);if(h!=session147||!h||!r){api_leave147();return -1;}unsigned kind=type&0xff000000u;if(kind!=0x04000000u&&kind!=0x03000000u&&kind!=0x02000000u&&kind!=0x01000000u){api_leave147();return -1;}char scratch[16];const char*s=msir_text147(&records147,record,0,scratch);print8("MSI: ");print8(s?s:"");for(unsigned i=1;i<=r->fields;++i){print8(" ");s=msir_text147(&records147,record,i,scratch);print8(s?s:"");}print8("\n");api_leave147();return 0;}
