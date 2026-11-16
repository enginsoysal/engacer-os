/* Shared file presentation; provider capabilities remain separate from view. */
static desktop_rect files_tip_bounds12;
static const char*files_type_name12(const char*name,unsigned kind){return ui12_file_type(name,kind);}
static void files_usb_view_path12(char*out){copy(out,"/System/Settings/usb-view12-",256);append(out,owner.user,256);append(out,".bin",256);}
static void files_usb_view_load12(void){char path[256];unsigned data[4],bytes=0;usb_view12=0;files_usb_view_path12(path);if(!v6_verify(m6_volume(),path)&&!v6_read(m6_volume(),path,0,data,sizeof(data),&bytes)&&bytes==sizeof(data)&&data[0]==0x36565755&&data[1]==1&&data[2]<=1&&!data[3])usb_view12=data[2];}
static unsigned files_usb_view_save12(void){char path[256];unsigned data[4]={0x36565755,1,usb_view12,0};files_usb_view_path12(path);return v6_put(m6_volume(),path,sizeof(data),memory_source,data);}
static void files_reveal_view12(desktop_window*w,application*a){
 unsigned row=0,chosen=0,page=a->usb_mode10?files_usb_rows12(w):file_page_size11(w);
 if(a->usb_mode10==1&&a->usb_selected10){unsigned count=files_drive_count12();while(row<count&&files_drive_at12(row)+1!=a->usb_selected10)++row;chosen=row<count;}
 else if(a->usb_mode10==2&&a->usb_selected10){row=a->usb_selected10-1;chosen=1;}
 else if(!a->usb_mode10){row=selection_focus11[a-apps];chosen=selected_row11(a,row);}
 if(chosen)a->offset=row/page*page;
}
static void files_order12(desktop_window*w,application*a,unsigned key,unsigned toggle){
 unsigned slot=(unsigned)(a-apps);file_window11*f=&file_windows11[slot];unsigned focused=selection_index11(a,selection_focus11[slot]),anchor=selection_index11(a,selection_anchor11[slot]);
 if(toggle&&f->sort==key)f->descending^=1;else{f->sort=key;f->descending=0;}file_lists11[slot].generation=0;a->offset=0;
 file_listing11*l=file_listing11_for(slot,a->path,f->sort,f->descending);for(unsigned i=0;i<l->count;++i){if(l->order[i]==focused)selection_focus11[slot]=i;if(l->order[i]==anchor)selection_anchor11[slot]=i;}
 if(focused<V6_ENTRIES&&(selected11[slot][focused/8]&(1u<<(focused%8)))){unsigned page=file_page_size11(w);a->offset=selection_focus11[slot]/page*page;}
 unsigned status=file_save_view11(a);if(status)notice(a,"Order changed for this window; saving the preference failed.");else a->notice[0]=0;interaction11.last_valid=0;control_active=0;invalidate(w->bounds);
}
static unsigned files_column_action12(desktop_window*w,application*a,uint64_t token,unsigned command){
 if(command<F12_COLUMN_NAME||command>F12_COLUMN_TYPE)return 0;
 if(w->app==FILES&&!a->usb_mode10&&!file_block_owner11(token))files_order12(w,a,command-F12_COLUMN_NAME,1);return 1;
}
static void files_header_cell12(desktop_window*w,uint64_t token,desktop_rect r,const char*label,unsigned key,unsigned enabled){
 file_window11*f=&file_windows11[w-model.windows];unsigned command=F12_COLUMN_NAME+key,state=enabled?component_state12(token,command):0;ui12_palette p=ui12_theme(preferences.dark,preferences.accent);
 if(state&(UI12_HOVER|UI12_PRESSED|UI12_FOCUS)){ui12_style s=ui12_control_style(p,state,0);ui73_round(r.x,r.y,r.width,r.height,4,s.fill);if(state&UI12_FOCUS)file_focus_rect11(r);}
 ui73_fit(r.x+10,r.y+8,r.width-20,label,UI12_BODY,p.ink);if(enabled){file_control11(token,r,command);if(f->sort==key){int x=r.x+18+(int)ui73_measure(label,UI12_BODY),y=r.y+14;for(int n=0;n<5;++n)rectangle((desktop_rect){x+n,y+(f->descending?n:4-n),9-2*n,1},p.ink);}}
}
static void files_details_header12(desktop_window*w,uint64_t token,int x,int top,int width,unsigned native){
 ui12_file_columns c=ui12_file_details(width);files_header_cell12(w,token,(desktop_rect){x,top,c.name,32},"Name",0,native);
 if(c.type_visible)files_header_cell12(w,token,(desktop_rect){x+c.name+12,top,c.type,32},"Type",2,native);
 if(c.size_visible)files_header_cell12(w,token,(desktop_rect){x+width-c.size,top,c.size,32},"Size",1,native);
 rectangle((desktop_rect){x,top+34,width,1},ui12_theme(preferences.dark,preferences.accent).line);
}
static void files_details_text12(desktop_rect r,const char*name,const char*type,uint64_t bytes,unsigned folder){
 ui12_file_columns c=ui12_file_details(r.width);ui73_fit(r.x+44,r.y+8,c.name-46,name,UI12_BODY,ink());
 if(c.type_visible)ui73_fit(r.x+c.name+22,r.y+8,c.type-12,type,UI12_BODY,ink());
 if(c.size_visible){char size[48];if(folder)copy(size,"-",48);else file_size_text11(size,bytes);ui73_fit(r.x+r.width-c.size+10,r.y+8,c.size-12,size,UI12_BODY,ink());}
}
static void files_row_state12(desktop_window*w,uint64_t token,desktop_rect r,unsigned command,unsigned chosen){
 unsigned active=model.focused==(unsigned)(w-model.windows)&&!desktop_focus11,hover=hover12.window==token&&hover12.action==command&&hover12.kind==I11_ITEM;ui12_palette p=ui12_theme(preferences.dark,preferences.accent);
 if(chosen)ui73_round(r.x,r.y,r.width,r.height,6,active?file_tint11():ui12_mix(p.paper,p.ink,1,12));else if(hover)ui73_round(r.x,r.y,r.width,r.height,6,ui12_mix(p.paper,p.ink,1,24));
 unsigned row=command>=USB_ROW10&&command<USB_ROW10+6?apps[w-model.windows].offset+command-USB_ROW10:command-FILE_ROW;
 if(active&&((!control_active&&selection_focus11[w-model.windows]==row)||chosen))file_focus_rect11(r);
}
static unsigned files_icon_lines12(const char*name,unsigned width,char lines[2][256]){
 unsigned at=0;for(unsigned line=0;line<2;++line){unsigned n=0;while(name[at]&&n<252){lines[line][n]=name[at];lines[line][n+1]=0;if(ui73_measure(lines[line],UI12_BODY)>width)break;++n;++at;}lines[line][n]=0;
  if(line==1&&name[at]){while(n&&ui73_measure(lines[line],UI12_BODY)+ui73_measure("...",UI12_BODY)>width)lines[line][--n]=0;append(lines[line],"...",256);return 1;}}
 return 0;
}
static void files_icon_label12(desktop_rect r,const char*name){char lines[2][256];files_icon_lines12(name,r.width,lines);for(unsigned i=0;i<2;++i)if(lines[i][0]){unsigned width=ui73_measure(lines[i],UI12_BODY);text(r.x+(r.width-(int)width)/2,r.y+(int)i*21,lines[i],UI12_BODY,ink());}}
/* A full-name tip owns no heap buffer and never extends outside its window. */
static unsigned files_tip_content12(i11_target target,char lines[12][64],desktop_rect*out){
 if(target.kind!=I11_ITEM||!target.window||launcher||context11||guide_open11||file_dialog_state11.mode||dragging||interaction11.captured)return 0;
 desktop_window*w=desktop_lookup(&model,target.window);if(!w||w->app!=FILES||w->minimized)return 0;application*a=&apps[w-model.windows];if(a->usb_mode10==1)return 0;
 desktop_rect row={0};for(unsigned i=0;i<control_count;++i)if(controls[i].window==target.window&&controls[i].action==target.action)row=controls[i].rect;if(!row.width)return 0;
 char name[256];if(a->usb_mode10==2){if(target.action<USB_ROW10||target.action>=USB_ROW10+6)return 0;rem10_entry item;unsigned total;if(rem10_list(a->usb_disk10,a->usb_context10,a->usb_part10,a->usb_path10,a->offset+target.action-USB_ROW10,&item,1,&total))return 0;copy(name,item.name,256);}
 else{const v6_entry*e=file_target_entry11(target);if(!e)return 0;copy(name,file_label11(e),256);}
 unsigned icons=file_windows11[w-model.windows].view,available=icons?(unsigned)row.width-12:(unsigned)ui12_file_details(row.width).name-46;
 if(icons){char label_lines[2][256];if(!files_icon_lines12(name,available,label_lines))return 0;}else if(ui73_measure(name,UI12_BODY)<=available)return 0;
 int left=w->bounds.x+12,right=w->bounds.x+w->bounds.width-12,top=w->bounds.y+44,bottom=w->bounds.y+w->bounds.height-12;
 if(left<8)left=8;if(right>(int)model.width-8)right=(int)model.width-8;if(top<8)top=8;if(bottom>(int)model.height-68)bottom=(int)model.height-68;
 int width=right-left;if(width>480)width=480;if(width<160)return 0;unsigned at=0,count=0;
 while(name[at]&&count<12){unsigned n=0;while(name[at]&&n<63){lines[count][n]=name[at];lines[count][n+1]=0;if(ui73_measure(lines[count],UI12_SECONDARY)>(unsigned)(width-24)){lines[count][n]=0;break;}++n;++at;}if(!n)return 0;++count;}
 if(name[at]||!count)return 0;int height=(int)count*21+16;if(height>bottom-top)return 0;int x=row.x+8,y=row.y+row.height+4;if(x+width>right)x=right-width;if(x<left)x=left;if(y+height>bottom)y=row.y-height-4;if(y<top)y=top;*out=(desktop_rect){x,y,width,height};return count;
}
static void files_name_tip_damage12(i11_target next){if(files_tip_bounds12.width)invalidate(files_tip_bounds12);char lines[12][64];desktop_rect r;if(files_tip_content12(next,lines,&r))invalidate(r);}
static void files_name_tip_draw12(void){
 files_tip_bounds12=(desktop_rect){0};
 /* Keyboard window/location changes can leave the last pointer target stale. */
 if(desktop_hit(&model,(int)pointer_x,(int)pointer_y)!=hover12.window)return;
 unsigned under=0;for(unsigned i=0;i<control_count;++i){control*c=&controls[i];desktop_rect r=c->rect;if(c->window==hover12.window&&c->action==hover12.action&&(int)pointer_x>=r.x&&(int)pointer_x<r.x+r.width&&(int)pointer_y>=r.y&&(int)pointer_y<r.y+r.height)under=1;}if(!under)return;
 char lines[12][64];desktop_rect r;unsigned n=files_tip_content12(hover12,lines,&r);if(!n)return;files_tip_bounds12=r;ui12_palette p=ui12_theme(preferences.dark,preferences.accent);ui73_round(r.x,r.y,r.width,r.height,6,p.ink);ui73_round(r.x+1,r.y+1,r.width-2,r.height-2,5,p.surface);for(unsigned i=0;i<n;++i)text(r.x+12,r.y+8+(int)i*21,lines[i],UI12_SECONDARY,p.ink);
}
static void files_native_breadcrumbs12(application*a,uint64_t token,desktop_rect field){
 component_field12(field,0);file_control11(token,field,F11_ADDRESS);int edit=field.width>=130?52:0,right=field.x+field.width-edit;
 char home[256],bin[256],label[256];home72(home);file_bin_path11(bin,0);unsigned root=1;const char*root_name="System drive";
 if(file_in_bin11(a->path)){root=length(bin);root_name="Recycle Bin";}else if(file_within11(a->path,home)){root=length(home);root_name="Home";}
 uint16_t starts[128],ends[128];unsigned count=0,at=root;while(a->path[at]&&count<128){if(a->path[at]=='/'){++at;continue;}starts[count]=(uint16_t)at;while(a->path[at]&&a->path[at]!='/')++at;ends[count++]=(uint16_t)at;}
 int root_width=(int)ui73_measure(root_name,UI12_BODY)+16,total=root_width;
 for(unsigned i=0;i<count;++i){unsigned n=ends[i]-starts[i];memcpy(label,a->path+starts[i],n);label[n]=0;total+=16+(int)ui73_measure(label,UI12_BODY)+16;}
 int x=field.x+6,available=right-x-6;if(root_width>available)root_width=available;
 if(root_width>12){ui73_fit(x+4,field.y+8,root_width-8,root_name,UI12_BODY,ink());file_control11(token,(desktop_rect){x,field.y,root_width,36},F11_CRUMB+root);}x+=root_width;
 unsigned first=0;if(total>available&&count>1){if(right-x>60){text(x+4,field.y+8,"/ ...",UI12_BODY,ink());x+=48;}first=count-1;}
 for(unsigned i=first;i<count&&right-x>28;++i){text(x+4,field.y+8,"/",UI12_BODY,ink());x+=16;unsigned n=ends[i]-starts[i];memcpy(label,a->path+starts[i],n);label[n]=0;int width=(int)ui73_measure(label,UI12_BODY)+16;if(width>right-x-4)width=right-x-4;if(width<12)break;ui73_fit(x+4,field.y+8,width-8,label,UI12_BODY,ink());file_control11(token,(desktop_rect){x,field.y,width,36},F11_CRUMB+ends[i]);x+=width;}
 if(edit)button(token,right,field.y,edit,"Edit",F11_ADDRESS,0);
}
