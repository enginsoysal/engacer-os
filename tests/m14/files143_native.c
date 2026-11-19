/* Own Windows PE probe for real shared file state; not an original app. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned size,pad;U reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;W show,reserved_bytes;unsigned pad2;U reserved_data,input,output,error;} SI;
typedef struct {U process,thread;unsigned pid,tid;} PI;
typedef struct {U internal,high;unsigned offset,offset_high;U event;} OV;
__declspec(dllimport) U CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,U);
__declspec(dllimport) int ReadFile(U,void*,unsigned,unsigned*,void*);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int SetFilePointerEx(U,long long,long long*,unsigned);
__declspec(dllimport) int SetEndOfFile(U);
__declspec(dllimport) int FlushFileBuffers(U);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) int MoveFileExW(const W*,const W*,unsigned);
__declspec(dllimport) unsigned GetFileAttributesW(const W*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,SI*,PI*);
__declspec(dllimport) unsigned WaitForSingleObject(U,unsigned);
__declspec(dllimport) int GetExitCodeProcess(U,unsigned*);
__declspec(dllimport) int LockFileEx(U,unsigned,unsigned,unsigned,unsigned,OV*);
__declspec(dllimport) int UnlockFileEx(U,unsigned,unsigned,unsigned,OV*);
__declspec(dllimport) U CreateThread(void*,U,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) U CreateEventW(void*,int,int,const W*);
__declspec(dllimport) int SetEvent(U);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) W* GetCommandLineW(void);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
static void require(int good,unsigned code){if(!good)ExitProcess(code);}
static int same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static U open(const W*path,unsigned access,unsigned share,unsigned create){return CreateFileW(path,access,share,0,create,128,0);}
static void seek(U handle,long long position){require(SetFilePointerEx(handle,position,0,0),30);}
static void write(U h,const char*text,unsigned size){unsigned wrote=0;require(WriteFile(h,text,size,&wrote,0)&&wrote==size,31);}
static void read(U h,char*text,unsigned size){unsigned got=0;require(ReadFile(h,text,size,&got,0)&&got==size,32);}
static U lock_ready;static volatile unsigned lock_finished;
static unsigned lock_worker(void*unused){
 (void)unused;U handle=open(L"m143-file.bin",0xc0000000u,7,3);require(handle!=~(U)0,50);OV range={0};require(SetEvent(lock_ready)&&LockFileEx(handle,2,0,1,0,&range),51);
 write(handle,"a",1);require(UnlockFileEx(handle,0,1,0,&range)&&CloseHandle(handle),52);lock_finished=1;return 0;
}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){
 unsigned got=0;char data[32]={0};
 if(same(GetCommandLineW(),L"files143 child")){
  U denied=open(L"m143-file.bin",0x80000000u,1,3);require(denied==~(U)0&&GetLastError()==32,10);
  U child=open(L"m143-file.bin",0xc0000000u,7,3);require(child!=~(U)0,11);
  read(child,data,3);require(data[0]=='a'&&data[1]=='b'&&data[2]=='c',12);
  seek(child,1);write(child,"x",1);require(FlushFileBuffers(child)&&CloseHandle(child),13);ExitProcess(0);
 }
 DeleteFileW(L"m143-file.bin");
 U h=open(L"m143-file.bin",0xc0000000u,7,1);require(h!=~(U)0,14);write(h,"abc",3);
 require(ReadFile(h,0,0,&got,0)&&!got&&WriteFile(h,0,0,&got,0)&&!got,53);
 U duplicate=open(L"m143-file.bin",0x80000000u,7,3);require(duplicate!=~(U)0,15);
 read(duplicate,data,3);require(data[0]=='a'&&data[1]=='b'&&data[2]=='c',16);require(CloseHandle(duplicate),17);
 U stale=duplicate;duplicate=open(L"m143-file.bin",0x80000000u,7,3);require(duplicate!=~(U)0&&duplicate!=stale,18);
 require(!ReadFile(stale,data,1,&got,0)&&GetLastError()==6&&CloseHandle(duplicate),19);
 OV range={0};require(LockFileEx(h,3,0,3,0,&range),54);duplicate=open(L"m143-file.bin",0xc0000000u,7,3);require(duplicate!=~(U)0,55);
 require(!ReadFile(duplicate,data,1,&got,0)&&GetLastError()==33,56);seek(h,0);read(h,data,3);
 require(!LockFileEx(duplicate,3,0,3,0,&range)&&GetLastError()==33,57);
 require(!UnlockFileEx(duplicate,0,3,0,&range)&&GetLastError()==158&&UnlockFileEx(h,0,3,0,&range),58);
 require(LockFileEx(h,3,0,3,0,&range)&&LockFileEx(h,1,0,3,0,&range),66);
 require(UnlockFileEx(h,0,3,0,&range),67);seek(duplicate,0);read(duplicate,data,3);seek(h,0);
 require(!WriteFile(h,"Q",1,&got,0)&&GetLastError()==33&&!got&&UnlockFileEx(h,0,3,0,&range),68);
 require(LockFileEx(h,1,0,3,0,&range),59);seek(duplicate,0);read(duplicate,data,3);seek(h,0);
 require(!WriteFile(h,"Q",1,&got,0)&&GetLastError()==33&&!got,60);require(UnlockFileEx(h,0,3,0,&range)&&CloseHandle(duplicate),61);
 require(LockFileEx(h,3,0,1,0,&range),62);lock_ready=CreateEventW(0,1,0,0);U worker=CreateThread(0,0,lock_worker,0,0,0);require(lock_ready&&worker&&!WaitForSingleObject(lock_ready,10000),63);
 Sleep(300);require(!lock_finished&&UnlockFileEx(h,0,1,0,&range)&&!WaitForSingleObject(worker,10000)&&lock_finished,64);require(CloseHandle(worker)&&CloseHandle(lock_ready),65);
 SI startup={0};PI process={0};startup.size=sizeof(startup);W command[]=L"files143 child";
 require(CreateProcessW(L"C:\\Program Files\\7-Zip\\child.exe",command,0,0,0,0,0,0,&startup,&process),20);
 unsigned code=259;require(!WaitForSingleObject(process.process,10000)&&GetExitCodeProcess(process.process,&code)&&!code,21);
 require(CloseHandle(process.process)&&CloseHandle(process.thread),22);
 seek(h,0);read(h,data,3);require(data[0]=='a'&&data[1]=='x'&&data[2]=='c',23);
 seek(h,65537);write(h,"Z",1);seek(h,65533);read(h,data,5);require(!data[0]&&!data[1]&&!data[2]&&!data[3]&&data[4]=='Z',24);
 seek(h,1);require(SetEndOfFile(h),25);seek(h,4);require(SetEndOfFile(h),26);seek(h,0);read(h,data,4);require(data[0]=='a'&&!data[1]&&!data[2]&&!data[3],27);
 seek(h,0);require(SetEndOfFile(h),28);write(h,"durable file bytes\n",19);require(FlushFileBuffers(h)&&CloseHandle(h),29);
 U reader=open(L"m143-file.bin",0x80000000u,1,3);require(reader!=~(U)0,33);
 U conflict=open(L"m143-file.bin",0x40000000u,7,3);require(conflict==~(U)0&&GetLastError()==32,34);
 require(!DeleteFileW(L"m143-file.bin")&&GetLastError()==32&&CloseHandle(reader),35);
 U pending=open(L"m143-delete.bin",0xc0010000u,7,2);require(pending!=~(U)0,36);
 U other=open(L"m143-delete.bin",0x80000000u,7,3);require(other!=~(U)0&&DeleteFileW(L"m143-delete.bin"),37);
 conflict=open(L"m143-delete.bin",0x80000000u,7,3);require(conflict==~(U)0&&GetLastError()==303,38);
 require(CloseHandle(pending)&&CloseHandle(other)&&GetFileAttributesW(L"m143-delete.bin")==~0u,39);
 DeleteFileW(L"M143-Rename.bin");pending=open(L"m143-rename.bin",0xc0010000u,7,2);require(pending!=~(U)0,40);
 write(pending,"R",1);require(MoveFileExW(L"m143-rename.bin",L"M143-Rename.bin",0),41);seek(pending,0);read(pending,data,1);require(data[0]=='R'&&CloseHandle(pending)&&DeleteFileW(L"M143-Rename.bin"),42);
 static const char pass[]="M143_NATIVE_SHARED_FILES_PASS\n";write(GetStdHandle((unsigned)-11),pass,sizeof(pass)-1);ExitProcess(0);
}
