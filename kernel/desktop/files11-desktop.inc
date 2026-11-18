#ifdef ENGINE_M12
/* Display-only reference preference. Hiding never deletes a service or user item. */
typedef struct {uint64_t magic;uint32_t version,hidden;} desktop_record12;
_Static_assert(sizeof(desktop_record12)==16,"Desktop preference must stay bounded");
static void desktop_path12(char*path){copy(path,"/System/Settings/desktop12-",256);append(path,owner.user,256);append(path,".bin",256);}
static void desktop_load12(void){char path[256];desktop_path12(path);desktop_record12 record;unsigned bytes=0;desktop_hidden12=0;
 if(v6_verify(m6_volume(),path)||v6_read(m6_volume(),path,0,&record,sizeof(record),&bytes)||bytes!=sizeof(record)||record.magic!=UINT64_C(0x31504f544b534544)||record.version!=1||(record.hidden&~15u))return;
 desktop_hidden12=record.hidden;
}
static unsigned desktop_first12(unsigned total,unsigned last){
 if(last&&total>4)return total-1;
 for(unsigned i=0;i<4;++i){unsigned row=last?3-i:i;if(DESKTOP_VISIBLE11&(1u<<row))return row;}
 return total>4?4:total;
}
static void desktop_references12(unsigned hidden){if(hidden&~15u)return;char path[256];desktop_path12(path);desktop_record12 record={UINT64_C(0x31504f544b534544),1,hidden};
 if(v6_put(m6_volume(),path,sizeof(record),memory_source,&record)){file_notice11(0,"Could not save your desktop icons. The previous layout is kept for this session.");return;}
 desktop_hidden12=hidden;desktop_selection11&=DESKTOP_VISIBLE11;interaction11.last_valid=0;
 if(desktop_item_focus11<4&&!(DESKTOP_VISIBLE11&(1u<<desktop_item_focus11)))desktop_item_focus11=desktop_first12(desktop_children11()+4,0);
 whole();
}
#endif
static void desktop_open_builtin11(unsigned row){
 if(row>=DESKTOP_BUILTINS11||!(DESKTOP_VISIBLE11&(1u<<row)))return;
 desktop_focus11=0;
#ifdef ENGINE_M12
 if(row==3){file_action11(0,F11_BIN);whole();return;}
#endif
 if(row==2)launch(SETTINGS,0);
 else{char path[256];if(row==1)root_path(path,"Documents");else home72(path);launch(FILES,path);}
 whole();
}
#ifndef ENGINE_M12
static unsigned desktop_rows11(void){unsigned rows=model.height>190?(model.height-190)/95:1;return rows?rows:1;}
#endif
static unsigned desktop_capacity11(void){
#ifdef ENGINE_M12
 return ui12_desktop_capacity(model.width,model.height);
#else
 unsigned columns=model.width>210?(model.width-190)/126:1;if(!columns)columns=1;unsigned count=columns*desktop_rows11();return count>128?128:count;
#endif
}
#ifdef ENGINE_M12
static void desktop_label12(desktop_rect r,const char*label,uint32_t foreground,uint32_t backing){
#ifndef ENGINE_M13
 (void)backing;
#endif
 char first[64];unsigned used=0,last_space=0;
 while(label[used]&&used<63){first[used]=label[used];first[used+1]=0;if(ui73_measure(first,UI12_BODY)>(unsigned)r.width-12){first[used]=0;break;}if(label[used]==' ')last_space=used;++used;}
 first[used]=0;if(label[used]&&last_space){used=last_space;first[used]=0;}
 while(label[used]==' ')++used;
 unsigned width=ui73_measure(first,UI12_BODY);
#ifdef ENGINE_M13
 ui73_round(r.x+(r.width-(int)width)/2-3,r.y+58,width+6,22,4,backing);
#endif
 ui73_fit(r.x+(r.width-(int)width)/2,r.y+60,r.width-12,first,UI12_BODY,foreground);
 if(label[used]){width=ui73_measure(label+used,UI12_BODY);int x=width<=(unsigned)r.width-12?r.x+(r.width-(int)width)/2:r.x+6;
#ifdef ENGINE_M13
 unsigned shown=width<(unsigned)r.width-12?width:(unsigned)r.width-12;ui73_round(x-3,r.y+82,shown+6,22,4,backing);
#endif
 ui73_fit(x,r.y+84,r.width-12,label+used,UI12_BODY,foreground);}
}
static void desktop_tile12(desktop_rect r,unsigned action,unsigned selected,unsigned focused,unsigned icon,const v6_entry*entry12,const char*label){
 access_capture16(0,action,label,3);
 unsigned hovered=hover12.kind==I11_ITEM&&!hover12.window&&hover12.action==action;
 uint32_t foreground=desktop_ink11();
 if(selected||hovered){ui73_round(r.x,r.y,r.width,r.height,UI12_RADIUS,selected?0x315b62:0x29454e);foreground=0xe5f0f3;}
 if(focused&&desktop_focus11){uint32_t stroke=foreground;rectangle((desktop_rect){r.x+2,r.y+2,r.width-4,1},stroke);rectangle((desktop_rect){r.x+2,r.y+r.height-3,r.width-4,1},stroke);rectangle((desktop_rect){r.x+2,r.y+2,1,r.height-4},stroke);rectangle((desktop_rect){r.x+r.width-3,r.y+2,1,r.height-4},stroke);}
 unsigned icon_dark=selected||hovered||foreground==0xffffff;
 if(entry12){ui12_icon(shell_entry_icon12(entry12),r.x+36,r.y+6,48,icon_dark);if(shell_suffix12(file_label11(entry12),"link"))ui12_icon(ICON12_SHORTCUT,r.x+36,r.y+30,24,icon_dark);}
 else ui12_icon(icon,r.x+36,r.y+6,48,icon_dark);
 desktop_label12(r,label,foreground,selected?0x315b62:hovered?0x29454e:(access_flags16&1)?0:appearance11.wallpaper);
 if(control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){r,0,action};
}
static void draw_desktop_builtin12(void){
 static const char*names[]={"My files","Documents","Appearance","Recycle Bin"};
 static const unsigned icons[]={ICON12_HOME,ICON12_FOLDER,ICON12_SETTINGS,ICON12_TRASH};
 for(unsigned i=0;i<UI12_DESKTOP_BUILTINS;++i){if(!(DESKTOP_VISIBLE11&(1u<<i)))continue;ui12_desktop_cell cell=ui12_desktop_position(model.height,i,1);desktop_rect r={cell.x,cell.y,cell.width,cell.height};desktop_tile12(r,30000+i,!!(desktop_selection11&(1u<<i)),desktop_item_focus11==i,icons[i],0,names[i]);}
}
#endif
static void desktop_set_selected11(unsigned row,unsigned value){if(row<DESKTOP_BUILTINS11){if(value&&!(DESKTOP_VISIBLE11&(1u<<row)))return;if(value)desktop_selection11|=1u<<row;else desktop_selection11&=~(1u<<row);return;}const v6_entry*e=desktop_child11(row-DESKTOP_BUILTINS11);if(!e)return;unsigned index=(unsigned)(e-m6_volume()->entries);if(value)desktop_files_selected11[index/8]|=(uint8_t)(1u<<(index%8));else desktop_files_selected11[index/8]&=(uint8_t)~(1u<<(index%8));}
static unsigned desktop_is_selected11(unsigned row){return row<DESKTOP_BUILTINS11?!!(desktop_selection11&(1u<<row)):file_selected_desktop11(row-DESKTOP_BUILTINS11);}
static void desktop_select11(unsigned row,unsigned modifiers,unsigned preserve){unsigned total=desktop_children11()+DESKTOP_BUILTINS11;if(row>=total||(row<DESKTOP_BUILTINS11&&!(DESKTOP_VISIBLE11&(1u<<row))))return;if(preserve&&desktop_is_selected11(row)){desktop_item_focus11=row;return;}if(!(modifiers&3)){desktop_selection11=0;memset(desktop_files_selected11,0,sizeof(desktop_files_selected11));}
 if(modifiers&2){unsigned anchor=desktop_anchor11<total?desktop_anchor11:row;if(!(modifiers&1)){desktop_selection11=0;memset(desktop_files_selected11,0,sizeof(desktop_files_selected11));}unsigned lo=anchor<row?anchor:row,hi=anchor>row?anchor:row;for(unsigned n=lo;n<=hi;++n)desktop_set_selected11(n,1);}
 else{desktop_set_selected11(row,(modifiers&1)?!desktop_is_selected11(row):1);desktop_anchor11=row;}desktop_item_focus11=row;if(row>=DESKTOP_BUILTINS11)desktop_page11=(row-DESKTOP_BUILTINS11)/desktop_capacity11();
}
static void draw_desktop_files11(void){unsigned count=desktop_children11(),page=desktop_capacity11();
#ifndef ENGINE_M12
 unsigned rows=desktop_rows11();
#endif
if(desktop_page11*page>=count)desktop_page11=count?(count-1)/page:0;unsigned start=desktop_page11*page;
 for(unsigned n=0;n<page&&start+n<count;++n){unsigned row=start+n;const v6_entry*e=desktop_child11(row);
#ifdef ENGINE_M12
 ui12_desktop_cell cell=ui12_desktop_position(model.height,n,0);desktop_rect r={cell.x,cell.y,cell.width,cell.height};desktop_tile12(r,F11_DESKTOP_ITEM+row,file_selected_desktop11(row),desktop_item_focus11==row+DESKTOP_BUILTINS11,0,e,file_label11(e));
#else
 int x=176+(int)(n/rows)*126,y=110+(int)(n%rows)*95;desktop_rect r={x,y,120,88};if(file_selected_desktop11(row))ui73_round(x,y,120,88,6,0x315b62);
 if(e->kind==2)folder_icon72(x+38,y+9,42,0xf0ce87);else{ui73_round(x+43,y+6,32,39,4,0xe8f2f4);rectangle((desktop_rect){x+49,y+17,20,2},0x78959c);rectangle((desktop_rect){x+49,y+24,16,2},0x78959c);if(file_suffix11(e->path,"link")){rectangle((desktop_rect){x+35,y+33,15,12},paper());rectangle((desktop_rect){x+38,y+38,9,2},ink());rectangle((desktop_rect){x+45,y+35,2,8},ink());}}
  ui73_paragraph(x+6,y+54,108,2,file_label11(e),file_selected_desktop11(row)?0xe5f0f3:desktop_ink11());if(control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){r,0,F11_DESKTOP_ITEM+row};
#endif
 }
 #ifdef ENGINE_M12
 unsigned caption=V6_ENTRIES;
 if(hover12.kind==I11_ITEM&&!hover12.window&&hover12.action>=F11_DESKTOP_ITEM&&hover12.action<F11_DESKTOP_ITEM+count)caption=hover12.action-F11_DESKTOP_ITEM;
 else if(desktop_focus11&&desktop_item_focus11>=DESKTOP_BUILTINS11&&desktop_item_focus11-DESKTOP_BUILTINS11<count&&file_selected_desktop11(desktop_item_focus11-DESKTOP_BUILTINS11))caption=desktop_item_focus11-DESKTOP_BUILTINS11;
 if(caption<count){const v6_entry*e=desktop_child11(caption);
#ifdef ENGINE_M13
 ui73_round(30,model.height-144,model.width-60,28,4,(access_flags16&1)?0:appearance11.wallpaper);ui73_fit(38,model.height-140,model.width-76,file_label11(e),UI12_SECONDARY,desktop_ink11());
#else
 ui73_fit(38,86,model.width-76,file_label11(e),UI12_SECONDARY,desktop_ink11());
#endif
 }
 if(count>page){int y=(int)model.height-105;unsigned actions[]={F11_DESKTOP_PREV,F11_DESKTOP_NEXT};const char*names[]={"Previous","Next"};for(unsigned i=0;i<2;++i){desktop_rect r={30+(int)i*124,y,112,36};unsigned enabled=i?start+page<count:desktop_page11!=0;component_button12(0,r,names[i],actions[i],0,enabled);if(enabled&&control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){r,0,actions[i]};}char info[64],number[24];copy(info,"Desktop page ",64);decimal(number,desktop_page11+1);append(info,number,64);append(info," of ",64);decimal(number,(count+page-1)/page);append(info,number,64);text(290,y+8,info,1,desktop_ink11());}
#else
if(count>page){int y=(int)model.height-105;button(0,176,y,65,"<",F11_DESKTOP_PREV,0);button(0,249,y,65,">",F11_DESKTOP_NEXT,0);char info[64],number[24];decimal(number,desktop_page11+1);copy(info,"Desktop page ",64);append(info,number,64);text(326,y+9,info,1,desktop_ink11());}
#endif
}
static unsigned files_begin_drag11(i11_target target,unsigned modifiers){if(file_job_state11.active||file_job_state11.waiting||file_dialog_state11.mode)return 0;desktop_window*w=file_owner_window11(target.window);
 if(w){application*a=&apps[w-model.windows];if(target.action>=FILE_ROW&&target.action<FILE_ROW+V6_ENTRIES){unsigned row=target.action-FILE_ROW;if(!selected_row11(a,row))select_row11(a,row,0,0);}else if(a->usb_mode10==2&&target.action>=USB_ROW10&&target.action<USB_ROW10+6){unsigned row=a->offset+target.action-USB_ROW10;if(!selected_row11(a,row))select_row11(a,row,0,0);a->usb_selected10=row+1;}else return 0;}
 else if(!target.window&&target.action>=F11_DESKTOP_ITEM&&target.action<F11_DESKTOP_ITEM+V6_ENTRIES){unsigned row=target.action-F11_DESKTOP_ITEM;if(!file_selected_desktop11(row))desktop_select11(row+DESKTOP_BUILTINS11,0,0);}else return 0;
 unsigned count=0,status=file_collect11(target.window,file_drag_roots11,&count);if(status){file_notice11(target.window,"Select up to 128 native items, or one supported USB file.");return 0;}
 file_drag11=1;file_drag_count11=count;file_drag_copy11=(modifiers&1)||file_drag_roots11[0].provider==F11_USB;file_drag_x11=pointer_x;file_drag_y11=pointer_y;context11=0;whole();return 1;
}
static void files_drag_motion11(unsigned x,unsigned y,unsigned modifiers){if(!file_drag11)return;invalidate((desktop_rect){(int)file_drag_x11+14,(int)file_drag_y11+18,286,58});file_drag_x11=x;file_drag_y11=y;file_drag_copy11=(modifiers&1)||file_drag_roots11[0].provider==F11_USB;invalidate((desktop_rect){(int)x+14,(int)y+18,286,58});}
static void files_cancel_drag11(void){if(file_drag11){file_drag11=0;whole();}i11_cancel(&interaction11);}
static void files_drop11(i11_target target,unsigned modifiers){if(!file_drag11)return;file_drag11=0;whole();
#ifdef ENGINE_M12
 if(files_busy12()){file_notice11(target.window,"Wait for the transfer or choose Cancel before dropping more files.");return;}
#endif
char destination[256];unsigned status=0;desktop_window*w=file_owner_window11(target.window);application*a=w?&apps[w-model.windows]:0;
 if(a&&a->usb_mode10==2){if(file_drag_count11!=1||file_drag_roots11[0].provider!=F11_NATIVE||file_drag_roots11[0].kind!=1||!file_user_item11(file_drag_roots11[0].source)){file_notice11(target.window,"USB accepts one native file at a time; folder copies are unavailable.");return;}copy(destination,a->usb_path10,256);if(target.action>=USB_ROW10&&target.action<USB_ROW10+6){unsigned total,row=target.action-USB_ROW10;if(usb_listing10(a,a->offset,6,&total)||a->offset+row>=total||usb_rows10[row].kind!=2){file_notice11(target.window,"Drop onto a folder or the folder background.");return;}char path[256];status=file_join11(path,destination,usb_rows10[row].name);copy(destination,path,256);}if(!status)status=rem10_export(a->usb_disk10,a->usb_context10,a->usb_part10,destination,file_drag_roots11[0].source);file_notice11(target.window,status?"USB copy failed or the name already exists. Existing files were kept.":"Copied and flushed to USB. Use Safe remove before unplugging.");return;}
 if(a&&!a->usb_mode10){copy(destination,a->path,256);if(target.kind==I11_ITEM){const v6_entry*e=file_target_entry11(target);if(!e||e->kind!=2){file_notice11(target.window,"Drop onto a folder or the folder background.");return;}copy(destination,e->path,256);}else if(target.kind!=I11_BACKGROUND){file_notice11(target.window,"Drop onto a folder or empty space inside the folder.");return;}}
 else if(!target.window){if(target.action==30000)home72(destination);else if(target.action==30001)root_path(destination,"Documents");else if(target.action>=F11_DESKTOP_ITEM&&target.action<F11_DESKTOP_ITEM+V6_ENTRIES){const v6_entry*e=file_target_entry11(target);if(!e||e->kind!=2){file_notice11(0,"Drop onto a folder or empty desktop space.");return;}copy(destination,e->path,256);}else if(target.kind==I11_BACKGROUND)root_path(destination,"Desktop");else{file_notice11(0,"Drop onto a folder or empty desktop space.");return;}}
 else{file_notice11(0,"Drop onto a Files folder or the desktop.");return;}
 if(!writable72(destination)||file_in_bin11(destination)){file_notice11(target.window,"This location is protected. Choose one of your own folders.");return;}
 status=file_job_start11((modifiers&1)||file_drag_roots11[0].provider==F11_USB?F11_JOB_COPY:F11_JOB_MOVE,target.window,file_drag_roots11,file_drag_count11,destination);if(status)file_notice11(target.window,file_error_text11(status));
}
