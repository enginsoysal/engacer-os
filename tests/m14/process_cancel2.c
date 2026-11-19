/* Native task-group cancellation fixture; never executed on the host. */
typedef unsigned long long U;typedef unsigned short W;
typedef struct {unsigned size,pad;U reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;W show,reserved_bytes;unsigned pad2;U reserved_data,input,output,error;} SI;
typedef struct {U process,thread;unsigned pid,tid;} PI;
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,SI*,PI*);
__declspec(dllimport) W* GetCommandLineW(void);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){W*command=GetCommandLineW();if(command[0]=='g'&&command[1]=='r'){Sleep(60000);ExitProcess(1);}
 for(unsigned i=0;i<3;++i){SI si={0};PI pi;W text[]=L"group child";si.size=sizeof(si);if(!CreateProcessW(L"C:\\Program Files\\7-Zip\\child.exe",text,0,0,0,0,0,0,&si,&pi))ExitProcess(2);}
 static const char ready[]="M142_PROCESS_GROUP_CANCEL_READY\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ready,sizeof(ready)-1,&wrote,0);Sleep(60000);ExitProcess(3);
}
