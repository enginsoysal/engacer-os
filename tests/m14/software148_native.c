/* Actual software raises, C filters/finally and vectored continuation in CPL3. */
typedef unsigned long long U;
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) U CreateThread(void*,U,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) int CloseHandle(U);
static const unsigned char unwind_scratch142[128]="ENGACER_UNWIND_SCRATCH_142";
const void* volatile unwind_scratch_anchor142=unwind_scratch142;
__declspec(dllimport) void RaiseException(unsigned,unsigned,unsigned,const U*);
typedef struct {unsigned code,flags;U next,address;unsigned count,pad;U args[15];} RECORD;
typedef struct {RECORD*record;unsigned char*context;} POINTERS;
__declspec(dllimport) void* AddVectoredExceptionHandler(unsigned,int(*)(POINTERS*));
__declspec(dllimport) unsigned RemoveVectoredExceptionHandler(void*);
static volatile unsigned finally_count,filter_count,caught,continued;
static int resume(POINTERS*p){if(p->record->code!=0x6148148)return 0;if(p->record->flags||p->record->count!=3||p->record->args[0]!=0x123456789abcdef0ull||p->record->args[1]!=7||p->record->args[2]!=0xffffffffffffffffull)ExitProcess(96);++continued;return -1;}

__declspec(noinline) static void fault(void){U args[3]={0x1000,0,0};RaiseException(0x406d1388,0,3,args);}
__declspec(noinline) static void inner(void){__try{fault();}__finally{__atomic_fetch_add(&finally_count,1,__ATOMIC_SEQ_CST);}}
__declspec(noinline) static int filter(unsigned cookie){if(cookie<0x1420||cookie>0x1424)ExitProcess(92);__atomic_fetch_add(&filter_count,1,__ATOMIC_SEQ_CST);return 1;}
__declspec(noinline) static void cases(unsigned value){volatile unsigned cookie=value;for(unsigned i=0;i<12;++i){__try{inner();}__except(filter(cookie)){__atomic_fetch_add(&caught,1,__ATOMIC_SEQ_CST);}}}
static unsigned worker(void*value){cases((unsigned)(U)value);return 0;}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){void*h=AddVectoredExceptionHandler(1,resume);if(!h)ExitProcess(97);U args[3]={0x123456789abcdef0ull,7,~0ull};for(unsigned i=0;i<48;++i)RaiseException(0x6148148,0,3,args);if(continued!=48||!RemoveVectoredExceptionHandler(h))ExitProcess(98);U threads[4];for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,worker,(void*)(U)(0x1421+i),0,0);if(!threads[i])ExitProcess(93);}cases(0x1420);if(WaitForMultipleObjects(4,threads,1,30000))ExitProcess(94);for(unsigned i=0;i<4;++i)if(!CloseHandle(threads[i]))ExitProcess(95);if(finally_count!=60||filter_count!=60||caught!=60)ExitProcess(91);static const char ok[]="M148_SOFTWARE_VECTORED_C_SEH_FINALLY_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);}
