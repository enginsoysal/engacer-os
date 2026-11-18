/* Retained native file surfaces, using the shared scalable font/compositor. */
static unsigned file_sidebar11(const desktop_window*w){
#ifdef ENGINE_M12
 return ui12_files_sidebar(w->bounds.width,w->bounds.height);
#else
 return w->bounds.width>=700&&w->bounds.height>=540;
#endif
}
static int file_body_top11(const desktop_window*w){
#ifdef ENGINE_M12
 #ifdef ENGINE_M13
 return w->bounds.y+132;
#else
 return w->bounds.y+142;
#endif
#else
 return w->bounds.y+(w->bounds.height>=360?142:98);
#endif
}
static int file_body_bottom11(const desktop_window*w){uint64_t token=desktop_token(&model,(unsigned)(w-model.windows));
#ifdef ENGINE_M13
 unsigned reserve=apps[w-model.windows].notice[0]?82:54;
#else
 unsigned reserve=82;
#endif
 return w->bounds.y+w->bounds.height-(int)reserve-(file_job_state11.active&&file_job_state11.owner==token?64:0);}
static unsigned file_columns11(const desktop_window*w){unsigned slot=(unsigned)(w-model.windows);if(!file_windows11[slot].view)return 1;int width=w->bounds.width-32-(file_sidebar11(w)?
#ifdef ENGINE_M13
 192
#else
 170
#endif
 :0);
#ifdef ENGINE_M12
 width-=24;
#endif
 #ifdef ENGINE_M12
 return ui12_file_columns_count(width,1);
#endif
 unsigned columns=width>150?(unsigned)width/150:1;return columns?columns:1;}
static unsigned file_rows11(const desktop_window*w){int height=file_body_bottom11(w)-file_body_top11(w);unsigned icons=file_windows11[w-model.windows].view;
#ifdef ENGINE_M12
 return ui12_file_rows_count(height,icons);
#endif
 int rows=icons?(height-8)/100:(height-40)/44;if(rows<1)rows=1;if(rows>128)rows=128;return(unsigned)rows;}
static unsigned file_page_size11(const desktop_window*w){unsigned count=file_rows11(w)*file_columns11(w);return count>128?128:count;}
static uint32_t file_tint11(void){uint32_t base=paper(),accent=preferences.accent,result=0;for(unsigned shift=0;shift<24;shift+=8)result|=((3*((base>>shift)&255)+((accent>>shift)&255))/4)<<shift;return result;}
static void file_control11(uint64_t token,desktop_rect rect,unsigned command){if(control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){rect,token,command};}
static void file_button11(uint64_t token,int x,int y,int width,const char*label,unsigned command,unsigned enabled,unsigned primary){
#ifdef ENGINE_M12
 unsigned icon=command==NAV_BACK||command==NAV_PREVIOUS?ICON12_BACK:command==NAV_FORWARD||command==NAV_NEXT?ICON12_FORWARD:command==FILE_UP?ICON12_UP:command==F11_COPY?ICON12_COPY:command==F11_CUT?ICON12_CUT:command==F11_PASTE?ICON12_PASTE:0;
 if(enabled&&icon&&(width<60||ui73_measure(label,1)<=(unsigned)(width-35))){icon_button12(token,x,y,width,label,command,primary,icon);return;}
#endif
 if(enabled)button(token,x,y,width,label,command,primary);
#ifdef ENGINE_M12
 else component_button12(token,(desktop_rect){x,y,width,36},label,command,primary,0);
#else
 else{ui73_round(x,y,width,36,6,desktop_dark16()?0x20343c:0xecf0f2);ui73_fit(x+10,y+8,width-20,label,1,desktop_dark16()?0x87999e:0x78868d);}
#endif
}
static void file_size_text11(char*out,uint64_t size){const char*units[]={" B"," KiB"," MiB"," GiB"};unsigned unit=0;uint64_t divisor=1;while(unit<3&&size/divisor>=1024){divisor*=1024;++unit;}char number[24];decimal(number,size/divisor);copy(out,number,48);if(unit){append(out,".",48);decimal(number,(size%divisor)*10/divisor);append(out,number,48);}append(out,units[unit],48);}
#ifdef ENGINE_M12
 static const char *file_type_text11(const v6_entry*e){return files_type_name12(file_label11(e),e->kind);}
