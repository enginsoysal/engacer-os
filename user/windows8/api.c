#include "runtime.h"
static uint32_t error8;
static void cleanup_thread144(void);
static WCHAR command8[1200],cwd8[512];
static lock142 cwd_lock143;
static char command_utf8[1200],argv_text8[1200],*argv8[64],**env8;
static char *command_pointer144=command_utf8;
static void *guard_lookup144(unsigned,const char*,unsigned);
static unsigned guard_address144(void*);
static unsigned argc8,console_mode8[3]={7,3,3};
static unsigned app_type8,exit_count8;static uint64_t exit_callbacks8[64],matherr8;
static uint32_t fmode8,commode8;static char **initenv8;
typedef struct {uint64_t ptr;uint32_t count,pad;uint64_t base;uint32_t flags,file,charbuf,bufsiz;uint64_t tmp;} crt_file8;
static crt_file8 iob8[3];
static uint64_t process_started8;
typedef struct {uint64_t base,size;unsigned live;} virtual8;
static virtual8 virtual_blocks8[128];static uint64_t next_virtual8=UINT64_C(0x128000000);
static uint64_t tls_values8[16][64],tls_used8;
static lock142 tls_lock142;
static void last8(unsigned e){error8=e;*(volatile uint32_t*)(uintptr_t)(teb142()+0x68)=e;}
static unsigned lower8(unsigned c){return c>='A'&&c<='Z'?c+32:c;}
static void widecopy8(WCHAR*out,const WCHAR*in,unsigned cap){unsigned n=0;while(n+1<cap&&in&&in[n]){out[n]=in[n];++n;}if(cap)out[n]=0;}
static void winpath8(const char*native,char*out,unsigned cap){
 if(!memcmp(native,job8->product_root,len8(job8->product_root))&&job8->product_root[0]){copy8(out,job8->windows_root,cap);append8(out,native+len8(job8->product_root),cap);}
 else if(!memcmp(native,job8->user_root,len8(job8->user_root))){copy8(out,"C:\\Users\\",cap);const char*name=job8->user_root;for(unsigned i=0;job8->user_root[i];++i)if(job8->user_root[i]=='/')name=job8->user_root+i+1;append8(out,name,cap);append8(out,native+len8(job8->user_root),cap);}
 else copy8(out,native,cap);for(unsigned i=0;out[i];++i)if(out[i]=='/')out[i]='\\';
}
static int nativepath_mode143(const WCHAR*wide,char*out,unsigned flags){
 w8_path_result143 result;WCHAR directory[512];lock_enter142(&cwd_lock143);widecopy8(directory,cwd8,512);lock_leave142(&cwd_lock143);
 int64_t status=(int64_t)sys8(W8_SYS_PATH143,(uint64_t)(uintptr_t)wide,(uint64_t)(uintptr_t)directory,(uint64_t)(uintptr_t)&result,flags,0);
 if(status<0){last8((unsigned)-status);return 0;}memcpy(out,result.native,256);return 1;
}
static int nativepath8(const WCHAR*wide,char*out){return nativepath_mode143(wide,out,0);}
static int MS f_MultiByteToWideChar(unsigned,unsigned,const char*,int,WCHAR*,int);
static int MS f_WideCharToMultiByte(unsigned,unsigned,const WCHAR*,int,char*,int,const char*,int*);
#include "environment143.inc"
static void callbacks8(void){while(exit_count8){uint64_t callback=exit_callbacks8[--exit_count8];if(callback)((void(MS*)(void))(uintptr_t)callback)();}}
static NORETURN void MS f_exit(unsigned code){callbacks8();pe8_exit(code);}
static NORETURN void MS f__exit(unsigned code){pe8_exit(code);}
static NORETURN void MS f_ExitProcess(unsigned code){pe8_exit(code);}
static void MS f__cexit(void){callbacks8();}
static void MS f__c_exit(void){exit_count8=0;}
static uint64_t MS f__onexit(uint64_t fn){if(exit_count8==64)return 0;exit_callbacks8[exit_count8++]=fn;return fn;}
static uint64_t MS f___dllonexit(uint64_t fn,uint64_t**begin,uint64_t**end){if(!begin||!end)return 0;size_t count=*begin&&*end>=*begin?(size_t)(*end-*begin):0;if(count>=64)return 0;uint64_t*p=realloc8(*begin,(count+1)*8);if(!p)return 0;p[count]=fn;*begin=p;*end=p+count+1;return fn;}
static void MS f__initterm(uint64_t*begin,uint64_t*end){if(!begin||!end||end<begin||end-begin>4096)fail8("Invalid CRT initializer table.");while(begin<end){uint64_t fn=*begin++;if(fn)((void(MS*)(void))(uintptr_t)fn)();}}
static void MS f___set_app_type(unsigned type){app_type8=type;}
static uint64_t MS f___setusermatherr(uint64_t handler){uint64_t previous=matherr8;matherr8=handler;return previous;}
static int MS f___getmainargs(int*argc,char***argv,char***env,int expand,void*startup){(void)startup;if(expand){last8(50);return -1;}env8=environment_crt143();if(!env8)return -1;initenv8=env8;*argc=(int)argc8;*argv=argv8;*env=env8;return 0;}
static char***MS f___p___initenv(void){initenv8=environment_crt143();return &initenv8;}
static void *MS f_malloc(size_t size){return alloc8(size);}
static void MS f_free(void*p){free8(p);}
static void *MS f_realloc(void*p,size_t size){return realloc8(p,size);}
static void *MS f_memcpy(void*d,const void*s,size_t n){return memcpy(d,s,n);}
static void *MS f_memset(void*d,int c,size_t n){return memset(d,c,n);}
static void *MS f_memmove(void*d,const void*s,size_t n){return memmove(d,s,n);}
static int MS f_memcmp(const void*a,const void*b,size_t n){return memcmp(a,b,n);}
static size_t MS f_strlen(const char*s){return strlen(s);}
static int MS f_strcmp(const char*a,const char*b){while(*a&&*a==*b){++a;++b;}return (uint8_t)*a-(uint8_t)*b;}
static int MS f_wcscmp(const WCHAR*a,const WCHAR*b){while(*a&&*a==*b){++a;++b;}return (int)*a-(int)*b;}
static char *MS f_strchr(const char*s,int c){do{if((uint8_t)*s==(uint8_t)c)return (char*)s;}while(*s++);return 0;}
static char *MS f_strstr(const char*a,const char*b){unsigned n=len8(b);if(!n)return (char*)a;for(;*a;++a)if(len8(a)>=n&&!memcmp(a,b,n))return (char*)a;return 0;}
static WCHAR *MS f_wcsstr(const WCHAR*a,const WCHAR*b){unsigned n=wlen8(b);if(!n)return (WCHAR*)a;for(;*a;++a)if(wlen8(a)>=n&&!memcmp(a,b,n*2))return (WCHAR*)a;return 0;}
static int MS f_fputc(int c,crt_file8*f){if(!f||f->file<1||f->file>2)return -1;char s[2]={(char)c,0};sys8(W8_SYS_OUTPUT,(uint64_t)s,1,0,0,0);return (uint8_t)c;}
static int MS f_fputs(const char*s,crt_file8*f){if(!f||f->file<1||f->file>2)return -1;print8(s);return 0;}
static int MS f_fflush(crt_file8*f){if(f&&(f<iob8||f>=iob8+3))return -1;return 0;}
static int MS f_fgetc(crt_file8*f){(void)f;return -1;}
static int MS f__isatty(int fd){return fd>=0&&fd<3;}
static int64_t MS f__get_osfhandle(int fd){return fd>=0&&fd<3?fd+1:-1;}
static WCHAR *MS f_GetCommandLineW(void){return command8;}
static char *MS f_GetCommandLineA(void){return command_utf8;}
static uint32_t MS f_GetLastError(void){return *(volatile uint32_t*)(uintptr_t)(teb142()+0x68);}
static void MS f_SetLastError(uint32_t error){last8(error);}
static uint32_t MS f_GetCurrentProcessId(void){return *(volatile uint32_t*)(uintptr_t)(teb142()+0x40);}
static uint32_t MS f_GetCurrentThreadId(void){return tid142();}
static HANDLE MS f_GetCurrentProcess(void){return UINT64_MAX;}
static HANDLE MS f_GetCurrentThread(void){return UINT64_MAX-1;}
static HANDLE MS f_GetStdHandle(int32_t kind){return kind==-10?1:kind==-11?2:kind==-12?3:UINT64_MAX;}
static uint32_t MS f_GetTickCount(void){return (uint32_t)sys8(W8_SYS_TIME,0,0,0,0,0);}
static int MS f_QueryPerformanceCounter(uint64_t*out){if(!out){last8(87);return 0;}*out=sys8(W8_SYS_TIME,0,0,0,0,0);return 1;}
static int MS f_QueryPerformanceFrequency(uint64_t*out){if(!out){last8(87);return 0;}*out=1000;return 1;}
static void MS f_GetSystemTimeAsFileTime(uint64_t*out){if(out)*out=sys8(W8_SYS_TIME,1,0,0,0,0);}
static uint32_t MS f_GetVersion(void){return 0x1db10106u;}
static int MS f_GetVersionExW(void*data){uint32_t*n=data;if(!n||(n[0]!=276&&n[0]!=284)){last8(87);return 0;}unsigned bytes=n[0];memset((uint8_t*)data+4,0,bytes-4);n[1]=6;n[2]=1;n[3]=7601;n[4]=2;return 1;}
static void MS f_GetSystemInfo(void*out){memset(out,0,48);*(uint16_t*)out=9;*(uint32_t*)((uint8_t*)out+4)=4096;*(uint64_t*)((uint8_t*)out+8)=W8_BASE;*(uint64_t*)((uint8_t*)out+16)=W8_LIMIT-1;*(uint64_t*)((uint8_t*)out+24)=1;*(uint32_t*)((uint8_t*)out+32)=1;*(uint32_t*)((uint8_t*)out+36)=8664;*(uint32_t*)((uint8_t*)out+40)=65536;*(uint16_t*)((uint8_t*)out+44)=6;}
static int MS f_GetProcessAffinityMask(HANDLE p,uint64_t*process,uint64_t*system){if(p!=UINT64_MAX||!process||!system){last8(87);return 0;}*process=*system=1;return 1;}
static int MS f_SetProcessAffinityMask(HANDLE p,uint64_t mask){if(p!=UINT64_MAX||mask!=1){last8(87);return 0;}return 1;}
static uint64_t MS f_SetThreadAffinityMask(HANDLE p,uint64_t mask){if((p!=UINT64_MAX-1&&p!=1)||mask!=1){last8(87);return 0;}return 1;}
static int MS f_GlobalMemoryStatusEx(void*out){if(!out||*(uint32_t*)out!=64){last8(87);return 0;}uint64_t total=sys8(W8_SYS_INFO,1,0,0,0,0),free=sys8(W8_SYS_INFO,2,0,0,0,0);uint64_t*v=(uint64_t*)out;*(uint32_t*)((uint8_t*)out+4)=total?(uint32_t)((total-free)*100/total):0;v[1]=total;v[2]=free;v[3]=total;v[4]=free;v[5]=32*1024*1024;v[6]=32*1024*1024;v[7]=0;return 1;}
static uint64_t MS f_GetLargePageMinimum(void){return 0;}
static void *MS f_VirtualAlloc(void*requested,size_t size,unsigned flags,unsigned protect){
 if(!size||size>24*1024*1024||(flags&~0x3000u)||!(flags&0x1000u)||(protect!=4&&protect!=2)){last8(50);return 0;}uint64_t bytes=(size+4095)&~UINT64_C(4095),base=(uint64_t)(uintptr_t)requested;
 if(!base){base=next_virtual8;next_virtual8+=(bytes+65535)&~UINT64_C(65535);}if(base<UINT64_C(0x128000000)||base+bytes>UINT64_C(0x138000000)||(base&4095)){last8(487);return 0;}
 unsigned slot=0;while(slot<128&&virtual_blocks8[slot].live)++slot;if(slot==128||sys8(W8_SYS_MAP,base,bytes,protect==4?3:1,0,0)){last8(8);return 0;}virtual_blocks8[slot]=(virtual8){base,bytes,1};return (void*)(uintptr_t)base;
}
static int MS f_VirtualFree(void*p,size_t size,unsigned type){uint64_t base=(uint64_t)(uintptr_t)p;for(unsigned i=0;i<128;++i)if(virtual_blocks8[i].live&&virtual_blocks8[i].base==base){virtual8*v=virtual_blocks8+i;if(type!=0x8000||size){last8(87);return 0;}if(sys8(W8_SYS_UNMAP,v->base,v->size,0,0,0)){last8(487);return 0;}v->live=0;return 1;}last8(487);return 0;}
static unsigned MS f_TlsAlloc(void){lock_enter142(&tls_lock142);for(unsigned i=0;i<64;++i)if(!(tls_used8&(UINT64_C(1)<<i))){tls_used8|=UINT64_C(1)<<i;for(unsigned t=0;t<16;++t)tls_values8[t][i]=0;lock_leave142(&tls_lock142);return i;}lock_leave142(&tls_lock142);last8(259);return UINT32_MAX;}
static int MS f_TlsFree(unsigned i){lock_enter142(&tls_lock142);int valid=i<64&&(tls_used8&(UINT64_C(1)<<i));if(valid){tls_used8&=~(UINT64_C(1)<<i);for(unsigned t=0;t<16;++t)tls_values8[t][i]=0;}lock_leave142(&tls_lock142);if(!valid)last8(87);return valid;}
static uint64_t MS f_TlsGetValue(unsigned i){lock_enter142(&tls_lock142);int valid=i<64&&(tls_used8&(UINT64_C(1)<<i));uint64_t value=valid?tls_values8[tid142()&255][i]:0;lock_leave142(&tls_lock142);last8(valid?0:87);return value;}
static int MS f_TlsSetValue(unsigned i,uint64_t value){lock_enter142(&tls_lock142);int valid=i<64&&(tls_used8&(UINT64_C(1)<<i));if(valid)tls_values8[tid142()&255][i]=value;lock_leave142(&tls_lock142);if(!valid)last8(87);return valid;}
static int MS f_IsProcessorFeaturePresent(unsigned feature){uint32_t a,b,c,d;__asm__ volatile("cpuid":"=a"(a),"=b"(b),"=c"(c),"=d"(d):"a"(1u),"c"(0));if(feature==6)return !!(d&(1u<<25));if(feature==10)return !!(d&(1u<<26));if(feature==13)return !!(d&(1u<<0));if(feature==17)return !!(c&(1u<<0));if(feature==23)return !!(c&(1u<<23));return 0;}
static int MS f_SystemFunction036(void*out,unsigned bytes){uint32_t a,b,c,d;__asm__ volatile("cpuid":"=a"(a),"=b"(b),"=c"(c),"=d"(d):"a"(1u),"c"(0));if(!(c&(1u<<30)))return 0;uint8_t*p=out;while(bytes){uint64_t v=0;unsigned char ok=0;for(unsigned retry=0;retry<16&&!ok;++retry)__asm__ volatile("rdrand %0; setc %1":"=r"(v),"=qm"(ok));if(!ok)return 0;unsigned n=bytes>8?8:bytes;memcpy(p,&v,n);p+=n;bytes-=n;}return 1;}
static void *MS f_SysAllocStringByteLen(const char*s,unsigned bytes){if(bytes>16*1024*1024)return 0;uint8_t*p=alloc8((size_t)bytes+6);if(!p)return 0;*(uint32_t*)p=bytes;if(s)memcpy(p+4,s,bytes);else memset(p+4,0,bytes);p[4+bytes]=p[5+bytes]=0;return p+4;}
static WCHAR *MS f_SysAllocStringLen(const WCHAR*s,unsigned len){if(len>8*1024*1024)return 0;return f_SysAllocStringByteLen((const char*)s,len*2);}
static WCHAR *MS f_SysAllocString(const WCHAR*s){return s?f_SysAllocStringLen(s,wlen8(s)):0;}
static void MS f_SysFreeString(void*s){if(s)free8((uint8_t*)s-4);}
static unsigned MS f_SysStringLen(const void*s){return s?(*(const uint32_t*)((const uint8_t*)s-4))/2:0;}
static unsigned MS f_SysStringByteLen(const void*s){return s?*(const uint32_t*)((const uint8_t*)s-4):0;}
static int MS f_VariantClear(void*v){if(!v)return (int)0x80070057u;if(*(uint16_t*)v==8)f_SysFreeString(*(void**)((uint8_t*)v+8));memset(v,0,16);return 0;}
static int MS f_VariantCopy(void*out,const void*in){if(!out||!in)return (int)0x80070057u;if(out==in)return 0;f_VariantClear(out);memcpy(out,in,16);if(*(const uint16_t*)in==8){void*s=*(void*const*)((const uint8_t*)in+8);void*copy=f_SysAllocStringByteLen(s,f_SysStringByteLen(s));if(s&&!copy){memset(out,0,16);return (int)0x8007000eu;}*(void**)((uint8_t*)out+8)=copy;}return 0;}

