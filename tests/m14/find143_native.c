/* Own PE probe for Unicode enumeration, extensionless names and stale searches. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned attributes,time[6],high,low,reserved[2];W name[260],alternate[14];} FIND;
_Static_assert(sizeof(FIND)==592,"Windows find data ABI");
__declspec(dllimport) U CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,U);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) U FindFirstFileW(const W*,FIND*);
__declspec(dllimport) int FindNextFileW(U,FIND*);
__declspec(dllimport) int FindClose(U);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static const W unicode_name[]=L"m143-find-R\u00e9sum\u00e9-\U0001f642.TXT",no_extension[]=L"m143-find-noextension";
static void require(int good,unsigned code){if(!good){char error[]="M143_FIND_CHECK_000\n";error[16]=(char)('0'+code/100);error[17]=(char)('0'+code/10%10);error[18]=(char)('0'+code%10);unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),error,sizeof(error)-1,&wrote,0);ExitProcess(code);}}
static int same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){
 DeleteFileW(unicode_name);DeleteFileW(no_extension);
 U file=CreateFileW(unicode_name,0x40000000u,7,0,1,128,0);require(file!=~(U)0&&CloseHandle(file),10);
 file=CreateFileW(no_extension,0x40000000u,7,0,1,128,0);require(file!=~(U)0&&CloseHandle(file),11);
 FIND data;U search=FindFirstFileW(L"M143-FIND-R\u00c9SUM\u00c9-?.txt",&data);require(search!=~(U)0&&same(data.name,unicode_name),12);
 require(!FindNextFileW(search,&data)&&GetLastError()==18&&FindClose(search),13);U stale=search;
 search=FindFirstFileW(L"M143-FIND-R\u00c9SUM\u00c9-?.txt",&data);require(search!=~(U)0&&search!=stale,14);
 require(!FindNextFileW(stale,&data)&&GetLastError()==6&&!FindClose(stale)&&GetLastError()==6&&FindClose(search),15);
 search=FindFirstFileW(L"m143-find-*.*",&data);require(search!=~(U)0,16);unsigned seen=0;
 do{if(same(data.name,unicode_name))seen|=1;if(same(data.name,no_extension))seen|=2;}while(FindNextFileW(search,&data));require(seen==3&&GetLastError()==18&&FindClose(search),17);
 search=FindFirstFileW(L"C:\\Users\\Owner\\Documents\\m143-find-missing\\*",&data);require(search==~(U)0&&GetLastError()==3,18);
 search=FindFirstFileW(L"C:\\Data\\*",&data);require(search==~(U)0&&GetLastError()==5,19);
 W malformed[]={0xd800,0};require(FindFirstFileW(malformed,&data)==~(U)0&&GetLastError()==1113,20);
 require(DeleteFileW(unicode_name)&&DeleteFileW(no_extension),21);
 static const char pass[]="M143_NATIVE_UNICODE_FIND_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),pass,sizeof(pass)-1,&wrote,0);ExitProcess(0);
}
