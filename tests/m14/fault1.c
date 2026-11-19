/* Actual CPL3 protection probes, compiled as synthetic Windows PE files. */
__declspec(dllimport) void ExitProcess(unsigned);
extern char __ImageBase;
void entry(void);
void* volatile relocation_anchor=&entry;
static volatile unsigned char writable_code[]={0xc3};
static const volatile unsigned char readonly_data[4096]={7};
void entry(void){
#if FAULT141 == 1
    ((void(*)(void))(void*)writable_code)();
#elif FAULT141 == 2
    *(volatile unsigned char*)(void*)readonly_data=9;
#else
    volatile unsigned char*base=(volatile unsigned char*)&__ImageBase;
    unsigned pe=*(const unsigned*)(base+60);
    unsigned size=*(const unsigned*)(base+pe+24+56);
    base[(size+65535u)&~65535u]=1;
#endif
    ExitProcess(77);
}