static int64_t file_api143(HANDLE handle,unsigned operation,uint64_t a,uint64_t b){
 int64_t result=(int64_t)sys8(W8_SYS_FILE_OP143,handle,operation,a,b,0);if(result<0)last8((unsigned)-result);return result;
}
static HANDLE MS f_CreateFileW(const WCHAR*name,unsigned access,unsigned share,void*security,unsigned creation,unsigned flags,HANDLE template){
 if(security||template){last8(50);return UINT64_MAX;}if(access&~0xc0010180u||share&~7u){last8(87);return UINT64_MAX;}
 if(flags&~0x0c0000a7u){last8(50);return UINT64_MAX;}if(flags&0x08000000u){last8(50);return UINT64_MAX;}
 w8_file_request143 request={.access=((access&0x80000000u)?9u:0u)|((access&0x40000000u)?18u:0u)|((access&0x10000u)?4u:0u)|((access&0x80u)?8u:0u)|((access&0x100u)?16u:0u),.share=share,.creation=creation,.flags=flags&0x040000a7u};
 if(!nativepath8(name,request.path))return UINT64_MAX;
 w8_file_info info;int exists=!stat8(request.path,&info);
 int64_t result=(int64_t)sys8(W8_SYS_FILE_OPEN143,(uint64_t)&request,0,0,0,0);if(result<0){last8((unsigned)-result);return UINT64_MAX;}
 last8(exists&&(creation==2||creation==4)?183:0);return (HANDLE)result;
}
static int MS f_ReadFile(HANDLE h,void*out,unsigned size,unsigned*got,void*overlapped){
 if(got)*got=0;if(!got||overlapped){last8(87);return 0;}if(h==1)return 1;
 unsigned total=0;while(total<size){unsigned count=size-total;if(count>4096)count=4096;int64_t read=file_api143(h,1,(uint64_t)(uintptr_t)((uint8_t*)out+total),count);if(read<0){*got=total;return 0;}total+=(unsigned)read;if((unsigned)read<count)break;}
 if(!size&&file_api143(h,1,(uint64_t)(uintptr_t)out,0)<0)return 0;*got=total;return 1;
}
static int MS f_WriteFile(HANDLE h,const void*in,unsigned size,unsigned*written,void*overlapped){
 if(written)*written=0;if(!written||overlapped){last8(87);return 0;}if(h==2||h==3){const uint8_t*p=in;unsigned remain=size;while(remain){unsigned n=remain>4096?4096:remain;if((int64_t)sys8(W8_SYS_OUTPUT,(uint64_t)p,n,0,0,0)<0){last8(29);return 0;}p+=n;remain-=n;}*written=size;return 1;}
 unsigned total=0;while(total<size){unsigned count=size-total;if(count>4096)count=4096;int64_t n=file_api143(h,2,(uint64_t)(uintptr_t)((const uint8_t*)in+total),count);if(n<0){*written=total;return 0;}total+=(unsigned)n;}
 if(!size&&file_api143(h,2,(uint64_t)(uintptr_t)in,0)<0)return 0;*written=total;return 1;
}
static unsigned MS f_SetFilePointer(HANDLE h,int32_t low,int32_t*high,unsigned method){
 int64_t offset=high?(int64_t)(((uint64_t)(uint32_t)*high<<32)|(uint32_t)low):(int64_t)low;
 int64_t result=file_api143(h,3,(uint64_t)offset,method);if(result<0)return UINT32_MAX;if(high)*high=(int32_t)((uint64_t)result>>32);last8(0);return (unsigned)result;
}
static int MS f_SetFilePointerEx(HANDLE h,int64_t distance,int64_t*position,unsigned method){int64_t result=file_api143(h,3,(uint64_t)distance,method);if(result<0)return 0;if(position)*position=result;return 1;}
static unsigned MS f_GetFileSize(HANDLE h,unsigned*high){int64_t result=file_api143(h,4,0,0);if(result<0)return UINT32_MAX;if(high)*high=(unsigned)((uint64_t)result>>32);last8(0);return (unsigned)result;}
static int MS f_GetFileSizeEx(HANDLE h,uint64_t*out){if(!out){last8(87);return 0;}int64_t result=file_api143(h,4,0,0);if(result<0)return 0;*out=(uint64_t)result;return 1;}
static int MS f_SetEndOfFile(HANDLE h){return file_api143(h,5,0,0)>=0;}
static int MS f_FlushFileBuffers(HANDLE h){return file_api143(h,6,0,0)>=0;}
typedef struct {uint64_t internal,high;uint32_t offset,offset_high;uint64_t event;} overlapped143;
static int MS f_LockFileEx(HANDLE h,unsigned flags,unsigned reserved,unsigned low,unsigned high,overlapped143*overlapped){
 if(!overlapped||reserved||(flags&~3u)){last8(87);return 0;}if(overlapped->event){last8(50);return 0;}
 w8_file_lock_request143 request={.offset=((uint64_t)overlapped->offset_high<<32)|overlapped->offset,.length=((uint64_t)high<<32)|low,.flags=flags};return file_api143(h,12,(uint64_t)&request,0)>=0;
}
static int MS f_UnlockFileEx(HANDLE h,unsigned reserved,unsigned low,unsigned high,overlapped143*overlapped){
 if(!overlapped||reserved){last8(87);return 0;}if(overlapped->event){last8(50);return 0;}
 w8_file_lock_request143 request={.offset=((uint64_t)overlapped->offset_high<<32)|overlapped->offset,.length=((uint64_t)high<<32)|low};return file_api143(h,13,(uint64_t)&request,0)>=0;
}
static int MS f_LockFile(HANDLE h,unsigned offset,unsigned offset_high,unsigned low,unsigned high){overlapped143 request={.offset=offset,.offset_high=offset_high};return f_LockFileEx(h,3,0,low,high,&request);}
static int MS f_UnlockFile(HANDLE h,unsigned offset,unsigned offset_high,unsigned low,unsigned high){overlapped143 request={.offset=offset,.offset_high=offset_high};return f_UnlockFileEx(h,0,low,high,&request);}
static int MS f_GetFileInformationByHandle(HANDLE h,void*out){
 if(!out){last8(87);return 0;}w8_file_info info;if(file_api143(h,8,(uint64_t)&info,0)<0)return 0;
 memset(out,0,52);uint8_t*b=out;*(uint32_t*)b=info.attributes;memcpy(b+4,info.time,24);*(uint32_t*)(b+28)=0x454e474e;*(uint32_t*)(b+32)=(uint32_t)(info.size>>32);*(uint32_t*)(b+36)=(uint32_t)info.size;*(uint32_t*)(b+40)=1;*(uint32_t*)(b+44)=(uint32_t)(info.identity>>32);*(uint32_t*)(b+48)=(uint32_t)info.identity;return 1;
}
static int MS f_SetFileTime(HANDLE h,const FILETIME*creation,const FILETIME*access,const FILETIME*write){
 w8_file_info info;if(file_api143(h,8,(uint64_t)&info,0)<0)return 0;if(creation)memcpy(info.time,creation,8);if(access)memcpy(info.time+1,access,8);if(write)memcpy(info.time+2,write,8);return file_api143(h,9,(uint64_t)&info,0)>=0;
}
static int file_path_api143(unsigned operation,const WCHAR*name,w8_file_info*information,unsigned attributes){char path[256];if(!nativepath8(name,path))return 0;int64_t status=(int64_t)sys8(W8_SYS_FILE_OP143,0,operation,(uint64_t)path,information?(uint64_t)information:attributes,0);if(status<0){last8((unsigned)-status);return 0;}return 1;}
static unsigned MS f_GetFileAttributesW(const WCHAR*name){w8_file_info information;if(!file_path_api143(15,name,&information,0))return UINT32_MAX;return information.attributes;}
static int MS f_SetFileAttributesW(const WCHAR*name,unsigned attributes){return file_path_api143(14,name,0,attributes);}
static int MS f_CreateDirectoryW(const WCHAR*name,void*security){if(security){last8(50);return 0;}return file_path_api143(16,name,0,0);}
static int MS f_DeleteFileW(const WCHAR*name){w8_file_info information;if(!file_path_api143(15,name,&information,0))return 0;if(information.kind!=1){last8(5);return 0;}return file_path_api143(10,name,0,0);}
static int MS f_RemoveDirectoryW(const WCHAR*name){return file_path_api143(17,name,0,0);}
static int MS f_MoveFileExW(const WCHAR*from,const WCHAR*to,unsigned flags){char a[256],b[256];if(flags&~1u){last8(50);return 0;}if(!nativepath8(from,a)||!nativepath_mode143(to,b,4))return 0;int64_t result=(int64_t)sys8(W8_SYS_FILE_OP143,0,11,(uint64_t)a,(uint64_t)b,flags);if(result<0){last8((unsigned)-result);return 0;}return 1;}
static int MS f_MoveFileW(const WCHAR*a,const WCHAR*b){return f_MoveFileExW(a,b,0);}
static int MS f_MoveFileWithProgressW(const WCHAR*a,const WCHAR*b,uint64_t callback,void*data,unsigned flags){if(callback){last8(50);return 0;}(void)data;return f_MoveFileExW(a,b,flags);}
static int MS f_CreateHardLinkW(const WCHAR*a,const WCHAR*b,void*c){(void)a;(void)b;(void)c;last8(50);return 0;}
static unsigned MS f_GetFullPathNameW(const WCHAR*name,unsigned cap,WCHAR*out,WCHAR**part){
 if(part)*part=0;if(!name||(cap&&!out)){last8(87);return 0;}w8_path_result143 result;WCHAR directory[512];
 lock_enter142(&cwd_lock143);widecopy8(directory,cwd8,512);lock_leave142(&cwd_lock143);
 int64_t status=(int64_t)sys8(W8_SYS_PATH143,(uint64_t)(uintptr_t)name,(uint64_t)(uintptr_t)directory,(uint64_t)(uintptr_t)&result,3,0);
 if(status<0){last8((unsigned)-status);return 0;}unsigned n=wlen8(result.windows);if(cap<=n)return n+1;widecopy8(out,result.windows,cap);
 if(part&&n&&out[n-1]!='\\'){unsigned at=n;while(at&&out[at-1]!='\\')--at;*part=out+at;}return n;
}
static unsigned MS f_GetFullPathNameA(const char*name,unsigned cap,char*out,char**part){
 if(part)*part=0;if(!name||(cap&&!out)){last8(87);return 0;}WCHAR input[1024],full[512];
 if(utf8_to16(name,input,1024)<0){last8(len8(name)>=1024?206:1113);return 0;}unsigned count=f_GetFullPathNameW(input,512,full,0);if(!count)return 0;
 char text[2048];if(utf16_to8(full,text,sizeof(text))<0){last8(1113);return 0;}unsigned bytes=len8(text);if(cap<=bytes)return bytes+1;memcpy(out,text,bytes+1);
 if(part&&bytes&&out[bytes-1]!='\\'){unsigned at=bytes;while(at&&out[at-1]!='\\')--at;*part=out+at;}return bytes;
}
static unsigned MS f_GetCurrentDirectoryW(unsigned cap,WCHAR*out){
 lock_enter142(&cwd_lock143);unsigned n=wlen8(cwd8);if(cap<=n){lock_leave142(&cwd_lock143);return n+1;}widecopy8(out,cwd8,cap);lock_leave142(&cwd_lock143);return n;
}
static int MS f_SetCurrentDirectoryW(const WCHAR*name){
 char path[256];w8_file_info info;if(!nativepath8(name,path))return 0;if(stat8(path,&info)||info.kind!=2){last8(3);return 0;}
 char win[512];WCHAR directory[512];winpath8(path,win,sizeof(win));if(utf8_to16(win,directory,512)<0){last8(206);return 0;}
 lock_enter142(&cwd_lock143);widecopy8(cwd8,directory,512);lock_leave142(&cwd_lock143);return 1;
}
#include "temporary143.inc"
static int MS f_GetDiskFreeSpaceExW(const WCHAR*root,uint64_t*available,uint64_t*total,uint64_t*free){if(root&&((root[0]!='C'&&root[0]!='c')||root[1]!=':')){last8(3);return 0;}uint64_t space=sys8(W8_SYS_INFO,3,0,0,0,0);if(available)*available=space;if(free)*free=space;if(total)*total=sys8(W8_SYS_INFO,4,0,0,0,0);return 1;}
static int MS f_GetDiskFreeSpaceW(const WCHAR*root,unsigned*sectors,unsigned*bytes,unsigned*free,unsigned*total){uint64_t a=0,b=0;if(!f_GetDiskFreeSpaceExW(root,&a,&b,0))return 0;if(sectors)*sectors=8;if(bytes)*bytes=512;if(free)*free=(unsigned)(a/4096);if(total)*total=(unsigned)(b/4096);return 1;}
static unsigned MS f_GetLogicalDriveStringsW(unsigned cap,WCHAR*out){if(cap<5)return 5;out[0]='C';out[1]=':';out[2]='\\';out[3]=out[4]=0;return 4;}
typedef struct {unsigned live,index,single,stream,generation;char folder[256],pattern[256];w8_file_info item;} find8;
static find8 finds8[16];static lock142 find_lock143;static unsigned find_generation143;
static HANDLE find_token143(unsigned slot){return UINT64_C(0xe0000000)|((uint64_t)finds8[slot].generation<<4)|slot;}
static int find_slot143(HANDLE handle){unsigned slot=(unsigned)(handle&15);return (handle&UINT64_C(0xfffffffff0000000))==UINT64_C(0xe0000000)&&finds8[slot].live&&finds8[slot].generation==((handle&0x0fffffffu)>>4)?(int)slot:-1;}
static void find_data8(const w8_file_info*info,void*out){memset(out,0,592);uint8_t*b=out;*(uint32_t*)b=info->attributes;memcpy(b+4,info->time,24);*(uint32_t*)(b+28)=(uint32_t)(info->size>>32);*(uint32_t*)(b+32)=(uint32_t)info->size;utf8_to16(info->name,(WCHAR*)(b+44),260);}
static int next_find8(find8*search,void*out){
 if(search->single){if(search->index)return 0;search->index=1;find_data8(&search->item,out);return 1;}
 for(;;){int64_t next=(int64_t)sys8(W8_SYS_FILE_OP143,0,18,(uint64_t)search->folder,(uint64_t)&search->item,search->index);if(next<0){last8((unsigned)-next);return -1;}if(!next)return 0;search->index=(unsigned)next;
  int64_t matched=(int64_t)sys8(W8_SYS_TEXT143,2,(uint64_t)search->pattern,(uint64_t)search->item.name,0,0);if(matched<0){last8((unsigned)-matched);return -1;}if(matched){find_data8(&search->item,out);return 1;}}
}
static HANDLE MS f_FindFirstFileW(const WCHAR*name,void*out){
 char path[256];if(!out){last8(87);return UINT64_MAX;}if(!nativepath_mode143(name,path,1))return UINT64_MAX;lock_enter142(&find_lock143);
 unsigned slot=0;while(slot<16&&finds8[slot].live)++slot;if(slot==16||find_generation143==0xffffffu){lock_leave142(&find_lock143);last8(4);return UINT64_MAX;}
 find8*search=finds8+slot;memset(search,0,sizeof(*search));unsigned wild=0;for(unsigned i=0;path[i];++i)if(path[i]=='*'||path[i]=='?')wild=1;
 if(!wild){int64_t status=(int64_t)sys8(W8_SYS_FILE_OP143,0,15,(uint64_t)path,(uint64_t)&search->item,0);if(status<0){lock_leave142(&find_lock143);last8((unsigned)-status);return UINT64_MAX;}search->single=1;}
 else{char*last=0;for(unsigned i=0;path[i];++i)if(path[i]=='/')last=path+i;if(!last){lock_leave142(&find_lock143);last8(3);return UINT64_MAX;}copy8(search->pattern,last+1,256);*last=0;copy8(search->folder,path,256);}
 int found=next_find8(search,out);if(found<=0){memset(search,0,sizeof(*search));lock_leave142(&find_lock143);if(!found)last8(2);return UINT64_MAX;}
 search->live=1;search->generation=++find_generation143;HANDLE result=find_token143(slot);lock_leave142(&find_lock143);return result;
}
static int MS f_FindNextFileW(HANDLE handle,void*out){
 if(!out){last8(87);return 0;}lock_enter142(&find_lock143);int slot=find_slot143(handle);if(slot<0||finds8[slot].stream){lock_leave142(&find_lock143);last8(6);return 0;}int found=next_find8(finds8+slot,out);lock_leave142(&find_lock143);if(!found)last8(18);return found>0;
}
static int MS f_FindClose(HANDLE handle){lock_enter142(&find_lock143);int slot=find_slot143(handle);if(slot<0){lock_leave142(&find_lock143);last8(6);return 0;}memset(finds8+slot,0,sizeof(find8));lock_leave142(&find_lock143);return 1;}
static HANDLE MS f_FindFirstStreamW(const WCHAR*name,unsigned level,void*out,unsigned flags){
 if(!out){last8(87);return UINT64_MAX;}if(level||flags){last8(50);return UINT64_MAX;}w8_file_info info;if(!file_path_api143(15,name,&info,0))return UINT64_MAX;if(info.kind!=1){last8(50);return UINT64_MAX;}
 lock_enter142(&find_lock143);unsigned slot=0;while(slot<16&&finds8[slot].live)++slot;if(slot==16||find_generation143==0xffffffu){lock_leave142(&find_lock143);last8(4);return UINT64_MAX;}
 memset(out,0,600);*(uint64_t*)out=info.size;utf8_to16("::$DATA",(WCHAR*)((uint8_t*)out+8),296);memset(finds8+slot,0,sizeof(find8));finds8[slot].live=finds8[slot].stream=1;finds8[slot].generation=++find_generation143;HANDLE result=find_token143(slot);lock_leave142(&find_lock143);return result;
}
static int MS f_FindNextStreamW(HANDLE handle,void*out){if(!out){last8(87);return 0;}lock_enter142(&find_lock143);int slot=find_slot143(handle);unsigned valid=slot>=0&&finds8[slot].stream;lock_leave142(&find_lock143);last8(valid?38:6);return 0;}
static int MS f_DeviceIoControl(HANDLE h,unsigned code,void*in,unsigned in_bytes,void*out,unsigned out_bytes,unsigned*returned,void*overlap){(void)code;(void)in;(void)in_bytes;(void)out;(void)out_bytes;(void)overlap;if(returned)*returned=0;last8(h>=256&&h<288?1:6);return 0;}

