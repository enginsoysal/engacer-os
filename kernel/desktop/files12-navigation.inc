/* Reuse eight history slots; never allocate a second history or a directory cache. */
static ui12_file_location files_current12(application*a){
 ui12_file_location l={0};l.provider=a->usb_mode10;l.offset=a->offset;
 if(l.provider==UI12_USB_FOLDER){l.disk=a->usb_disk10;l.context=a->usb_context10;l.part=a->usb_part10;copy(l.path,a->usb_path10,256);}
 else if(l.provider==UI12_NATIVE)copy(l.path,a->path,256);
 return l;
}
static void files_record12(application*a,const ui12_file_location*before){ui12_file_location after=files_current12(a);if(!ui12_location_equal(before,&after))files_selection_clear12(a);ui12_history_push(&navigation[a-apps],before,&after);}
static unsigned files_native_ready12(application*a){const v6_entry*e=entry(a->path);return equal(a->path,"/")||(e&&e->kind==2);}
static unsigned files_usb_ready12(application*a){const storage_disk*d=storage_get(a->usb_disk10);return d&&d->transport==STORAGE_USB&&d->readable&&d->context==a->usb_context10;}
static void files_selection_clear12(application*a){unsigned slot=(unsigned)(a-apps);a->usb_selected10=0;scroll_records12[slot].owner=0;if(scroll_capture12.owner==desktop_token(&model,slot)){scroll_capture12.owner=0;i11_cancel(&interaction11);}memset(selected11[slot],0,sizeof(selected11[slot]));selection_anchor11[slot]=selection_focus11[slot]=0;interaction11.last_valid=0;control_active=0;file_windows11[slot].address_active=0;if(a->usb_mode10)file_windows11[slot].view=usb_view12;}
static void files_apply12(application*a,const ui12_file_location*l){
 a->usb_mode10=l->provider;a->offset=l->offset;a->notice[0]=0;files_selection_clear12(a);
 if(l->provider==UI12_NATIVE){copy(a->path,l->path,256);a->usb_source10[0]=0;file_visit11(a);if(!files_native_ready12(a))notice(a,"This folder is no longer available. Use Back or Home.");}
 else if(l->provider==UI12_USB_FOLDER){a->usb_disk10=l->disk;a->usb_context10=l->context;a->usb_part10=l->part;copy(a->usb_path10,l->path,256);if(!files_usb_ready12(a))notice(a,"This drive is disconnected. Back and Home still work.");}
}
static void files_visit12(application*a,const char*path,unsigned remember){
 if(!equal(path,"/")){const v6_entry*e=entry(path);if(!e||e->kind!=2){notice(a,"This folder is unavailable. Your current location was kept.");return;}}
 ui12_file_location before=files_current12(a),next={0};copy(next.path,path,256);files_apply12(a,&next);if(remember)files_record12(a,&before);
 serial_text("M125_LOCATION native ");serial_text(path);serial_text("\n");
}
static unsigned files_drive_count12(void){unsigned n=0;for(unsigned i=0;i<storage_count();++i){const storage_disk*d=storage_get(i);if(d->transport==STORAGE_USB&&d->readable)++n;}return n;}
static unsigned files_drive_at12(unsigned row){for(unsigned i=0;i<storage_count();++i){const storage_disk*d=storage_get(i);if(d->transport==STORAGE_USB&&d->readable){if(!row)return i;--row;}}return STORAGE_MAX;}
static unsigned files_usb_rows12(desktop_window*w){unsigned n=file_page_size11(w);return n>6?6:n;}
static unsigned files_navigation12(desktop_window*w,application*a,uint64_t token,unsigned command){
 navigation72*h=&navigation[a-apps];
 if(command==NAV_BACK||command==NAV_FORWARD){unsigned forward=command==NAV_FORWARD;if(ui12_history_can(h,forward)){h->locations[h->position]=files_current12(a);h->position=forward?h->position+1:h->position-1;ui12_file_location next=h->locations[h->position];files_apply12(a,&next);}invalidate(w->bounds);return 1;}
 if(command==F12_REFRESH){file_lists11[a-apps].generation=0;a->notice[0]=0;if(a->usb_mode10)hw10_refresh();invalidate(w->bounds);return 1;}
 if(command==F12_USB_ROOT){if(a->usb_mode10==2){ui12_file_location before=files_current12(a);copy(a->usb_path10,"/",256);a->offset=0;files_selection_clear12(a);files_record12(a,&before);}invalidate(w->bounds);return 1;}
 if(command==FILE_UP&&a->usb_mode10){if(a->usb_mode10==2){if(equal(a->usb_path10,"/"))devices_action10(w,a,token,USB_DRIVES10);else devices_action10(w,a,token,USB_UP10);}return 1;}
 if(command==NAV_PREVIOUS||command==NAV_NEXT){unsigned total=0,page=a->usb_mode10?files_usb_rows12(w):file_page_size11(w);
  if(a->usb_mode10==1)total=files_drive_count12();else if(a->usb_mode10==2){if(usb_listing10(a,0,1,&total)){invalidate(w->bounds);return 1;}}else total=children72(a);
  if(command==NAV_PREVIOUS)a->offset=a->offset>page?a->offset-page:0;else if(a->offset+page<total)a->offset+=page;control_active=0;invalidate(w->bounds);return 1;}
 return 0;
}
static void files_address_text12(application*a,char*out){
 if(!a->usb_mode10){copy(out,a->path,272);return;}if(a->usb_mode10==1){copy(out,"USB drives",272);return;}
 char n[24];decimal(n,a->usb_disk10+1);copy(out,"USB:",272);append(out,n,272);append(out,":",272);append(out,a->usb_path10,272);
}
/* Return zero for the native address parser, one for success, two for bad input. */
static unsigned files_address12(application*a,const char*value){
 const char*aliases[]={"Home","Desktop","Documents","Downloads","Pictures","System drive","Recycle Bin","USB drives"};
 for(unsigned i=0;i<8;++i)if(!file_compare_text11(value,aliases[i]))return 0;
 unsigned explicit_usb=(value[0]=='u'||value[0]=='U')&&(value[1]=='s'||value[1]=='S')&&(value[2]=='b'||value[2]=='B')&&value[3]==':';
 if(!explicit_usb&&(!a->usb_mode10||value[0]=='/'))return 0;
 unsigned disk=a->usb_disk10,context=a->usb_context10,part=a->usb_part10;const char*path=value;char combined[256];
 if(explicit_usb){unsigned number=0,at=4;while(value[at]>='0'&&value[at]<='9'){if(number>STORAGE_MAX)break;number=number*10+value[at++]-'0';}if(!number||number>STORAGE_MAX||value[at++]!=':'||value[at]!='/'){notice(a,"Use a location such as USB:2:/Games.");return 2;}disk=number-1;path=value+at;if(rem10_volume(disk,&part,&context)){notice(a,"That USB drive cannot be opened. Choose a connected supported drive.");return 2;}}
 else{if(a->usb_mode10!=2){notice(a,"Choose a drive first, or enter a USB:2:/folder location.");return 2;}copy(combined,a->usb_path10,256);if(!equal(combined,"/"))append(combined,"/",256);if(length(combined)+length(value)>=256){notice(a,"This path is too long. Your location was kept.");return 2;}append(combined,value,256);path=combined;}
 unsigned total,status=rem10_list(disk,context,part,path,0,usb_rows10,1,&total);if(status){usb_notice10(a,status);return 2;}
 ui12_file_location before=files_current12(a),next={0};next.provider=UI12_USB_FOLDER;next.disk=disk;next.context=context;next.part=part;copy(next.path,path,256);files_apply12(a,&next);files_record12(a,&before);return 1;
}
static void files_title12(application*a,char*out,unsigned size){
 if(a->usb_mode10==1){copy(out,"USB drives - Files",size);return;}char n[24];decimal(n,a->usb_disk10+1);copy(out,"USB drive ",size);append(out,n,size);if(!equal(a->usb_path10,"/")){append(out," / ",size);append(out,file_basename11(a->usb_path10),size);}append(out," - Files",size);
}
