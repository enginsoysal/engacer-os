/* Synthetic Windows PE path probe; runs only inside an owned guest. */
typedef unsigned long long U;
typedef unsigned short W;
__declspec(dllimport) unsigned GetFullPathNameW(const W*,unsigned,W*,W**);
__declspec(dllimport) unsigned GetFullPathNameA(const char*,unsigned,char*,char**);
__declspec(dllimport) unsigned GetCurrentDirectoryW(unsigned,W*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static void check(int ok,unsigned code){if(!ok)ExitProcess(code);}
static unsigned length(const W*s){unsigned n=0;while(s[n])++n;return n;}
static int equal(const W*a,const W*b){unsigned i=0;while(a[i]&&a[i]==b[i])++i;return a[i]==b[i];}
void entry(void);
void* volatile relocation_anchor=&entry;
void entry(void){
 W cwd[512],out[512],expected[512],*leaf=0;unsigned n=GetCurrentDirectoryW(512,cwd);
 check(n&&n<500,10);for(unsigned i=0;i<n;++i)expected[i]=cwd[i];
 static const W name[]={'.','\\','p','a','t','h','-','r',0xe9,'s','u','m',0xe9,'-',0xd83d,0xde42,'.','t','x','t',0};
 unsigned at=n;expected[at++]='\\';for(unsigned i=2;name[i];++i)expected[at++]=name[i];expected[at]=0;
 check(GetFullPathNameW(name,512,out,&leaf)==at&&equal(out,expected)&&leaf==out+n+1,11);
 W guard[2]={0x1234,0x5678};check(GetFullPathNameW(name,1,guard,&leaf)==at+1&&guard[0]==0x1234&&guard[1]==0x5678&&leaf==0,12);
 check(GetFullPathNameW(name,0,0,0)==at+1,13);
 static const W dots[]={'C',':','\\','W','i','n','d','o','w','s','\\','.','.','\\','D','a','t','a','\\','f','i','l','e',0};
 static const W normalized[]={'C',':','\\','D','a','t','a','\\','f','i','l','e',0};
 check(GetFullPathNameW(dots,512,out,0)==length(normalized)&&equal(out,normalized),14);
 W malformed[]={0xd800,0};check(!GetFullPathNameW(malformed,512,out,0)&&GetLastError()==1113,15);
 check(!GetFullPathNameW((const W*)(U)1,512,out,0)&&GetLastError()==998,16);
 char narrow[512],*part=0;unsigned bytes=GetFullPathNameA(".\\path-\xc3\xa9.txt",512,narrow,&part);
 check(bytes&&part&&part[0]=='p'&&part[5]==(char)0xc3&&part[6]==(char)0xa9,17);
 static const char pass[]="M143_NATIVE_PATH_BOUNDARY_PASS\n";unsigned wrote=0;
 check(WriteFile(GetStdHandle((unsigned)-11),pass,sizeof(pass)-1,&wrote,0)&&wrote==sizeof(pass)-1,18);
 ExitProcess(0);
}
