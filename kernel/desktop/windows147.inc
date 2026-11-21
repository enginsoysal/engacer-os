/* Native frontend for the bounded original Windows-console compatibility profile. */
#define PRODUCT_ROOT8 "/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}"
enum {PREVIEW8=12000,INSTALL8,REMOVE8,CONFIRM8,BACK8,INFO8,ZIP8,EXTRACT8,CANCEL8,OUTPUT_PREV8,OUTPUT_NEXT8,LICENSE8,INSPECT141,CHOOSE_MSI147,DETAILS_MSI147,GUI144=12100};
extern const char windows8_licenses[];
static unsigned installed8(void){
 static uint64_t generation=UINT64_MAX;static unsigned valid;
 v6_volume*v=m6_volume();if(generation!=v->generation){generation=v->generation;const v6_entry*e=entry(PRODUCT_ROOT8 "/product.bin");valid=e&&e->kind==1&&!v6_verify(v,PRODUCT_ROOT8 "/product.bin");}
 return valid;
}
static unsigned review_source147(application*a){
 const v6_entry*e=entry(a->path);win_review147*r=&a->msi147;
 return e&&e->kind==1&&e->size==r->source_size&&e->first==r->source_first&&e->crc==r->source_crc;
}
static unsigned windows_choose_source147(application*a,const char*path){
 char owner[256];root_path(owner,"");unsigned n=length(owner);const v6_entry*e=entry(path);
 if(!n||memcmp(path,owner,n)||!e||e->kind!=1||!e->size||e->size>8u*1024u*1024u||ui12_file_natural(ui12_file_extension(file_basename11(path)),"msi"))return 0;
 memset(&a->msi147,0,sizeof(a->msi147));a->msi147.selected=1;copy(a->path,path,256);a->number=0;a->offset=0;return 1;
}
static void review_capture147(application*a,const w8_info*i){
 win_review147*r=&a->msi147;if(!r->waiting)return;
 if(i->job_id147!=r->job){r->waiting=r->ready=0;notice(a,"Another task replaced this review. Review the installer again.");return;}
 if(i->state==1)return;r->waiting=0;r->ready=0;
 if(i->state!=2||i->status||!review_source147(a)||!win_product_make147(r->root,sizeof(r->root),i->code)){notice(a,"The installer could not be reviewed, or changed during review. No installation was started.");return;}
 unsigned nonzero=0;for(unsigned k=0;k<32;++k)nonzero|=i->source_sha147[k];if(!nonzero){notice(a,"The review did not return a verified source digest. No installation was started.");return;}
 memcpy(r->digest,i->source_sha147,32);r->profile=i->profile147;r->files=i->files;r->total_bytes=i->total_bytes;
 r->registry=i->registry147;r->shortcuts=i->shortcuts147;r->features=i->features147;
 copy(r->product,i->product,sizeof(r->product));copy(r->version,i->version,sizeof(r->version));copy(r->publisher,i->publisher,sizeof(r->publisher));copy(r->code,i->code,sizeof(r->code));r->ready=1;
 notice(a,r->profile&W8_PROFILE_LEGACY147?"Installer reviewed. You can now confirm installation.":"Installer reviewed. Installation of this package is not enabled yet; no files were installed.");
}
static void init_windows8(application*app,uint64_t token){
 memset(&app->msi147,0,sizeof(app->msi147));if(!app->path[0])root_path(app->path,"Downloads/7z2606-x64.msi");app->number=0;app->offset=0;app->entered=0;
 int width=(int)model.width-80;if(width>940)width=940;int height=(int)model.height-120;if(height>730)height=730;
 desktop_place(&model,token,(desktop_rect){((int)model.width-width)/2,35,width,height});
}
static void draw_windows8(desktop_window*w,application*app,uint64_t token){
 int x=w->bounds.x+24,y=w->bounds.y+62,width=w->bounds.width-48;const w8_info*info=w8_current();
 if(app->calc_error){
  text(x,y,"Software licenses",2,ink());
  app->source_crc=page74(x,y+50,(unsigned)width,(unsigned)(w->bounds.height-190)/24,windows8_licenses,app->offset);
  button(token,x,w->bounds.y+w->bounds.height-57,140,"Previous",OUTPUT_PREV8,0);
  button(token,x+154,w->bounds.y+w->bounds.height-57,140,"Read more",OUTPUT_NEXT8,0);
  button(token,x+308,w->bounds.y+w->bounds.height-57,140,"Back to app",BACK8,1);return;
 }
 review_capture147(app,info);if(app->msi147.ready&&!review_source147(app)){app->msi147.ready=0;app->number=0;notice(app,"The installer changed. Review it again before installing.");}
 unsigned legacy=app->msi147.ready?!!(app->msi147.profile&W8_PROFILE_LEGACY147):!app->msi147.selected;unsigned installed=legacy&&installed8();
 ui73_round(x,y,64,64,12,preferences.accent);text(x+13,y+18,legacy?"7z":"MSI",2,0x102d29);
 ui73_fit(x+84,y+4,width-250,app->msi147.ready?app->msi147.product:legacy?"7-Zip Console":"Windows installer",2,ink());
 char identity[160];identity[0]=0;if(app->msi147.ready){copy(identity,app->msi147.version,sizeof(identity));append(identity,"  /  ",sizeof(identity));append(identity,app->msi147.publisher,sizeof(identity));}ui73_fit(x+84,y+38,width-100,app->msi147.ready?identity:legacy?"26.06  /  Igor Pavlov  /  Windows x64":"Choose an MSI, then review its package details.",1,ink());
 ui73_fit(x+width-150,y+9,150,info->state==1?"Working...":installed?"Installed":"Not installed",1,ink());
 ui73_paragraph(x,y+84,width,2,"Native Windows application support is being expanded. Review shows package metadata without running custom actions.",ink());
 if(app->number){
  text(x,y+145,app->number==1?"Install 7-Zip Console?":"Remove 7-Zip Console?",2,ink());
  ui73_paragraph(x,y+194,width,5,app->number==1?"" ENGINE_PRODUCT_NAME " will verify the included MSI before changing files, then install its 106 original files in a separate application folder. Your documents stay separate. The console program is supported; the Windows GUI is unavailable.":"Unchanged application files and product registrations will be removed. Your documents and modified application files will be kept. You can install the application again later.",ink());
  button(token,x,y+340,150,"Go back",BACK8,0);button(token,x+166,y+340,190,app->number==1?"Install 7-Zip":"Remove 7-Zip",CONFIRM8,1);
  button(token,x+372,y+340,150,"Licenses",LICENSE8,0);return;
 }
 if(!installed){
  ui73_round(x,y+132,width,76,8,desktop_dark16()?0x142b35:0xe8f0f4);
  button(token,x+width-188,y+145,174,"Choose MSI...",CHOOSE_MSI147,0);text(x+14,y+145,"Installer file",1,ink());ui73_fit(x+14,y+177,width-220,app->path,1,ink());
 }
 int actions=y+(installed?140:226);
 if(info->state==1){
  button(token,x,actions,150,"Cancel task",CANCEL8,0);
 }else{
  if(legacy)button(token,x,actions,160,installed?"Open 7-Zip":"Install 7-Zip",installed?INFO8:INSTALL8,1);else ui73_fit(x,actions+10,160,"Review only",1,ink());
  button(token,x+174,actions,170,installed?"Remove app":"Review installer",installed?REMOVE8:PREVIEW8,!legacy);
  button(token,x+358,actions,130,"Licenses",LICENSE8,0);button(token,x+736,actions,140,app->entered?"Hide details":"Details",DETAILS_MSI147,0);
  if(installed||!entry(PRODUCT_ROOT8))button(token,x+502,actions,220,"Check a Windows file",INSPECT141,0);
  if(legacy&&entry(PRODUCT_ROOT8)&&!installed)button(token,x+502,actions,190,"Recover / remove",REMOVE8,0);
 }
 if(installed&&info->state!=1){
  button(token,x,y+194,195,"Create test archive",ZIP8,0);button(token,x+209,y+194,195,"Extract test archive",EXTRACT8,0);
  button(token,x+418,y+194,210,"Open file manager",GUI144,0);button(token,x+642,y+194,190,"Choose MSI...",CHOOSE_MSI147,0);
  ui73_fit(x,y+246,width,"The test uses a separate sample document in your Documents folder.",1,ink());
 }
 const char*message=app->notice[0]?app->notice:info->message[0]?info->message:
  info->state==1?"7-Zip is running...":info->state==2&&info->command==W8_RUN?"Finished successfully.":installed?"Ready. Open the original Windows app or try creating and extracting a test archive.":"Choose Install 7-Zip to get started. Use Choose MSI to review another installer. Review alone does not install it.";
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
 (void)token;if(w->app!=WINDOWS8||command<PREVIEW8||(command>DETAILS_MSI147&&command!=GUI144))return 0;
 if(command==DETAILS_MSI147){app->entered^=1;invalidate(w->bounds);return 1;}
 if(command==LICENSE8){app->calc_error=1;app->offset=0;invalidate(w->bounds);return 1;}
 if(command==BACK8){app->number=0;app->calc_error=0;app->offset=0;invalidate(w->bounds);return 1;}
 if(command==OUTPUT_PREV8){app->offset=0;invalidate(w->bounds);return 1;}
 if(command==OUTPUT_NEXT8){const char*source=app->calc_error?windows8_licenses:w8_current()->output;if(source[app->source_crc])app->offset=app->source_crc;invalidate(w->bounds);return 1;}
 if(command==CANCEL8){w8_cancel();invalidate(w->bounds);return 1;}
 if(w8_pending()){notice(app,"A Windows task is already running. Wait or cancel it.");invalidate(w->bounds);return 1;}
 if(command==CHOOSE_MSI147){picker_begin12(token,P12_WINDOWS_MSI147);return 1;}
 if(command==INSTALL8&&app->msi147.selected&&(!app->msi147.ready||!review_source147(app)||!(app->msi147.profile&W8_PROFILE_LEGACY147))){notice(app,app->msi147.ready?"This package is review-only while its installation support is being completed.":"Review this installer before installing.");invalidate(w->bounds);return 1;}
 if(command==INSTALL8||command==REMOVE8){app->number=command==INSTALL8?1:2;invalidate(w->bounds);return 1;}
 if(command==INSPECT141){picker_begin12(token,P12_WINDOWS_INSPECT);return 1;}
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
   if(!e||e->kind!=1){notice(app,"Choose an available MSI file first.");invalidate(w->bounds);return 1;}
   r->source_size=e->size;r->source_first=e->first;r->source_crc=e->crc;
   result=w8_start(job,source,PRODUCT_ROOT8,user,arguments);if(!result){r->waiting=1;r->job=w8_current()->job_id147;}
  }else if(job==W8_INSTALL&&app->msi147.selected){
   if(!app->msi147.ready||!review_source147(app)||!(app->msi147.profile&W8_PROFILE_LEGACY147)){notice(app,"The reviewed installer is unavailable or changed. Review it again.");invalidate(w->bounds);return 1;}
   result=w8_start_reviewed147(job,source,app->msi147.root,user,arguments,app->msi147.digest);
  }else result=w8_start(job,source,PRODUCT_ROOT8,user,arguments);notice(app,result?"The Windows task could not start. Open System Monitor for memory details.":"");app->offset=0;
 }invalidate(w->bounds);return 1;
}
