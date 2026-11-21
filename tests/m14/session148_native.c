/* Owned native callers; unchanged original installers are tested separately. */
#include <stdint.h>
#include <engine/windows8.h>
void*memset(void*pointer,int value,size_t bytes){volatile uint8_t*out=pointer;for(size_t i=0;i<bytes;++i)out[i]=(uint8_t)value;return pointer;}
__declspec(dllimport) unsigned RegisterWindowMessageW(const uint16_t*);
__declspec(dllimport) unsigned RegisterWindowMessageA(const char*);
__declspec(dllimport) unsigned short GlobalAddAtomW(const uint16_t*);
__declspec(dllimport) unsigned short GlobalDeleteAtom(unsigned short);
__declspec(dllimport) const uint16_t*GetCommandLineW(void);
__declspec(dllimport) unsigned GetModuleFileNameW(uint64_t,uint16_t*,unsigned);
__declspec(dllimport) unsigned GetLongPathNameW(const uint16_t*,uint16_t*,unsigned);
__declspec(dllimport) unsigned GetShortPathNameW(const uint16_t*,uint16_t*,unsigned);
__declspec(dllimport) int GetFileAttributesExW(const uint16_t*,unsigned,void*);
__declspec(dllimport) uint64_t CreateFileW(const uint16_t*,unsigned,unsigned,void*,unsigned,unsigned,uint64_t);
__declspec(dllimport) int GetFileSizeEx(uint64_t,int64_t*);
__declspec(dllimport) int CreateProcessW(const uint16_t*,uint16_t*,void*,void*,int,unsigned,void*,const uint16_t*,void*,void*);
__declspec(dllimport) unsigned WaitForSingleObject(uint64_t,unsigned);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const uint64_t*,int,unsigned);
__declspec(dllimport) int GetExitCodeProcess(uint64_t,unsigned*);
__declspec(dllimport) uint64_t CreateThread(void*,uint64_t,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) int CloseHandle(uint64_t);
__declspec(dllimport) void InitializeSRWLock(uint64_t*);
__declspec(dllimport) void AcquireSRWLockExclusive(uint64_t*);
__declspec(dllimport) void AcquireSRWLockShared(uint64_t*);
__declspec(dllimport) void ReleaseSRWLockExclusive(uint64_t*);
__declspec(dllimport) void ReleaseSRWLockShared(uint64_t*);
__declspec(dllimport) uint8_t TryAcquireSRWLockExclusive(uint64_t*);
__declspec(dllimport) uint8_t TryAcquireSRWLockShared(uint64_t*);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) uint64_t LoadLibraryExA(const char*,uint64_t,unsigned);
__declspec(dllimport) uint64_t GetModuleHandleW(const uint16_t*);
__declspec(dllimport) int FreeLibrary(uint64_t);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) int MulDiv(int,int,int);
__declspec(dllimport) void SetLastError(unsigned);
__declspec(dllimport) uint16_t GetUserDefaultUILanguage(void);
__declspec(dllimport) uint16_t GetSystemDefaultUILanguage(void);
__declspec(dllimport) void*GetProcAddress(uint64_t,const char*);
__declspec(dllimport) unsigned GetSystemDirectoryW(uint16_t*,unsigned);
__declspec(dllimport) uint64_t HeapCreate(unsigned,uint64_t,uint64_t);
__declspec(dllimport) int HeapDestroy(uint64_t);
__declspec(dllimport) void*HeapAlloc(uint64_t,unsigned,uint64_t);
__declspec(dllimport) int HeapFree(uint64_t,unsigned,void*);
__declspec(dllimport) uint64_t HeapSize(uint64_t,unsigned,const void*);
__declspec(dllimport) void*HeapReAlloc(uint64_t,unsigned,void*,uint64_t);
__declspec(dllimport) unsigned SetErrorMode(unsigned);
__declspec(dllimport) unsigned GetErrorMode(void);
__declspec(dllimport) unsigned GetFileAttributesW(const uint16_t*);
__declspec(dllimport) int RemoveDirectoryW(const uint16_t*);
__declspec(dllimport) void*LocalFree(void*);
__declspec(dllimport) uint64_t CreateToolhelp32Snapshot(unsigned,unsigned);
__declspec(dllimport) int Process32FirstW(uint64_t,void*);
__declspec(dllimport) int Process32NextW(uint64_t,void*);
__declspec(dllimport) unsigned GetCurrentProcessId(void);
__declspec(dllimport) unsigned ResumeThread(uint64_t);
__declspec(dllimport) int PeekMessageW(void*,uint64_t,unsigned,unsigned,unsigned);
__declspec(dllimport) int PostMessageW(uint64_t,unsigned,uint64_t,int64_t);
__declspec(dllimport) unsigned RegisterClassExW(const void*);
__declspec(dllimport) int GetClassInfoExW(uint64_t,const uint16_t*,void*);
__declspec(dllimport) int UnregisterClassW(const uint16_t*,uint64_t);
__declspec(dllimport) uint64_t CreateWindowExW(unsigned,const uint16_t*,const uint16_t*,unsigned,int,int,int,int,uint64_t,uint64_t,uint64_t,void*);
__declspec(dllimport) int DestroyWindow(uint64_t);
__declspec(dllimport) uint64_t GetDesktopWindow(void);
__declspec(dllimport) uint64_t GetParent(uint64_t);
__declspec(dllimport) int IsWindow(uint64_t);
__declspec(dllimport) int GetWindowRect(uint64_t,void*);
__declspec(dllimport) int GetClientRect(uint64_t,void*);
__declspec(dllimport) int GetSystemMetrics(int);
__declspec(dllimport) uint64_t GetDC(uint64_t);
__declspec(dllimport) int ReleaseDC(uint64_t,uint64_t);
__declspec(dllimport) int GetDeviceCaps(uint64_t,int);
__declspec(dllimport) uint64_t CreateFontIndirectW(const void*);
__declspec(dllimport) uint64_t GetStockObject(int);
__declspec(dllimport) uint64_t SelectObject(uint64_t,uint64_t);
__declspec(dllimport) uint64_t GetCurrentObject(uint64_t,unsigned);
__declspec(dllimport) int GetObjectW(uint64_t,int,void*);
__declspec(dllimport) int GetTextMetricsW(uint64_t,void*);
__declspec(dllimport) int GetTextFaceW(uint64_t,int,uint16_t*);
__declspec(dllimport) int GetTextExtentPoint32W(uint64_t,const uint16_t*,int,void*);
__declspec(dllimport) int DeleteObject(uint64_t);

