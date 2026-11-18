/* Shared native frame. No retained pixels, animation timer or per-window cache. */
static unsigned window_active12(desktop_window*w){return model.focused==(unsigned)(w-model.windows)&&!desktop_focus11&&!launcher&&!switch_open11;}
static desktop_rect window_control_rect12(desktop_window*w,unsigned part){ui12_caption_rect r=ui12_caption_bounds(w->bounds.width,part);return(desktop_rect){w->bounds.x+r.x,w->bounds.y+r.y,r.width,r.height};}
static void window_frame12(desktop_window*w){
 desktop_rect r=w->bounds;ui12_palette p=desktop_palette16();unsigned active=window_active12(w),border=active?2:1;
#ifdef ENGINE_M13
 border=(access_flags16&1)?2:1;
#endif
 desktop_shadow16(r.x,r.y,r.width,r.height);
 #ifdef ENGINE_M13
 ui73_round(r.x,r.y,r.width,r.height,10,(access_flags16&1)?p.ink:active?blend15(p.line,p.accent,96):p.line);
#else
 ui73_round(r.x,r.y,r.width,r.height,10,active?p.ink:p.control_border);
#endif
 ui73_round(r.x+(int)border,r.y+(int)border,r.width-2*border,r.height-2*border,10-border,paper());
 uint32_t fill=ui12_caption_fill(p,active);
 ui73_round(r.x+(int)border,r.y+(int)border,r.width-2*border,UI12_CAPTION_HEIGHT-border,10-border,fill);
 rectangle((desktop_rect){r.x+(int)border,r.y+22,r.width-2*(int)border,18},fill);
 #ifdef ENGINE_M13
 rectangle((desktop_rect){r.x+1,r.y+39,r.width-2,1},active?blend15(p.line,p.accent,48):p.line);
#else
 if(active)rectangle((desktop_rect){r.x+12,r.y+38,r.width-24,2},preferences.accent);
#endif
}
static void window_caption12(desktop_window*w){
 desktop_rect r=w->bounds;uint64_t token=desktop_token(&model,w-model.windows);application*a=&apps[w-model.windows];ui12_palette p=desktop_palette16();unsigned active=window_active12(w),enabled=!file_block_owner11(token);
 char title[320];copy(title,titles[w->app],sizeof(title));
 if((w->app==FILES||w->app==EDITOR)&&a->path[0]){const char*name=a->path;for(unsigned i=0;a->path[i];++i)if(a->path[i]=='/'&&a->path[i+1])name=a->path+i+1;copy(title,a->dirty?"* ":"",sizeof(title));append(title,equal(a->path,"/")?"System drive":name,sizeof(title));append(title," - ",sizeof(title));append(title,titles[w->app],sizeof(title));}
 if(w->app==FILES&&a->usb_mode10)files_title12(a,title,sizeof(title));
 ui73_fit(r.x+44,r.y+11,r.width>188?r.width-188:0,title,UI12_BODY,active?p.ink:p.muted);
 window_state11*s=window_state_for11(token);
 for(unsigned part=1;part<=4;++part){
  desktop_rect button_rect=window_control_rect12(w,part);unsigned action=W12_MIN+part-1,state=enabled?component_state12(token,action):UI12_DISABLED;
  ui12_style style=ui12_caption_style(p,active,part,state);
  if(state&(UI12_HOVER|UI12_PRESSED|UI12_FOCUS))ui73_round(button_rect.x,button_rect.y,button_rect.width,button_rect.height,4,style.fill);
  if(state&UI12_FOCUS){rectangle((desktop_rect){button_rect.x,button_rect.y,button_rect.width,2},style.border);rectangle((desktop_rect){button_rect.x,button_rect.y+button_rect.height-2,button_rect.width,2},style.border);rectangle((desktop_rect){button_rect.x,button_rect.y,2,button_rect.height},style.border);rectangle((desktop_rect){button_rect.x+button_rect.width-2,button_rect.y,2,button_rect.height},style.border);}
  if(part==UI12_CAPTION_MENU)ui12_icon(w->app,button_rect.x+6,button_rect.y+6,20,preferences.dark);
  else{unsigned icon=part==UI12_CAPTION_MIN?ICON12_MINIMIZE:part==UI12_CAPTION_MAX?(s&&s->mode?ICON12_RESTORE:ICON12_MAXIMIZE):ICON12_CLOSE;ui12_icon_ink(icon,button_rect.x+12,button_rect.y+8,20,style.ink);}
  if(enabled&&control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){button_rect,token,action};
 }
}
static unsigned window_action12(uint64_t token,unsigned command){
 if(command<W12_MIN||command>W12_MENU)return 0;
 desktop_window*w=desktop_lookup(&model,token);if(!w||file_block_owner11(token))return 1;
 if(command==W12_CLOSE){close_window(token,0);task_damage();}
 else if(command==W12_MIN){desktop_minimize(&model,token,1);task_damage();}
 else if(command==W12_TOGGLE){window_state11*s=window_state_for11(token);if(s)window_mode11(token,s->mode?0:1);}
 else window_menu11((i11_target){token,31000,I11_CAPTION},w->bounds.x+4,w->bounds.y+40);
 return 1;
}
static i11_target window_hint_target12(i11_target hover){
 if(launcher||context11||switch_open11||guide_open11||dragging)return(i11_target){0,0,I11_BACKGROUND};
 i11_target target=hover;
 if(target.kind!=I11_BUTTON||target.action<W12_MIN||target.action>W12_MENU){
  if(!control_active||focused_action<W12_MIN||focused_action>W12_MENU)return(i11_target){0,0,I11_BACKGROUND};
  target=(i11_target){focused_control_window,focused_action,I11_BUTTON};
  desktop_window*w=desktop_lookup(&model,target.window);if(!w||model.focused!=(unsigned)(w-model.windows))return(i11_target){0,0,I11_BACKGROUND};
 }
 desktop_window*w=desktop_lookup(&model,target.window);if(!w||w->minimized||file_block_owner11(target.window))return(i11_target){0,0,I11_BACKGROUND};
 return target;
}
static const char*window_hint_label12(i11_target target){
 if(target.action==W12_MIN)return "Minimize";
 if(target.action==W12_CLOSE)return "Close (Alt+F4)";
 if(target.action==W12_MENU)return "Window menu (Alt+Space)";
 window_state11*s=window_state_for11(target.window);return s&&s->mode?"Restore":"Maximize";
}
static desktop_rect window_hint_rect12(i11_target target){
 desktop_window*w=desktop_lookup(&model,target.window);if(!w)return(desktop_rect){0,0,0,0};
 desktop_rect control_rect=window_control_rect12(w,target.action-W12_MIN+1);unsigned width=ui73_measure(window_hint_label12(target),UI12_SECONDARY)+16;
 if(width>model.width-16)width=model.width-16;
 int x=control_rect.x+control_rect.width-(int)width,y=w->bounds.y+44;
 if(x<8)x=8;if(x+(int)width>(int)model.width-8)x=(int)model.width-(int)width-8;
 if(y+28>(int)model.height-68)y=w->bounds.y-32;
 if(y<8)y=8;if(y+28>(int)model.height-68)y=(int)model.height-96;
 return(desktop_rect){x,y,(int)width,28};
}
static void window_hint_damage12(i11_target before,i11_target after){
 i11_target old=window_hint_target12(before),next=window_hint_target12(after);
 if(old.window)invalidate(window_hint_rect12(old));if(next.window)invalidate(window_hint_rect12(next));
}
static void window_hint_draw12(void){
 i11_target target=window_hint_target12(hover12);if(!target.window)return;
 desktop_rect r=window_hint_rect12(target);ui12_palette p=desktop_palette16();
 ui73_round(r.x,r.y,r.width,r.height,4,p.control_border);ui73_round(r.x+1,r.y+1,r.width-2,r.height-2,3,p.surface);
 ui73_fit(r.x+8,r.y+6,r.width-16,window_hint_label12(target),UI12_SECONDARY,p.ink);
}
