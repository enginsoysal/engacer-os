/* Shared Settings categories and explicit, bounded visual preview ownership. */
static unsigned settings_dirty13(void){return settings_preview13.owner&&(preferences.accent!=settings_preview13.accent||preferences.dark!=settings_preview13.dark||ui73_scale_choice()!=settings_preview13.scale||appearance11.wallpaper!=settings_preview13.wallpaper||appearance11.pattern!=settings_preview13.pattern);}
static unsigned settings_other13(uint64_t token){return settings_preview13.owner&&settings_preview13.owner!=token;}
static unsigned settings_busy13(void){return files_busy12()||file_dialog_state11.mode||w8_pending();}
static void settings_open13(uint64_t token){desktop_window*w=desktop_lookup(&model,token);if(!w)return;settings_page13[w-model.windows]=0;if(settings_invalid13)notice(&apps[w-model.windows],"Saved appearance could not be read. Safe defaults are active. Apply saves your new choices.");}
static unsigned settings_begin13(uint64_t token){desktop_window*w=desktop_lookup(&model,token);if(!w||w->app!=SETTINGS)return 0;if(settings_other13(token)){notice(&apps[w-model.windows],"Apply or cancel the preview in the other Settings window first.");whole();return 0;}if(!settings_preview13.owner)settings_preview13=(settings_preview_record13){token,preferences.accent,preferences.dark,ui73_scale_choice(),appearance11.wallpaper,appearance11.pattern};return 1;}
static unsigned settings_scale13(application*a,unsigned choice){if(picker_live12()){notice(a,"Finish or cancel the file dialog before changing display size.");return 0;}const os_boot_info_v0*changed=ui73_set_scale(choice);if(!changed){notice(a,"That size leaves too little room. Choose a smaller size.");return 0;}display=changed;model.width=changed->framebuffer_width;model.height=changed->framebuffer_height;for(unsigned i=0;i<DESKTOP_WINDOWS;++i)if(model.windows[i].live)desktop_place(&model,desktop_token(&model,i),model.windows[i].bounds);window_reflow11();usb_mouse_state(&pointer_x,&pointer_y,&previous_buttons);whole();return 1;}
static unsigned settings_cancel13(uint64_t token){desktop_window*w=desktop_lookup(&model,token);if(!w||settings_preview13.owner!=token)return 1;application*a=&apps[w-model.windows];if(ui73_scale_choice()!=settings_preview13.scale&&!settings_scale13(a,settings_preview13.scale)){whole();return 0;}preferences.accent=settings_preview13.accent;preferences.dark=settings_preview13.dark;appearance11.accent=preferences.accent;appearance11.dark=preferences.dark;appearance11.scale=settings_preview13.scale;appearance11.wallpaper=settings_preview13.wallpaper;appearance11.pattern=settings_preview13.pattern;settings_preview13.owner=0;notice(a,"Preview cancelled. Your previous session appearance is restored; no settings were written.");whole();return 1;}
static unsigned settings_close13(uint64_t token){desktop_window*w=desktop_lookup(&model,token);if(!w)return 1;if(!settings_cancel13(token))return 0;settings_page13[w-model.windows]=0;return 1;}
static void settings_button13(uint64_t token,int x,int y,int width,const char*label,unsigned command,unsigned selected,unsigned enabled){if(enabled)access_capture16(token,command,label,1);ui12_palette p=desktop_palette16();unsigned state=enabled?component_state12(token,command):UI12_DISABLED;ui12_style style=ui12_control_style(p,state|(selected?UI12_SELECTED:0),0);unsigned inset=(state&UI12_FOCUS)?3:1;ui73_round(x,y,width,36,6,style.border);ui73_round(x+inset,y+inset,width-2*inset,36-2*inset,6-inset,style.fill);ui73_fit(x+10,y+8,width-20,label,UI12_BODY,style.ink);if(enabled&&control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){{x,y,width,36},token,command};}
static void settings_draw13(desktop_window*w,application*a,uint64_t token){int x=w->bounds.x+24,y=w->bounds.y+56,width=w->bounds.width-48;unsigned page=settings_page13[w-model.windows],other=settings_other13(token);ui12_palette p=desktop_palette16();const char*titles13[]={"Appearance","Display","Mouse and keyboard","System","Accessibility"
#ifdef ENGINE_M13
 ,"Interface preview"
#endif
 };ui73_fit(x,y,width,titles13[page],UI12_HEADING,p.ink);
 const char*names[]={"Appearance","Display","Input","System","Accessibility"};int tab=(width-32)/5;for(unsigned i=0;i<5;++i)settings_button13(token,x+(tab+8)*(int)i,y+40,tab,names[i],S13_APPEARANCE+i,page==i,1);
 int top=y+96;
 if(page==0){ui73_fit(x,top,width,"Accent color",UI12_BODY,p.ink);const char*colors[]={"Mint","Lavender","Amber","Default"};const unsigned values[]={0x62e5bd,0x9caeff,0xf4c47c,DISTRO_ACCENT};for(unsigned i=0;i<4;++i)settings_button13(token,x+(int)i*112,top+26,104,colors[i],i==3?S13_ACCENT_DEFAULT:STYLE_MINT+i,preferences.accent==values[i],!other);
  ui73_fit(x,top+82,width,"Windows",UI12_BODY,p.ink);settings_button13(token,x,top+108,148,"Light",STYLE_PAPER,!preferences.dark,!other);settings_button13(token,x+160,top+108,148,"Dark",STYLE_DARK,preferences.dark,!other);
  ui73_fit(x,top+164,width,"Wallpaper",UI12_BODY,p.ink);const char*papers[]={"Ocean","Night","Paper"};const unsigned paper_colors[]={0x142c35,0x182039,0xd7e4e9};for(unsigned i=0;i<3;++i)settings_button13(token,x+(int)i*112,top+190,104,papers[i],45000+i,appearance11.wallpaper==paper_colors[i],!other);settings_button13(token,x+336,top+190,width-336,appearance11.pattern==0?"Gradient":appearance11.pattern==1?"Solid":"Horizon",45003,0,!other);
 }else if(page==1){ui73_paragraph(x,top,width,2,"Preview a comfortable size. Apply saves it; Cancel restores your previous choice.",p.ink);const char*sizes[]={"Automatic","100%","150%","200%"};for(unsigned i=0;i<4;++i)settings_button13(token,x+(int)i*112,top+62,104,sizes[i],SCALE_AUTO+i,ui73_scale_choice()==(i?i+1:0),!other);char info[128],value[24];copy(info,"Current desktop: ",128);decimal(value,model.width);append(info,value,128);append(info," x ",128);decimal(value,model.height);append(info,value,128);append(info," logical pixels",128);ui73_fit(x,top+124,width,info,UI12_BODY,p.ink);ui73_paragraph(x,top+162,width,3,"Unsupported sizes are refused. Windows reflow to remain reachable. File dialogs must finish before changing display size.",p.muted);
 }else if(page==2){ui73_fit(x,top,width,"Double-click interval",UI12_BODY,p.ink);unsigned speed=interaction11.double_ms?interaction11.double_ms:500;const char*speeds[]={"Fast - 200 ms","Normal - 500 ms","Slow - 900 ms"};const unsigned ms[]={200,500,900};for(unsigned i=0;i<3;++i)settings_button13(token,x+(int)i*194,top+30,186,speeds[i],S13_CLICK_FAST+i,speed==ms[i],1);ui73_paragraph(x,top+82,width,2,"A click selects an item; double-click opens it. Input choices save when clicked.",p.muted);ui73_fit(x,top+142,width,"Keyboard layout",UI12_BODY,p.ink);settings_button13(token,x,top+172,164,"US QWERTY",LAYOUT_US10,!input10_layout(),1);settings_button13(token,x+176,top+172,164,"US Dvorak",LAYOUT_DVORAK10,input10_layout()==1,1);
 }else if(page==4){ui73_paragraph(x,top,width,2,"Readable controls and keyboard navigation belong to the base desktop.",p.ink);
 settings_button13(token,x,top+58,width,(access_flags16&1)?"[x] High contrast":"[ ] High contrast",ACCESS_CONTRAST16,!!(access_flags16&1),1);
 settings_button13(token,x,top+106,width,(access_flags16&2)?"[x] Reduced motion":"[ ] Reduced motion",ACCESS_MOTION16,!!(access_flags16&2),1);
 ui73_paragraph(x,top+158,width,3,"F6 moves between window, taskbar, desktop and messages. Tab moves focus; Enter opens. F1 describes the focused control.",p.muted);
 settings_button13(token,x,top+234,200,"Reset accessibility",ACCESS_DEFAULTS16,0,1);

#ifdef ENGINE_M13
 }else if(page==5){
  ui73_paragraph(x,top,width,2,"Try the shared controls. This preview never changes files or preferences.",p.muted);
  settings_button13(token,x,top+54,176,"Normal button",60100,0,1);
  settings_button13(token,x+192,top+54,176,"Selected",60101,a->year74&1,1);
  settings_button13(token,x+384,top+54,width-384,"Unavailable",60103,0,0);
  desktop_rect field={x,top+112,width,44};unsigned focused=control_active&&focused_control_window==token&&focused_action==60102;
  component_field12(field,focused);ui73_fit(x+12,top+124,width-24,a->length?a->text:"Click here and type a short message",UI12_BODY,a->length?p.ink:p.muted);
  access_capture16(token,60102,"Preview text field",2);if(control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){field,token,60102};
  ui73_fit(x,top+184,width,"Body text stays readable at your chosen display size.",UI12_BODY,p.ink);
  ui73_fit(x,top+216,width,"Secondary text adds context without competing with the task.",UI12_SECONDARY,p.muted);
  settings_button13(token,x,top+262,224,"Back to System",S13_SYSTEM,0,1);
#endif
 }else{ui73_paragraph(x,top,width,2,"Required system services stay independent of optional applications.",p.ink);settings_button13(token,x,top+64,224,"Devices and hardware",DEVICES10,0,1);settings_button13(token,x+240,top+64,width-240,"Applications",10000,0,1);settings_button13(token,x,top+120,224,"Start and taskbar",45004,0,1);settings_button13(token,x+240,top+120,width-240,"Quick settings",TR12_OPEN,0,1);
#ifdef ENGINE_M13
 settings_button13(token,x,top+176,224,"Interface preview",59007,0,1);
#endif
 ui73_paragraph(x,top+224,width,2,"Removing an optional app does not remove the desktop, tray or your personal files.",p.muted);}
 int footer=w->bounds.y+w->bounds.height-116;if(page<2){settings_button13(token,x,footer,164,"Apply and save",PREFERENCES_SAVE,0,!other);settings_button13(token,x+176,footer,164,"Cancel preview",S13_CANCEL,0,settings_preview13.owner==token);settings_button13(token,x+352,footer,width-352,"Restore defaults",S13_DEFAULTS,0,!other);}
 const char*message=other?"Apply or cancel the preview in the other Settings window first.":a->notice[0]?a->notice:settings_dirty13()?"Appearance preview is not saved. Apply keeps it; Cancel or closing restores it.":page<2?"Preview changes before saving. Restore defaults previews this distribution's appearance.":page==2?"Input choices save immediately. Appearance previews keep their separate Apply / Cancel controls.":page==4?(access_invalid16?"Saved accessibility choices were invalid. Safe defaults are active; choose a setting to save a valid record.":"Choices save independently. High contrast overrides your theme; switching it off restores it. Reduced motion removes shadows and decorative control movement."):"Choose Devices, installed apps or Start preferences to manage your system.";unsigned review=file_dialog_state11.mode&&desktop_lookup(&model,file_dialog_state11.owner)&&file_dialog_state11.owner!=token&&a->notice[0];if(review)button(token,x+width-172,w->bounds.y+w->bounds.height-64,172,"Show current dialog",60003,0);ui73_paragraph(x,w->bounds.y+w->bounds.height-64,width-(review?184:0),2,message,p.ink);
}
static unsigned settings_action13(uint64_t token,unsigned command){desktop_window*w=desktop_lookup(&model,token);if(!w||w->app!=SETTINGS)return command>=S13_APPEARANCE&&command<=S13_CLICK_SLOW;application*a=&apps[w-model.windows];unsigned slot=w-model.windows;
 if(command>=S13_APPEARANCE&&command<=S13_ACCESS){settings_page13[slot]=command-S13_APPEARANCE;a->hardware_view10=0;a->offset=0;a->notice[0]=0;control_active=0;whole();return 1;}
#ifdef ENGINE_M13
 if(command==59007){settings_page13[slot]=5;a->length=0;a->text[0]=0;a->year74=0;a->notice[0]=0;control_active=0;whole();return 1;}
 if(settings_page13[slot]==5&&command>=60100&&command<=60103){
  if(command==60100)notice(a,"Button activated. No files or preferences were changed.");
  if(command==60101){a->year74^=1;notice(a,a->year74&1?"Selected. Click again to clear.":"Selection cleared.");}
  if(command==60102){control_active=1;focused_control_window=token;focused_action=60102;}
  whole();return 1;
 }
#endif
 if(command==S13_CANCEL){settings_cancel13(token);return 1;}
 if(command==PREFERENCES_SAVE){if(settings_other13(token)){notice(a,"Apply or cancel the preview in the other Settings window first.");whole();return 1;}if(settings_busy13()){notice(a,"Finish or cancel the file operation before saving appearance. Your preview is kept.");whole();return 1;}unsigned status=appearance_save11();if(!status){settings_preview13.owner=0;settings_invalid13=0;}notice(a,status?"Saving failed. The preview remains active; retry or Cancel. Startup persistence is not claimed.":"Appearance and normal window sizes saved for your user.");serial_text(status?"M11_APPEARANCE_SAVE_FAILED\n":"M11_APPEARANCE_SAVED\n");whole();return 1;}
 if(command==32100||(command>=S13_CLICK_FAST&&command<=S13_CLICK_SLOW)||command==LAYOUT_US10||command==LAYOUT_DVORAK10){if(settings_busy13()){notice(a,"Finish or cancel the file operation before saving input preferences.");whole();return 1;}if(command==LAYOUT_US10||command==LAYOUT_DVORAK10)return 0;unsigned speed=interaction11.double_ms?interaction11.double_ms:500;speed=command==32100?(speed==200?500:speed==500?900:200):(command==S13_CLICK_FAST?200:command==S13_CLICK_NORMAL?500:900);unsigned record[2]={0x31314955,speed};unsigned status=v6_put(m6_volume(),"/System/Settings/input11.bin",sizeof(record),memory_source,record);if(!status)interaction11.double_ms=speed;notice(a,status?"The double-click interval could not be saved. The previous setting is kept.":"Double-click interval saved. Keyboard and mouse selection behavior are unchanged.");whole();return 1;}
 if(command==10000){a->offset=74;a->year74=0;a->notice[0]=0;control_active=0;whole();return 1;}
 if(command==45004){start_open11();start_manage11=3;whole();return 1;}
 unsigned visual=(command>=STYLE_MINT&&command<=STYLE_PAPER)||(command>=45000&&command<=45003)||(command>=SCALE_AUTO&&command<=SCALE_200)||command==S13_ACCENT_DEFAULT||command==S13_DEFAULTS;
 if(!visual)return 0;if(!settings_begin13(token))return 1;a->notice[0]=0;
 if(command>=STYLE_MINT&&command<=STYLE_AMBER){const unsigned colors[]={0x62e5bd,0x9caeff,0xf4c47c};preferences.accent=colors[command-STYLE_MINT];}
 else if(command==STYLE_DARK||command==STYLE_PAPER)preferences.dark=command==STYLE_DARK;
 else if(command==S13_ACCENT_DEFAULT)preferences.accent=DISTRO_ACCENT;
 else if(command>=45000&&command<45003){const unsigned colors[]={0x142c35,0x182039,0xd7e4e9};appearance11.wallpaper=colors[command-45000];}
 else if(command==45003)appearance11.pattern=(appearance11.pattern+1)%3;
 else if(command>=SCALE_AUTO&&command<=SCALE_200){if(settings_scale13(a,command==SCALE_AUTO?0:command-SCALE_AUTO+1))notice(a,"Display preview changed. Apply saves it; Cancel restores the previous choice.");}
 else if(command==S13_DEFAULTS){if(settings_scale13(a,0)){preferences.accent=DISTRO_ACCENT;preferences.dark=DISTRO_DESKTOP_DARK;appearance11.wallpaper=DISTRO_DESKTOP_WALLPAPER;appearance11.pattern=0;notice(a,"Distribution defaults previewed. Apply saves; Cancel restores. Apps and files are unchanged.");}}
 if(!settings_dirty13())settings_preview13.owner=0;whole();return 1;
}
static unsigned settings_key13(int key){
#ifdef ENGINE_M13
 if(!launcher&&!context11&&!guide_open11&&!file_dialog_state11.mode&&model.focused<DESKTOP_WINDOWS){
  desktop_window*w=&model.windows[model.focused];uint64_t token=desktop_token(&model,model.focused);
  if(w->live&&!w->minimized&&w->app==SETTINGS&&settings_page13[model.focused]==5&&control_active&&focused_control_window==token&&focused_action==60102&&!(input11_modifiers()&~2u)){
   application*a=&apps[model.focused];if(key==8){if(a->length)a->text[--a->length]=0;whole();return 1;}
   if(key>=32&&key<127){if(a->length<48){a->text[a->length++]=(char)key;a->text[a->length]=0;}whole();return 1;}
  }
 }
#endif
if(key!=27||launcher||context11||switch_open11||guide_open11||file_dialog_state11.mode||model.focused>=DESKTOP_WINDOWS)return 0;desktop_window*w=&model.windows[model.focused];if(!w->live||w->minimized||w->app!=SETTINGS||settings_preview13.owner!=desktop_token(&model,model.focused))return 0;settings_cancel13(settings_preview13.owner);return 1;}
