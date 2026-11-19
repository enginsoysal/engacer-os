/* Compiler-generated C structured exception and finally metadata. */
typedef unsigned long long U;
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
static volatile unsigned finally_count,caught;
__declspec(noinline) static void fault(void){volatile U address=1;*(volatile unsigned*)(U)address=7;}
__declspec(noinline) static void inner(void){__try{fault();}__finally{++finally_count;}}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){for(unsigned i=0;i<12;++i){__try{inner();}__except(1){++caught;}}if(finally_count!=12||caught!=12)ExitProcess(91);static const char ok[]="M142_C_SEH_FINALLY_UNWIND_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);}
