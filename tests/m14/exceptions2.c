/* Real hardware faults handled through the Windows x64 ABI in CPL3. */
typedef unsigned long long U;typedef struct {unsigned code,flags;U next,address;unsigned count,pad;U args[15];} RECORD;
typedef struct {RECORD*record;unsigned char*context;} POINTERS;
__declspec(dllimport) void* AddVectoredExceptionHandler(unsigned,int(*)(POINTERS*));
__declspec(dllimport) void* AddVectoredContinueHandler(unsigned,int(*)(POINTERS*));
__declspec(dllimport) unsigned RemoveVectoredExceptionHandler(void*);
__declspec(dllimport) unsigned RemoveVectoredContinueHandler(void*);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
extern char resume_av142[],resume_ud142[];
static volatile unsigned order,handled,continued;
static int first(POINTERS*p){if(order!=0||*(unsigned*)(p->context+48)!=0x10000f)ExitProcess(71);order=1;return 0;}
static int second(POINTERS*p){(void)p;if(order!=1)ExitProcess(72);order=2;return 0;}
static int handle(POINTERS*p){if(order!=2)ExitProcess(73);order=3;
 if(p->record->code==0xc0000005u){if(p->record->count!=2||p->record->args[0]!=1||p->record->args[1]!=1||*(U*)(p->context+120)!=1)ExitProcess(74);*(U*)(p->context+248)=(U)resume_av142;}
 else if(p->record->code==0xc000001du){if(p->record->count)ExitProcess(75);*(U*)(p->context+248)=(U)resume_ud142;}else ExitProcess(76);

#ifdef INVALID_MXCSR142
 *(unsigned*)(p->context+52)=0xffffffffu;
#endif
#ifdef INVALID_RIP142
 *(U*)(p->context+248)=0xffff800000000000ull;
#endif
 ++handled;return -1;
}
static int continuation(POINTERS*p){(void)p;if(order!=3)ExitProcess(77);order=4;++continued;return 0;}
void entry(void);void* volatile relocation_anchor=&entry;
void entry(void){
 void*a=AddVectoredExceptionHandler(0,second),*b=AddVectoredExceptionHandler(0,handle),*head=AddVectoredExceptionHandler(1,first),*c=AddVectoredContinueHandler(0,continuation);if(!a||!b||!head||!c)ExitProcess(78);
 for(unsigned i=0;i<24;++i){order=0;__asm__ volatile("movq $1, %%rax; .global resume_av142; movl $7,(%%rax); resume_av142:":::"rax","memory");if(order!=4)ExitProcess(79);order=0;__asm__ volatile(".global resume_ud142; ud2; resume_ud142:":::"memory");if(order!=4)ExitProcess(80);}
 if(handled!=48||continued!=48||!RemoveVectoredExceptionHandler(a)||RemoveVectoredExceptionHandler(a)||!RemoveVectoredExceptionHandler(b)||!RemoveVectoredExceptionHandler(head)||!RemoveVectoredContinueHandler(c))ExitProcess(81);
 for(unsigned i=0;i<128;++i){void*h=AddVectoredExceptionHandler(0,first);if(!h||!RemoveVectoredExceptionHandler(h)||RemoveVectoredExceptionHandler(h))ExitProcess(82);}
 static const char ok[]="M142_VECTORED_HARDWARE_FAULTS_RESUME_PASS\n";unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),ok,sizeof(ok)-1,&wrote,0);ExitProcess(0);
}
