#include <engine/windows8.h>
#include <engine/install/m6.h>
#include <engine/elf.h>
#include <engine/m3.h>
#include <engine/sha256.h>
#ifdef ENGINE_M14
#include <engine/winproduct147.h>
#include <engine/wintxn147.h>
#include <engine/winexe148.h>
#define ENGINE_EXE_BROKER148 1
static unsigned installer_user_grant147(const char*,unsigned);
static unsigned exe_user_grant148(const char*,unsigned);
static unsigned exe_admit148(unsigned,const uint8_t*);
static unsigned exe_hash_file148(const char*,uint64_t,const char*);
#endif
extern void *memmove(void*,const void*,size_t);
#define NX (UINT64_C(1)<<63)
#define RESERVED141 UINT64_C(0x200)
#define VIRTUAL141_PAGES 32768u
#define OWN8 10000u
#define WRITE8_PAGES 2048u
#define TRAP8 (KERNEL_STACK+0x80000)
typedef struct {char path[256];uint64_t position,size;unsigned live,write,object,access,share,generation,legacy;} file8;
#define THREADS142 16u
#define THREAD_STACK142(i) (UINT64_C(0x104000000)+(uint64_t)(i)*0x200000)
#define THREAD_TEB142(i) (W8_TEB+(uint64_t)(i)*0x10000)
enum {T142_FREE,T142_READY,T142_SLEEP,T142_PARK,T142_SUSPENDED,T142_EXITED,T142_OBJECT,T143_FILELOCK,T144_GUI,T147_PIPE};
typedef struct {
 trap_frame frame;_Alignas(16) uint8_t fx[512];
 uint64_t deadline,address,teb,low,top;
 unsigned state,generation,code,closed,exiting,exception_depth;
 uint64_t exception_stack,exception_packets[4],wait_handles[32];unsigned wait_count,wait_all;
} thread142;
typedef struct {unsigned live,generation,object,kind,access;} process_handle142;
typedef struct {unsigned live,generation,object,access;} sync_cap142;
typedef struct {unsigned live,generation,object,access;} registry_cap143;
typedef struct {unsigned used,pid,live,code,primary_id,primary_done,primary_code,refs,slot,parent_pid;} process_object142;
typedef struct {
 uint64_t owned[OWN8],cr3,pd,entry,virtual_pages,lazy_faults;
 unsigned count,cancel,created_root,current,cursor,object;
#ifdef ENGINE_M14
 unsigned install_authority147,exe_context148,image_pin148,exe_child_error148;
 char app_id1410[39];
 char named_owner1410[256];
#endif
 process_handle142 handles[32];sync_cap142 sync_handles[64];registry_cap143 registry_handles[32];
 uint64_t exception_entry,wait_epoch;file8 files[32];thread142 threads[THREADS142];w8_mailbox input;char image_name148[64];
 _Alignas(16) w8_info child_info;
} private_space142;
#define SPACES142 4u
#define META_PAGES142 48u
#define META_BASE142(i) (KERNEL_STACK+0x100000+(uint64_t)(i)*0x30000)
_Static_assert(offsetof(private_space142,child_info)+sizeof(w8_info)==sizeof(private_space142),"Child output must remain the optional metadata tail");
_Static_assert(sizeof(private_space142)<=META_PAGES142*4096,"Windows metadata exceeds its bounded kernel slab");
static private_space142 *spaces142[SPACES142];
static uint64_t metadata_backing142[SPACES142][META_PAGES142];
static unsigned metadata_pages142[SPACES142],active_space142,generation142;
static process_object142 process_objects142[32];
static unsigned process_id142=8,process_handle_generation142,space_cursor142,root_terminal142,root_waiting142;
static char root_end_message142[192];
static unsigned ready8,quantum8;
static trap_frame context8;static _Alignas(16) uint8_t fx8[512];static uint8_t pic8;
static uint64_t old_gs8;static w8_info info8;static w8_info*const root_info142=&info8;static uint8_t io8[4096];
#define info8 (*(active_space142?&spaces142[active_space142]->child_info:root_info142))
extern void timer_claim142(unsigned,unsigned);
static unsigned timer_needed142,sync_resident142,file_resident143,registry_resident143,ui_resident144,clipboard_resident144,mapping_resident146,pipe_resident147,exe_resident148;
static void refresh_sync_waits142(void);
static unsigned sync_deadline_needed142(void);
static void release_sync_grants142(void);
#ifdef ENGINE_M14
static void mapping_release146(void);
static void pipe_release147(void);
static unsigned mapping_name_taken146(const uint16_t*);
#endif
volatile unsigned w8_active;
uint64_t w8_saved_rsp,w8_kernel_cr3;
#ifdef ENGINE_M14
static unsigned installer_authority147(void){return spaces142[active_space142]->install_authority147;}
static int equal8(const char*,const char*);
static unsigned exe_image_pinned148(const char*path){for(unsigned i=0;i<SPACES142;++i){private_space142*s=spaces142[i];if(s&&s->exe_context148&&s->image_pin148&&process_objects142[s->object].live&&s->image_pin148<=V6_ENTRIES&&equal8(path,m6_volume()->entries[s->image_pin148-1].path))return 1;}return 0;}
/* A reviewed image lease protects its actual table entry without a duplicate
 * installer cache or a larger resident table. Bind it only in the EXE broker. */
static unsigned exe_volume_guard148(v6_volume*volume,const char*path,const v6_entry*pending){
 if(volume!=m6_volume())return 0;
 for(unsigned i=0;i<SPACES142;++i){private_space142*s=spaces142[i];if(!s||!s->exe_context148||!s->image_pin148||!process_objects142[s->object].live)continue;
  unsigned index=s->image_pin148-1;if(index>=V6_ENTRIES||volume->entries[index].kind!=1)return V6_BUSY;
  if(pending){if(memcmp(volume->entries+index,pending+index,sizeof(v6_entry)))return V6_BUSY;}
  else if(!path||equal8(path,volume->entries[index].path))return V6_BUSY;
 }
 return 0;
}
#endif
#define created_root8 (spaces142[active_space142]->created_root)
#define owned8 (spaces142[active_space142]->owned)
#define cr3_8 (spaces142[active_space142]->cr3)
#define pd8 (spaces142[active_space142]->pd)
#define entry8 (spaces142[active_space142]->entry)
#define count8 (spaces142[active_space142]->count)
#define cancel8 (spaces142[active_space142]->cancel)
#define virtual_pages141 (spaces142[active_space142]->virtual_pages)
#define lazy_faults141 (spaces142[active_space142]->lazy_faults)
#define files8 (spaces142[active_space142]->files)
#define threads142 (spaces142[active_space142]->threads)
#define current142 (spaces142[active_space142]->current)
#define cursor142 (spaces142[active_space142]->cursor)
#define input8 (spaces142[active_space142]->input)

