/* Responsive M12 setup. Existing action IDs and destructive admission stay intact. */
static unsigned compact15(unsigned h){return h<450;}
static unsigned choice15(unsigned selected){
#ifdef ENGINE_M13
 return selected?TAP_SELECTED13:0;
#else
 return selected?1:0;
#endif
}
static uint32_t choice_ink15(ui12_palette p,unsigned selected){
#ifdef ENGINE_M13
 return selected?ui12_foreground(p.selection):p.ink;
#else
 return selected?ui12_foreground(p.accent):p.ink;
#endif
}
static uint32_t border15(ui12_palette p,unsigned index){
#ifdef ENGINE_M13
 return kind75[index]==1||kind75[index]==TAP_SELECTED13?p.accent:p.control_border;
#else
 (void)index;return p.control_border;
#endif
}
static const char*accent_name15(void){return accent==DISTRO_ACCENT?"Default":accent==0x62e5bd?"Mint":accent==0x9caeff?"Lavender":accent==0xf4c47c?"Amber":"Custom";}
static void hint15(unsigned x,unsigned y,unsigned w,unsigned lines,const char*s){ui12_palette p=ui12_theme(0,accent);ui73_paragraph(x,y,w,lines,validation?validation:s,validation?0x994334:p.muted);}
#ifdef ENGINE_M13
static void welcome13(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);unsigned small=compact15(h);
 label(x,y,"Welcome to " ENGINE_PRODUCT_NAME,UI12_HEADING,p.ink);
 ui73_paragraph(x,y+48,w,2,"A personal desktop. A few guided choices. Start with the recommended settings, or make it your own.",p.muted);
 if(!small){
  ui73_round(x,y+108,w,124,UI12_RADIUS,p.selection);unsigned mid=x+w/2;
  ui73_round(mid-120,y+124,240,88,10,p.ink);ui73_round(mid-114,y+130,228,72,6,UI13_SETUP_BACKDROP);
  ui73_round(mid-88,y+146,176,42,5,p.surface);ui73_folder(mid-76,y+156,24,0xf0c87c);
  gui6_rect(mid-42,y+157,108,3,p.line);gui6_rect(mid-42,y+167,78,3,p.line);
  ui73_round(mid-114,y+192,228,10,3,p.paper);gui6_rect(mid-13,y+212,26,8,p.ink);ui73_round(mid-44,y+220,88,4,2,p.ink);
 }
 unsigned first=small?112:252;const char*lines[]={"Works offline. No online account needed.","Your choice of apps and appearance.","A clear review before any disk changes."};
 for(unsigned i=0;i<3;++i){ui73_round(x,y+first+i*32+5,10,10,5,p.accent);ui73_fit(x+22,y+first+i*32,w-22,lines[i],UI12_BODY,p.ink);}
 hint15(x,y+h-(startup_options13?164:108),w,2,"Nothing is erased until you review the disk and choose Install. Next continues setup.");
 if(startup_options13){unsigned half=(w-12)/2;tap75(x,y+h-100,half,44,"Recovery and details",50,0);tap75(x+half+12,y+h-100,half,44,"Open installed system",83,0);}
 tap75(x,y+h-44,240,44,startup_options13?"Hide startup options":"More startup options",50500,0);
}
#endif
static void welcome15(unsigned x,unsigned y,unsigned w,unsigned h){
#ifdef ENGINE_M13
 welcome13(x,y,w,h);return;
#endif
 ui12_palette p=ui12_theme(0,accent);unsigned small=compact15(h);label(x,y,"Let's set up " ENGINE_PRODUCT_NAME ".",UI12_HEADING,p.ink);
 ui73_paragraph(x,y+48,w,2,"Your own desktop. A few clear choices. Everything works offline.",p.muted);
 if(!small)art75(x,y+108,w);
 unsigned first=small?116:256;const char*steps15[]={"1. Choose an installation disk","2. Choose your apps and appearance","3. Review, install and restart"};
 for(unsigned i=0;i<3;++i)label(x,y+first+i*34,steps15[i],UI12_BODY,p.ink);
 hint15(x,y+h-108,w,2,"Nothing is erased until you review the disk and choose Install. Your files on other disks stay separate.");
 unsigned half=(w-12)/2;tap75(x,y+h-44,half,44,"Recovery and details",50,0);tap75(x+half+12,y+h-44,half,44,"Open installed system",83,0);
}
static void keyboard15(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);label(x,y,"Keyboard and display",UI12_HEADING,p.ink);ui73_paragraph(x,y+48,w,2,"Choose your layout and try it below. No online account is needed.",p.muted);
 unsigned half=(w-12)/2;tap75(x,y+104,half,44,"US QWERTY",50000,choice15(!setup11.layout));tap75(x+half+12,y+104,half,44,"US Dvorak",50001,choice15(setup11.layout));
 tap75(x,y+160,w-100,44,keyboard_test11[0]?keyboard_test11:"Click here to try typing",50002,0);tap75(x+w-88,y+160,88,44,"Clear",50003,0);
 if(focus<controls&&buttons[focus].action==50002){unsigned at=ui73_measure(keyboard_test11,UI12_BODY);if(at>w-132)at=w-132;gui6_rect(x+12+at,y+171,2,22,p.ink);}
 label(x,y+224,"Text and control size",UI12_BODY,p.ink);const char*sizes[]={"Auto","100%","150%","200%"};unsigned cell=(w-36)/4;for(unsigned i=0;i<4;++i)tap75(x+i*(cell+12),y+260,cell,44,sizes[i],50010+i,choice15(setup11.scale==(i?i+1:0)));
 hint15(x,y+(compact15(h)?328:344),w,2,"English interface. Clock: UTC. Auto keeps a readable size. Unsupported sizes keep your previous choice.");
}
static void disk15(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);unsigned small=compact15(h),count=storage_count();label(x,y,maintenance?"Choose the system disk":"Choose an installation disk",UI12_HEADING,p.ink);
 ui73_paragraph(x,y+48,w,2,"Click a whole row to select it. Next is available only for a usable disk.",p.muted);
 unsigned panel=y+92,row_height=small?38:53,panel_height=small?184:250;ui73_round(x,panel,w,panel_height,UI12_RADIUS,p.line);ui73_round(x+2,panel+2,w-4,panel_height-4,UI12_RADIUS-2,p.surface);
 label(x+16,panel+8,"DISKS",UI12_SECONDARY,p.muted);label(x+w-112,panel+8,"CAPACITY",UI12_SECONDARY,p.muted);
 if(!count)ui73_paragraph(x+20,panel+52,w-40,3,"No disk is connected. Power off the VM, add a supported hard disk and connect it at power on. Then start again.",0x994334);
 for(unsigned row=0;row<4;++row){unsigned index=disk_page*4+row;if(index>=count)break;const storage_disk*d=storage_get(index);unsigned yy=panel+28+row*row_height,hh=row_height-2;char name[40],size[32];diskname75(index,name);capacity75(d,size);unsigned selected=chosen==index;uint32_t bg=selected?p.selection:p.surface;gui6_rect(x+4,yy,w-8,hh,bg);if(selected)gui6_rect(x+4,yy,4,hh,p.accent);
  if(controls<24){unsigned at=controls++;buttons[at]=(control){x+4,yy,w-8,hh,100+index};title75[at]="";kind75[at]=0;}
  ui73_round(x+16,yy+(hh-16)/2,16,16,8,selected?p.accent:p.control_border);ui73_round(x+19,yy+(hh-16)/2+3,10,10,5,bg);if(selected)ui73_round(x+22,yy+(hh-16)/2+6,4,4,2,p.accent);
  ui73_fit(x+42,yy+(small?2:4),w-164,name,UI12_BODY,suitable75(d)?p.ink:p.muted);label(x+w-112,yy+(small?10:14),size,UI12_BODY,p.ink);
  ui73_fit(x+42,yy+(small?20:28),w-164,suitable75(d)?(selected?(chosen_state75==1?"Selected - ready for setup":chosen_state75==2?"Selected - existing data":"Selected - check connection"):"Supported hard disk"):"Inspection only",UI12_SECONDARY,p.muted);
 }
 unsigned tools=panel+panel_height+12;tap75(x,tools,128,40,"Disk tools...",90,chosen<count?0:2);unsigned next=140;if(count>4){tap75(x+next,tools,56,40,"<",94,disk_page?0:2);tap75(x+next+64,tools,56,40,">",95,(disk_page+1)*4<count?0:2);next+=132;}
 if(!maintenance&&chosen_state75==2)tap75(x+next,tools,w-next,40,replace_selected?"[x] Replace disk":"[ ] Replace disk",91,replace_selected?3:0);
 const char*help=chosen>=count?"Select a disk row to enable Next.":chosen_state75==1?"Ready for whole-disk setup. Review names this disk before writing.":chosen_state75==3?"Inspection only. Installation needs a supported writable disk, 2 GiB to 2 TiB.":chosen_state75==4?"The disk could not be read. Check its connection and try again.":replace_selected?"Review will ask again before erasing this disk. Other disks are kept.":"This disk has existing data. Back it up before choosing Replace disk.";
 hint15(x,y+h-44,w,2,help);
}
static void apps15(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);label(x,y,"Choose your apps",UI12_HEADING,p.ink);ui73_paragraph(x,y+48,w,2,"Desktop, Files, Settings and recovery stay. Other apps can be removed or reinstalled independently.",p.muted);
 unsigned cell=(w-24)/3;tap75(x,y+96,cell,40,"All available",50100,0);tap75(x+cell+12,y+96,cell,40,"Essentials",50101,0);tap75(x+2*(cell+12),y+96,cell,40,"No optional apps",50102,0);
 unsigned row=0,seen=0,total=0;for(unsigned k=1;k<APP74_KINDS;++k){if(!(DISTRO_APPS74_MASK&(1u<<k)))continue;++total;if(seen++<apps_page11*6||row>=6)continue;unsigned xx=x+(row%2)*((w+12)/2),yy=y+152+(row/2)*48,ww=(w-12)/2,selected=!!(setup11.apps&(1u<<k)),at=controls;
  tap75(xx,yy,ww,40,"",50200+k,choice15(selected));if(at<controls)title75[at]=setup_titles11[k];ui12_icon(k,xx+10,yy+8,24,0);ui73_fit(xx+44,yy+9,ww-86,setup_titles11[k],UI12_BODY,choice_ink15(p,selected));uint32_t mark=selected?ui12_foreground(accent):p.control_border;unsigned bx=xx+ww-26,by=yy+13;gui6_rect(bx,by,14,14,
#ifdef ENGINE_M13
 selected?accent:p.control_border
#else
 mark
#endif
 );gui6_rect(bx+2,by+2,10,10,selected?accent:p.surface);if(selected){for(unsigned z=0;z<3;++z)gui6_rect(bx+2+z,by+6+z,2,2,mark);for(unsigned z=0;z<6;++z)gui6_rect(bx+5+z,by+9-z,2,2,mark);}++row;
 }
 tap75(x,y+296,96,36,"Previous",50103,apps_page11?0:2);tap75(x+108,y+296,112,36,"More apps",50104,(apps_page11+1)*6<total?0:2);char count[48];decimal(setup_count11(),count);unsigned at=0;while(count[at])++at;const char*tail=setup_count11()==1?" optional app":" optional apps";while(*tail)count[at++]=*tail++;count[at]=0;ui73_fit(x+232,y+306,w-232,count,UI12_SECONDARY,p.muted);
 tap75(x,y+h-44,w,44,preferences.guide?"[x] Show the first-start guide":"[ ] Show the first-start guide",20,0);
}
static void name15(unsigned x,unsigned y,unsigned w){
 ui12_palette p=ui12_theme(0,accent);tap75(x,y,w,44,preferences.user[0]?preferences.user:"Type your account name",30,0);if(focus>=controls||buttons[focus].action!=30)return;
 unsigned lo=name_cursor11<name_anchor11?name_cursor11:name_anchor11,hi=name_cursor11>name_anchor11?name_cursor11:name_anchor11;char prefix[32];memcpy(prefix,preferences.user,lo);prefix[lo]=0;unsigned a=ui73_measure(prefix,UI12_BODY);memcpy(prefix,preferences.user,hi);prefix[hi]=0;unsigned b=ui73_measure(prefix,UI12_BODY);memcpy(prefix,preferences.user,name_cursor11);prefix[name_cursor11]=0;unsigned caret=ui73_measure(prefix,UI12_BODY),scroll=caret>w-28?caret-(w-28):0;
 gui7_clip(x+2,y+2,w-4,40);gui6_rect(x+2,y+2,w-4,40,p.surface);if(hi>lo)gui6_rect(x+12+a-scroll,y+10,b-a,24,p.selection);gui6_text(x+12-scroll,y+11,preferences.user,UI12_BODY,p.ink);gui6_rect(x+12+caret-scroll,y+10,2,24,p.ink);unsigned parent_y=top+98;gui7_clip(body+12,parent_y,width-276,bottom-parent_y-12);
}
static void style15(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);label(x,y,"Make it yours",UI12_HEADING,p.ink);label(x,y+48,"Local account name",UI12_BODY,p.ink);name15(x,y+76,w);hint15(x,y+128,w,1,"Letters, numbers, - or _. Up to 31 characters. No online account.");
 label(x,y+160,"Accent colour",UI12_BODY,p.ink);unsigned cell=(w-36)/4;const char*names[]={"Default","Mint","Lavender","Amber"};const unsigned colors[]={DISTRO_ACCENT,0x62e5bd,0x9caeff,0xf4c47c};for(unsigned i=0;i<4;++i)tap75(x+i*(cell+12),y+184,cell,44,names[i],i?30+i:50400,choice15(accent==colors[i]&&(!i||accent!=DISTRO_ACCENT)));
 label(x,y+236,"Desktop appearance",UI12_BODY,p.ink);tap75(x,y+260,112,44,"Light",50300,choice15(!setup11.dark));tap75(x+124,y+260,112,44,"Dark",50301,choice15(setup11.dark));
 label(x,y+310,"Wallpaper",UI12_BODY,p.ink);cell=(w-24)/3;const unsigned wallpapers[]={0x142c35,0x182039,0xd7e4e9};const char*wallnames[]={"Ocean","Night","Paper"};for(unsigned i=0;i<3;++i)tap75(x+i*(cell+12),y+336,cell,44,wallnames[i],50310+i,choice15(setup11.wallpaper==wallpapers[i]));
 if(h>=480){ui12_palette desktop=ui12_theme(setup11.dark,accent);ui73_round(x,y+404,w,96,8,setup11.wallpaper);ui73_folder(x+18,y+424,32,0xf0cd82);ui73_round(x+78,y+418,w-96,54,6,desktop.paper);label(x+94,y+434,"Your desktop preview",UI12_BODY,desktop.ink);gui6_rect(x+4,y+476,w-8,20,desktop.surface);gui6_rect(x+12,y+480,62,12,accent);}
}
static void review15(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);label(x,y,maintenance?"Review recovery":"Review your choices",UI12_HEADING,p.ink);ui73_paragraph(x,y+48,w,2,maintenance?"Only the reviewed boot operation changes. Your personal files stay.":"Check the disk and your choices. Installation uses this whole disk.",p.muted);
 char disk[40],size[32],apps[32],style[96];diskname75(chosen,disk);capacity75(storage_get(chosen),size);decimal(setup_count11(),apps);const char*parts[]={setup11.dark?"Dark":"Light",setup11.wallpaper==0x182039?"Night":setup11.wallpaper==0xd7e4e9?"Paper":"Ocean",accent_name15()};unsigned at=0;for(unsigned i=0;i<3;++i){if(i){style[at++]=' ';style[at++]='/';style[at++]=' ';}const char*q=parts[i];while(*q)style[at++]=*q++;}style[at]=0;
 if(maintenance){ui73_round(x,y+96,w,160,8,p.selection);label(x+16,y+112,"Selected disk",UI12_BODY,p.muted);ui73_fit(x+160,y+112,w-176,disk,UI12_BODY,p.ink);label(x+16,y+152,"Operation",UI12_BODY,p.muted);ui73_fit(x+160,y+152,w-176,maintenance==1?"Repair boot files":maintenance==2?"Update boot slot":"Restore previous boot slot",UI12_BODY,p.ink);ui73_paragraph(x+16,y+200,w-32,2,"Your account, apps, files and appearance are kept.",p.ink);hint15(x,y+h-44,w,2,"Review this disk before choosing Apply repair.");return;}
 const char*keys[]={"Install on","Capacity","Account","Keyboard","Optional apps","Appearance","Display size","First-start guide"};const char*values[]={disk,size,preferences.user,setup11.layout?"US Dvorak":"US QWERTY",apps,style,setup11.scale==2?"100%":setup11.scale==3?"150%":setup11.scale==4?"200%":"Automatic",preferences.guide?"Show once":"Off"};
 unsigned extra=ui73_measure(preferences.user,UI12_BODY)>w-160?16:0;ui73_round(x,y+92,w,224+extra,8,p.selection);unsigned yy=y+104;for(unsigned i=0;i<8;++i){label(x+12,yy,keys[i],UI12_BODY,p.muted);if(i==2&&extra)ui73_paragraph(x+148,yy,w-160,2,values[i],p.ink);else ui73_fit(x+148,yy,w-160,values[i],UI12_BODY,p.ink);yy+=26+(i==2?extra:0);}
 if(replace_selected)tap75(x,y+h-44,w,44,replace_consent?"[x] Erase every partition on this disk":"[ ] I agree to erase this entire disk",92,3);else hint15(x,y+h-44,w,2,"Back changes your choices. Install starts real writes to the selected disk.");
}
static void progress15(unsigned x,unsigned y,unsigned w,unsigned h){
#ifdef ENGINE_M13
progress14(x,y,w,h);return;
#endif
ui12_palette p=ui12_theme(0,accent);unsigned bar=y+(compact15(h)?212:260);gui6_rect(x,bar-70,w,138,p.paper);ui73_paragraph(x,bar-64,w,2,stage?stage:"Preparing your installation",p.ink);ui73_round(x,bar,w,14,7,p.line);if(percent)ui73_round(x,bar,w*(percent>100?100:percent)/100,14,7,p.accent);char value[24];decimal(percent,value);unsigned n=0;while(value[n])++n;value[n++]='%';value[n]=0;label(x,bar+28,value,UI12_SECTION,p.ink);}
static void finish15(unsigned x,unsigned y,unsigned w,unsigned h){
#ifdef ENGINE_M13
finish14(x,y,w,h);return;
#endif
ui12_palette p=ui12_theme(0,accent);label(x,y,maintenance?"Recovery complete":"Ready for your desktop",UI12_HEADING,p.ink);ui73_paragraph(x,y+56,w,3,maintenance?"The reviewed boot operation completed. Restart to use your installed system.":"Your choices and system files have been saved and verified. Restart to enter the installed desktop.",p.ink);ui73_folder(x+20,y+140,56,0xf0cd82);label(x+104,y+154,maintenance?"Boot files verified":"Installation verified",UI12_SECTION,p.ink);hint15(x,y+h-100,w,3,"Choose Restart below. Keep the hard disk connected. The matching ISO can stay attached; disconnect only CD/DVD when testing disk-only startup.");}
static void render72(void){
 painting73=1;uint64_t began=counter75();unsigned oldfocus=focus;uint32_t sig=model75()^(maintenance*7919u);gui7_clip_reset();unsigned x=body+12,y=top+98,cw=width-276,ch=bottom>y+12?bottom-y-12:0;ui12_palette p=ui12_theme(0,accent);
 if(width<756||height<560||cw<480||ch<380){controls=0;framed75=0;gui6_rect(0,0,screen->framebuffer_width,screen->framebuffer_height,p.paper);ui73_paragraph(24,36,screen->framebuffer_width-48,3,"Setup needs 800 x 600 or more logical space. Use Auto or 100% size, or choose a larger display.",p.ink);keyboard_page11=1;tap75(24,screen->framebuffer_height-72,180,44,"Use automatic size",50010,1);focus=0;goto done15;}
 if(framed75&&previous_mode75==0&&last_step75==5&&step==5){gui7_clip(x,y,cw,ch);progress15(x,y,cw,ch);signature75=sig;goto done15;}
 if(framed75&&previous_mode75==0&&last_step75==step&&signature75==sig&&previous_count75==controls){if(previous_focus75<controls)outline75(buttons[previous_focus75],border15(p,previous_focus75));if(focus<controls)outline75(buttons[focus],p.ink);++focus_frames75;goto done15;}
 if(!framed75||previous_mode75!=0){gui6_rect(0,0,screen->framebuffer_width,screen->framebuffer_height,
#ifdef ENGINE_M13
 UI13_SETUP_BACKDROP
#else
 0x173340
#endif
 );ui73_shadow(left,top,width,height);ui73_round(left,top,width,height,16,p.paper);ui73_round(left,top,196,height,16,0x102c3b);gui6_rect(left+180,top,16,height,0x102c3b);ui73_fit(left+24,top+28,152,DISTRO_NAME,UI12_SECTION,0xffffff);label(left+24,top+height-52,"Your space.",UI12_BODY,0xb4ced8);label(left+24,top+height-32,"Your system.",UI12_BODY,0xb4ced8);framed75=1;++full_frames75;}
 ++content_frames75;gui6_rect(left+196,top+16,width-212,height-16,p.paper);gui6_rect(left+12,top+70,172,height-130,0x102c3b);label(left+24,top+73,maintenance?"RECOVERY":"SETUP",UI12_SECONDARY,0xa9c7d4);
 unsigned visual=maintenance?(step==1?0:step==4?1:step==5?2:3):setup_visual11(),total=maintenance?4:8;const char*names[]={"Welcome","Keyboard / size","Choose a disk","Your apps","Your style","Review","Installing","Ready"};const char*repair[]={"Choose a disk","Review","Applying","Ready"};unsigned spacing=(height-184)/total;if(spacing>47)spacing=47;for(unsigned i=0;i<total;++i){unsigned yy=top+125+i*spacing;ui73_round(left+12,yy-8,172,38,8,i==visual?0x264e5d:0x102c3b);char n[2]={(char)('1'+i),0};label(left+25,yy,n,UI12_BODY,i<=visual?0x62e5bd:0x7394a5);ui73_fit(left+52,yy,124,maintenance?repair[i]:names[i],UI12_BODY,i==visual?0xffffff:0xb4ced8);}
 char heading[32]="STEP ";decimal(visual+1,heading+5);unsigned n=0;while(heading[n])++n;heading[n++]=' ';heading[n++]='O';heading[n++]='F';heading[n++]=' ';heading[n++]=(char)('0'+total);heading[n]=0;label(x,top+29,heading,UI12_SECONDARY,p.muted);gui6_rect(x,top+65,cw,4,p.line);gui6_rect(x,top+65,cw*(visual+1)/total,4,p.accent);
 controls=0;gui7_clip(x,y,cw,ch);if(step==0){if(keyboard_page11)keyboard15(x,y,cw,ch);else welcome15(x,y,cw,ch);}else if(step==1)disk15(x,y,cw,ch);else if(step==2)apps15(x,y,cw,ch);else if(step==3)style15(x,y,cw,ch);else if(step==4)review15(x,y,cw,ch);else if(step==5){label(x,y,maintenance?"Applying recovery":"Installing your system",UI12_HEADING,p.ink);ui73_paragraph(x,y+56,cw,2,"Keep the VM powered on and the disk connected. Each completed phase is checked.",p.muted);progress15(x,y,cw,ch);}else finish15(x,y,cw,ch);gui7_clip_reset();
 gui6_rect(left+196,bottom-8,width-214,1,p.line);if(step<5){if(step||keyboard_page11)tap75(x,bottom+8,120,48,"Back",1,0);unsigned disabled=step==1&&(chosen>=storage_count()||(!maintenance&&(chosen_state75==3||chosen_state75==4||(chosen_state75==2&&!replace_selected))));if(step==4&&!maintenance&&replace_selected&&!replace_consent)disabled=1;tap75(left+width-242,bottom+8,214,48,step==4?(maintenance?"Apply repair":"Install " ENGINE_PRODUCT_NAME):"Next",2,disabled?2:1);}if(step==6)tap75(left+width-298,bottom+8,270,48,"Restart to " ENGINE_PRODUCT_NAME,84,1);
 static unsigned previous_visual15=UINT32_MAX;if(previous_visual15!=visual+(maintenance?16u:0u)){previous_visual15=visual+(maintenance?16u:0u);focus=0;for(unsigned i=0;i<controls;++i)if(kind75[i]==1)focus=i;}else focus=oldfocus<controls?oldfocus:0;
#ifdef ENGINE_M13
 if(oldfocus<controls&&oldfocus!=focus)outline75(buttons[oldfocus],border15(p,oldfocus));
#endif
 if(focus<controls)outline75(buttons[focus],p.ink);signature75=sig;previous_accent75=accent;last_step75=step;previous_mode75=0;previous_count75=controls;
 done15:previous_focus75=focus;gui7_clip_reset();painting73=0;paint_cycles75=counter75()-began;if(paint_cycles75>longest_frame75)longest_frame75=paint_cycles75;serial_text("M73_VIEW step=");serial_hex(step);serial_text("\nM75_FRAME full=");serial_hex(full_frames75);serial_text(" content=");serial_hex(content_frames75);serial_text(" focus=");serial_hex(focus_frames75);serial_text("\n");
}