#else
static const char *file_type_text11(const v6_entry*e){if(e->kind==2)return "Folder";char extension[12];file_extension11(extension,file_label11(e));if(equal(extension,"link"))return "Shortcut";if(equal(extension,"txt")||equal(extension,"md")||equal(extension,"log"))return "Text document";if(equal(extension,"bmp"))return "BMP image";if(equal(extension,"wav"))return "WAV audio";if(equal(extension,"zip"))return "ZIP archive";if(equal(extension,"msi"))return "MSI package";if(equal(extension,"exe"))return "EXE file";return "File";}
#endif
static void file_icon11(int x,int y,unsigned size,const v6_entry*e){
#ifdef ENGINE_M12
 shell_file_icon12(x,y,size,e);
#else
 if(e->kind==2){folder_icon72(x,y,size,0xf0ce87);return;}ui73_round(x+3,y,size*3/4,size,4,desktop_dark16()?0x91adb7:0xd8e8ef);rectangle((desktop_rect){x+8,y+(int)size/3,(int)size/2,2},0x698e9a);rectangle((desktop_rect){x+8,y+(int)size/2,(int)size/3,2},0x698e9a);if(file_suffix11(file_label11(e),"link")){rectangle((desktop_rect){x,y+(int)size-12,13,12},paper());rectangle((desktop_rect){x+2,y+(int)size-7,8,2},ink());rectangle((desktop_rect){x+8,y+(int)size-10,2,7},ink());}
#endif
}
static void file_focus_rect11(desktop_rect r){
#ifdef ENGINE_M12
 uint32_t stroke=ink();
#else
 uint32_t stroke=preferences.accent;
#endif
 rectangle((desktop_rect){r.x,r.y,r.width,1},stroke);rectangle((desktop_rect){r.x,r.y+r.height-1,r.width,1},stroke);rectangle((desktop_rect){r.x,r.y,1,r.height},stroke);rectangle((desktop_rect){r.x+r.width-1,r.y,1,r.height},stroke);
}
static void file_text_field11(desktop_rect rect,const char*value,unsigned cursor,unsigned anchor,unsigned active,unsigned set_field){
#ifdef ENGINE_M12
 component_field12(rect,active);
#else
 ui73_round(rect.x,rect.y,rect.width,rect.height,6,desktop_dark16()?0x10232c:0xffffff);file_focus_rect11(rect);
#endif
 unsigned n=length(value);if(cursor>n)cursor=n;if(anchor>n)anchor=n;unsigned start=0;char prefix[320];for(;;){copy(prefix,value+start,cursor-start+1);if(ui73_measure(prefix,1)<(unsigned)(rect.width-24)||start==cursor)break;++start;}
 if(active&&cursor!=anchor){unsigned lo=cursor<anchor?cursor:anchor,hi=cursor>anchor?cursor:anchor;if(lo<start)lo=start;if(hi>start){copy(prefix,value+start,lo-start+1);unsigned left=ui73_measure(prefix,1);copy(prefix,value+start,hi-start+1);unsigned right=ui73_measure(prefix,1);if(left>(unsigned)(rect.width-20))left=rect.width-20;if(right>(unsigned)(rect.width-20))right=rect.width-20;if(right>left)rectangle((desktop_rect){rect.x+10+(int)left,rect.y+7,(int)(right-left),22},file_tint11());}}
 ui73_fit(rect.x+10,rect.y+8,rect.width-20,value+start,1,ink());if(active){copy(prefix,value+start,cursor-start+1);unsigned caret=ui73_measure(prefix,1);if(caret<(unsigned)(rect.width-20))rectangle((desktop_rect){rect.x+10+(int)caret,rect.y+7,1,22},ink());}if(set_field){file_field_rect11=rect;file_field_scroll11=start;}}