static uint64_t thread_token142(unsigned i){return UINT64_C(0x40000000)|((uint64_t)threads142[i].generation<<8)|i;}
static int thread_slot142(uint64_t token){unsigned i=(unsigned)(token&255);return i<THREADS142&&threads142[i].state&&!threads142[i].closed&&threads142[i].generation==((token&UINT64_C(0x3fffffff))>>8)&&(token&UINT64_C(0xffffffffc0000000))==UINT64_C(0x40000000)?(int)i:-1;}
static void save_thread142(void){threads142[current142].frame=context8;memcpy(threads142[current142].fx,fx8,512);}
static int choose_thread142(void){
 uint64_t now=m3_clock_ticks()*10;
 for(unsigned i=0;i<THREADS142;++i){thread142*t=threads142+i;if((t->state==T142_SLEEP||t->state==T142_PARK||t->state==T144_GUI)&&t->deadline!=UINT64_MAX&&now>=t->deadline){t->frame.rax=t->state==T142_PARK?258:0;t->state=T142_READY;}}
 for(unsigned n=0;n<THREADS142;++n){unsigned i=(cursor142+n)%THREADS142;if(threads142[i].state==T142_READY){current142=i;cursor142=(i+1)%THREADS142;context8=threads142[i].frame;memcpy(fx8,threads142[i].fx,512);return 1;}}
 return 0;
}
extern void w8_enter(trap_frame*,uint64_t);
extern NORETURN void w8_escape(void);
extern uint64_t kernel_entry_pt(void);
extern const char windows8_licenses[];
extern const uint8_t windows8_runtime_image[];extern const unsigned windows8_runtime_size;
#ifdef ENGINE_M14
#include <engine/winbundle147.h>
static const uint8_t *windows147_msi_image,*windows147_msiexec_image,*windows147_runtime_image,*windows147_xcopy_image,*windows147_cmd_image;
static unsigned windows147_msi_size,windows147_msiexec_size,windows147_runtime_size,windows147_xcopy_size,windows147_cmd_size;
#define windows8_runtime_image windows147_runtime_image
#define windows8_runtime_size windows147_runtime_size
unsigned w8_boot_services147(const winbundle147*b){uint8_t hash[32];if(!b||!b->dll||!b->exe||!b->runtime||!b->xcopy||!b->cmd)return 1;
 engine_sha256(b->dll,b->dll_size,hash);if(memcmp(hash,b->dll_hash,32))return 1;
 engine_sha256(b->exe,b->exe_size,hash);if(memcmp(hash,b->exe_hash,32))return 1;
 engine_sha256(b->runtime,b->runtime_size,hash);if(memcmp(hash,b->runtime_hash,32))return 1;
 engine_sha256(b->xcopy,b->xcopy_size,hash);if(memcmp(hash,b->xcopy_hash,32))return 1;
 engine_sha256(b->cmd,b->cmd_size,hash);if(memcmp(hash,b->cmd_hash,32))return 1;
 windows147_xcopy_image=b->xcopy;windows147_xcopy_size=b->xcopy_size;windows147_cmd_image=b->cmd;windows147_cmd_size=b->cmd_size;
 windows147_runtime_image=b->runtime;windows147_runtime_size=b->runtime_size;
 windows147_msi_image=b->dll;windows147_msi_size=b->dll_size;windows147_msiexec_image=b->exe;windows147_msiexec_size=b->exe_size;
 serial_text("M147_BOOT_SERVICE_DIGESTS_OK\n");return 0;}
