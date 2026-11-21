/* Resolve existing absolute names through the filesystem's actual long names.
 * The native volume does not generate DOS 8.3 aliases; none are fabricated. */
static unsigned MS f_GetLongPathNameW(const WCHAR*name,WCHAR*out,unsigned capacity){
 if(!name||(capacity&&!out)){last8(87);return 0;}
 if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)name,6,1,0,0)){last8(998);return 0;}
 if(!name[0]||name[1]!=':'||(name[2]!='\\'&&name[2]!='/')){last8(50);return 0;}
 char native[256],windows[512];if(!nativepath8(name,native))return 0;w8_file_info information;int64_t status=(int64_t)sys8(W8_SYS_FILE_OP143,0,15,(uint64_t)(uintptr_t)native,(uint64_t)(uintptr_t)&information,0);if(status<0){last8((unsigned)-status);return 0;}
 winpath8(native,windows,sizeof(windows));WCHAR wide[512];int units=utf8_to16(windows,wide,512);if(units<0){last8(206);return 0;}
 if(capacity<=(unsigned)units)return(unsigned)units+1;
 if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,((uint64_t)(unsigned)units+1)*2,2,0,0)){last8(998);return 0;}
 memcpy(out,wide,((size_t)(unsigned)units+1)*2);return(unsigned)units;
}
static unsigned MS f_GetShortPathNameW(const WCHAR*name,WCHAR*out,unsigned capacity){
 if(!name||(capacity&&!out)){last8(87);return 0;}w8_file_info information;if(!file_path_api143(15,name,&information,0))return 0;
 WCHAR copy[1024];unsigned units=0;while(units<1024&&name[units]){copy[units]=name[units];++units;}if(units==1024){last8(206);return 0;}copy[units]=0;
 /* A volume without stored short aliases returns its existing long-name path,
  * as permitted by the Windows API contract. No guessed alias is published. */
 if(capacity<=units)return units+1;if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,((uint64_t)units+1)*2,2,0,0)){last8(998);return 0;}memcpy(out,copy,((size_t)units+1)*2);return units;
}
