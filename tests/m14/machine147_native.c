/* Own probe of the real kernel install/remove authority and machine views. */
#define W8_USER
#include <engine/windows8.h>
typedef uint64_t H;typedef uint16_t W;
__declspec(dllimport) int RegCreateKeyExW(H,const W*,unsigned,W*,unsigned,unsigned,void*,H*,unsigned*);
__declspec(dllimport) int RegOpenKeyExW(H,const W*,unsigned,unsigned,H*);
__declspec(dllimport) int RegQueryValueExW(H,const W*,unsigned*,unsigned*,void*,unsigned*);
__declspec(dllimport) int RegSetValueExW(H,const W*,unsigned,unsigned,const void*,unsigned);
__declspec(dllimport) int RegDeleteValueW(H,const W*);
__declspec(dllimport) int RegDeleteKeyW(H,const W*);
__declspec(dllimport) int RegCloseKey(H);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
#define LM UINT64_C(0xffffffff80000002)
#define CU UINT64_C(0xffffffff80000001)
static const W key[]=L"Software\\Engacer147MachineProbe",parent[]=L"Software",leaf[]=L"Engacer147MachineProbe",name[]=L"ScopeValue";
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
static int read147(unsigned view,unsigned expected){H h=0;int status=RegOpenKeyExW(LM,key,0,0x20019u|view,&h);if(status==2)return 2;check147(!status&&h,10);unsigned value=0,bytes=4,type=0;check147(!RegQueryValueExW(h,name,0,&type,&value,&bytes)&&type==4&&bytes==4&&value==expected,11);check147(!RegCloseKey(h),12);return 0;}
static void pass147(const char*text){unsigned n=0;while(text[n])++n;unsigned wrote=0;check147(WriteFile(GetStdHandle((unsigned)-11),text,n,&wrote,0)&&wrote==n,90);ExitProcess(0);}
void entry(void);void*volatile anchor147=&entry;
void entry(void){
 unsigned command=*(const volatile uint32_t*)(uintptr_t)(W8_MAILBOX+4);int a=read147(0x100,0x14700064),b=read147(0x200,0x14700032);check147(a==b,13);
 if(command==W8_REMOVE){
  for(unsigned i=0;i<2;++i){unsigned view=i?0x200:0x100;H h=0;
   if(a==2){unsigned disposition=0,value=i?0x14700032:0x14700064;check147(!RegCreateKeyExW(LM,key,0,0,0,view|0x1000fu,0,&h,&disposition)&&h&&disposition==1,20);check147(!RegSetValueExW(h,name,0,4,&value,4)&&!RegCloseKey(h),21);}
   else{check147(!RegOpenKeyExW(LM,parent,0,view|0x1000fu,&h)&&h,22);check147(!RegDeleteKeyW(h,leaf)&&!RegCloseKey(h),23);}
  }
  if(a==2){check147(!read147(0x100,0x14700064)&&!read147(0x200,0x14700032),24);pass147("M147_MACHINE_CONFIRMED_WORKER_TWO_VIEWS_WRITE_PASS\n");}
  check147(read147(0x100,0)==2&&read147(0x200,0)==2,25);pass147("M147_MACHINE_REMOVE_AUTHORITY_CLEANUP_PASS\n");
 }
 check147(command==W8_RUN,30);H denied=123;unsigned disposition=0;check147(RegCreateKeyExW(LM,key,0,0,0,3,0,&denied,&disposition)==5&&denied==0,31);denied=123;check147(RegOpenKeyExW(LM,key,0,0x2001fu,&denied)==5&&denied==0,32);denied=123;check147(RegOpenKeyExW(LM,key,0,0x300u|1u,&denied)==87&&denied==0,33);
 H user=0;check147(RegOpenKeyExW(CU,key,0,1,&user)==2&&user==0,34);
 if(!a){H h=0;check147(!RegOpenKeyExW(LM,key,0,0x100u|0x20019u,&h),35);unsigned value=99;check147(RegSetValueExW(h,name,0,4,&value,4)==5&&RegDeleteValueW(h,name)==5,36);H child=0;check147(RegCreateKeyExW(h,L"Child",0,0,0,3,0,&child,0)==5&&child==0,37);check147(!RegCloseKey(h),38);pass147("M147_MACHINE_RUN_READ_ONLY_VIEWS_PASS\n");}
 pass147("M147_MACHINE_ABSENT_READ_ONLY_PASS\n");
}
