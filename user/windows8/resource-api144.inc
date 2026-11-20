#include "resource-core144.h"
static HANDLE MS f_FindResourceW(HANDLE module,const WCHAR*name,const WCHAR*type){unsigned error;HANDLE result=pe8_find_resource(module,type,name,0x409,0,&error);if(error)last8(error);return result;}
static HANDLE MS f_FindResourceExW(HANDLE module,const WCHAR*type,const WCHAR*name,unsigned language){unsigned error;HANDLE result=pe8_find_resource(module,type,name,language,1,&error);if(error)last8(error);return result;}
static HANDLE MS f_LoadResource(HANDLE module,HANDLE resource){const void*data;unsigned bytes;unsigned error=pe8_resource_data(module,resource,&data,&bytes);if(error){last8(error);return 0;}return resource;}
static void *MS f_LockResource(HANDLE resource){const void*data;unsigned bytes;unsigned error=pe8_resource_data(0,resource,&data,&bytes);if(error){last8(error);return 0;}return(void*)data;}
static unsigned MS f_SizeofResource(HANDLE module,HANDLE resource){const void*data;unsigned bytes;unsigned error=pe8_resource_data(module,resource,&data,&bytes);if(error){last8(error);return 0;}return bytes;}
static int MS f_FreeResource(HANDLE resource){(void)resource;return 0; /* Obsolete Win32 API; module lifetime owns these bytes. */}
static int MS f_LoadStringW(HANDLE module,unsigned id,WCHAR*out,int capacity){
 if(!out||capacity<0){last8(87);return 0;}unsigned error;HANDLE handle=pe8_find_resource(module,(const WCHAR*)(uintptr_t)6,(const WCHAR*)(uintptr_t)((id>>4)+1),0x409,0,&error);if(error){last8(error);if(capacity)out[0]=0;return 0;}
 const void*data;unsigned bytes;error=pe8_resource_data(module,handle,&data,&bytes);if(error){last8(error);return 0;}const uint16_t*text;unsigned units;error=resource_string144(data,bytes,id&15,&text,&units);if(error){last8(error);return 0;}
 if(!capacity){*(const uint16_t**)out=text;return(int)units;}unsigned n=units;if(n>=(unsigned)capacity)n=(unsigned)capacity-1;memcpy(out,text,(size_t)n*2);out[n]=0;return(int)n;
}
