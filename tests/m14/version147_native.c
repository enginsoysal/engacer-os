/* Own Win64 caller checks actual version bytes from the unchanged WiX file. */
#include <stdint.h>
#include <stddef.h>
__declspec(dllimport) unsigned GetFileVersionInfoSizeW(const uint16_t*,unsigned*);
__declspec(dllimport) int GetFileVersionInfoW(const uint16_t*,unsigned,unsigned,void*);
__declspec(dllimport) int VerQueryValueW(const void*,const uint16_t*,void**,unsigned*);
__declspec(dllimport) void*GetProcessHeap(void);
__declspec(dllimport) void*HeapAlloc(void*,unsigned,size_t);
__declspec(dllimport) int HeapFree(void*,unsigned,void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
void entry(void);void*volatile anchor147=&entry;
static void check147(int value,unsigned code){if(!value)ExitProcess(code);}
void entry(void){
 unsigned handle=99,n=GetFileVersionInfoSizeW(L"C:\\Program Files\\7-Zip\\wix147.dll",&handle);check147(n==816&&handle==0,101);uint8_t*data=HeapAlloc(GetProcessHeap(),0,n+16);check147(data!=0,102);for(unsigned i=0;i<n+16;++i)data[i]=0x9b;
 check147(GetFileVersionInfoW(L"C:\\Program Files\\7-Zip\\wix147.dll",0,n,data),103);for(unsigned i=n;i<n+16;++i)check147(data[i]==0x9b,104);
 void*value=0;unsigned bytes=0;check147(VerQueryValueW(data,L"\\",&value,&bytes)&&bytes==52,105);uint32_t*fixed=value;check147(fixed[0]==0xfeef04bdu&&fixed[1]==0x10000u&&fixed[2]==0x60000u&&fixed[3]==0x20000u,106);
 check147(VerQueryValueW(data,L"\\VarFileInfo\\Translation",&value,&bytes)&&bytes==4&&*(uint32_t*)value==0x409u,107);
 check147(VerQueryValueW(data,L"\\StringFileInfo\\04090000\\FileVersion",&value,&bytes)&&bytes==8,108);const uint16_t*text=value;const uint16_t expected[]=L"6.0.2.0";for(unsigned i=0;i<8;++i)check147(text[i]==expected[i],109);
 value=(void*)(uintptr_t)99;bytes=99;check147(!VerQueryValueW(data,L"\\Missing",&value,&bytes)&&!value&&!bytes,110);
 uint8_t first=data[0];for(unsigned i=0;i<16;++i)data[i]=0x9b;check147(GetFileVersionInfoW(L"C:\\Program Files\\7-Zip\\wix147.dll",0,1,data)&&data[0]==first,111);for(unsigned i=1;i<16;++i)check147(data[i]==0x9b,112);
 check147(HeapFree(GetProcessHeap(),0,data),113);handle=99;check147(!GetFileVersionInfoSizeW(L"C:\\Program Files\\7-Zip\\missing147.dll",&handle)&&handle==0&&GetLastError()==2,114);
 static const char output[]="M147_NATIVE_ORIGINAL_VERSION_RESOURCE_BYTES_PASS\n";unsigned done=0;check147(WriteFile(GetStdHandle((unsigned)-11),output,sizeof(output)-1,&done,0)&&done==sizeof(output)-1,115);ExitProcess(0);
}
