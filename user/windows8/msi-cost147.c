/* Bounded clean-install costing from original MSI relations. No target writes. */
#include "msi-plan147.h"
#include "msi_db.h"
static void cost_require147(int yes,const char *message){if(!yes)fail8(message);}
static void join147(char *out,const char *text){cost_require147(len8(out)+len8(text)<256,"MSI destination exceeds the native path bound.");append8(out,text,256);}
static int case_equal147(const char *a,const char *b){unsigned i=0;while(a[i]&&b[i]){unsigned x=(uint8_t)a[i],y=(uint8_t)b[i];if(x>='a'&&x<='z')x-=32;if(y>='a'&&y<='z')y-=32;if(x!=y)return 0;++i;}return a[i]==b[i];}
static int leaf147(const char *text,unsigned n){
 if(!n||n>127||text[n-1]==' '||text[n-1]=='.')return 0;
 char base[16];unsigned bn=0;
 for(unsigned i=0;i<n;++i){unsigned c=(uint8_t)text[i];if(c<32||c>=127||c=='/'||c=='\\'||c==':'||c=='*'||c=='?'||c=='"'||c=='<'||c=='>'||c=='|')return 0;}
 while(bn<n&&text[bn]!='.'&&bn+1<sizeof(base)){unsigned c=(uint8_t)text[bn];base[bn]=(char)(c>='a'&&c<='z'?c-32:c);++bn;}base[bn]=0;
 static const char *const reserved[]={"CON","PRN","AUX","NUL","CLOCK$","CONIN$","CONOUT$"};for(unsigned i=0;i<sizeof(reserved)/sizeof(reserved[0]);++i)if(equal8(base,reserved[i]))return 0;
 if(bn==4&&(!memcmp(base,"COM",3)||!memcmp(base,"LPT",3))&&base[3]>='1'&&base[3]<='9')return 0;return 1;
}
static void target147(const char *field,char out[128],unsigned directory){
 unsigned end=0;while(field[end]&&(!directory||field[end]!=':'))++end;unsigned start=0;
 for(unsigned i=0;i<end;++i)if(field[i]=='|'){cost_require147(!start,"MSI long-name metadata is malformed.");start=i+1;}
 unsigned n=end-start;if(directory&&n==1&&field[start]=='.'){out[0]='.';out[1]=0;return;}
 cost_require147(leaf147(field+start,n),"MSI payload/directory leaf is invalid or outside the ASCII name profile.");memcpy(out,field+start,n);out[n]=0;
}
static unsigned directory147(const msia_plan147 *p,const char *id){for(unsigned i=0;i<p->directory_count;++i)if(equal8(p->directories[i].id,id))return i;fail8("MSI references a missing directory.");}
static unsigned feature147(const msia_plan147 *p,const char *id){for(unsigned i=0;i<p->feature_count;++i)if(equal8(p->features[i].id,id))return i;fail8("MSI references a missing feature.");}
static unsigned component147(const msia_plan147 *p,const char *id){for(unsigned i=0;i<p->component_count;++i)if(equal8(p->components[i].id,id))return i;fail8("MSI references a missing component.");}
static void resolve_directory147(msia_plan147 *p,unsigned index,unsigned depth){
 msia_directory147 *d=p->directories+index;if(d->state==2)return;cost_require147(depth<=32&&d->state!=1,"MSI directory graph contains a cycle or exceeds its depth bound.");d->state=1;d->windows[0]=d->relative[0]=0;
 if(equal8(d->id,"TARGETDIR")){cost_require147(!d->parent[0],"MSI target directory must be the root.");copy8(d->windows,"C:\\",256);}
 else if(equal8(d->id,"ProgramFiles64Folder")||equal8(d->id,"ProgramFilesFolder")){cost_require147(equal8(d->parent,"TARGETDIR"),"MSI system-directory parent is unsupported.");copy8(d->windows,equal8(d->id,"ProgramFiles64Folder")?"C:\\Program Files\\":"C:\\Program Files (x86)\\",256);}
 else if(equal8(d->id,"ProgramMenuFolder")){cost_require147(equal8(d->parent,"TARGETDIR"),"MSI system-directory parent is unsupported.");copy8(d->windows,p->user_windows,256);join147(d->windows,"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\");}
 else if(equal8(d->id,"DesktopFolder")){cost_require147(equal8(d->parent,"TARGETDIR"),"MSI system-directory parent is unsupported.");copy8(d->windows,p->user_windows,256);join147(d->windows,"\\Desktop\\");}
 else{
  cost_require147(d->parent[0],"MSI contains an unsupported directory root.");unsigned parent=directory147(p,d->parent);resolve_directory147(p,parent,depth+1);msia_directory147 *base=p->directories+parent;copy8(d->windows,base->windows,256);char leaf[128];target147(d->target,leaf,1);if(!equal8(leaf,".")){join147(d->windows,leaf);join147(d->windows,"\\");}
  if(index==p->primary_directory){cost_require147(!equal8(leaf,"."),"MSI program directory must have its own name.");d->inside=1;}
  else if(base->inside){d->inside=1;copy8(d->relative,base->relative,256);if(!equal8(leaf,".")){if(d->relative[0])join147(d->relative,"/");join147(d->relative,leaf);}}
 }
 const char *existing=msip_get147(&p->properties,d->id);cost_require147(!existing[0]||equal8(existing,d->windows),"Custom MSI directory overrides are not supported by this profile.");cost_require147(!msip_set147(&p->properties,d->id,d->windows),"MSI directory properties exceed their memory bound.");d->state=2;
}
unsigned msia_file_path147(const msia_plan147 *p,unsigned index,char out[256]){
 if(!p||index>=p->file_count||!out)return 87;const msia_file147 *file=p->files+index;const msia_directory147 *d=p->directories+p->components[file->component].directory;char name[128];target147(file->name,name,0);
 if(!d->inside)return 50;copy8(out,p->product_root,256);if(d->relative[0]){join147(out,"/");join147(out,d->relative);}join147(out,"/");join147(out,name);return 0;
}
static const char *formatted_reference147(void *opaque,unsigned prefix,const char *name){
 msia_plan147 *p=opaque;if(prefix!='#'&&prefix!='$'){p->format_error=87;return "";}if(!p->costed)return "";
 if(prefix=='#'){
  for(unsigned i=0;i<p->file_count;++i)if(equal8(p->files[i].id,name)){
   msia_file147 *file=p->files+i;if(!file->selected)return "";char leaf[128];target147(file->name,leaf,0);copy8(p->format_scratch,p->directories[p->components[file->component].directory].windows,256);join147(p->format_scratch,leaf);return p->format_scratch;
  }
 }else{
  for(unsigned i=0;i<p->component_count;++i)if(equal8(p->components[i].id,name))return p->components[i].selected?p->directories[p->components[i].directory].windows:"";
 }return "";
}
unsigned msia_format147(msia_plan147 *p,const char *text,char *out,unsigned capacity){
 if(!p)return 87;p->format_error=0;unsigned status=msip_format147(&p->properties,text,out,capacity,formatted_reference147,p);if(p->format_error){if(out&&capacity)out[0]=0;return p->format_error;}return status;
}
void msia_cost147(msia_plan147 *p,const char *user_windows){
 cost_require147(p&&!p->costed&&user_windows&&len8(user_windows)<128,"MSI costing session/user is invalid or already costed.");copy8(p->user_windows,user_windows,256);
 msi8_table dirs=msi8_table_open("Directory");cost_require147(dirs.columns==3&&dirs.rows&&dirs.rows<=128,"MSI directory table exceeds its bound.");p->directories=calloc8(dirs.rows,sizeof(*p->directories));cost_require147(p->directories!=0,"Not enough memory for MSI directories.");p->directory_count=dirs.rows;p->primary_directory=UINT32_MAX;
 for(unsigned i=0;i<dirs.rows;++i){msia_directory147 *d=p->directories+i;d->id=msi8_text(&dirs,i,0);d->parent=msi8_text(&dirs,i,1);d->target=msi8_text(&dirs,i,2);unsigned n=0;cost_require147(msip_name147(d->id,&n),"MSI directory identifier is invalid.");for(unsigned j=0;j<i;++j)cost_require147(!equal8(d->id,p->directories[j].id),"MSI directory keys are duplicated.");if(equal8(d->parent,"ProgramFiles64Folder")||equal8(d->parent,"ProgramFilesFolder")){cost_require147(p->primary_directory==UINT32_MAX,"Multiple MSI program roots require a separate installation profile.");p->primary_directory=i;}}
 cost_require147(p->primary_directory!=UINT32_MAX,"MSI has no supported isolated program root.");free8(dirs.data.data);for(unsigned i=0;i<p->directory_count;++i)resolve_directory147(p,i,0);copy8(p->program_alias,p->directories[p->primary_directory].windows,256);unsigned length=len8(p->program_alias);if(length&&p->program_alias[length-1]=='\\')p->program_alias[length-1]=0;
 cost_require147(!msip_set147(&p->properties,"SystemFolder","C:\\Windows\\SysWOW64\\")&&!msip_set147(&p->properties,"System64Folder","C:\\Windows\\System32\\")&&!msip_set147(&p->properties,"WindowsFolder","C:\\Windows\\"),"MSI system-folder property allocation failed.");
 msi8_table features=msi8_table_open("Feature");cost_require147(features.columns==8&&features.rows&&features.rows<=64,"MSI feature table exceeds its bound.");p->features=calloc8(features.rows,sizeof(*p->features));cost_require147(p->features!=0,"Not enough memory for MSI features.");p->feature_count=features.rows;
 for(unsigned i=0;i<features.rows;++i){msia_feature147 *f=p->features+i;f->id=msi8_text(&features,i,0);f->parent=msi8_text(&features,i,1);f->level=msi8_integer(&features,i,5);int attributes=msi8_integer(&features,i,7);cost_require147(f->id[0]&&f->level>=0&&f->level<=32767&&attributes>=0&&!(attributes&~24),"MSI feature level/attributes are unsupported.");f->attributes=(unsigned)attributes;for(unsigned j=0;j<i;++j)cost_require147(!equal8(f->id,p->features[j].id),"MSI feature keys are duplicated.");}free8(features.data.data);
 msi8_table conditions=msi8_table_open("Condition");cost_require147(conditions.rows<=64&&(!conditions.rows||conditions.columns==3),"MSI feature conditions exceed their bound.");
 for(unsigned i=0;i<conditions.rows;++i){msia_feature147 *f=p->features+feature147(p,msi8_text(&conditions,i,0));cost_require147(!f->condition_seen++,"Multiple MSI conditions for one feature are unsupported.");int level=msi8_integer(&conditions,i,1),result=msia_condition147(p,msi8_text(&conditions,i,2));cost_require147(level>=0&&level<=32767&&result<2,"MSI feature condition is invalid/unsupported.");if(result==1)f->level=level;}if(conditions.data.data)free8(conditions.data.data);
 int32_t install_level=1;const char *requested=msip_get147(&p->properties,"INSTALLLEVEL");if(requested[0]){unsigned n=len8(requested);cost_require147(n<=5,"MSI INSTALLLEVEL exceeds its bound.");install_level=0;for(unsigned i=0;i<n;++i){cost_require147(requested[i]>='0'&&requested[i]<='9',"MSI INSTALLLEVEL is invalid.");install_level=install_level*10+requested[i]-'0';}cost_require147(install_level<=32767,"MSI INSTALLLEVEL exceeds its bound.");}
 for(unsigned i=0;i<p->feature_count;++i)p->features[i].selected=p->features[i].level>0&&p->features[i].level<=install_level;
 for(unsigned i=0;i<p->feature_count;++i){unsigned at=i,depth=0;while(p->features[at].parent[0]){cost_require147(++depth<=32,"MSI feature graph contains a cycle or exceeds its depth bound.");at=feature147(p,p->features[at].parent);cost_require147(!p->features[i].selected||p->features[at].selected,"Selecting a child of an absent MSI feature is unsupported.");}}
 msi8_table components=msi8_table_open("Component");cost_require147(components.columns==6&&components.rows&&components.rows<=512,"MSI component table exceeds its bound.");p->components=calloc8(components.rows,sizeof(*p->components));cost_require147(p->components!=0,"Not enough memory for MSI components.");p->component_count=components.rows;
 for(unsigned i=0;i<components.rows;++i){msia_component147 *c=p->components+i;c->id=msi8_text(&components,i,0);c->directory=directory147(p,msi8_text(&components,i,2));int attributes=msi8_integer(&components,i,3);cost_require147(attributes==0||attributes==256||attributes==260,"MSI component attributes are unsupported.");c->attributes=(unsigned)attributes;c->condition=msi8_text(&components,i,4);c->key=msi8_text(&components,i,5);cost_require147(c->id[0]&&msia_condition147(p,c->condition)!=3,"MSI component identity/condition is invalid.");for(unsigned j=0;j<i;++j)cost_require147(!equal8(c->id,p->components[j].id),"MSI component keys are duplicated.");}free8(components.data.data);
 msi8_table links=msi8_table_open("FeatureComponents");cost_require147(links.columns==2&&links.rows<=4096,"MSI feature/component relationships exceed their bound.");for(unsigned i=0;i<links.rows;++i){const char *feature=msi8_text(&links,i,0),*component=msi8_text(&links,i,1);unsigned fi=feature147(p,feature),ci=component147(p,component);for(unsigned j=0;j<i;++j)cost_require147(!equal8(feature,msi8_text(&links,j,0))||!equal8(component,msi8_text(&links,j,1)),"MSI feature/component relationships are duplicated.");if(p->features[fi].selected)p->components[ci].selected=1;}free8(links.data.data);
 for(unsigned i=0;i<p->component_count;++i)if(msia_condition147(p,p->components[i].condition)==0)p->components[i].selected=0;
 msi8_table files=msi8_table_open("File");cost_require147(files.columns==8&&files.rows&&files.rows<=256,"MSI file table exceeds its bound.");p->files=calloc8(files.rows,sizeof(*p->files));cost_require147(p->files!=0,"Not enough memory for MSI files.");p->file_count=files.rows;unsigned last_sequence=0;
 for(unsigned i=0;i<files.rows;++i){msia_file147 *file=p->files+i;file->id=msi8_text(&files,i,0);file->component=component147(p,msi8_text(&files,i,1));file->name=msi8_text(&files,i,2);int size=msi8_integer(&files,i,3),attributes=msi8_integer(&files,i,6),sequence=msi8_integer(&files,i,7);cost_require147(file->id[0]&&size>=0&&size<=32*1024*1024&&(attributes==0||attributes==512)&&sequence>0&&sequence<=32767,"MSI file size/attributes/sequence is unsupported.");file->size=(unsigned)size;file->attributes=(unsigned)attributes;file->sequence=(unsigned)sequence;file->selected=p->components[file->component].selected;if(file->sequence>last_sequence)last_sequence=file->sequence;
  char path[256];cost_require147(!msia_file_path147(p,i,path),"MSI file target is outside its isolated program root.");
  for(unsigned j=0;j<i;++j){cost_require147(!equal8(file->id,p->files[j].id)&&file->sequence!=p->files[j].sequence,"MSI file keys/sequences are duplicated.");char prior[256];cost_require147(!msia_file_path147(p,j,prior)&&!case_equal147(path,prior),"MSI file destinations collide.");}
  if(file->selected){cost_require147(file->size<=32*1024*1024-p->selected_bytes,"Selected MSI files exceed the expanded-byte quota.");++p->selected_files;p->selected_bytes+=file->size;}
 }free8(files.data.data);
 msi8_table media=msi8_table_open("Media");cost_require147(media.columns==6&&media.rows==1&&msi8_integer(&media,0,0)==1&&msi8_integer(&media,0,1)==(int32_t)last_sequence,"MSI requires unsupported media layout.");const char *cabinet=msi8_text(&media,0,3);unsigned n=0;cost_require147(cabinet[0]=='#'&&msip_name147(cabinet+1,&n),"MSI requires an unsupported external cabinet.");p->cabinet=cabinet+1;free8(media.data.data);p->costed=1;
}
