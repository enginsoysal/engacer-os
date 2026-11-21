/* Own native codec caller with separately generated independent expected data. */
#include <stdint.h>
#include <stddef.h>
#include "codepage147_expected.h"
__declspec(dllimport) unsigned GetACP(void);
__declspec(dllimport) unsigned GetOEMCP(void);
__declspec(dllimport) int IsValidCodePage(unsigned);
__declspec(dllimport) int GetCPInfo(unsigned,void*);
__declspec(dllimport) int MultiByteToWideChar(unsigned,unsigned,const char*,int,uint16_t*,int);
__declspec(dllimport) int WideCharToMultiByte(unsigned,unsigned,const uint16_t*,int,char*,int,const char*,int*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
void entry(void);void*volatile anchor147=&entry;
void entry(void){
 check147(GetACP()==65001&&GetOEMCP()==65001&&IsValidCodePage(65001)&&IsValidCodePage(1252)&&!IsValidCodePage(932),10);
 for(unsigned cp=0;cp<2;++cp){unsigned char info[36];for(unsigned i=0;i<36;++i)info[i]=0x9b;check147(GetCPInfo(cp?1252:65001,info),11);check147(*(unsigned*)info==(cp?1u:4u)&&info[4]=='?'&&info[5]==0,12);for(unsigned i=6;i<20;++i)check147(info[i]==0,13);for(unsigned i=20;i<36;++i)check147(info[i]==0x9b,14);}
 unsigned char info[20];check147(!GetCPInfo(932,info)&&GetLastError()==87,15);
 for(unsigned i=0;i<256;++i){
  char source=(char)i,encoded[2]={(char)0x9b,(char)0x9b};uint16_t wide[2]={0x9b9b,0x9b9b};check147(MultiByteToWideChar(1252,0,&source,1,wide,1)==1&&wide[0]==expected1252_147[i]&&wide[1]==0x9b9b,20);
  int used=99;check147(WideCharToMultiByte(1252,0,wide,1,0,0,0,&used)==1&&!used,21);check147(WideCharToMultiByte(1252,0,wide,1,encoded,1,0,&used)==1&&(unsigned char)encoded[0]==i&&!used&&(unsigned char)encoded[1]==0x9b,22);
 }
 static const char utf8[]={ (char)0xe2,(char)0x82,(char)0xac,(char)0xf0,(char)0x9f,(char)0x98,(char)0x80,0};uint16_t wide[8]={0};check147(MultiByteToWideChar(65001,8,utf8,-1,wide,8)==4&&wide[0]==0x20ac&&wide[1]==0xd83d&&wide[2]==0xde00&&!wide[3],30);char output[9]={0};check147(WideCharToMultiByte(65001,0,wide,-1,output,8,0,0)==8,31);for(unsigned i=0;i<8;++i)check147(output[i]==utf8[i],32);
 static const char bad[]={(char)0xf9,(char)0x80,(char)0x80,(char)0x80};check147(!MultiByteToWideChar(65001,8,bad,4,wide,8)&&GetLastError()==1113,33);
 uint16_t missing[]={0x4e00};int used=0;check147(WideCharToMultiByte(1252,0x400,missing,1,0,0,"!",&used)==1&&used,34);check147(WideCharToMultiByte(1252,0x400,missing,1,output,1,"!",&used)==1&&used&&output[0]=='!',35);
 static const char text[]="M147_NATIVE_CODEPAGE_UTF8_CP1252_REFERENCE_PASS\n";unsigned n=0;check147(WriteFile(GetStdHandle((unsigned)-11),text,sizeof(text)-1,&n,0)&&n==sizeof(text)-1,40);ExitProcess(0);
}
