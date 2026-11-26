/* i386 imports point at per-process stdcall adapters. The adapter page is
 * immutable in ring 3 and carries no readable kernel pointers. */
#define PE32_THUNKS1410 ((uint32_t)W8_X86_BASE)
#define PE32_STACK1410 UINT32_C(0x5ff00000)
#define PE32_TEB1410 UINT32_C(0x5fe00000)
#define PE32_STACK_BYTES1410 UINT32_C(0x10000)
#define PE32_EXIT_RETURN1410 UINT32_C(0x40000ff0)
#define PE32_GATE_FIRST1410 UINT32_C(0x14100000)

enum {
 X86_EXIT1410,X86_GET_ERROR1410,X86_SET_ERROR1410,X86_PID1410,
 X86_STD_HANDLE1410,X86_WRITE1410,
};
typedef struct {const char *name;uint8_t arguments;} pe32_api1410;
static const pe32_api1410 pe32_kernel1410[]={
 {"ExitProcess",1},{"GetLastError",0},{"SetLastError",1},{"GetCurrentProcessId",0},
 {"GetStdHandle",1},{"WriteFile",5},
};
static unsigned pe32_string1410(const win_pe32_image1410 *image,uint32_t rva,char *out,unsigned cap){
 for(unsigned i=0;i<cap;++i){
  if(rva>=image->bytes||!win_pe32_mapped1410(image,rva,1)||
     user8(W8_PE32_IMAGE1410+rva,out+i,1,0))return 1;
  ++rva;
  if(!out[i])return !i;
  if((uint8_t)out[i]<32||(uint8_t)out[i]>126)return 1;
 }
 return 1;
}
static unsigned pe32_name_equal1410(const char *a,const char *b){
 return equal_utf8_143(a,length8(a),b,length8(b))==1;
}
static uint32_t pe32_find_api1410(const char *library,const char *name){
 if(!pe32_name_equal1410(library,"kernel32.dll")&&
    !pe32_name_equal1410(library,"kernelbase.dll"))return 0;
 for(unsigned i=0;i<sizeof(pe32_kernel1410)/sizeof(*pe32_kernel1410);++i)
  if(equal8(name,pe32_kernel1410[i].name))return PE32_THUNKS1410+i*16u;
 return 0;
}
static unsigned pe32_bind_imports1410(const win_pe32_image1410 *image){
 win_pe32_directory1410 directory=image->directories[1];
 if(!directory.bytes)return 0;
 for(unsigned at=0;at+20<=directory.bytes;at+=20){
  uint32_t descriptor[5];
  if(user8(W8_PE32_IMAGE1410+directory.rva+at,descriptor,sizeof(descriptor),0))return 1;
  if(!(descriptor[0]|descriptor[1]|descriptor[2]|descriptor[3]|descriptor[4]))return 0;
  char library[128];
  if(!descriptor[3]||!descriptor[4]||pe32_string1410(image,descriptor[3],library,sizeof(library)))return 1;
  uint32_t lookup=descriptor[0]?descriptor[0]:descriptor[4],iat=descriptor[4];
  unsigned end=0;
  for(unsigned slot=0;slot<4096;++slot){
   uint32_t entry;
   if(!win_pe32_mapped1410(image,lookup,4)||!win_pe32_mapped1410(image,iat,4)||
      user8(W8_PE32_IMAGE1410+lookup,&entry,sizeof(entry),0))return 1;
   if(!entry){end=1;break;}
   if(entry&0x80000000u||entry>image->bytes-2)return 1;
   char name[160];
   if(pe32_string1410(image,entry+2,name,sizeof(name)))return 1;
   uint32_t target=pe32_find_api1410(library,name);
   if(!target||user8(W8_PE32_IMAGE1410+iat,&target,sizeof(target),1))return 1;
   lookup+=4;iat+=4;
  }
  if(!end)return 1;
 }
 return 1;
}
static unsigned pe32_install_thunks1410(void){
 if(map8(PE32_THUNKS1410,4096,3))return 1;
 for(unsigned i=0;i<sizeof(pe32_kernel1410)/sizeof(*pe32_kernel1410);++i){
  uint8_t stub[16]={0xb8,0,0,0,0,0xcd,0x80,0xc2,0,0,0xcc,0xcc,0xcc,0xcc,0xcc,0xcc};
  uint32_t call=PE32_GATE_FIRST1410+i;
  memcpy(stub+1,&call,4);stub[8]=(uint8_t)(pe32_kernel1410[i].arguments*4);
  if(user8(PE32_THUNKS1410+i*16u,stub,sizeof(stub),1))return 1;
 }
 uint8_t exit_return[]={0x50,0x6a,0,0xb8,0,0,0,0,0xcd,0x80,0xcc};
 uint32_t exit_call=PE32_GATE_FIRST1410+X86_EXIT1410;
 memcpy(exit_return+4,&exit_call,4);
 if(user8(PE32_EXIT_RETURN1410,exit_return,sizeof(exit_return),1))return 1;
 uint64_t *pte=pte8(PE32_THUNKS1410,0);
 *pte=(*pte&UINT64_C(0x000ffffffffff000))|5;
 return 0;
}
static inline unsigned pe32_start1410(const char *source,uint64_t *entry,uint64_t *stack){
 win_pe32_image1410 image;
 if(!pe32_parse_file1410(source,&image)||
    image.directories[9].bytes||image.directories[13].bytes||image.directories[14].bytes||
    pe32_map1410(source,&image)||pe32_install_thunks1410()||
    pe32_bind_imports1410(&image)||pe32_protect1410(W8_PE32_IMAGE1410,&image)||
    map8(PE32_STACK1410-16384u,16384,3)||map8(PE32_TEB1410,4096,3))return 1;
 uint32_t teb[16]={0};
 teb[0]=UINT32_MAX;teb[1]=PE32_STACK1410;teb[2]=PE32_STACK1410-PE32_STACK_BYTES1410;
 teb[6]=PE32_TEB1410;teb[8]=input8.process_id;
 if(user8(PE32_TEB1410,teb,sizeof(teb),1))return 1;
 uint32_t returning=PE32_EXIT_RETURN1410;
 *entry=W8_PE32_IMAGE1410+image.entry;*stack=PE32_STACK1410-4;
 return user8(*stack,&returning,sizeof(returning),1);
}