#endif
static void group_peak142(void);
/* Shared supervisor-only upper-half pages; no idle allocation per process slot. */
static void free_space142(unsigned slot){
 uint64_t base=META_BASE142(slot),*pt=(void*)(uintptr_t)kernel_entry_pt();spaces142[slot]=0;
 while(metadata_pages142[slot]){unsigned i=--metadata_pages142[slot];uint64_t va=base+(uint64_t)i*4096;pt[((va>>12)&511)]=0;__asm__ volatile("invlpg (%0)"::"r"(va):"memory");page_free(metadata_backing142[slot][i]);metadata_backing142[slot][i]=0;}
}
static unsigned allocate_space142(unsigned slot){
 if(slot>=SPACES142||spaces142[slot])return 1;unsigned bytes=slot?sizeof(private_space142):offsetof(private_space142,child_info);unsigned pages=(bytes+4095)/4096;
 uint64_t base=META_BASE142(slot),*pt=(void*)(uintptr_t)kernel_entry_pt();
 for(unsigned i=0;i<pages;++i)if(pt[(((base>>12)+i)&511)])return 1;
 for(unsigned i=0;i<pages;++i){uint64_t physical=page_alloc();if(!physical){free_space142(slot);return 1;}metadata_backing142[slot][i]=physical;++metadata_pages142[slot];group_peak142();uint64_t va=base+(uint64_t)i*4096;pt[((va>>12)&511)]=physical|3|NX;__asm__ volatile("invlpg (%0)"::"r"(va):"memory");}
 spaces142[slot]=(void*)(uintptr_t)base;active_space142=slot;return 0;
}
static unsigned terminated142(const char*s,unsigned cap){for(unsigned i=0;i<cap;++i)if(!s[i])return 1;return 0;}
static unsigned length8(const char*s){unsigned n=0;while(s[n])++n;return n;}
static int equal8(const char*a,const char*b){while(*a&&*a==*b){++a;++b;}return *a==*b;}
static void copy8(char*out,const char*in,unsigned cap){unsigned n=0;while(n+1<cap&&in[n]){out[n]=in[n];++n;}out[n]=0;}
static int prefix8(const char*p,const char*root){unsigned n=length8(root);return n&&(!memcmp(p,root,n))&&(p[n]=='/'||!p[n]);}
static void group_peak142(void){uint64_t total=sync_resident142+file_resident143+registry_resident143+ui_resident144+clipboard_resident144+mapping_resident146+pipe_resident147+exe_resident148;for(unsigned i=0;i<SPACES142;++i){total+=metadata_pages142[i];if(spaces142[i])total+=spaces142[i]->count;}if(total>root_info142->peak_pages)root_info142->peak_pages=total;}
static void peak8(void){if((uint64_t)count8+metadata_pages142[active_space142]>info8.peak_pages)info8.peak_pages=(uint64_t)count8+metadata_pages142[active_space142];group_peak142();}
static uint64_t allocate8(void){if(count8==OWN8)return 0;uint64_t p=page_alloc();if(p)owned8[count8++]=p;peak8();return p;}
static uint64_t *pte8(uint64_t va,unsigned create){
 if(va<W8_BASE||va>=W8_LIMIT)return 0;uint64_t*pd=(void*)(uintptr_t)pd8;unsigned at=(unsigned)((va>>21)&511);uint64_t page=pd[at]&UINT64_C(0x000ffffffffff000);
 if(!page&&create){page=allocate8();if(!page)return 0;pd[at]=page|7;}return page?(uint64_t*)(uintptr_t)page+((va>>12)&511):0;
}
static void free_owned8(uint64_t page);
static unsigned reserve141(uint64_t va,uint64_t bytes,unsigned permissions,unsigned lazy){
 if(!bytes||(va&4095)||(bytes&4095)||va<W8_BASE||va>=W8_LIMIT||bytes>W8_LIMIT-va||bytes>32*1024*1024||(permissions!=1&&permissions!=3&&permissions!=5))return 1;
 if(bytes/4096>VIRTUAL141_PAGES-virtual_pages141)return 1;
 for(uint64_t at=va;at<va+bytes;at+=4096){uint64_t*p=pte8(at,1);if(!p||*p)return 1;}
 uint64_t end=va;for(;end<va+bytes;end+=4096){uint64_t*p=pte8(end,0),physical=lazy?0:allocate8();if(!lazy&&!physical)break;*p=physical|(lazy?RESERVED141|4:5)|((permissions&2)?2:0)|((permissions&4)?0:NX);}
 if(end<va+bytes){for(uint64_t at=va;at<end;at+=4096){uint64_t*p=pte8(at,0);if(*p&1)free_owned8(*p&UINT64_C(0x000ffffffffff000));*p=0;}return 1;}
 virtual_pages141+=bytes/4096;
 return 0;
}
static unsigned map8(uint64_t va,uint64_t bytes,unsigned permissions){return reserve141(va,bytes,permissions,0);}
static unsigned commit141(uint64_t va,unsigned write,unsigned execute){
 uint64_t*p=pte8(va,0);if(!p||(*p&1)||!(*p&RESERVED141)||(write&&!(*p&2))||(execute&&(*p&NX)))return 1;
 uint64_t physical=allocate8();if(!physical)return 1;*p=physical|(*p&(NX|6))|1;++lazy_faults141;__asm__ volatile("invlpg (%0)"::"r"(va):"memory");return 0;
}
static unsigned user8(uint64_t va,void*buffer,unsigned bytes,unsigned to_user){
 if(va<W8_BASE||va>=W8_LIMIT||bytes>W8_LIMIT-va)return 1;uint8_t*b=buffer;
 while(bytes){uint64_t*p=pte8(va,0);if(p&&!(*p&1)&&(*p&RESERVED141)&&commit141(va,to_user,0))return 1;if(!p||!(*p&1)||(to_user&&!(*p&2)))return 1;unsigned n=4096-(unsigned)(va&4095);if(n>bytes)n=bytes;void*physical=(void*)(uintptr_t)((*p&UINT64_C(0x000ffffffffff000))+(va&4095));
  if(to_user)memcpy(physical,b,n);else memcpy(b,physical,n);b+=n;va+=n;bytes-=n;}return 0;
}
static unsigned string8(uint64_t va,char*out,unsigned cap){for(unsigned i=0;i<cap;++i){if(user8(va+i,out+i,1,0))return 1;if(!out[i])return 0;}return 1;}
#include "path-access147.inc"
static const v6_entry *find8(const char*p){v6_volume*v=m6_volume();if(!v)return 0;for(unsigned i=0;i<V6_ENTRIES;++i)if(v->entries[i].kind&&equal8(v->entries[i].path,p))return v->entries+i;return 0;}
#include "path143.inc"
static unsigned exact8(const char*p,uint64_t off,void*out,unsigned n){unsigned got=0;return v6_read(m6_volume(),p,off,out,n,&got)||got!=n;}
static unsigned memory_source8(void*c,uint64_t off,void*out,unsigned n){memcpy(out,(uint8_t*)c+off,n);return 0;}
static uint64_t now8(void);
#include "protected143.inc"
#include "metadata143.inc"
static const uint8_t *boot_package8;static unsigned boot_package_size8;
unsigned w8_boot_package(const void*p,unsigned bytes){static const uint8_t expected[]={0x6d,0xc8,0x22,0x56,0x9e,0x77,0x7d,0x9a,0x3e,0xcd,0x5f,0xfc,0xbc,0x22,0xb5,0x56,0x00,0xaf,0x87,0xe6,0xc5,0xd9,0x81,0x0a,0x64,0xe8,0x56,0x6c,0xf5,0xa4,0xaf,0x9f};uint8_t hash[32];if(bytes!=2003456)return 1;engine_sha256(p,bytes,hash);if(memcmp(hash,expected,32))return 1;boot_package8=p;boot_package_size8=bytes;serial_text("M8_BOOT_MSI_DIGEST_OK\n");return 0;}
unsigned w8_distribute(void*opaque,const char*user){if(!boot_package8||!boot_package_size8)return V6_INVALID;char path[256];copy8(path,user,256);unsigned n=length8(path);if(n+27>=256)return V6_INVALID;memcpy(path+n,"/Downloads/7z2606-x64.msi",26);return v6_put(opaque,path,boot_package_size8,memory_source8,(void*)boot_package8);}
unsigned w8_install_runtime(void*opaque){
 v6_volume*v=opaque;unsigned parent=v6_mkdir(v,"/Applications/Windows");if(parent&&parent!=V6_EXISTS)return parent;unsigned s=v6_mkdir(v,"/System/Windows");if(s&&s!=V6_EXISTS)return s;if(!windows8_runtime_size)return V6_INVALID;
 unsigned licenses=length8(windows8_licenses);if(v6_put(v,"/System/Licenses/Windows-runtime-LGPL.txt",licenses,memory_source8,(void*)windows8_licenses)||v6_put(v,"/System/Windows/runtime8.elf",windows8_runtime_size,memory_source8,(void*)windows8_runtime_image))return V6_IO;
#ifdef ENGINE_M14
 if(!windows147_xcopy_size||!windows147_cmd_size)return V6_INVALID;s=v6_mkdir(v,"/System/Windows/Tools");if(s&&s!=V6_EXISTS)return s;
 if(v6_put(v,"/System/Windows/Tools/xcopy.exe",windows147_xcopy_size,memory_source8,(void*)windows147_xcopy_image)||v6_put(v,"/System/Windows/Tools/cmd.exe",windows147_cmd_size,memory_source8,(void*)windows147_cmd_image))return V6_IO;
 if(!windows147_msi_size||!windows147_msiexec_size)return V6_INVALID;s=v6_mkdir(v,"/System/Windows/Installer");if(s&&s!=V6_EXISTS)return s;
 if(v6_put(v,"/System/Windows/Installer/msi.dll",windows147_msi_size,memory_source8,(void*)windows147_msi_image)||v6_put(v,"/System/Windows/Installer/msiexec.exe",windows147_msiexec_size,memory_source8,(void*)windows147_msiexec_image))return V6_IO;
#endif
 return 0;
}
static void output_record142(w8_info*record,const char*s,unsigned n){unsigned old=length8(record->output);if(n>W8_TEXT-1){s+=n-(W8_TEXT-1);n=W8_TEXT-1;}if(n>W8_TEXT-1-old){unsigned drop=n-(W8_TEXT-1-old);memmove(record->output,record->output+drop,old-drop);old-=drop;}memcpy(record->output+old,s,n);record->output[old+n]=0;++record->revision;}
static void output8(const char*s,unsigned n){output_record142(&info8,s,n);if(active_space142)output_record142(root_info142,s,n);}
#include "files143.inc"
static void snapshot8(void){w8_mailbox value;if(user8(W8_MAILBOX,&value,sizeof(value),0))return;
 info8.percent=value.percent<=100?value.percent:0;copy8(info8.product,value.product,sizeof(info8.product));copy8(info8.version,value.version,sizeof(info8.version));copy8(info8.publisher,value.publisher,sizeof(info8.publisher));copy8(info8.code,value.code,sizeof(info8.code));copy8(info8.message,value.message,sizeof(info8.message));info8.files=value.files;info8.total_bytes=value.total_bytes;
#ifdef ENGINE_M14
 memcpy(info8.source_sha147,value.source_sha147,32);info8.profile147=value.profile147&(W8_PROFILE_LEGACY147|W8_PROFILE_GENERIC147|W8_PROFILE_EXE148);info8.registry147=value.registry;info8.shortcuts147=value.shortcuts;info8.features147=value.features;
#endif
++info8.revision;serial_text("M8_PROGRESS percent=");serial_hex(info8.percent);serial_text(" ");serial_text(info8.message);serial_text("\n");}
static void finish8(unsigned status){snapshot8();info8.status=status;info8.state=status?3:2;
 for(unsigned i=0;i<32;++i)if(files8[i].live){unsigned error=close8(i,status?0:1);if(error){(void)close8(i,0);info8.status=error;info8.state=3;copy8(info8.message,"An open file could not be saved.",sizeof(info8.message));}}w8_active=0;w8_escape();}
static void release_grants142(void);
static void registry_release143(void);
#include "ui144.inc"
#ifdef ENGINE_M14
#include "stream147.inc"
#endif
static void release8(void){if(!spaces142[active_space142])return;ui_release144();release_sync_grants142();release_grants142();file_release143();registry_release143();
#ifdef ENGINE_M14
 stream_release147();mapping_release146();pipe_release147();
#endif
 while(count8)page_free(owned8[--count8]);free_space142(active_space142);}

