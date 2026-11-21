/* Owned caller of the production native MSI DLL; no host execution. */
#include <stdint.h>
#include <stddef.h>
__declspec(dllimport) unsigned MsiCreateRecord(unsigned);
__declspec(dllimport) unsigned MsiCloseHandle(unsigned);
__declspec(dllimport) unsigned MsiGetActiveDatabase(unsigned);
__declspec(dllimport) unsigned MsiRecordSetStringW(unsigned,unsigned,const uint16_t*);
__declspec(dllimport) unsigned MsiRecordGetStringW(unsigned,unsigned,uint16_t*,unsigned*);
__declspec(dllimport) unsigned MsiRecordSetInteger(unsigned,unsigned,int32_t);
__declspec(dllimport) int32_t MsiRecordGetInteger(unsigned,unsigned);
__declspec(dllimport) unsigned MsiRecordGetFieldCount(unsigned);
__declspec(dllimport) unsigned MsiRecordDataSize(unsigned,unsigned);
__declspec(dllimport) int MsiRecordIsNull(unsigned,unsigned);
__declspec(dllimport) unsigned MsiRecordClearData(unsigned);
__declspec(dllimport) unsigned MsiFormatRecordW(unsigned,unsigned,uint16_t*,unsigned*);
__declspec(dllimport) uint64_t CreateThread(void*,size_t,void*,void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const uint64_t*,int,unsigned);
__declspec(dllimport) int GetExitCodeThread(uint64_t,unsigned*);
__declspec(dllimport) int CloseHandle(uint64_t);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
static const uint16_t text147[]={'E','u','r','o',' ',0x20ac,' ',0xd83d,0xde00,0};
static unsigned worker147(void*opaque){unsigned id=(unsigned)(uintptr_t)opaque;for(unsigned i=0;i<100;++i){unsigned h=MsiCreateRecord(2);check147(h&&MsiRecordGetFieldCount(h)==2,10);check147(!MsiRecordSetInteger(h,1,(int32_t)(id*100+i))&&MsiRecordGetInteger(h,1)==(int32_t)(id*100+i),11);check147(!MsiRecordSetStringW(h,0,text147)&&MsiRecordDataSize(h,0)==9,12);uint16_t out[12];unsigned cap=12;check147(!MsiRecordGetStringW(h,0,out,&cap)&&cap==9,13);for(unsigned n=0;n<10;++n)check147(out[n]==text147[n],14);check147(!MsiCloseHandle(h)&&MsiCloseHandle(h)==6,15);}return 0;}
void entry(void);void*volatile anchor147=&entry;
void entry(void){
 check147(!MsiGetActiveDatabase(0)&&!MsiGetActiveDatabase(0x14700001),51);
 unsigned records[64];for(unsigned i=0;i<64;++i){records[i]=MsiCreateRecord(0);check147(records[i]!=0,20);}check147(!MsiCreateRecord(0)&&!MsiCreateRecord(33),21);for(unsigned i=0;i<64;++i)check147(!MsiCloseHandle(records[i]),22);
 unsigned h=MsiCreateRecord(1);check147(h&&MsiRecordIsNull(h,0),23);check147(!MsiRecordSetStringW(h,0,text147),24);uint16_t out[12];for(unsigned i=0;i<12;++i)out[i]=0x9b9b;unsigned cap=8;check147(MsiRecordGetStringW(h,0,out,&cap)==234&&cap==9&&out[7]==0&&out[8]==0x9b9b,25);cap=9;check147(MsiRecordGetStringW(h,0,out,&cap)==234&&out[7]==0&&out[9]==0x9b9b,26);
 uint16_t invalid[]={0xd800,0};check147(MsiRecordSetStringW(h,0,invalid)==1113,27);cap=12;check147(!MsiRecordGetStringW(h,0,out,&cap)&&out[7]==0xd83d&&out[8]==0xde00,28);check147(!MsiRecordClearData(h)&&MsiRecordIsNull(h,0)&&!MsiCloseHandle(h),29);
 h=MsiCreateRecord(1);check147(h&&!MsiRecordSetStringW(h,0,L"Number=[1] [Missing]")&&!MsiRecordSetInteger(h,1,42),41);uint16_t formatted[64];cap=64;check147(!MsiFormatRecordW(0,h,formatted,&cap)&&cap==10,42);static const uint16_t expected[]=L"Number=42 ";for(unsigned i=0;i<11;++i)check147(formatted[i]==expected[i],43);check147(!MsiCloseHandle(h),44);
 uint64_t threads[4];for(unsigned i=0;i<4;++i){threads[i]=CreateThread(0,0,(void*)worker147,(void*)(uintptr_t)i,0,0);check147(threads[i]!=0,30);}check147(WaitForMultipleObjects(4,threads,1,30000)==0,31);for(unsigned i=0;i<4;++i){unsigned code=259;check147(GetExitCodeThread(threads[i],&code)&&code==0&&CloseHandle(threads[i]),32);}
 static const char pass[]="M147_NATIVE_MSI_EXPORT_RECORD_UNICODE_THREADS_PASS\n";unsigned written=0;check147(WriteFile(GetStdHandle((unsigned)-11),pass,sizeof(pass)-1,&written,0)&&written==sizeof(pass)-1,40);ExitProcess(0);
}
