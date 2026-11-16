/* One frame for the native volume, USB collection, USB folders and empty/error states. */
static void files_nav_button12(uint64_t token,int x,int y,unsigned command,unsigned icon,unsigned enabled){
 desktop_rect r={x,y,44,36};component_button12(token,r,"",command,0,enabled);
 ui12_palette p=ui12_theme(preferences.dark,preferences.accent);ui12_style s=ui12_control_style(p,enabled?component_state12(token,command):UI12_DISABLED,0);
 ui12_icon_ink(icon,x+10,y+6,24,s.ink);if(enabled)file_control11(token,r,command);
}
static void files_breadcrumbs12(desktop_window*w,application*a,uint64_t token,desktop_rect field){
 (void)w;component_field12(field,0);file_control11(token,field,F11_ADDRESS);int editable=field.width>=130?52:0,right=field.x+field.width-editable;
 if(a->usb_mode10==1)ui73_fit(field.x+10,field.y+8,right-field.x-18,"USB drives",UI12_BODY,ink());
 else{char label[48],n[24];decimal(n,a->usb_disk10+1);copy(label,"USB ",48);append(label,n,48);int root=(int)ui73_measure(label,UI12_BODY)+16;if(root>right-field.x-8)root=right-field.x-8;
  if(root>16){ui73_fit(field.x+10,field.y+8,root-8,label,UI12_BODY,ink());file_control11(token,(desktop_rect){field.x+4,field.y,root,36},F12_USB_ROOT);}
  if(!equal(a->usb_path10,"/")&&right-field.x-root>26){text(field.x+root+5,field.y+8,"/",UI12_BODY,ink());ui73_fit(field.x+root+20,field.y+8,right-field.x-root-26,file_basename11(a->usb_path10),UI12_BODY,ink());}}
 if(editable)button(token,right,field.y,editable,"Edit",F11_ADDRESS,0);
}
static const char*files_nav_hint12(uint64_t token,i11_target target){
 if(target.window!=token)return 0;if(target.action==NAV_BACK)return "Back (Alt+Left)";if(target.action==NAV_FORWARD)return "Forward (Alt+Right)";if(target.action==FILE_UP)return "Up one level (Alt+Up)";if(target.action==F12_REFRESH)return "Refresh this location";if(target.action==NAV_PREVIOUS)return "Previous page of items";if(target.action==NAV_NEXT)return "Next page of items";return 0;
}
static void files_hint_damage12(i11_target before,i11_target after){
 i11_target targets[]={before,after};for(unsigned i=0;i<2;++i){desktop_window*w=desktop_lookup(&model,targets[i].window);if(w&&w->app==FILES&&files_nav_hint12(targets[i].window,targets[i]))invalidate((desktop_rect){w->bounds.x+12,w->bounds.y+w->bounds.height-32,w->bounds.width-24,30});}
}
static void files_frame12(desktop_window*w,application*a,uint64_t token){
 int x=w->bounds.x+16,y=w->bounds.y+49,width=w->bounds.width;unsigned sidebar=file_sidebar11(w),compact=width<600;navigation72*h=&navigation[a-apps];
 files_nav_button12(token,x,y,NAV_BACK,ICON12_BACK,ui12_history_can(h,0));files_nav_button12(token,x+52,y,NAV_FORWARD,ICON12_FORWARD,ui12_history_can(h,1));
 unsigned up=a->usb_mode10==2||(!a->usb_mode10&&!equal(a->path,"/"));files_nav_button12(token,x+104,y,FILE_UP,ICON12_UP,up);files_nav_button12(token,x+156,y,F12_REFRESH,ICON12_REFRESH,1);
 int tools=compact?0:184,address_width=width-32-208-tools;if(address_width<48)address_width=48;file_breadcrumbs11(w,a,token,(desktop_rect){x+208,y,address_width,36});
 if(!compact){file_button11(token,w->bounds.x+width-190,y,82,file_windows11[a-apps].view?"Details":"Icons",F11_VIEW,!a->usb_mode10,0);file_button11(token,w->bounds.x+width-100,y,84,"Sort",F11_SORT,!a->usb_mode10,0);}
 int by=y+44,next=0;if(!sidebar){button(token,x,by,80,"Places",F11_PLACES,0);next=88;}
 if(!a->usb_mode10){unsigned selected=file_selected_count11(a),writable=files_native_ready12(a)&&writable72(a->path)&&!file_in_bin11(a->path)&&!m6_volume()->readonly;
  if(file_is_bin11(a->path)){file_button11(token,x+next,by,112,"Restore",F11_RESTORE,selected!=0,1);button(token,x+next+120,by,174,"Empty Bin...",F11_EMPTY,0);if(width>=700)file_button11(token,x+next+302,by,78,"Copy",F11_COPY,selected!=0,0);}
  else{file_button11(token,x+next,by,112,"New folder",FILE_FOLDER,writable,1);next+=120;if(width>=780){file_button11(token,x+next,by,112,"New text file",F11_NEW_TEXT,writable,0);next+=120;}if(width>=600){file_button11(token,x+next,by,72,"Copy",F11_COPY,selected!=0,0);next+=80;file_button11(token,x+next,by,65,"Cut",F11_CUT,selected&&writable,0);next+=73;}file_button11(token,x+next,by,75,"Paste",F11_PASTE,writable&&clipboard_kind11==2&&file_clip11.count,0);next+=83;if(width>=700){file_button11(token,x+next,by,94,"Recycle",F11_RECYCLE,selected&&writable,0);next+=102;file_button11(token,x+next,by,72,"Undo",F11_UNDO,file_undo_state11.kind!=0,0);}}}
 else if(a->usb_mode10==2){unsigned ready=files_usb_ready12(a);file_button11(token,x+next,by,176,a->usb_source10[0]?"Copy here":"Copy to Downloads",a->usb_source10[0]?USB_EXPORT10:USB_IMPORT10,ready&&(a->usb_source10[0]?storage_writable(storage_get(a->usb_disk10)):a->usb_selected10!=0),1);next+=184;file_button11(token,x+next,by,120,"Safe remove",USB_EJECT10,ready,0);}
 else ui73_fit(x+next,by+8,width-32-next,"Click to select a drive. Double-click to open.",UI12_SECONDARY,ink());
 if(sidebar){int top=file_body_top11(w),bottom=file_body_bottom11(w);ui73_round(x,top,154,bottom-top,6,preferences.dark?0x20363e:0xeaf1f2);text(x+10,top+10,"Places",UI12_BODY,ink());const char*places[]={"Home","Desktop","Documents","Downloads","Pictures","System drive","USB drives","Recycle Bin"};
  for(unsigned i=0;i<8;++i){char place[256];if(!i)home72(place);else if(i<5)root_path(place,places[i]);else if(i==5)copy(place,"/",256);else if(i==7)file_bin_path11(place,0);else place[0]=0;unsigned selected=i==6?a->usb_mode10!=0:!a->usb_mode10&&equal(place,a->path);button(token,x+6,top+38+(int)i*38,142,places[i],i<6?NAV_HOME+i:i==6?USB_OPEN10:F11_BIN,selected);}}
}
static void files_footer12(desktop_window*w,application*a,uint64_t token,unsigned count,unsigned selected,const char*message){
 int x=w->bounds.x+16,footer=w->bounds.y+w->bounds.height-76,width=w->bounds.width;unsigned page=a->usb_mode10?files_usb_rows12(w):file_page_size11(w);
 ui73_fit(x,footer+9,40,"Page",UI12_SECONDARY,ink());file_button11(token,x+48,footer,64,"Prev",NAV_PREVIOUS,count&&a->offset!=0,0);file_button11(token,x+120,footer,64,"Next",NAV_NEXT,a->offset+page<count,0);char info[96],n[24];decimal(n,count);copy(info,n,96);append(info,count==1?" item | ":" items | ",96);decimal(n,selected);append(info,n,96);append(info," selected",96);ui73_fit(x+208,footer+9,width-240-(file_job_error11?108:0),info,UI12_SECONDARY,ink());if(file_job_error11)button(token,w->bounds.x+width-118,footer,102,"Details",F11_JOB_DETAILS,0);
 const char*hint=files_nav_hint12(token,hover12);if(!hint&&control_active)hint=files_nav_hint12(token,(i11_target){focused_control_window,focused_action,I11_BUTTON});ui73_fit(x,w->bounds.y+w->bounds.height-26,width-32,a->notice[0]?a->notice:hint?hint:message,UI12_SECONDARY,ink());if(file_job_state11.active&&file_job_state11.owner==token)file_job_draw11(token,x,w->bounds.y+w->bounds.height-138,width-32);
}
static void files_empty12(int x,int y,int width,int height,unsigned icon,const char*title,const char*detail){
 if(height<190){ui12_icon(icon,x+12,y+8,24,preferences.dark);ui73_fit(x+48,y+8,width-60,title,UI12_SECTION,ink());unsigned lines=height>60?(height-60)/21:1;if(lines>3)lines=3;ui73_paragraph(x+12,y+52,width-24,lines,detail,ink());}
 else{ui12_icon(icon,x+20,y+12,40,preferences.dark);ui73_fit(x+20,y+68,width-40,title,UI12_SECTION,ink());ui73_paragraph(x+20,y+104,width-40,3,detail,ink());}
}
static void files_usb_body12(desktop_window*w,application*a,uint64_t token){
 int x=w->bounds.x+16+(file_sidebar11(w)?170:0),top=file_body_top11(w),width=w->bounds.width-56-(file_sidebar11(w)?170:0),start=top+42;unsigned rows=files_usb_rows12(w),count=0,selected=0,status=0;
 text(x+10,top+8,"Name",UI12_BODY,ink());if(width>=400){text(x+width-230,top+8,"Type",UI12_BODY,ink());text(x+width-92,top+8,"Size",UI12_BODY,ink());}rectangle((desktop_rect){x,top+34,width,1},preferences.dark?0x35515a:0xd7e3e8);
 if(a->usb_mode10==1){const storage_disk*selected_drive=a->usb_selected10?storage_get(a->usb_selected10-1):0;if(selected_drive&&(!selected_drive->readable||selected_drive->transport!=STORAGE_USB||selected_drive->context!=a->usb_context10)){a->usb_selected10=0;selected_drive=0;}selected=selected_drive&&selected_drive->readable&&selected_drive->transport==STORAGE_USB;count=files_drive_count12();if(a->offset>=count)a->offset=0;
  for(unsigned i=0;i<rows&&a->offset+i<count;++i){unsigned disk=files_drive_at12(a->offset+i);const storage_disk*d=storage_get(disk);desktop_rect r={x,start+(int)i*44,width,36};unsigned chosen=a->usb_selected10==disk+1;if(chosen){ui73_round(r.x,r.y,r.width,r.height,6,file_tint11());file_focus_rect11(r);}file_control11(token,r,USB_DISK10+disk);ui12_icon(ICON12_USB,x+10,r.y+5,24,preferences.dark);char label[64],n[24];decimal(n,disk+1);copy(label,"USB drive ",64);append(label,n,64);ui73_fit(x+44,r.y+8,width-(width>=400?282:46),label,UI12_BODY,ink());if(width>=400){ui73_fit(x+width-230,r.y+8,130,"USB drive",UI12_BODY,ink());char size[48];file_size_text11(size,d->sectors*d->sector_bytes);ui73_fit(x+width-92,r.y+8,90,size,UI12_BODY,ink());}}
  if(!count)files_empty12(x,start,width,file_body_bottom11(w)-start,ICON12_USB,"No USB drive is connected","Connect a supported USB drive and choose Refresh. Back, Home and the other places remain available.");}
 else{for(unsigned row=0;row<V6_ENTRIES;++row)selected+=selected_row11(a,row);status=usb_listing10(a,a->offset,rows,&count);if(status){usb_notice10(a,status);files_empty12(x,start,width,file_body_bottom11(w)-start,ICON12_USB,status==B_ABSENT?"This drive is disconnected":"This location is unavailable","Back and Home still work. Choose USB drives to select a connected drive; Refresh never substitutes a different device.");count=0;}
  else{for(unsigned i=0;i<rows&&a->offset+i<count;++i){rem10_entry*e=&usb_rows10[i];desktop_rect r={x,start+(int)i*44,width,36};unsigned chosen=selected_row11(a,a->offset+i);if(chosen){ui73_round(r.x,r.y,r.width,r.height,6,file_tint11());file_focus_rect11(r);}file_control11(token,r,USB_ROW10+i);ui12_icon(shell_path_icon12(e->name,e->kind),x+10,r.y+5,24,preferences.dark);ui73_fit(x+44,r.y+8,width-(width>=400?282:46),e->name,UI12_BODY,ink());if(width>=400){ui73_fit(x+width-230,r.y+8,130,e->kind==2?"Folder":"USB file",UI12_BODY,ink());char size[48];if(e->kind==2)copy(size,"-",48);else file_size_text11(size,e->size);ui73_fit(x+width-92,r.y+8,90,size,UI12_BODY,ink());}}
   if(!count)files_empty12(x,start,width,file_body_bottom11(w)-start,ICON12_USB,"This USB folder is empty","The navigation frame stays here. Use Back, Up or Home to continue browsing.");}}
 files_footer12(w,a,token,count,selected,a->usb_mode10==1?"USB drive selection never formats or erases the device.":"FAT32 browsing and one-file create-only copies. Safe remove before unplugging.");
}