static void reap_threads142(void){
 for(unsigned i=0;i<THREADS142;++i){thread142*t=threads142+i;if(t->state!=T142_EXITED)continue;ui_thread_release144(active_space142,i);
  if(t->teb){for(unsigned range=0;range<3;++range){uint64_t low=range==2?t->exception_stack:range?t->teb:t->low,top=range==2?(low?low+32768:0):range?t->teb+8192:t->top;
   for(uint64_t va=low;va<top;va+=4096){uint64_t*p=pte8(va,0);if(p&&(*p&(1|RESERVED141))){if(*p&1)free_owned8(*p&UINT64_C(0x000ffffffffff000));*p=0;--virtual_pages141;}}
  }t->teb=t->low=t->top=t->exception_stack=0;t->exception_depth=0;}
  if(i&&t->closed)memset(t,0,sizeof(*t));
 }
}
#ifdef ENGINE_M14
#include "transaction147.inc"
#endif
static unsigned rollback8(void){
#ifdef ENGINE_M14
 if(spaces142[active_space142]->exe_context148)return 2;
 if((input8.command==W8_INSTALL||input8.command==W8_REMOVE)&&transaction_pending147()){unsigned pending=transaction_keep147();if(pending)return pending;}
#endif
 if(!created_root8)return 0;
#ifdef ENGINE_M14
 unsigned keep=transaction_keep147();if(keep)return keep;
#endif
 v6_volume*v=m6_volume();
 char plan[256],product[256];copy8(plan,input8.product_root,256);copy8(product,input8.product_root,256);
 unsigned root_length=length8(input8.product_root);memcpy(plan+root_length,"/install.plan",14);memcpy(product+root_length,"/product.bin",13);
 for(unsigned pass=0;pass<V6_ENTRIES;++pass){const char*chosen=0;unsigned longest=0;
  for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*e=v->entries+i;if(e->kind&&prefix8(e->path,input8.product_root)&&!equal8(e->path,input8.product_root)&&!equal8(e->path,plan)&&!equal8(e->path,product)){unsigned n=length8(e->path);if(n>longest){chosen=e->path;longest=n;}}}
  if(!chosen){if(find8(product)&&v6_remove(v,product))return 1;if(find8(plan)&&v6_remove(v,plan))return 1;if(find8(input8.product_root)&&v6_remove(v,input8.product_root))return 1;created_root8=0;return 0;}
  char path[256];copy8(path,chosen,256);if(v6_remove(v,path))return 1;
 }return 1;
}
static unsigned prepare_transition8(void){if(ready8)return 0;uint64_t pages[4];unsigned count=0;for(;count<4;++count)if(!(pages[count]=page_alloc()))break;if(count<4){while(count)page_free(pages[--count]);return 1;}uint64_t*pt=(void*)(uintptr_t)kernel_entry_pt();for(unsigned i=0;i<4;++i)pt[((TRAP8>>12)&511)+i]=pages[i]|3|NX;ready8=1;return 0;}
#ifdef ENGINE_M14
/* Both strings come from the kernel launch request, outside the user mailbox. */
static void init_app_owner1410(private_space142 *space,const char *root,const char *user){
 char *out=space->named_owner1410;
 memcpy(space->app_id1410,root+sizeof(WIN_PRODUCT_BASE147)-1,sizeof(space->app_id1410));
 uint8_t digest[32];engine_sha256_context hash;
 static const char hex[]="0123456789abcdef";
 engine_sha256_init(&hash);
 engine_sha256_update(&hash,user,length8(user)+1);
 engine_sha256_update(&hash,space->app_id1410,sizeof(space->app_id1410));
 engine_sha256_final(&hash,digest);
 memset(out,0,sizeof(space->named_owner1410));
 for(unsigned i=0;i<32;++i){out[i*2]=hex[digest[i]>>4];out[i*2+1]=hex[digest[i]&15];}
}
#endif
static unsigned start_space142(unsigned command,const char*source,const char*root,const char*user,const char*arguments,unsigned slot,unsigned object,const w8_process_request*request,const private_space142*parent){
 if(parent){root=parent->input.product_root;user=parent->input.user_root;}
 if(slot>=SPACES142||spaces142[slot]||generation142>=0x3fffffu||command<1||command>W8_INSPECT||!source||!user||length8(source)>255||length8(user)>223||!prefix8(user,"/Users"))return V6_INVALID;
 active_space142=slot;if(allocate_space142(slot))goto failure;spaces142[slot]->object=object;memset(&info8,0,sizeof(info8));info8.peak_pages=metadata_pages142[slot];created_root8=0;memset(&input8,0,sizeof(input8));info8.state=1;info8.command=command;input8.magic=W8_MAGIC;input8.command=command;
 copy8(input8.source,source,256);copy8(input8.user_root,user,256);if(root)copy8(input8.product_root,root,256);if(arguments)copy8(input8.arguments,arguments,sizeof(input8.arguments));copy8(input8.windows_root,"C:\\Program Files\\7-Zip",256);input8.process_id=process_objects142[object].pid;info8.job_id147=input8.process_id;if(request){copy8(input8.startup_command,request->command,1200);copy8(input8.startup_directory,request->directory,256);input8.startup_flags=request->flags;}
#ifdef ENGINE_M14
 spaces142[slot]->install_authority147=parent?parent->install_authority147:(command==W8_INSTALL||command==W8_REMOVE);
 if(!win_product_root147(root))goto failure;
 if(parent){
  /* The caller's kernel space supplies both the path grant and object owner. */
  memcpy(spaces142[slot]->app_id1410,parent->app_id1410,sizeof(parent->app_id1410));
  memcpy(spaces142[slot]->named_owner1410,parent->named_owner1410,sizeof(parent->named_owner1410));
 }else init_app_owner1410(spaces142[slot],root,user);
#else
 if(!root||!equal8(root,"/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}"))goto failure;
#endif
 if(prepare_transition8())goto failure;cr3_8=allocate8();uint64_t pdpt=allocate8();pd8=allocate8();if(!cr3_8||!pdpt||!pd8)goto failure;
 ((uint64_t*)(uintptr_t)cr3_8)[0]=pdpt|7;((uint64_t*)(uintptr_t)cr3_8)[256]=kernel_stack_branch()|3;for(unsigned i=0;i<4;++i)((uint64_t*)(uintptr_t)pdpt)[i]=kernel_pd(i)|3;((uint64_t*)(uintptr_t)pdpt)[4]=pd8|7;
 elf_header header;if(v6_verify(m6_volume(),"/System/Windows/runtime8.elf")||exact8("/System/Windows/runtime8.elf",0,&header,sizeof(header))||memcmp(header.ident,"\177ELF\2\1\1",7)||header.machine!=62||header.type!=2||header.phnum>8||header.phentsize!=56)goto failure;
 unsigned executable=0;for(unsigned i=0;i<header.phnum;++i){elf_segment s;if(exact8("/System/Windows/runtime8.elf",header.phoff+i*56,&s,sizeof(s)))goto failure;if(s.type!=1||!s.memsz)continue;
  if(s.vaddr<W8_BASE||s.vaddr>=W8_BASE+0x100000||s.memsz>W8_BASE+0x100000-s.vaddr||s.filesz>s.memsz||s.filesz>0x100000||(s.vaddr&4095)||s.flags>6||(s.flags&3)==3)goto failure;
  unsigned pages=(unsigned)((s.memsz+4095)/4096);if(map8(s.vaddr,(uint64_t)pages*4096,3))goto failure;
  for(unsigned p=0;p<pages;++p){unsigned n=s.filesz>(uint64_t)p*4096?(unsigned)(s.filesz-(uint64_t)p*4096):0;if(n>4096)n=4096;uint64_t*leaf=pte8(s.vaddr+(uint64_t)p*4096,0);if(n&&exact8("/System/Windows/runtime8.elf",s.offset+(uint64_t)p*4096,(void*)(uintptr_t)(*leaf&UINT64_C(0x000ffffffffff000)),n))goto failure;*leaf=(*leaf&UINT64_C(0x000ffffffffff000))|5|((s.flags&2)?2:0)|((s.flags&1)?0:NX);}
  if((s.flags&1)&&header.entry>=s.vaddr&&header.entry<s.vaddr+s.filesz)executable=1;
 }
 if(!executable||map8(W8_MAILBOX,4096,3)||map8(W8_STACK_TOP-16384,16384,3)||map8(W8_TEB,8192,3))goto failure;
 if(user8(W8_MAILBOX,&input8,sizeof(input8),1))goto failure;
 uint64_t self=W8_TEB,stack=W8_STACK_TOP,limit=W8_STACK_LOW,pid=input8.process_id;if(user8(W8_TEB+0x40,&pid,8,1)||user8(W8_TEB+0x30,&self,8,1)||user8(W8_TEB+8,&stack,8,1)||user8(W8_TEB+16,&limit,8,1))goto failure;
 memset(&context8,0,sizeof(context8));context8.cs=0x1b;context8.ss=0x23;context8.rflags=0x202;context8.rip=header.entry;context8.rsp=W8_STACK_TOP-8;entry8=header.entry;
 memset(fx8,0,sizeof(fx8));*(uint16_t*)fx8=0x37f;*(uint32_t*)(fx8+24)=0x1f80;cancel8=0;

 threads142[0].state=request&&(request->flags&4)?T142_SUSPENDED:T142_READY;threads142[0].generation=++generation142;
 threads142[0].teb=W8_TEB;threads142[0].low=W8_STACK_LOW;threads142[0].top=W8_STACK_TOP;
 current142=cursor142=0;save_thread142();
 {uint64_t id=thread_token142(0);if(user8(W8_TEB+0x48,&id,8,1))goto failure;}
 process_objects142[object].live=1;process_objects142[object].slot=slot;process_objects142[object].primary_id=(unsigned)thread_token142(0);
 serial_text(slot?"M142_CHILD_CREATED command=":"M8_CPL3_CREATED command=");serial_hex(command);serial_text(" pid=");serial_hex(input8.process_id);serial_text("\n");return 0;
 failure:release8();if(!slot){root_info142->state=3;root_info142->status=1;copy8(root_info142->message,"The protected Windows runtime could not be loaded.",sizeof(root_info142->message));++root_info142->revision;}return V6_INVALID;
}
#ifdef ENGINE_M14
#include "pipe147.inc"
#endif
#include "process142.inc"
#ifdef ENGINE_M14
#define W8_NAMED_OWNER (spaces142[active_space142]->named_owner1410)
#endif
#include "sync142.inc"
#ifdef ENGINE_M14
#include "mapping146.inc"
#endif
unsigned w8_pending(void){for(unsigned i=0;i<SPACES142;++i)if(spaces142[i])return 1;return 0;}
unsigned w8_runnable(void){
 refresh_sync_waits142();unsigned runnable=0,needed=sync_deadline_needed142();uint64_t now=m3_clock_ticks()*10;
 for(unsigned p=0;p<SPACES142;++p)if(spaces142[p])for(unsigned i=0;i<THREADS142;++i){thread142*t=spaces142[p]->threads+i;if(t->state==T142_READY)runnable=1;if((t->state==T142_SLEEP||t->state==T142_PARK||t->state==T144_GUI)&&t->deadline!=UINT64_MAX){needed=1;if(now>=t->deadline)runnable=1;}}
 timer_needed142=needed;timer_claim142(1,needed);return runnable;
}
unsigned w8_clock_event142(void){return timer_needed142;}
const w8_info *w8_current(void){return root_info142;}
void w8_pump(void){
 if(!w8_pending()||!choose_space142())return;uint64_t flags;__asm__ volatile("pushfq; popq %0; cli":"=r"(flags)::"memory");__asm__ volatile("movq %%cr3,%0":"=r"(w8_kernel_cr3));
 uint32_t lo,hi;__asm__ volatile("rdmsr":"=a"(lo),"=d"(hi):"c"(0xc0000101u));old_gs8=((uint64_t)hi<<32)|lo;__asm__ volatile("wrmsr"::"a"((uint32_t)threads142[current142].teb),"d"((uint32_t)(threads142[current142].teb>>32)),"c"(0xc0000101u));
 pic8=in8(0x21);out8(0x21,pic8&~1u);interrupts_set_kernel_stack(TRAP8+16384);quantum8=0;w8_active=1;
 __asm__ volatile("fxrstor64 %0"::"m"(fx8):"memory");w8_enter(&context8,cr3_8);__asm__ volatile("fxsave64 %0":"=m"(fx8)::"memory");save_thread142();
 __asm__ volatile("wrmsr"::"a"((uint32_t)old_gs8),"d"((uint32_t)(old_gs8>>32)),"c"(0xc0000101u));out8(0x21,pic8);interrupts_set_kernel_stack(KERNEL_STACK_TOP);if(flags&512)__asm__ volatile("sti":::"memory");
 if(active_space142)++info8.quanta;++root_info142->quanta;peak8();
 if(info8.state!=1){unsigned code=info8.status,slot=active_space142;if(info8.status&&created_root8){unsigned cleanup=rollback8();copy8(info8.message,cleanup==2?"Installation stopped. Its transaction was kept; choose Recover / remove.":cleanup==3?"The recovery record needs inspection. Files were kept; no automatic rollback was performed.":cleanup?"Installation stopped and cleanup was interrupted; use Recover / remove.":"Installation stopped. Its new files were removed. Restore resources, then choose Install again.",sizeof(info8.message));}end_space142(slot,code);}

}

