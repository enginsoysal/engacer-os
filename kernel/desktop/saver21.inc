/* Existing desktop buffers, timer wakeups and input providers; no extra worker. */
static saver_record21 saver_defaults21(void){return (saver_record21){0x31325345,1,0,60,0};}
static void saver_path21(char*path){copy(path,"/System/Settings/screensaver21-",256);append(path,owner.user,256);append(path,".bin",256);}
static void saver_load21(void){
 saver_saved21=saver_defaults21();char path[256];saver_path21(path);saver_record21 p;unsigned bytes=0;
 const v6_entry*stored=entry(path);if(stored){saver_invalid21=1;if(stored->size==sizeof(p)&&!v6_verify(m6_volume(),path)&&!v6_read(m6_volume(),path,0,&p,sizeof(p),&bytes)&&bytes==sizeof(p)&&p.magic==saver_saved21.magic&&p.version==1&&p.enabled<=1&&(p.seconds==60||p.seconds==300||p.seconds==600)&&p.style<=2){saver_saved21=p;saver_invalid21=0;}}
 saver_draft21=saver_saved21;saver_input21=input13_activity();saver_idle21=m3_clock_ticks();
}
static void saver_cancel21(uint64_t token){if(saver_owner21==token){saver_draft21=saver_saved21;saver_owner21=0;}}
static void saver_begin21(uint64_t token){if(!saver_owner21){saver_owner21=token;saver_draft21=saver_saved21;}}
static unsigned saver_action21(uint64_t token,unsigned command){
 if(command<S21_OPEN||command>S21_BACK)return 0;desktop_window*w=desktop_lookup(&model,token);if(!w||w->app!=SETTINGS)return 1;application*a=&apps[w-model.windows];
 if(command==S21_OPEN){settings_search_clear18(token);settings_page13[w-model.windows]=6;a->notice[0]=0;control_active=0;whole();return 1;}
 if(settings_page13[w-model.windows]!=6)return 1;
 if(command==S21_BACK){saver_cancel21(token);settings_page13[w-model.windows]=0;notice(a,"Screensaver changes cancelled. Your saved choices are kept.");whole();return 1;}
 if(saver_owner21&&saver_owner21!=token){notice(a,"Apply or cancel screensaver changes in the other Settings window first.");whole();return 1;}
 if(command==S21_CANCEL){saver_cancel21(token);notice(a,"Screensaver changes cancelled. Your saved choices are kept.");whole();return 1;}
 if(command==S21_APPLY){if(settings_busy13()){notice(a,"Finish or cancel the file operation first. Screensaver changes are kept.");whole();return 1;}char path[256];saver_path21(path);unsigned status=v6_put(m6_volume(),path,sizeof(saver_draft21),memory_source,&saver_draft21);if(!status){saver_saved21=saver_draft21;saver_owner21=0;saver_invalid21=0;saver_idle21=m3_clock_ticks();}notice(a,status?"Screensaver could not be saved. Try Apply again or Cancel changes.":"Screensaver choices saved for your user.");whole();return 1;}
 if(command==S21_PREVIEW){saver_style21=saver_owner21?saver_draft21.style:saver_saved21.style;saver_phase21=1;saver_input21=input13_activity();saver_quiet21=m3_clock_ticks();whole();return 1;}
 saver_begin21(token);
 if(command==S21_OFF||command==S21_ON)saver_draft21.enabled=command==S21_ON;
 else if(command>=S21_MINUTE&&command<=S21_TEN)saver_draft21.seconds=command==S21_MINUTE?60:command==S21_FIVE?300:600;
 else if(command>=S21_LOGO&&command<=S21_BLANK)saver_draft21.style=command-S21_LOGO;
 else if(command==S21_DEFAULTS)saver_draft21=saver_defaults21();
 notice(a,"Changes are not saved. Apply keeps them; Cancel or leaving this page restores them.");whole();return 1;
}
static void saver_settings21(desktop_window*w,application*a,uint64_t token,int x,int top,int width){
 ui12_palette p=desktop_palette16();unsigned other=saver_owner21&&saver_owner21!=token;const saver_record21*r=saver_owner21==token?&saver_draft21:&saver_saved21;
 ui73_paragraph(x,top,width,2,"A quiet screen while you are away. Move the mouse or press a key to return. This does not lock your computer.",p.ink);
 settings_button13(token,x,top+46,140,"Off",S21_OFF,!r->enabled,!other);settings_button13(token,x+152,top+46,140,"On",S21_ON,r->enabled,!other);
 ui73_fit(x,top+94,width,"Start after no keyboard or mouse activity",UI12_BODY,p.ink);
 const char*waits[]={"1 minute","5 minutes","10 minutes"};const unsigned times[]={60,300,600};for(unsigned i=0;i<3;++i)settings_button13(token,x+(int)i*160,top+118,152,waits[i],S21_MINUTE+i,r->seconds==times[i],!other);
 ui73_fit(x,top+164,width,"Style",UI12_BODY,p.ink);const char*styles[]={"Engacer logo","Clock","Blank"};for(unsigned i=0;i<3;++i)settings_button13(token,x+(int)i*160,top+188,152,styles[i],S21_LOGO+i,r->style==i,!other);
 settings_button13(token,x,top+232,152,"Preview",S21_PREVIEW,0,!other);settings_button13(token,x+164,top+232,152,"Back",S21_BACK,0,1);
 int footer=w->bounds.y+w->bounds.height-116;settings_button13(token,x,footer,164,"Apply and save",S21_APPLY,0,!other&&saver_owner21==token);settings_button13(token,x+176,footer,164,"Cancel changes",S21_CANCEL,0,saver_owner21==token);settings_button13(token,x+352,footer,width-352,"Restore defaults",S21_DEFAULTS,0,!other);
 const char*message=other?"Apply or cancel screensaver changes in the other Settings window first.":a->notice[0]?a->notice:saver_invalid21?"Saved screensaver choices were invalid. Off is active. Apply saves valid choices.":"Off is the default. Preview never saves. Reduced motion keeps the logo still.";
 ui73_paragraph(x,w->bounds.y+w->bounds.height-64,width,2,message,p.ink);
}
static uint64_t saver_stamp21(uint64_t now){return now/(saver_style21==1?6000u:100u);}
static unsigned saver_work21(int key){
 uint64_t now=m3_clock_ticks(),activity=input13_activity();unsigned changed=activity!=saver_input21;if(changed){saver_input21=activity;saver_idle21=now;}
 if(saver_phase21==1){if(!input13_held()&&key<0){saver_phase21=2;saver_frame21=saver_stamp21(now);whole();return 1;}return 0;}
 if(saver_phase21==2){if(changed){saver_phase21=3;saver_quiet21=now+5;whole();return 1;}if(saver_style21!=2&&saver_stamp21(now)!=saver_frame21){saver_frame21=saver_stamp21(now);if(saver_style21==1||!(access_flags16&2)){whole();return 1;}}return 0;}
 if(saver_phase21==3){if(changed||key>=0||input13_held())saver_quiet21=now+5;else if(now>=saver_quiet21){saver_phase21=0;saver_idle21=now;whole();return 1;}return 0;}
 if(changed||input13_held()||dragging||window_keyboard_move11){saver_idle21=now;return 0;}
 if(saver_saved21.enabled&&now-saver_idle21>=(uint64_t)saver_saved21.seconds*100){saver_style21=saver_saved21.style;saver_phase21=2;saver_frame21=saver_stamp21(now);whole();return 1;}return 0;
}
static unsigned saver_capture21(int key){
 if(!saver_phase21)return 0;
 if(key==256)usb_mouse_state(&pointer_x,&pointer_y,&previous_buttons);
 if(key==138)(void)input10_take_wheel();
 return 1;
}
static void saver_draw21(void){
 rectangle((desktop_rect){0,0,(int)model.width,(int)model.height},0);if(saver_style21==2)return;
 int width=(int)model.width,height=(int)model.height,x=(width-320)/2,y=(height-180)/2;
 if(!(access_flags16&2)){unsigned dx=(unsigned)(width-360),dy=(unsigned)(height-220);x=20+(int)(saver_frame21*13%(dx?dx:1));y=20+(int)(saver_frame21*7%(dy?dy:1));}
 if(saver_style21==1){clock7_time now;char label[32]="Clock unavailable";if(!clock7_read(&now)){padded74(label,now.hour);append(label,":",32);char part[8];padded74(part,now.minute);append(label,part,32);append(label," UTC",32);}ui73_fit(x,y+40,320,label,6,0xffffff);}
 else{ui12_icon_ink(ICON12_START,x+130,y,60,0xffffff);ui73_fit(x+48,y+90,272,ENGINE_PRODUCT_NAME,UI12_HEADING,0xffffff);}
 ui73_fit(24,height-42,width-48,"Move the mouse or press a key to return.",UI12_BODY,0xffffff);
}
