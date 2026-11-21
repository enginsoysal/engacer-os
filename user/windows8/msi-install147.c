/* Ordered fresh-install effects, published only after complete verification. */
#include "msi-install147.h"
#include "msi-registry147.h"
#include "msi-shortcuts147.h"
#include "msi-condition147.h"
#include "msi_db.h"
static unsigned install_path147(char out[256],const char*root,const char*tail){unsigned n=len8(root),m=len8(tail);if(n+m>=256)return 206;memcpy(out,root,n);memcpy(out+n,tail,m+1);return 0;}
static unsigned install_shape147(msia_plan147*p){
 /* Recovery/removal and custom script support must be qualified before they
  * can be admitted here. Even an authored Continue bit cannot skip a body. */
 if(p->custom_count)return 50;
 static const char*const required[]={"InstallInitialize","InstallFiles","InstallFinalize"};
 unsigned order=0;for(unsigned k=0;k<3;++k){unsigned found=0;for(unsigned i=0;i<p->action_count;++i)if(equal8(p->actions[i].name,required[k])){if(p->actions[i].sequence<=order||msia_condition147(p,p->actions[i].condition)==MSIC_FALSE147||msia_condition147(p,p->actions[i].condition)==MSIC_ERROR147)return 87;order=p->actions[i].sequence;found=1;}if(!found)return 50;}
 unsigned first=0,last=0;for(unsigned i=0;i<p->action_count;++i){msia_action147*a=p->actions+i;if(a->kind||msia_condition147(p,a->condition)==MSIC_ERROR147)return 50;if(equal8(a->name,"InstallInitialize"))first=a->sequence;if(equal8(a->name,"InstallFinalize"))last=a->sequence;}
 for(unsigned i=0;i<p->action_count;++i){msia_action147*a=p->actions+i;if(equal8(a->name,"CreateShortcuts")||equal8(a->name,"WriteRegistryValues")||equal8(a->name,"PublishProduct")||equal8(a->name,"RegisterProduct")){if(a->sequence<=first||a->sequence>=last)return 50;}}
 /* Empty ancillary authoring is supported. Never silently omit requested
  * directory creation, arbitrary RemoveFile patterns or upgrade behavior. */
 static const char*const unsupported[]={"CreateFolder","RemoveFile"};for(unsigned i=0;i<2;++i){msi8_table table=msi8_table_open(unsupported[i]);unsigned rows=table.rows;if(table.data.data)free8(table.data.data);if(rows)return 50;}
 return 0;
}
static unsigned install_related147(msia_plan147*p){
 const char*base="/Applications/Windows";w8_file_info info;uint64_t cursor=0;const char*upgrade=msip_get147(&p->properties,"UpgradeCode");
 for(;;){int64_t next=(int64_t)sys8(W8_SYS_ENUM,(uint64_t)(uintptr_t)base,(uint64_t)(uintptr_t)&info,cursor,0,0);if(next<0)return 5;if(!next)return 0;if((uint64_t)next<=cursor)return 13;cursor=(uint64_t)next;
  if(info.kind!=2||!win_product_guid147(info.name,1))return 50;char root[256],path[256];if(!win_product_make147(root,sizeof(root),info.name))return 13;
  unsigned status=install_path147(path,root,"/.EngacerMSI/transaction.bin");if(status)return status;w8_file_info pending;if(!stat8(path,&pending))return 1618;
  status=install_path147(path,root,"/product.bin");if(status)return status;void*raw=0;unsigned bytes=load8(path,&raw,WIN_TX_LIMIT147);if(!bytes)return 50;
  if(!win_tx_validate147(raw,bytes)){free8(raw);return 50;}const win_tx_header147*h=raw;
  if(!win_tx_bound147(raw,root,h->user,0)){free8(raw);return 13;}
  unsigned conflict=win_tx_equal147(h->code,p->code)?1638:win_tx_equal147(h->alias,p->program_alias)?183:upgrade[0]&&h->upgrade[0]&&win_tx_equal147(h->upgrade,upgrade)?1638:0;
  free8(raw);if(conflict)return conflict;
 }
}
unsigned msia_install147(msia_plan147*p,const void*source,unsigned bytes){
 if(!p||!p->costed||!source||job8->command!=W8_INSTALL||!equal8(p->product_root,job8->product_root)||bytes!=p->source_bytes||memcmp(p->source_sha256,job8->source_sha147,32))return 87;
 unsigned status=install_shape147(p);if(!status)status=install_related147(p);if(status)return status;
 for(unsigned i=0;i<p->launch_count;++i)if(msia_condition147(p,p->launches[i].condition)!=MSIC_TRUE147)return 1603;
 msij147*j=msij_create147(p);if(!j)return 8;msil_plan147*links=0;
 status=msireg_snapshot147(p,j);if(!status)status=msil_prepare147(p,j,&links);if(!status)status=msij_properties147(j,&p->properties);
 if(!status){int64_t alias=(int64_t)sys8(W8_SYS_ALIAS147,(uint64_t)(uintptr_t)p->program_alias,0,0,0,0);if(alias<0)status=(unsigned)-alias;}
 if(!status)status=msif_stage147(p,j,source,bytes);if(!status)status=msil_stage147(p,links);
 char pending[256],product[256];if(!status)status=install_path147(pending,p->product_root,"/.EngacerMSI/transaction.bin");if(!status)status=install_path147(product,p->product_root,"/product.bin");
 if(!status)status=msij_write147(j,pending);
 unsigned files=0,registry=0,shortcuts=0,final=0;
 for(unsigned i=0;!status&&i<p->action_count;++i){msia_action147*a=p->actions+i;int condition=msia_condition147(p,a->condition);if(condition==MSIC_ERROR147){status=87;break;}if(condition==MSIC_FALSE147)continue;
  if(equal8(a->name,"InstallFiles")){status=msif_promote147(p);files=!status;}
  else if(equal8(a->name,"CreateShortcuts")){if(!files)status=50;else{status=msil_apply147(p,links);shortcuts=!status;}}
  else if(equal8(a->name,"WriteRegistryValues")){if(!files)status=50;else{status=msireg_apply147(j);registry=!status;}}
  else if(equal8(a->name,"InstallFinalize")){
   const win_tx_header147*h=(const void*)j->data;if(!files||(h->registry&&!registry)||(h->links&&!shortcuts)){status=50;break;}
   status=msif_verify147(j);if(!status){int64_t result=(int64_t)sys8(W8_SYS_MOVE,(uint64_t)(uintptr_t)pending,(uint64_t)(uintptr_t)product,2,0,0);if(result<0)status=(unsigned)-result;else final=1;}
  }
  sys8(W8_SYS_YIELD,0,0,0,0,0);
 }
 if(!status&&!final)status=50;msil_close147(links);msij_close147(j);return status;
}
