/* Measure managed allocation overhead, not application or CPU performance. */
typedef unsigned long long H;
typedef unsigned long long Q;
typedef struct {unsigned length,load;Q total,available,page_total,page_available,virtual_total,virtual_available,extended;} MEMORY;
__declspec(dllimport) H GetProcessHeap(void);
__declspec(dllimport) void*HeapAlloc(H,unsigned,Q);
__declspec(dllimport) Q HeapSize(H,unsigned,const void*);
__declspec(dllimport) int HeapFree(H,unsigned,void*);
__declspec(dllimport) int GlobalMemoryStatusEx(MEMORY*);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static const char*volatile relocation="heap";
static void*pointers[1000];
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void number(Q value){char text[32],reverse[32];unsigned n=0,k=0;do{reverse[n++]=(char)('0'+value%10);value/=10;}while(value);while(n)text[k++]=reverse[--n];text[k]=0;say(text);}
void entry(void){if(relocation[0]!='h')ExitProcess(1);MEMORY before={0},after={0};before.length=after.length=64;H heap=GetProcessHeap();if(!GlobalMemoryStatusEx(&before))ExitProcess(2);
 for(unsigned i=0;i<1000;++i){unsigned char*p=HeapAlloc(heap,0,16);if(!p)ExitProcess(3);for(unsigned j=0;j<16;++j)p[j]=(unsigned char)i;pointers[i]=p;}
 if(!GlobalMemoryStatusEx(&after))ExitProcess(4);Q bytes=before.available-after.available;say("HEAP144_DELTA_BYTES=");number(bytes);say("\nHEAP144_ALLOC_SIZE=");number(HeapSize(heap,0,pointers[0]));say("\n");
 for(unsigned i=0;i<1000;++i){unsigned char*p=pointers[i];for(unsigned j=0;j<16;++j)if(p[j]!=(unsigned char)i)ExitProcess(5);if(!HeapFree(heap,0,p))ExitProcess(6);}
 say("M144_HEAP_OVERHEAD_PASS\n");ExitProcess(0);
}
