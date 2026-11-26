#include <engine/winexe148.h>
/* Native frontend for the bounded original Windows-console compatibility profile. */
#define PRODUCT_ROOT8 "/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}"
enum {PREVIEW8=12000,INSTALL8,REMOVE8,CONFIRM8,BACK8,INFO8,ZIP8,EXTRACT8,CANCEL8,OUTPUT_PREV8,OUTPUT_NEXT8,LICENSE8,INSPECT141,CHOOSE_MSI147,DETAILS_MSI147,GUI144=12100,PRODUCT_ROW147=12200,PRODUCTS147=12208,PRODUCT_MORE147=12209,RUN_PRODUCT1410=12301};
extern const char windows8_licenses[];
static unsigned installed8(void){
 static uint64_t generation=UINT64_MAX;static unsigned valid;
 v6_volume*v=m6_volume();if(generation!=v->generation){generation=v->generation;const v6_entry*e=entry(PRODUCT_ROOT8 "/product.bin");valid=e&&e->kind==1&&!v6_verify(v,PRODUCT_ROOT8 "/product.bin");}
 return valid;
}
static unsigned removal_completion147(void){static uint64_t generation=UINT64_MAX;static unsigned present;v6_volume*v=m6_volume();if(generation!=v->generation){generation=v->generation;char path[256];present=win_product_completion147(path,sizeof(path),PRODUCT_ROOT8)&&entry(path)!=0;}return present;}
static const char* selected_root147(const application*a){return a->msi147.ready?a->msi147.root:PRODUCT_ROOT8;}
static unsigned exe_front_record148(exe_record148*r){char owner[256];root_path(owner,"");unsigned n=length(owner);if(n&&owner[n-1]=='/')owner[n-1]=0;return w8_exe_record148(owner,r);}
static unsigned exe_front_select148(application*a){exe_record148 r;if(!exe_front_record148(&r)||r.state==EXE148_REMOVED)return 0;win_review147*v=&a->msi147;memset(v,0,sizeof(*v));v->selected=2;v->ready=1;v->profile=W8_PROFILE_EXE148;v->files=4;v->shortcuts=2;for(unsigned i=0;i<4;++i)v->total_bytes+=exe_payloads148[i].bytes;copy(v->root,EXE148_ROOT,256);copy(v->product,"SumatraPDF",96);copy(v->version,"3.6.1",32);copy(v->publisher,"Krzysztof Kowalczyk",96);copy(v->code,EXE148_CODE,40);memcpy(v->digest,r.source_sha,32);copy(a->path,EXE148_ROOT "/SumatraPDF.exe",256);a->calc_error=a->number=a->offset=0;a->notice[0]=0;return 1;}
static unsigned product_state147(const application*a,unsigned completion){if(equal(selected_root147(a),EXE148_ROOT)){exe_record148 r;return exe_front_record148(&r)&&(completion?(r.state!=EXE148_INSTALLED&&r.state!=EXE148_REMOVED):r.state==EXE148_INSTALLED);}const char*root=selected_root147(a);if(equal(root,PRODUCT_ROOT8))return completion?removal_completion147():installed8();char path[256];if(completion){if(!win_product_completion147(path,256,root))return 0;}else{copy(path,root,256);append(path,"/product.bin",256);}const v6_entry*e=entry(path);return e&&e->kind==1;}
/* Inventory metadata is display-only. The service validates the full journal
 * and immutable source before obtaining an effect; a header grants no authority. */
