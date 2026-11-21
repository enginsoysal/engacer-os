/* Checked streaming AMD64 loader. Inspection never calls foreign entry points. */
#define MODULES141 32u
#define IMAGE141_LIMIT (32u*1024*1024)
#define ARENA141 UINT64_C(0x110000000)
#include "module142.h"
static module141 modules141[MODULES141];
static lock142 loader_lock142;
static unsigned loading141,forwarding141,sequence141,inspect141;
static int parent141=-1;
static uint16_t u16(const void*p){uint16_t v;memcpy(&v,p,2);return v;}
static uint32_t u32(const void*p){uint32_t v;memcpy(&v,p,4);return v;}
static uint64_t u64(const void*p){uint64_t v;memcpy(&v,p,8);return v;}
static unsigned range141(uint64_t off,uint64_t bytes,uint64_t size){return off<=size&&bytes<=size-off;}
static void* rva141(module141*m,uint64_t rva,uint64_t bytes){if(!range141(rva,bytes,m->size))fail8("The Windows image contains an invalid relative address.");return m->base+rva;}
static const char* name141(module141*m,uint64_t rva){const char*p=rva141(m,rva,1);for(unsigned i=0;i<512&&i<m->size-rva;++i)if(!p[i])return p;fail8("The Windows image contains an unterminated name.");}
static const char* basename141(const char*p){const char*last=p;for(unsigned i=0;p[i];++i)if(p[i]=='/'||p[i]=='\\')last=p+i+1;return last;}
static int slot141(uint64_t base){for(unsigned i=0;i<MODULES141;++i)if(modules141[i].state&&(uint64_t)(uintptr_t)modules141[i].base==base)return (int)i;return -1;}
uint64_t pe8_main(void){return modules141[0].state?(uint64_t)(uintptr_t)modules141[0].base:0;}
uint64_t pe8_module(const char*name){for(unsigned i=0;i<MODULES141;++i)if(modules141[i].state&&!case8(modules141[i].name,basename141(name)))return (uint64_t)(uintptr_t)modules141[i].base;return 0;}
const char*pe8_path(uint64_t base){int i=slot141(base);return i<0?0:modules141[i].path;}
static void read141(int file,uint64_t size,uint64_t off,void*out,unsigned bytes){if(!range141(off,bytes,size)||seek8(file,(int64_t)off,0)!=(int64_t)off||read8(file,out,bytes)!=(int)bytes)fail8("The Windows image is truncated or could not be read.");}
static unsigned leaf141(const char*name){unsigned n=0;for(;name[n];++n)if(n>=95||name[n]=='/'||name[n]=='\\'||name[n]==':'||(unsigned char)name[n]<32)return 0;return n&&name[0]!='.';}
static unsigned candidate141(const char*folder,const char*name,char*out){
 copy8(out,folder,256);if(len8(out)+len8(name)+2>=256)return 0;append8(out,"/",256);append8(out,name,256);w8_file_info info;if(!stat8(out,&info))return info.kind==1;
 for(unsigned at=0;at<1024;){int64_t next=(int64_t)sys8(W8_SYS_ENUM,(uint64_t)folder,(uint64_t)&info,at,0,0);if(next<=0)break;at=(unsigned)next;if(info.kind==1&&!case8(info.name,name)){copy8(out,folder,256);append8(out,"/",256);append8(out,info.name,256);return 1;}}return 0;
}
#include "resource144.inc"
static uint64_t load141(const char*,unsigned);
static uint64_t dependency141(int owner,const char*name){
 if(owner<0||!leaf141(name))return 0;uint64_t found=pe8_module(name);
 if(!found){char folder[256],path[256];copy8(folder,modules141[owner].path,256);char*end=folder+len8(folder);while(end>folder&&end[-1]!='/')--end;if(end<=folder)return 0;end[-1]=0;
  if(!candidate141(folder,name,path)){copy8(folder,modules141[0].path,256);end=folder+len8(folder);while(end>folder&&end[-1]!='/')--end;if(end<=folder)return 0;end[-1]=0;if(!candidate141(folder,name,path))return 0;}
  found=load141(path,0);
 }
 int child=slot141(found);if(child>=0)modules141[owner].dependencies|=UINT32_C(1)<<(unsigned)child;return found;
}
static void*pe8_import_impl142(const char*dll,const char*name,unsigned ordinal){uint64_t module=dependency141(parent141,dll);return module?pe8_symbol(module,name,ordinal):0;}
static void*pe8_symbol_impl142(uint64_t base,const char*name,unsigned ordinal){
 int index=slot141(base);if(index<0)return 0;module141*m=modules141+index;if(!m->exports||m->export_size<40)return 0;
 uint8_t*e=rva141(m,m->exports,m->export_size);uint32_t first=u32(e+16),functions=u32(e+20),names=u32(e+24),selected=UINT32_MAX;
 if(functions>65536||names>65536)fail8("The Windows export table exceeds its bound.");
 if(ordinal){if(ordinal<first||ordinal-first>=functions)return 0;selected=ordinal-first;}
 else if(name){uint8_t*n=rva141(m,u32(e+32),(uint64_t)names*4),*o=rva141(m,u32(e+36),(uint64_t)names*2);for(unsigned i=0;i<names;++i)if(equal8(name141(m,u32(n+i*4)),name)){selected=u16(o+i*2);break;}}
 if(selected>=functions)return 0;uint32_t result=u32((uint8_t*)rva141(m,u32(e+28),(uint64_t)functions*4)+selected*4);if(!result)return 0;
 if(result>=m->exports&&result-m->exports<m->export_size){
  if(++forwarding141>32)fail8("The Windows export forwarder chain is cyclic or too deep.");const char*forward=name141(m,result);if(len8(forward)>=m->export_size-(result-m->exports))fail8("The Windows export forwarder is outside its directory.");
  char dll[96];unsigned n=0;while(forward[n]&&forward[n]!='.'&&n<80){dll[n]=forward[n];++n;}if(forward[n]!='.')fail8("The Windows export forwarder is malformed.");dll[n]=0;append8(dll,".dll",96);const char*symbol=forward+n+1;unsigned ord=0;
  if(*symbol=='#'){++symbol;if(!*symbol)fail8("The forwarded ordinal is empty.");for(;*symbol;++symbol){if(*symbol<'0'||*symbol>'9'||ord>6553)fail8("The forwarded ordinal is invalid.");ord=ord*10+(unsigned)(*symbol-'0');}if(!ord||ord>65535)fail8("The forwarded ordinal is invalid.");symbol=0;}
  int old=parent141;parent141=index;void*resolved=resolve8(dll,symbol,ord);parent141=old;--forwarding141;return resolved;
 }
 return rva141(m,result,1);
}
static unsigned imports141(module141*m,uint32_t address,uint32_t bytes,unsigned delay,unsigned bind){
 if(!address){if(bytes)fail8("The Windows import directory has no address.");return 0;}unsigned stride=delay?32:20,terminated=0,count=0;
 rva141(m,address,bytes);
 for(uint64_t off=0;off+stride<=bytes;off+=stride){uint8_t*d=rva141(m,(uint64_t)address+off,stride);unsigned any=0;for(unsigned i=0;i<stride;i+=4)any|=u32(d+i);if(!any){terminated=1;break;}
  uint32_t name=delay?u32(d+4):u32(d+12),iat=delay?u32(d+12):u32(d+16),lookup=delay?u32(d+16):u32(d);if(delay&&u32(d)!=1)fail8("Unsupported Windows delay-import address format.");if(!lookup&&!delay)lookup=iat;if(!lookup||!iat)fail8("The Windows import arrays are missing.");const char*dll=name141(m,name);if(!leaf141(dll))fail8("The Windows import DLL name is invalid.");
  if(delay){if(u32(d+8))rva141(m,u32(d+8),8);if(u32(d+20))rva141(m,u32(d+20),8);if(u32(d+24))rva141(m,u32(d+24),8);}
  unsigned ended=0;for(unsigned i=0;i<4096;++i){uint64_t thunk=u64(rva141(m,(uint64_t)lookup+(uint64_t)i*8,8));rva141(m,(uint64_t)iat+(uint64_t)i*8,8);if(!thunk){ended=1;break;}
   unsigned ordinal=0;const char*symbol=0;if(thunk>>63){if(thunk&UINT64_C(0x7fffffffffff0000))fail8("The Windows ordinal import is invalid.");ordinal=(unsigned)(thunk&65535);if(!ordinal)fail8("The Windows ordinal import is zero.");}else{if(thunk>UINT32_MAX-2)fail8("The Windows name import is invalid.");rva141(m,thunk,2);symbol=name141(m,thunk+2);}
   ++count;if(bind&&!delay){void*fn=resolve8(dll,symbol,ordinal);if(!fn){print8("Unsupported import: ");print8(dll);print8("!");if(symbol)print8(symbol);else number8(ordinal);print8("\n");fail8("A required Windows function is not available yet.");}*(uint64_t*)rva141(m,(uint64_t)iat+(uint64_t)i*8,8)=(uint64_t)(uintptr_t)fn;}
  }if(!ended)fail8("The Windows import array is not terminated.");
 }if(!terminated)fail8("The Windows import directory is not terminated.");return count;
}
static uint64_t address141(uint32_t size){uint64_t at=ARENA141;for(unsigned pass=0;pass<=MODULES141;++pass){unsigned overlap=0;for(unsigned i=0;i<MODULES141;++i){module141*m=modules141+i;if(!m->state)continue;uint64_t start=(uint64_t)(uintptr_t)m->base,end=start+((m->size+65535u)&~UINT64_C(65535))+65536;if(at<end&&start<at+size+65536){at=(end+65535)&~UINT64_C(65535);overlap=1;break;}}if(!overlap){if(at>=W8_HEAP||size+UINT64_C(65536)>W8_HEAP-at)break;return at;}}fail8("The Windows image address-space quota was reached.");}
#include "tls142.inc"
static void attach141(unsigned index){module141*m=modules141+index;if(!m->state||m->attached)return;m->attached=1;for(unsigned i=0;i<MODULES141;++i)if(m->dependencies&(UINT32_C(1)<<i))attach141(i);tls_notify_impl142(m,1);if(m->dll&&m->entry){if(!((int(MS*)(void*,unsigned,void*))(m->base+m->entry))(m->base,1,0))fail8("The Windows DLL rejected process attachment.");}m->sequence=++sequence141;}
static uint64_t load141(const char*path,unsigned external){
 const char*name=basename141(path);if(!leaf141(name)||len8(path)>=256)fail8("The Windows module path exceeds its bound.");
 for(unsigned i=0;i<MODULES141;++i)if(modules141[i].state&&!case8(modules141[i].name,name)){if(case8(modules141[i].path,path))fail8("A DLL with this name is already loaded from another folder.");if(external){if(modules141[i].references==UINT32_MAX)fail8("The Windows module reference quota was reached.");++modules141[i].references;}return (uint64_t)(uintptr_t)modules141[i].base;}
 unsigned index=0;while(index<MODULES141&&modules141[index].state)++index;if(index==MODULES141)fail8("The Windows module quota of 32 was reached.");
 w8_file_info info;if(stat8(path,&info)||info.kind!=1||info.size<64||info.size>IMAGE141_LIMIT)fail8("The Windows image cannot be read or exceeds the 32 MiB file quota.");int file=open8(path,0);if(file<0)fail8("The Windows image could not be opened.");
 uint8_t dos[64],header[24],optional[512],sections[32][40];read141(file,info.size,0,dos,64);uint32_t offset=u32(dos+60);read141(file,info.size,offset,header,24);
 if(u16(dos)!=0x5a4d||u32(header)!=0x4550||u16(header+4)!=0x8664)fail8("Choose a Windows x64 file. Windows x86 and ARM64 require separate support.");
 unsigned number=u16(header+6),options=u16(header+20);if(!number||number>32||options<240||options>sizeof(optional))fail8("The Windows image has an unsupported section/header count.");read141(file,info.size,(uint64_t)offset+24,optional,options);
 if(u16(optional)!=0x20b||u32(optional+32)!=4096||u32(optional+108)<16)fail8("The Windows image is not a supported PE32+ layout.");
 for(unsigned directory=0;directory<16;++directory){uint32_t rva=u32(optional+112+directory*8),bytes=u32(optional+116+directory*8);if(!rva&&bytes)fail8("The Windows data directory has no address.");if(rva&&bytes&&!range141(rva,bytes,directory==4?info.size:u32(optional+56)))fail8("The Windows data directory is outside its image or file.");}
 if(!inspect141&&index==0&&((u16(header+22)&0x2000)||(u16(optional+68)!=3&&u16(optional+68)!=2)))fail8("This Windows executable subsystem is not supported. The app was not started.");
 uint32_t size=u32(optional+56),headers=u32(optional+60),entry=u32(optional+16);if(!size||(size&4095)||size>IMAGE141_LIMIT||headers>info.size||headers>size||headers<(uint64_t)offset+24+options+(uint64_t)number*40||entry>=size)fail8("The Windows image size, headers or entry point are invalid.");
 read141(file,info.size,(uint64_t)offset+24+options,sections,number*40);uint32_t previous=(headers+4095u)&~4095u;
 for(unsigned i=0;i<number;++i){uint8_t*s=sections[i];uint32_t raw=u32(s+16),span=u32(s+8)>raw?u32(s+8):raw,rva=u32(s+12),flags=u32(s+36);if(!span)continue;if((rva&4095)||rva<previous||!range141(rva,span,size)||!range141(u32(s+20),raw,info.size)||((flags&0xa0000000u)==0xa0000000u))fail8("The Windows image has overlapping, writable-executable or invalid sections.");previous=(rva+span+4095u)&~4095u;}
 uint64_t address=address141(size);if(sys8(W8_SYS_RESERVE,address,size,3,0,0))fail8("The Windows image could not reserve its bounded address range.");module141*m=modules141+index;memset(m,0,sizeof(*m));m->base=(void*)(uintptr_t)address;m->size=size;m->entry=entry;m->state=1;m->dll=(u16(header+22)&0x2000)!=0;m->subsystem=u16(optional+68);m->references=external;if(module_generation144==UINT32_MAX)fail8("The Windows module generation quota was reached.");m->generation=++module_generation144;m->resources=u32(optional+128);m->resource_bytes=u32(optional+132);copy8(m->name,name,96);copy8(m->path,path,256);++loading141;
 uint32_t fingerprint=2166136261u;read141(file,info.size,0,m->base,headers);for(unsigned j=0;j<headers;++j)fingerprint=(fingerprint^m->base[j])*16777619u;
 for(unsigned i=0;i<number;++i){uint8_t*s=sections[i];uint32_t raw=u32(s+16),rva=u32(s+12);if(raw){read141(file,info.size,u32(s+20),m->base+rva,raw);for(unsigned j=0;j<raw;++j)fingerprint=(fingerprint^m->base[rva+j])*16777619u;}}
 close8(file);print8(len8(path)>=sizeof("/System/Windows/Installer/")-1&&!memcmp(path,"/System/Windows/Installer/",sizeof("/System/Windows/Installer/")-1)?"Mapped Engacer service image: ":"Mapped original image: ");print8(name);print8(" bytes=");number8(size);print8(" source-fnv32=");number8(fingerprint);print8("\n");
 uint64_t delta=address-u64(optional+24);uint32_t reloc=u32(optional+152),reloc_size=u32(optional+156);
 if(delta){if(!reloc||!reloc_size)fail8("The Windows image has no usable relocation directory.");rva141(m,reloc,reloc_size);uint64_t off=0;while(off<reloc_size){uint8_t*b=rva141(m,(uint64_t)reloc+off,8);uint32_t page=u32(b),bytes=u32(b+4);if(bytes<8||(bytes&1)||bytes>reloc_size-off)fail8("The Windows relocation block is invalid.");b=rva141(m,(uint64_t)reloc+off,bytes);for(unsigned j=8;j<bytes;j+=2){unsigned item=u16(b+j),type=item>>12;if(!type)continue;if(type!=10)fail8("The Windows relocation type is unsupported.");uint64_t*p=rva141(m,(uint64_t)page+(item&4095),8);*p+=delta;}off+=bytes;}}
 m->unwind_rva=u32(optional+136);m->unwind_bytes=u32(optional+140);if(m->unwind_bytes%12||m->unwind_bytes/12>262144)fail8("The Windows exception directory exceeds the supported table layout.");
 uint32_t unwind_end142=0;for(unsigned at=0;at<m->unwind_bytes;at+=12){uint8_t*function=rva141(m,(uint64_t)m->unwind_rva+at,12);uint32_t begin=u32(function),end=u32(function+4),data=u32(function+8);if(begin<unwind_end142||begin>=end||end>m->size||(data&3)||!range141(data,4,m->size))fail8("The Windows runtime-function table is not ordered or contains invalid ranges.");unwind_end142=end;}
 m->exports=u32(optional+112);m->export_size=u32(optional+116);if(m->exports)rva141(m,m->exports,m->export_size);else if(m->export_size)fail8("The Windows export directory has no address.");
 int old=parent141;parent141=(int)index;unsigned direct=imports141(m,u32(optional+120),u32(optional+124),0,!inspect141),delayed=imports141(m,u32(optional+216),u32(optional+220),1,0);parent141=old;
 if(!inspect141)tls_prepare142(m,index,u32(optional+184),u32(optional+188));
 if(sys8(W8_SYS_PROTECT,address,size,1,0,0))fail8("The Windows image could not receive final read-only protection.");
 unsigned executable_entry=entry==0;for(unsigned i=0;i<number;++i){uint8_t*s=sections[i];uint32_t raw=u32(s+16),span=u32(s+8)>raw?u32(s+8):raw,rva=u32(s+12),flags=u32(s+36);if(!span)continue;unsigned permissions=(flags&0x20000000u)?5:(flags&0x80000000u)?3:1;if(entry>=rva&&(uint64_t)entry<rva+span&&(permissions&4))executable_entry=1;if(sys8(W8_SYS_PROTECT,address+rva,(span+4095u)&~4095u,permissions,0,0))fail8("The Windows section permissions could not be applied.");}
 if(!executable_entry)fail8("The Windows entry point is not in an executable section.");m->state=2;--loading141;
 if(inspect141){print8("Inspection only: direct imports=");number8(direct);print8(" delayed imports=");number8(delayed);print8(" static TLS=");number8(u32(optional+184)!=0);print8(". No app code was executed.\n");}
 else if(!loading141)attach141(index);return address;
}
static unsigned terminating142;
#include "lifetime142.inc"
NORETURN void pe8_exit(unsigned code){lock_enter142(&loader_lock142);sys8(W8_SYS_QUIESCE,code,0,0,0,0);
#ifdef ENGINE_M14
fls_thread_exit147();
#endif
pe8_shutdown();exit8(code);}
static uint64_t pe8_load_impl142(const char*path){return terminating142?0:load141(path,1);}
static uint64_t pe8_named_impl142(const char*name){
 if(terminating142||!leaf141(name))return 0;uint64_t loaded=pe8_module(name);if(loaded)return load141(pe8_path(loaded),1);
 char folder[256],path[256];if(!modules141[0].state)return 0;copy8(folder,modules141[0].path,256);char*end=folder+len8(folder);while(end>folder&&end[-1]!='/')--end;if(end<=folder)return 0;end[-1]=0;
 return candidate141(folder,name,path)?load141(path,1):0;
}
static int pe8_release_impl142(uint64_t base){if(terminating142)return 0;int index=slot141(base);if(index<=0||!modules141[index].references)return 0;--modules141[index].references;uint32_t reachable=1;for(unsigned i=1;i<MODULES141;++i)if(modules141[i].state&&modules141[i].references)reachable|=UINT32_C(1)<<i;
 for(unsigned pass=0;pass<MODULES141;++pass){uint32_t next=reachable;for(unsigned i=0;i<MODULES141;++i)if(reachable&(UINT32_C(1)<<i))next|=modules141[i].dependencies;if(next==reachable)break;reachable=next;}
 for(unsigned pass=0;pass<MODULES141;++pass){int chosen=-1;for(unsigned i=1;i<MODULES141;++i)if(modules141[i].state&&!(reachable&(UINT32_C(1)<<i))&&(chosen<0||modules141[i].sequence>modules141[chosen].sequence))chosen=(int)i;if(chosen<0)break;module141*m=modules141+chosen;if(m->attached)tls_notify_impl142(m,0);if(m->attached&&m->dll&&m->entry)(void)((int(MS*)(void*,unsigned,void*))(m->base+m->entry))(m->base,0,0);tls_release_module142((unsigned)chosen);resource_release144((uint64_t)(uintptr_t)m->base);if(sys8(W8_SYS_UNMAP,(uint64_t)(uintptr_t)m->base,m->size,0,0,0))fail8("The Windows module could not be released.");for(unsigned i=0;i<MODULES141;++i)modules141[i].dependencies&=~(UINT32_C(1)<<chosen);memset(m,0,sizeof(*m));}return 1;
}
void pe8_inspect(const char*path){inspect141=1;pe8_load(path);uint64_t values[4];if(sys8(W8_SYS_VMINFO,(uint64_t)values,0,0,0,0))fail8("The Windows memory observation could not be read.");print8("Memory pages: reserved=");number8(values[0]);print8(" owned=");number8(values[1]);print8(" demand-commits=");number8(values[2]);print8(" physical-quota=");number8(values[3]);print8("\nMapping inspection completed. Running this app is a separate compatibility test.\n");exit8(0);}
void pe8_run(const char*path,const char*arguments){(void)arguments;uint64_t base=pe8_load(path);module141*m=modules141;if(m->dll||(m->subsystem!=3&&m->subsystem!=2))fail8("This Windows executable subsystem is not supported. The app was not started.");print8(equal8(path,"/System/Windows/Installer/msiexec.exe")?"Running the native Engacer MSI service in a protected process.\n\n":"Running the original Windows executable in a protected process.\n\n");((void(MS*)(void))(uintptr_t)(base+m->entry))();pe8_exit(0);}