typedef struct {uint64_t debug;int32_t lock,recursion;uint64_t owner,semaphore,spin;} critical8;
static void MS f_InitializeCriticalSection(critical8*c){memset(c,0,sizeof(*c));c->lock=-1;}
static int MS f_InitializeCriticalSectionAndSpinCount(critical8*c,unsigned spin){f_InitializeCriticalSection(c);c->spin=spin;return 1;}
static int MS f_InitializeCriticalSectionEx(critical8*c,unsigned spin,unsigned flags){if(flags&~0x1000000u){last8(87);return 0;}return f_InitializeCriticalSectionAndSpinCount(c,spin);}
static void MS f_EnterCriticalSection(critical8*c){uint64_t self=tid142();for(;;){uint64_t owner=__atomic_load_n(&c->owner,__ATOMIC_ACQUIRE);if(owner==self){++c->recursion;return;}if(!owner&&__atomic_compare_exchange_n(&c->owner,&owner,self,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED)){c->recursion=1;c->lock=0;return;}if(owner)sys8(W8_SYS_PARK,(uint64_t)(uintptr_t)&c->owner,owner,UINT32_MAX,0,0);}}
static int MS f_TryEnterCriticalSection(critical8*c){uint64_t self=tid142(),owner=0;if(c->owner==self){++c->recursion;return 1;}if(!__atomic_compare_exchange_n(&c->owner,&owner,self,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED))return 0;c->recursion=1;c->lock=0;return 1;}
static void MS f_LeaveCriticalSection(critical8*c){if(c->owner!=tid142()||c->recursion<=0)fail8("A Windows critical section was released without ownership.");if(!--c->recursion){c->lock=-1;__atomic_store_n(&c->owner,0,__ATOMIC_RELEASE);sys8(W8_SYS_WAKE,(uint64_t)(uintptr_t)&c->owner,UINT32_MAX,0,0,0);}}
static void MS f_DeleteCriticalSection(critical8*c){if(c->owner||c->recursion)fail8("A Windows process deleted an owned critical section.");memset(c,0,sizeof(*c));}
#include "sync142.inc"
static unsigned MS f_ResumeThread(HANDLE h){int64_t result=(int64_t)sys8(W8_SYS_THREAD_RESUME,h,0,0,0,0);if(result<0)last8(6);return (unsigned)result;}
static NORETURN void MS f_ExitThread(unsigned code){if(sys8(W8_SYS_THREAD_BEGIN_EXIT,0,0,0,0,0)==1)pe8_exit(code);cleanup_thread144();pe8_thread_detach();sys8(W8_SYS_THREAD_EXIT,code,0,0,0,0);pe8_exit(code);}
static void thread_entry142(uint64_t entry,void*arg){
 unsigned row=tid142()&255;lock_enter142(&tls_lock142);memset(tls_values8[row],0,sizeof(tls_values8[row]));lock_leave142(&tls_lock142);
 pe8_thread_attach();
 unsigned code=((unsigned(MS*)(void*))(uintptr_t)entry)(arg);f_ExitThread(code);
}
static HANDLE MS f_CreateThread(void*security,size_t stack,uint64_t entry,void*arg,unsigned flags,unsigned*id){
 if(security||stack>0x100000||!entry||(flags&~4u)){last8(50);return 0;}
 int64_t token=(int64_t)sys8(W8_SYS_THREAD_CREATE,(uint64_t)(uintptr_t)thread_entry142,entry,(uint64_t)(uintptr_t)arg,(flags&4)!=0,0);
 if(token<0){last8(8);return 0;}if(id)*id=(unsigned)token;return (HANDLE)token;
}
static NORETURN void MS f__endthreadex(unsigned code){f_ExitThread(code);}
static unsigned MS f_GetThreadId(HANDLE h){int64_t id=(int64_t)sys8(W8_SYS_THREAD_ID,h,0,0,0,0);if(id<0){last8(6);return 0;}return (unsigned)id;}
static uint64_t MS f__beginthreadex(void*security,unsigned stack,uint64_t entry,void*arg,unsigned flags,unsigned*id){return f_CreateThread(security,stack,entry,arg,flags,id);}
static int MS f_GetExitCodeThread(HANDLE h,unsigned*code){if(!code){last8(87);return 0;}int64_t state=(int64_t)sys8(W8_SYS_THREAD_STATUS,h,(uint64_t)(uintptr_t)code,0,0,0);if(state<0){last8(6);return 0;}if(state==259)*code=259;return 1;}
static void MS f_Sleep(unsigned timeout){sys8(W8_SYS_SLEEP,timeout,0,0,0,0);}
static int MS f_GetProcessTimes(HANDLE h,FILETIME*a,FILETIME*b,FILETIME*c,FILETIME*d){(void)h;(void)a;(void)b;(void)c;(void)d;last8(50);return 0;}
static int MS f_GetConsoleMode(HANDLE h,unsigned*mode){if(h<1||h>3||!mode){last8(6);return 0;}*mode=console_mode8[h-1];return 1;}
static int MS f_SetConsoleMode(HANDLE h,unsigned mode){if(h<1||h>3){last8(6);return 0;}console_mode8[h-1]=mode;return 1;}
static int MS f_GetConsoleScreenBufferInfo(HANDLE h,void*out){if((h!=2&&h!=3)||!out){last8(6);return 0;}int16_t*data=out;memset(data,0,22);data[0]=120;data[1]=50;data[4]=7;data[7]=119;data[8]=49;data[9]=120;data[10]=50;return 1;}
static uint64_t console_handlers8[16];static unsigned ignore_console8,file_oem8;
static int MS f_SetConsoleCtrlHandler(uint64_t callback,int add){if(!callback){ignore_console8=add!=0;return 1;}if(add){for(unsigned i=0;i<16;++i)if(!console_handlers8[i]){console_handlers8[i]=callback;return 1;}last8(8);return 0;}for(unsigned i=0;i<16;++i)if(console_handlers8[i]==callback){console_handlers8[i]=0;return 1;}last8(87);return 0;}
static void MS f_SetFileApisToOEM(void){file_oem8=1;}
static unsigned MS f_GetOEMCP(void){return 65001;}
static unsigned MS f_GetACP(void){return 65001;}
static int MS f_MultiByteToWideChar(unsigned cp,unsigned flags,const char*src,int count,WCHAR*out,int capacity){
 if(!src||count==0||count< -1||capacity<0||(flags&~8u)||(cp!=0&&cp!=1&&cp!=65001&&cp!=1252)){last8(87);return 0;}unsigned n=count<0?len8(src)+1:(unsigned)count,used=0;
 static const uint16_t high[]={0x20ac,0x81,0x201a,0x192,0x201e,0x2026,0x2020,0x2021,0x2c6,0x2030,0x160,0x2039,0x152,0x8d,0x17d,0x8f,0x90,0x2018,0x2019,0x201c,0x201d,0x2022,0x2013,0x2014,0x2dc,0x2122,0x161,0x203a,0x153,0x9d,0x17e,0x178};
 for(unsigned i=0;i<n;){unsigned v=(uint8_t)src[i++],extra=0,min=0;if(cp==1252){if(v>=128&&v<160)v=high[v-128];}else{if(v>=0xf0){v&=7;extra=3;min=65536;}else if(v>=0xe0){v&=15;extra=2;min=2048;}else if(v>=0xc2){v&=31;extra=1;min=128;}else if(v>=128){last8(1113);return 0;}if(extra>n-i){last8(1113);return 0;}for(unsigned j=0;j<extra;++j){unsigned b=(uint8_t)src[i++];if((b&0xc0)!=0x80){last8(1113);return 0;}v=(v<<6)|(b&63);}if(v<min||v>0x10ffff||(v>=0xd800&&v<=0xdfff)){last8(1113);return 0;}}
  unsigned units=v>65535?2:1;if(capacity&&used+units>(unsigned)capacity){last8(122);return 0;}if(out&&capacity){if(units==1)out[used]=(WCHAR)v;else{v-=0x10000;out[used]=(WCHAR)(0xd800+(v>>10));out[used+1]=(WCHAR)(0xdc00+(v&1023));}}used+=units;
 }return (int)used;
}
static int MS f_WideCharToMultiByte(unsigned cp,unsigned flags,const WCHAR*src,int count,char*out,int capacity,const char*default_char,int*used_default){
 if(!src||count==0||count< -1||capacity<0||(flags&~0x400u)||(cp!=0&&cp!=1&&cp!=65001&&cp!=1252)){last8(87);return 0;}unsigned n=count<0?wlen8(src)+1:(unsigned)count,used=0;if(used_default)*used_default=0;
 for(unsigned i=0;i<n;++i){unsigned v=src[i];if(v>=0xd800&&v<=0xdbff){if(i+1>=n||src[i+1]<0xdc00||src[i+1]>0xdfff){last8(1113);return 0;}v=0x10000+((v-0xd800)<<10)+(src[++i]-0xdc00);}else if(v>=0xdc00&&v<=0xdfff){last8(1113);return 0;}
  unsigned bytes=cp==1252?1:v<128?1:v<2048?2:v<65536?3:4;if(capacity&&used+bytes>(unsigned)capacity){last8(122);return 0;}if(out&&capacity){if(cp==1252){if(v<=255)out[used]=(char)v;else{out[used]=default_char?*default_char:'?';if(used_default)*used_default=1;}}else if(bytes==1)out[used]=(char)v;else{out[used]=(char)((bytes==2?0xc0:bytes==3?0xe0:0xf0)|(v>>(6*(bytes-1))));for(unsigned j=1;j<bytes;++j)out[used+j]=(char)(0x80|((v>>(6*(bytes-j-1)))&63));}}used+=bytes;
 }return (int)used;
}
static WCHAR *MS f_CharUpperW(WCHAR*p){if((uintptr_t)p<=65535){unsigned v=(unsigned)(uintptr_t)p;if(v>='a'&&v<='z')v-=32;return (WCHAR*)(uintptr_t)v;}for(unsigned i=0;p&&p[i];++i)if(p[i]>='a'&&p[i]<='z')p[i]-=32;return p;}
static const char *MS f_CharPrevExA(unsigned cp,const char*start,const char*current,unsigned flags){(void)flags;if(current<=start)return start;const char*p=current-1;if(cp==65001||cp==0||cp==1)while(p>start&&((uint8_t)*p&0xc0)==0x80)--p;return p;}
static int MS f_FormatMessageW(unsigned flags,const void*source,unsigned code,unsigned language,void*out,unsigned capacity,void*args){(void)source;(void)language;(void)args;if(!(flags&0x1000u)){last8(50);return 0;}const char*message=code==2?"The file could not be found.":code==3?"The path could not be found.":code==5?"Access is denied.":code==50?"This operation is not supported by this runtime.":code==80||code==183?"The file already exists.":code==8?"Not enough memory.":"The requested operation failed.";WCHAR wide[128];int n=utf8_to16(message,wide,128);if(n<0)return 0;if(flags&0x100u){WCHAR*p=alloc8(((unsigned)n+1)*2);if(!p){last8(8);return 0;}memcpy(p,wide,((unsigned)n+1)*2);*(WCHAR**)out=p;}else{if(capacity<=(unsigned)n){last8(122);return 0;}memcpy(out,wide,((unsigned)n+1)*2);}return n;}
static void *MS f_LocalFree(void*p){free8(p);return 0;}
static int leap8(unsigned year){return !(year%4)&&(year%100||!(year%400));}
static int MS f_FileTimeToSystemTime(const uint64_t*time,uint16_t*out){if(!time||!out)return 0;uint64_t seconds=*time/10000000,days=seconds/86400;unsigned year=1601;uint64_t remaining=days;while(year<=9999&&remaining>=(uint64_t)(365+leap8(year))){remaining-=365+(unsigned)leap8(year);++year;}if(year>9999){last8(87);return 0;}static const unsigned months[]={31,28,31,30,31,30,31,31,30,31,30,31};unsigned month=0;while(month<11){unsigned n=months[month]+(month==1&&leap8(year));if(remaining<n)break;remaining-=n;++month;}out[0]=(uint16_t)year;out[1]=(uint16_t)(month+1);out[2]=(uint16_t)((days+1)%7);out[3]=(uint16_t)(remaining+1);out[4]=(uint16_t)((seconds/3600)%24);out[5]=(uint16_t)((seconds/60)%60);out[6]=(uint16_t)(seconds%60);out[7]=(uint16_t)((*time%10000000)/10000);return 1;}
static int MS f_FileTimeToDosDateTime(const uint64_t*time,uint16_t*date,uint16_t*clock){uint16_t s[8];if(!date||!clock||!f_FileTimeToSystemTime(time,s)||s[0]<1980||s[0]>2107)return 0;*date=(uint16_t)(((s[0]-1980)<<9)|(s[1]<<5)|s[3]);*clock=(uint16_t)((s[4]<<11)|(s[5]<<5)|(s[6]/2));return 1;}
static int MS f_DosDateTimeToFileTime(unsigned date,unsigned time,uint64_t*out){unsigned year=1980+(date>>9),month=(date>>5)&15,day=date&31,hour=time>>11,minute=(time>>5)&63,second=(time&31)*2;static const unsigned lengths[]={31,28,31,30,31,30,31,31,30,31,30,31};if(!out||month<1||month>12||!day||day>lengths[month-1]+(month==2&&leap8(year))||hour>23||minute>59||second>59){last8(87);return 0;}uint64_t days=0;for(unsigned y=1601;y<year;++y)days+=365+(unsigned)leap8(y);for(unsigned m=1;m<month;++m)days+=lengths[m-1]+(m==2&&leap8(year));days+=day-1;*out=(days*86400+hour*3600+minute*60+second)*10000000;return 1;}
static int MS f_FileTimeToLocalFileTime(const uint64_t*in,uint64_t*out){if(!in||!out)return 0;*out=*in;return 1;}
static int MS f_LocalFileTimeToFileTime(const uint64_t*in,uint64_t*out){return f_FileTimeToLocalFileTime(in,out);}
static int MS f_CompareFileTime(const uint64_t*a,const uint64_t*b){return *a<*b?-1:*a>*b?1:0;}

