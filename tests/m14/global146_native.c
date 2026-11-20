/* Owned native global-memory ownership, quotas and concurrent lifetimes. */
typedef unsigned long long U;
__declspec(dllimport) U GlobalAlloc(unsigned,U);
__declspec(dllimport) U GlobalFree(U);
__declspec(dllimport) void*GlobalLock(U);
__declspec(dllimport) int GlobalUnlock(U);
__declspec(dllimport) U GlobalSize(U);
__declspec(dllimport) unsigned GlobalFlags(U);
__declspec(dllimport) U GlobalHandle(const void*);
__declspec(dllimport) void*LocalAlloc(unsigned,U);
__declspec(dllimport) void*LocalFree(void*);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void SetLastError(unsigned);
__declspec(dllimport) U CreateThread(void*,U,unsigned(*)(void*),void*,unsigned,unsigned*);
__declspec(dllimport) unsigned WaitForMultipleObjects(unsigned,const U*,int,unsigned);
__declspec(dllimport) int GetExitCodeThread(U,unsigned*);
__declspec(dllimport) int CloseHandle(U);
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
static void check(int yes,unsigned code){if(!yes)ExitProcess(code);}
static unsigned worker(void*argument){
 unsigned seed=(unsigned)(U)argument;
 for(unsigned cycle=0;cycle<100;++cycle){U h=GlobalAlloc(0x42,33);if(!h)return 80;unsigned char*p=GlobalLock(h);if(!p)return 81;
  for(U i=0;i<GlobalSize(h);++i)if(p[i])return 82;p[0]=(unsigned char)seed;
  if(GlobalHandle(p)!=h||GlobalFlags(h)!=1||GlobalUnlock(h)||GetLastError())return 83;
  if(GlobalFree(h)||GlobalFlags(h)!=0x8000||GetLastError()!=6)return 84;
 }return 0;
}
void entry(void);void*volatile anchor146=&entry;
void entry(void){
 U fixed=GlobalAlloc(0x40,19);check(fixed!=0&&GlobalLock(fixed)==(void*)fixed&&GlobalFlags(fixed)==0,10);
 check(GlobalUnlock(fixed)&&GlobalHandle((void*)fixed)==fixed&&GlobalSize(fixed)>=19,11);
 check(LocalFree((void*)fixed)==(void*)fixed&&GetLastError()==6&&GlobalSize(fixed)>=19,12);
 check(!GlobalFree(fixed)&&!GlobalFree(0),13);
 void*local=LocalAlloc(0x40,32);check(local!=0,14);check(GlobalFree((U)local)==(U)local&&GetLastError()==6,15);check(!LocalFree(local),16);
 U discarded=GlobalAlloc(2,0);check(discarded&&GlobalSize(discarded)==0&&GlobalFlags(discarded)==0x4000,17);
 check(!GlobalLock(discarded)&&GetLastError()==157&&!GlobalFree(discarded),18);
 U h=GlobalAlloc(0x42,23);check(h!=0&&h!=discarded,19);unsigned char*p=GlobalLock(h);check(p!=0&&GlobalHandle(p)==h,20);
 U size=GlobalSize(h);for(U i=0;i<size;++i)check(p[i]==0,21);p[0]=77;
 check(GlobalLock(h)==p&&GlobalFlags(h)==2&&GlobalUnlock(h)&&GlobalFlags(h)==1,22);
 SetLastError(99);check(!GlobalUnlock(h)&&GetLastError()==0&&GlobalFlags(h)==0,23);
 check(!GlobalUnlock(h)&&GetLastError()==158,24);
 for(unsigned i=0;i<255;++i)check(GlobalLock(h)==p,25);check(GlobalFlags(h)==255,26);
 check(!GlobalLock(h)&&GetLastError()==1816&&p[0]==77&&GlobalFlags(h)==255,27);
 check(!GlobalFree(h)&&!GlobalLock(h)&&GetLastError()==6,28);
 U newer=GlobalAlloc(2,23);check(newer&&newer!=h&&GlobalFlags(h)==0x8000,29);check(!GlobalFree(newer),30);
 check(!GlobalAlloc(0x80000000u,32)&&GetLastError()==50,31);
 check(!GlobalAlloc(2,24u*1024u*1024u+1)&&GetLastError()==8,32);
 U handles[128];for(unsigned i=0;i<128;++i){handles[i]=GlobalAlloc(0x42,17);check(handles[i]!=0,33);}
 check(!GlobalAlloc(2,1)&&GetLastError()==1816,34);
 for(unsigned i=0;i<128;++i){check(GlobalSize(handles[i])>=17,35);check(!GlobalFree(handles[i]),36);}
 unsigned id=0;U threads[2]={CreateThread(0,0,worker,(void*)41,0,&id),CreateThread(0,0,worker,(void*)59,0,&id)};
 check(threads[0]&&threads[1]&&WaitForMultipleObjects(2,threads,1,10000)==0,37);
 for(unsigned i=0;i<2;++i){unsigned code=999;check(GetExitCodeThread(threads[i],&code)&&code==0&&CloseHandle(threads[i]),38);}
 U again=GlobalAlloc(0x42,4097);check(again&&GlobalSize(again)>=4097&&!GlobalFree(again),39);
 static const char message[]="M146_GLOBAL_MEMORY_OWNERSHIP_QUOTA_THREADS_PASS\n";unsigned written=0;
 check(WriteFile(GetStdHandle((unsigned)-11),message,sizeof(message)-1,&written,0)&&written==sizeof(message)-1,40);ExitProcess(0);
}
