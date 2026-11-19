/* Compiler-generated C filters/finally on independent Windows thread stacks. */
typedef unsigned long long U;
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) U CreateThread(void*,U,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) int CloseHandle(U);
static const unsigned char unwind_scratch142[128]="ENGACER_UNWIND_SCRATCH_142";
const void* volatile unwind_scratch_anchor142=unwind_scratch142;
static volatile unsigned finally_count,filter_count,caught;
__declspec(noinline) static void fault(void){volatile U address=1;*(volatile unsigned*)(U)address=7;}
__declspec(noinline) static void inner(void){__try{fault();}__finally{__atomic_fetch_add(&finally_count,1,__ATOMIC_SEQ_CST);}}
__declspec(noinline) static int filter(unsigned cookie){if(cookie<0x1420||cookie>0x1424)ExitProcess(92);__atomic_fetch_add(&filter_count,1,__ATOMIC_SEQ_CST);return 1;}
__declspec(noinline) static void cases(unsigned value){volatile unsigned cookie=value;for(unsigned i=0;i<12;++i){__try{inner();}__except(filter(cookie)){__atomic_fetch_add(&caught,1,__ATOMIC_SEQ_CST);}}}
static unsigned worker(void*value){cases((unsigned)(U)value);return 0;}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){U threads[4];for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,worker,(void*)(U)(0x1421+i),0,0);if(!threads[i])ExitProcess(93);}cases(0x1420);if(WaitForMultipleObjects(4,threads,1,30000))ExitProcess(94);for(unsigned i=0;i<4;++i)if(!CloseHandle(threads[i]))ExitProcess(95);if(finally_count!=60||filter_count!=60||caught!=60)ExitProcess(91);static const char ok[]="M142_C_SEH_FINALLY_UNWIND_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);}
