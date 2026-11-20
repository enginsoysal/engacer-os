/* Owned native protection changes, real write faults, image and allocation ranges. */
typedef unsigned long long U;typedef struct {unsigned code,flags;U next,address;unsigned count,pad;U args[15];} RECORD;
typedef struct {RECORD*record;unsigned char*context;} POINTERS;
__declspec(dllimport) void*AddVectoredExceptionHandler(unsigned,int(*)(POINTERS*));
__declspec(dllimport) unsigned RemoveVectoredExceptionHandler(void*);
__declspec(dllimport) void*VirtualAlloc(void*,U,unsigned,unsigned);
__declspec(dllimport) int VirtualFree(void*,U,unsigned);
__declspec(dllimport) int VirtualProtect(void*,U,unsigned,unsigned*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
#pragma section(".vptest",read,write)
__declspec(allocate(".vptest")) __declspec(align(4096)) static volatile unsigned char image145[8192]={17};
static volatile U expected145;static volatile unsigned faults145;
extern char resume_write145[];
static void check(int yes,unsigned code){if(!yes)ExitProcess(code);}
static int fault145(POINTERS*p){if(p->record->code!=0xc0000005u||p->record->count!=2||p->record->args[0]!=1||p->record->args[1]!=expected145)ExitProcess(90);++faults145;*(U*)(p->context+248)=(U)resume_write145;return -1;}
__declspec(noinline) static void blocked145(volatile unsigned char*p){expected145=(U)p;__asm__ volatile("movb $99,(%0); .global resume_write145; resume_write145:"::"r"(p):"memory");}
void entry(void);void*volatile anchor145=&entry;
void entry(void){
 unsigned old=0;void*handler=AddVectoredExceptionHandler(1,fault145);check(handler!=0,10);
 image145[0]=17;image145[4096]=23;
 check(VirtualProtect((void*)(image145+1),1,2,&old)&&old==4,11);blocked145(image145);check(image145[0]==17&&faults145==1,12);
 image145[4096]=29;check(VirtualProtect((void*)image145,4096,4,&old)&&old==2,13);image145[0]=31;
 check(VirtualProtect((void*)(image145+4095),2,2,&old)&&old==4,14);blocked145(image145);blocked145(image145+4096);check(faults145==3&&image145[4096]==29,15);
 check(VirtualProtect((void*)image145,8192,4,&old)&&old==2,16);image145[0]=17;image145[4096]=23;
 volatile unsigned char*p=VirtualAlloc(0,8192,0x3000,4);check(p!=0,17);p[0]=42;p[4096]=57;
 check(VirtualProtect((void*)p,4096,2,&old)&&old==4,18);blocked145(p);check(faults145==4&&p[0]==42,19);p[4096]=58;
 old=123;check(!VirtualProtect((void*)p,12288,4,&old)&&GetLastError()==487&&old==123,20);blocked145(p);check(faults145==5,21);
 check(!VirtualProtect((void*)p,4096,4,(unsigned*)1)&&GetLastError()==998,22);blocked145(p);check(faults145==6,23);
 check(!VirtualProtect((void*)p,4096,64,&old)&&GetLastError()==50,24);blocked145(p);check(faults145==7,25);
 check(!VirtualProtect((void*)p,0,4,&old)&&GetLastError()==87,26);
 check(VirtualProtect((void*)p,4096,4,&old)&&old==2,27);p[0]=61;
 /* Execute copied native instructions only after the real RW -> RX transition. */
 p[0]=0xb8;p[1]=42;p[2]=0;p[3]=0;p[4]=0;p[5]=0xc3;
 check(VirtualProtect((void*)p,4096,32,&old)&&old==4,28);check(((int(*)(void))p)()==42,29);blocked145(p);check(faults145==8,30);
 check(VirtualProtect((void*)p,4096,4,&old)&&old==32,31);p[0]=62;
 check(VirtualFree((void*)p,0,0x8000),32);check(!VirtualProtect((void*)p,4096,2,&old)&&GetLastError()==487,33);
 check(RemoveVectoredExceptionHandler(handler)!=0,34);
 static const char ok[]="M145_PROTECTION_EIGHT_REAL_FAULTS_PASS\n";unsigned written;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&written,0);ExitProcess(0);
}
