/* File metadata must outlive processes, rename and application removal. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned size,pad;U reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;W show,reserved_bytes;unsigned pad2;U reserved_data,input,output,error;} SI;
typedef struct {U process,thread;unsigned pid,tid;} PI;
__declspec(dllimport) U CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,U);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) int SetFileTime(U,const U*,const U*,const U*);
__declspec(dllimport) int GetFileInformationByHandle(U,void*);
__declspec(dllimport) int SetFileAttributesW(const W*,unsigned);
__declspec(dllimport) unsigned GetFileAttributesW(const W*);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) int MoveFileExW(const W*,const W*,unsigned);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,SI*,PI*);
__declspec(dllimport) int GetExitCodeProcess(U,unsigned*);
__declspec(dllimport) unsigned WaitForSingleObject(U,unsigned);
__declspec(dllimport) W* GetCommandLineW(void);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
static const U creation=132537600000000000ULL,access=132537700000000000ULL,modified=132537800000000000ULL;
static const W original[]=L"m143-metadata.bin",renamed[]=L"m143-metadata-renamed.bin";
static void require(int good,unsigned code){if(!good){char error[]="M143_METADATA_CHECK_000\n";error[20]=(char)('0'+code/100);error[21]=(char)('0'+code/10%10);error[22]=(char)('0'+code%10);unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),error,sizeof(error)-1,&wrote,0);ExitProcess(code);}}
static U inspect(U handle){unsigned info[13];require(GetFileInformationByHandle(handle,info),10);require(info[0]==34&&(((U)info[2]<<32)|info[1])==creation&&(((U)info[4]<<32)|info[3])==access&&(((U)info[6]<<32)|info[5])==modified,11);return ((U)info[11]<<32)|info[12];}
#ifndef READ143
static int same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static void child(const W*name){U handle=CreateFileW(name,0x80000000u,7,0,3,128,0);require(handle!=~(U)0&&inspect(handle)&&CloseHandle(handle),12);}
static void spawn(W*command){SI startup={0};PI process={0};startup.size=sizeof(startup);require(CreateProcessW(L"C:\\Users\\Owner\\Documents\\m143-metadata-child.exe",command,0,0,0,0,0,0,&startup,&process),13);unsigned code=259;require(!WaitForSingleObject(process.process,10000)&&GetExitCodeProcess(process.process,&code)&&!code&&CloseHandle(process.process)&&CloseHandle(process.thread),14);}
#endif
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){
#ifdef READ143
 (void)original;
 U handle=CreateFileW(renamed,0x80000000u,7,0,3,128,0);require(handle!=~(U)0&&inspect(handle)&&CloseHandle(handle),15);
 static const char pass[]="M143_METADATA_RESTART_AND_REMOVE_PASS\n";
#else
 W*command=GetCommandLineW();if(same(command,L"metadata143 original")){child(original);ExitProcess(0);}if(same(command,L"metadata143 renamed")){child(renamed);ExitProcess(0);}
 SetFileAttributesW(original,32);DeleteFileW(original);SetFileAttributesW(renamed,32);DeleteFileW(renamed);
 U handle=CreateFileW(original,0xc0000000u,7,0,1,128,0);require(handle!=~(U)0,16);unsigned wrote=0;require(WriteFile(handle,"metadata survives\n",18,&wrote,0)&&wrote==18,17);
 require(SetFileTime(handle,&creation,&access,&modified)&&SetFileAttributesW(original,34),18);U identity=inspect(handle);require(identity!=0,19);
 U query=CreateFileW(original,0x80u,0,0,3,128,0);require(query!=~(U)0&&inspect(query)==identity&&CloseHandle(query),20);
 W first[]=L"metadata143 original";spawn(first);require(inspect(handle)==identity&&MoveFileExW(original,renamed,0)&&inspect(handle)==identity,21);
 W second[]=L"metadata143 renamed";spawn(second);require(CloseHandle(handle)&&GetFileAttributesW(original)==~0u&&GetFileAttributesW(renamed)==34,22);
 require(SetFileAttributesW(renamed,35),23);handle=CreateFileW(renamed,0x40000000u,7,0,3,128,0);require(handle==~(U)0&&GetLastError()==5&&!DeleteFileW(renamed)&&GetLastError()==5,24);
 handle=CreateFileW(renamed,0x100u,0,0,3,128,0);require(handle!=~(U)0&&SetFileTime(handle,&creation,&access,&modified)&&CloseHandle(handle)&&SetFileAttributesW(renamed,34),25);
 static const char pass[]="M143_NATIVE_FILE_METADATA_PASS\n";
#endif
 unsigned wrote_final=0;WriteFile(GetStdHandle((unsigned)-11),pass,sizeof(pass)-1,&wrote_final,0);ExitProcess(0);
}
