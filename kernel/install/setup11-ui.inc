/* Original M11.5 pages share the existing damage-only wizard compositor. */
#define SETUP_TITLE11(symbol,kind,id,title,worker,ready) [kind]=title,
static const char *setup_titles11[APP74_KINDS]={[1]="Files",[3]="Settings",APP74_CATALOG(SETUP_TITLE11)};
#undef SETUP_TITLE11
static unsigned setup_count11(void){unsigned n=0;for(unsigned i=1;i<APP74_KINDS;++i)if(setup11.apps&(1u<<i))++n;return n;}
static unsigned setup_visual11(void){return step?step+1:keyboard_page11;}
static void setup_keyboard11(unsigned x,unsigned y,unsigned cw){
 label(x,y,"Your keyboard and display",4,0x193746);
 ui73_paragraph(x,y+52,cw,2,"Choose a layout, then try typing below. Everything works offline.",0x506976);
 unsigned half=(cw-12)/2;
 tap75(x,y+112,half,48,"US QWERTY",50000,setup11.layout?0:1);
 tap75(x+half+12,y+112,half,48,"US Dvorak",50001,setup11.layout?1:0);
 tap75(x,y+180,cw-100,48,keyboard_test11[0]?keyboard_test11:"Click here to test your keyboard",50002,0);
 tap75(x+cw-88,y+180,88,48,"Clear",50003,0);
 label(x,y+254,"Text and control size",2,0x193746);
 const char *sizes[]={"Auto","100%","150%","200%"};unsigned w=(cw-36)/4;
 for(unsigned i=0;i<4;++i)tap75(x+i*(w+12),y+290,w,46,sizes[i],50010+i,setup11.scale==(i?i+1:0)?1:0);
 ui73_paragraph(x,y+363,cw,2,validation?validation:"Language: English. Clock: UTC. More languages and regional formats are not available in this release.",validation?0x994334:0x506976);
}
static void setup_apps11(unsigned x,unsigned y,unsigned cw){
 label(x,y,"Choose what comes with you",4,0x193746);
 ui73_paragraph(x,y+52,cw,2,"Desktop, Files, Settings and recovery services stay. All other apps are optional and can be reinstalled offline.",0x506976);
 unsigned w=(cw-24)/3;
 tap75(x,y+114,w,44,"All available",50100,0);tap75(x+w+12,y+114,w,44,"Essentials",50101,0);tap75(x+2*(w+12),y+114,w,44,"No optional apps",50102,0);
 unsigned row=0,seen=0,total=0;for(unsigned k=1;k<APP74_KINDS;++k)if(DISTRO_APPS74_MASK&(1u<<k))++total;
 for(unsigned k=1;k<APP74_KINDS;++k){if(!(DISTRO_APPS74_MASK&(1u<<k)))continue;if(seen++<apps_page11*6)continue;if(row>=6)break;
  unsigned at=controls;tap75(x+(row%2)*((cw+12)/2),y+178+(row/2)*58,(cw-12)/2,48,setup_titles11[k],50200+k,setup11.apps&(1u<<k)?1:0);(void)at;++row;
 }
 tap75(x,y+362,100,42,"Previous",50103,apps_page11?0:2);tap75(x+112,y+362,100,42,"More apps",50104,(apps_page11+1)*6<total?0:2);
 char count[48];decimal(setup_count11(),count);unsigned n=0;while(count[n])++n;memcpy(count+n," optional apps selected",24);label(x+230,y+376,count,1,0x506976);
 tap75(x,y+420,cw,46,preferences.guide?"[x] Show a short first-start guide":"[ ] Show a short first-start guide",20,0);
}
static void setup_name11(unsigned x,unsigned y,unsigned cw){
 tap75(x,y,cw,52,preferences.user[0]?preferences.user:"Type your account name",30,0);
 if(focus<controls&&buttons[focus].action==30){
  unsigned lo=name_cursor11<name_anchor11?name_cursor11:name_anchor11,hi=name_cursor11>name_anchor11?name_cursor11:name_anchor11;
  char prefix[32];memcpy(prefix,preferences.user,lo);prefix[lo]=0;unsigned a=ui73_measure(prefix,2);memcpy(prefix,preferences.user,hi);prefix[hi]=0;unsigned b=ui73_measure(prefix,2);
  if(hi>lo){gui6_rect(x+16+a,y+12,b-a,26,0xd5eee5);ui73_fit(x+16,y+15,cw-32,preferences.user,2,0x193746);}
  memcpy(prefix,preferences.user,name_cursor11);prefix[name_cursor11]=0;gui6_rect(x+16+ui73_measure(prefix,2),y+12,2,26,0x19846e);
 }
}
static void setup_style11(unsigned x,unsigned y,unsigned cw){
 label(x,y,"Make yourself at home",4,0x193746);label(x,y+55,"Your account name",2,0x193746);setup_name11(x,y+85,cw);
 ui73_paragraph(x,y+148,cw,1,"Letters, numbers, - or _. Select the box to replace Owner. No online account is required.",0x506976);
 unsigned w=(cw-24)/3;const unsigned colors[]={0x62e5bd,0x9caeff,0xf4c47c};const char*names[]={"Mint","Lavender","Amber"};
 label(x,y+203,"Accent",1,0x506976);for(unsigned i=0;i<3;++i)tap75(x+i*(w+12),y+229,w,44,names[i],31+i,accent==colors[i]?1:0);
 label(x,y+290,"Desktop appearance",1,0x506976);tap75(x,y+316,120,44,"Light",50300,setup11.dark?0:1);tap75(x+132,y+316,120,44,"Dark",50301,setup11.dark?1:0);
 const unsigned wallpapers[]={0x142c35,0x182039,0xd7e4e9};const char*wallnames[]={"Ocean","Night","Paper"};
 label(x,y+378,"Wallpaper",1,0x506976);for(unsigned i=0;i<3;++i)tap75(x+i*(w+12),y+401,w,44,wallnames[i],50310+i,setup11.wallpaper==wallpapers[i]?1:0);
 ui73_paragraph(x,y+459,cw,1,validation?validation:"Your colours, keyboard and display choices will be saved to your installed desktop.",validation?0x994334:0x506976);
}
static void setup_review11(unsigned x,unsigned y,unsigned cw){
 label(x,y,maintenance?"Review recovery":"Ready to make it yours?",4,0x193746);
 ui73_paragraph(x,y+54,cw,2,maintenance?"Only verified boot files change. Personal files stay.":"Check every choice. Installation uses the whole selected disk.",0x506976);
 char disk[32],size[32],apps[32];diskname75(chosen,disk);capacity75(storage_get(chosen),size);decimal(setup_count11(),apps);
 unsigned n=0;while(apps[n])++n;memcpy(apps+n," optional apps",15);
 if(maintenance){ui73_round(x,y+112,cw,172,10,0xeaf0f4);label(x+20,y+134,"Selected disk",2,0x506976);ui73_fit(x+190,y+134,cw-210,disk,2,0x193746);label(x+20,y+180,"Operation",2,0x506976);ui73_fit(x+190,y+180,cw-210,maintenance==1?"Repair boot files":maintenance==2?"Update boot slot":"Restore previous boot slot",2,0x193746);ui73_paragraph(x+20,y+228,cw-40,2,"Your existing account, apps, files and appearance are kept.",0x506976);return;}
 char style[80];const char*parts[]={setup11.dark?"Dark":"Light",setup11.wallpaper==0x182039?"Night":setup11.wallpaper==0xd7e4e9?"Paper":"Ocean",accent==0x9caeff?"Lavender":accent==0xf4c47c?"Amber":"Mint"};unsigned at=0;for(unsigned i=0;i<3;++i){if(i){memcpy(style+at," / ",3);at+=3;}const char*p=parts[i];while(*p)style[at++]=*p++;}style[at]=0;
 const char*keys[]={"Install on","Capacity","Account","Keyboard","Apps","Appearance","Display size","First-start guide"};
 const char*values[]={disk,size,preferences.user,setup11.layout?"US Dvorak":"US QWERTY",apps,style,setup11.scale==2?"100%":setup11.scale==3?"150%":setup11.scale==4?"200%":"Automatic",preferences.guide?"Show once":"Off"};
 ui73_round(x,y+108,cw,278,10,0xeaf0f4);for(unsigned i=0;i<8;++i){label(x+16,y+124+i*31,keys[i],1,0x506976);ui73_fit(x+172,y+124+i*31,cw-188,values[i],2,0x193746);}
 if(!maintenance&&replace_selected)tap75(x,y+404,cw,48,replace_consent?"[x] Erase every partition on this disk":"[ ] I agree to erase this entire disk",92,3);
 ui73_paragraph(x,y+465,cw,1,validation?validation:replace_selected?"Erasure cannot be undone. Other disks are not installation targets.":"Back changes your choices. Install starts real disk writes.",validation?0x994334:0x506976);
}
static unsigned setup_action11(unsigned a){
 if(busy)return 0;
 if(a==2&&!maintenance&&step==0){if(!keyboard_page11){keyboard_page11=1;keyboard_test11[0]=0;keyboard_test_length11=0;}else{keyboard_page11=0;step=1;}validation=0;focus=0;render();return 1;}
 if(a==1&&!maintenance&&(keyboard_page11||step==1)){keyboard_page11=!keyboard_page11;step=0;replace_consent=0;m6_cancel();validation=0;focus=0;render();return 1;}
 if(a==30&&step==3){name_cursor11=0;while(preferences.user[name_cursor11])++name_cursor11;name_anchor11=0;render();return 1;}
 if(a>=50000&&a<=50003&&keyboard_page11){if(a<50002){setup11.layout=a-50000;input10_set_layout(setup11.layout);}else if(a==50003){keyboard_test11[0]=0;keyboard_test_length11=0;}validation=0;render();return 1;}
 if(a>=50010&&a<=50013&&keyboard_page11){unsigned choice=a==50010?0:a-50009;const os_boot_info_v0*b=ui73_set_scale(choice);if(!b){validation="That size needs a larger display. Your previous size is unchanged.";render();return 1;}
  setup11.scale=choice;screen=b;width=b->framebuffer_width>1200?1160:b->framebuffer_width-40;height=b->framebuffer_height>740?700:b->framebuffer_height-40;left=(b->framebuffer_width-width)/2;top=(b->framebuffer_height-height)/2;body=left+220;bottom=top+height-70;usb_mouse_limits(ui73_width(),ui73_height());framed75=0;validation=0;render();return 1;}
 if(step==2&&a>=50100&&a<=50104){if(a<50103){setup11.apps=a==50100?DISTRO_APPS74_MASK:a==50101?DISTRO_APPS74_MASK&((1u<<2)|(1u<<4)|(1u<<7)|(1u<<8)):0;}else if(a==50103&&apps_page11)--apps_page11;else if(a==50104&&apps_page11<2)++apps_page11;calculator_selection=!!(setup11.apps&(1u<<4));render();return 1;}
 if(step==2&&a>=50200&&a<50200+APP74_KINDS){unsigned bit=1u<<(a-50200);setup11.apps^=bit&DISTRO_APPS74_MASK;calculator_selection=!!(setup11.apps&(1u<<4));render();return 1;}
 if(step==3&&a>=50300&&a<=50312){if(a<=50301)setup11.dark=a-50300;else if(a>=50310){const unsigned c[]={0x142c35,0x182039,0xd7e4e9};setup11.wallpaper=c[a-50310];}render();return 1;}
 return 0;
}
static unsigned setup_key11(int key){
 if(key==27&&keyboard_page11){setup_action11(1);return 1;}
 if(keyboard_page11&&focus<controls&&buttons[focus].action==50002){if(key==8&&keyboard_test_length11)keyboard_test11[--keyboard_test_length11]=0;else if(key>=32&&key<=126&&keyboard_test_length11<31){keyboard_test11[keyboard_test_length11++]=(char)key;keyboard_test11[keyboard_test_length11]=0;}else return 0;render();return 1;}
 if(step!=3||focus>=controls||buttons[focus].action!=30)return 0;
 unsigned n=0;while(preferences.user[n])++n;unsigned shift=!!(input11_modifiers()&2),lo=name_cursor11<name_anchor11?name_cursor11:name_anchor11,hi=name_cursor11>name_anchor11?name_cursor11:name_anchor11;
 if(key==1||((input11_modifiers()&1)&&key=='a')){name_anchor11=0;name_cursor11=n;}
 else if(key==128||key==129||key==130||key==131){if(key==128){if(!shift&&lo!=hi)name_cursor11=lo;else if(name_cursor11)--name_cursor11;}if(key==129){if(!shift&&lo!=hi)name_cursor11=hi;else if(name_cursor11<n)++name_cursor11;}if(key==130)name_cursor11=0;if(key==131)name_cursor11=n;if(!shift)name_anchor11=name_cursor11;}
 else if(key==8||key==127||key==132||((key>='a'&&key<='z')||(key>='A'&&key<='Z')||(key>='0'&&key<='9')||key=='_'||key=='-')){
  if(lo==hi){if(key==8&&lo)--lo;else if((key==127||key==132)&&hi<n)++hi;}
  unsigned add=key!=8&&key!=127&&key!=132;if(n-(hi-lo)+add>31){validation="Use at most 31 letters, numbers, - or _.";render();return 1;}
  for(unsigned i=hi;i<=n;++i)preferences.user[lo+i-hi]=preferences.user[i];n-=hi-lo;name_cursor11=lo;
  if(add){for(unsigned i=n+1;i>lo;--i)preferences.user[i]=preferences.user[i-1];preferences.user[lo]=(char)key;++name_cursor11;}
  name_anchor11=name_cursor11;validation=0;
 }else if(key>=32&&key<=126){validation="Use only letters, numbers, - or _ in this account name.";}else return 0;
 render();return 1;
}