#include <engine/network/clock.h>
#ifdef ENGINE_M14
/* One worker CPU serializes this shared wall-clock anchor across app lifetimes. */
static uint64_t utc_filetime148,utc_microseconds148;
static uint64_t now8(void){
 if(!utc_filetime148){uint64_t began=m3_clock_microseconds();clock7_time t;
  for(unsigned attempt=0;attempt<64;++attempt){
   if(!clock7_read(&t)&&t.days>=584754){utc_filetime148=(((uint64_t)t.days-584754)*86400+t.seconds)*UINT64_C(10000000);utc_microseconds148=m3_clock_microseconds();break;}
   if(m3_clock_microseconds()-began>=5000)break;__asm__ volatile("pause");
  }
  if(!utc_filetime148)return 0;
 }
 uint64_t current=m3_clock_microseconds();if(current<utc_microseconds148)return 0;uint64_t elapsed=current-utc_microseconds148;
 if(elapsed>(UINT64_MAX-utc_filetime148)/10)return 0;return utc_filetime148+elapsed*10;
}
#else
static uint64_t now8(void){clock7_time t;if(clock7_read(&t)||t.days<584754)return 0;return (((uint64_t)t.days-584754)*86400+t.seconds)*UINT64_C(10000000);}
#endif
static unsigned information8(const v6_entry*entry,w8_file_info*out){
 memset(out,0,sizeof(*out));out->size=entry->size;out->crc=entry->crc;out->kind=entry->kind;out->identity=(uint64_t)(entry-m6_volume()->entries)+1;
 file_metadata143 metadata;unsigned object=file_object_slot143(entry->path),error=0;if(object<FILE_OBJECTS143){metadata=file_objects143[object]->metadata;out->size=file_objects143[object]->size;}else error=metadata_load143(entry->path,entry->kind,&metadata);if(error)return error;
 out->attributes=metadata.attributes;memcpy(out->time,metadata.times,sizeof(out->time));
 const char*name=entry->path;for(unsigned i=0;entry->path[i];++i)if(entry->path[i]=='/')name=entry->path+i+1;copy8(out->name,name,256);return 0;
}
#include "registry143.inc"
#ifdef ENGINE_M14
#include "exe-broker148.inc"
#endif
static void free_owned8(uint64_t page){for(unsigned i=0;i<count8;++i)if(owned8[i]==page){owned8[i]=owned8[--count8];page_free(page);return;}}
#include "exception142.inc"
static int64_t dispatch8(trap_frame*f){
 uint64_t a=f->rdi,b=f->rsi,c=f->rdx,d=f->r10,e=f->r8;char path[256];
 switch(f->rax){
 case W8_SYS_UI144:return ui_syscall144(a,b,c,d,e,f);
#ifdef ENGINE_M14
 case W8_SYS_MAPPING146:return e?-87:mapping_call146(a,b,c,d);
 case W8_SYS_PIPE147:return e?-87:pipe_call147(a,b,c,d,f);
 case W8_SYS_ALIAS147:return alias_set147(a,b,c,d,e);
 case W8_SYS_STREAM147:return stream_call147(a,b,c,d,e);
#endif
 case W8_SYS_PATH143:return e?-87:path_syscall143(a,b,c,d);
 case W8_SYS_REGISTRY143:return c||d||e?-87:registry_syscall143(a,b);
 case W8_SYS_TEXT143:if(d||e)return -87;if(a==1)return text_compare143(b,c);if(a==2)return text_find143(b,c);return -87;
 case W8_SYS_PAGE145:{
  /* Probe the complete range and old-protection output before changing any PTE. */
  if(e||!b||(a&4095)||(b&4095)||a<W8_BASE||a>=W8_LIMIT||b>W8_LIMIT-a||b>32*1024*1024)return -87;
  if(c!=1&&c!=3&&c!=5)return -50;
  unsigned old=0;
  for(uint64_t at=a;at<a+b;at+=4096){uint64_t*p=pte8(at,0);if(!p||!(*p&(1|RESERVED141)))return -487;
#ifdef ENGINE_M14
 if((*p&MAP_SHARED146)&&!mapping_protect146(at,(unsigned)c))return -5;
#endif
 if(at==a)old=(*p&NX)?((*p&2)?4:2):32;}
  if(user8(d,&old,sizeof(old),1))return -998;
  for(uint64_t at=a;at<a+b;at+=4096){uint64_t*p=pte8(at,0);*p=(*p&~(NX|UINT64_C(2)))|((c&2)?2:0)|((c&4)?0:NX);__asm__ volatile("invlpg (%0)"::"r"(at):"memory");}
  return 0;
 }
 case W8_SYS_MAP:return map8(a,b,(unsigned)c);
 case W8_SYS_RESERVE:return reserve141(a,b,(unsigned)c,1);
 case W8_SYS_SYNC_CREATE:return create_sync142(a,b,c);
 case W8_SYS_SYNC_OPERATION:return operate_sync142(a,b,c,d);
 case W8_SYS_SYNC_CLOSE:return close_sync142(a);
 case W8_SYS_WAIT_OBJECTS:return wait_objects142(f,a);
 case W8_SYS_PROCESS_EPOCH:return (int64_t)spaces142[active_space142]->wait_epoch;
 case W8_SYS_EXCEPTION_REGISTER:if(!access_exception142(a,4))return -1;spaces142[active_space142]->exception_entry=a;return 0;
 case W8_SYS_EXCEPTION_RETURN:return return_exception142(f,a);
 case W8_SYS_SOFTWARE148:return software_exception148(f,a,b,c,d);
#ifdef ENGINE_M14
 case W8_SYS_EXE148:return exe_syscall148(f,a,b,c,d,e);
#endif
 case W8_SYS_VMINFO:{uint64_t values[4]={virtual_pages141,count8,lazy_faults141,OWN8};return user8(a,values,sizeof(values),1)?-1:0;}
 case W8_SYS_UNMAP:case W8_SYS_PROTECT:{
  if(!b||(a&4095)||(b&4095)||a<W8_BASE||a>=W8_LIMIT||b>W8_LIMIT-a||b>32*1024*1024)return -1;
  if(f->rax==W8_SYS_PROTECT&&c!=1&&c!=3&&c!=5)return -1;
  for(uint64_t at=a;at<a+b;at+=4096){uint64_t*p=pte8(at,0);if(!p||!(*p&(1|RESERVED141)))return -1;
#ifdef ENGINE_M14
 if((*p&MAP_SHARED146)&&(f->rax==W8_SYS_UNMAP||!mapping_protect146(at,(unsigned)c)))return -1;
#endif
 }
  for(uint64_t at=a;at<a+b;at+=4096){uint64_t*p=pte8(at,0),physical=*p&UINT64_C(0x000ffffffffff000);if(f->rax==W8_SYS_UNMAP){unsigned present=*p&1;*p=0;if(present)free_owned8(physical);--virtual_pages141;}else *p=physical|
#ifdef ENGINE_M14
 (*p&MAP_SHARED146)|
#endif
 ((*p&1)?5:RESERVED141|4)|((c&2)?2:0)|((c&4)?0:NX);__asm__ volatile("invlpg (%0)"::"r"(at):"memory");}return 0;
 }
 case W8_SYS_FILE_OPEN143:{w8_file_request143 request;if(b||c||d||e||user8(a,&request,sizeof(request),0)||!terminated142(request.path,256))return -87;int64_t slot=file_open143(request.path,request.access,request.share,request.creation,request.flags,0);return slot<0?slot:(int64_t)file_token143((unsigned)slot);}
 case W8_SYS_FILE_OP143:{if(!a&&b>=10&&b<=18&&b!=12&&b!=13){char target[256];if(string8(c,path,256))return -998;
  if(b==18){if(!path8(path,0))return -5;const v6_entry*directory=find8(path);if(!directory)return -3;if(directory->kind!=2)return -267;if(e>=V6_ENTRIES)return 0;unsigned prefix=length8(path);for(unsigned i=(unsigned)e;i<V6_ENTRIES;++i){const v6_entry*entry=m6_volume()->entries+i;if(!entry->kind||memcmp(entry->path,path,prefix)||entry->path[prefix]!='/')continue;const char*name=entry->path+prefix+1;unsigned nested=0;while(*name)if(*name++=='/')nested=1;if(nested)continue;w8_file_info information;unsigned error=information8(entry,&information);if(error)return -(int64_t)error;if(user8(d,&information,sizeof(information),1))return -998;return i+1;}return 0;}
  if(b==10)return -(int64_t)file_delete143(path);if(b==14)return -(int64_t)file_attributes143(path,(unsigned)d);
  if(b==15){if(!path8(path,0))return -5;const v6_entry*entry=find8(path);if(!entry)return -2;w8_file_info information;unsigned error=information8(entry,&information);if(error)return -(int64_t)error;return user8(d,&information,sizeof(information),1)?-998:0;}
  if(b==16||b==17){if(!path8(path,1))return -5;const v6_entry*entry=find8(path);if(b==17){if(!entry)return -3;if(entry->kind!=2)return -267;for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*child=m6_volume()->entries+i;if(child->kind&&!equal8(child->path,path)&&prefix8(child->path,path))return -145;}return -(int64_t)file_delete143(path);}
   if(entry)return -183;char parent[256];copy8(parent,path,256);unsigned n=length8(parent);while(n&&parent[n-1]!='/')--n;if(!n)return -3;parent[n-1]=0;const v6_entry*directory=find8(parent);if(!directory||directory->kind!=2)return -3;return v6_mkdir(m6_volume(),path)?-1117:0;}
  if(string8(d,target,256))return -998;return -(int64_t)file_move143(path,target,(unsigned)e);}int slot=file_handle143(a);if(slot<0)return -6;file8*grant=files8+slot;file_object143*object=file_objects143[grant->object];
  switch(b){case 1:return d>4096?-87:file_read143((unsigned)slot,c,(unsigned)d);case 2:return d>4096?-87:file_write143((unsigned)slot,c,(unsigned)d);
   case 3:return file_seek143((unsigned)slot,(int64_t)c,(unsigned)d);case 4:return (int64_t)object->size;
   case 5:return !(grant->access&2)?-5:-(int64_t)file_resize143(object,grant->position);
   case 6:return !(grant->access&2)?-5:-(int64_t)file_flush143(object);
   case 7:return -(int64_t)close8((unsigned)slot,1);
   case 8:case 9:{w8_file_info info;memset(&info,0,sizeof(info));
    if(b==9){if(!(grant->access&18)||!path8(grant->path,1))return -5;if(user8(c,&info,sizeof(info),0))return -998;return -(int64_t)file_set_metadata143(object,&info);}
    info.size=object->size;info.kind=1;info.attributes=object->metadata.attributes;memcpy(info.time,object->metadata.times,sizeof(info.time));const v6_entry*entry=find8(object->path);info.identity=entry?(uint64_t)(entry-m6_volume()->entries)+1:0;return user8(c,&info,sizeof(info),1)?-998:0;}
#ifdef ENGINE_M14
   case W8_FILE_COPY148:return d||e?-87:file_copy148((unsigned)slot,c);
   case W8_FILE_WRITE148:return e||d>UINT32_MAX?-87:file_write_large148((unsigned)slot,c,(unsigned)d);
#endif
   case 12:case 13:return d||e?-87:file_lock_call143(f,(unsigned)slot,a,c,b==13);
   default:return -50;
  }
 }
 case W8_SYS_OPEN:{if(string8(a,path,256)||b>2)return -1;return file_open143(path,b?2:1,b?0:1,b==2?1:b?2:3,0,1);}
 case W8_SYS_READ:return a>=32||c>4096?-6:file_read143((unsigned)a,b,(unsigned)c);
 case W8_SYS_WRITE:return a>=32||c>4096?-6:file_write143((unsigned)a,b,(unsigned)c);
 case W8_SYS_SEEK:return a>=32?-6:file_seek143((unsigned)a,(int64_t)b,(unsigned)c);
 case W8_SYS_CLOSE:if(b>1||a>=32)return -1;return close8((unsigned)a,b?0:1)?-1:0;
 case W8_SYS_STAT:{if(string8(a,path,256)||!path8(path,0))return -1;const v6_entry*e=find8(path);if(!e)return -1;w8_file_info result;if(information8(e,&result))return -1;return user8(b,&result,sizeof(result),1)?-1:0;}
 case W8_SYS_ENUM:{
  if(string8(a,path,256)||!path8(path,0)||c>=V6_ENTRIES)return -1;unsigned len=length8(path);v6_volume*v=m6_volume();
  for(unsigned i=(unsigned)c;i<V6_ENTRIES;++i){const v6_entry*e=v->entries+i;if(!e->kind||memcmp(e->path,path,len)||e->path[len]!='/')continue;const char*p=e->path+len+1;unsigned slash=0;while(*p)if(*p++=='/')slash=1;if(slash)continue;w8_file_info result;if(information8(e,&result)||user8(b,&result,sizeof(result),1))return -1;return i+1;}return 0;
 }
 case W8_SYS_MKDIR:case W8_SYS_DELETE:{if(string8(a,path,256)||b>1||c||d||e)return -1;if(!path8(path,1)
#ifdef ENGINE_M14
 &&!(f->rax==W8_SYS_MKDIR&&installer_authority147()&&installer_user_grant147(path,1))
#endif
 ){return -1;}
 unsigned s=f->rax==W8_SYS_MKDIR?v6_mkdir(m6_volume(),path):file_delete143(path);if(b&&s==V6_EXISTS)return -80;if(!s&&f->rax==W8_SYS_MKDIR&&input8.command==W8_INSTALL&&equal8(path,input8.product_root))created_root8=1;return !s||s==V6_EXISTS?0:-1;}
 case W8_SYS_MOVE:{char destination[256];if(string8(a,path,256)||string8(b,destination,256)||!path8(path,1)||!path8(destination,1)||d||e)return -1;
#ifdef ENGINE_M14
 if(c==2)return staging_move147(path,destination);
#endif
 if(c>1)return -1;return file_move143(path,destination,(unsigned)c)?-1:0;}
 case W8_SYS_TRUNCATE:{if(a>=32||!files8[a].live||!files8[a].write)return -1;return file_resize143(file_objects143[files8[a].object],files8[a].position)?-1:0;}
 case W8_SYS_OUTPUT:{if(b>4096||user8(a,io8,(unsigned)b,0))return -1;output8((char*)io8,(unsigned)b);return (int64_t)b;}
 case W8_SYS_THREAD_CREATE:{
  /* Runtime trampoline is required to lie in an executable user mapping. */
  uint64_t*entry=pte8(a,0);if(!entry||!(*entry&1)||(*entry&NX)||d>1)return -1;
  unsigned slot=1;while(slot<THREADS142&&threads142[slot].state)++slot;if(slot==THREADS142||generation142>=0x3fffffu)return -1;
  thread142*t=threads142+slot;uint64_t low=THREAD_STACK142(slot),top=low+0x100000,teb=THREAD_TEB142(slot);
  if(map8(top-16384,16384,3))return -1;
  if(map8(teb,8192,3)){for(uint64_t v=top-16384;v<top;v+=4096){uint64_t*p=pte8(v,0);free_owned8(*p&UINT64_C(0x000ffffffffff000));*p=0;--virtual_pages141;}return -1;}
  memset(t,0,sizeof(*t));t->generation=++generation142;t->state=d?T142_SUSPENDED:T142_READY;t->low=low;t->top=top;t->teb=teb;
  uint64_t id=thread_token142(slot),pid=input8.process_id;
  if(user8(teb+0x40,&pid,8,1)||user8(teb+0x30,&teb,8,1)||user8(teb+8,&top,8,1)||user8(teb+16,&low,8,1)||user8(teb+0x48,&id,8,1))return -1;
  t->frame.cs=0x1b;t->frame.ss=0x23;t->frame.rflags=0x202;t->frame.rip=a;t->frame.rsp=top-8;t->frame.rdi=b;t->frame.rsi=c;
  *(uint16_t*)t->fx=0x37f;*(uint32_t*)(t->fx+24)=0x1f80;return (int64_t)id;
 }
 case W8_SYS_PROCESS_CREATE:return create_process142(a,b);
 case W8_SYS_PROCESS_STATUS:return process_status142(a,b,(unsigned)c);
 case W8_SYS_PROCESS_CLOSE:return close_process_handle142(a);
 case W8_SYS_PROCESS_ID:{if(a==UINT64_MAX)return input8.process_id;int h=process_handle_slot142(a);if(h<0||spaces142[active_space142]->handles[h].kind!=1)return -1;return spaces142[active_space142]->handles[h].access&0x1400u?(int64_t)process_objects142[spaces142[active_space142]->handles[h].object].pid:-5;}
 case W8_SYS_THREAD_ID:{if(a==UINT64_MAX-1)return (int64_t)thread_token142(current142);int h=process_handle_slot142(a);if(h>=0){process_handle142*cap=spaces142[active_space142]->handles+h;return cap->kind==2?(int64_t)process_objects142[cap->object].primary_id:-1;}int t=thread_slot142(a);return t<0?-1:(int64_t)thread_token142((unsigned)t);}
 case W8_SYS_PROCESS_TERMINATE:return terminate_process142(a,(unsigned)b);
 case W8_SYS_SECURITY148:{
  if(a||b||c||d||e)return -87;
#ifdef ENGINE_M14
  const v6_entry*owner=find8(input8.user_root);if(!owner||owner->kind!=2)return -1008;
  return W8_SECURITY_AUTHENTICATED148|W8_SECURITY_USERS148|W8_SECURITY_INTERACTIVE148;
#else
  return -50;
#endif
 }
 case W8_SYS_PROCESSES148:{
  if(b==2)return e?-87:open_process148((unsigned)a,(unsigned)c,(unsigned)d);
  if(b==3)return d||e?-87:process_image148(a,c);
  _Static_assert(SPACES142==W8_PROCESS_SNAPSHOT_MAX148,"Process inventory must cover every Windows space");
  if(c||d||e||b>1)return -87;
  if(b==1){if(string8(a,path,256))return -998;if(!path_content1410(path))return -5;unsigned error=child_image142(path);if(error)return -(int64_t)error;
   const char*name=path;for(unsigned j=0;path[j];++j)if(path[j]=='/')name=path+j+1;char*current=spaces142[active_space142]->image_name148;
   if(current[0]&&!equal8(current,name))return -5;copy8(current,name,64);return 0;
  }w8_process_snapshot148 snapshot={0};
  for(unsigned i=0;i<SPACES142;++i){private_space142*p=spaces142[i];if(!p)continue;process_object142*o=process_objects142+p->object;if(!o->used||!o->live)continue;
   w8_process_record148*r=snapshot.records+snapshot.count++;r->pid=o->pid;r->parent=o->parent_pid;
   for(unsigned j=0;j<THREADS142;++j)if(p->threads[j].state&&p->threads[j].state!=T142_EXITED)++r->threads;
   const char*name=p->image_name148;if(!name[0]){name=p->input.source;for(unsigned j=0;p->input.source[j];++j)if(p->input.source[j]=='/')name=p->input.source+j+1;}copy8(r->name,name,sizeof(r->name));
  }return user8(a,&snapshot,sizeof(snapshot),1)?-998:0;
 }
 case W8_SYS_THREAD_LIST:{w8_thread_snapshot result[THREADS142];memset(result,0,sizeof(result));unsigned count=0;for(unsigned i=0;i<THREADS142;++i)if(threads142[i].state&&threads142[i].state!=T142_EXITED){result[i]=(w8_thread_snapshot){threads142[i].teb,(uint32_t)thread_token142(i),threads142[i].state};++count;}return user8(a,result,sizeof(result),1)?-1:(int64_t)count;}
 case W8_SYS_ACCESS:{if(!b||a<W8_BASE||a>=W8_LIMIT||b>W8_LIMIT-a||!c||(c&~7u))return -1;for(uint64_t at=a&~UINT64_C(4095);at<a+b;at+=4096){uint64_t*p=pte8(at,0);if(!p||!(*p&(1|RESERVED141))||((c&2)&&!(*p&2))||((c&4)&&(*p&NX)))return -1;}return 0;}
 case W8_SYS_QUIESCE:for(unsigned i=0;i<THREADS142;++i)if(i!=current142&&threads142[i].state){threads142[i].state=T142_EXITED;threads142[i].code=(unsigned)a;}return 0;
 case W8_SYS_THREAD_CLOSE:{int slot=thread_slot142(a);if(slot<0)return -1;threads142[slot].closed=1;return 0;}
 case W8_SYS_THREAD_RESUME:{if((a&W8_HANDLE_TAG_MASK)==W8_PROCESS_TAG)return resume_process_thread142(a);int slot=thread_slot142(a);if(slot<0||threads142[slot].state==T142_EXITED)return -1;unsigned suspended=threads142[slot].state==T142_SUSPENDED;if(suspended)threads142[slot].state=T142_READY;return suspended;}
 case W8_SYS_THREAD_STATUS:{if((a&W8_HANDLE_TAG_MASK)==W8_PROCESS_TAG)return process_status142(a,b,2);int slot=a==UINT64_MAX-1?(int)current142:thread_slot142(a);if(slot<0)return -1;thread142*t=threads142+slot;if(b&&user8(b,&t->code,4,1))return -1;return t->state==T142_EXITED?0:259;}
 case W8_SYS_THREAD_BEGIN_EXIT:{
  thread142*t=threads142+current142;if(t->exiting)return 0;unsigned live=0;
  for(unsigned i=0;i<THREADS142;++i)if(threads142[i].state&&threads142[i].state!=T142_EXITED&&!threads142[i].exiting)++live;
  if(live==1)return 1;t->exiting=1;return 0;
 }
 case W8_SYS_THREAD_EXIT:{
  ui_thread_release144(active_space142,current142);threads142[current142].state=T142_EXITED;threads142[current142].code=(unsigned)a;if(!current142){process_object142*o=process_objects142+spaces142[active_space142]->object;o->primary_done=1;o->primary_code=(unsigned)a;wake_process_waiters142();}
  ++spaces142[active_space142]->wait_epoch;for(unsigned i=0;i<THREADS142;++i)if(threads142[i].state==T142_PARK){threads142[i].state=T142_READY;threads142[i].frame.rax=0;}
  refresh_sync_waits142();unsigned live=0;for(unsigned i=0;i<THREADS142;++i)if(threads142[i].state&&threads142[i].state!=T142_EXITED)++live;
  if(!live){threads142[current142].state=T142_READY;return 1;}context8=*f;w8_active=0;w8_escape();break;
 }
 case W8_SYS_SLEEP:case W8_SYS_PARK:{
  unsigned park=f->rax==W8_SYS_PARK;
  if(park){if(e>1)return -1;if(e&&d!=spaces142[active_space142]->wait_epoch)return 0;uint32_t value;if(user8(a,&value,4,0))return -1;if(value!=(uint32_t)b)return 0;}
  uint64_t delay=park?c:a;if(delay>UINT32_MAX)return -1;
  thread142*t=threads142+current142;t->state=delay?(park?T142_PARK:T142_SLEEP):T142_READY;
  t->address=park?a:0;t->deadline=delay==UINT32_MAX?UINT64_MAX:m3_clock_ticks()*10+delay;
  context8=*f;context8.rax=0;w8_active=0;w8_escape();break;
 }
 case W8_SYS_WAKE:{unsigned woke=0;for(unsigned i=0;i<THREADS142&&woke<b;++i)if(threads142[i].state==T142_PARK&&threads142[i].address==a){threads142[i].state=T142_READY;threads142[i].frame.rax=0;++woke;}return woke;}
 case W8_SYS_EXIT:finish8((unsigned)a);break;
 case W8_SYS_TIME:return a?((int64_t)now8()):(int64_t)(m3_clock_ticks()*10);
 case W8_SYS_YIELD:snapshot8();context8=*f;context8.rax=0;w8_active=0;w8_escape();break;
 case W8_SYS_METADATA:{
  if(a>=32||!files8[a].live||b>1)return -1;file_object143*object=file_objects143[files8[a].object];w8_file_info data;memset(&data,0,sizeof(data));
  if(b){if(!path8(files8[a].path,1)||user8(c,&data,sizeof(data),0))return -1;return file_set_metadata143(object,&data)?-1:0;}
  memcpy(data.time,object->metadata.times,sizeof(data.time));data.attributes=object->metadata.attributes;return user8(c,&data,sizeof(data),1)?-1:0;
 }
 case W8_SYS_INFO:if(a==0)return 1;else if(a==1)return (int64_t)(pages_stats().total_pages*4096);else if(a==2)return (int64_t)((pages_stats().total_pages-pages_stats().current_pages)*4096);else if(a==3)return (int64_t)(v6_capacity(m6_volume())-v6_used(m6_volume()));else if(a==4)return (int64_t)v6_capacity(m6_volume());else if(a==5){v6_volume*v=m6_volume();unsigned free=0;if(v)for(unsigned i=0;i<V6_ENTRIES;++i)if(!v->entries[i].kind)++free;return free;}return -1;
 default:(void)d;return -1;
 }return -1;
}
trap_frame *w8_trap(trap_frame*f){
 if(!w8_active)return f;
 if(f->vector==14){uint64_t address;__asm__ volatile("movq %%cr2,%0":"=r"(address));
  if(!(f->error&1)&&address>=W8_BASE&&address<W8_LIMIT&&!commit141(address,(f->error&2)!=0,(f->error&16)!=0))return f;
  if(!(f->error&1)&&address>=threads142[current142].low&&address<threads142[current142].top&&address+65536>=f->rsp&&!map8(address&~UINT64_C(4095),4096,3))return f;
 }
 if(f->vector==128){f->rax=(uint64_t)dispatch8(f);return f;}
 if(f->vector==32){out8(0x20,0x20);if(++quantum8<1)return f;context8=*f;w8_active=0;w8_escape();}
 serial_text("M8_PROCESS_FAULT vector=");serial_hex(f->vector);serial_text(" rip=");serial_hex(f->rip);serial_text(" address=");uint64_t addr;__asm__ volatile("movq %%cr2,%0":"=r"(addr));serial_hex(addr);serial_text("\n");
 uint64_t fault_address;__asm__ volatile("movq %%cr2,%0":"=r"(fault_address));if((f->vector==14||f->vector==6||f->vector==0)&&enter_exception142(f,fault_address))return f;
 copy8(info8.message,"The Windows process stopped after an unsupported operation or memory fault.",sizeof(info8.message));info8.state=3;info8.status=f->vector==14?0xc0000005u:f->vector==6?0xc000001du:f->vector==0?0xc0000094u:0xc0000001u;w8_active=0;w8_escape();
}
