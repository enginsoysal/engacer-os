/* Persistent kernel HKCU and a separately labelled legacy installed read view. */
static lock142 legacy_registry_lock143;
static struct {unsigned generation,access;} legacy_registry_caps143[16];
static unsigned legacy_registry_generation143;
static int registry_legacy_slot143(HANDLE handle){unsigned slot=(unsigned)(handle&15);return (handle&UINT64_C(0xfffffffff0000000))==UINT64_C(0xc0000000)&&registry_handles8[slot].live&&legacy_registry_caps143[slot].generation==((handle&0x0fffffffu)>>4)?(int)slot:-1;}
static int registry_api143(unsigned operation,w8_registry_request143*request,w8_registry_result143*result){request->result=(uint64_t)(uintptr_t)result;int64_t status=(int64_t)sys8(W8_SYS_REGISTRY143,operation,(uint64_t)(uintptr_t)request,0,0,0);return status<0?(int)-status:0;}
static int registry_predefined143(HANDLE root,unsigned value){return root==(HANDLE)value||root==(UINT64_C(0xffffffff00000000)|value);}
static int registry_open_legacy143(HANDLE root,const WCHAR*key,unsigned access,HANDLE*out){
 if(access&~0x20019u)return 5;lock_enter142(&legacy_registry_lock143);HANDLE old=0;int status=legacy_RegOpenKeyExW(root,key,0,access,&old);
 if(!status){unsigned slot=(unsigned)(old-0x4000);if(legacy_registry_generation143==0xffffffu){legacy_RegCloseKey(old);status=8;}else{legacy_registry_caps143[slot].generation=++legacy_registry_generation143;legacy_registry_caps143[slot].access=access;*out=UINT64_C(0xc0000000)|((uint64_t)legacy_registry_caps143[slot].generation<<4)|slot;}}
 lock_leave142(&legacy_registry_lock143);return status;
}
static int MS f_RegOpenKeyExW(HANDLE root,const WCHAR*key,unsigned options,unsigned access,HANDLE*out){
 if(!out)return 87;*out=0;if(options)return 50;
#ifndef ENGINE_M14
 if(registry_predefined143(root,0x80000002u))return registry_open_legacy143(root,key,access,out);
#endif
 w8_registry_request143 request={.root=root,.name=(uint64_t)(uintptr_t)key,.access=access};w8_registry_result143 result={0};int status=registry_api143(1,&request,&result);
 if(!status)*out=result.handle;else if(status==2&&(registry_predefined143(root,0x80000001u)
#ifdef ENGINE_M14
 ||registry_predefined143(root,0x80000002u)
#endif
 )&&!(access&~0x20019u)){return registry_open_legacy143(root,key,access,out);}
 return status;
}
static int MS f_RegCreateKeyExW(HANDLE root,const WCHAR*key,unsigned reserved,WCHAR*class_name,unsigned options,unsigned access,void*security,HANDLE*out,unsigned*disposition){
 if(!out||!key||reserved)return 87;*out=0;if(class_name||security||options)return 50;
#ifndef ENGINE_M14
 if(registry_predefined143(root,0x80000002u))return 5;
#endif
 w8_registry_request143 request={.root=root,.name=(uint64_t)(uintptr_t)key,.access=access,.flags=options};w8_registry_result143 result={0};int status=registry_api143(2,&request,&result);
 if(!status){*out=result.handle;if(disposition)*disposition=result.disposition;}return status;
}
static int MS f_RegCloseKey(HANDLE handle){
 if((handle&UINT64_C(0xfffffffff0000000))==UINT64_C(0xc0000000)){lock_enter142(&legacy_registry_lock143);int slot=registry_legacy_slot143(handle);int status=slot<0?6:legacy_RegCloseKey(0x4000+(unsigned)slot);lock_leave142(&legacy_registry_lock143);return status;}
 if(registry_predefined143(handle,0x80000002u))return 0;w8_registry_request143 request={.root=handle};return registry_api143(5,&request,0);
}
static int registry_root_view143(HANDLE root,unsigned access,unsigned create,HANDLE*out){
 if(!registry_predefined143(root,0x80000001u)
#ifdef ENGINE_M14
 &&!registry_predefined143(root,0x80000002u)
#endif
 ){*out=root;return 0;}static const WCHAR empty[]={0};
 return create?f_RegCreateKeyExW(root,empty,0,0,0,access,0,out,0):f_RegOpenKeyExW(root,empty,0,access,out);
}
static int MS f_RegQueryValueExW(HANDLE handle,const WCHAR*name,unsigned*reserved,unsigned*type,void*out,unsigned*bytes){
 if(reserved||(!bytes&&out))return 87;
 if((handle&UINT64_C(0xfffffffff0000000))==UINT64_C(0xc0000000)){lock_enter142(&legacy_registry_lock143);int slot=registry_legacy_slot143(handle);unsigned ignored=0;int status=slot<0?6:!(legacy_registry_caps143[slot].access&1)?5:legacy_RegQueryValueExW(0x4000+(unsigned)slot,name,0,type,out,bytes?bytes:&ignored);lock_leave142(&legacy_registry_lock143);return status;}
 HANDLE view=0;int status=registry_root_view143(handle,1,0,&view);if(status)return status;
 w8_registry_request143 request={.root=view,.name=(uint64_t)(uintptr_t)name,.data=(uint64_t)(uintptr_t)out,.bytes=bytes?*bytes:0};w8_registry_result143 result={0};status=registry_api143(4,&request,&result);
 if(!status||status==234){if(type)*type=result.type;if(bytes)*bytes=result.bytes;}if(view!=handle)f_RegCloseKey(view);return status;
}
static int MS f_RegSetValueExW(HANDLE handle,const WCHAR*name,unsigned reserved,unsigned type,const void*data,unsigned bytes){
 if(reserved||(!data&&bytes))return 87;if(bytes>2048)return 1450;if((handle&UINT64_C(0xfffffffff0000000))==UINT64_C(0xc0000000)
#ifndef ENGINE_M14
 ||registry_predefined143(handle,0x80000002u)
#endif
 )return 5;
 HANDLE view=0;int status=registry_root_view143(handle,3,1,&view);if(status)return status;w8_registry_request143 request={.root=view,.name=(uint64_t)(uintptr_t)name,.data=(uint64_t)(uintptr_t)data,.bytes=bytes,.type=type};status=registry_api143(3,&request,0);if(view!=handle)f_RegCloseKey(view);return status;
}
static int MS f_RegDeleteValueW(HANDLE handle,const WCHAR*name){HANDLE view=0;int status=registry_root_view143(handle,2,0,&view);if(status)return status;w8_registry_request143 request={.root=view,.name=(uint64_t)(uintptr_t)name};status=registry_api143(6,&request,0);if(view!=handle)f_RegCloseKey(view);return status;}
static int MS f_RegDeleteKeyW(HANDLE handle,const WCHAR*name){if(!name)return 87;
#ifndef ENGINE_M14
 if(registry_predefined143(handle,0x80000002u))return 5;
#endif
 w8_registry_request143 request={.root=handle,.name=(uint64_t)(uintptr_t)name};return registry_api143(10,&request,0);}
