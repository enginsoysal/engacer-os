/* Real nested faults on independent Windows exception stacks. */
typedef unsigned long long U;typedef struct {unsigned code,flags;U next,address;unsigned count,pad;U args[15];} RECORD;typedef struct {RECORD*record;unsigned char*context;} POINTERS;
__declspec(dllimport) void* AddVectoredExceptionHandler(unsigned,int(*)(POINTERS*));
__declspec(dllimport) unsigned RemoveVectoredExceptionHandler(void*);
__declspec(dllimport) U CreateThread(void*,U,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
extern char resume_nested1142[],resume_nested2142[],resume_nested3142[],resume_nested4142[],resume_nested5142[];
#define FAULT142(n) __declspec(noinline) static void fault##n(void){__asm__ volatile("movq $" #n ", %%rax; movl $1,(%%rax); .global resume_nested" #n "142; resume_nested" #n "142:":::"rax","memory");}
FAULT142(1) FAULT142(2) FAULT142(3) FAULT142(4)
#ifdef OVERFLOW142
FAULT142(5)
#endif
static volatile unsigned handled;
static int handler(POINTERS*p){if(p->record->code!=0xc0000005u||p->record->count!=2||p->record->args[0]!=1)ExitProcess(61);U address=p->record->args[1];char*resume;
 if(address==1){fault2();resume=resume_nested1142;}else if(address==2){fault3();resume=resume_nested2142;}else if(address==3){fault4();resume=resume_nested3142;}else if(address==4){
#ifdef OVERFLOW142
 fault5();
#endif
 resume=resume_nested4142;}else ExitProcess(62);
 *(U*)(p->context+248)=(U)resume;__atomic_fetch_add(&handled,1,__ATOMIC_SEQ_CST);return -1;
}
static void cases(void){for(unsigned i=0;i<24;++i)fault1();}
static unsigned worker(void*unused){(void)unused;cases();return 0;}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){void*handle=AddVectoredExceptionHandler(1,handler);if(!handle)ExitProcess(63);U threads[4];for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,worker,0,0,0);if(!threads[i])ExitProcess(64);}cases();if(WaitForMultipleObjects(4,threads,1,30000))ExitProcess(65);for(unsigned i=0;i<4;++i)if(!CloseHandle(threads[i]))ExitProcess(66);if(handled!=480||!RemoveVectoredExceptionHandler(handle))ExitProcess(67);static const char ok[]="M142_NESTED_THREAD_FAULTS_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);}
