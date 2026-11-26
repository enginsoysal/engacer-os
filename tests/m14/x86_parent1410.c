#include <stdint.h>
typedef uint64_t H;
typedef uint16_t W;
typedef struct {unsigned size,pad;H reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;uint16_t show,reserved_bytes;unsigned pad2;H reserved_data,input,output,error;} Startup;
typedef struct {H process,thread;unsigned pid,tid;} Process;
__declspec(dllimport) int CreateProcessW(const W*,W*,void*,void*,int,unsigned,void*,const W*,Startup*,Process*);
__declspec(dllimport) unsigned WaitForSingleObject(H,unsigned);
__declspec(dllimport) int GetExitCodeProcess(H,unsigned*);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) H GetStdHandle(int);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int CloseHandle(H);
static void run(const W *name,unsigned expected){
 Startup startup={0};startup.size=sizeof(startup);
 Process process={0};
 if(!CreateProcessW(name,0,0,0,0,0,0,0,&startup,&process))ExitProcess(91);
 if(WaitForSingleObject(process.process,30000)!=0)ExitProcess(92);
 unsigned status=0;
 if(!GetExitCodeProcess(process.process,&status)||status!=expected)ExitProcess(93);
 if(!CloseHandle(process.thread)||!CloseHandle(process.process))ExitProcess(94);
}
static const W paths[][64]={
 L"C:\\Program Files\\7-Zip\\helper32.exe",L"C:\\Program Files\\7-Zip\\fault32.exe"
};
static const W *volatile children[]={paths[0],paths[1]};
void entry(void){
 run(children[0],0);run(children[1],0xc000001du);
 static const char text[]="M1410_X64_PARENT_I386_CHILD_PASS\n";
 unsigned bytes=0;
 if(!WriteFile(GetStdHandle(-11),text,sizeof(text)-1,&bytes,0)||bytes!=sizeof(text)-1)ExitProcess(95);
 ExitProcess(0);
}