static int MS f_RegEnumValueW(HANDLE handle,unsigned index,WCHAR*name,unsigned*name_units,unsigned*reserved,unsigned*type,void*data,unsigned*bytes){
 if(!name_units||reserved||(!bytes&&data))return 87;HANDLE view=0;int status=registry_root_view143(handle,1,0,&view);if(status)return status;
 w8_registry_request143 request={.root=view,.index=index,.name_output=(uint64_t)(uintptr_t)name,.name_capacity=*name_units,.data=(uint64_t)(uintptr_t)data,.bytes=bytes?*bytes:0};w8_registry_result143 result={0};status=registry_api143(7,&request,&result);
 if(!status||status==234){*name_units=result.name_units;if(type)*type=result.type;if(bytes)*bytes=result.bytes;}if(view!=handle)f_RegCloseKey(view);return status;
}
static int MS f_RegEnumKeyExW(HANDLE handle,unsigned index,WCHAR*name,unsigned*name_units,unsigned*reserved,WCHAR*class_name,unsigned*class_units,FILETIME*time){
 if(!name_units||reserved)return 87;if(class_name)return 50;HANDLE view=0;int status=registry_root_view143(handle,8,0,&view);if(status)return status;
 w8_registry_request143 request={.root=view,.index=index,.name_output=(uint64_t)(uintptr_t)name,.name_capacity=*name_units};w8_registry_result143 result={0};status=registry_api143(9,&request,&result);
 if(!status||status==234){*name_units=result.name_units;if(class_units)*class_units=0;if(time){time->lo=(uint32_t)result.time;time->hi=(uint32_t)(result.time>>32);}}if(view!=handle)f_RegCloseKey(view);return status;
}
static int MS f_RegFlushKey(HANDLE handle){HANDLE view=0;int status=registry_root_view143(handle,1,0,&view);if(status)return status;w8_registry_request143 request={.root=view};status=registry_api143(8,&request,0);if(view!=handle)f_RegCloseKey(view);return status;}
#ifdef ENGINE_M14
static int MS f_RegQueryInfoKeyW(HANDLE handle,WCHAR*class_name,unsigned*class_units,unsigned*reserved,unsigned*subkeys,unsigned*max_subkey,unsigned*max_class,unsigned*values,unsigned*max_value_name,unsigned*max_value_bytes,unsigned*security_bytes,FILETIME*last_write){
 if(reserved||(class_name&&!class_units))return 87;if(security_bytes||last_write)return 50;
 unsigned*outputs[]={class_units,subkeys,max_subkey,max_class,values,max_value_name,max_value_bytes};for(unsigned i=0;i<7;++i)if(outputs[i]&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)outputs[i],4,3,0,0))return 998;
 if(class_name&&*class_units&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)class_name,2,2,0,0))return 998;
 HANDLE view=0;int status=registry_root_view143(handle,1,0,&view);if(status)return status;w8_registry_info148 info;w8_registry_request143 request={.root=view,.data=(uint64_t)(uintptr_t)&info,.bytes=sizeof(info)};status=registry_api143(12,&request,0);if(view!=handle)f_RegCloseKey(view);if(status)return status;
 if(class_name&&*class_units)*class_name=0;if(class_units)*class_units=0;if(subkeys)*subkeys=info.subkeys;if(max_subkey)*max_subkey=info.max_subkey_units;if(max_class)*max_class=info.max_class_units;if(values)*values=info.values;if(max_value_name)*max_value_name=info.max_value_name_units;if(max_value_bytes)*max_value_bytes=info.max_value_bytes;return 0;
}
#endif