uint64_t pe8_load(const char*path){lock_enter142(&loader_lock142);uint64_t result=pe8_load_impl142(path);lock_leave142(&loader_lock142);return result;}
uint64_t pe8_named(const char*name){lock_enter142(&loader_lock142);uint64_t result=pe8_named_impl142(name);lock_leave142(&loader_lock142);return result;}
int pe8_release(uint64_t base){lock_enter142(&loader_lock142);int result=pe8_release_impl142(base);lock_leave142(&loader_lock142);return result;}

void*pe8_import(const char*dll,const char*name,unsigned ordinal){lock_enter142(&loader_lock142);void*result=pe8_import_impl142(dll,name,ordinal);lock_leave142(&loader_lock142);return result;}
void*pe8_symbol(uint64_t base,const char*name,unsigned ordinal){lock_enter142(&loader_lock142);void*result=pe8_symbol_impl142(base,name,ordinal);lock_leave142(&loader_lock142);return result;}

#include "unwind142.inc"

/* The loader lock keeps the matching image alive across the atomic kernel change. */
int64_t pe8_protect145(uint64_t address,uint64_t bytes,unsigned permissions,uint64_t old){
 lock_enter142(&loader_lock142);int64_t result=-487;
 for(unsigned n=0;n<MODULES141;++n){module141*m=modules141+n;uint64_t base=(uint64_t)(uintptr_t)m->base;if(m->state>=2&&address>=base&&address-base<m->size&&bytes<=m->size-(address-base)){result=(int64_t)sys8(W8_SYS_PAGE145,address,bytes,permissions,old,0);break;}}
 lock_leave142(&loader_lock142);return result;
}