static unsigned product_header147(const char*root,win_tx_header147*h,unsigned verify){
 char path[256],owner[256];root_path(owner,"");unsigned n=length(owner);if(n&&owner[n-1]=='/')owner[n-1]=0;
 const char*tail[]={"/.EngacerMSI/transaction.bin","/product.bin",0};for(unsigned i=0;i<3;++i){if(i==2){if(!win_product_completion147(path,256,root))return 0;}else{copy(path,root,256);append(path,tail[i],256);}const v6_entry*e=entry(path);if(!e)continue;unsigned got=0;if(e->kind!=1||e->size>WIN_TX_LIMIT147||v6_read(m6_volume(),path,0,h,sizeof(*h),&got)||got!=sizeof(*h)||!win_tx_header_shape147(h,(unsigned)e->size)||!win_tx_bound147(h,root,owner,0)||(verify&&v6_verify(m6_volume(),path)))return 0;return 1;}return 0;
}
static unsigned inventory_product147(unsigned requested,char root[256],win_tx_header147*h){
 v6_volume*v=m6_volume();unsigned found=0;for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*e=v->entries+i;if(!e->kind)continue;char candidate[256];candidate[0]=0;
  if(e->kind==2&&win_product_root147(e->path))copy(candidate,e->path,256);
  else if(e->kind==1){unsigned base=sizeof(WIN_PRODUCT_DONE_BASE147)-1;if(length(e->path)==base+38+5&&!memcmp(e->path,WIN_PRODUCT_DONE_BASE147,base)&&equal(e->path+base+38,".done")){char code[40];memcpy(code,e->path+base,38);code[38]=0;if(win_product_make147(candidate,256,code)&&entry(candidate))candidate[0]=0;}}
  if(candidate[0]&&product_header147(candidate,h,0)){if(found++==requested){copy(root,candidate,256);return 1;}}
 }return 0;
}
static unsigned select_product147(application*a,unsigned index){char root[256];win_tx_header147 h;if(!inventory_product147(index,root,&h)||!product_header147(root,&h,1))return 0;win_review147*r=&a->msi147;memset(r,0,sizeof(*r));r->selected=2;r->ready=1;r->profile=W8_PROFILE_GENERIC147;if(equal(root,PRODUCT_ROOT8))r->profile|=W8_PROFILE_LEGACY147;r->files=h.files;r->registry=h.registry;r->shortcuts=h.links;copy(r->root,root,256);copy(r->product,h.product,96);copy(r->version,h.version,32);copy(r->publisher,h.publisher,96);copy(r->code,h.code,40);memcpy(r->digest,h.source_sha,32);a->calc_error=0;a->offset=0;a->number=0;a->notice[0]=0;return 1;}
static unsigned windows_run_path1410(const application *app,const char *path){
 const char *root=selected_root147(app);
 unsigned n=length(root);
 if(!app->msi147.ready||!win_product_root147(root)||
    length(path)<n||memcmp(path,root,n)||(path[n]&&path[n]!='/'))return 0;
 /* Package control trees are never launch locations. */
 if(path[n]=='/'&&path[n+1]=='.')return 0;
 return 1;
}
static unsigned windows_run_installed1410(application *app,const char *path){
 if(!windows_run_path1410(app,path)||!product_state147(app,0)||
    ui12_file_natural(ui12_file_extension(file_basename11(path)),"exe"))return 0;
 const v6_entry *image=entry(path);
 if(!image||image->kind!=1||v6_verify(m6_volume(),path))return 0;
 win_tx_header147 header;
 const char *alias=EXE148_ALIAS;
 if(!(app->msi147.profile&W8_PROFILE_EXE148)){
  if(!product_header147(selected_root147(app),&header,1))return 0;
  alias=header.alias;
 }
 char user[256];root_path(user,"");unsigned n=length(user);if(n&&user[n-1]=='/')user[n-1]=0;
 if(w8_start_app1410(path,selected_root147(app),user,alias))return 0;
 app->offset=0;return 1;
}
static unsigned review_source147(application*a){
 const v6_entry*e=entry(a->path);win_review147*r=&a->msi147;
 return e&&e->kind==1&&e->size==r->source_size&&e->first==r->source_first&&e->crc==r->source_crc;
}
static unsigned windows_choose_source147(application*a,const char*path){
 char owner[256];root_path(owner,"");unsigned n=length(owner);const v6_entry*e=entry(path);
 const char*extension=ui12_file_extension(file_basename11(path));unsigned is_msi=!ui12_file_natural(extension,"msi"),is_exe=!ui12_file_natural(extension,"exe");
 if(!n||memcmp(path,owner,n)||!e||e->kind!=1||!e->size||(!is_msi&&!is_exe)||e->size>(is_exe?64u:8u)*1024u*1024u)return 0;
 memset(&a->msi147,0,sizeof(a->msi147));a->msi147.selected=1;copy(a->path,path,256);a->number=0;a->offset=0;return 1;
}
static void review_capture147(application*a,const w8_info*i){
 win_review147*r=&a->msi147;if(!r->waiting)return;
 if(i->job_id147!=r->job){r->waiting=r->ready=0;notice(a,"Another task replaced this review. Review the installer again.");return;}
 if(i->state==1)return;r->waiting=0;r->ready=0;
 if(i->state==2&&!i->status&&!i->code[0]&&!ui12_file_natural(ui12_file_extension(file_basename11(a->path)),"exe")){notice(a,i->message);return;}
 if(i->state!=2||i->status||!review_source147(a)||!win_product_make147(r->root,sizeof(r->root),i->code)){notice(a,"The installer could not be reviewed, or changed during review. No installation was started.");return;}
 unsigned nonzero=0;for(unsigned k=0;k<32;++k)nonzero|=i->source_sha147[k];if(!nonzero){notice(a,"The review did not return a verified source digest. No installation was started.");return;}
 memcpy(r->digest,i->source_sha147,32);r->profile=i->profile147;r->files=i->files;r->total_bytes=i->total_bytes;
 r->registry=i->registry147;r->shortcuts=i->shortcuts147;r->features=i->features147;
 copy(r->product,i->product,sizeof(r->product));copy(r->version,i->version,sizeof(r->version));copy(r->publisher,i->publisher,sizeof(r->publisher));copy(r->code,i->code,sizeof(r->code));r->ready=1;
 notice(a,r->profile&(W8_PROFILE_LEGACY147|W8_PROFILE_GENERIC147|W8_PROFILE_EXE148)?"Installer reviewed. You can now confirm installation.":"Installer reviewed. Installation of this package is not enabled yet; no files were installed.");
}
static void init_windows8(application*app,uint64_t token){
 unsigned supplied=app->path[0]!=0;memset(&app->msi147,0,sizeof(app->msi147));if(!supplied)root_path(app->path,"Downloads/7z2606-x64.msi");else if(!windows_choose_source147(app,app->path)){app->msi147.selected=1;notice(app,"Choose an available installer in your folders, then review it before installing.");}app->number=0;app->offset=0;app->entered=0;
 int width=(int)model.width-80;if(width>940)width=940;int height=(int)model.height-120;if(height>730)height=730;
 desktop_place(&model,token,(desktop_rect){((int)model.width-width)/2,35,width,height});
}
static void draw_windows8(desktop_window*w,application*app,uint64_t token){
 int x=w->bounds.x+24,y=w->bounds.y+62,width=w->bounds.width-48;const w8_info*info=w8_current();
 if(app->calc_error==1){
  text(x,y,"Software licenses",2,ink());
  app->source_crc=page74(x,y+50,(unsigned)width,(unsigned)(w->bounds.height-190)/24,windows8_licenses,app->offset);
  button(token,x,w->bounds.y+w->bounds.height-57,140,"Previous",OUTPUT_PREV8,0);
  button(token,x+154,w->bounds.y+w->bounds.height-57,140,"Read more",OUTPUT_NEXT8,0);
  button(token,x+308,w->bounds.y+w->bounds.height-57,140,"Back to app",BACK8,1);return;
 }
 if(app->calc_error==2){text(x,y,"Installed apps and recovery",2,ink());ui73_paragraph(x,y+45,width,2,"Choose an application to manage it. Its original download is not needed for removal.",ink());exe_record148 er;unsigned has_exe=exe_front_record148(&er)&&er.state!=EXE148_REMOVED;if(has_exe)button(token,x,y+110,width,er.state==EXE148_INSTALLED?"SumatraPDF 3.6.1 - original EXE":"SumatraPDF - interrupted EXE; inspect details",12300,0);unsigned count=has_exe;for(unsigned i=0;i<8;++i){char root[256];win_tx_header147 h;if(!inventory_product147(app->offset+i,root,&h))break;button(token,x,y+110+(int)(i+has_exe)*40,width,h.product,PRODUCT_ROW147+i,0);++count;}if(!count)text(x,y+120,"No registered applications or recovery records were found.",1,ink());button(token,x,w->bounds.y+w->bounds.height-57,140,"Back",BACK8,0);char root[256];win_tx_header147 h;if(inventory_product147(app->offset+8,root,&h))button(token,x+154,w->bounds.y+w->bounds.height-57,140,"More apps",PRODUCT_MORE147,0);return;}
 review_capture147(app,info);if(app->msi147.selected==1&&app->msi147.ready&&!review_source147(app)){if(product_state147(app,0)||product_state147(app,1)){app->msi147.selected=2;app->number=0;}else{app->msi147.ready=0;app->number=0;notice(app,"The installer changed. Review it again before installing.");}}
 unsigned legacy=app->msi147.ready?!!(app->msi147.profile&W8_PROFILE_LEGACY147):!app->msi147.selected;unsigned installed=product_state147(app,0),completion=product_state147(app,1),recovering=!installed&&(entry(selected_root147(app))||completion);
 ui73_round(x,y,64,64,12,preferences.accent);text(x+13,y+18,legacy?"7z":!ui12_file_natural(ui12_file_extension(file_basename11(app->path)),"exe")?"EXE":"MSI",2,0x102d29);
 ui73_fit(x+84,y+4,width-250,app->msi147.ready?app->msi147.product:legacy?"7-Zip Console":"Windows installer",2,ink());
 char identity[160];identity[0]=0;if(app->msi147.ready){copy(identity,app->msi147.version,sizeof(identity));append(identity,"  /  ",sizeof(identity));append(identity,app->msi147.publisher,sizeof(identity));}ui73_fit(x+84,y+38,width-100,app->msi147.ready?identity:legacy?"26.06  /  Igor Pavlov  /  Windows x64":"Choose an installer, then review its details.",1,ink());
 ui73_fit(x+width-150,y+9,150,info->state==1?"Working...":installed?"Installed":recovering?"Recovery needed":"Not installed",1,ink());
 ui73_paragraph(x,y+84,width-190,2,"Native Windows application support is being expanded. Review shows package metadata without running custom actions.",ink());
 if(app->number){
  text(x,y+145,app->number==1?"Install this application?":recovering?"Finish recovery?":"Remove this application?",2,ink());
  ui73_paragraph(x,y+194,width,5,app->number==1?"" ENGINE_PRODUCT_NAME " will verify the reviewed source. An EXE opens its original setup window with access to its application folder, two approved shortcuts and a private temporary folder. MSI installation uses its authored package actions. Your documents stay separate.":recovering?"Engacer OS will finish the interrupted operation using its recovery records. Saved application files stay in Documents > Recovered applications. Your other files will not be removed.":"Unchanged application files and product registrations will be removed. Your documents and modified application files will be kept. You can install the application again later.",ink());
  if(app->number==1&&(app->msi147.profile&W8_PROFILE_EXE148)){ui73_fit(x,y+276,width,"Approved folder: " EXE148_ALIAS,1,ink());ui73_fit(x,y+300,width,"Original setup arguments: -install -d \"" EXE148_ALIAS "\"",1,ink());}
  button(token,x,y+340,150,"Go back",BACK8,0);button(token,x+166,y+340,190,app->number==1?"Install app":recovering?"Finish recovery":"Remove app",CONFIRM8,1);
  button(token,x+372,y+340,150,"Licenses",LICENSE8,0);return;
 }
 if(!installed){
  ui73_round(x,y+132,width,76,8,desktop_dark16()?0x142b35:0xe8f0f4);
  button(token,x+width-188,y+145,174,"Choose installer...",CHOOSE_MSI147,0);text(x+14,y+145,"Installer file",1,ink());ui73_fit(x+14,y+177,width-220,app->path,1,ink());
 }
 int actions=y+(installed?140:226);
 if(info->state==1){
  button(token,x,actions,150,"Cancel task",CANCEL8,0);
 }else{
  if(recovering&&(app->msi147.profile&W8_PROFILE_EXE148)){ui73_fit(x,actions+10,160,"Inspection required",1,ink());}else if(installed||(legacy&&(!app->msi147.selected||app->msi147.selected==1))||recovering||(app->msi147.selected==1&&app->msi147.ready&&(app->msi147.profile&(W8_PROFILE_GENERIC147|W8_PROFILE_EXE148))))button(token,x,actions,160,installed?(legacy?"Run 7-Zip console":"Remove app"):recovering?"Recover app":"Install app",installed?(legacy?INFO8:REMOVE8):recovering?REMOVE8:INSTALL8,1);else ui73_fit(x,actions+10,160,"Review only",1,ink());
  button(token,x+174,actions,170,installed?(legacy?"Remove app":"Choose installer..."):"Review installer",installed?(legacy?REMOVE8:CHOOSE_MSI147):PREVIEW8,!legacy);
  button(token,x+358,actions,130,"Licenses",LICENSE8,0);button(token,x+736,actions,140,app->entered?"Hide details":"Details",DETAILS_MSI147,0);
  if(installed&&!legacy&&app->msi147.ready)button(token,x+502,actions,220,"Open app executable",RUN_PRODUCT1410,1);
  else if(installed||(!entry(selected_root147(app))&&!completion))button(token,x+502,actions,220,"Check a Windows file",INSPECT141,0);
 }
 if(installed&&!legacy&&app->msi147.ready&&info->state!=1)
  button(token,x,y+194,220,"Check a Windows file",INSPECT141,0);
 if(installed&&legacy&&info->state!=1){
  button(token,x,y+194,195,"Create test archive",ZIP8,0);button(token,x+209,y+194,195,"Extract test archive",EXTRACT8,0);
  button(token,x+418,y+194,210,"Open file manager",GUI144,0);button(token,x+642,y+194,190,"Choose installer...",CHOOSE_MSI147,0);
  ui73_fit(x,y+246,width,"The test uses a separate sample document in your Documents folder.",1,ink());
 }
 if(info->state!=1)button(token,x+width-174,y+82,174,"Installed apps",PRODUCTS147,0);
 const char*message=app->notice[0]?app->notice:info->message[0]?info->message:
  info->state==1?"A Windows task is running...":info->state==2&&info->command==W8_RUN?"Finished successfully.":installed?(legacy?"Ready. Run the 7-Zip console or try creating and extracting a test archive.":"Installed. Choose an executable in this app’s folder to open it."):recovering?(app->msi147.profile&W8_PROFILE_EXE148?"An EXE operation was interrupted. Keep its files and protected record for inspection. Automatic EXE recovery is not supported yet.":"A previous operation needs cleanup. Choose Recover app. The original download is not needed."):"Choose Install app for the included 7-Zip, or Choose installer to review another installer. Review alone does not install it.";
 ui73_paragraph(x,y+294,width,info->command==W8_RUN||info->command==W8_INSPECT?2:3,message,ink());
 if(info->state==1&&info->command!=W8_RUN){
  unsigned filled=(unsigned)width*info->percent/100;ui73_round(x,y+374,width,8,4,desktop_dark16()?0x233c47:0xdce8ee);
  if(filled)ui73_round(x,y+374,(int)filled,8,4,preferences.accent);
  char progress[40];decimal(progress,info->percent);append(progress,"% complete",40);text(x,y+390,progress,1,ink());
 }
 if(app->msi147.ready&&info->state!=1&&info->command!=W8_RUN&&info->command!=W8_INSPECT){char summary[128],number[32];decimal(number,app->msi147.files);copy(summary,number,sizeof(summary));append(summary," files  /  ",sizeof(summary));decimal(number,(app->msi147.total_bytes+1023)/1024);append(summary,number,sizeof(summary));append(summary," KiB installed size",sizeof(summary));ui73_fit(x,y+374,width,summary,1,ink());}
 if(w->bounds.height>600&&info->output[0]&&(app->entered||info->command==W8_RUN||info->command==W8_INSPECT)){
  int top=y+(info->command==W8_RUN||info->command==W8_INSPECT?382:442);unsigned rows=(unsigned)(w->bounds.y+w->bounds.height-80-top)/24;
  text(x,top-28,info->command==W8_INSPECT?"File check details - application not started":info->command==W8_RUN?"Output from the original Windows program":"Installer details",1,ink());
  app->source_crc=page74(x,top,(unsigned)width,rows,info->output,app->offset);
  button(token,x,w->bounds.y+w->bounds.height-57,140,"Previous",OUTPUT_PREV8,0);button(token,x+154,w->bounds.y+w->bounds.height-57,140,"More output",OUTPUT_NEXT8,0);
 }
}
static void sample_name8(char*out,const char*base,unsigned number,const char*extension){
 copy(out,base,256);if(number){char suffix[24];decimal(suffix,number+1);append(out,"-",256);append(out,suffix,256);}append(out,extension,256);
}
static unsigned action_windows8(desktop_window*w,application*app,uint64_t token,unsigned command){
 (void)token;if(w->app!=WINDOWS8||command<PREVIEW8||(command>DETAILS_MSI147&&command!=GUI144&&command!=12300&&command!=RUN_PRODUCT1410&&(command<PRODUCT_ROW147||command>PRODUCT_MORE147)))return 0;
 if(command==12300){if(!exe_front_select148(app))notice(app,"This EXE record needs inspection. No operation started.");invalidate(w->bounds);return 1;}
 if(command==DETAILS_MSI147){app->entered^=1;invalidate(w->bounds);return 1;}
 if(command==LICENSE8){app->calc_error=1;app->offset=0;invalidate(w->bounds);return 1;}
 if(command==PRODUCTS147){app->calc_error=2;app->offset=0;invalidate(w->bounds);return 1;}
 if(command>=PRODUCT_ROW147&&command<PRODUCTS147){if(!select_product147(app,app->offset+command-PRODUCT_ROW147))notice(app,"This application record needs inspection; no task was started.");invalidate(w->bounds);return 1;}
 if(command==PRODUCT_MORE147){app->offset+=8;invalidate(w->bounds);return 1;}
 if(command==BACK8){app->number=0;app->calc_error=0;app->offset=0;invalidate(w->bounds);return 1;}
 if(command==OUTPUT_PREV8){app->offset=0;invalidate(w->bounds);return 1;}
 if(command==OUTPUT_NEXT8){const char*source=app->calc_error?windows8_licenses:w8_current()->output;if(source[app->source_crc])app->offset=app->source_crc;invalidate(w->bounds);return 1;}
 if(command==CANCEL8){w8_cancel();invalidate(w->bounds);return 1;}
 if(w8_pending()){notice(app,"A Windows task is already running. Wait or cancel it.");invalidate(w->bounds);return 1;}
 if(command==CHOOSE_MSI147){picker_begin12(token,P12_WINDOWS_MSI147);return 1;}
 if(command==INSTALL8&&app->msi147.selected&&(!app->msi147.ready||!review_source147(app)||!(app->msi147.profile&(W8_PROFILE_LEGACY147|W8_PROFILE_GENERIC147|W8_PROFILE_EXE148)))){notice(app,app->msi147.ready?"This package requires installer features that are not supported yet.":"Review this installer before installing.");invalidate(w->bounds);return 1;}
 if(command==INSTALL8||command==REMOVE8){app->number=command==INSTALL8?1:2;invalidate(w->bounds);return 1;}
 if(command==INSPECT141){picker_begin12(token,P12_WINDOWS_INSPECT);return 1;}
 if(command==RUN_PRODUCT1410){
  if(app->msi147.ready&&product_state147(app,0))picker_begin12(token,P12_WINDOWS_RUN1410);
  return 1;
 }
 unsigned job=0;const char*source=app->path,*arguments="";char sample_arguments[512];
 if(command==CONFIRM8){job=app->number==1?W8_INSTALL:app->number==2?W8_REMOVE:0;app->number=0;}
 if(command==PREVIEW8)job=W8_PREVIEW;
 if(command==GUI144){job=W8_RUN;source=PRODUCT_ROOT8 "/7zFM.exe";arguments="";}
 if(command==INFO8||command==ZIP8||command==EXTRACT8){job=W8_RUN;source=PRODUCT_ROOT8 "/7z.exe";arguments=command==INFO8?"i":command==ZIP8?"a -tzip -mx=1 -mmt=off -y EngineOS-Windows.zip EngineOS-Windows.txt":"x -mmt=off -y -oEngineOS-Windows-Extracted EngineOS-Windows.zip";}
 if(command==ZIP8||command==EXTRACT8){
  char path[256],name[256],archive[256];unsigned chosen=100,latest=100;
  for(unsigned i=0;i<100;++i){sample_name8(name,"EngineOS-Windows",i,".zip");root_path(path,"Documents/");append(path,name,256);if(entry(path))latest=i;}chosen=latest==100?0:latest+1;
  if(command==ZIP8){
   if(chosen==100){notice(app,"The sample archive limit was reached. Move or remove old sample archives in Documents, then try again.");invalidate(w->bounds);return 1;}
   sample_name8(archive,"EngineOS-Windows",chosen,".zip");copy(sample_arguments,"a -tzip -mx=1 -mmt=off -y ",512);append(sample_arguments,archive,512);append(sample_arguments," EngineOS-Windows.txt",512);
  }else{
   if(latest==100){notice(app,"Create a test archive first, then choose Extract test archive.");invalidate(w->bounds);return 1;}
   sample_name8(archive,"EngineOS-Windows",latest,".zip");chosen=100;
   for(unsigned i=0;i<100;++i){sample_name8(name,"EngineOS-Windows-Extracted",i,"");root_path(path,"Documents/");append(path,name,256);if(!entry(path)){chosen=i;break;}}
   if(chosen==100){notice(app,"The sample folder limit was reached. Move or remove old extraction folders in Documents, then try again.");invalidate(w->bounds);return 1;}
   sample_name8(name,"EngineOS-Windows-Extracted",chosen,"");copy(sample_arguments,"x -mmt=off -y -o",512);append(sample_arguments,name,512);append(sample_arguments," ",512);append(sample_arguments,archive,512);
  }arguments=sample_arguments;
 }
 if(job){
  char user[256];root_path(user,"");unsigned n=length(user);if(n&&user[n-1]=='/')user[n-1]=0;
  if(command==ZIP8){char path[256];root_path(path,"Documents/EngineOS-Windows.txt");if(!entry(path)){static const char sample[]="Created in " ENGINE_PRODUCT_NAME " and archived by the original Windows 7-Zip application.\n";if(v6_put(m6_volume(),path,sizeof(sample)-1,memory_source,(void*)sample)){notice(app,"The sample document could not be created.");invalidate(w->bounds);return 1;}}}
  unsigned result;
  if(job==W8_PREVIEW){win_review147*r=&app->msi147;const v6_entry*e=entry(source);r->ready=r->waiting=0;
   if(!e||e->kind!=1){notice(app,"Choose an available installer file first.");invalidate(w->bounds);return 1;}
   r->source_size=e->size;r->source_first=e->first;r->source_crc=e->crc;
   result=w8_start(job,source,PRODUCT_ROOT8,user,arguments);if(!result){r->waiting=1;r->job=w8_current()->job_id147;}
  }else if(job==W8_INSTALL&&app->msi147.selected){
   if(!app->msi147.ready||!review_source147(app)||!(app->msi147.profile&(W8_PROFILE_LEGACY147|W8_PROFILE_GENERIC147|W8_PROFILE_EXE148))){notice(app,"The reviewed installer is unavailable or changed. Review it again.");invalidate(w->bounds);return 1;}
   result=w8_start_reviewed147(job,source,app->msi147.root,user,arguments,app->msi147.digest);
  }else{if(job==W8_REMOVE&&app->msi147.profile&W8_PROFILE_EXE148)source=EXE148_ROOT "/SumatraPDF.exe";result=w8_start(job,source,job==W8_REMOVE?selected_root147(app):PRODUCT_ROOT8,user,arguments);}notice(app,result?"The Windows task could not start. Open System Monitor for memory details.":"");app->offset=0;
 }invalidate(w->bounds);return 1;
}
