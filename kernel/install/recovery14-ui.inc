/* M13.4 uses the existing compositor for real progress, result and recovery. */
static unsigned framed14,width14,height14,accent14,kind14;
static unsigned frame14(unsigned kind){
 ui12_palette p=ui12_theme(0,accent);unsigned fresh=!framed14||width14!=width||height14!=height||accent14!=accent||kind14!=kind;
 if(fresh){
  gui7_clip_reset();gui6_rect(0,0,screen->framebuffer_width,screen->framebuffer_height,UI13_SETUP_BACKDROP);ui73_shadow(left,top,width,height);ui73_round(left,top,width,height,16,p.paper);
  ui73_round(left,top,196,height,16,UI13_SETUP_BACKDROP);gui6_rect(left+180,top,16,height,UI13_SETUP_BACKDROP);ui73_fit(left+24,top+28,152,DISTRO_NAME,UI12_SECTION,0xffffff);
  label(left+24,top+76,"RECOVERY",UI12_SECONDARY,0xb4ced8);ui73_paragraph(left+24,top+132,148,4,"Read the result. Choose what to do next.",0xffffff);ui73_paragraph(left+24,top+height-90,148,3,"Keep the matching ISO for recovery.",0xb4ced8);
  framed14=1;width14=width;height14=height;accent14=accent;kind14=kind;
 }
 gui6_rect(left+196,top+16,width-212,height-32,p.paper);label(body+12,top+29,"SETUP / RECOVERY",UI12_SECONDARY,p.muted);gui6_rect(body+12,top+65,width-276,2,p.line);return fresh;
}
static void recovery14(void){
 unsigned bad=failure&&!diagnostics,fresh=frame14(bad?1:2),old=focus,x=body+12,y=top+98,w=width-276,h=bottom-y-12;ui12_palette p=ui12_theme(0,accent);
 if(bad){
  ui12_icon(ICON12_WARNING,x,y,32,0);label(x+44,y,"Could not finish",UI12_HEADING,p.ink);ui73_paragraph(x,y+64,w,3,failure,0x994334);
  ui73_paragraph(x,y+172,w,3,!m6_live()?"Recovery needs the matching ISO. Attach it to the VM before restarting; the installed workspace is unavailable.":step==6?"Your installation was verified, but restarting did not complete. Keep the hard disk connected and try restarting the VM.":"This operation is not marked successful. Some disk changes may have been written. Keep the ISO connected for recovery.",p.ink);
  unsigned cell=(w-12)/2;u13_button(x,y+h-64,cell,!m6_live()||step==6?"Restart the VM":"Choose a disk",!m6_live()||step==6?86:63,1,1,0);u13_button(x+cell+12,y+h-64,cell,"Details and recovery",50,1,0,0);
 }else{
  label(x,y,"Recovery and details",UI12_HEADING,p.ink);ui73_paragraph(x,y+52,w,2,m6_live()?"Select an operation, then review its exact disk before applying. Your existing files stay separate from boot repair.":"Attach the matching recovery ISO and restart. Boot repair is unavailable from this installed workspace.",p.muted);
  const char*result=notice?notice:failure; if(result)ui73_paragraph(x,y+112,w,3,result,0x994334);
  else ui73_paragraph(x,y+112,w,3,"Use the matching ISO for this build. Repair restores checked boot files; update and rollback operate on verified boot slots.",p.ink);
  if(h>=450){u13_number(x,y+218,pages_stats().current_pages*4," KiB managed RAM",p.muted);u13_number(x+w/2,y+218,pages_stats().peak_pages*4," KiB peak",p.muted);ui73_fit(x,y+250,w,BUILD_ID,UI12_SECONDARY,p.muted);}
  unsigned cell=(w-12)/2,first=y+h-148;if(!installed&&m6_live()){u13_button(x,first,cell,"Repair boot files",80,1,0,0);u13_button(x+cell+12,first,cell,"Update boot slot",81,1,0,0);u13_button(x,first+52,cell,"Roll back boot slot",82,1,0,0);}
  u13_button(x+cell+12,first+52,cell,"Advanced terminal",64,1,0,0);u13_button(x,bottom+24,180,"Return",62,1,1,0);
 }
 focus=fresh?(bad?0:controls-1):(old<controls?old:0);if(focus<controls)u13_outline(buttons[focus],p.ink);
}
static void progress14(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);unsigned bar=y+(h<450?240:280),shown=percent>100?100:percent;gui6_rect(x,y+104,w,h-104,p.paper);
 label(x,bar-132,"Current operation",UI12_SECONDARY,p.muted);ui73_paragraph(x,bar-106,w,3,stage?stage:"Preparing your installation",p.ink);
 ui73_round(x,bar,w,12,6,p.line);if(shown)ui73_round(x,bar,w*shown/100,12,6,p.accent);char value[32];decimal(shown,value);unsigned n=0;while(value[n])++n;memcpy(value+n,"% checked",10);label(x,bar+26,value,UI12_SECTION,p.ink);
 ui73_paragraph(x,y+h-58,w,2,"Progress follows verified installation work. It is not a time estimate.",p.muted);
}
static void finish14(unsigned x,unsigned y,unsigned w,unsigned h){
 ui12_palette p=ui12_theme(0,accent);label(x,y,maintenance?"Recovery complete":"Ready for your desktop",UI12_HEADING,p.ink);
 ui73_paragraph(x,y+56,w,2,maintenance?"The reviewed boot operation passed verification. Restart to use your installed system.":"Engacer OS is installed. Your system files and choices passed verification.",p.ink);
 unsigned card=y+(h<450?112:128);ui73_round(x,card,w,104,UI12_RADIUS,p.selection);ui12_icon(ICON12_CHECK,x+16,card+24,48,0);label(x+88,card+20,maintenance?"Boot files verified":"Installation verified",UI12_SECTION,p.ink);ui73_fit(x+88,card+56,w-104,preferences.user,UI12_BODY,p.ink);
 if(h>=450)label(x,y+270,preferences.guide?"First-start tips are ready for you.":"Your desktop will open without first-start tips.",UI12_BODY,p.muted);
 ui73_paragraph(x,y+h-(h<450?130:114),w,3,"Restart below opens your installed desktop. Keep the hard disk connected. The matching ISO may remain connected; disconnect only CD/DVD for disk-only testing.",p.muted);
}
