/* Engacer-authored lazy MSI service with a bounded fresh-install controller. */
#include "msi-plan147.h"
#include "msi_db.h"
#include "msi-install147.h"
#include "msi-registry147.h"
unsigned msi_bind147(msia_plan147*);
void msi_unbind147(void);
unsigned MsiGetActiveDatabase(unsigned);
unsigned MsiCloseHandle(unsigned);
unsigned msi_table147(unsigned,const char*,msi8_table*);
static unsigned table_count147(unsigned database,const char *name){msi8_table table;if(msi_table147(database,name,&table))fail8("The active MSI database handle is unavailable.");unsigned count=table.rows;if(table.data.data)free8(table.data.data);return count;}
__declspec(dllexport) unsigned EngacerMsiRun147(void){
 if(job8->magic!=W8_MAGIC)exit8(87);
 if(job8->command!=W8_PREVIEW&&job8->command!=W8_INSTALL)fail8("Reusable MSI removal and recovery are still in development. No product was published.");
 progress8(2,"Reading the selected original MSI package.");void *source=0;unsigned bytes=load8(job8->source,&source,8*1024*1024);if(!bytes)fail8("The original MSI package could not be read within its input bound.");msia_plan147 *plan=msia_prepare147(source,bytes);
 if(job8->command==W8_INSTALL&&memcmp(job8->source_sha147,plan->source_sha256,32))fail8("The reviewed MSI source changed. No installation was started.");
 /* The preview describes a planned owner-confirmed machine installation.
  * It cannot grant write authority; only the kernel INSTALL context can. */
 if(msip_set147(&plan->properties,"Privileged","1"))fail8("MSI privilege property exceeds its bound.");
 if(equal8(msip_get147(&plan->properties,"ALLUSERS"),"2")&&msip_set147(&plan->properties,"ALLUSERS","1"))fail8("MSI installation-context property exceeds its bound.");
 if(msireg_appsearch147(plan))fail8("The MSI registry search is outside the supported profile. No installation was started.");
 const char *owner=job8->user_root;for(unsigned i=0;job8->user_root[i];++i)if(job8->user_root[i]=='/')owner=job8->user_root+i+1;char user[256];copy8(user,"C:\\Users\\",sizeof(user));if(!owner[0]||len8(owner)+len8(user)>=sizeof(user))fail8("MSI user alias exceeds its bound.");append8(user,owner,sizeof(user));msia_cost147(plan,user);unsigned install=msi_bind147(plan);if(!install)fail8("The native MSI session could not be bound.");unsigned database=MsiGetActiveDatabase(install);if(!database)fail8("The active MSI database could not be acquired.");
 static const uint8_t legacy147[32]={0x6d,0xc8,0x22,0x56,0x9e,0x77,0x7d,0x9a,0x3e,0xcd,0x5f,0xfc,0xbc,0x22,0xb5,0x56,0x00,0xaf,0x87,0xe6,0xc5,0xd9,0x81,0x0a,0x64,0xe8,0x56,0x6c,0xf5,0xa4,0xaf,0x9f};
 if(job8->command==W8_PREVIEW)memcpy(job8->source_sha147,plan->source_sha256,32);job8->profile147=!memcmp(legacy147,plan->source_sha256,32)?W8_PROFILE_LEGACY147:0;
 copy8(job8->product,plan->product,sizeof(job8->product));copy8(job8->version,plan->version,sizeof(job8->version));copy8(job8->publisher,plan->publisher,sizeof(job8->publisher));copy8(job8->code,plan->code,sizeof(job8->code));job8->files=plan->selected_files;job8->total_bytes=plan->selected_bytes;job8->features=plan->feature_count;job8->registry=table_count147(database,"Registry");job8->shortcuts=table_count147(database,"Shortcut");
 if(job8->command==W8_INSTALL){unsigned status=msia_install147(plan,source,bytes);if(MsiCloseHandle(database))fail8("The active MSI database could not be closed.");msi_unbind147();msia_close147(plan);free8(source);if(status){print8("MSI installation status: ");number8(status);print8("\n");copy8(job8->message,"Installation could not finish. Retained recovery records must be inspected before retrying.",sizeof(job8->message));return status;}progress8(100,"Application files, registry values and shortcuts were installed and verified.");return 0;}
 print8("MSI original product: ");print8(plan->product);print8("\nSelected original files: ");number8(plan->selected_files);print8(" bytes: ");number8(plan->selected_bytes);print8("\nAuthored registry entries: ");number8(job8->registry);print8(" shortcuts: ");number8(job8->shortcuts);print8("\nMSI execute actions: ");number8(plan->action_count);print8(" custom-action metadata: ");number8(plan->custom_count);print8("\nM147_NATIVE_MSI_READ_ONLY_PLAN_PASS\n");if(MsiCloseHandle(database))fail8("The active MSI database could not be closed.");msi_unbind147();msia_close147(plan);free8(source);progress8(100,"Read-only MSI preview complete. No installation was performed.");return 0;
}
