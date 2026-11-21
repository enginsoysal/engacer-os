/* Lazy native MSI entry: preview, fresh install, or cached-source ownership undo. */
#include "msi-plan147.h"
#include "msi_db.h"
#include "msi-install147.h"
#include "msi-remove147.h"
#include "msi-registry147.h"
unsigned msi_bind147(msia_plan147*);
void msi_unbind147(void);
unsigned MsiGetActiveDatabase(unsigned);
unsigned MsiCloseHandle(unsigned);
unsigned msi_table147(unsigned,const char*,msi8_table*);
static unsigned table_count147(unsigned database,const char*name){msi8_table table;if(msi_table147(database,name,&table))fail8("The active MSI database handle is unavailable.");unsigned count=table.rows;if(table.data.data)free8(table.data.data);return count;}
static void service_path147(char out[256],const char*tail){if(!win_product_root147(job8->product_root)||len8(job8->product_root)+len8(tail)>=256)fail8("The product recovery path is invalid.");copy8(out,job8->product_root,256);append8(out,tail,256);}
static msij147*removal_journal147(char source[256]){
 char path[256];service_path147(path,"/.EngacerMSI/transaction.bin");w8_file_info info;
 if(stat8(path,&info))service_path147(path,"/product.bin");
 msij147*j=msij_read147(path,job8->product_root,job8->user_root);if(!j)fail8("No valid product or recovery record was found. No files were removed.");service_path147(source,"/.EngacerMSI/source.msi");return j;
}
static void user_alias147(char user[256]){
 const char*owner=job8->user_root;for(unsigned i=0;job8->user_root[i];++i)if(job8->user_root[i]=='/')owner=job8->user_root+i+1;copy8(user,"C:\\Users\\",256);if(!owner[0]||len8(owner)+len8(user)>=256)fail8("The MSI user alias exceeds its bound.");append8(user,owner,256);
}
static void metadata_service147(msia_plan147*p,unsigned database){
 static const uint8_t legacy[32]={0x6d,0xc8,0x22,0x56,0x9e,0x77,0x7d,0x9a,0x3e,0xcd,0x5f,0xfc,0xbc,0x22,0xb5,0x56,0x00,0xaf,0x87,0xe6,0xc5,0xd9,0x81,0x0a,0x64,0xe8,0x56,0x6c,0xf5,0xa4,0xaf,0x9f};
 if(job8->command!=W8_INSTALL)memcpy(job8->source_sha147,p->source_sha256,32);job8->profile147=!memcmp(legacy,p->source_sha256,32)?W8_PROFILE_LEGACY147:0;
 copy8(job8->product,p->product,sizeof(job8->product));copy8(job8->version,p->version,sizeof(job8->version));copy8(job8->publisher,p->publisher,sizeof(job8->publisher));copy8(job8->code,p->code,sizeof(job8->code));job8->files=p->selected_files;job8->total_bytes=p->selected_bytes;job8->features=p->feature_count;job8->registry=table_count147(database,"Registry");job8->shortcuts=table_count147(database,"Shortcut");
}
__declspec(dllexport) unsigned EngacerMsiRun147(void){
 if(job8->magic!=W8_MAGIC)exit8(87);if(job8->command!=W8_PREVIEW&&job8->command!=W8_INSTALL&&job8->command!=W8_REMOVE)fail8("This MSI operation is not supported.");
 char source_path[256];copy8(source_path,job8->source,256);msij147*recovery=job8->command==W8_REMOVE?removal_journal147(source_path):0;
 progress8(2,recovery?"Reading the application's saved original installer.":"Reading the selected original MSI package.");void*source=0;unsigned bytes=load8(source_path,&source,8*1024*1024);if(!bytes)fail8("The original installer is missing or exceeds its input bound. No installation or removal was started.");msia_plan147*p=msia_prepare147(source,bytes);
 if(job8->command==W8_INSTALL&&memcmp(job8->source_sha147,p->source_sha256,32))fail8("The reviewed MSI source changed. No installation was started.");
 if(recovery){if(msij_restore147(recovery,p))fail8("The saved installer or original selection no longer matches its recovery record. No files were removed.");}
 else{
  if(msip_set147(&p->properties,"Privileged","1"))fail8("The MSI privilege property exceeds its bound.");
  if(equal8(msip_get147(&p->properties,"ALLUSERS"),"2")&&msip_set147(&p->properties,"ALLUSERS","1"))fail8("The MSI installation-context property exceeds its bound.");
  if(msireg_appsearch147(p))fail8("The MSI registry search is outside the supported profile. No installation was started.");
 }
 char user[256];user_alias147(user);msia_cost147(p,user);
 if(recovery&&!equal8(((const win_tx_header147*)(const void*)recovery->data)->alias,p->program_alias))fail8("The saved program location no longer matches the original installer. No files were removed.");
 unsigned install=msi_bind147(p);if(!install)fail8("The native MSI session could not be bound.");unsigned database=MsiGetActiveDatabase(install);if(!database)fail8("The active MSI database could not be acquired.");metadata_service147(p,database);
 unsigned status=0,kept=0;
 if(job8->command==W8_INSTALL)status=msia_install147(p,source,bytes);
 else if(recovery){int64_t alias=(int64_t)sys8(W8_SYS_ALIAS147,(uint64_t)(uintptr_t)p->program_alias,0,0,0,0);status=alias<0?(unsigned)-alias:msir_remove147(p,recovery,&kept);}
 else{
  print8("MSI original product: ");print8(p->product);print8("\nSelected original files: ");number8(p->selected_files);print8(" bytes: ");number8(p->selected_bytes);print8("\nAuthored registry entries: ");number8(job8->registry);print8(" shortcuts: ");number8(job8->shortcuts);print8("\nMSI execute actions: ");number8(p->action_count);print8(" custom-action metadata: ");number8(p->custom_count);print8("\nM147_NATIVE_MSI_READ_ONLY_PLAN_PASS\n");
 }
 if(MsiCloseHandle(database))fail8("The active MSI database could not be closed.");msi_unbind147();msia_close147(p);msij_close147(recovery);free8(source);
 if(status){print8("MSI operation status: ");number8(status);print8("\n");copy8(job8->message,"The operation could not finish. Recovery records and your files were kept; inspect Details before retrying.",sizeof(job8->message));return status;}
 if(job8->command==W8_INSTALL)progress8(100,"Application files, registry values and shortcuts were installed and verified.");
 else if(job8->command==W8_REMOVE)progress8(100,kept?"Removed. Changed files were saved in Documents > Recovered applications.":"Removed. Your personal files are unchanged.");
 else progress8(100,"Read-only MSI preview complete. No installation was performed.");return 0;
}
