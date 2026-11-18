/* One frame for the native volume, USB collection, USB folders and empty/error states. */
static void files_nav_button12(uint64_t token,int x,int y,unsigned command,unsigned icon,unsigned enabled){
 const char*name=command==NAV_BACK?"Back":command==NAV_FORWARD?"Forward":command==FILE_UP?"Up one level":command==F12_REFRESH?"Refresh":command==NAV_PREVIOUS?"Previous page":command==NAV_NEXT?"Next page":"Navigate folders";
 desktop_rect r={x,y,44,36};component_button12(token,r,"",command,0,enabled);
 ui12_palette p=desktop_palette16();ui12_style s=ui12_control_style(p,enabled?component_state12(token,command):UI12_DISABLED,0);
 ui12_icon_ink(icon,x+10,y+6,24,s.ink);if(enabled){access_capture16(token,command,name,1);file_control11(token,r,command);}
}
static void files_breadcrumbs12(desktop_window*w,application*a,uint64_t token,desktop_rect field){
 (void)w;component_field12(field,0);file_control11(token,field,F11_ADDRESS);int editable=field.width>=130?52:0,right=field.x+field.width-editable;
 if(a->usb_mode10==1)ui73_fit(field.x+10,field.y+8,right-field.x-18,"USB drives",UI12_BODY,ink());
 else{char label[48],n[24];decimal(n,a->usb_disk10+1);copy(label,"USB ",48);append(label,n,48);int root=(int)ui73_measure(label,UI12_BODY)+16;if(root>right-field.x-8)root=right-field.x-8;
  if(root>16){ui73_fit(field.x+10,field.y+8,root-8,label,UI12_BODY,ink());file_control11(token,(desktop_rect){field.x+4,field.y,root,36},F12_USB_ROOT);}
  if(!equal(a->usb_path10,"/")&&right-field.x-root>26){unsigned slashes=0;for(unsigned i=0;a->usb_path10[i];++i)slashes+=a->usb_path10[i]=='/';int leaf=field.x+root;if(slashes>1){text(leaf+5,field.y+8,"/ ...",UI12_BODY,ink());leaf+=44;}if(right-leaf>26){text(leaf+5,field.y+8,"/",UI12_BODY,ink());ui73_fit(leaf+20,field.y+8,right-leaf-26,file_basename11(a->usb_path10),UI12_BODY,ink());}}}
 if(editable)button(token,right,field.y,editable,"Edit",F11_ADDRESS,0);
}
static const char*files_nav_hint12(uint64_t token,i11_target target){
 if(target.window!=token)return 0;if(target.action==NAV_BACK)return "Back (Alt+Left)";if(target.action==NAV_FORWARD)return "Forward (Alt+Right)";if(target.action==FILE_UP)return "Up one level (Alt+Up)";if(target.action==F12_REFRESH)return "Refresh this location";if(target.action==NAV_PREVIOUS)return "Previous page of items";if(target.action==NAV_NEXT)return "Next page of items";return 0;
}
static void files_hint_damage12(i11_target before,i11_target after){
 i11_target targets[]={before,after};for(unsigned i=0;i<2;++i){desktop_window*w=desktop_lookup(&model,targets[i].window);if(w&&w->app==FILES&&files_nav_hint12(targets[i].window,targets[i]))invalidate((desktop_rect){w->bounds.x+12,w->bounds.y+w->bounds.height-32,w->bounds.width-24,30});}
}
#ifdef ENGINE_M13
#include "files17-frame.inc"
#endif
static void files_frame12(desktop_window*w,application*a,uint64_t token){
#ifdef ENGINE_M13
 files_frame17(w,a,token);return;
#endif
 int x=w->bounds.x+16,y=w->bounds.y+49,width=w->bounds.width;unsigned sidebar=file_sidebar11(w),compact=width<600;navigation72*h=&navigation[a-apps];
 files_nav_button12(token,x,y,NAV_BACK,ICON12_BACK,ui12_history_can(h,0));files_nav_button12(token,x+52,y,NAV_FORWARD,ICON12_FORWARD,ui12_history_can(h,1));
 unsigned up=a->usb_mode10==2||(!a->usb_mode10&&!equal(a->path,"/"));files_nav_button12(token,x+104,y,FILE_UP,ICON12_UP,up);files_nav_button12(token,x+156,y,F12_REFRESH,ICON12_REFRESH,1);
 int tools=compact?0:184,address_width=width-32-208-tools;if(address_width<48)address_width=48;file_breadcrumbs11(w,a,token,(desktop_rect){x+208,y,address_width,36});
 if(!compact){file_button11(token,w->bounds.x+width-190,y,82,file_windows11[a-apps].view?"Details":"Icons",F11_VIEW,1,0);file_button11(token,w->bounds.x+width-100,y,84,"Sort",F11_SORT,!a->usb_mode10,0);}
 int by=y+44,next=0;if(!sidebar){button(token,x,by,80,"Places",F11_PLACES,0);next=88;}
 if(!a->usb_mode10){unsigned bin=file_is_bin11(a->path);
  file_button11(token,x+next,by,112,bin?"Restore":"New folder",bin?F11_RESTORE:FILE_FOLDER,files_can_command12(token,bin?F11_RESTORE:FILE_FOLDER),1);next+=120;
  if(width>=700){file_button11(token,x+next,by,72,"Copy",F11_COPY,files_can_command12(token,F11_COPY),0);next+=80;file_button11(token,x+next,by,64,"Cut",F11_CUT,files_can_command12(token,F11_CUT),0);next+=72;}
  file_button11(token,x+next,by,75,"Paste",F11_PASTE,files_can_command12(token,F11_PASTE),0);next+=83;
  file_button11(token,x+next,by,100,"Actions...",F12_COMMANDS,1,0);
 }
 else if(a->usb_mode10==2){unsigned ready=files_usb_ready12(a);unsigned can_copy=ready&&!files_busy12()&&(a->usb_source10[0]?storage_writable(storage_get(a->usb_disk10)):files_can_command12(token,F11_COPY));
  file_button11(token,x+next,by,176,a->usb_source10[0]?"Copy here":"Copy to Downloads",a->usb_source10[0]?USB_EXPORT10:USB_IMPORT10,can_copy,1);next+=184;file_button11(token,x+next,by,120,"Safe remove",USB_EJECT10,ready&&!files_busy12(),0);
  if(width>=700)file_button11(token,x+next+128,by,100,"Actions...",F12_COMMANDS,1,0);
 }
 else ui73_fit(x+next,by+8,width-32-next,"Click to select a drive. Double-click to open.",UI12_SECONDARY,ink());
 if(sidebar){int top=file_body_top11(w),bottom=file_body_bottom11(w);ui73_round(x,top,154,bottom-top,6,desktop_dark16()?0x20363e:0xeaf1f2);text(x+10,top+10,"Places",UI12_BODY,ink());const char*places[]={"Home","Desktop","Documents","Downloads","Pictures","System drive","USB drives","Recycle Bin"};
  for(unsigned i=0;i<8;++i){char place[256];if(!i)home72(place);else if(i<5)root_path(place,places[i]);else if(i==5)copy(place,"/",256);else if(i==7)file_bin_path11(place,0);else place[0]=0;unsigned selected=i==6?a->usb_mode10!=0:!a->usb_mode10&&equal(place,a->path);button(token,x+6,top+38+(int)i*38,142,places[i],i<6?NAV_HOME+i:i==6?USB_OPEN10:F11_BIN,selected);}}
}
static void files_footer12(desktop_window*w,application*a,uint64_t token,unsigned count,unsigned selected,const char*message){
#ifdef ENGINE_M13
 files_footer17(w,a,token,count,selected,message);return;
#endif
 int x=w->bounds.x+16,footer=w->bounds.y+w->bounds.height-76,width=w->bounds.width;unsigned page=a->usb_mode10?files_usb_rows12(w):file_page_size11(w);
 ui73_fit(x,footer+9,40,"Page",UI12_SECONDARY,ink());file_button11(token,x+48,footer,64,"Prev",NAV_PREVIOUS,count&&a->offset!=0,0);file_button11(token,x+120,footer,64,"Next",NAV_NEXT,a->offset+page<count,0);char info[96],n[24];decimal(n,count);copy(info,n,96);append(info,count==1?" item | ":" items | ",96);decimal(n,selected);append(info,n,96);append(info," selected",96);ui73_fit(x+208,footer+9,width-240-(file_job_result11[0]?108:0),info,UI12_SECONDARY,ink());if(file_job_result11[0]&&!files_busy12())button(token,w->bounds.x+width-118,footer,102,"Details",F11_JOB_DETAILS,0);
 const char*hint=files_nav_hint12(token,hover12);if(!hint&&control_active)hint=files_nav_hint12(token,(i11_target){focused_control_window,focused_action,I11_BUTTON});ui73_fit(x,w->bounds.y+w->bounds.height-26,width-32,a->notice[0]?a->notice:hint?hint:message,UI12_SECONDARY,ink());if(file_job_state11.active&&file_job_state11.owner==token)file_job_draw11(token,x,w->bounds.y+w->bounds.height-138,width-32);
}
static void files_empty12(int x,int y,int width,int height,unsigned icon,const char*title,const char*detail){
 if(height<190){ui12_icon(icon,x+12,y+8,24,preferences.dark);ui73_fit(x+48,y+8,width-60,title,UI12_SECTION,ink());unsigned lines=height>60?(height-60)/21:1;if(lines>3)lines=3;ui73_paragraph(x+12,y+52,width-24,lines,detail,ink());}
 else{ui12_icon(icon,x+20,y+12,40,preferences.dark);ui73_fit(x+20,y+68,width-40,title,UI12_SECTION,ink());ui73_paragraph(x+20,y+104,width-40,3,detail,ink());}
}
static void files_usb_body12(desktop_window*w,application*a,uint64_t token){
 int x=w->bounds.x+16+(int)
#ifdef ENGINE_M13
 files_sidebar_width17(w)
#else
 (file_sidebar11(w)?170:0)
#endif
 ,top=file_body_top11(w),width=w->bounds.width-56-(int)
#ifdef ENGINE_M13
 files_sidebar_width17(w)
#else
 (file_sidebar11(w)?170:0)
#endif
 ;
 unsigned icons=file_windows11[a-apps].view,columns=file_columns11(w),rows=files_usb_rows12(w),count=0,selected=0,status=0;int start=top+(icons?6:42);
 if(!icons)files_details_header12(w,token,x,top,width,0);
 if(a->usb_mode10==1){const storage_disk*d=a->usb_selected10?storage_get(a->usb_selected10-1):0;if(d&&(!d->readable||d->transport!=STORAGE_USB||d->context!=a->usb_context10)){a->usb_selected10=0;d=0;}selected=d&&d->readable&&d->transport==STORAGE_USB;count=files_drive_count12();if(a->offset>=count)a->offset=0;}
 else{for(unsigned row=0;row<V6_ENTRIES;++row)selected+=selected_row11(a,row);status=usb_listing10(a,a->offset,rows,&count);if(!status&&count&&a->offset>=count){a->offset=0;status=usb_listing10(a,0,rows,&count);}}
 if(status){usb_notice10(a,status);files_empty12(x,start,width,file_body_bottom11(w)-start,ICON12_USB,status==B_ABSENT?"This drive is disconnected":"This location is unavailable","Choose USB drives to select a connected drive.");count=0;}
 else if(!count)files_empty12(x,start,width,file_body_bottom11(w)-start,ICON12_USB,a->usb_mode10==1?"No USB drive is connected":"This USB folder is empty",a->usb_mode10==1?"Connect a USB drive, then choose Refresh.":"Use Back, Up or Home to continue browsing.");
 else for(unsigned i=0;i<rows&&a->offset+i<count;++i){
  desktop_rect r=icons?(desktop_rect){x+(int)(i%columns)*(width/(int)columns),start+(int)(i/columns)*112,width/(int)columns-8,108}:(desktop_rect){x,start+(int)i*44,width,36};
  unsigned disk=0,folder=0,command=USB_ROW10+i,chosen=a->usb_mode10==2?selected_row11(a,a->offset+i):0,icon;uint64_t bytes=0;char label[256];const char*type;
  if(a->usb_mode10==1){disk=files_drive_at12(a->offset+i);const storage_disk*d=storage_get(disk);command=USB_DISK10+disk;chosen=a->usb_selected10==disk+1;char number[24];decimal(number,disk+1);copy(label,"USB drive ",256);append(label,number,256);bytes=d->sectors*d->sector_bytes;type="USB drive";icon=ICON12_USB;}
  else{rem10_entry*e=&usb_rows10[i];copy(label,e->name,256);folder=e->kind==2;bytes=e->size;type=files_type_name12(label,e->kind);icon=shell_path_icon12(label,e->kind);}
  files_row_state12(w,token,r,command,chosen);file_control11(token,r,command);access_capture16(token,command,label,3);
  if(icons){ui12_icon(icon,r.x+(r.width-48)/2,r.y+7,48,preferences.dark);files_icon_label12((desktop_rect){r.x+6,r.y+62,r.width-12,42},label);}
  else{ui12_icon(icon,r.x+10,r.y+5,24,preferences.dark);files_details_text12(r,label,type,bytes,folder);}
 }
 files_footer12(w,a,token,count,selected,a->usb_mode10==1?"Opening a drive never formats or erases it.":"USB order is unchanged. Safe remove before unplugging.");
}
