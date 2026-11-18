/* Shared native control presentation. Existing M11 input remains authoritative. */
static i11_target hover12;
enum {SCROLLBAR12=47000};
typedef struct {uint64_t owner;desktop_rect track;unsigned total,visible,step;} scroll_record12;
static scroll_record12 scroll_records12[DESKTOP_WINDOWS];
static struct {uint64_t owner;unsigned first,total,visible,step;int grab;} scroll_capture12;
static unsigned component_state12(uint64_t window,unsigned action){
 unsigned state=0;
 if(hover12.kind==I11_BUTTON&&hover12.window==window&&hover12.action==action){
  state|=UI12_HOVER;
  if(interaction11.captured==1&&!interaction11.dragged&&interaction11.down.window==window&&interaction11.down.action==action)state|=UI12_PRESSED;
 }
 if(control_active&&focused_control_window==window&&focused_action==action)state|=UI12_FOCUS;
 if(access_flags16&2)state&=~(UI12_HOVER|UI12_PRESSED);
 return state;
}
static void component_button12(uint64_t window,desktop_rect r,const char*label,unsigned action,unsigned primary,unsigned enabled){
 if(enabled)access_capture16(window,action,label,1);
 ui12_palette p=desktop_palette16();
 unsigned state=enabled?component_state12(window,action):UI12_DISABLED;
 ui12_style s=ui12_control_style(p,state,primary);
 unsigned inset=(state&UI12_FOCUS)?3:1;
 ui73_round(r.x,r.y,r.width,r.height,UI12_RADIUS,s.border);
 if(r.width>(int)(2*inset)&&r.height>(int)(2*inset))ui73_round(r.x+inset,r.y+inset,r.width-2*inset,r.height-2*inset,UI12_RADIUS-inset,s.fill);
 ui73_fit(r.x+10,r.y+8+!!(state&UI12_PRESSED),r.width>20?(unsigned)r.width-20:0,label,UI12_BODY,s.ink);
}
static void component_hover12(i11_target next,unsigned buttons){
 /* Captured window movement must not highlight objects behind the old bounds. */
 if(dragging||(interaction11.captured&&interaction11.down.kind==I11_CAPTION))next=(i11_target){0,0,I11_BACKGROUND};
 if(i11_same(next,hover12)&&buttons==previous_buttons)return;
 window_hint_damage12(hover12,next);files_hint_damage12(hover12,next);
 files_name_tip_damage12(next);
 /* The full desktop name lives above the grid, outside the hovered tile. */
 if((!hover12.window&&hover12.action>=F11_DESKTOP_ITEM&&hover12.action<F11_DESKTOP_ITEM+V6_ENTRIES)||(!next.window&&next.action>=F11_DESKTOP_ITEM&&next.action<F11_DESKTOP_ITEM+V6_ENTRIES))invalidate((desktop_rect){30,
#ifdef ENGINE_M13
 (int)model.height-144,
#else
 82,
#endif
 (int)model.width-60,28});
 for(unsigned i=0;i<control_count;++i){control*c=&controls[i];
  unsigned before=(hover12.kind==I11_BUTTON||hover12.kind==I11_ITEM)&&c->window==hover12.window&&c->action==hover12.action;
  unsigned after=(next.kind==I11_BUTTON||next.kind==I11_ITEM)&&c->window==next.window&&c->action==next.action;
  if(before||after)invalidate(c->rect);
 }
 hover12=next;
}
static void component_field12(desktop_rect r,unsigned active){
 ui12_palette p=desktop_palette16();unsigned inset=active?2:1;
 ui73_round(r.x,r.y,r.width,r.height,UI12_RADIUS,active?p.ink:p.control_border);
 if(r.width>(int)(2*inset)&&r.height>(int)(2*inset))ui73_round(r.x+inset,r.y+inset,r.width-2*inset,r.height-2*inset,UI12_RADIUS-inset,p.surface);
}
static void component_scrollbar12(uint64_t owner_id,desktop_rect track,unsigned first,unsigned visible,unsigned total,unsigned step){
 desktop_window*w=desktop_lookup(&model,owner_id);if(!w)return;
 scroll_record12*r=&scroll_records12[w-model.windows];r->owner=0;
 if(track.width<12||track.height<24||!total||visible>=total||!step)return;
 *r=(scroll_record12){owner_id,track,total,visible,step};
 ui12_palette p=desktop_palette16();
 ui73_round(track.x,track.y,track.width,track.height,6,p.surface);
 unsigned size=ui12_scroll_size(track.height,visible,total),offset=ui12_scroll_offset(track.height,visible,total,first);
 uint32_t tint=scroll_capture12.owner==owner_id||((component_state12(owner_id,SCROLLBAR12)&(UI12_HOVER|UI12_FOCUS)))?p.ink:p.control_border;
 ui73_round(track.x+6,track.y+(int)offset,track.width-12,size,4,tint);
 if(control_count<DESKTOP_CONTROLS)controls[control_count++]=(control){track,owner_id,SCROLLBAR12};
}
static void component_scroll_set12(scroll_record12*r,unsigned first){
 desktop_window*w=desktop_lookup(&model,r->owner);if(!w||w->app!=FILES||r->visible>=r->total)return;
 unsigned maximum=r->total-r->visible;if(first>maximum)first=maximum;
 apps[w-model.windows].offset=first*r->step;invalidate(w->bounds);
}
static void component_scroll_cancel12(void){
 desktop_window*w=desktop_lookup(&model,scroll_capture12.owner);
 if(w){scroll_record12*r=&scroll_records12[w-model.windows];if(r->owner==scroll_capture12.owner)component_scroll_set12(r,scroll_capture12.first);}
 scroll_capture12.owner=0;i11_cancel(&interaction11);serial_text("M12_SCROLL_CANCEL\n");
}
static unsigned component_scroll_key12(int key){
 if(scroll_capture12.owner){if(key==27||key==137||key==141)component_scroll_cancel12();return 1;}
 if(!control_active||focused_action!=SCROLLBAR12||input11_modifiers()||launcher||context11||guide_open11||file_dialog_state11.mode)return 0;
 desktop_window*w=desktop_lookup(&model,focused_control_window);if(!w)return 0;
 unsigned slot=(unsigned)(w-model.windows);
 if(w->app!=FILES||w->minimized||model.focused!=slot||desktop_focus11||apps[slot].usb_mode10||file_windows11[slot].address_active)return 0;
 scroll_record12*r=&scroll_records12[w-model.windows];if(r->owner!=focused_control_window)return 0;
 unsigned first=apps[w-model.windows].offset/r->step;
 if(key==133){if(first)--first;}else if(key==134)++first;else if(key==130)first=0;else if(key==131)first=r->total;else return key==10;
 component_scroll_set12(r,first);return 1;
}
static unsigned component_scroll_pointer12(i11_target hit,int y,unsigned buttons){
 if(scroll_capture12.owner){
  desktop_window*w=desktop_lookup(&model,scroll_capture12.owner);
  if(!w){scroll_capture12.owner=0;return 1;}
  scroll_record12*r=&scroll_records12[w-model.windows];
  if((buttons&2)||r->owner!=scroll_capture12.owner||r->total!=scroll_capture12.total||r->visible!=scroll_capture12.visible||r->step!=scroll_capture12.step){component_scroll_cancel12();return 1;}
  int position=y-r->track.y-scroll_capture12.grab;if(position<0)position=0;
  component_scroll_set12(r,ui12_scroll_value(r->track.height,r->visible,r->total,(unsigned)position));
  if(!(buttons&1)){scroll_capture12.owner=0;serial_text("M12_SCROLL_END\n");}
  return 1;
 }
 if(!(buttons&1)||(previous_buttons&1)||(buttons&2)||hit.action!=SCROLLBAR12||hit.kind!=I11_BUTTON)return 0;
 desktop_window*w=desktop_lookup(&model,hit.window);if(!w||w->app!=FILES)return 0;
 scroll_record12*r=&scroll_records12[w-model.windows];if(r->owner!=hit.window)return 0;
 desktop_focus(&model,hit.window);desktop_focus11=0;control_active=1;focused_control_window=hit.window;focused_action=SCROLLBAR12;
 unsigned first=apps[w-model.windows].offset/r->step;
 unsigned offset=ui12_scroll_offset(r->track.height,r->visible,r->total,first),size=ui12_scroll_size(r->track.height,r->visible,r->total);
 int at=y-r->track.y;
 if(at<(int)offset)component_scroll_set12(r,first>r->visible?first-r->visible:0);
 else if(at>=(int)(offset+size))component_scroll_set12(r,first+r->visible);
 else{scroll_capture12.owner=hit.window;scroll_capture12.first=first;scroll_capture12.total=r->total;scroll_capture12.visible=r->visible;scroll_capture12.step=r->step;scroll_capture12.grab=at-(int)offset;invalidate(w->bounds);serial_text("M12_SCROLL_BEGIN\n");}
 i11_cancel(&interaction11);return 1;
}