static unsigned provider8(const char*name){if(!case8(name,"kernel32.dll")||!case8(name,"kernelbase.dll"))return 1;if(!case8(name,"msvcrt.dll"))return 2;if(!case8(name,"oleaut32.dll"))return 3;if(!case8(name,"user32.dll"))return 4;if(!case8(name,"advapi32.dll"))return 5;if(!case8(name,"comctl32.dll"))return 6;if(!case8(name,"comdlg32.dll"))return 7;if(!case8(name,"gdi32.dll"))return 8;if(!case8(name,"ole32.dll"))return 9;if(!case8(name,"shell32.dll"))return 10;if(!case8(name,"mpr.dll"))return 11;return 0;}
static HANDLE MS f_GetModuleHandleA(const char*name){if(!name)return pe8_main();uint64_t real=pe8_module(name);if(real)return real;unsigned id=provider8(name);if(id)return 0x70000000+id*0x10000;last8(126);return 0;}
static HANDLE MS f_GetModuleHandleW(const WCHAR*name){if(!name)return pe8_main();char text[256];if(utf16_to8(name,text,256)<0){last8(206);return 0;}return f_GetModuleHandleA(text);}
static void *MS f_GetProcAddress(HANDLE module,const char*name){
 if(module>=0x70010000&&module<=0x700b0000&&!(module&65535)){static const char*names[]={"","kernel32.dll","msvcrt.dll","oleaut32.dll","user32.dll","advapi32.dll","comctl32.dll","comdlg32.dll","gdi32.dll","ole32.dll","shell32.dll","mpr.dll"};void*p=resolve8(names[(module-0x70000000)/65536],(uintptr_t)name<65536?0:name,(uintptr_t)name<65536?(unsigned)(uintptr_t)name:0);if(guard_address144(p))p=0;if(!p)last8(127);return p;}
 void*p=pe8_symbol(module,(uintptr_t)name<65536?0:name,(uintptr_t)name<65536?(unsigned)(uintptr_t)name:0);if(guard_address144(p))p=0;if(!p)last8(127);return p;
}
static HANDLE MS f_LoadLibraryExW(const WCHAR*name,HANDLE file,unsigned flags){if(file||(flags&~8u)){last8(50);return 0;}char text[256];if(utf16_to8(name,text,256)<0){last8(206);return 0;}unsigned id=provider8(text);if(id)return 0x70000000+id*0x10000;char path[256];unsigned separator=0;for(unsigned i=0;text[i];++i)if(text[i]=='/'||text[i]=='\\')separator=1;
 if(!separator){HANDLE found=pe8_named(text);if(!found)last8(126);return found;}else if(!nativepath8(name,path)){last8(126);return 0;}w8_file_info info;if(stat8(path,&info)){last8(126);return 0;}return pe8_load(path);}
