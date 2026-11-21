/* Owned ordinary file copies; original installer qualification is separate. */
typedef unsigned long long U;typedef unsigned short W;
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int ReadFile(U,void*,unsigned,unsigned*,void*);
__declspec(dllimport) U CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,U);
__declspec(dllimport) unsigned GetTempPathW(unsigned,W*);
__declspec(dllimport) int CopyFileW(const W*,const W*,int);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) int SetFileAttributesW(const W*,unsigned);
__declspec(dllimport) unsigned GetFileAttributesW(const W*);
__declspec(dllimport) int GetFileAttributesExW(const W*,unsigned,void*);
__declspec(dllimport) int SetFileTime(U,const U*,const U*,const U*);
__declspec(dllimport) unsigned FormatMessageA(unsigned,const void*,unsigned,unsigned,void*,unsigned,void*);
__declspec(dllimport) void* LocalFree(void*);
static unsigned char data[8193],readback[8193];
static void check(int value,unsigned code){if(!value)ExitProcess(code);}
static void append(W*path,unsigned n,const W*tail){while(*tail)path[n++]=*tail++;path[n]=0;}
static void verify(const W*path){U f=CreateFileW(path,0x80000000,1,0,3,0x80,0);check(f!=~0ull,111);unsigned got=0;check(ReadFile(f,readback,sizeof(readback),&got,0)&&got==sizeof(readback)&&CloseHandle(f),112);for(unsigned i=0;i<sizeof(data);++i)check(data[i]==readback[i],113);}
void entry(void);void*volatile relocation_anchor=&entry;
void entry(void){char*message=0;unsigned chars=FormatMessageA(0x1300,0,8,0x400,&message,0,0);check(chars&&message&&message[chars]==0&&!LocalFree(message),125);char guard[4]={'x','y','z',0};check(!FormatMessageA(0x1200,0,5,0,guard,3,0)&&GetLastError()==122&&guard[0]=='x',126);check(!FormatMessageA(0x1200,0,0x1234567,0,guard,4,0)&&GetLastError()==317,127);W a[256],b[256];unsigned n=GetTempPathW(240,a);check(n&&n<240,101);for(unsigned i=0;i<=n;++i)b[i]=a[i];append(a,n,L"copy148-source.bin");append(b,n,L"copy148-target.bin");
 SetFileAttributesW(a,0x80);DeleteFileW(a);SetFileAttributesW(b,0x80);DeleteFileW(b);
 for(unsigned i=0;i<sizeof(data);++i)data[i]=(unsigned char)(i*37+11);
 U f=CreateFileW(a,0x40000000,0,0,1,0x80,0);unsigned wrote=0;U times[3]={133000000000000000ull,133100000000000000ull,133200000000000000ull};check(f!=~0ull&&WriteFile(f,data,sizeof(data),&wrote,0)&&wrote==sizeof(data)&&SetFileTime(f,times,times+1,times+2)&&CloseHandle(f),102);
 check(SetFileAttributesW(a,0x23)&&CopyFileW(a,b,1),103);verify(b);check(GetFileAttributesW(b)==0x23,104);
 unsigned meta[9];check(GetFileAttributesExW(b,0,meta),105);for(unsigned i=0;i<3;++i)check(((U)meta[2+i*2]<<32|meta[1+i*2])==times[i],106);
 check(!CopyFileW(a,b,2)&&GetLastError()==80,107);check(!CopyFileW(a,b,0)&&GetLastError()==5,108);verify(b);
 check(SetFileAttributesW(a,0x80)&&SetFileAttributesW(b,0x80),109);check(!CopyFileW(a,a,0)&&GetLastError()==32,110);verify(a);
 f=CreateFileW(b,0x40000000,0,0,2,0x80,0);check(f!=~0ull&&WriteFile(f,"short",5,&wrote,0)&&CloseHandle(f),114);check(CopyFileW(a,b,0),115);verify(b);
 check(DeleteFileW(a)&&!CopyFileW(a,b,0)&&GetLastError()==2,116);verify(b);check(DeleteFileW(b),117);
 f=CreateFileW(a,0x40000000,0,0,1,0x80,0);check(f!=~0ull&&CloseHandle(f)&&CopyFileW(a,b,1),118);check(GetFileAttributesExW(b,0,meta)&&!meta[7]&&!meta[8]&&DeleteFileW(a)&&DeleteFileW(b),119);
 check(CopyFileW(L"C:\\Users\\Owner\\Downloads\\copy148-large.bin",b,1),120);
 f=CreateFileW(b,0x80000000,1,0,3,0x80,0);check(f!=~0ull,121);unsigned total=0;
 for(;;){unsigned got=0;check(ReadFile(f,readback,4096,&got,0),122);if(!got)break;for(unsigned j=0;j<got;++j)check(readback[j]==(unsigned char)((total+j)*37+11),123);total+=got;}
 check(total==11u*1024*1024&&CloseHandle(f)&&DeleteFileW(b),124);
 static const char ok[]="M148_COPY_FILE_BYTES_REPLACEMENT_METADATA_GUARDS_PASS\n";WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);
}
