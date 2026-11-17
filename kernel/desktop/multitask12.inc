/* Shared eight-token overlay; no thumbnails, worker or retained pixel buffers. */
static uint64_t arrange_owner12;
static unsigned arrange_side12;
_Static_assert(sizeof(arrange_owner12)+sizeof(arrange_side12)<=16,"bounded arrangement identity");
static void multitask_label12(uint64_t token,char *label,unsigned capacity){
 desktop_window*w=desktop_lookup(&model,token);if(!w){copy(label,"Window closed",capacity);return;}
 unsigned slot=(unsigned)(w-model.windows);char number[24];decimal(number,slot+1);copy(label,number,capacity);append(label,". ",capacity);
 if(w->minimized)append(label,"[min] ",capacity);if(w->app==EDITOR&&apps[slot].view.dirty)append(label,"[unsaved] ",capacity);
 if(w->app==FILES&&apps[slot].usb_mode10)files_title12(&apps[slot],label+length(label),capacity-length(label));
 else append(label,(w->app==FILES||w->app==EDITOR)&&apps[slot].path[0]?file_basename11(apps[slot].path):titles[w->app],capacity);
}
static void multitask_cancel12(void){switch_open11=switch_count11=switch_choice11=0;arrange_owner12=0;control_active=0;whole();}
static void multitask_arrange12(uint64_t token){
 desktop_window*w=desktop_lookup(&model,token);if(!w||file_block_owner11(token))return;
 arrange_owner12=token;arrange_side12=0;switch_open11=2;switch_count11=4;switch_choice11=window_snap_allowed11(w)?0:2;launcher=context11=0;control_active=0;whole();
}
static void multitask_snap12(uint64_t token,unsigned mode){
 window_mode11(token,mode);desktop_window*w=desktop_lookup(&model,token);window_state11*s=window_state_for11(token);
 if(!w||!s||s->mode!=mode||mode<2)return;
 arrange_owner12=token;arrange_side12=mode==2?3:2;switch_count11=switch_choice11=0;
 for(unsigned i=model.count;i;--i){unsigned slot=model.order[i-1];uint64_t other=desktop_token(&model,slot);desktop_window*next=&model.windows[slot];
  if(other!=token&&!file_block_owner11(other)&&window_snap_allowed11(next))switch_tokens11[switch_count11++]=other;
 }
 if(switch_count11){switch_open11=3;launcher=context11=0;control_active=0;whole();}else arrange_owner12=0;
}
static unsigned multitask_choose12(unsigned index){
 if(switch_open11<2)return 0;
 if(switch_open11==2){uint64_t token=arrange_owner12;desktop_window*w=desktop_lookup(&model,token);
  if(index>=3){multitask_cancel12();return 1;}
  if(!w||file_block_owner11(token)){multitask_cancel12();return 1;}
  if(index<2&&!window_snap_allowed11(w)){copy(shell_notice,"This app needs more room. Maximize it or use a wider desktop.",96);whole();return 1;}
  multitask_cancel12();multitask_snap12(token,index==0?2:index==1?3:1);return 1;
 }
 uint64_t owner=arrange_owner12,other=index<switch_count11?switch_tokens11[index]:0;unsigned side=arrange_side12;multitask_cancel12();
 if(desktop_lookup(&model,owner)&&desktop_lookup(&model,other)&&!file_block_owner11(other))window_mode11(other,side);return 1;
}
static unsigned multitask_key12(int key){
 if(switch_open11<2)return 0;
 if(key==135||key==143){multitask_cancel12();return 0;}
 if(key==27||key==141){multitask_cancel12();return 1;}
 unsigned count=switch_open11==2?4:switch_count11+1;
 if(key==10||key==32){multitask_choose12(switch_choice11);return 1;}
 if(key==9||key==129||key==134){switch_choice11=(switch_choice11+1)%count;whole();}
 else if(key==136||key==128||key==133){switch_choice11=(switch_choice11+count-1)%count;whole();}
 return 1;
}
static void multitask_preview12(desktop_rect bounds){
 int edge=3;uint32_t color=preferences.accent;
 rectangle((desktop_rect){bounds.x+6,bounds.y+6,bounds.width-12,edge},color);
 rectangle((desktop_rect){bounds.x+6,bounds.y+bounds.height-9,bounds.width-12,edge},color);
 rectangle((desktop_rect){bounds.x+6,bounds.y+6,edge,bounds.height-12},color);
 rectangle((desktop_rect){bounds.x+bounds.width-9,bounds.y+6,edge,bounds.height-12},color);
}
static void multitask_overlay12(void){
 unsigned mode=switch_open11,count=mode==2?4:switch_count11+(mode==3);
 if(!mode)return;
 if(mode>=2&&!desktop_lookup(&model,arrange_owner12)){multitask_cancel12();return;}
 if(mode==2&&switch_choice11<3){desktop_window*w=desktop_lookup(&model,arrange_owner12);if(switch_choice11==2||window_snap_allowed11(w)){
  int width=model.width,height=model.height-60;unsigned choice=switch_choice11;
  multitask_preview12((desktop_rect){choice==1?width/2:0,0,choice==2?width:choice==0?width/2:width-width/2,height});
 }}
 int width=model.width<680?(int)model.width-32:640,height=108+(int)count*48,x=((int)model.width-width)/2,y=((int)model.height-60-height)/2;
 ui12_palette palette=ui12_theme(preferences.dark,preferences.accent);ui73_shadow(x,y,width,height);ui73_round(x,y,width,height,12,paper());
 ui73_fit(x+20,y+18,width-40,mode==1?"Switch windows":mode==2?"Arrange this window":"Choose a window for the other side",UI12_SECTION,palette.ink);
 for(unsigned i=0;i<count;++i){int top=y+60+(int)i*48;char label[160];unsigned icon=0,enabled=1;
  if(mode==2){const char*names[]={"Left half","Right half","Maximize","Cancel"};copy(label,names[i],sizeof(label));desktop_window*w=desktop_lookup(&model,arrange_owner12);enabled=i>=2||window_snap_allowed11(w);icon=i==0?ICON12_BACK:i==1?ICON12_FORWARD:i==2?ICON12_MAXIMIZE:ICON12_CLOSE;}
  else if(mode==3&&i==switch_count11){copy(label,"Keep the other side unchanged",sizeof(label));icon=ICON12_CLOSE;}
  else{desktop_window*w=desktop_lookup(&model,switch_tokens11[i]);multitask_label12(switch_tokens11[i],label,sizeof(label));enabled=w!=0;icon=w?w->app:0;}
  if(enabled)button(0,x+16,top,width-32,"",W11_SWITCH+i,i==switch_choice11);
  else component_button12(0,(desktop_rect){x+16,top,width-32,36},"",0,i==switch_choice11,0);
  unsigned state=enabled?component_state12(0,W11_SWITCH+i):UI12_DISABLED;ui12_style style=ui12_control_style(palette,state,i==switch_choice11);
  if(mode==2||(mode==3&&i==switch_count11))ui12_icon_ink(icon,x+26,top+6,24,style.ink);else ui12_icon(icon,x+26,top+6,24,preferences.dark);
  ui73_fit(x+64,top+9+!!(state&UI12_PRESSED),width-96,label,UI12_BODY,style.ink);
 }
 const char*hint=mode==1?"Alt+Tab switches. Arrows choose. Enter opens. Escape cancels.":mode==2?"Preview only. Choose a layout or Cancel; your work is kept.":"Choose another window, or Escape to keep this layout.";
 if(mode==2&&switch_choice11<2&&!window_snap_allowed11(desktop_lookup(&model,arrange_owner12)))hint="This app needs more room. Choose Maximize or Cancel.";
 ui73_fit(x+20,y+height-28,width-40,hint,UI12_SECONDARY,palette.muted);
}
