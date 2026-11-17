/* Provider-backed, event-driven quick controls. No worker or retained pixels. */
static void tray_changed12(void){invalidate((desktop_rect){(int)model.width-180,(int)model.height-60,180,60});if(tray_open12)invalidate(tray_bounds12);}
static void tray_close12(void){tray_open12=0;control_active=0;whole();}
static void tray_today12(void){clock7_time now;if(!clock7_read(&now)&&now.year>=2000&&now.year<=2099){tray_year12=now.year;tray_month12=now.month;tray_day12=now.day;}else tray_year12=tray_month12=tray_day12=0;}
static void tray_begin12(unsigned mode){
 if(model.width<800||model.height<600){copy(shell_notice,"Quick settings needs 800x600 or larger. Open Settings.",96);whole();return;}
 if(dragging)window_drag_end11(1);if(file_drag11)files_cancel_drag11();component_scroll_cancel12();i11_cancel(&interaction11);
 switch_open11=launcher=context11=0;tray_open12=mode;tray_focus12=tray_usb_page12=control_active=0;tray_notice12[0]=0;tray_today12();whole();
}
static void tray_button12(uint64_t owner,int x,int y,int width,const char*label,unsigned action,unsigned primary,unsigned enabled){
 if(enabled)button(owner,x,y,width,label,action,primary);else component_button12(owner,(desktop_rect){x,y,width,36},label,action,primary,0);
}
static unsigned tray_usb_count12(void){unsigned count=0;for(unsigned i=0;i<storage_count();++i){const storage_disk*d=storage_get(i);if(d&&d->transport==STORAGE_USB&&d->readable)++count;}return count;}
static uint64_t tray_drive_owner12(unsigned index,const storage_disk*d){return UINT64_C(0x8000000000000000)|((uint64_t)d->context<<16)|(index+1);}
static void tray_bar12(int bar){
 if(model.width<1000){icon_button12(0,(int)model.width-56,bar+15,40,"",TR12_OPEN,tray_open12,ICON12_SETTINGS);return;}
 unsigned count=control_count;task_clock74(bar);if(control_count==count+1)--control_count;
 clock7_time now;if(clock7_read(&now)){ui73_fit((int)model.width-82,bar+12,64,"System",1,0xe5eef2);text((int)model.width-168,bar+34,"Time unavailable",5,0xabb7c6);}
 else{char value[40],part[8];padded74(value,now.hour);append(value,":",40);padded74(part,now.minute);append(value,part,40);append(value," UTC",40);rectangle((desktop_rect){(int)model.width-96,bar+2,96,28},0x0b1922);ui73_fit((int)model.width-96,bar+8,88,value,1,0xe5eef2);}
 access_capture16(0,TR12_DATE,"Date and time",1);
 if(component_state12(0,TR12_DATE)&UI12_FOCUS){rectangle((desktop_rect){(int)model.width-96,bar+2,94,2},0xffffff);rectangle((desktop_rect){(int)model.width-96,bar+56,94,2},0xffffff);rectangle((desktop_rect){(int)model.width-96,bar+2,2,56},0xffffff);rectangle((desktop_rect){(int)model.width-4,bar+2,2,56},0xffffff);}
 if(control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){{(int)model.width-180,bar,180,60},0,TR12_DATE};
 const unsigned actions[]={TR12_NETWORK,TR12_USB_OPEN,TR12_SOUND};const unsigned icons[]={ICON12_NETWORK,ICON12_USB,ICON12_SOUND};
 net7_configuration net=net7_current();audio74_info audio=audio74_current();
 for(unsigned i=0;i<3;++i){int x=(int)model.width-172+(int)i*26;unsigned active=i==0?net.state==NET7_CONNECTED:i==1?tray_usb_count12()!=0:audio.state==AUDIO74_PLAYING;
  ui12_icon_ink(icons[i],x,bar+8,20,active?0x62e5bd:0xabb7c6);
  access_capture16(0,actions[i],i==0?"Network status":i==1?"USB drives":"Sound and volume",1);
  if(component_state12(0,actions[i])&UI12_FOCUS)rectangle((desktop_rect){x,bar+31,22,2},0xffffff);
  if(control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){{x-2,bar+4,24,28},0,actions[i]};
 }
 if(tray_open12||(component_state12(0,TR12_DATE)&UI12_FOCUS))rectangle((desktop_rect){(int)model.width-176,bar+57,168,2},preferences.accent);
}
static unsigned tray_navigation12(unsigned index,control*out){
 unsigned found=0;desktop_rect b=tray_bounds12;
 for(unsigned i=0;i<control_count;++i){control*c=&controls[i];desktop_rect r=c->rect;if(c->action<TR12_QUICK||c->action>=TR12_END||r.x<b.x||r.y<b.y||r.x+r.width>b.x+b.width||r.y+r.height>b.y+b.height)continue;
  if(found++==index&&out)*out=*c;
 }return found;
}
static void tray_quick12(int x,int y,int width){
 ui12_palette p=desktop_palette16();net7_configuration net=net7_current();audio74_info audio=audio74_current();char value[96],part[24];
 ui12_icon(ICON12_NETWORK,x,y,24,preferences.dark);ui73_fit(x+34,y+3,width-34,net.state==NET7_CONNECTED?"Local network connected":net.state==NET7_CONFIGURING?"Connecting to the local network":net.state==NET7_NO_INTERFACE?"No supported network interface":net.state==NET7_FAILED?"Network setup failed":"Network disconnected",1,p.ink);
 if(net.state==NET7_CONNECTED){copy(value,"IPv4 ",96);for(unsigned i=0;i<4;++i){decimal(part,(net.address>>(24-i*8))&255);append(value,part,96);if(i<3)append(value,".",96);}append(value," - Internet not checked",96);}
 else copy(value,net.state==NET7_NO_INTERFACE?"No compatible wired-network provider is active.":net.state==NET7_CONFIGURING?"Automatic DHCP is in progress.":"Check the connection, then choose Retry.",96);
 ui73_fit(x,y+34,width,value,5,p.muted);
 tray_button12(0,x,y+62,142,"Retry network",TR12_RETRY,0,net.state==NET7_DISCONNECTED||net.state==NET7_FAILED);tray_button12(0,x+150,y+62,width-150,"Devices",TR12_DEVICES,0,1);
 ui12_icon(ICON12_SOUND,x,y+118,24,preferences.dark);ui73_fit(x+34,y+121,width-34,audio.state==AUDIO74_PLAYING?"Audio: playing":audio.state==AUDIO74_PAUSED?"Audio: paused":audio.state==AUDIO74_FAILED?"Audio: playback unavailable":"Audio: idle",1,p.ink);
 ui73_fit(x,y+151,width,audio.state==AUDIO74_FAILED?"Open Media Player for the playback failure details.":"Hardware support is checked when playback starts.",5,p.muted);
 tray_button12(0,x,y+178,90,"Quieter",TR12_QUIETER,0,audio.volume!=0);tray_button12(0,x+98,y+178,90,"Louder",TR12_LOUDER,0,audio.volume<100);tray_button12(0,x+196,y+178,90,audio.volume?"Mute":"Unmute",TR12_MUTE,0,1);
 decimal(value,audio.volume);append(value,"%",96);ui73_fit(x+298,y+188,width-298,value,1,p.ink);ui73_fit(x,y+222,width,"Software PCM playback level; applies to supported audio.",5,p.muted);
 tray_button12(0,x,y+252,190,"Settings",TR12_SETTINGS,0,1);tray_button12(0,x+198,y+252,width-198,"Media Player",TR12_MEDIA,0,1);
 ui73_fit(x,y+306,width,"Wi-Fi, Bluetooth and battery controls: unavailable.",5,p.muted);ui73_fit(x,y+326,width,"Those providers are not implemented in this build.",5,p.muted);
}
static void tray_drives12(int x,int y,int width){
 ui12_palette p=desktop_palette16();unsigned count=tray_usb_count12();if(tray_usb_page12*4>=count)tray_usb_page12=0;
 ui73_fit(x,y,width,"Open a drive, or flush and safely remove it.",1,p.ink);
 if(!count){ui73_paragraph(x,y+52,width,3,"No readable USB drive is connected. Connect one to use it. Opening this panel never formats or erases a disk.",p.ink);}
 unsigned ordinal=0,shown=0;
 for(unsigned i=0;i<storage_count()&&shown<4;++i){const storage_disk*d=storage_get(i);if(!d||d->transport!=STORAGE_USB||!d->readable)continue;if(ordinal++<tray_usb_page12*4)continue;
  int top=y+38+(int)shown++*62;char label[64]="USB drive ",number[24];decimal(number,i+1);append(label,number,64);append(label," - ",64);decimal(number,d->sectors*(uint64_t)d->sector_bytes/(1024*1024));append(label,number,64);append(label," MiB",64);
  ui73_fit(x,top,width-206,label,1,p.ink);ui73_fit(x,top+23,width-206,storage_writable(d)?"Read and write":"Read only",5,p.muted);uint64_t owner=tray_drive_owner12(i,d);
  tray_button12(owner,x+width-198,top,76,"Open",TR12_DRIVE+i,0,1);tray_button12(owner,x+width-114,top,114,"Safe remove",TR12_EJECT+i,0,1);
 }
 tray_button12(0,x,y+300,100,"Previous",TR12_USB_PREV,0,tray_usb_page12!=0);tray_button12(0,x+108,y+300,100,"Next",TR12_USB_NEXT,0,(tray_usb_page12+1)*4<count);tray_button12(0,x+216,y+300,width-216,"Refresh",TR12_REFRESH,0,1);
}
static void tray_calendar12(int x,int y,int width){
 ui12_palette p=desktop_palette16();clock7_time now;
 unsigned unavailable=clock7_read(&now);if(!unavailable&&!tray_year12&&now.year>=2000&&now.year<=2099){tray_year12=now.year;tray_month12=now.month;tray_day12=now.day;}
 if(unavailable||!tray_year12){ui73_paragraph(x,y,width,3,"Calendar is unavailable for this clock value. Supported years: 2000-2099. Other quick controls remain available.",p.ink);return;}
 static const char*months[]={"January","February","March","April","May","June","July","August","September","October","November","December"};char title[64],number[24];copy(title,months[tray_month12-1],64);append(title," ",64);decimal(number,tray_year12);append(title,number,64);append(title," - UTC",64);
 tray_button12(0,x,y,44,"<",TR12_MONTH_PREV,0,tray_year12>2000||tray_month12>1);ui73_fit(x+54,y+9,width-108,title,1,p.ink);tray_button12(0,x+width-44,y,44,">",TR12_MONTH_NEXT,0,tray_year12<2099||tray_month12<12);
 static const char*week[]={"Mon","Tue","Wed","Thu","Fri","Sat","Sun"};int cell=width/7;for(unsigned i=0;i<7;++i)ui73_fit(x+(int)i*cell+5,y+48,cell-6,week[i],5,p.muted);
 clock7_time first;unsigned leading=0;if(!clock7_calendar(tray_year12,tray_month12,1,0,0,0,&first))leading=(first.days+5)%7;
 for(unsigned day=1;day<=days74(tray_year12,tray_month12);++day){unsigned index=leading+day-1;decimal(number,day);int xx=x+(int)(index%7)*cell,yy=y+70+(int)(index/7)*38;tray_button12(0,xx,yy,cell-4,number,TR12_DAY+day,tray_day12==day,1);if(now.year==tray_year12&&now.month==tray_month12&&now.day==day)rectangle((desktop_rect){xx+10,yy+33,cell-24,2},preferences.accent);}
 tray_button12(0,x,y+304,100,"Today",TR12_TODAY,0,1);tray_button12(0,x+108,y+304,width-108,"Open Calendar",TR12_CALENDAR_APP,0,1);
}
static void tray_draw12(void){
 if(!tray_open12)return;tray_bounds12=(desktop_rect){(int)model.width-456,(int)model.height-584,440,508};desktop_rect r=tray_bounds12;ui12_palette p=desktop_palette16();
 desktop_shadow16(r.x,r.y,r.width,r.height);ui73_round(r.x,r.y,r.width,r.height,12,p.paper);ui73_fit(r.x+16,r.y+15,r.width-112,"System",3,p.ink);tray_button12(0,r.x+r.width-92,r.y+10,76,"Close",TR12_CLOSE,0,1);
 const char*tabs[]={"Quick settings","USB drives","Calendar"};for(unsigned i=0;i<3;++i)tray_button12(0,r.x+16+(int)i*136,r.y+54,128,tabs[i],TR12_QUICK+i,tray_open12==i+1,1);
 int x=r.x+16,y=r.y+104,width=r.width-32;if(tray_open12==1)tray_quick12(x,y,width);else if(tray_open12==2)tray_drives12(x,y,width);else tray_calendar12(x,y,width);
 if(tray_notice12[0])ui73_paragraph(x,r.y+r.height-56,width,2,tray_notice12,p.ink);else ui73_fit(x,r.y+r.height-36,width,"Tab chooses a control. Enter opens. Escape closes.",5,p.muted);
}
static i11_target tray_target12(int x,int y){
 for(unsigned i=control_count;i;--i){control*c=&controls[i-1];desktop_rect r=c->rect;if(c->action>=TR12_OPEN&&c->action<TR12_END&&x>=r.x&&y>=r.y&&x<r.x+r.width&&y<r.y+r.height)return(i11_target){c->window,c->action,I11_BUTTON};}
 if(y>=(int)model.height-60)for(unsigned i=control_count;i;--i){control*c=&controls[i-1];desktop_rect r=c->rect;if(!c->window&&(c->action==0||(c->action>=S11_PINNED&&c->action<S11_END))&&x>=r.x&&y>=r.y&&x<r.x+r.width&&y<r.y+r.height)return(i11_target){0,c->action,I11_BUTTON};}
 return(i11_target){0,0,I11_BACKGROUND};
}
static uint64_t tray_launch12(unsigned kind){
 if(!app7_available(kind)){copy(tray_notice12,"This optional app is not installed. Use Settings > Applications.",160);whole();return 0;}
 uint64_t token=launch(kind,0);if(!token){copy(tray_notice12,"Close a window first. Up to eight windows may be open.",160);whole();}return token;
}
static unsigned tray_action12(uint64_t owner,unsigned command){
 if(command<TR12_OPEN||command>=TR12_END)return 0;
 if(command==TR12_OPEN||command==TR12_NETWORK||command==TR12_SOUND||command==TR12_DATE||command==TR12_USB_OPEN){unsigned mode=command==TR12_DATE?3:command==TR12_USB_OPEN?2:1;if(tray_open12==mode)tray_close12();else tray_begin12(mode);return 1;}
 if(!tray_open12)return 1;
 if(command==TR12_CLOSE){tray_close12();return 1;}
 if(command>=TR12_QUICK&&command<=TR12_CALENDAR){tray_open12=command-TR12_QUICK+1;tray_notice12[0]=0;control_active=0;tray_focus12=0;whole();return 1;}
 if(command==TR12_RETRY){unsigned state=net7_current().state;if(state==NET7_DISCONNECTED||state==NET7_FAILED){net7_retry();copy(tray_notice12,"Retrying automatic local-network configuration.",160);}}
 else if(command==TR12_QUIETER||command==TR12_LOUDER||command==TR12_MUTE){unsigned volume=audio74_current().volume;if(command==TR12_QUIETER)volume=volume>=10?volume-10:0;else if(command==TR12_LOUDER)volume=volume<=90?volume+10:100;else if(volume){tray_previous_volume12=volume;volume=0;}else volume=tray_previous_volume12?tray_previous_volume12:100;
  audio74_volume(volume);
  if(files_busy12()||file_dialog_state11.mode||w8_pending())copy(tray_notice12,"Level changed for this session. Finish the file operation, then change it again to save.",160);
  else{unsigned values[2]={0x41443734,volume};unsigned status=v6_put(m6_volume(),"/System/Settings/audio74.bin",sizeof(values),memory_source,values);copy(tray_notice12,status?"Playback level changed for this session; saving failed.":"Playback level saved for the next start.",160);}
 }else if(command==TR12_SETTINGS||command==TR12_DEVICES||command==TR12_MEDIA||command==TR12_CALENDAR_APP){unsigned kind=command==TR12_MEDIA?MEDIA74:command==TR12_CALENDAR_APP?CALENDAR74:SETTINGS;uint64_t token=tray_launch12(kind);desktop_window*w=desktop_lookup(&model,token);if(w){application*a=&apps[w-model.windows];if(command==TR12_DEVICES)devices_action10(w,a,token,DEVICES10);if(command==TR12_CALENDAR_APP&&tray_year12){a->year74=(int)tray_year12;a->month74=(int)tray_month12;a->day74=(int)tray_day12;calendar_load74(a);}tray_close12();}return 1;
 }else if(command==TR12_TODAY)tray_today12();
 else if(command==TR12_MONTH_PREV){if(tray_year12>2000||tray_month12>1){if(tray_month12>1)--tray_month12;else{--tray_year12;tray_month12=12;}tray_day12=1;}}
 else if(command==TR12_MONTH_NEXT){if(tray_year12<2099||tray_month12<12){if(tray_month12<12)++tray_month12;else{++tray_year12;tray_month12=1;}tray_day12=1;}}
 else if(command>TR12_DAY&&command<=TR12_DAY+31){unsigned day=command-TR12_DAY;if(tray_year12&&day<=days74(tray_year12,tray_month12))tray_day12=day;}
 else if(command==TR12_USB_PREV){if(tray_usb_page12)--tray_usb_page12;}
 else if(command==TR12_USB_NEXT){if((tray_usb_page12+1)*4<tray_usb_count12())++tray_usb_page12;}
 else if(command==TR12_REFRESH)hw10_refresh();
 else if((command>=TR12_DRIVE&&command<TR12_DRIVE+STORAGE_MAX)||(command>=TR12_EJECT&&command<TR12_EJECT+STORAGE_MAX)){
  unsigned eject=command>=TR12_EJECT,disk=command-(eject?TR12_EJECT:TR12_DRIVE);const storage_disk*d=storage_get(disk);
  if(!d||d->transport!=STORAGE_USB||!d->readable||owner!=tray_drive_owner12(disk,d)){copy(tray_notice12,"The drive changed or disconnected. Choose the connected drive again.",160);whole();return 1;}
  unsigned context=d->context;
  if(eject){if(files_busy12()||w8_pending())copy(tray_notice12,"Finish or cancel the transfer before removing a drive.",160);else{unsigned status=usb10_eject(disk,context);copy(tray_notice12,status==B_ABSENT?"The drive disconnected; it is not reported as safely removed.":status?"Safe removal failed. Keep the drive connected and check Devices.":"Safe to unplug the USB drive. Reconnect it to use it again.",160);if(!status){hw10_refresh();for(unsigned i=0;i<DESKTOP_WINDOWS;++i)if(model.windows[i].live&&model.windows[i].app==FILES&&apps[i].usb_mode10){apps[i].usb_selected10=0;invalidate(model.windows[i].bounds);}}}}
  else{uint64_t token=tray_launch12(FILES);desktop_window*w=desktop_lookup(&model,token);if(w){application*a=&apps[w-model.windows];devices_action10(w,a,token,USB_OPEN10);a->usb_selected10=disk+1;a->usb_context10=context;devices_action10(w,a,token,USB_DISK10+disk);tray_close12();return 1;}}
 }
 control_active=0;whole();return 1;
}
static unsigned tray_key12(int key){
 if(key==151){if(tray_open12==1)tray_close12();else tray_begin12(1);return 1;}
 if(!tray_open12)return 0;
 if(key==135||key==143||key==137){tray_close12();return 0;}
 if(key==27||key==141||key==144){tray_close12();return 1;}
 unsigned count=tray_navigation12(0,0);if(!count)return 1;
 if(key==9||key==134||key==129||key==136||key==133||key==128){unsigned reverse=key==136||key==133||key==128;if(!control_active)tray_focus12=reverse?count-1:0;else tray_focus12=(tray_focus12+(reverse?count-1:1))%count;control choice;if(tray_navigation12(tray_focus12,&choice)){control_active=1;focused_action=choice.action;focused_control_window=choice.window;}whole();}
 else if(key==10||key==32){control choice;if(!control_active)tray_focus12=0;if(tray_focus12>=count)tray_focus12=0;tray_navigation12(tray_focus12,&choice);tray_action12(choice.window,choice.action);}
 return 1;
}
