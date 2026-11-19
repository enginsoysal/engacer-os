/* Own PE probe: copied environments, bounded ownership and atomic temporary files. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned size,pad;U reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;W show,reserved_bytes;unsigned pad2;U reserved_data,input,output,error;} SI;
typedef struct {U process,thread;unsigned pid,tid;} PI;
__declspec(dllimport) unsigned GetEnvironmentVariableW(const W*,W*,unsigned);
__declspec(dllimport) unsigned GetEnvironmentVariableA(const char*,char*,unsigned);
__declspec(dllimport) int SetEnvironmentVariableW(const W*,const W*);
__declspec(dllimport) int SetEnvironmentVariableA(const char*,const char*);
__declspec(dllimport) W* GetEnvironmentStringsW(void);
__declspec(dllimport) char* GetEnvironmentStringsA(void);
__declspec(dllimport) int FreeEnvironmentStringsW(W*);
__declspec(dllimport) int FreeEnvironmentStringsA(char*);
__declspec(dllimport) unsigned ExpandEnvironmentStringsW(const W*,W*,unsigned);
__declspec(dllimport) unsigned ExpandEnvironmentStringsA(const char*,char*,unsigned);
__declspec(dllimport) unsigned GetTempPathW(unsigned,W*);
__declspec(dllimport) unsigned GetTempPathA(unsigned,char*);
__declspec(dllimport) unsigned GetTempFileNameW(const W*,const W*,unsigned,W*);
__declspec(dllimport) unsigned GetTempFileNameA(const char*,const char*,unsigned,char*);
__declspec(dllimport) unsigned GetFileAttributesW(const W*);
__declspec(dllimport) int DeleteFileW(const W*);
__declspec(dllimport) U CreateFileW(const W*,unsigned,unsigned,void*,unsigned,unsigned,U);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,SI*,PI*);
__declspec(dllimport) unsigned ResumeThread(U);
__declspec(dllimport) unsigned WaitForSingleObject(U,unsigned);
__declspec(dllimport) int GetExitCodeProcess(U,unsigned*);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) W* GetCommandLineW(void);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int ReadFile(U,void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static const W variable[]=L"R\u00e9sum\u00e9";
static void require(int good,unsigned code){if(!good){char error[]="M143_ENV_CHECK_000\n";error[15]=(char)('0'+code/100);error[16]=(char)('0'+code/10%10);error[17]=(char)('0'+code%10);unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),error,sizeof(error)-1,&wrote,0);ExitProcess(code);}}
static int same(const W*a,const W*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static int same_a(const char*a,const char*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static unsigned length(const W*s){unsigned n=0;while(s[n])++n;return n;}
static PI spawn(W*command,unsigned flags,void*environment){SI startup={0};PI process={0};startup.size=sizeof(startup);require(CreateProcessW(L"C:\\Program Files\\7-Zip\\child.exe",command,0,0,0,flags,environment,0,&startup,&process),40);return process;}
static void join(PI process){unsigned code=259;require(!WaitForSingleObject(process.process,10000)&&GetExitCodeProcess(process.process,&code)&&!code,41);require(CloseHandle(process.process)&&CloseHandle(process.thread),42);}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){
 W buffer[512];char narrow[1024];W*command=GetCommandLineW();
 if(same(command,L"environment143 inherited")){
  require(GetEnvironmentVariableW(L"R\u00c9SUM\u00c9",buffer,512)==6&&same(buffer,L"before"),10);
  require(!GetEnvironmentVariableW(L"Empty",buffer,512)&&GetLastError()==0,11);
  require(SetEnvironmentVariableW(variable,L"child"),12);ExitProcess(0);
 }
 if(same(command,L"environment143 unicode")||same(command,L"environment143 ansi")){
  require(GetEnvironmentVariableW(L"ONLY",buffer,512)>0&&same(buffer,L"custom-\u00e9"),13);
  require(!GetEnvironmentVariableW(L"USERPROFILE",buffer,512)&&GetLastError()==203,14);
  require(GetEnvironmentVariableA("Only",narrow,1024)==9&&same_a(narrow,"custom-\xc3\xa9"),15);ExitProcess(0);
 }
 W profile[512],old_temp[261];require(GetEnvironmentVariableW(L"USERPROFILE",profile,512)>0&&GetTempPathW(261,old_temp)>0,16);
 require(SetEnvironmentVariableW(variable,L"before")&&SetEnvironmentVariableW(L"Empty",L""),17);
 require(GetEnvironmentVariableW(L"R\u00c9SUM\u00c9",0,0)==7,18);W guard[2]={0x1234,0x5678};require(GetEnvironmentVariableW(variable,guard,1)==7&&guard[1]==0x5678,19);
 W*copy=GetEnvironmentStringsW();char*ansi_copy=GetEnvironmentStringsA();require(copy&&ansi_copy,20);
 require(!FreeEnvironmentStringsW((W*)ansi_copy)&&GetLastError()==87&&FreeEnvironmentStringsA(ansi_copy),21);
 W inherited[]=L"environment143 inherited";PI child=spawn(inherited,4,0);
 require(SetEnvironmentVariableW(variable,L"after")&&ResumeThread(child.thread)==1,22);join(child);require(GetEnvironmentVariableW(variable,buffer,512)==5&&same(buffer,L"after"),23);
 unsigned saw_old=0;for(unsigned i=0;copy[i];i+=length(copy+i)+1)if(same(copy+i,L"R\u00e9sum\u00e9=before"))saw_old=1;require(saw_old&&FreeEnvironmentStringsW(copy)&&!FreeEnvironmentStringsW(copy),24);
 require(ExpandEnvironmentStringsW(L"%R\u00c9SUM\u00c9%/%Missing%",buffer,512)==16&&same(buffer,L"after/%Missing%"),25);
 require(SetEnvironmentVariableA("Utf8","\xc3\xa9-\xf0\x9f\x99\x82")&&GetEnvironmentVariableA("UTF8",narrow,1024)==7&&same_a(narrow,"\xc3\xa9-\xf0\x9f\x99\x82"),26);
 require(ExpandEnvironmentStringsA("%Utf8%",narrow,1024)==8&&same_a(narrow,"\xc3\xa9-\xf0\x9f\x99\x82"),27);
 W explicit_w[]=L"Zed=end\0Only=custom-\u00e9\0Empty=\0\0";W unicode_command[]=L"environment143 unicode";join(spawn(unicode_command,0x400,explicit_w));
 char explicit_a[]="Only=custom-\xc3\xa9\0Empty=\0\0";W ansi_command[]=L"environment143 ansi";join(spawn(ansi_command,0,explicit_a));
 SI refused_start={0};PI refused={0};refused_start.size=sizeof(refused_start);W invalid_block[]={0xd800,'=','x',0,0};
 require(!CreateProcessW(L"C:\\Program Files\\7-Zip\\child.exe",unicode_command,0,0,0,0x400,invalid_block,0,&refused_start,&refused)&&GetLastError()==1113&&!refused.process&&!refused.thread,45);
 W no_equals[]=L"NoEquals\0\0";require(!CreateProcessW(L"C:\\Program Files\\7-Zip\\child.exe",unicode_command,0,0,0,0x400,no_equals,0,&refused_start,&refused)&&GetLastError()==87&&!refused.process&&!refused.thread,46);
 W malformed[]={0xd800,0};require(!SetEnvironmentVariableW(malformed,L"x")&&GetLastError()==1113,28);
 require(!SetEnvironmentVariableW(L"a=b",L"x")&&GetLastError()==87,29);
 require(SetEnvironmentVariableW(L"Gone",L"x")&&SetEnvironmentVariableW(L"gONE",0)&&!GetEnvironmentVariableW(L"Gone",buffer,512)&&GetLastError()==203,30);
 unsigned filled=0;for(unsigned n=0;n<65;++n){W name[]=L"Capacity00";name[8]=(W)('0'+n/10);name[9]=(W)('0'+n%10);if(!SetEnvironmentVariableW(name,L"bounded")){require(GetLastError()==8,47);break;}++filled;}require(filled&&filled<64,48);
 W*full=GetEnvironmentStringsW();require(full!=0,49);unsigned entries=0;for(unsigned at=0;full[at];at+=length(full+at)+1)++entries;require(entries==64&&FreeEnvironmentStringsW(full),50);
 for(unsigned n=0;n<filled;++n){W name[]=L"Capacity00";name[8]=(W)('0'+n/10);name[9]=(W)('0'+n%10);require(SetEnvironmentVariableW(name,0),51);}
 W*copies[32];for(unsigned n=0;n<32;++n){copies[n]=GetEnvironmentStringsW();require(copies[n]!=0,52);}require(!GetEnvironmentStringsW()&&GetLastError()==8,53);for(unsigned n=0;n<32;++n)require(FreeEnvironmentStringsW(copies[n]),54);
 require(SetEnvironmentVariableW(L"USERPROFILE",L"C:\\Data"),31);U escaped=CreateFileW(L"C:\\Data\\environment-escape.txt",0x40000000u,0,0,2,128,0);require(escaped==~(U)0&&GetLastError()==5&&SetEnvironmentVariableW(L"USERPROFILE",profile),32);
 const W*missing=L"C:\\Users\\Owner\\Documents\\m143-no-directory";require(GetFileAttributesW(missing)==~0u&&SetEnvironmentVariableW(L"TMP",missing),33);
 require(GetTempPathW(512,buffer)>0&&GetFileAttributesW(missing)==~0u,34);W first[260],second[260];require(!GetTempFileNameW(buffer,L"no",0,first)&&GetLastError()==3,35);
 require(SetEnvironmentVariableW(L"TMP",old_temp)&&GetTempPathW(512,buffer)>0,36);
 require(GetTempFileNameW(buffer,L"ow",0x12345678u,first)==0x12345678u&&GetFileAttributesW(first)==~0u,37);
 unsigned number=GetTempFileNameW(buffer,L"ow",0,first);require(number!=0,38);unsigned next=(number+1)&65535;if(!next)next=1;W collision[260];require(GetTempFileNameW(buffer,L"ow",next,collision)==next,55);
 U kept=CreateFileW(collision,0x40000000u,0,0,1,128,0);unsigned transferred=0;require(kept!=~(U)0&&WriteFile(kept,"kept",4,&transferred,0)&&transferred==4&&CloseHandle(kept),56);
 unsigned second_number=GetTempFileNameW(buffer,L"ow",0,second);require(second_number&&second_number!=next&&!same(first,second),57);
 kept=CreateFileW(collision,0x80000000u,1,0,3,128,0);char retained[5]={0};require(kept!=~(U)0&&ReadFile(kept,retained,4,&transferred,0)&&transferred==4&&same_a(retained,"kept")&&CloseHandle(kept),58);
 require(DeleteFileW(first)&&DeleteFileW(second)&&DeleteFileW(collision)&&GetTempPathA(1024,narrow)>0,39);
 char temp_a[260];require(GetTempFileNameA(narrow,"aw",0,temp_a)>0,43);W converted[260];unsigned i=0;for(;temp_a[i]&&i<259;++i)converted[i]=(unsigned char)temp_a[i];converted[i]=0;require(DeleteFileW(converted),44);
 static const char pass[]="M143_NATIVE_ENVIRONMENT_TEMP_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),pass,sizeof(pass)-1,&wrote,0);ExitProcess(0);
}
