/* Windows x64 loader fixture; never a substitute for an original application. */
typedef unsigned long long U;
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) U LoadLibraryA(const char*);
__declspec(dllimport) void* GetProcAddress(U,const char*);
__declspec(dllimport) int FreeLibrary(U);
__declspec(dllimport) int forwarded(void);
__declspec(dllimport) int forwardedOrdinal(void);
__declspec(dllimport) int delayed(void);
extern char __ImageBase;
void* __delayLoadHelper2(const unsigned*descriptor,void**slot){
    char*base=&__ImageBase;
    U*module=(U*)(base+descriptor[2]);
    if(!*module)*module=LoadLibraryA(base+descriptor[1]);
    if(!*module)ExitProcess(10);
    U*iat=(U*)(base+descriptor[3]);
    U*names=(U*)(base+descriptor[4]);
    U name=names[(U*)slot-iat];
    void*target=GetProcAddress(*module,name>>63?(const char*)(name&65535):base+name+2);
    if(!target)ExitProcess(11);
    *slot=target;return target;
}
static volatile unsigned char sparse[24*1024*1024];
void entry(void);
void* volatile relocation_anchor=&entry;
static void print(const char*p,unsigned n){unsigned wrote;WriteFile(GetStdHandle((unsigned)-11),p,n,&wrote,0);}
void entry(void){
    sparse[0]=19;sparse[sizeof(sparse)-1]=23;
    if(forwarded()!=42||forwardedOrdinal()!=42||sparse[0]+sparse[sizeof(sparse)-1]!=42)ExitProcess(7);
    for(unsigned i=0;i<48;++i){
        U first=LoadLibraryA("dynamic.dll"),second=LoadLibraryA("dynamic.dll");
        if(!first||first!=second)ExitProcess(8);
        int(*value)(void)=(int(*)(void))GetProcAddress(first,"value");
        if(!value||value()!=42||!FreeLibrary(first)||value()!=42||!FreeLibrary(second))ExitProcess(9);
    }
    static const char delay[]="M141_DELAY_CALL_BEGIN\n";
    print(delay,sizeof(delay)-1);
    if(delayed()!=42)ExitProcess(12);
    static const char ok[]="M141_SPARSE_FORWARD_REFERENCE_REUSE_PASS\n";
    print(ok,sizeof(ok)-1);ExitProcess(0);
}