__declspec(dllimport) int GetWindowLongW(uint64_t,int);
__declspec(dllimport) int64_t GetWindowLongPtrW(uint64_t,int);
__declspec(dllimport) int64_t SetWindowLongPtrW(uint64_t,int,int64_t);
__declspec(dllimport) int AdjustWindowRectEx(void*,unsigned,int,unsigned);
__declspec(dllimport) int AdjustWindowRect(void*,unsigned,int);
__declspec(dllimport) int SetWindowPos(uint64_t,uint64_t,int,int,int,int,unsigned);
__declspec(dllimport) int64_t DefWindowProcW(uint64_t,unsigned,uint64_t,int64_t);
__declspec(dllimport) int64_t SendMessageW(uint64_t,unsigned,uint64_t,int64_t);
typedef struct{uint64_t window,after;int x,y,width,height;unsigned flags,pad;} native_position148;
_Static_assert(sizeof(native_position148)==40,"Owned WINDOWPOS ABI");
static unsigned class_created148,class_destroyed148,class_pre148,class_post148,class_moves148,class_sizes148;static uint32_t class_move148,class_size148;static int class_delta148;
static int64_t class_proc148(uint64_t window,unsigned message,uint64_t wp,int64_t lp){if(message==1)++class_created148;if(message==0x82)++class_destroyed148;if(message==0x46){++class_pre148;if(class_delta148){((native_position148*)(uintptr_t)lp)->width+=class_delta148;class_delta148=0;}}if(message==0x47)++class_post148;if(message==3){++class_moves148;class_move148=(uint32_t)lp;}if(message==5){++class_sizes148;class_size148=(uint32_t)lp;}if(message>=0x8100&&message<=0x8104)return 10;return DefWindowProcW(window,message,wp,lp);}
static void check(int ok,unsigned error){if(!ok)ExitProcess(error);}
static void say148(const char*);
typedef int64_t(*native_subproc148)(uint64_t,unsigned,uint64_t,int64_t,uint64_t,uint64_t);
static int(*set_sub148)(uint64_t,native_subproc148,uint64_t,uint64_t);static int(*get_sub148)(uint64_t,native_subproc148,uint64_t,uint64_t*);static int(*remove_sub148)(uint64_t,native_subproc148,uint64_t);static int64_t(*def_sub148)(uint64_t,unsigned,uint64_t,int64_t);static uint64_t subclass_order148,subclass_data148;
static int64_t subclass_proc_test148(uint64_t h,unsigned message,uint64_t wp,int64_t lp,uint64_t id,uint64_t data){
 if(message==0x82){check(remove_sub148(h,subclass_proc_test148,id),440);return def_sub148(h,message,wp,lp);}
 if(message>=0x8100&&message<=0x8104){subclass_order148=subclass_order148*10+id;subclass_data148=data;
  if(id==2&&message==0x8101)check(remove_sub148(h,subclass_proc_test148,1),441);
  if(id==2&&message==0x8102)check(set_sub148(h,subclass_proc_test148,1,77),442);
  if(id==2&&message==0x8103)check(remove_sub148(h,subclass_proc_test148,2),443);
  if(message==0x8104)check(SendMessageW(h,0x8100,0,0)==110,444);
  return def_sub148(h,message,wp,lp)+(int64_t)id*100;
 }return def_sub148(h,message,wp,lp);
}
static void subclass_tests148(uint64_t h){
 uint64_t dll=LoadLibraryExA("comctl32.dll",0,0);check(dll!=0,445);set_sub148=GetProcAddress(dll,"SetWindowSubclass");get_sub148=GetProcAddress(dll,"GetWindowSubclass");remove_sub148=GetProcAddress(dll,"RemoveWindowSubclass");def_sub148=GetProcAddress(dll,"DefSubclassProc");check(set_sub148&&get_sub148&&remove_sub148&&def_sub148,446);check(GetProcAddress(dll,(const char*)410)==(void*)set_sub148&&GetProcAddress(dll,(const char*)413)==(void*)def_sub148,447);
 check(set_sub148(h,subclass_proc_test148,1,11)&&set_sub148(h,subclass_proc_test148,2,22),448);uint64_t data=99;for(unsigned i=0;i<500;++i)check(set_sub148(h,subclass_proc_test148,1,i),449);check(get_sub148(h,subclass_proc_test148,1,&data)&&data==499,450);
 subclass_order148=0;check(SendMessageW(h,0x8100,0,0)==310&&subclass_order148==21&&subclass_data148==499,451);
 subclass_order148=0;check(SendMessageW(h,0x8101,0,0)==210&&subclass_order148==2&&!get_sub148(h,subclass_proc_test148,1,&data),452);
 subclass_order148=0;check(SendMessageW(h,0x8102,0,0)==210&&subclass_order148==2&&get_sub148(h,subclass_proc_test148,1,&data)&&data==77,453);
 subclass_order148=0;check(SendMessageW(h,0x8103,0,0)==310&&subclass_order148==12&&!get_sub148(h,subclass_proc_test148,2,&data),454);
 subclass_order148=0;check(SendMessageW(h,0x8104,0,0)==110&&subclass_order148==11,455);
 check(remove_sub148(h,subclass_proc_test148,1)&&!remove_sub148(h,subclass_proc_test148,1)&&SendMessageW(h,0x8100,0,0)==10,456);
 for(unsigned i=0;i<16;++i)check(set_sub148(h,subclass_proc_test148,10+i,i),457);check(!set_sub148(h,subclass_proc_test148,99,0)&&GetLastError()==1816,458);for(unsigned i=0;i<16;++i)check(remove_sub148(h,subclass_proc_test148,10+i),459);
 check(set_sub148(h,subclass_proc_test148,1,0)&&FreeLibrary(dll),460);say148("M148_NATIVE_SUBCLASS_CHAIN_MUTATION_PASS\n");
}
typedef struct {int height,width,escapement,orientation,weight;uint8_t italic,underline,strike,charset,out_precision,clip_precision,quality,pitch;uint16_t face[32];} native_logfont148;
typedef struct {int height,ascent,descent,internal,external,average,maximum,weight,overhang,aspect_x,aspect_y;uint16_t first,last,default_char,break_char;uint8_t italic,underline,strike,pitch,charset,pad[3];} native_textmetric148;
_Static_assert(sizeof(native_logfont148)==92&&sizeof(native_textmetric148)==60,"Owned Windows font records");
static int64_t subclass_auto148(uint64_t h,unsigned m,uint64_t wp,int64_t lp,uint64_t id,uint64_t data){(void)id;(void)data;return def_sub148(h,m,wp,lp);}
static void subclass_cleanup148(unsigned atom){for(unsigned turn=0;turn<10;++turn){uint64_t h=CreateWindowExW(0,(const uint16_t*)(uintptr_t)atom,L"Automatic callback cleanup",0,0,0,100,100,0,0,0,0);check(h!=0,461);for(unsigned i=0;i<16;++i)check(set_sub148(h,subclass_auto148,i,turn),462);check(DestroyWindow(h),463);}say148("M148_NATIVE_SUBCLASS_AUTOMATIC_CLEANUP_PASS\n");}
static void button_tests148(uint64_t parent){
 uint64_t button=CreateWindowExW(0,L"Button",L"Install now",0x40000000,0,0,120,30,parent,41,0,0);check(button!=0,464);uint64_t dc=GetDC(button);int text[2],ideal[2]={0,0};check(dc&&GetTextExtentPoint32W(dc,L"Install now",11,text)&&ReleaseDC(button,dc)&&SendMessageW(button,0x1601,0,(int64_t)(uintptr_t)ideal)&&ideal[0]>=text[0]+12&&ideal[1]>=text[1]+8,465);
 int natural=ideal[1];ideal[0]=80;ideal[1]=0;check(SendMessageW(button,0x1601,0,(int64_t)(uintptr_t)ideal)&&ideal[0]==80&&ideal[1]==natural,466);native_logfont148 lf={.height=-28,.weight=600};uint64_t font=CreateFontIndirectW(&lf);check(font!=0,467);SendMessageW(button,0x30,font,0);ideal[0]=0;check(SendMessageW(button,0x1601,0,(int64_t)(uintptr_t)ideal)&&ideal[1]>natural,468);
 ideal[0]=55;ideal[1]=66;check(!SendMessageW(button,0x1601,1,(int64_t)(uintptr_t)ideal)&&GetLastError()==87&&ideal[0]==55&&ideal[1]==66,469);check(!SendMessageW(button,0x1601,0,1)&&GetLastError()==998,470);check(DestroyWindow(button)&&DeleteObject(font),471);
 uint64_t checkbutton=CreateWindowExW(0,L"Button",L"Optional item",0x40000003,0,0,123,37,parent,42,0,0);ideal[0]=0;ideal[1]=0;check(checkbutton&&SendMessageW(checkbutton,0x1601,0,(int64_t)(uintptr_t)ideal)&&ideal[0]==123&&ideal[1]==37&&DestroyWindow(checkbutton),472);say148("M148_NATIVE_BUTTON_IDEAL_FONT_GEOMETRY_PASS\n");
}
static uint64_t lock,left,right;
static void(*shutdown_gp148)(uint64_t);
static unsigned gp_shutdown_worker148(void*token){shutdown_gp148((uint64_t)(uintptr_t)token);return 0;}
void entry(void);void*volatile relocation_anchor148=&entry;
static void say148(const char*text){unsigned n=0,written;while(text[n])++n;check(WriteFile(GetStdHandle((unsigned)-11),text,n,&written,0)&&written==n,264);}
static void number148(uint64_t value){char text[32],reverse[24];unsigned n=0,used=0;do{reverse[n++]=(char)('0'+value%10);value/=10;}while(value);while(n)text[used++]=reverse[--n];text[used]=0;say148(text);}
typedef struct {unsigned size,usage,pid,pad;uint64_t heap;unsigned module,threads,parent;int priority;unsigned flags;uint16_t name[260];unsigned tail;} process_entry_native148;
_Static_assert(sizeof(process_entry_native148)==568,"Native caller PROCESSENTRY32W size");
static void snapshot_check148(uint64_t snapshot,unsigned child,unsigned present){
 process_entry_native148 entry={0};check(!Process32FirstW(snapshot,&entry)&&GetLastError()==24,284);entry.size=567;check(!Process32FirstW(snapshot,&entry)&&GetLastError()==24,296);entry.size=600;check(!Process32FirstW(snapshot,&entry)&&GetLastError()==24,297);entry.size=sizeof(entry);
 unsigned count=0,own=0,found=0;check(Process32FirstW(snapshot,&entry),285);
 do{++count;check(!entry.usage&&!entry.heap&&!entry.module&&!entry.flags&&entry.threads==1&&entry.priority==8,286);
  const uint16_t expected[]=L"7zFM.exe";for(unsigned i=0;i<sizeof(expected)/2;++i)check(entry.name[i]==expected[i],287);
  if(entry.pid==GetCurrentProcessId())++own;if(entry.pid==child){++found;check(entry.parent==GetCurrentProcessId(),288);}
 }while(Process32NextW(snapshot,&entry));check(GetLastError()==18&&own==1&&found==present&&count==1+present,289);
}
static uint64_t owned_pages148(void){uint64_t values[4];register uint64_t r8 __asm__("r8")=0;register uint64_t r10 __asm__("r10")=0;uint64_t result=W8_SYS_VMINFO;__asm__ volatile("int $0x80":"+a"(result):"D"((uint64_t)(uintptr_t)values),"S"(UINT64_C(0)),"d"(UINT64_C(0)),"r"(r10),"r"(r8):"memory","rcx","r11");check(!result,260);return values[1];}
static int64_t security_profile148(uint64_t argument){register uint64_t r8 __asm__("r8")=0;register uint64_t r10 __asm__("r10")=0;uint64_t result=W8_SYS_SECURITY148;__asm__ volatile("int $0x80":"+a"(result):"D"(argument),"S"(UINT64_C(0)),"d"(UINT64_C(0)),"r"(r10),"r"(r8):"memory","rcx","r11");return(int64_t)result;}
static unsigned worker(void*kind){
 for(unsigned i=0;i<1000;++i){
  if((uintptr_t)kind<4){AcquireSRWLockExclusive(&lock);++left;right=left*3;ReleaseSRWLockExclusive(&lock);}
  else{AcquireSRWLockShared(&lock);check(right==left*3,241);ReleaseSRWLockShared(&lock);}
 }for(unsigned i=0;i<64;++i){uint64_t dc=GetDC(0);check(dc&&GetDeviceCaps(dc,88)==96&&ReleaseDC(0,dc),393);}return 0;
}
static void font_tests148(void){
 native_logfont148 lf={.height=-14,.weight=400},copy={0};lf.face[0]='S';lf.face[1]='e';lf.face[2]='g';
 uint64_t dc=GetDC(0),font=CreateFontIndirectW(&lf);check(dc&&font,420);uint64_t stock=GetCurrentObject(dc,6);check(stock==GetStockObject(13)&&SelectObject(dc,font)==stock&&GetCurrentObject(dc,6)==font,421);
 check(GetObjectW(font,0,0)==92&&GetObjectW(font,92,&copy)==92&&copy.height==-14&&copy.face[0]=='S',422);uint8_t fragment[4]={0,0,0,0xa5};check(GetObjectW(font,3,fragment)==3&&fragment[3]==0xa5&&fragment[0]==0xf2,423);
 native_textmetric148 small,big;uint16_t face[16];check(GetTextMetricsW(dc,&small)&&small.height>=14&&small.height==small.ascent+small.descent&&small.weight==400&&!small.italic&&small.pitch==0x21&&small.first==32&&small.last==0x20ac,424);
 check(GetTextFaceW(dc,0,0)==6&&GetTextFaceW(dc,16,face)==6&&face[0]=='I'&&face[4]=='r'&&!face[5],425);face[0]=99;check(GetTextFaceW(dc,1,face)==1&&!face[0],426);
 int narrow[2],wide[2];check(GetTextExtentPoint32W(dc,L"iii",3,narrow)&&GetTextExtentPoint32W(dc,L"WWW",3,wide)&&wide[0]>narrow[0]&&wide[1]==small.height,427);
 check(!DeleteObject(font)&&GetLastError()==170&&SelectObject(dc,stock)==font&&DeleteObject(font)&&!DeleteObject(font),428);
 lf.height=-28;lf.weight=700;font=CreateFontIndirectW(&lf);check(font&&SelectObject(dc,font)==stock&&GetTextMetricsW(dc,&big)&&big.height>small.height&&big.weight==600&&big.last==126,429);
 check(ReleaseDC(0,dc)&&DeleteObject(font),430);lf.height=-16;lf.weight=400;uint64_t fonts[64];for(unsigned i=0;i<64;++i){fonts[i]=CreateFontIndirectW(&lf);check(fonts[i]&&fonts[i]!=font,431);}check(!CreateFontIndirectW(&lf)&&GetLastError()==1816,432);for(unsigned i=0;i<64;++i)check(DeleteObject(fonts[i]),433);
 lf.italic=1;check(!CreateFontIndirectW(&lf)&&GetLastError()==50,434);lf.italic=0;lf.width=10;check(!CreateFontIndirectW(&lf)&&GetLastError()==50,435);check(!CreateFontIndirectW((void*)1)&&GetLastError()==998,436);check(!GetStockObject(10)&&GetLastError()==50,437);
 say148("M148_NATIVE_FONT_OBJECT_METRICS_LIFETIME_PASS\n");
}
void entry(void){
 font_tests148();
 check(security_profile148(0)==7&&security_profile148(1)==-87,386);
 uint64_t desktop=GetDesktopWindow();int desktop_rect[4],desktop_client[4];check(desktop&&IsWindow(desktop)&&!GetParent(desktop)&&GetWindowRect(desktop,desktop_rect)&&GetClientRect(desktop,desktop_client),388);for(unsigned i=0;i<4;++i)check(desktop_rect[i]==desktop_client[i],389);check(!desktop_rect[0]&&!desktop_rect[1]&&desktop_rect[2]==GetSystemMetrics(0)&&desktop_rect[3]==GetSystemMetrics(1)&&desktop_rect[2]>0&&desktop_rect[3]>0&&!DestroyWindow(desktop)&&GetLastError()==5&&IsWindow(desktop),390);
 uint64_t desktop_dc=GetDC(0);check(desktop_dc&&GetDeviceCaps(desktop_dc,8)==desktop_rect[2]&&GetDeviceCaps(desktop_dc,10)==desktop_rect[3]&&GetDeviceCaps(desktop_dc,12)==32&&GetDeviceCaps(desktop_dc,14)==1&&GetDeviceCaps(desktop_dc,24)==-1&&GetDeviceCaps(desktop_dc,88)==96&&GetDeviceCaps(desktop_dc,90)==96&&ReleaseDC(0,desktop_dc),391);check(!GetDeviceCaps(desktop_dc,88)&&GetLastError()==6,392);
 const uint16_t*line=GetCommandLineW();unsigned child=0;
 for(unsigned i=0;line&&line[i];++i)if(line[i]==' '&&(line[i+1]=='!'||line[i+1]=='?')&&!line[i+2])child=line[i+1]=='!'?1:2;
 if(child){check(GetErrorMode()==(child==1?0x8001u:0u),261);check(RegisterWindowMessageW(L"Engacer.Message148.ChildFirst")>=0xc000,221);ExitProcess(RegisterWindowMessageW(L"Engacer.Message148.Parent"));}
 check(!GetErrorMode()&&!SetErrorMode(4)&&!GetErrorMode()&&!SetErrorMode(0x8001)&&GetErrorMode()==0x8001,262);
 SetLastError(0x148);check(GetUserDefaultUILanguage()==0x409&&GetSystemDefaultUILanguage()==0x409&&GetLastError()==0x148,374);
 check(MulDiv(420,96,96)==420&&MulDiv(5,1,2)==3&&MulDiv(-5,1,2)==-3&&MulDiv(5,1,-2)==-3&&MulDiv(-5,1,-2)==3&&MulDiv(INT32_MAX,INT32_MAX,INT32_MAX)==INT32_MAX&&MulDiv(INT32_MAX,INT32_MAX,1)==-1&&MulDiv(1,1,0)==-1&&MulDiv(INT32_MIN,0,1)==0&&MulDiv(INT32_MIN,1,INT32_MIN)==-1&&GetLastError()==0x148,394);
 uint64_t advapi=LoadLibraryExA("advapi32.dll",0,0);int(*allocate_sid)(const unsigned char*,unsigned char,unsigned,unsigned,unsigned,unsigned,unsigned,unsigned,unsigned,unsigned,void**)=GetProcAddress(advapi,"AllocateAndInitializeSid");void*(*free_sid)(void*)=GetProcAddress(advapi,"FreeSid");unsigned(*length_sid)(const void*)=GetProcAddress(advapi,"GetLengthSid");int(*valid_sid)(const void*)=GetProcAddress(advapi,"IsValidSid");int(*equal_sid)(const void*,const void*)=GetProcAddress(advapi,"EqualSid");check(advapi&&allocate_sid&&free_sid&&length_sid&&valid_sid&&equal_sid,375);
 unsigned char authority[6]={0,0,0,0,0,5};void*admin_sid=0,*same_sid=0,*users_sid=0;check(allocate_sid(authority,2,32,544,0,0,0,0,0,0,&admin_sid)&&allocate_sid(authority,2,32,544,0,0,0,0,0,0,&same_sid)&&allocate_sid(authority,2,32,545,0,0,0,0,0,0,&users_sid),376);
 int(*membership)(uint64_t,const void*,int*)=GetProcAddress(advapi,"CheckTokenMembership");int member[3]={0x148,99,0x148};check(membership&&membership(0,admin_sid,member+1)&&!member[1]&&member[0]==0x148&&member[2]==0x148&&membership(0,users_sid,member+1)&&member[1]==1,382);
 w8_mailbox*startup_mailbox=(void*)(uintptr_t)W8_MAILBOX;char saved_root=startup_mailbox->user_root[0];startup_mailbox->user_root[0]='?';check(security_profile148(0)==7&&membership(0,users_sid,member+1)&&member[1]==1,387);startup_mailbox->user_root[0]=saved_root;
 member[1]=99;check(!membership(1,users_sid,member+1)&&!member[1]&&GetLastError()==50,383);
 for(unsigned i=0;i<3;++i){void*group=0;unsigned rid=i==0?11:i==1?4:999;check(allocate_sid(authority,1,rid,0,0,0,0,0,0,0,&group)&&membership(0,group,member+1)&&member[1]==(i<2)&&!free_sid(group),384);}
 unsigned char world[6]={0,0,0,0,0,1};void*everyone=0;check(allocate_sid(world,1,0,0,0,0,0,0,0,0,&everyone)&&membership(0,everyone,member+1)&&member[1]==1&&!free_sid(everyone),385);
 check(valid_sid(admin_sid)&&length_sid(admin_sid)==16&&equal_sid(admin_sid,same_sid)&&!equal_sid(admin_sid,users_sid)&&((unsigned char*)admin_sid)[0]==1&&((unsigned char*)admin_sid)[1]==2&&((unsigned char*)admin_sid)[7]==5&&((unsigned*)admin_sid)[2]==32&&((unsigned*)admin_sid)[3]==544,377);
 check(!free_sid(admin_sid)&&!free_sid(same_sid)&&!free_sid(users_sid),378);void*maximum_sid=0;check(allocate_sid(authority,8,1,2,3,4,5,6,7,8,&maximum_sid)&&length_sid(maximum_sid)==40&&((unsigned*)maximum_sid)[9]==8&&!free_sid(maximum_sid),379);
 maximum_sid=(void*)99;check(!allocate_sid(authority,9,0,0,0,0,0,0,0,0,&maximum_sid)&&!maximum_sid&&GetLastError()==1337,380);unsigned char bad_sid[8]={2,0,0,0,0,0,0,5};check(!valid_sid(bad_sid)&&!valid_sid(0)&&FreeLibrary(advapi),381);
 unsigned id=RegisterWindowMessageW(L"Engacer.Message148.Parent");check(id>=0xc000&&id<=0xffff,222);
 check(RegisterWindowMessageA("engacer.message148.parent")==id,347);unsigned unicode_message=RegisterWindowMessageA("Engacer.Message148.\xc3\xa9");check(unicode_message>=0xc000&&unicode_message==RegisterWindowMessageW(L"Engacer.Message148.\u00e9"),348);
 check(!RegisterWindowMessageA(0)&&GetLastError()==87&&!RegisterWindowMessageA("\xff")&&GetLastError()==1113,349);
 struct{unsigned size,style;int64_t(*proc)(uint64_t,unsigned,uint64_t,int64_t);int class_extra,window_extra;uint64_t instance,icon,cursor,background;const uint16_t*menu,*name;uint64_t small_icon;} class_definition={80,0,class_proc148,0,16,0,0,0,0,0,L"Engacer.ClassEx148",0},class_readback={0};
 _Static_assert(sizeof(class_definition)==80,"Owned WNDCLASSEXW ABI");
 check(!RegisterClassExW(&class_readback)&&GetLastError()==87,350);unsigned class_atom=RegisterClassExW(&class_definition);check(class_atom>=0xc000&&!RegisterClassExW(&class_definition)&&GetLastError()==1410,351);
 class_readback.size=80;check(GetClassInfoExW(0,(const uint16_t*)(uintptr_t)class_atom,&class_readback)&&class_readback.proc==class_proc148&&class_readback.window_extra==16&&!class_readback.small_icon,352);
 uint64_t hidden=CreateWindowExW(0,(const uint16_t*)(uintptr_t)class_atom,L"Owned class lifecycle",0,0,0,100,100,0,0,0,0);check(hidden&&class_created148==1&&!UnregisterClassW(class_definition.name,0)&&GetLastError()==1412,353);
 SetLastError(0x148);check(!GetWindowLongW(hidden,-16)&&GetLastError()==0x148&&GetWindowLongW(desktop,-16)==0x10000000&&!SetWindowLongPtrW(hidden,8,INT64_C(0x11223344aabbccdd))&&GetWindowLongW(hidden,8)==(int)0xaabbccddu&&GetWindowLongW(hidden,12)==0x11223344&&GetWindowLongPtrW(hidden,8)==INT64_C(0x11223344aabbccdd),395);check(!GetWindowLongW(hidden,13)&&GetLastError()==1413,396);
 int adjusted[4]={0,0,123,67},plain_adjusted[4]={0,0,123,67};check(AdjustWindowRectEx(adjusted,0x02c80000,0,0)&&AdjustWindowRect(plain_adjusted,0x02c80000,0),397);for(unsigned i=0;i<4;++i)check(adjusted[i]==plain_adjusted[i],398);
 uint64_t framed=CreateWindowExW(0,(const uint16_t*)(uintptr_t)class_atom,L"Owned client geometry",0x02c80000,0,0,adjusted[2]-adjusted[0],adjusted[3]-adjusted[1],0,0,0,0);int framed_client[4];check(framed&&class_created148==2&&GetClientRect(framed,framed_client)&&!framed_client[0]&&!framed_client[1]&&framed_client[2]==123&&framed_client[3]==67,399);
 class_delta148=10;check(SetWindowPos(framed,0,0,0,202,141,0x216)&&GetClientRect(framed,framed_client)&&framed_client[2]==210&&framed_client[3]==100&&class_pre148==1&&class_post148==1&&!class_moves148&&class_sizes148==1&&class_size148==(210u|(100u<<16)),401);
 int placed[4];check(SetWindowPos(framed,0,30,40,-7,-9,0x215)&&GetWindowRect(framed,placed)&&placed[0]==30&&placed[1]==40&&placed[2]-placed[0]==212&&placed[3]-placed[1]==141&&class_pre148==2&&class_post148==2&&class_moves148==1&&class_sizes148==1&&class_move148==(31u|(80u<<16)),402);
 check(SetWindowPos(framed,0,35,45,0,0,0x415)&&class_pre148==2&&class_post148==3&&class_moves148==2&&class_sizes148==1&&class_move148==(36u|(85u<<16)),403);check(!SetWindowPos(framed,0,1,1,1,1,0)&&GetLastError()==50&&GetWindowRect(framed,placed)&&placed[0]==35&&placed[1]==45&&DestroyWindow(framed)&&class_destroyed148==1,404);
 int invalid_adjustment[4]={INT32_MIN,0,10,10};check(!AdjustWindowRectEx(invalid_adjustment,0x02c80000,0,0)&&invalid_adjustment[0]==INT32_MIN&&!AdjustWindowRectEx(plain_adjusted,0x02c80000,0,0x200),400);
 button_tests148(hidden);
 subclass_tests148(hidden);
 check(DestroyWindow(hidden)&&class_destroyed148==2,354);subclass_cleanup148(class_atom);check(UnregisterClassW(class_definition.name,0)&&!GetClassInfoExW(0,class_definition.name,&class_readback)&&GetLastError()==1411,354);
 for(unsigned i=0;i<70000;++i)check(RegisterWindowMessageW(L"engacer.message148.parent")==id,223);
 uint16_t path[512],command[520];unsigned n=GetModuleFileNameW(0,path,512);check(n&&n<512,224);
 uint16_t long_path[512];check(GetLongPathNameW(path,0,0)==n+1,362);long_path[0]=0x9b9b;check(GetLongPathNameW(path,long_path,n)==n+1&&long_path[0]==0x9b9b,363);check(GetLongPathNameW(path,long_path,512)==n,364);for(unsigned i=0;i<=n;++i)check(long_path[i]==path[i],365);check(GetLongPathNameW(long_path,long_path,512)==n&&!GetLongPathNameW(L"relative",long_path,512)&&GetLastError()==50,366);
 check(GetShortPathNameW(path,0,0)==n+1,367);long_path[0]=0x9b9b;check(GetShortPathNameW(path,long_path,n)==n+1&&long_path[0]==0x9b9b&&GetShortPathNameW(path,long_path,512)==n,368);for(unsigned i=0;i<=n;++i)check(long_path[i]==path[i],369);check(GetShortPathNameW(long_path,long_path,512)==n&&!GetShortPathNameW(L"C:\\Users\\Owner\\Documents\\Missing-short-path-148",long_path,512),370);
 unsigned attributes[11]={0};attributes[0]=attributes[10]=0x9b9b9b9b;check(GetFileAttributesExW(path,0,attributes+1)&&attributes[1]==GetFileAttributesW(path)&&attributes[0]==0x9b9b9b9b&&attributes[10]==0x9b9b9b9b,371);
 uint64_t file_metadata=CreateFileW(path,0x80000000,1,0,3,0x80,0);int64_t metadata_size=0;check(file_metadata!=UINT64_MAX&&GetFileSizeEx(file_metadata,&metadata_size)&&metadata_size>0&&((uint64_t)attributes[8]<<32|attributes[9])==(uint64_t)metadata_size&&CloseHandle(file_metadata),372);
 attributes[1]=0xabcdef;check(!GetFileAttributesExW(path,1,attributes+1)&&GetLastError()==87&&attributes[1]==0xabcdef&&!GetFileAttributesExW(L"C:\\Users\\Owner\\Documents\\Missing-metadata148",0,attributes+1)&&attributes[1]==0xabcdef,373);
 command[0]='"';for(unsigned i=0;i<n;++i)command[i+1]=path[i];command[n+1]='"';command[n+2]=' ';command[n+3]='!';command[n+4]=0;
 uint8_t startup[104]={0};*(unsigned*)startup=104;struct{uint64_t process,thread;unsigned pid,tid;} process={0};
 check(CreateProcessW(path,command,0,0,0,4,0,0,startup,&process),225);uint64_t snapshot=CreateToolhelp32Snapshot(2,0);check(snapshot!=UINT64_MAX,290);snapshot_check148(snapshot,process.pid,1);check(ResumeThread(process.thread)==1,291);check(WaitForSingleObject(process.process,30000)==0,226);
 unsigned result=0;check(GetExitCodeProcess(process.process,&result)&&result==id,227);check(CloseHandle(process.thread)&&CloseHandle(process.process),228);
 snapshot_check148(snapshot,process.pid,1);check(CloseHandle(snapshot),292);process_entry_native148 stale={.size=sizeof(stale)};check(!Process32FirstW(snapshot,&stale)&&GetLastError()==6,293);
 uint64_t fresh=CreateToolhelp32Snapshot(2,UINT32_MAX);check(fresh!=UINT64_MAX&&fresh!=snapshot,294);snapshot_check148(fresh,process.pid,0);check(CloseHandle(fresh),295);
 command[n+3]='?';check(CreateProcessW(path,command,0,0,0,0x04000000u,0,0,startup,&process),265);check(WaitForSingleObject(process.process,30000)==0,266);
 check(GetExitCodeProcess(process.process,&result)&&result==id&&CloseHandle(process.thread)&&CloseHandle(process.process),267);check(SetErrorMode(0)==0x8001&&!GetErrorMode(),268);
 unsigned other=RegisterWindowMessageW(L"Engacer.Message148.ChildFirst");check(other>=0xc000&&other!=id,229);
 uint64_t module=LoadLibraryExA("kernel32.dll",0,0);check(module&&module==GetModuleHandleW(L"kernel32.dll")&&FreeLibrary(module),238);
 check(!LoadLibraryExA(0,0,0)&&GetLastError()==87,239);
 check(!LoadLibraryExA("\xff",0,0)&&GetLastError()==1113,240);
 check(!LoadLibraryExA("kernel32.dll",1,0)&&GetLastError()==50,242);
 uint16_t system[260];check(GetSystemDirectoryW(system,260)==19,243);
 uint64_t shell=LoadLibraryExA("SHLWAPI.dll",0,0);int(*append)(uint16_t*,const uint16_t*)=GetProcAddress(shell,"PathAppendW");
 check(shell&&append&&append(system,L"own.dll"),244);const uint16_t expected[]=L"C:\\Windows\\System32\\own.dll";for(unsigned i=0;i<sizeof(expected)/2;++i)check(system[i]==expected[i],245);
 uint64_t shell32=LoadLibraryExA("shell32.dll",0,0);int(*folder)(uint64_t,int,uint64_t,unsigned,uint16_t*)=GetProcAddress(shell32,"SHGetFolderPathW");check(folder!=0,269);
 uint16_t**(*split_command)(const uint16_t*,int*)=GetProcAddress(shell32,"CommandLineToArgvW");check(split_command!=0,355);int arguments=0;uint16_t**words=split_command(L"p \"a b\" \"\" tail",&arguments);check(words&&arguments==4&&words[0][0]=='p'&&!words[0][1]&&words[1][0]=='a'&&words[1][1]==' '&&words[1][2]=='b'&&!words[1][3]&&!words[2][0]&&words[3][0]=='t'&&!words[3][4],356);check(!LocalFree(words),357);
 words=split_command(L" p",&arguments);check(words&&arguments==2&&!words[0][0]&&words[1][0]=='p'&&!LocalFree(words),358);
 words=split_command(L"",&arguments);check(words&&arguments==1,359);for(unsigned i=0;i<=n;++i)check(words[0][i]==path[i],360);check(!LocalFree(words)&&!split_command(0,&arguments)&&!split_command(L"p",0),361);
 uint16_t profile[260],known[260];check(!folder(0,0x28,0,0,profile)&&!folder(0,0x1c,0,0,known),270);unsigned folder_attributes=GetFileAttributesW(known);check(folder_attributes!=UINT32_MAX&&(folder_attributes&16),282);
 check(append(profile,L"AppData\\Local"),271);for(unsigned i=0;profile[i]||known[i];++i)check(profile[i]==known[i],272);
 check(!folder(0,0x1c,0,1,profile),273);for(unsigned i=0;profile[i]||known[i];++i)check(profile[i]==known[i],274);
 known[0]='x';check(folder(0,0x1c,1,0,known)==(int)0x80070005u&&!known[0],275);
 check(!folder(0,0x4006,0,0,known),276);unsigned favorites=GetFileAttributesW(known);
 if(favorites==UINT32_MAX){profile[0]='x';check(folder(0,6,0,0,profile)!=0&&!profile[0],277);check(GetFileAttributesW(known)==UINT32_MAX,278);check(!folder(0,0x8006,0,0,profile),279);folder_attributes=GetFileAttributesW(profile);check(folder_attributes!=UINT32_MAX&&(folder_attributes&16),283);check(RemoveDirectoryW(profile),280);}
 check(FreeLibrary(shell32)&&FreeLibrary(shell),281);
 uint64_t gdiplus=LoadLibraryExA("gdiplus.dll",0,0);unsigned(*startup_gp)(uint64_t*,const void*,void*)=GetProcAddress(gdiplus,"GdiplusStartup");shutdown_gp148=GetProcAddress(gdiplus,"GdiplusShutdown");check(startup_gp&&shutdown_gp148,303);
 struct{unsigned version,pad;uint64_t callback;int suppress_thread,suppress_codecs;} gp_input={1,0,0,0,0};uint64_t gp_token=0;
 check(!startup_gp(&gp_token,&gp_input,0)&&gp_token,304);uint64_t gp_thread=CreateThread(0,0,gp_shutdown_worker148,(void*)(uintptr_t)gp_token,0,0);check(gp_thread&&WaitForSingleObject(gp_thread,30000)==0&&CloseHandle(gp_thread),305);
 uint64_t gp_tokens[8];gp_input.suppress_codecs=1;for(unsigned i=0;i<8;++i){check(!startup_gp(gp_tokens+i,&gp_input,0)&&gp_tokens[i]!=gp_token,306);for(unsigned j=0;j<i;++j)check(gp_tokens[j]!=gp_tokens[i],307);}
 check(startup_gp(&gp_token,&gp_input,0)==3&&!gp_token,308);for(unsigned i=0;i<8;++i)shutdown_gp148(gp_tokens[i]);
 gp_input.version=0;check(startup_gp(&gp_token,&gp_input,0)==17&&!gp_token,309);gp_input.version=1;gp_input.suppress_thread=1;check(startup_gp(&gp_token,&gp_input,0)==2&&!gp_token,310);
 uint64_t hooks[2]={99,99};check(!startup_gp(&gp_token,&gp_input,hooks)&&gp_token&&hooks[0]!=99&&hooks[1]!=99&&hooks[0]&&hooks[1],311);
 unsigned(*hook)(uint64_t*)=(void*)(uintptr_t)hooks[0];void(*unhook)(uint64_t)=(void*)(uintptr_t)hooks[1];uint64_t hook_tokens[8];
 check(hook(0)==2,313);for(unsigned i=0;i<8;++i){check(!hook(hook_tokens+i)&&hook_tokens[i],314);for(unsigned j=0;j<i;++j)check(hook_tokens[j]!=hook_tokens[i],315);}
 uint64_t extra_hook=99;check(hook(&extra_hook)==3&&!extra_hook,316);
 struct{uint64_t window;unsigned message,pad;uint64_t wp;int64_t lp;unsigned time;int x,y;unsigned private_;} notification={0};
 _Static_assert(sizeof(notification)==48,"AMD64 MSG ABI");
 check(PostMessageW(0,0x7e,0,0)&&PeekMessageW(&notification,0,0x7e,0x7e,1)&&notification.message==0x7e,317);
 for(unsigned i=0;i<8;++i)unhook(hook_tokens[i]);uint64_t renewed_hook=0;check(!hook(&renewed_hook)&&renewed_hook!=hook_tokens[7],318);unhook(renewed_hook);
 void*(*gp_alloc)(size_t)=GetProcAddress(gdiplus,"GdipAlloc");void(*gp_free)(void*)=GetProcAddress(gdiplus,"GdipFree");check(gp_alloc&&gp_free,320);
 unsigned char*gp_blocks[8];for(unsigned i=0;i<8;++i){size_t bytes=17+(size_t)i*8192;gp_blocks[i]=gp_alloc(bytes);check(gp_blocks[i]&&!((uintptr_t)gp_blocks[i]&15),321);for(size_t j=0;j<bytes;++j)gp_blocks[i][j]=(unsigned char)(i+j);}
 for(unsigned i=0;i<8;++i){size_t bytes=17+(size_t)i*8192;for(size_t j=0;j<bytes;++j)check(gp_blocks[i][j]==(unsigned char)(i+j),322);gp_free(gp_blocks[i]);}gp_free(0);check(!gp_alloc(SIZE_MAX),323);
 unsigned(*bitmap_create)(int,int,int,unsigned,void*,void**)=GetProcAddress(gdiplus,"GdipCreateBitmapFromScan0");unsigned(*bitmap_dispose)(void*)=GetProcAddress(gdiplus,"GdipDisposeImage");
 unsigned(*bitmap_width)(void*,unsigned*)=GetProcAddress(gdiplus,"GdipGetImageWidth");unsigned(*bitmap_height)(void*,unsigned*)=GetProcAddress(gdiplus,"GdipGetImageHeight");unsigned(*bitmap_get)(void*,int,int,unsigned*)=GetProcAddress(gdiplus,"GdipBitmapGetPixel");unsigned(*bitmap_set)(void*,int,int,unsigned)=GetProcAddress(gdiplus,"GdipBitmapSetPixel");
 check(bitmap_create&&bitmap_dispose&&bitmap_width&&bitmap_height&&bitmap_get&&bitmap_set,324);
 void*bitmap=0;unsigned dimension=0,color=99;check(!bitmap_create(7,3,0,0x26200a,0,&bitmap)&&bitmap,325);check(!bitmap_width(bitmap,&dimension)&&dimension==7&&!bitmap_height(bitmap,&dimension)&&dimension==3,326);
 check(!bitmap_get(bitmap,6,2,&color)&&!color&&!bitmap_set(bitmap,6,2,0x80402010)&&!bitmap_get(bitmap,6,2,&color)&&color==0x80402010,327);check(bitmap_get(bitmap,7,0,&color)==2&&bitmap_set(bitmap,0,-1,0)==2,328);
 unsigned(*graphics_create)(void*,void**)=GetProcAddress(gdiplus,"GdipGetImageGraphicsContext");unsigned(*graphics_delete)(void*)=GetProcAddress(gdiplus,"GdipDeleteGraphics");unsigned(*graphics_clear)(void*,unsigned)=GetProcAddress(gdiplus,"GdipGraphicsClear");check(graphics_create&&graphics_delete&&graphics_clear,337);
 void*contexts[32];for(unsigned i=0;i<32;++i)check(!graphics_create(bitmap,contexts+i)&&contexts[i],338);void*extra_context=(void*)99;check(graphics_create(bitmap,&extra_context)==3&&!extra_context&&bitmap_dispose(bitmap)==4,339);
 const char*setting_names[4]={"CompositingQuality","SmoothingMode","TextRenderingHint","PageUnit"};int defaults[4]={0,3,0,1},selected[4]={2,4,5,2};
 for(unsigned i=0;i<4;++i){char set_name[64]="GdipSet",get_name[64]="GdipGet";unsigned n=0;while(setting_names[i][n]){set_name[7+n]=get_name[7+n]=setting_names[i][n];++n;}set_name[7+n]=get_name[7+n]=0;unsigned(*setter)(void*,int)=GetProcAddress(gdiplus,set_name);unsigned(*getter)(void*,int*)=GetProcAddress(gdiplus,get_name);int actual=-99;check(setter&&getter&&!getter(contexts[0],&actual)&&actual==defaults[i],344);check(!setter(contexts[0],selected[i])&&!getter(contexts[0],&actual)&&actual==selected[i]&&!getter(contexts[1],&actual)&&actual==defaults[i],345);if(i)check(setter(contexts[0],99)==2&&!getter(contexts[0],&actual)&&actual==selected[i],346);}
 check(!graphics_clear(contexts[0],0x80442211),340);for(int y=0;y<3;++y)for(int x=0;x<7;++x)check(!bitmap_get(bitmap,x,y,&color)&&color==0x80442211,341);
 for(unsigned i=0;i<32;++i)check(!graphics_delete(contexts[i]),342);check(graphics_delete(contexts[31])==2&&graphics_clear(contexts[0],0)==2,343);check(!bitmap_dispose(bitmap)&&bitmap_dispose(bitmap)==2,329);
 unsigned external[6]={0xff112233,0xff445566,0xff778899,0xffaabbcc,0xff123456,0xff654321};
 check(!bitmap_create(3,2,-12,0x26200a,external+3,&bitmap)&&!bitmap_get(bitmap,0,1,&color)&&color==external[0],330);check(!bitmap_set(bitmap,2,0,0x80abcdef)&&external[5]==0x80abcdef&&!bitmap_dispose(bitmap)&&external[0]==0xff112233,331);
 bitmap=(void*)99;check(bitmap_create(0,1,0,0x26200a,0,&bitmap)==2&&!bitmap,332);check(bitmap_create(100000,100000,0,0x26200a,0,&bitmap)==3&&!bitmap,333);
 void*bitmaps[32];for(unsigned i=0;i<32;++i)check(!bitmap_create(1,1,0,0x21808,0,bitmaps+i),334);check(bitmap_create(1,1,0,0x21808,0,&bitmap)==3&&!bitmap,335);for(unsigned i=0;i<32;++i)check(!bitmap_dispose(bitmaps[i]),336);
 shutdown_gp148(gp_token);extra_hook=99;check(hook(&extra_hook)==18&&!extra_hook,319);check(FreeLibrary(gdiplus),312);
 unsigned short atom=GlobalAddAtomW(L"Engacer.Message148.Parent");check(atom>=0xc000&&!GlobalDeleteAtom(atom)&&RegisterWindowMessageW(L"Engacer.Message148.Parent")==id,230);
 InitializeSRWLock(&lock);check(TryAcquireSRWLockExclusive(&lock)&&!TryAcquireSRWLockExclusive(&lock)&&!TryAcquireSRWLockShared(&lock),231);ReleaseSRWLockExclusive(&lock);
 check(TryAcquireSRWLockShared(&lock)&&TryAcquireSRWLockShared(&lock)&&!TryAcquireSRWLockExclusive(&lock),232);ReleaseSRWLockShared(&lock);ReleaseSRWLockShared(&lock);
 uint64_t threads[8];for(unsigned i=0;i<8;++i){threads[i]=CreateThread(0,0,worker,(void*)(uintptr_t)i,4,0);check(threads[i]!=0,233);}
 uint64_t snapshots[8];for(unsigned i=0;i<8;++i){snapshots[i]=CreateToolhelp32Snapshot(2,0);check(snapshots[i]!=UINT64_MAX,298);}
 check(CreateToolhelp32Snapshot(2,0)==UINT64_MAX&&GetLastError()==8,299);process_entry_native148 thread_entry={.size=sizeof(thread_entry)};check(Process32FirstW(snapshots[0],&thread_entry)&&thread_entry.pid==GetCurrentProcessId()&&thread_entry.threads==9,300);
 for(unsigned i=0;i<8;++i)check(CloseHandle(snapshots[i]),301);for(unsigned i=0;i<8;++i)check(ResumeThread(threads[i])==1,302);
 check(WaitForMultipleObjects(8,threads,1,30000)==0,234);for(unsigned i=0;i<8;++i)check(CloseHandle(threads[i]),235);
 check(left==4000&&right==12000&&!lock,236);
 uint64_t warm=HeapCreate(0,0,0);check(warm&&HeapDestroy(warm),247);uint64_t pages=owned_pages148();
 uint64_t h=HeapCreate(0,131072,0),other_heap=HeapCreate(0,0,0);check(h&&other_heap&&h!=other_heap,248);
 uint8_t*data=HeapAlloc(h,0,1);check(data&&!((uintptr_t)data&15)&&HeapSize(h,0,data)>=1,249);data[0]=0x3f;
 check(!HeapFree(other_heap,0,data)&&data[0]==0x3f,250);
 data=HeapReAlloc(h,8,data,70000);check(data&&data[0]==0x3f,251);for(unsigned i=1;i<70000;++i)check(data[i]==0,252);
 check(!HeapReAlloc(h,16,data,1024*1024)&&data[0]==0x3f,253);
 uint8_t*small=HeapReAlloc(h,0,data,32);check(small==data&&HeapFree(h,0,small),254);
 check(HeapAlloc(other_heap,8,16000)!=0,255);check(HeapDestroy(h)&&HeapDestroy(other_heap),256);
 check(!HeapAlloc(h,0,1)&&!HeapDestroy(h),257);uint64_t after=owned_pages148();check(after==pages,258);
 say148("M148_HEAP_PAGES before=");number148(pages);say148(" after=");number148(after);say148("\n");
 static const char text[]="M148_NATIVE_SESSION_MESSAGES_SRW_PASS\n";unsigned written=0;
 check(WriteFile(GetStdHandle((unsigned)-11),text,sizeof(text)-1,&written,0)&&written==sizeof(text)-1,237);ExitProcess(0);
}
