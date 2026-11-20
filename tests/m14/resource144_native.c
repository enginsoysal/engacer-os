/* Owned Win64 PE resource/image/heap fixture; no foreign app imitation. */
typedef unsigned long long H;
typedef unsigned long long SIZE;
typedef unsigned short W;
__declspec(dllimport) H LoadLibraryW(const W*);
__declspec(dllimport) int FreeLibrary(H);
__declspec(dllimport) void*GetProcAddress(H,const char*);
__declspec(dllimport) H FindResourceW(H,const W*,const W*);
__declspec(dllimport) H FindResourceExW(H,const W*,const W*,unsigned);
__declspec(dllimport) H LoadResource(H,H);
__declspec(dllimport) unsigned SizeofResource(H,H);
__declspec(dllimport) const void*LockResource(H);
__declspec(dllimport) int LoadStringW(H,unsigned,W*,int);
__declspec(dllimport) H LoadImageW(H,const W*,unsigned,int,int,unsigned);
__declspec(dllimport) H LoadBitmapW(H,const W*);
__declspec(dllimport) int DestroyIcon(H);
__declspec(dllimport) int DeleteObject(H);
__declspec(dllimport) H ImageList_Create(int,int,unsigned,int,int);
__declspec(dllimport) int ImageList_ReplaceIcon(H,int,H);
__declspec(dllimport) int ImageList_AddMasked(H,H,unsigned);
__declspec(dllimport) int ImageList_GetImageCount(H);
__declspec(dllimport) int ImageList_Destroy(H);
__declspec(dllimport) H GetProcessHeap(void);
__declspec(dllimport) void*HeapAlloc(H,unsigned,SIZE);
__declspec(dllimport) int HeapFree(H,unsigned,void*);
__declspec(dllimport) SIZE HeapSize(H,unsigned,const void*);
__declspec(dllimport) H GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(H,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) unsigned GetLastError(void);
static const W*volatile anchor144=L"Native resource fixture";
static void say(const char*s){unsigned n=0,w=0;while(s[n])++n;WriteFile(GetStdHandle((unsigned)-11),s,n,&w,0);}
static void check(unsigned ok,const char*text){if(!ok){say("M144_RESOURCE_FAIL ");say(text);say("\n");ExitProcess(1);}}
void entry(void){
 check(anchor144[0]=='N',"fixture relocation");H heap=GetProcessHeap();unsigned char*memory=HeapAlloc(heap,8,128);check(memory!=0,"HeapAlloc");for(unsigned i=0;i<128;++i)check(memory[i]==0,"zero-initialized heap");check(HeapSize(heap,0,memory)>=128,"heap size");check(!HeapFree(heap,0,memory+1)&&GetLastError()==87,"interior pointer refusal");check(HeapFree(heap,0,memory),"HeapFree");check(HeapSize(heap,0,memory)==(SIZE)-1,"freed heap refusal");
 H common=LoadLibraryW(L"comctl32.dll");check(common!=0,"known provider");check(GetProcAddress(common,"ImageList_Create")!=0,"implemented dynamic API");check(GetProcAddress(common,"PropertySheetW")==0&&GetLastError()==127,"unsupported discovery remains null");check(FreeLibrary(common),"provider release");
 H stale=0;
 for(unsigned turn=0;turn<25;++turn){H module=LoadLibraryW(L"resources144.dll");check(module!=0,"resource-only DLL load");
  if(stale)check(SizeofResource(module,stale)==0&&GetLastError()==1814,"stale resource generation");
  H resource=FindResourceW(module,(const W*)1,(const W*)10);check(resource!=0,"FindResourceW");check(resource==FindResourceW(module,L"#1",L"#10"),"numeric string resource IDs");check(resource==FindResourceExW(module,(const W*)10,(const W*)1,0x409),"exact language lookup");check(!FindResourceExW(module,(const W*)10,(const W*)1,0x419)&&GetLastError()==1815,"absent language");
  check(SizeofResource(module,resource)==26,"resource length");const char*data=LockResource(LoadResource(module,resource));check(data&&data[0]=='i'&&data[25]=='\n',"real immutable resource data");
  W text[32];check(LoadStringW(module,2,text,32)==16&&text[0]=='N'&&text[15]=='s'&&text[16]==0,"counted UTF16 string");check(LoadStringW(module,2,text,5)==4&&text[4]==0,"truncated string termination");const W*view=0;check(LoadStringW(module,2,(W*)&view,0)==16&&view&&view[0]=='N',"zero-copy string view");check(LoadStringW(module,3,text,32)==4&&text[3]==0xe9,"Unicode resource string");
  H icon=LoadImageW(module,(const W*)1,1,4,2,0);check(icon!=0,"original icon resource decoder");H bitmap=LoadBitmapW(module,(const W*)1);check(bitmap!=0,"original bitmap resource decoder");H list=ImageList_Create(4,2,0x21,0,1);check(list!=0,"image list creation");check(ImageList_ReplaceIcon(list,-1,icon)==0,"append copied icon");check(ImageList_GetImageCount(list)==1,"image list count");check(DestroyIcon(icon),"source icon destroyed");check(ImageList_GetImageCount(list)==1,"copied icon lifetime");check(ImageList_AddMasked(list,bitmap,0x00ff00ff)==1&&ImageList_GetImageCount(list)==3,"masked bitmap strip");check(DeleteObject(bitmap),"bitmap released");check(ImageList_Destroy(list),"image list released");check(!ImageList_Destroy(list)&&GetLastError()==6,"stale image-list refusal");
  stale=resource;check(FreeLibrary(module),"resource DLL unmap");check(!LockResource(stale)&&GetLastError()==1814,"resource invalid after unload");
 }
 say("M144_RESOURCE_IMAGE_HEAP_PASS\n");ExitProcess(0);
}
