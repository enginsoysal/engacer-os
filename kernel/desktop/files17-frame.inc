/* One compact frame across native folders and the existing USB providers. */
static void files_frame17(desktop_window*w,application*a,uint64_t token){
 int x=w->bounds.x+16,y=w->bounds.y+46,width=w->bounds.width;unsigned sidebar=file_sidebar11(w);navigation72*h=&navigation[a-apps];
 files_nav_button12(token,x,y,NAV_BACK,ICON12_BACK,ui12_history_can(h,0));files_nav_button12(token,x+48,y,NAV_FORWARD,ICON12_FORWARD,ui12_history_can(h,1));
 unsigned up=a->usb_mode10==2||(!a->usb_mode10&&!equal(a->path,"/"));files_nav_button12(token,x+96,y,FILE_UP,ICON12_UP,up);files_nav_button12(token,x+144,y,F12_REFRESH,ICON12_REFRESH,1);
 int filter_width=width>=900?208:176,address_width=width-32-192-filter_width-8;
 file_breadcrumbs11(w,a,token,(desktop_rect){x+192,y,address_width,36});files_filter17_draw(w,a,token,(desktop_rect){x+width-32-filter_width,y,filter_width,36});
 int by=y+40,next=0;if(!sidebar){button(token,x,by,72,"Places",F11_PLACES,0);next=80;}
 if(!a->usb_mode10){unsigned bin=file_is_bin11(a->path);
  file_button11(token,x+next,by,112,bin?"Restore":"New folder",bin?F11_RESTORE:FILE_FOLDER,files_can_command12(token,bin?F11_RESTORE:FILE_FOLDER),1);next+=120;
  if(width>=700){file_button11(token,x+next,by,64,"Copy",F11_COPY,files_can_command12(token,F11_COPY),0);next+=72;file_button11(token,x+next,by,56,"Cut",F11_CUT,files_can_command12(token,F11_CUT),0);next+=64;}
  if(width>=600){file_button11(token,x+next,by,72,"Paste",F11_PASTE,files_can_command12(token,F11_PASTE),0);next+=80;}
  if(width>=1000){file_button11(token,x+next,by,108,"Rename",F11_RENAME,files_can_command12(token,F11_RENAME),0);next+=116;file_button11(token,x+next,by,108,"Recycle",F11_RECYCLE,files_can_command12(token,F11_RECYCLE),0);next+=116;}
  file_button11(token,x+next,by,72,"More",F12_COMMANDS,1,0);
 }else if(a->usb_mode10==2){unsigned ready=files_usb_ready12(a),can_copy=ready&&!files_busy12()&&(a->usb_source10[0]?storage_writable(storage_get(a->usb_disk10)):files_can_command12(token,F11_COPY));
  file_button11(token,x+next,by,168,a->usb_source10[0]?"Copy here":"Copy to Downloads",a->usb_source10[0]?USB_EXPORT10:USB_IMPORT10,can_copy,1);next+=176;
  file_button11(token,x+next,by,112,"Safe remove",USB_EJECT10,ready&&!files_busy12(),0);next+=120;
  if(width>=800)file_button11(token,x+next,by,72,"More",F12_COMMANDS,1,0);
 }else ui73_fit(x+next,by+9,width-next-216,"Connected USB drives",UI12_SECONDARY,ink());
 file_button11(token,w->bounds.x+width-(a->usb_mode10&&width<600?100:188),by,84,file_windows11[a-apps].view?"Details":"Icons",F11_VIEW,1,0);
 if(!a->usb_mode10||width>=600)file_button11(token,w->bounds.x+width-96,by,80,"Sort",F11_SORT,!a->usb_mode10,0);
 if(sidebar){int top=file_body_top11(w),bottom=file_body_bottom11(w);ui12_palette p=desktop_palette16();ui73_round(x,top,176,bottom-top,5,p.surface);
  const char*places[]={"Home","Desktop","Documents","Downloads","Pictures","System drive","USB drives","Recycle Bin"};
  const unsigned icons[]={ICON12_HOME,ICON12_FOLDER,ICON12_FOLDER,ICON12_DOWNLOADS,ICON12_IMAGES,ICON12_VOLUME,ICON12_USB,ICON12_TRASH};
  for(unsigned i=0;i<8;++i){char path[256];if(!i)home72(path);else if(i<5)root_path(path,places[i]);else if(i==5)copy(path,"/",256);else if(i==7)file_bin_path11(path,0);else path[0]=0;
   unsigned chosen=i==6?a->usb_mode10!=0:!a->usb_mode10&&equal(path,a->path),command=i<6?NAV_HOME+i:i==6?USB_OPEN10:F11_BIN;
   desktop_rect r={x+4,top+8+(int)i*38,168,36};unsigned state=component_state12(token,command);
   if(chosen||(state&(UI12_HOVER|UI12_PRESSED|UI12_FOCUS)))ui73_round(r.x,r.y,r.width,r.height,5,chosen?file_tint11():p.surface);
   ui12_icon_ink(icons[i],r.x+8,r.y+8,20,p.ink);ui73_fit(r.x+36,r.y+8,r.width-44,places[i],UI12_BODY,p.ink);file_control11(token,r,command);access_capture16(token,command,places[i],1);if(state&UI12_FOCUS)file_focus_rect11(r);
  }
 }
}
static void files_footer17(desktop_window*w,application*a,uint64_t token,unsigned count,unsigned selected,const char*message){
 int x=w->bounds.x+16,width=w->bounds.width,reserve=a->notice[0]?76:48,y=w->bounds.y+w->bounds.height-reserve;
 unsigned page=a->usb_mode10?files_usb_rows12(w):file_page_size11(w);file_filter17*f=files_filter17_for((unsigned)(a-apps));
 files_nav_button12(token,x,y,NAV_PREVIOUS,ICON12_BACK,count&&a->offset!=0);files_nav_button12(token,x+48,y,NAV_NEXT,ICON12_FORWARD,a->offset+page<count);
 char info[128],number[24];decimal(number,count);copy(info,number,sizeof(info));append(info,!a->usb_mode10&&f&&f->query[0]?" matches | ":count==1?" item | ":" items | ",sizeof(info));decimal(number,selected);append(info,number,sizeof(info));append(info," selected",sizeof(info));
 ui12_palette p=desktop_palette16();int info_width=width>=760?280:220;ui73_fit(x+104,y+9,info_width,info,UI12_SECONDARY,p.ink);
 const char*hint=files_nav_hint12(token,hover12);if(!hint&&control_active)hint=files_nav_hint12(token,(i11_target){focused_control_window,focused_action,I11_BUTTON});
 int details=file_job_result11[0]&&!files_busy12()?88:0;ui73_fit(x+112+info_width,y+9,width-32-120-info_width-details,hint?hint:!a->usb_mode10&&f&&f->query[0]?"Name filter active":a->usb_mode10?message:"System folders",UI12_SECONDARY,p.muted);
 if(details)button(token,w->bounds.x+width-96,y,80,"Details",F11_JOB_DETAILS,0);
 if(a->notice[0])ui73_fit(x,w->bounds.y+w->bounds.height-26,width-32,a->notice,UI12_SECONDARY,p.ink);
 if(file_job_state11.active&&file_job_state11.owner==token)file_job_draw11(token,x,w->bounds.y+w->bounds.height-reserve-62,width-32);
}