static HANDLE MS f_LoadLibraryW(const WCHAR*name){return f_LoadLibraryExW(name,0,0);}
static HANDLE MS f_LoadLibraryA(const char*name){WCHAR wide[256];if(utf8_to16(name,wide,256)<0)return 0;return f_LoadLibraryW(wide);}
static int MS f_FreeLibrary(HANDLE module){for(unsigned id=1;id<=11;++id)if(module==0x70000000+id*0x10000)return 1;if(pe8_release(module))return 1;last8(6);return 0;}
static unsigned MS f_GetModuleFileNameW(HANDLE module,WCHAR*out,unsigned cap){if(!cap||!out){last8(87);return 0;}const char*path=pe8_path(module?module:pe8_main());if(!path){last8(126);return 0;}char win[512];winpath8(path,win,512);WCHAR wide[512];int n=utf8_to16(win,wide,512);if(n<0){last8(206);return 0;}if((unsigned)n>=cap){widecopy8(out,wide,cap);last8(122);return cap;}widecopy8(out,wide,cap);return (unsigned)n;}
static unsigned MS f_GetModuleFileNameA(HANDLE module,char*out,unsigned cap){WCHAR wide[512];unsigned n=f_GetModuleFileNameW(module,wide,512);if(!n)return 0;char value[1024];if(utf16_to8(wide,value,1024)<0)return 0;unsigned bytes=len8(value);if(cap<=bytes){copy8(out,value,cap);last8(122);return cap;}copy8(out,value,cap);return bytes;}
static int MS f_IsDebuggerPresent(void){return 0;}
static int MS f_LookupPrivilegeValueW(const WCHAR*system,const WCHAR*name,void*luid){(void)system;(void)name;(void)luid;last8(1313);return 0;}
static int MS f_OpenProcessToken(HANDLE process,unsigned access,HANDLE*out){(void)process;(void)access;if(out)*out=0;last8(50);return 0;}
static int MS f_AdjustTokenPrivileges(HANDLE token,int disable,void*new_state,unsigned size,void*previous,unsigned*needed){(void)token;(void)disable;(void)new_state;(void)size;(void)previous;if(needed)*needed=0;last8(50);return 0;}
static int MS f_GetFileSecurityW(const WCHAR*file,unsigned info,void*out,unsigned length,unsigned*needed){(void)file;(void)info;(void)out;(void)length;if(needed)*needed=0;last8(50);return 0;}
static int MS f_SetFileSecurityW(const WCHAR*file,unsigned info,const void*data){(void)file;(void)info;(void)data;last8(50);return 0;}
typedef struct {unsigned live;char key[256];} reg_handle8;
static reg_handle8 registry_handles8[16];
static int MS legacy_RegOpenKeyExW(HANDLE root,const WCHAR*key,unsigned options,unsigned access,HANDLE*out){
 (void)options;(void)access;if(!out)return 87;*out=0;char text[256];if(utf16_to8(key,text,256)<0)return 87;
 if((root&UINT64_C(0xffffffff))!=0x80000001u&&(root&UINT64_C(0xffffffff))!=0x80000002u)return 2;
 char file[256];copy8(file,job8->product_root,256);append8(file,"/registry.txt",256);void*data=0;unsigned bytes=load8(file,&data,65536);if(!bytes)return 2;
 unsigned match=0;char wanted[280];wanted[0]=(root&0xffffffffu)==0x80000001u?'1':'2';wanted[1]='|';copy8(wanted+2,text,sizeof(wanted)-2);append8(wanted,"|",sizeof(wanted));unsigned n=len8(wanted);
 for(unsigned at=0;at<bytes;){unsigned end=at;while(end<bytes&&((char*)data)[end]!='\n')++end;if(end-at>=n&&!memcmp((char*)data+at,wanted,n))match=1;at=end+1;}free8(data);if(!match)return 2;
 unsigned id=0;while(id<16&&registry_handles8[id].live)++id;if(id==16)return 8;registry_handles8[id].live=1;copy8(registry_handles8[id].key,wanted,256);*out=0x4000+id;return 0;
}
static int MS legacy_RegQueryValueExW(HANDLE h,const WCHAR*name,unsigned*reserved,unsigned*type,void*out,unsigned*bytes){
 if(reserved||!bytes||h<0x4000||h>=0x4010||!registry_handles8[h-0x4000].live)return 87;char key[512],value[128];copy8(key,registry_handles8[h-0x4000].key,512);if(utf16_to8(name,value,128)<0)return 87;append8(key,value,512);append8(key,"|",512);
 char file[256];copy8(file,job8->product_root,256);append8(file,"/registry.txt",256);void*data=0;unsigned size=load8(file,&data,65536);if(!size)return 2;unsigned n=len8(key),status=2;
 for(unsigned at=0;at<size;){unsigned end=at;while(end<size&&((char*)data)[end]!='\n')++end;if(end-at>=n&&!memcmp((char*)data+at,key,n)){char temp[512];unsigned len=end-at-n;if(len>=sizeof(temp)){status=87;break;}memcpy(temp,(char*)data+at+n,len);temp[len]=0;WCHAR wide[512];int count=utf8_to16(temp,wide,512);if(count<0){status=87;break;}unsigned needed=((unsigned)count+1)*2;if(type)*type=1;unsigned capacity=*bytes;*bytes=needed;if(out&&capacity<needed){status=234;break;}if(out)memcpy(out,wide,needed);status=0;break;}at=end+1;}
 free8(data);return (int)status;
}
static int MS legacy_RegCloseKey(HANDLE h){if(h<0x4000||h>=0x4010||!registry_handles8[h-0x4000].live)return 6;memset(registry_handles8+(h-0x4000),0,sizeof(reg_handle8));return 0;}

