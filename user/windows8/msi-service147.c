/* Engacer-authored lazy MSI service. Native write actions are added separately. */
#include "msi-plan147.h"
#include "msi_db.h"
unsigned msi_bind147(msia_plan147*);
void msi_unbind147(void);
static unsigned table_count147(const char *name){msi8_table table=msi8_table_open(name);unsigned count=table.rows;if(table.data.data)free8(table.data.data);return count;}
__declspec(dllexport) unsigned EngacerMsiRun147(void){
 if(job8->magic!=W8_MAGIC)exit8(87);
 if(job8->command!=W8_PREVIEW)fail8("Reusable MSI write actions are still in development. No product was published.");
 progress8(2,"Reading the selected original MSI package.");void *source=0;unsigned bytes=load8(job8->source,&source,8*1024*1024);if(!bytes)fail8("The original MSI package could not be read within its input bound.");msia_plan147 *plan=msia_prepare147(source,bytes);
 /* The preview describes a planned owner-confirmed machine installation.
  * It cannot grant write authority; only the kernel INSTALL context can. */
 if(msip_set147(&plan->properties,"Privileged","1"))fail8("MSI privilege property exceeds its bound.");
 if(equal8(msip_get147(&plan->properties,"ALLUSERS"),"2")&&msip_set147(&plan->properties,"ALLUSERS","1"))fail8("MSI installation-context property exceeds its bound.");
 const char *owner=job8->user_root;for(unsigned i=0;job8->user_root[i];++i)if(job8->user_root[i]=='/')owner=job8->user_root+i+1;char user[256];copy8(user,"C:\\Users\\",sizeof(user));if(!owner[0]||len8(owner)+len8(user)>=sizeof(user))fail8("MSI user alias exceeds its bound.");append8(user,owner,sizeof(user));msia_cost147(plan,user);if(!msi_bind147(plan))fail8("The native MSI session could not be bound.");
 copy8(job8->product,plan->product,sizeof(job8->product));copy8(job8->version,plan->version,sizeof(job8->version));copy8(job8->publisher,plan->publisher,sizeof(job8->publisher));copy8(job8->code,plan->code,sizeof(job8->code));job8->files=plan->selected_files;job8->total_bytes=plan->selected_bytes;job8->features=plan->feature_count;job8->registry=table_count147("Registry");job8->shortcuts=table_count147("Shortcut");
 print8("MSI original product: ");print8(plan->product);print8("\nSelected original files: ");number8(plan->selected_files);print8(" bytes: ");number8(plan->selected_bytes);print8("\nMSI execute actions: ");number8(plan->action_count);print8(" custom-action metadata: ");number8(plan->custom_count);print8("\nM147_NATIVE_MSI_READ_ONLY_PLAN_PASS\n");msi_unbind147();msia_close147(plan);free8(source);progress8(100,"Read-only MSI preview complete. No installation was performed.");return 0;
}