#ifdef ENGINE_M13
#include "files17-ui.inc"
#endif
static void file_breadcrumbs11(desktop_window*w,application*a,uint64_t token,desktop_rect field){
 (void)w;file_window11*f=&file_windows11[a-apps];
 if(f->address_active){file_text_field11(field,f->address,f->cursor,f->anchor,1,0);file_control11(token,field,F11_ADDRESS_FIELD);return;}
#ifdef ENGINE_M12
 if(a->usb_mode10){files_breadcrumbs12(w,a,token,field);return;}
 files_native_breadcrumbs12(a,token,field);return;
#endif
#ifdef ENGINE_M12
 component_field12(field,0);
#else
 ui73_round(field.x,field.y,field.width,field.height,6,desktop_dark16()?0x10232c:0xffffff);
#endif
 int editable=field.width>=130?52:0,right=field.x+field.width-editable;file_control11(token,field,F11_ADDRESS);
 char home[256],bin[256];home72(home);file_bin_path11(bin,0);unsigned recycled=file_in_bin11(a->path),at=recycled?length(bin):file_within11(a->path,home)?length(home):1;const char*root=recycled?"Recycle Bin":at>1?"Home":"System drive";
 int x=field.x+6,width=(int)ui73_measure(root,1)+16;if(width>right-x-6)width=right-x-6;
 if(width>12){ui73_fit(x+4,field.y+8,width-8,root,1,ink());file_control11(token,(desktop_rect){x,field.y,width,36},F11_CRUMB+at);}x+=width+12;
 unsigned last=at;for(unsigned i=at;a->path[i];++i)if(a->path[i]=='/')last=i+1;
 if(last<length(a->path)&&last!=at&&right-x>30){text(x-7,field.y+8,"/",1,ink());ui73_fit(x+5,field.y+8,right-x-12,a->path+last,1,ink());file_control11(token,(desktop_rect){x,field.y,right-x-4,36},F11_CRUMB+length(a->path));}
 if(editable)button(token,right,field.y,editable,"Edit",F11_ADDRESS,0);
}
static void file_job_draw11(uint64_t token,int x,int y,int width){
#ifdef ENGINE_M12
 file_job11*j=&file_job_state11;char label[320],number[24];const char*phase=(j->phase==2||j->phase==4)?"Verifying":j->mode==F11_JOB_COPY?"Copying":j->mode==F11_JOB_MOVE?"Moving":j->mode==F11_JOB_RECYCLE?"Recycling":"Working";
 copy(label,j->cancel?"Cancelling safely":phase,320);if(j->source[0]){append(label,": ",320);append(label,file_basename11(j->source),320);}ui73_fit(x,y,width-124,label,UI12_BODY,ink());
 file_button11(token,x+width-108,y,108,j->cancel?"Cancelling":"Cancel",F11_CANCEL_JOB,!j->cancel,0);
 copy(label,"To: ",320);if(j->target[0])append(label,j->target,320);else if(j->count)append(label,j->roots[0].target,320);ui73_fit(x,y+23,width-124,label,UI12_SECONDARY,ink());
 uint64_t done=j->total_bytes?j->done_bytes:j->mode==F11_JOB_COPY?j->node:j->completed,all=j->total_bytes?j->total_bytes:j->mode==F11_JOB_COPY?j->node_count:j->count;
 unsigned percent=all?(unsigned)(done*100/all):0;if(percent>100)percent=100;
 rectangle((desktop_rect){x,y+48,width-60,5},desktop_dark16()?0x35515a:0xd7e3e8);rectangle((desktop_rect){x,y+48,(width-60)*(int)percent/100,5},preferences.accent);decimal(number,percent);append(number,"%",24);ui73_fit(x+width-52,y+39,52,number,UI12_SECONDARY,ink());
#else
file_job11*j=&file_job_state11;const char*phase=j->mode==F11_JOB_COPY?(j->phase==2?"Verifying copy":"Copying files"):j->mode==F11_JOB_MOVE?"Moving items":j->mode==F11_JOB_RECYCLE?"Moving to Recycle Bin":j->mode==F11_JOB_RESTORE?"Restoring items":j->mode==F11_JOB_LINK?"Creating shortcuts":"Removing selected items";char label[128],number[24];copy(label,phase,128);if(j->source[0]){append(label,": ",128);append(label,file_basename11(j->source),128);}ui73_fit(x,y,width-118,label,1,ink());button(token,x+width-108,y,108,"Cancel",F11_CANCEL_JOB,0);uint64_t done=j->total_bytes?j->done_bytes:j->mode==F11_JOB_COPY?j->node:j->completed,all=j->total_bytes?j->total_bytes:j->mode==F11_JOB_COPY?j->node_count:j->count;unsigned percent=all?(unsigned)(done*100/all):0;if(percent>100)percent=100;rectangle((desktop_rect){x,y+31,width-124,5},desktop_dark16()?0x35515a:0xd7e3e8);rectangle((desktop_rect){x,y+31,(width-124)*(int)percent/100,5},preferences.accent);decimal(number,percent);append(number,"%",24);ui73_fit(x,y+40,width-124,number,1,ink());
#endif
}
static void draw_files11(desktop_window*w,application*a,uint64_t token){
#ifdef ENGINE_M12
 files_frame12(w,a,token);if(a->usb_mode10){files_usb_body12(w,a,token);return;}

#ifdef ENGINE_M13
 (void)file_listing11_for((unsigned)(a-apps),a->path,file_windows11[a-apps].sort,file_windows11[a-apps].descending);
#endif
 int x=w->bounds.x+16,width=w->bounds.width;unsigned sidebar=file_sidebar11(w);
#else
if(a->usb_mode10){draw_usb10(w,a,token);return;}int x=w->bounds.x+16,y=w->bounds.y+49,width=w->bounds.width;unsigned compact=width<600,sidebar=file_sidebar11(w);button(token,x,y,44,"<",NAV_BACK,0);int nav=52;if(!compact){button(token,x+nav,y,44,">",NAV_FORWARD,0);nav+=52;}button(token,x+nav,y,44,"Up",FILE_UP,0);nav+=52;if(!sidebar){button(token,x+nav,y,85,"Places",F11_PLACES,0);nav+=93;}int tools=compact?0:184,address_width=width-32-nav-tools;if(address_width<48)address_width=48;file_breadcrumbs11(w,a,token,(desktop_rect){x+nav,y,address_width,36});if(!compact){button(token,w->bounds.x+width-190,y,82,file_windows11[a-apps].view?"Details":"Icons",F11_VIEW,0);button(token,w->bounds.x+width-100,y,84,"Sort",F11_SORT,0);}
#endif

#ifndef ENGINE_M12
 unsigned selected=file_selected_count11(a),writable=writable72(a->path)&&!file_in_bin11(a->path)&&!m6_volume()->readonly;unsigned bin=file_is_bin11(a->path);
 if(w->bounds.height>=360){int by=y+44;if(bin){file_button11(token,x,by,112,"Restore",F11_RESTORE,selected!=0,1);button(token,x+120,by,174,"Empty Bin...",F11_EMPTY,0);file_button11(token,x+302,by,78,"Copy",F11_COPY,selected!=0,0);}else{file_button11(token,x,by,112,"New folder",FILE_FOLDER,writable,1);int next=120;if(width>=780){file_button11(token,x+next,by,112,"New text file",F11_NEW_TEXT,writable,0);next+=120;}if(width>=600){file_button11(token,x+next,by,72,"Copy",F11_COPY,selected!=0,0);next+=80;file_button11(token,x+next,by,65,"Cut",F11_CUT,selected&&writable,0);next+=73;}file_button11(token,x+next,by,75,"Paste",F11_PASTE,writable&&clipboard_kind11==2&&file_clip11.count,0);next+=83;if(width>=700){file_button11(token,x+next,by,94,"Recycle",F11_RECYCLE,selected&&writable,0);next+=102;file_button11(token,x+next,by,72,"Undo",F11_UNDO,file_undo_state11.kind!=0,0);}}}

#else
 unsigned bin=file_is_bin11(a->path),writable=writable72(a->path);
#endif
 int top=file_body_top11(w),bottom=file_body_bottom11(w),list=x+(sidebar?
#ifdef ENGINE_M13
 192
#else
 170
#endif
 :0),list_width=width-32-(sidebar?
#ifdef ENGINE_M13
 192
#else
 170
#endif
 :0);
#ifdef ENGINE_M12
 list_width-=24;
#endif

#ifndef ENGINE_M12
 if(sidebar){ui73_round(x,top,154,bottom-top,6,desktop_dark16()?0x20363e:0xeaf1f2);text(x+10,top+10,"Places",1,ink());const char*places[]={"Home","Desktop","Documents","Downloads","Pictures","System drive","USB drives","Recycle Bin"};for(unsigned i=0;i<8;++i){char place[256];if(i==0)home72(place);else if(i<5)root_path(place,places[i]);else if(i==5)copy(place,"/",256);else if(i==7)file_bin_path11(place,0);else place[0]=0;button(token,x+6,top+38+(int)i*38,142,places[i],i<6?NAV_HOME+i:i==6?USB_OPEN10:F11_BIN,equal(place,a->path));}}

#endif
#ifdef ENGINE_M12
 if(!files_native_ready12(a)){a->offset=0;ui73_fit(list+12,top+12,list_width-24,"This folder is no longer available",UI12_SECTION,ink());ui73_paragraph(list+12,top+56,list_width-24,3,"Use Back, Home or another place. Refresh checks the same location without changing your files.",ink());files_footer12(w,a,token,0,0,"The original location was kept for navigation.");return;}
#endif
 unsigned count=children72(a),page=file_page_size11(w),columns=file_columns11(w),icons=file_windows11[a-apps].view;if(a->offset>=count)a->offset=count?count-1:0;if(icons)a->offset=a->offset/columns*columns;
 #ifdef ENGINE_M12
 const int tile_height=112,tile_hit=108,tile_icon=48,tile_label=62;
#else
 const int tile_height=100,tile_hit=92,tile_icon=40,tile_label=54;
#endif
 int start=top+6;if(!icons){
#ifdef ENGINE_M12
 files_details_header12(w,token,list,top,list_width,1);
#else
 text(list+10,top+8,"Name",1,ink());if(list_width>=400){text(list+list_width-230,top+8,"Type",1,ink());text(list+list_width-92,top+8,"Size",1,ink());}rectangle((desktop_rect){list,top+34,list_width,1},desktop_dark16()?0x35515a:0xd7e3e8);
#endif
 start=top+42;}
 for(unsigned i=0;i<page&&a->offset+i<count;++i){unsigned row=a->offset+i;const v6_entry*e=child_at(a,row);if(!e)break;desktop_rect rect=icons?(desktop_rect){list+(int)(i%columns)*(list_width/(int)columns),start+(int)(i/columns)*tile_height,list_width/(int)columns-8,tile_hit}:(desktop_rect){list,start+(int)i*44,list_width,36};unsigned chosen=selected_row11(a,row);
#ifdef ENGINE_M12
 files_row_state12(w,token,rect,FILE_ROW+row,chosen);
 access_capture16(token,FILE_ROW+row,file_label11(e),3);
#else
 if(chosen)ui73_round(rect.x,rect.y,rect.width,rect.height,6,file_tint11());if(chosen||(model.focused==(unsigned)(w-model.windows)&&!control_active&&selection_focus11[a-apps]==row))file_focus_rect11(rect);
#endif
 file_control11(token,rect,FILE_ROW+row);
  if(icons){file_icon11(rect.x+(rect.width-tile_icon)/2,rect.y+7,tile_icon,e);
#ifdef ENGINE_M12
 files_icon_label12((desktop_rect){rect.x+6,rect.y+tile_label,rect.width-12,42},file_label11(e));
#else
 ui73_paragraph(rect.x+6,rect.y+tile_label,rect.width-12,2,file_label11(e),ink());
#endif
}
  else{file_icon11(rect.x+10,rect.y+5,24,e);
#ifdef ENGINE_M12
 files_details_text12(rect,file_label11(e),file_type_text11(e),e->size,e->kind==2);
#else
 int name_width=list_width-(list_width>=400?282:46);ui73_fit(rect.x+44,rect.y+8,name_width,file_label11(e),1,ink());if(list_width>=400){ui73_fit(rect.x+list_width-230,rect.y+8,130,file_type_text11(e),1,ink());char size[48];if(e->kind==2)copy(size,"-",48);else file_size_text11(size,e->size);ui73_fit(rect.x+list_width-92,rect.y+8,90,size,1,ink());}
#endif
}
 }
 if(!count){
#ifdef ENGINE_M12
 #ifdef ENGINE_M13
 file_filter17*filter=files_filter17_for((unsigned)(a-apps));if(filter&&filter->query[0])files_empty12(list,start,list_width,bottom-start,ICON12_FOLDER,"No matching names","Clear the filter or try a shorter name. Your files have not changed.");else
#endif
 files_empty12(list,start,list_width,bottom-start,bin?ICON12_TRASH:ICON12_FOLDER,bin?"The Recycle Bin is empty.":"This folder is empty.",bin?"Recycled items appear here.":writable?"Use New folder or Paste.":"Choose Home for your files.");
#else
if(bottom-start>=145){folder_icon72(list+22,start+18,50,0xf0ce87);ui73_fit(list+22,start+84,list_width-44,bin?"The Recycle Bin is empty.":"This folder is empty.",2,ink());ui73_fit(list+22,start+120,list_width-44,bin?"Recycled items will appear here with Restore actions.":writable?"Create a folder, create a text file, or Paste items here.":"This location is protected.",1,ink());}else ui73_fit(list+12,start+12,list_width-24,bin?"The Recycle Bin is empty.":"This folder is empty.",1,ink());
#endif
 }
#ifdef ENGINE_M12
 unsigned units=icons?columns:1;component_scrollbar12(token,(desktop_rect){w->bounds.x+width-36,start,20,bottom-start},a->offset/units,icons?file_rows11(w):page,(count+units-1)/units,units);
#endif

#ifdef ENGINE_M12
 files_footer12(w,a,token,count,file_selected_count11(a),bin?"Restore items to their original folders. Permanent removal needs review.":"Click selects. Double-click or Enter opens. Right-click shows actions.");
#else
 int footer=w->bounds.y+w->bounds.height-76;button(token,x,footer,40,"<",NAV_PREVIOUS,0);button(token,x+48,footer,40,">",NAV_NEXT,0);char info[96],number[24];decimal(number,count);copy(info,number,96);append(info,count==1?" item | ":" items | ",96);decimal(number,selected);append(info,number,96);append(info," selected",96);ui73_fit(x+104,footer+8,width-136-(file_job_error11?108:0),info,1,ink());if(file_job_error11)button(token,w->bounds.x+width-118,footer,102,"Details",F11_JOB_DETAILS,0);
 ui73_fit(x,w->bounds.y+w->bounds.height-26,width-32,a->notice[0]?a->notice:bin?"Restore items to their original folders. Permanent removal needs review.":"Click selects. Double-click or Enter opens. Right-click shows actions.",5,ink());if(file_job_state11.active&&file_job_state11.owner==token)file_job_draw11(token,x,w->bounds.y+w->bounds.height-138,width-32);
#endif
}
static void file_dialog_button11(int x,int y,int width,const char*label,unsigned command,unsigned enabled,unsigned primary,unsigned index,unsigned danger){file_dialog11*d=&file_dialog_state11;if(danger&&enabled){ui73_round(x,y,width,36,6,0xb63d45);ui73_fit(x+10,y+8,width-20,label,1,0xffffff);file_control11(d->owner,(desktop_rect){x,y,width,36},command);}else file_button11(d->owner,x,y,width,label,command,enabled,primary);if(enabled&&d->focus==index)file_focus_rect11((desktop_rect){x-2,y-2,width+4,40});}
static void files_draw_dialog11(void){
#ifdef ENGINE_M12
 if(picker_draw12())return;
#endif
file_dialog11*d=&file_dialog_state11;if(!d->mode||!file_dialog_owner_focused11())return;int width=model.width>720?660:(int)model.width-40,height=d->mode==F11_DLG_PROPERTIES||d->mode==F11_DLG_RESULT?420:d->mode==F11_DLG_OPEN_WITH?370:d->mode==F11_DLG_CONFLICT?340:300;if(height>(int)model.height-100)height=(int)model.height-100;if(height<180)height=180;int x=((int)model.width-width)/2,y=((int)model.height-60-height)/2;if(y<8)y=8;desktop_shadow16(x,y,width,height);ui73_round(x,y,width,height,12,paper());const char*title=d->mode==F11_DLG_RENAME?"Rename item":d->mode==F11_DLG_NEW_FOLDER?"Create a folder":d->mode==F11_DLG_NEW_TEXT?"Create a text file":d->mode==F11_DLG_CONFLICT?"Choose what to keep":d->mode==F11_DLG_PROPERTIES?"Properties":d->mode==F11_DLG_OPEN_WITH?"Choose an app":d->mode==F11_DLG_RESULT?"File operation details":"Delete permanently?";ui73_fit(x+24,y+22,width-48,title,2,ink());
 if(d->mode==F11_DLG_RENAME||d->mode==F11_DLG_NEW_FOLDER||d->mode==F11_DLG_NEW_TEXT){ui73_fit(x+24,y+65,width-48,d->mode==F11_DLG_RENAME?"Your file contents stay the same.":d->mode==F11_DLG_NEW_FOLDER?"Give this folder a name that makes sense to you.":"Create an empty text file, then open it when you are ready.",1,ink());text(x+24,y+103,"Name",1,ink());desktop_rect field={x+24,y+128,width-48,40};file_text_field11(field,d->input,d->cursor,d->anchor,d->focus==0,1);file_control11(d->owner,field,F11_NAME_FIELD);ui73_paragraph(x+24,y+180,width-48,height>=280?2:1,d->error[0]?d->error:"Enter confirms. Escape cancels. The original is kept until the change is saved.",d->error[0]?0xc75652:ink());file_dialog_button11(x+24,y+height-54,150,d->mode==F11_DLG_RENAME?"Rename":"Create",F11_DIALOG_OK,1,1,1,0);file_dialog_button11(x+width-144,y+height-54,120,"Cancel",F11_DIALOG_CANCEL,1,0,2,0);}
 else if(d->mode==F11_DLG_CONFLICT){char message[128],number[24];decimal(number,file_job_state11.conflicts);copy(message,number,128);append(message," matching names already exist. Nothing is overwritten by default.",128);ui73_paragraph(x+24,y+66,width-48,2,message,ink());ui73_paragraph(x+24,y+124,width-48,2,file_job_state11.replace_allowed?"Replace permanently replaces the reviewed destination files. Keep both saves separate names.":"Folder replacement or replacement of an open/protected item is unavailable. Choose Keep both or Skip.",ink());int bw=(width-56)/2;file_dialog_button11(x+24,y+height-100,bw,"Keep both",F11_KEEP_BOTH,1,1,0,0);file_dialog_button11(x+32+bw,y+height-100,bw,"Skip matches",F11_SKIP,1,0,1,0);file_dialog_button11(x+24,y+height-54,bw,"Replace files",F11_REPLACE,file_job_state11.replace_allowed,0,2,1);file_dialog_button11(x+32+bw,y+height-54,bw,"Cancel",F11_DIALOG_CANCEL,1,0,3,0);}
 else if(d->mode==F11_DLG_OPEN_WITH){ui73_fit(x+24,y+65,width-48,file_basename11(d->path),1,ink());const unsigned choices[]={EDITOR,IMAGES74,ARCHIVES74,MEDIA74,BROWSER74,WINDOWS8};unsigned row=0;for(unsigned i=0;i<6;++i)if(app7_available(choices[i])){int bw=(width-56)/2;file_dialog_button11(x+24+(int)(row%2)*(bw+8),y+100+(int)(row/2)*44,bw,titles[choices[i]],F11_ASSOC_APP+choices[i],1,0,row,0);++row;}char extension[12],label[80];file_extension11(extension,d->path);copy(label,d->always?"[x] Always use for .":"[ ] Always use for .",80);append(label,extension[0]?extension:"(no extension)",80);file_dialog_button11(x+24,y+height-54,width-192,label,F11_ALWAYS,extension[0]!=0,0,row,0);file_dialog_button11(x+width-144,y+height-54,120,"Cancel",F11_DIALOG_CANCEL,1,0,row+1,0);}
 else if(d->mode==F11_DLG_PROPERTIES){const v6_entry*e=d->provider==F11_USB?0:entry(d->path);const char*name=e?file_label11(e):file_basename11(d->path);ui73_fit(x+24,y+65,width-48,name[0]?name:"System drive",1,ink());text(x+24,y+104,"Type",1,ink());ui73_fit(x+136,y+104,width-160,e?file_type_text11(e):d->provider==F11_USB?(d->item_kind==2?"USB folder":"USB file"):equal(d->path,"/")?"Native system drive":"Unavailable item",1,ink());char size[80],number[24];uint64_t bytes=e?e->size:d->provider==F11_USB?d->size:0;decimal(number,bytes);copy(size,e&&e->kind==2?"Folder metadata":number,80);if(!e||e->kind!=2)append(size," bytes",80);text(x+24,y+136,"Size",1,ink());ui73_fit(x+136,y+136,width-160,size,1,ink());char location[256];copy(location,d->path,256);recycle_record11 record;char meta[256];if(e&&!file_trash_record11(e->path,&record,meta))copy(location,record.original,256);text(x+24,y+170,file_in_bin11(d->path)?"Original location":"Location",1,ink());unsigned lines=height>252?(unsigned)(height-252)/21:1;if(lines>4)lines=4;if(!lines)lines=1;ui73_paragraph(x+24,y+198,width-48,lines,location,ink());file_dialog_button11(x+width-144,y+height-54,120,"Close",F11_DIALOG_CANCEL,1,1,0,0);}
 else if(d->mode==F11_DLG_RESULT){
#ifdef ENGINE_M12
  file_job11*j=&file_job_state11;ui73_paragraph(x+24,y+65,width-48,3,file_job_result11,ink());
  if(height>=380){const char*source=j->source[0]?j->source:j->count?j->roots[0].source:"";const char*target=j->target[0]?j->target:j->count?j->roots[0].target:"";
   text(x+24,y+146,"From",UI12_SECONDARY,ink());ui73_paragraph(x+24,y+169,width-48,2,source,ink());text(x+24,y+225,"To",UI12_SECONDARY,ink());ui73_paragraph(x+24,y+248,width-48,2,target,ink());}
#else
 ui73_paragraph(x+24,y+70,width-48,height>260?6:3,file_job_result11,ink());
#endif
 file_dialog_button11(x+width-144,y+height-54,120,"Close",F11_DIALOG_CANCEL,1,1,0,0);}

 else{ui73_paragraph(x+24,y+70,width-48,3,d->mode==F11_DLG_EMPTY?"Permanently remove every item and folder in the Recycle Bin. This cannot be undone.":"Permanently remove the selected items and their contents. This cannot be undone.",ink());if(d->error[0])ui73_paragraph(x+24,y+150,width-48,2,d->error,0xc75652);file_dialog_button11(x+24,y+height-54,width>500?210:width/2-28,"Delete permanently",F11_DIALOG_OK,1,0,0,1);file_dialog_button11(x+width-144,y+height-54,120,"Cancel",F11_DIALOG_CANCEL,1,0,1,0);}
}
static void files_draw_context11(void){if(!context11)return;unsigned visible=file_menu_visible11(),width=file_menu_width14();if(context_choice11<file_menu_scroll11)file_menu_scroll11=context_choice11;if(context_choice11>=file_menu_scroll11+visible)file_menu_scroll11=context_choice11-visible+1;int x=(int)context_x11,y=(int)context_y11;desktop_shadow16(x,y,width,visible*38+file_menu_footer14());ui73_round(x,y,width,visible*38+file_menu_footer14(),8,paper());for(unsigned i=0;i<visible&&file_menu_scroll11+i<file_menu_count11;++i){unsigned index=file_menu_scroll11+i;file_menu11*item=&file_menu_items11[index];file_button11(context_window11,x+6,y+6+(int)i*38,width-12,item->label,32000+index,item->enabled,context_choice11==index);}ui73_paragraph(x+10,y+10+(int)visible*38,width-20,2,file_menu_count11>visible?"Scroll or use arrow keys for more actions.":file_menu_reason11[0]?file_menu_reason11:"Escape closes this menu.",ink());}
static void files_draw_overlay11(void){files_draw_dialog11();desktop_window*owner_window=file_owner_window11(file_job_state11.owner);if(file_job_state11.active&&(!owner_window||owner_window->minimized)){int y=(int)model.height-124;ui73_round(16,y,model.width-32,60,8,paper());file_job_draw11(0,28,y+5,model.width-56);}else if(file_job_error11&&(!owner_window||owner_window->minimized)){int y=(int)model.height-108;ui73_round(16,y,model.width-32,42,8,paper());ui73_fit(28,y+10,model.width-180,"A file operation stopped. Review the completed items and reason.",1,ink());button(0,(int)model.width-128,y+3,104,"Details",F11_JOB_DETAILS,0);}if(file_drag11){int x=(int)file_drag_x11+16,y=(int)file_drag_y11+20;if(x+280>(int)model.width)x=(int)model.width-286;if(y+54>(int)model.height-60)y=(int)model.height-118;ui73_round(x,y,280,52,8,paper());char label[80],number[24];decimal(number,file_drag_count11);copy(label,file_drag_copy11?"Copy ":"Move ",80);append(label,number,80);append(label," items",80);text(x+10,y+6,label,1,ink());ui73_fit(x+10,y+29,260,"Drop onto a folder. Escape cancels.",1,ink());}}
static unsigned file_modal_control11(uint64_t token,unsigned command){
#ifdef ENGINE_M12
 if(picker_control12(token,command))return 1;
#endif
return file_dialog_state11.mode&&file_dialog_owner_focused11()&&file_dialog_state11.owner==token&&((command>=F11_DIALOG_OK&&command<=F11_ALWAYS)||(command>=F11_ASSOC_APP&&command<F11_ASSOC_APP+APP74_KINDS)||command==F11_NAME_FIELD);}
static unsigned file_block_control11(uint64_t token,unsigned command){return command!=70&&command!=0&&!(command>=42000&&command<43400)&&file_dialog_state11.mode&&file_dialog_state11.owner==token&&!file_modal_control11(token,command);}
static unsigned file_block_owner11(uint64_t token){return file_dialog_state11.mode&&file_dialog_state11.owner==token;}
