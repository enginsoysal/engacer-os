/* Bounded shared committed RAM sections; unsupported file/security modes refuse. */
static HANDLE mapping_open146(unsigned open,HANDLE file,unsigned protection,uint64_t bytes,unsigned access,const WCHAR*name){
 wmap_create146 request={.file=file,.bytes=bytes,.protection=protection,.access=access};
 if(name){if(wlen8(name)>=96){last8(206);return 0;}widecopy8(request.name,name,96);}
 wmap_result146 result;int64_t status=(int64_t)sys8(W8_SYS_MAPPING146,open?WMAP_OPEN146:WMAP_CREATE146,(uint64_t)(uintptr_t)&request,(uint64_t)(uintptr_t)&result,0,0);
 if(status<0){last8((unsigned)-status);return 0;}if(!open)last8(result.existed?183:0);return result.handle;
}
static HANDLE MS f_CreateFileMappingW(HANDLE file,void*attributes,unsigned protection,unsigned high,unsigned low,const WCHAR*name){
 if(attributes){last8(50);return 0;}return mapping_open146(0,file,protection,((uint64_t)high<<32)|low,0,name);
}
static HANDLE MS f_OpenFileMappingW(unsigned access,int inherit,const WCHAR*name){
 if(inherit){last8(50);return 0;}if(!name||!name[0]){last8(87);return 0;}return mapping_open146(1,0,0,0,access,name);
}
static void*MS f_MapViewOfFile(HANDLE mapping,unsigned access,unsigned high,unsigned low,size_t bytes){
 wmap_view146 request={.handle=mapping,.offset=((uint64_t)high<<32)|low,.bytes=bytes,.access=access};wmap_result146 result;
 int64_t status=(int64_t)sys8(W8_SYS_MAPPING146,WMAP_VIEW146,(uint64_t)(uintptr_t)&request,(uint64_t)(uintptr_t)&result,0,0);
 if(status<0){last8((unsigned)-status);return 0;}return(void*)(uintptr_t)result.handle;
}
static int MS f_UnmapViewOfFile(void*base){int64_t status=(int64_t)sys8(W8_SYS_MAPPING146,WMAP_UNMAP146,(uint64_t)(uintptr_t)base,0,0,0);if(status<0){last8((unsigned)-status);return 0;}return 1;}
