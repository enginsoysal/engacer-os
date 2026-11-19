/* Actual compiler-generated Win64 static TLS; executed only inside Engacer OS. */
typedef unsigned long long U;
typedef void (*CALLBACK)(void*,unsigned,void*);
__declspec(dllimport) U CreateThread(void*,U,void*,void*,unsigned,unsigned*);
__declspec(dllimport) unsigned ResumeThread(U);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) void ExitThread(unsigned);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) U LoadLibraryA(const char*);
__declspec(dllimport) void* GetProcAddress(U,const char*);
__declspec(dllimport) int FreeLibrary(U);
unsigned _tls_index;
#pragma section(".tls",read,write)
#pragma section(".tls$ZZZ",read,write)
__declspec(allocate(".tls")) char _tls_start;
__declspec(thread) static volatile unsigned local=17;
__declspec(thread) static volatile unsigned zero;
__declspec(allocate(".tls$ZZZ")) char _tls_end;
static volatile unsigned attached,detached,process_attached;
static void print(const char*s,unsigned n){unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),s,n,&wrote,0);}
static volatile unsigned char*tail(void){U vector;__asm__ volatile("movq %%gs:0x58,%0":"=r"(vector));return (volatile unsigned char*)((U*)vector)[_tls_index]+((U)&_tls_end-(U)&_tls_start);}
static void callback(void*base,unsigned reason,void*reserved){
 (void)base;
 if(reason==1||reason==2)for(unsigned i=0;i<16;++i)if(tail()[i])ExitProcess(74);
 if(reason==1){if(local!=17||zero)ExitProcess(61);++process_attached;}
 if(reason==2){if(local!=17||zero)ExitProcess(62);__atomic_add_fetch(&attached,1,__ATOMIC_SEQ_CST);}
 if(reason==3){
#ifndef TLS_DLL142
  #ifdef TLS_LAST142
  if(local!=42||tail()[0]!=99)ExitProcess(75);static const char main_end[]="M142_TLS_MAIN_THREAD_EXIT_PASS\n";print(main_end,sizeof(main_end)-1);
#else
  if(local<100||local>103||tail()[0]!=local-99)ExitProcess(75);
#endif
#endif
  __atomic_add_fetch(&detached,1,__ATOMIC_SEQ_CST);
 }
 if(reason==0){
#ifdef TLS_DLL142
  static const char normal[]="M142_TLS_DLL_PROCESS_END\n",unload[]="M142_TLS_DLL_FREE\n";print(reserved?normal:unload,reserved?sizeof(normal)-1:sizeof(unload)-1);
#else
  #ifdef TLS_LAST142
  if(local!=100||tail()[0]!=1||!reserved)ExitProcess(63);static const char end[]="M142_TLS_LAST_THREAD_PROCESS_DETACH_PASS\n";
#else
  if(local!=42||tail()[0]!=99||!reserved)ExitProcess(63);static const char end[]="M142_TLS_PROCESS_DETACH_PASS\n";
#endif
  print(end,sizeof(end)-1);
#endif
 }
}
static CALLBACK callbacks[]={callback,0};
struct TLS {void*start,*end;unsigned*index;CALLBACK*callbacks;unsigned zero,flags;};
const struct TLS _tls_used={&_tls_start,&_tls_end,&_tls_index,callbacks,16,0};
#ifdef TLS_DLL142
__declspec(dllexport) unsigned swap(unsigned value){unsigned previous=local;local=value;return previous;}
#else
__declspec(dllimport) unsigned swap(unsigned);
static unsigned worker(void*arg){unsigned n=(unsigned)(U)arg;U expected=0x1122334400000000ull+n,observed;unsigned mxcsr=0x1f80u|((n&3)<<13),actual_mxcsr;
 __asm__ volatile("movq %0,%%xmm6; ldmxcsr %1"::"r"(expected),"m"(mxcsr):"xmm6");if(local!=17||zero||swap(200+n)!=17)ExitProcess(64);local=100+n;zero=300+n;tail()[0]=(unsigned char)(n+1);for(unsigned i=0;i<20;++i){Sleep(10);__asm__ volatile("movq %%xmm6,%0; stmxcsr %1":"=r"(observed),"=m"(actual_mxcsr));if(observed!=expected||actual_mxcsr!=mxcsr)ExitProcess(76);if(local!=100+n||zero!=300+n)ExitProcess(65);}if(swap(400+n)!=200+n)ExitProcess(66);return n;}
void entry(void);
void* volatile relocation_anchor=&entry;
void entry(void){
 if(process_attached!=1||local!=17||zero||swap(75)!=17)ExitProcess(67);local=42;tail()[0]=99;
#ifdef TLS_LAST142
 if(!CreateThread(0,0,worker,0,0,0))ExitProcess(77);ExitThread(0);ExitProcess(78);
#endif
 U threads[4];for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,worker,(void*)(U)i,4,0);if(!threads[i])ExitProcess(68);}
 for(unsigned i=0;i<8;++i){U dll=LoadLibraryA("tlsdynamic.dll");if(!dll)ExitProcess(69);unsigned(*fn)(unsigned)=(unsigned(*)(unsigned))GetProcAddress(dll,"swap");if(!fn||fn(77)!=17||fn(88)!=77||!FreeLibrary(dll))ExitProcess(70);}
 for(unsigned i=0;i<4;++i)if(ResumeThread(threads[i])!=1)ExitProcess(71);
 if(WaitForMultipleObjects(4,threads,1,5000)!=0||attached!=4||detached!=4||local!=42||zero||swap(85)!=75)ExitProcess(72);
 for(unsigned i=0;i<4;++i)if(!CloseHandle(threads[i]))ExitProcess(73);
 static const char ok[]="M142_STATIC_TLS_TEMPLATE_THREADS_DLL_PASS\n";print(ok,sizeof(ok)-1);ExitProcess(0);
}
#endif
