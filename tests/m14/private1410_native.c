/* Run unchanged in both app bundles. Only the backing DLL differs. */
#include <stdint.h>

typedef uint64_t H;
typedef uint16_t W;
__declspec(dllimport) H LoadLibraryW(const W *);
__declspec(dllimport) void *GetProcAddress(H,const char *);
__declspec(dllimport) int FreeLibrary(H);
__declspec(dllimport) unsigned GetModuleFileNameW(H,W *,unsigned);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) unsigned GetTempPathW(unsigned,W *);
__declspec(dllimport) H CreateFileW(const W *,unsigned,unsigned,void *,unsigned,unsigned,H);
__declspec(dllimport) int ReadFile(H,void *,unsigned,unsigned *,void *);
__declspec(dllimport) int WriteFile(H,const void *,unsigned,unsigned *,void *);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int CloseHandle(H);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) int RegCreateKeyExW(H,const W *,unsigned,W *,unsigned,unsigned,void *,H *,unsigned *);
__declspec(dllimport) int RegQueryValueExW(H,const W *,unsigned *,unsigned *,void *,unsigned *);
__declspec(dllimport) int RegSetValueExW(H,const W *,unsigned,unsigned,const void *,unsigned);
__declspec(dllimport) int RegCloseKey(H);

static void require(int condition,unsigned error){
 if(!condition)ExitProcess(error);
}

static const char a[]="M1410_PRIVATE_APP_A_PASS\n",b[]="M1410_PRIVATE_APP_B_PASS\n";
static const char *volatile messages[]={a,b};

void entry(void){
 H named=LoadLibraryW(L"bundle-test.dll");
 H explicit=LoadLibraryW(L"C:\\Windows\\System32\\bundle-test.dll");
 require(named&&explicit==named,61);
 static const W logical[]=L"C:\\Windows\\System32\\bundle-test.dll";
 W module_name[260];
 unsigned chars=GetModuleFileNameW(named,module_name,260);
 require(chars+1==sizeof(logical)/sizeof(*logical),76);
 for(unsigned i=0;i<=chars;++i)require(module_name[i]==logical[i],77);
 require(!LoadLibraryW(L"C:\\Users\\Owner\\Downloads\\bundle-test.dll")&&GetLastError()==126,78);
 unsigned (*identify)(void)=(unsigned (*)(void))GetProcAddress(named,"BundleIdentity");
 require(identify!=0,62);
 unsigned identity=identify();
 require(identity==0x41||identity==0x42,63);
 require(FreeLibrary(explicit)&&FreeLibrary(named),64);

 H key=0;
 unsigned disposition=0;
 require(!RegCreateKeyExW(UINT64_C(0xffffffff80000001),L"Software\\EngacerBundleIsolation",0,0,0,3,0,&key,&disposition),65);
 if(disposition==1){
  require(!RegSetValueExW(key,L"Marker",0,4,&identity,sizeof(identity)),66);
 }else{
  unsigned value=0,bytes=sizeof(value),type=0;
  require(disposition==2&&!RegQueryValueExW(key,L"Marker",0,&type,&value,&bytes)&&
          type==4&&bytes==sizeof(value)&&value==identity,67);
 }
 require(!RegCloseKey(key),68);

 W temp[260];
 static const W leaf[]=L"bundle-test.bin";
 unsigned n=GetTempPathW(260,temp);
 require(n&&n+sizeof(leaf)/sizeof(*leaf)<=260,69);
 for(unsigned i=0;i<sizeof(leaf)/sizeof(*leaf);++i)temp[n+i]=leaf[i];
 H file=CreateFileW(temp,0xc0000000u,0,0,4,128,0);
 require(file!=UINT64_MAX,70);
 unsigned value=0,bytes=0;
 require(ReadFile(file,&value,sizeof(value),&bytes,0),71);
 if(bytes)require(bytes==sizeof(value)&&value==identity,72);
 else require(WriteFile(file,&identity,sizeof(identity),&bytes,0)&&bytes==sizeof(identity),73);
 require(CloseHandle(file),74);

 require(WriteFile(GetStdHandle((unsigned)-11),messages[identity-0x41],sizeof(a)-1,&bytes,0),75);
 ExitProcess(0);
}
