/* Version queries read resources as data; they never load or execute a DLL. */
#include "version147.h"
static int version_read147(void*context,uint64_t offset,void*out,unsigned n){int file=*(int*)context;return seek8(file,(int64_t)offset,0)!=(int64_t)offset||read8(file,out,n)!=(int)n;}
static unsigned version_blob147(const WCHAR*name,uint8_t**data,unsigned*bytes){
 char path[256];if(!name){last8(87);return 0;}if(!nativepath8(name,path))return 0;w8_file_info info;int missing=stat8(path,&info);
 if(missing){unsigned separator=0,n=0;for(;n<512&&name[n];++n)separator|=name[n]=='/'||name[n]=='\\'||name[n]==':';if(!separator&&n<512){char leaf[256];if(f_WideCharToMultiByte(65001,0,name,-1,leaf,sizeof(leaf),0,0)){uint64_t module=pe8_module(leaf);const char*loaded=module?pe8_path(module):0;if(loaded){copy8(path,loaded,sizeof(path));missing=stat8(path,&info);}}}}
 if(missing){last8(2);return 0;}if(info.kind!=1||info.size>32u*1024u*1024u){last8(193);return 0;}int file=open8(path,0);if(file<0){last8(5);return 0;}ver_file147 input;ver_resource147 resource;unsigned error=ver_open147(&input,version_read147,&file,info.size,&resource);uint8_t*blob=0;
 if(!error){blob=alloc8(resource.bytes);if(!blob)error=8;else if(version_read147(&file,resource.offset,blob,resource.bytes))error=30;else{ver_node147 root;if(!ver_root147(blob,resource.bytes,&root))error=13;}}
 if(close8(file)&&!error)error=30;if(error){if(blob)free8(blob);last8(error);return 0;}*data=blob;*bytes=resource.bytes;return 1;
}
static unsigned MS f_GetFileVersionInfoSizeW(const WCHAR*name,unsigned*handle){
 if(handle){if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)handle,4,2,0,0)){last8(87);return 0;}*handle=0;}uint8_t*data=0;unsigned bytes=0;if(!version_blob147(name,&data,&bytes))return 0;free8(data);return bytes;
}
static int MS f_GetFileVersionInfoW(const WCHAR*name,unsigned handle,unsigned capacity,void*out){
 (void)handle;if(!capacity||!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,capacity,2,0,0)){last8(87);return 0;}uint8_t*data=0;unsigned bytes=0;if(!version_blob147(name,&data,&bytes))return 0;unsigned copy=bytes<capacity?bytes:capacity;memcpy(out,data,copy);free8(data);return 1;
}
static int MS f_VerQueryValueW(const void*block,const WCHAR*path,void**out,unsigned*length){
 if(!block||!path||!out||!length||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,sizeof(*out),2,0,0)||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)length,4,2,0,0)){last8(87);return 0;}*out=0;*length=0;
 if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)block,6,1,0,0)){last8(87);return 0;}unsigned bytes=ver_u16_147(block);if(bytes<8||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)block,bytes,1,0,0)){last8(13);return 0;}
 WCHAR checked[16*129+2];unsigned n=0;for(;n<sizeof(checked)/sizeof(checked[0]);++n){if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)(path+n),2,1,0,0)){last8(87);return 0;}checked[n]=path[n];if(!checked[n])break;}if(n==sizeof(checked)/sizeof(checked[0])){last8(87);return 0;}
 unsigned offset=0,count=0,error=ver_query147(block,bytes,checked,&offset,&count);if(error){last8(error);return 0;}*out=(uint8_t*)(uintptr_t)block+offset;*length=count;return 1;
}
