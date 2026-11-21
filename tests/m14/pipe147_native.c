/* Own caller of actual native anonymous pipes and inherited process handles. */
#define W8_USER
#include <engine/windows8.h>
#include <engine/sha256.h>
typedef uint64_t H;typedef uint16_t W;
typedef struct {unsigned size,pad;uint64_t reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;uint16_t show,reserved_bytes;unsigned pad2;uint64_t reserved_data,input,output,error;} START147;
typedef struct {unsigned size,pad;uint64_t descriptor;unsigned inherit,pad2;} SA147;
__declspec(dllimport) int CreatePipe(H*,H*,SA147*,unsigned);
__declspec(dllimport) int DuplicateHandle(H,H,H,H*,unsigned,int,unsigned);
__declspec(dllimport) int GetHandleInformation(H,unsigned*);
__declspec(dllimport) int SetHandleInformation(H,unsigned,unsigned);
__declspec(dllimport) unsigned GetFileType(H);
__declspec(dllimport) H GetStdHandle(int);
__declspec(dllimport) H GetCurrentProcess(void);
__declspec(dllimport) unsigned GetPriorityClass(H);
__declspec(dllimport) int ReadFile(H,void*,unsigned,unsigned*,void*);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int CloseHandle(H);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,START147*,w8_process_result*);
__declspec(dllimport) unsigned WaitForSingleObject(H,unsigned);
__declspec(dllimport) int GetExitCodeProcess(H,unsigned*);
__declspec(dllimport) void GetStartupInfoW(START147*);
__declspec(dllimport) W*GetCommandLineW(void);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) H CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,H);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) int RegCreateKeyExW(H,const W*,unsigned,W*,unsigned,unsigned,void*,H*,unsigned*);
__declspec(dllimport) int RegDeleteKeyW(H,const W*);
__declspec(dllimport) int RegCloseKey(H);
void*memcpy(void*d,const void*s,size_t n){uint8_t*a=d;const uint8_t*b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void*memset(void*d,int c,size_t n){uint8_t*a=d;for(size_t i=0;i<n;++i)a[i]=(uint8_t)c;return d;}
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
static int child147(void){const W*s=GetCommandLineW();for(unsigned i=0;s[i];++i)if(s[i]==' '&&s[i+1]=='c'&&s[i+2]=='h'&&s[i+3]=='i'&&s[i+4]=='l'&&s[i+5]=='d'&&!s[i+6])return 1;return 0;}
static void message147(const char*s){unsigned n=0,wrote=0;while(s[n])++n;check147(WriteFile(GetStdHandle(-11),s,n,&wrote,0)&&wrote==n,90);}
static const uint8_t expected147[32]={0xe8,0xf9,0x7c,0x62,0xd0,0xd5,0xe5,0x9b,0x14,0x3c,0x48,0x2b,0x16,0x6a,0xa5,0xad,0xe2,0x9d,0x87,0xd4,0xee,0x70,0x5b,0xc8,0xee,0x34,0x1f,0xbe,0x88,0xc1,0xb1,0x7d};
void entry(void);void*volatile anchor147=&entry;
void entry(void){
 if(child147()){
  /* Editing user startup data cannot manufacture kernel installation authority. */
  *(volatile uint32_t*)(uintptr_t)(W8_MAILBOX+4)=W8_INSTALL;
  H key=0,file=CreateFileW(L"C:\\Program Files\\7-Zip\\pipe-authority147.tmp",0x40000000u,0,0,1,0,0);
#ifdef PIPE_AUTH147
  check147(file!=UINT64_MAX&&CloseHandle(file)&&DeleteFileW(L"C:\\Program Files\\7-Zip\\pipe-authority147.tmp"),60);check147(!RegCreateKeyExW(UINT64_C(0xffffffff80000002),L"Software\\EngacerPipeGrant147",0,0,0,0x10003u,0,&key,0)&&key,61);check147(!RegCloseKey(key)&&!RegDeleteKeyW(UINT64_C(0xffffffff80000002),L"Software\\EngacerPipeGrant147"),62);
#else
  check147(file==UINT64_MAX&&GetLastError()==5,60);check147(RegCreateKeyExW(UINT64_C(0xffffffff80000002),L"Software\\EngacerPipeGrant147",0,0,0,3,0,&key,0)==5&&!key,61);
#endif
  START147 start;GetStartupInfoW(&start);check147(start.flags==0x100&&start.input==GetStdHandle(-10)&&start.output==GetStdHandle(-11)&&GetFileType(start.input)==3&&GetFileType(start.output)==3,10);Sleep(100);engine_sha256_context hash;engine_sha256_init(&hash);uint8_t data[4096],digest[32];unsigned total=0;
  for(;;){unsigned got=0;int ok=ReadFile(start.input,data,sizeof(data),&got,0);if(!ok){check147(GetLastError()==109&&!got,11);break;}check147(got&&engine_sha256_update(&hash,data,got),12);total+=got;}
  check147(total==1024*1024&&engine_sha256_final(&hash,digest),13);for(unsigned i=0;i<32;++i)check147(digest[i]==expected147[i],14);unsigned wrote=0;check147(WriteFile(start.output,digest,32,&wrote,0)&&wrote==32,15);check147(CloseHandle(start.input)&&CloseHandle(start.output),16);ExitProcess(0);
 }
#ifdef PIPE_BLOCK147
 H r=0,w=0;check147(CreatePipe(&r,&w,0,0),70);unsigned n=0;uint8_t data[4096]={0};message147("M147_PIPE_BLOCK_READY\n");
 #if PIPE_BLOCK147==1
 (void)ReadFile(r,data,1,&n,0);
 #else
 (void)WriteFile(w,data,sizeof(data),&n,0);
 #endif
 ExitProcess(71);
#else
 H r=0,w=0;check147(CreatePipe(&r,&w,0,0)&&GetFileType(r)==3&&GetFileType(w)==3,20);unsigned n=0,flags=9;check147(GetHandleInformation(r,&flags)&&flags==0,21);check147(!ReadFile(w,&flags,1,&n,0)&&GetLastError()==5&&!n,22);check147(!WriteFile(r,&flags,1,&n,0)&&GetLastError()==5&&!n,23);H duplicate=0;check147(DuplicateHandle(GetCurrentProcess(),r,GetCurrentProcess(),&duplicate,0,0,2)&&duplicate!=r,24);check147(CloseHandle(r)&&!CloseHandle(r)&&GetLastError()==6,25);check147(CloseHandle(w),26);check147(!ReadFile(duplicate,&flags,1,&n,0)&&GetLastError()==109&&!n,27);check147(CloseHandle(duplicate),28);
 check147(CreatePipe(&r,&w,0,0)&&CloseHandle(r),54);check147(!WriteFile(w,&flags,1,&n,0)&&GetLastError()==109&&!n&&CloseHandle(w),55);
 H handles[32];for(unsigned i=0;i<16;++i)check147(CreatePipe(handles+i*2,handles+i*2+1,0,0),30);check147(!CreatePipe(&r,&w,0,0)&&GetLastError()==8,31);for(unsigned i=0;i<32;++i)check147(CloseHandle(handles[i]),32);
 SA147 sa={.size=sizeof(sa),.inherit=1};H inread=0,inwrite=0,outread=0,outwrite=0,errwrite=0;check147(CreatePipe(&inread,&inwrite,&sa,0)&&CreatePipe(&outread,&outwrite,&sa,0),40);check147(SetHandleInformation(inwrite,1,0)&&SetHandleInformation(outread,1,0),41);flags=0;check147(GetHandleInformation(inread,&flags)&&flags==1&&GetHandleInformation(inwrite,&flags)&&flags==0,42);
 check147(DuplicateHandle(GetCurrentProcess(),outwrite,GetCurrentProcess(),&errwrite,0,1,2),53);
 START147 start={.size=sizeof(start),.flags=0x100,.input=inread,.output=outwrite,.error=errwrite};w8_process_result process={0};W command[]=L"\"C:\\Program Files\\7-Zip\\child147.exe\" child";check147(GetPriorityClass(GetCurrentProcess())==0x20,43);check147(CreateProcessW(0,command,0,0,1,GetPriorityClass(GetCurrentProcess())|0x08000000u,0,0,&start,&process),44);check147(CloseHandle(inread)&&CloseHandle(outwrite)&&CloseHandle(errwrite),45);
 uint8_t data[4096];for(unsigned at=0;at<1024*1024;at+=sizeof(data)){for(unsigned i=0;i<sizeof(data);++i)data[i]=(uint8_t)((at+i)*37+((at+i)>>8));unsigned wrote=0;check147(WriteFile(inwrite,data,sizeof(data),&wrote,0)&&wrote==sizeof(data),46);}check147(CloseHandle(inwrite),47);
 uint8_t digest[32];unsigned used=0;while(used<32){unsigned got=0;check147(ReadFile(outread,digest+used,32-used,&got,0)&&got,48);used+=got;}for(unsigned i=0;i<32;++i)check147(digest[i]==expected147[i],49);unsigned got=0;check147(!ReadFile(outread,data,1,&got,0)&&GetLastError()==109&&!got,50);check147(CloseHandle(outread)&&WaitForSingleObject(process.process,30000)==0,51);unsigned code=259;check147(GetExitCodeProcess(process.process,&code)&&code==0&&CloseHandle(process.thread)&&CloseHandle(process.process),52);message147("M147_NATIVE_PIPE_INHERITED_1M_SHA_EOF_QUOTA_PASS\n");ExitProcess(0);
#endif
}
