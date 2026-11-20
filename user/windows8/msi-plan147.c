/* Actual MSI database-derived properties and ordered action admission. */
#include "msi-plan147.h"
#include "msi_db.h"
#include "msi-condition147.h"
#include <engine/sha256.h>
static msia_plan147 *active_plan147;
static void require147(int condition,const char *message){if(!condition)fail8(message);}
static void *allocate_plan147(void *context,size_t bytes){(void)context;return alloc8(bytes);}
static void release_plan147(void *context,void *p){(void)context;free8(p);}
static const char *lookup_plan147(void *opaque,unsigned prefix,const char *name){
 msia_plan147 *plan=opaque;if(prefix){plan->condition_unsupported=1;return "";}return msip_get147(&plan->properties,name);
}
int msia_condition147(msia_plan147 *plan,const char *condition){plan->condition_unsupported=0;int result=msic_evaluate147(condition,lookup_plan147,plan);return plan->condition_unsupported?MSIC_ERROR147:result;}
static int standard147(const char *name){
 static const char *const names[]={"AppSearch","FindRelatedProducts","LaunchConditions","ValidateProductID","CostInitialize","FileCost","CostFinalize","MigrateFeatureStates","InstallValidate","RemoveExistingProducts","InstallInitialize","ProcessComponents","UnpublishFeatures","RemoveRegistryValues","RemoveShortcuts","RemoveFiles","RemoveFolders","CreateFolders","InstallFiles","CreateShortcuts","WriteRegistryValues","RegisterUser","RegisterProduct","PublishFeatures","PublishProduct","InstallFinalize"};
 for(unsigned i=0;i<sizeof(names)/sizeof(names[0]);++i)if(equal8(name,names[i]))return 1;return 0;
}
static int guid147(const char *text){
 if(len8(text)!=38||text[0]!='{'||text[37]!='}')return 0;
 for(unsigned i=1;i<37;++i){unsigned c=(unsigned char)text[i];if(i==9||i==14||i==19||i==24){if(c!='-')return 0;}else if(!((c>='0'&&c<='9')||(c>='A'&&c<='F')||(c>='a'&&c<='f')))return 0;}return 1;
}
static void metadata147(char *out,unsigned capacity,const char *value){require147(value[0]&&len8(value)<capacity,"MSI product metadata is missing or exceeds the supported bound.");copy8(out,value,capacity);}
void msia_close147(msia_plan147 *plan){
 if(!plan)return;require147(plan==active_plan147,"MSI session ownership is invalid.");
 if(plan->actions)free8(plan->actions);if(plan->launches)free8(plan->launches);msip_destroy147(&plan->properties);msi8_database_close();active_plan147=0;free8(plan);
}
msia_plan147 *msia_prepare147(const void *source,unsigned bytes){
 require147(!active_plan147,"Only one MSI database session may be active in this worker.");
 msi8_database(source,bytes);msia_plan147 *plan=calloc8(1,sizeof(*plan));require147(plan!=0,"Not enough memory for the MSI session.");active_plan147=plan;plan->properties=(msip_session147){.alloc=allocate_plan147,.release=release_plan147};plan->source_bytes=bytes;engine_sha256(source,bytes,plan->source_sha256);
 msi8_table properties=msi8_table_open("Property");require147(properties.columns==2&&properties.rows<=256,"MSI Property layout exceeds the supported profile.");
 for(unsigned row=0;row<properties.rows;++row){const char *name=msi8_text(&properties,row,0),*value=msi8_text(&properties,row,1);for(unsigned prior=0;prior<row;++prior)require147(!equal8(name,msi8_text(&properties,prior,0)),"MSI Property keys are duplicated.");require147(msip_set147(&plan->properties,name,value)==0,"MSI Property name/value or allocation exceeds its bound.");}free8(properties.data.data);
 metadata147(plan->product,sizeof(plan->product),msip_get147(&plan->properties,"ProductName"));metadata147(plan->version,sizeof(plan->version),msip_get147(&plan->properties,"ProductVersion"));metadata147(plan->publisher,sizeof(plan->publisher),msip_get147(&plan->properties,"Manufacturer"));
 const char *code=msip_get147(&plan->properties,"ProductCode");require147(guid147(code),"MSI ProductCode is not a valid bounded GUID.");copy8(plan->code,code,sizeof(plan->code));for(unsigned i=0;plan->code[i];++i)if(plan->code[i]>='a'&&plan->code[i]<='f')plan->code[i]-=32;
 copy8(plan->product_root,"/Applications/Windows/",sizeof(plan->product_root));append8(plan->product_root,plan->code,sizeof(plan->product_root));
 msi8_table custom=msi8_table_open("CustomAction");require147(custom.rows<=32&&(!custom.rows||(custom.columns>=4&&custom.columns<=5)),"MSI custom-action metadata exceeds its bound.");
 for(unsigned row=0;row<custom.rows;++row){unsigned type=(unsigned)msi8_integer(&custom,row,1);const char *name=msi8_text(&custom,row,0),*action_source=msi8_text(&custom,row,2),*target=msi8_text(&custom,row,3);unsigned n=0;
  require147(name[0]&&len8(name)<=72&&!standard147(name)&&len8(target)<=4096,"MSI custom-action identity/target is invalid.");require147(type==MSIA_PROPERTY147||type==MSIA_DEFERRED_DLL147,"MSI requires a custom-action type that is not implemented.");
  require147(msip_name147(action_source,&n),"MSI custom-action source is invalid.");if(type==MSIA_DEFERRED_DLL147)require147(msip_name147(target,&n),"MSI DLL export name is outside the supported profile.");
  for(unsigned prior=0;prior<row;++prior)require147(!equal8(name,msi8_text(&custom,prior,0)),"MSI custom-action keys are duplicated.");
  if(custom.columns==5)require147(msi8_integer(&custom,row,4)==INT32_MIN||msi8_integer(&custom,row,4)==0,"MSI extended custom-action flags are unsupported.");
 }
 plan->custom_count=custom.rows;msi8_table sequence=msi8_table_open("InstallExecuteSequence");require147(sequence.columns==3&&sequence.rows&&sequence.rows<=128,"MSI execution sequence exceeds its supported bound.");plan->actions=calloc8(sequence.rows,sizeof(*plan->actions));require147(plan->actions!=0,"Not enough memory for the MSI action plan.");
 for(unsigned row=0;row<sequence.rows;++row){
  msia_action147 action={.name=msi8_text(&sequence,row,0),.condition=msi8_text(&sequence,row,1)};int32_t order=msi8_integer(&sequence,row,2);require147(order>0&&order<=32767,"MSI execution sequence number is unsupported.");action.sequence=(unsigned)order;
  require147(action.name[0]&&len8(action.name)<=72&&msia_condition147(plan,action.condition)!=MSIC_ERROR147,"MSI action name or condition is invalid/unsupported.");
  if(!standard147(action.name)){
   unsigned index=0;while(index<custom.rows&&!equal8(action.name,msi8_text(&custom,index,0)))++index;require147(index<custom.rows,"MSI requires an unknown standard/custom action.");action.kind=(unsigned)msi8_integer(&custom,index,1);action.source=msi8_text(&custom,index,2);action.target=msi8_text(&custom,index,3);
  }
  unsigned at=plan->action_count;for(unsigned i=0;i<plan->action_count;++i)require147(plan->actions[i].sequence!=action.sequence&&!equal8(plan->actions[i].name,action.name),"MSI action names or sequence positions are duplicated.");
  while(at&&plan->actions[at-1].sequence>action.sequence){plan->actions[at]=plan->actions[at-1];--at;}plan->actions[at]=action;++plan->action_count;
 }
 free8(sequence.data.data);if(custom.data.data)free8(custom.data.data);
 msi8_table launch=msi8_table_open("LaunchCondition");require147(launch.rows<=32&&(!launch.rows||launch.columns==2),"MSI launch conditions exceed their supported bound.");
 if(launch.rows){plan->launches=calloc8(launch.rows,sizeof(*plan->launches));require147(plan->launches!=0,"Not enough memory for MSI launch conditions.");for(unsigned row=0;row<launch.rows;++row){const char *condition=msi8_text(&launch,row,0),*message=msi8_text(&launch,row,1);require147(msia_condition147(plan,condition)!=MSIC_ERROR147&&len8(message)<=4096,"MSI launch condition/message is unsupported.");plan->launches[plan->launch_count++]=(msia_launch147){condition,message};}}
 if(launch.data.data)free8(launch.data.data);return plan;
}
unsigned msia_property_action147(msia_plan147 *plan,unsigned index){
 if(!plan||plan!=active_plan147||index>=plan->action_count||plan->actions[index].kind!=MSIA_PROPERTY147)return MSIP_PARAMETER147;
 msia_action147 *action=plan->actions+index;int condition=msia_condition147(plan,action->condition);if(condition==MSIC_ERROR147)return MSIP_PARAMETER147;if(condition==MSIC_FALSE147)return MSIP_OK147;
 char formatted[4097];unsigned status=msip_format147(&plan->properties,action->target,formatted,sizeof(formatted),0,0);return status?status:msip_set147(&plan->properties,action->source,formatted);
}
