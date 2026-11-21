/* Exact standard metadata ABI, sourced from the existing checked file layer. */
static int MS f_GetFileAttributesExW(const WCHAR*name,unsigned level,void*out){
 if(level||!out){last8(87);return 0;}if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,36,2,0,0)){last8(998);return 0;}
 w8_file_info info;if(!file_path_api143(15,name,&info,0))return 0;
 uint32_t data[9];data[0]=info.attributes;memcpy(data+1,info.time,24);data[7]=(uint32_t)(info.size>>32);data[8]=(uint32_t)info.size;memcpy(out,data,sizeof(data));return 1;
}