#include "registry143.inc"

#define GUARD8(symbol,label) static NORETURN void MS symbol(void){fail8(label " is not implemented in this Windows profile.");}
GUARD8(guard_cxx8,"C++ exception unwinding")
GUARD8(guard_seh8,"Legacy Windows exception filtering")
static int MS f___C_specific_handler(w8_exception_record142*r,uint64_t frame,w8_context142*c,void*d){return seh_c_specific142(r,frame,c,d);}
GUARD8(guard_pure8,"A pure virtual C++ call")
static void MS f_type_info_destructor(void*p){(void)p; /* type_info carries no cached name in this CRT profile. */}
static HANDLE MS f_OpenFileMappingW(unsigned access,int inherit,const WCHAR*name){(void)access;(void)inherit;(void)name;last8(2);return 0;}
static void *MS f_MapViewOfFile(HANDLE mapping,unsigned access,unsigned high,unsigned low,size_t bytes){(void)mapping;(void)access;(void)high;(void)low;(void)bytes;last8(6);return 0;}
static int MS f_UnmapViewOfFile(void*base){(void)base;last8(487);return 0;}

#include "process142.inc"
#include "exception142.inc"
#include "heap-api144.inc"
#include "resource-api144.inc"
#include "images144.inc"
#include "ui144.inc"
#include "window-api144.inc"
#include "painting144.inc"
#include "image-draw145.inc"
#include "menus144.inc"
#include "accelerators144.inc"
#include "controls144.inc"
#include "com144.inc"
#include "security-api144.inc"
#include "shell-icons144.inc"
typedef struct {const char*name;void*address;unsigned provider;} api8;
#define API8(name,provider) {#name,(void*)(uintptr_t)&f_##name,provider}
static const api8 api8_table[]={
 API8(ImageList_Draw,6),API8(DrawIconEx,4),API8(DrawIcon,4),
 API8(RegisterClipboardFormatW,4),API8(GetClipboardFormatNameW,4),
 API8(LsaOpenPolicy,5),API8(LsaClose,5),API8(LsaAddAccountRights,5),API8(LookupAccountNameW,5),API8(GetUserNameW,5),
 API8(CoInitializeEx,9),API8(CoInitialize,9),API8(CoUninitialize,9),API8(OleInitialize,9),API8(OleUninitialize,9),API8(RegisterDragDrop,9),API8(RevokeDragDrop,9),
 API8(GetClientRect,4),API8(GetWindowRect,4),API8(ClientToScreen,4),API8(ScreenToClient,4),API8(MoveWindow,4),API8(GetDlgItem,4),API8(SendDlgItemMessageW,4),API8(SetDlgItemTextW,4),API8(IsWindowEnabled,4),API8(EnableWindow,4),API8(IsZoomed,4),API8(GetDialogBaseUnits,4),API8(MapDialogRect,4),API8(SystemParametersInfoW,4),API8(MonitorFromWindow,4),API8(GetMonitorInfoA,4),API8(GetCursorPos,4),API8(LoadCursorW,4),API8(SetCursor,4),
 API8(InitCommonControls,6),API8(InitCommonControlsEx,6),
 API8(GetProcessHeap,1),API8(HeapAlloc,1),API8(HeapFree,1),API8(HeapSize,1),API8(LocalAlloc,1),API8(lstrlenW,1),API8(GetUserDefaultLangID,1),API8(GetSystemDefaultLangID,1),API8(wcslen,2),API8(srand,2),API8(rand,2),API8(CoTaskMemAlloc,9),API8(CoTaskMemFree,9),API8(CoTaskMemRealloc,9),
 API8(LoadIconW,4),API8(LoadBitmapW,4),API8(LoadImageW,4),API8(DestroyIcon,4),API8(DeleteObject,8),API8(ImageList_Create,6),API8(ImageList_Destroy,6),API8(ImageList_GetImageCount,6),API8(ImageList_ReplaceIcon,6),API8(ImageList_AddMasked,6),
 API8(FindResourceW,1),API8(FindResourceExW,1),API8(LoadResource,1),API8(LockResource,1),API8(SizeofResource,1),API8(FreeResource,1),API8(LoadStringW,4),
 API8(RegisterClassW,4),API8(GetClassInfoW,4),API8(CallWindowProcW,4),API8(SendMessageW,4),API8(CreateWindowExW,4),API8(DestroyWindow,4),API8(PostMessageW,4),API8(PostQuitMessage,4),API8(PeekMessageW,4),API8(GetMessageW,4),API8(DispatchMessageW,4),API8(TranslateMessage,4),API8(DefWindowProcW,4),API8(SetWindowTextW,4),API8(GetWindowTextW,4),API8(GetWindowTextLengthW,4),API8(GetWindowLongPtrW,4),API8(SetWindowLongPtrW,4),API8(ShowWindow,4),API8(GetParent,4),API8(IsWindow,4),
 API8(AddVectoredExceptionHandler,1),API8(AddVectoredContinueHandler,1),API8(RemoveVectoredExceptionHandler,1),API8(RemoveVectoredContinueHandler,1),API8(SetUnhandledExceptionFilter,1),
 API8(exit,2),API8(_exit,2),API8(_cexit,2),API8(_c_exit,2),API8(_onexit,2),API8(__dllonexit,2),API8(_initterm,2),API8(__set_app_type,2),API8(__setusermatherr,2),API8(__getmainargs,2),API8(__p___initenv,2),
 API8(malloc,2),API8(free,2),API8(realloc,2),API8(memcpy,2),API8(memmove,2),API8(memset,2),API8(memcmp,2),API8(strlen,2),API8(strcmp,2),API8(wcscmp,2),API8(strchr,2),API8(strstr,2),API8(wcsstr,2),API8(fputc,2),API8(fputs,2),API8(fflush,2),API8(fgetc,2),API8(_isatty,2),API8(_get_osfhandle,2),API8(_beginthreadex,2),API8(_endthreadex,2),
 {"_acmdln",&command_pointer144,2},{"_iob",iob8,2},{"__initenv",&initenv8,2},{"_fmode",&fmode8,2},{"_commode",&commode8,2},
 {"__CxxFrameHandler",guard_cxx8,2},{"_CxxThrowException",guard_cxx8,2},{"?terminate@@YAXXZ",guard_cxx8,2},{"__C_specific_handler",f___C_specific_handler,2},{"_XcptFilter",guard_seh8,2},{"_purecall",guard_pure8,2},{"??1type_info@@UEAA@XZ",f_type_info_destructor,2},
 API8(GetEnvironmentVariableW,1),API8(GetEnvironmentVariableA,1),API8(SetEnvironmentVariableW,1),API8(SetEnvironmentVariableA,1),API8(GetEnvironmentStringsW,1),API8(GetEnvironmentStringsA,1),API8(FreeEnvironmentStringsW,1),API8(FreeEnvironmentStringsA,1),API8(ExpandEnvironmentStringsW,1),API8(ExpandEnvironmentStringsA,1),API8(CreateProcessW,1),API8(CreateProcessA,1),API8(GetExitCodeProcess,1),API8(GetProcessId,1),API8(TerminateProcess,1),API8(GetStartupInfoW,1),API8(GetStartupInfoA,1),API8(ExitProcess,1),API8(GetCommandLineW,1),API8(GetCommandLineA,1),API8(GetLastError,1),API8(SetLastError,1),API8(GetCurrentProcessId,1),API8(GetCurrentThreadId,1),API8(GetCurrentProcess,1),API8(GetCurrentThread,1),API8(GetStdHandle,1),API8(GetTickCount,1),API8(QueryPerformanceCounter,1),API8(QueryPerformanceFrequency,1),API8(GetSystemTimeAsFileTime,1),API8(GetVersion,1),API8(GetVersionExW,1),API8(GetSystemInfo,1),API8(GetProcessAffinityMask,1),API8(SetProcessAffinityMask,1),API8(SetThreadAffinityMask,1),API8(GlobalMemoryStatusEx,1),API8(GetLargePageMinimum,1),API8(VirtualAlloc,1),API8(VirtualFree,1),API8(TlsAlloc,1),API8(TlsFree,1),API8(TlsGetValue,1),API8(TlsSetValue,1),API8(IsProcessorFeaturePresent,1),
 API8(CreateFileW,1),API8(ReadFile,1),API8(WriteFile,1),API8(SetFilePointer,1),API8(SetFilePointerEx,1),API8(GetFileSize,1),API8(GetFileSizeEx,1),API8(SetEndOfFile,1),API8(FlushFileBuffers,1),API8(LockFileEx,1),API8(UnlockFileEx,1),API8(LockFile,1),API8(UnlockFile,1),API8(GetFileInformationByHandle,1),API8(SetFileTime,1),API8(GetFileAttributesW,1),API8(SetFileAttributesW,1),API8(CreateDirectoryW,1),API8(DeleteFileW,1),API8(RemoveDirectoryW,1),API8(MoveFileW,1),API8(MoveFileExW,1),API8(MoveFileWithProgressW,1),API8(CreateHardLinkW,1),API8(GetFullPathNameW,1),API8(GetFullPathNameA,1),API8(GetCurrentDirectoryW,1),API8(SetCurrentDirectoryW,1),API8(GetTempPathW,1),API8(GetTempPathA,1),API8(GetTempFileNameW,1),API8(GetTempFileNameA,1),API8(GetDiskFreeSpaceExW,1),API8(GetDiskFreeSpaceW,1),API8(GetLogicalDriveStringsW,1),API8(FindFirstFileW,1),API8(FindNextFileW,1),API8(FindClose,1),API8(FindFirstStreamW,1),API8(FindNextStreamW,1),API8(DeviceIoControl,1),
 API8(InitializeCriticalSection,1),API8(InitializeCriticalSectionAndSpinCount,1),API8(InitializeCriticalSectionEx,1),API8(EnterCriticalSection,1),API8(TryEnterCriticalSection,1),API8(LeaveCriticalSection,1),API8(DeleteCriticalSection,1),API8(CreateWaitableTimerW,1),API8(SetWaitableTimer,1),API8(CancelWaitableTimer,1),API8(CreateEventW,1),API8(CreateSemaphoreW,1),API8(SetEvent,1),API8(ResetEvent,1),API8(ReleaseSemaphore,1),API8(OpenEventW,1),API8(OpenSemaphoreW,1),API8(OpenWaitableTimerW,1),API8(WaitForSingleObject,1),API8(WaitForMultipleObjects,1),API8(CloseHandle,1),API8(CreateThread,1),API8(ExitThread,1),API8(GetExitCodeThread,1),API8(GetThreadId,1),API8(ResumeThread,1),API8(Sleep,1),API8(GetProcessTimes,1),API8(GetConsoleMode,1),API8(SetConsoleMode,1),API8(GetConsoleScreenBufferInfo,1),API8(SetConsoleCtrlHandler,1),API8(SetFileApisToOEM,1),API8(GetOEMCP,1),API8(GetACP,1),API8(MultiByteToWideChar,1),API8(WideCharToMultiByte,1),API8(FormatMessageW,1),API8(LocalFree,1),API8(FileTimeToSystemTime,1),API8(FileTimeToDosDateTime,1),API8(DosDateTimeToFileTime,1),API8(FileTimeToLocalFileTime,1),API8(LocalFileTimeToFileTime,1),API8(CompareFileTime,1),API8(GetModuleHandleA,1),API8(GetModuleHandleW,1),API8(GetProcAddress,1),API8(LoadLibraryExW,1),API8(LoadLibraryW,1),API8(LoadLibraryA,1),API8(FreeLibrary,1),API8(GetModuleFileNameW,1),API8(GetModuleFileNameA,1),API8(IsDebuggerPresent,1),
 API8(OpenFileMappingW,1),API8(MapViewOfFile,1),API8(UnmapViewOfFile,1),
 API8(CreateMenu,4),API8(CreatePopupMenu,4),API8(IsMenu,4),API8(InsertMenuItemW,4),API8(SetMenuItemInfoW,4),API8(GetMenuItemInfoW,4),API8(GetMenuItemCount,4),API8(GetSubMenu,4),API8(GetMenuItemID,4),API8(DestroyMenu,4),API8(RemoveMenu,4),API8(AppendMenuW,4),API8(EnableMenuItem,4),API8(CheckMenuItem,4),API8(GetMenu,4),API8(SetMenu,4),API8(DrawMenuBar,4),API8(LoadMenuW,4),
 API8(LoadAcceleratorsW,4),API8(CreateAcceleratorTableW,4),API8(CopyAcceleratorTableW,4),API8(DestroyAcceleratorTable,4),API8(TranslateAcceleratorW,4),API8(GetWindowPlacement,4),API8(SetWindowPlacement,4),API8(GetFocus,4),API8(SetFocus,4),API8(GetCapture,4),API8(SetCapture,4),API8(ReleaseCapture,4),API8(SetTimer,4),API8(KillTimer,4),API8(CreateStatusWindowW,6),API8(SetParent,4),API8(CreateToolbarEx,6),API8(SHGetSpecialFolderLocation,10),API8(SHGetFileInfoW,10),
 API8(GetDC,4),API8(ReleaseDC,4),API8(InvalidateRect,4),API8(ValidateRect,4),API8(GetUpdateRect,4),API8(UpdateWindow,4),API8(BeginPaint,4),API8(EndPaint,4),API8(GetSysColor,4),API8(GetSysColorBrush,4),API8(FillRect,4),API8(SetTextColor,8),API8(SetBkColor,8),API8(SetBkMode,8),API8(GetTextExtentPoint32W,8),API8(TextOutW,8),
 API8(CharUpperW,4),API8(CharPrevExA,4),API8(LookupPrivilegeValueW,5),API8(OpenProcessToken,5),API8(AdjustTokenPrivileges,5),API8(GetFileSecurityW,5),API8(SetFileSecurityW,5),API8(SystemFunction036,5),API8(RegOpenKeyExW,5),API8(RegQueryValueExW,5),API8(RegCloseKey,5),API8(RegCreateKeyExW,5),API8(RegSetValueExW,5),API8(RegDeleteValueW,5),API8(RegDeleteKeyW,5),API8(RegEnumValueW,5),API8(RegEnumKeyExW,5),API8(RegFlushKey,5)
};
#undef API8
#include "guarded-ui144.inc"
void *resolve8(const char*dll,const char*name,unsigned ordinal){unsigned provider=provider8(dll);if(provider==2&&name&&equal8(name,"__initenv")&&!initenv8){initenv8=environment_crt143();if(!initenv8)return 0;}if(provider==3){switch(ordinal){case 2:return f_SysAllocString;case 4:return f_SysAllocStringLen;case 6:return f_SysFreeString;case 7:return f_SysStringLen;case 9:return f_VariantClear;case 10:return f_VariantCopy;case 149:return f_SysStringByteLen;case 150:return f_SysAllocStringByteLen;}if(name){if(equal8(name,"SysAllocString"))return f_SysAllocString;if(equal8(name,"SysAllocStringLen"))return f_SysAllocStringLen;if(equal8(name,"SysFreeString"))return f_SysFreeString;if(equal8(name,"SysStringLen"))return f_SysStringLen;if(equal8(name,"SysStringByteLen"))return f_SysStringByteLen;if(equal8(name,"SysAllocStringByteLen"))return f_SysAllocStringByteLen;if(equal8(name,"VariantClear"))return f_VariantClear;if(equal8(name,"VariantCopy"))return f_VariantCopy;}return 0;}
 if(provider==6&&!name&&ordinal==17)return f_InitCommonControls;
 if(provider){if(name)for(unsigned i=0;i<sizeof(api8_table)/sizeof(api8_table[0]);++i)if(api8_table[i].provider==provider&&equal8(api8_table[i].name,name))return api8_table[i].address;return guard_lookup144(provider,name,ordinal);}return pe8_import(dll,name,ordinal);
}
void init_win8(void){
 if(sys8(W8_SYS_EXCEPTION_REGISTER,(uint64_t)(uintptr_t)exception_entry142,0,0,0,0))fail8("Native exception dispatcher registration failed.");
 char win[512];if(job8->startup_command[0])copy8(command_utf8,job8->startup_command,sizeof(command_utf8));else{winpath8(job8->source,win,sizeof(win));copy8(command_utf8,"\"",sizeof(command_utf8));append8(command_utf8,win,sizeof(command_utf8));append8(command_utf8,"\" ",sizeof(command_utf8));append8(command_utf8,job8->arguments,sizeof(command_utf8));}if(utf8_to16(command_utf8,command8,1200)<0)fail8("Windows command line exceeds its bound.");
 char cwd[256];if(job8->startup_directory[0])copy8(cwd,job8->startup_directory,256);else{copy8(cwd,job8->user_root,256);append8(cwd,"/Documents",256);}winpath8(cwd,win,sizeof(win));if(utf8_to16(win,cwd8,512)<0)fail8("Windows working directory is too long.");
 unsigned at=0,out=0;while(command_utf8[at]&&argc8<63){while(command_utf8[at]==' '||command_utf8[at]=='\t')++at;if(!command_utf8[at])break;argv8[argc8++]=argv_text8+out;unsigned quoted=0;while(command_utf8[at]){char c=command_utf8[at++];if(c=='\"'){quoted^=1;continue;}if(!quoted&&(c==' '||c=='\t'))break;if(out+1>=sizeof(argv_text8))fail8("Windows arguments exceed their bound.");argv_text8[out++]=c;}argv_text8[out++]=0;}argv8[argc8]=0;
 for(unsigned i=0;i<3;++i){iob8[i].file=i;iob8[i].flags=i?2:1;}process_started8=sys8(W8_SYS_TIME,0,0,0,0,0);(void)process_started8;(void)app_type8;(void)error8;(void)file_oem8;(void)ignore_console8;
}