#ifdef ENGINE_M14
/* Shell convenience deletion retains existing registry capability checks. */
static int MS f_SHDeleteValueW(HANDLE root,const WCHAR*subkey,const WCHAR*value){
 HANDLE opened=0;int status=f_RegOpenKeyExW(root,subkey,0,2,&opened);if(status)return status;
 status=f_RegDeleteValueW(opened,value);int closed=f_RegCloseKey(opened);return status?status:closed;
}
static int shell_delete_tree148(HANDLE root,const WCHAR*subkey,unsigned*budget,unsigned depth){
 if(depth>=32)return 206;if(!*budget)return 8;--*budget;
 HANDLE opened=0;int status=f_RegOpenKeyExW(root,subkey,0,0x1000bu,&opened);if(status)return status;
 for(;;){WCHAR child[768];unsigned units=768;status=f_RegEnumKeyExW(opened,0,child,&units,0,0,0,0);
  if(status==259){status=0;break;}if(status)break;status=shell_delete_tree148(opened,child,budget,depth+1);if(status)break;
 }
 /* NULL clears values/children but retains the key; an empty string deletes it. */
 if(!status&&!subkey)for(;;){WCHAR value[256];unsigned units=256;status=f_RegEnumValueW(opened,0,value,&units,0,0,0,0);
  if(status==259){status=0;break;}if(status)break;if(!*budget){status=8;break;}--*budget;status=f_RegDeleteValueW(opened,value);if(status)break;
 }
 int closed=f_RegCloseKey(opened);if(!status)status=closed;
 return status||!subkey?status:f_RegDeleteKeyW(root,subkey);
}
static int MS f_SHDeleteKeyW(HANDLE root,const WCHAR*subkey){unsigned budget=1024;return shell_delete_tree148(root,subkey,&budget,0);}
static int MS f_SHSetValueW(HANDLE root,const WCHAR*subkey,const WCHAR*name,unsigned type,const void*data,unsigned bytes){
 if(subkey&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)subkey,2,1,0,0))return 998;
 if(!subkey||!subkey[0])return f_RegSetValueExW(root,name,0,type,data,bytes);
 HANDLE opened=0;int status=f_RegCreateKeyExW(root,subkey,0,0,0,2,0,&opened,0);if(status)return status;
 status=f_RegSetValueExW(opened,name,0,type,data,bytes);int closed=f_RegCloseKey(opened);return status?status:closed;
}
#endif
