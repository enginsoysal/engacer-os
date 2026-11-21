/* Bounded synchronous copying through checked file handles and owner grants. */
static int MS f_CopyFileW(const WCHAR*from,const WCHAR*to,int fail_exists){
 w8_file_info source={0},target,completed;char destination[256];
 if(!nativepath_mode143(to,destination,4))return 0;
 HANDLE input=f_CreateFileW(from,0x80000000u,1,0,3,0x80,0);if(input==UINT64_MAX)return 0;
 unsigned error=0;HANDLE output=UINT64_MAX;
 if(file_api143(input,8,(uint64_t)(uintptr_t)&source,0)<0)error=f_GetLastError();
 else if(source.kind!=1)error=5;else if(source.size>64u*1024u*1024u)error=223;
 int64_t exists=(int64_t)sys8(W8_SYS_FILE_OP143,0,15,(uint64_t)(uintptr_t)destination,(uint64_t)(uintptr_t)&target,0);
 if(!error&&exists>=0){if(fail_exists)error=80;else if(target.kind!=1||(target.attributes&3))error=5;else if(source.identity&&source.identity==target.identity)error=32;}
 if(!error&&exists<0&&exists!=-2&&exists!=-3)error=(unsigned)-exists;
 if(!error){output=f_CreateFileW(to,0x40000000u,0,0,fail_exists?1:2,0x80,0);if(output==UINT64_MAX)error=f_GetLastError();}
 if(!error&&file_api143(output,W8_FILE_COPY148,input,0)<0)error=f_GetLastError();
 if(!error&&file_api143(output,8,(uint64_t)(uintptr_t)&completed,0)<0)error=f_GetLastError();
 if(!error){completed.attributes=source.attributes;completed.time[1]=sys8(W8_SYS_TIME,1,0,0,0,0);completed.time[2]=source.time[2];if(file_api143(output,9,(uint64_t)(uintptr_t)&completed,0)<0)error=f_GetLastError();}
 if(output!=UINT64_MAX&&file_api143(output,7,0,0)<0&&!error)error=f_GetLastError();
 if(file_api143(input,7,0,0)<0&&!error)error=f_GetLastError();
 if(error){last8(error);return 0;}return 1;
}
