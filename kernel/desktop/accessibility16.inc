/* Base-owned accessibility. No app slot, worker, heap cache or idle polling. */
static void access_path16(char*path){copy(path,"/System/Settings/accessibility16-",256);append(path,owner.user,256);append(path,".bin",256);}
static void access_load16(void){char path[256];unsigned record[4],bytes=0;access_path16(path);access_flags16=access_invalid16=0;const v6_entry*saved=entry(path);if(!saved)return;access_invalid16=1;if(saved->kind!=1||saved->size!=sizeof(record))return;
 if(v6_verify(m6_volume(),path)||v6_read(m6_volume(),path,0,record,sizeof(record),&bytes)||bytes!=sizeof(record)||record[0]!=0x36314155||record[1]!=1||record[2]>3||record[3])return;access_flags16=record[2];access_invalid16=0;
}
static unsigned access_registered16(uint64_t owner_id,unsigned command){if(owner_id&&!desktop_lookup(&model,owner_id))return 0;for(unsigned i=0;i<control_count;++i)if(controls[i].window==owner_id&&controls[i].action==command)return 1;return 0;}
static void access_help_close16(void){unsigned region=access_help16>>8;access_help16=0;control_active=0;access_region16=0;
 if(picker_live12()&&file_dialog_owner_focused11()&&file_dialog_state11.owner==access_help_item16.owner){whole();return;}
 if(access_help_item16.role&&access_registered16(access_help_item16.owner,access_help_item16.action)){focused_control_window=access_help_item16.owner;focused_action=access_help_item16.action;control_active=1;access_region16=region;}whole();
}
static unsigned access_action16(uint64_t token,unsigned command){
 if(command==ACCESS_HELP_BODY16)return 1;if(command==ACCESS_HELP_CLOSE16){access_help_close16();return 1;}
 if(command<ACCESS_CONTRAST16||command>ACCESS_DEFAULTS16)return 0;desktop_window*w=desktop_lookup(&model,token);if(!w||w->app!=SETTINGS)return 1;application*a=&apps[w-model.windows];
 if(settings_busy13()){notice(a,"Finish or cancel the file operation before saving accessibility. Your choices are kept.");whole();return 1;}
 unsigned next=command==ACCESS_DEFAULTS16?0:access_flags16^(command==ACCESS_CONTRAST16?1u:2u);unsigned record[4]={0x36314155,1,next,0};char path[256];access_path16(path);
 unsigned status=v6_put(m6_volume(),path,sizeof(record),memory_source,record);if(!status){access_flags16=next;access_invalid16=0;notice(a,"Accessibility saved. Appearance and optional apps are unchanged.");}else notice(a,"Accessibility could not be saved. The previous choices are kept.");whole();return 1;
}
static unsigned access_eligible16(const control*c,unsigned region){
 if(c->action==70)return 0;if(!region){if(model.focused>=DESKTOP_WINDOWS||model.windows[model.focused].minimized)return 0;return c->window==desktop_token(&model,model.focused);}
 if(c->window)return 0;if(region==1)return c->rect.y>=(int)model.height-60;
 if(region==2)return(c->action>=30000&&c->action<30000+DESKTOP_BUILTINS11)||(c->action>=F11_DESKTOP_ITEM&&c->action<F11_DESKTOP_ITEM+V6_ENTRIES);
 return feedback_visible14()&&c->action==60002;
}
static unsigned access_choose16(unsigned region,int direction,unsigned next){
 unsigned count=0,current=0;for(unsigned i=0;i<control_count;++i)if(access_eligible16(&controls[i],region)){if(control_active&&controls[i].window==focused_control_window&&controls[i].action==focused_action)current=count+1;++count;}if(!count)return 0;
 unsigned selected=next?(direction<0?(current?current+count-2:count-1):(current?current:0))%count:0;for(unsigned i=0,at=0;i<control_count;++i)if(access_eligible16(&controls[i],region)&&at++==selected){control*c=&controls[i];focused_control_window=c->window;focused_action=c->action;control_active=1;access_region16=region;desktop_focus11=region==2;
  if(region==2){unsigned row=c->action>=F11_DESKTOP_ITEM?c->action-F11_DESKTOP_ITEM+DESKTOP_BUILTINS11:c->action-30000;desktop_select11(row,0,1);control_active=1;}whole();return 1;}
 return 0;
}
static void access_describe16(void){
 access_help_item16=(access_semantic16){0};copy(access_help_item16.label,"Keyboard navigation",sizeof(access_help_item16.label));
 if(picker_live12()&&file_dialog_owner_focused11()){
  file_dialog11*d=&file_dialog_state11;unsigned at=d->focus;const char*name="File dialog";unsigned command=0,role=1;
  if(picker12.phase){name=at==2?"Folder name":at==7?"Cancel":at==5?"Back":at==6?"Discard and open":picker12.phase==P12_REPLACE_REVIEW?"Replace file":picker12.phase==P12_DIRTY_REVIEW?"Save and open":"Create folder";command=at==2?P12_NAME:at==7?P12_CANCEL:at==5?P12_REVIEW_BACK:at==6?P12_DISCARD_OPEN:picker12.phase==P12_REPLACE_REVIEW?P12_REPLACE:picker12.phase==P12_DIRTY_REVIEW?P12_SAVE_OPEN:P12_ACCEPT;role=at==2?2:1;}
  else{static const unsigned commands[]={P12_ADDRESS,0,P12_NAME,P12_FILTER,P12_ACCEPT,P12_CANCEL,P12_BACK,P12_FORWARD,P12_UP,P12_HOME,P12_DOCUMENTS,P12_DOWNLOADS,P12_PICTURES,P12_NEW_FOLDER,P12_PREVIOUS,P12_NEXT};static const char*names[]={"Folder address","File list","File name","File type","Open","Cancel","Back","Forward","Up","Home","Documents","Downloads","Pictures","New folder","Previous page","Next page"};
   if(at<16){name=names[at];command=commands[at];role=at==0||at==2?2:at==1?3:1;if(at==4)name=picker12.purpose==P12_TEXT_SAVE?"Save":picker12.purpose==P12_ZIP_FOLDER?"Choose folder":"Open";if(at==1){const v6_entry*selected=picker_selected12();if(selected){name=file_basename11(selected->path);command=P12_ROW+picker12.selected;}}}}
  access_help_item16.owner=d->owner;access_help_item16.action=command;access_help_item16.role=role;copy(access_help_item16.label,name,sizeof(access_help_item16.label));
 }
 else if(control_active&&access_registered16(focused_control_window,focused_action)){
  if(access_focus16.owner==focused_control_window&&access_focus16.action==focused_action&&access_focus16.label[0])access_help_item16=access_focus16;
  else{access_help_item16.owner=focused_control_window;access_help_item16.action=focused_action;access_help_item16.role=1;const char*name=focused_action==49000?"Minimize window":focused_action==49001?"Maximize or restore window":focused_action==49002?"Close window":focused_action==49003?"Window menu":focused_action==60002?"Dismiss notification":focused_action==40026?"Folder address":focused_action==54018?"Folder address":focused_action==54019?"File name":focused_action==S11_SEARCH?"Search apps and folders":"Selected control";copy(access_help_item16.label,name,sizeof(access_help_item16.label));}
 }
 access_help16=1|(access_region16<<8);control_active=1;focused_control_window=0;focused_action=ACCESS_HELP_CLOSE16;whole();
}
static unsigned access_blocked16(void){return launcher||context11||switch_open11||guide_open11||tray_open12||file_dialog_state11.mode||dragging||file_drag11||interaction11.captured;}
static unsigned access_key16(int key){
 if(access_help16){if(key==27||key==10||key==32||key==153)access_help_close16();else if(key==9||key==136){control_active=1;focused_control_window=0;focused_action=ACCESS_HELP_CLOSE16;whole();}return 1;}
 if(key==153){access_describe16();return 1;}
 if(key==152){if(access_blocked16())return 1;int direction=(input11_modifiers()&2)?-1:1;for(unsigned n=1;n<=4;++n){unsigned region=(access_region16+(direction<0?4-n:n))%4;if(access_choose16(region,direction,0))break;}return 1;}
 if(access_blocked16())return 0;
 if(access_region16&&control_active&&!focused_control_window&&access_registered16(0,focused_action)){
  if(key==9||key==136){access_choose16(access_region16,key==136?-1:1,1);return 1;}
  if(key==10||key==32){unsigned command=focused_action,region=access_region16;control_active=0;access_region16=0;if(region==2)open_target11((i11_target){0,command,I11_ITEM});else action(0,command);whole();return 1;}
 }
 return 0;
}
static desktop_rect access_bounds16(void){int w=model.width>680?640:(int)model.width-40,h=252;return(desktop_rect){((int)model.width-w)/2,((int)model.height-60-h)/2,w,h};}
static i11_target access_target16(int x,int y){desktop_rect r=access_bounds16();unsigned close=x>=r.x+r.width-132&&x<r.x+r.width-28&&y>=r.y+r.height-52&&y<r.y+r.height-16;return(i11_target){0,close?ACCESS_HELP_CLOSE16:ACCESS_HELP_BODY16,I11_BUTTON};}
static void access_draw16(void){if(!access_help16)return;desktop_rect r=access_bounds16();ui12_palette p=desktop_palette16();desktop_shadow16(r.x,r.y,r.width,r.height);ui73_round(r.x,r.y,r.width,r.height,10,p.ink);ui73_round(r.x+2,r.y+2,r.width-4,r.height-4,8,p.paper);
 ui73_fit(r.x+24,r.y+20,r.width-48,"Focus help",UI12_HEADING,p.ink);const char*role=access_help_item16.role==4?"Checkbox":access_help_item16.role==2?"Text field":access_help_item16.role==3?"Item":access_help_item16.role?"Button":"Keyboard";ui73_fit(r.x+24,r.y+60,r.width-48,role,UI12_SECONDARY,p.muted);ui73_paragraph(r.x+24,r.y+86,r.width-48,2,access_help_item16.label,p.ink);
 ui73_paragraph(r.x+24,r.y+138,r.width-48,2,"Tab and Shift+Tab move focus. Enter activates. F6 changes panes. Escape closes this help and keeps your work.",p.muted);button(0,r.x+r.width-132,r.y+r.height-52,104,"Close",ACCESS_HELP_CLOSE16,1);
}
