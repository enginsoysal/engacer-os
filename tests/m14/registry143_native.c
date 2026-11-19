/* Own Windows PE probe for durable user preferences and private key grants. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned size,pad;U reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;W show,reserved_bytes;unsigned pad2;U reserved_data,input,output,error;} SI;
typedef struct {U process,thread;unsigned pid,tid;} PI;
__declspec(dllimport) int RegCreateKeyExW(U,const W*,unsigned,W*,unsigned,unsigned,void*,U*,unsigned*);
__declspec(dllimport) int RegOpenKeyExW(U,const W*,unsigned,unsigned,U*);
__declspec(dllimport) int RegQueryValueExW(U,const W*,unsigned*,unsigned*,void*,unsigned*);
__declspec(dllimport) int RegSetValueExW(U,const W*,unsigned,unsigned,const void*,unsigned);
__declspec(dllimport) int RegCloseKey(U);
__declspec(dllimport) int RegDeleteValueW(U,const W*);
__declspec(dllimport) int RegDeleteKeyW(U,const W*);
__declspec(dllimport) int RegEnumValueW(U,unsigned,W*,unsigned*,unsigned*,unsigned*,void*,unsigned*);
__declspec(dllimport) int RegEnumKeyExW(U,unsigned,W*,unsigned*,unsigned*,W*,unsigned*,void*);
__declspec(dllimport) int RegFlushKey(U);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,SI*,PI*);
__declspec(dllimport) int GetExitCodeProcess(U,unsigned*);
__declspec(dllimport) unsigned WaitForSingleObject(U,unsigned);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) W* GetCommandLineW(void);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void SetLastError(unsigned);
#define HKCU ((U)0xffffffff80000001ULL)
#define ALL 0xf003fu
static const W key_name[]=L"Software\\EngacerM143\\R\u00e9sum\u00e9-\U0001f642";
static void print(const char*text,unsigned size){unsigned wrote=0;WriteFile(GetStdHandle((unsigned)-11),text,size,&wrote,0);}
static void require(int good,unsigned code){if(!good){char text[]="M143_REGISTRY_CHECK_000\n";text[20]=(char)('0'+code/100);text[21]=(char)('0'+code/10%10);text[22]=(char)('0'+code%10);print(text,sizeof(text)-1);ExitProcess(code);}}
#ifndef READ143
static int same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
#endif
static unsigned count_value(U key){unsigned value=0,type=0,bytes=4;require(!RegQueryValueExW(key,L"COUNT",0,&type,&value,&bytes)&&type==4&&bytes==4,10);return value;}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){
 U key=0;
#ifdef READ143
 require(!RegOpenKeyExW(HKCU,key_name,0,1,&key)&&count_value(key)==0x87654321u,11);
 require(!RegCloseKey(key),12);static const char pass[]="M143_REGISTRY_RESTART_PASS\n";print(pass,sizeof(pass)-1);ExitProcess(0);
#else
 if(same(GetCommandLineW(),L"registry143 child")){
  require(!RegOpenKeyExW(HKCU,key_name,0,ALL,&key)&&count_value(key)==0x12345678u,13);
  unsigned value=0x87654321u;require(!RegSetValueExW(key,L"Count",0,4,&value,4)&&!RegFlushKey(key)&&!RegCloseKey(key),14);ExitProcess(0);
 }
 unsigned disposition=0;require(!RegCreateKeyExW(HKCU,key_name,0,0,0,ALL,0,&key,&disposition)&&(disposition==1||disposition==2),15);
 U refused=0;W malformed[]={0xd800,0};require(RegCreateKeyExW(HKCU,malformed,0,0,0,ALL,0,&refused,0)==1113&&!refused,44);
 require(RegCreateKeyExW(HKCU,L"Software\\EngacerM143\\Volatile",0,0,1,ALL,0,&refused,0)==50&&!refused,45);
 require(RegOpenKeyExW(HKCU,key_name,0,0x100u|1,&refused)==50&&!refused,46);
 unsigned value=0x12345678u;require(!RegSetValueExW(key,L"Count",0,4,&value,4)&&count_value(key)==value,16);
 unsigned char binary[]={0,0x7f,0xff};require(!RegSetValueExW(key,L"Blob",0,3,binary,3),17);
 require(RegSetValueExW(key,L"Oversized",0,3,binary,2049)==1450,47);
 unsigned type=0,bytes=0;require(!RegQueryValueExW(key,L"BLOB",0,&type,0,&bytes)&&type==3&&bytes==3,18);
 unsigned char guarded[]={0xa5,0xa5,0xa5,0xa5};bytes=2;require(RegQueryValueExW(key,L"blob",0,&type,guarded,&bytes)==234&&bytes==3&&guarded[3]==0xa5,19);
 bytes=3;require(!RegQueryValueExW(key,L"Blob",0,&type,guarded,&bytes)&&guarded[0]==0&&guarded[1]==0x7f&&guarded[2]==0xff&&guarded[3]==0xa5,20);
 W raw[]={'a','b','c'},text[4]={0,0,0,0x1234};require(!RegSetValueExW(key,L"Text",0,1,raw,6),21);
 bytes=6;require(!RegQueryValueExW(key,L"Text",0,&type,text,&bytes)&&bytes==6&&text[0]=='a'&&text[2]=='c'&&text[3]==0x1234,22);
 require(RegQueryValueExW(key,0,0,&type,0,&bytes)==2||bytes==0,23);
 require(!RegSetValueExW(key,0,0,3,0,0),24);bytes=99;require(!RegQueryValueExW(key,0,0,&type,0,&bytes)&&type==3&&!bytes,25);
 U read=0;require(!RegOpenKeyExW(HKCU,L"software\\engacerm143\\R\u00c9SUM\u00c9-\U0001f642",0,1,&read),26);
 require(count_value(read)==value&&RegSetValueExW(read,L"Count",0,4,&value,4)==5,27);
 U stale=read;require(!RegCloseKey(read)&&!RegOpenKeyExW(HKCU,key_name,0,1,&read)&&read!=stale,28);
 bytes=4;require(RegQueryValueExW(stale,L"Count",0,&type,&value,&bytes)==6&&!RegCloseKey(read),29);
 unsigned entries=0;for(unsigned i=0;i<8;++i){W name[256];unsigned units=256;unsigned char data[2048];bytes=sizeof(data);int status=RegEnumValueW(key,i,name,&units,0,&type,data,&bytes);if(status==259)break;require(!status&&units<256&&name[units]==0,30);++entries;}require(entries==4,31);
 W tiny[2]={0x1234,0x5678};unsigned units=1;bytes=0;require(RegEnumValueW(key,0,tiny,&units,0,&type,0,&bytes)==234&&units>1&&tiny[0]==0x1234&&tiny[1]==0x5678,32);
 U parent=0;require(!RegOpenKeyExW(HKCU,L"Software\\EngacerM143",0,ALL,&parent),33);W child_name[256];units=256;
 require(!RegEnumKeyExW(parent,0,child_name,&units,0,0,0,0)&&same(child_name,L"R\u00e9sum\u00e9-\U0001f642"),34);
 require(RegDeleteKeyW(HKCU,L"Software\\EngacerM143")==5&&!RegCloseKey(parent),35);
 U deleted=0,recreated=0;require(!RegCreateKeyExW(HKCU,L"Software\\EngacerM143\\DeleteMe",0,0,0,ALL,0,&deleted,0),36);
 require(!RegDeleteKeyW(HKCU,L"Software\\EngacerM143\\DeleteMe")&&!RegCreateKeyExW(HKCU,L"Software\\EngacerM143\\DeleteMe",0,0,0,ALL,0,&recreated,0),37);
 bytes=4;require(RegQueryValueExW(deleted,L"x",0,0,&value,&bytes)==1018&&!RegCloseKey(deleted)&&!RegCloseKey(recreated)&&!RegDeleteKeyW(HKCU,L"Software\\EngacerM143\\DeleteMe"),38);
 require(!RegDeleteValueW(key,L"Blob"),39);bytes=0;require(RegQueryValueExW(key,L"Blob",0,0,0,&bytes)==2&&!RegSetValueExW(key,L"Blob",0,3,binary,3),40);
 SetLastError(0x143);bytes=0;require(RegQueryValueExW(key,L"Missing",0,0,0,&bytes)==2&&GetLastError()==0x143,48);
 SI startup={0};PI process={0};startup.size=sizeof(startup);W command[]=L"registry143 child";
 require(CreateProcessW(L"C:\\Program Files\\7-Zip\\child.exe",command,0,0,0,0,0,0,&startup,&process),41);
 unsigned code=259;require(!WaitForSingleObject(process.process,10000)&&GetExitCodeProcess(process.process,&code)&&!code,42);
 require(CloseHandle(process.process)&&CloseHandle(process.thread)&&count_value(key)==0x87654321u&&!RegFlushKey(key)&&!RegCloseKey(key),43);
 static const char pass[]="M143_NATIVE_REGISTRY_PASS\n";print(pass,sizeof(pass)-1);ExitProcess(0);
#endif
}
