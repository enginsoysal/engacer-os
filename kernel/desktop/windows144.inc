#include <engine/keymap145.h>
/* Native compositor bridge: records only, never application code pointers. */
static uint64_t foreign_focus144;
static desktop_rect foreign_clip144;
static desktop_rect foreign_intersect144(desktop_rect a,desktop_rect b){int left=a.x>b.x?a.x:b.x,top=a.y>b.y?a.y:b.y,right=a.x+a.width<b.x+b.width?a.x+a.width:b.x+b.width,bottom=a.y+a.height<b.y+b.height?a.y+a.height:b.y+b.height;return(desktop_rect){left,top,right>left?right-left:0,bottom>top?bottom-top:0};}
static void foreign_commands145(uint64_t handle,int x,int y,desktop_rect clip,unsigned menu){wui_draw144 draw;
 for(unsigned n=0;menu?w8_ui_menudraw_at145(handle,n,&draw):w8_ui_draw_at144(handle,n,&draw);++n){
  desktop_rect bounded=foreign_intersect144(clip,(desktop_rect){x+draw.clip.x,y+draw.clip.y,draw.clip.width,draw.clip.height});if(!bounded.width||!bounded.height)continue;
  gui7_clip((unsigned)bounded.x,(unsigned)bounded.y,(unsigned)bounded.width,(unsigned)bounded.height);
  if(draw.kind==1)rectangle((desktop_rect){x+draw.bounds.x,y+draw.bounds.y,draw.bounds.width,draw.bounds.height},draw.color);
  else if(draw.kind==2){
#ifdef ENGINE_M14
   text(x+draw.bounds.x,y+draw.bounds.y,draw.text,ui148_font_role((unsigned)draw.bounds.height),draw.color);
#else
   text(x+draw.bounds.x,y+draw.bounds.y,draw.text,1,draw.color);
#endif
  }
  else if(draw.kind==4)ui145_argb_tile(x+draw.bounds.x,y+draw.bounds.y,(unsigned)draw.bounds.width,(unsigned)draw.bounds.height,draw.pixels);
#ifdef ENGINE_M14
  else if(draw.kind==5){uint64_t id;memcpy(&id,draw.text,8);wui_image_view148 image;if(w8_ui_image148(handle,id,&image))ui148_image(x+draw.bounds.x,y+draw.bounds.y,&image);}
#endif
 }
}
/* One bounded traversal stack: legal HWND nesting must not recurse on the kernel stack. */
static void foreign_draw_node144(uint64_t handle,int x,int y,desktop_rect clip){
 typedef struct {uint64_t handle,last_child;int x,y;desktop_rect clip;unsigned phase,painted;} frame144;
 frame144 frames[WUI_DEPTH146];unsigned count=1;frames[0]=(frame144){.handle=handle,.x=x,.y=y,.clip=clip};
 wui_view144 child;
 while(count){frame144*node=frames+count-1;
  if(node->clip.width<=0||node->clip.height<=0){--count;continue;}
  if(!node->painted){node->painted=1;foreign_commands145(node->handle,node->x,node->y,node->clip,0);}
  unsigned descended=0;
  while(node->phase<2){unsigned found=0;wui_view144 candidate;for(unsigned slot=0;slot<WUI_WINDOWS144;++slot){if(!w8_ui_at144(slot,&candidate)||candidate.description.parent!=node->handle||!candidate.description.visible||((candidate.description.exstyle&8)!=0)!=node->phase||candidate.handle<=node->last_child)continue;if(!found||candidate.handle<child.handle){child=candidate;found=1;}}
   if(!found){++node->phase;node->last_child=0;continue;}node->last_child=child.handle;
   wui_rect144 b=child.description.bounds;int border=child.description.style&0x00800000?1:0;
   if(border){desktop_rect outer=foreign_intersect144(node->clip,(desktop_rect){node->x+b.x,node->y+b.y,b.width,b.height});if(outer.width&&outer.height){gui7_clip((unsigned)outer.x,(unsigned)outer.y,(unsigned)outer.width,(unsigned)outer.height);rectangle((desktop_rect){node->x+b.x,node->y+b.y,b.width,b.height},0xa0a0a0);}}
   desktop_rect bounded=foreign_intersect144(node->clip,(desktop_rect){node->x+b.x+border,node->y+b.y+border,b.width-border*2,b.height-border*2});
   if(count<WUI_DEPTH146){frames[count++]=(frame144){.handle=child.handle,.x=node->x+b.x+border,.y=node->y+b.y+border,.clip=bounded};descended=1;break;}
  }
  if(!descended)--count;
 }
}
static void foreign_draw144(const desktop_window*w,uint64_t handle){int menu=(int)w8_ui_menuheight145(handle);if(menu){desktop_rect bar=foreign_intersect144(foreign_clip144,(desktop_rect){w->bounds.x+1,w->bounds.y+40,w->bounds.width-2,menu});foreign_commands145(handle,w->bounds.x+1,w->bounds.y+40,bar,1);}desktop_rect clip=foreign_intersect144(foreign_clip144,(desktop_rect){w->bounds.x+1,w->bounds.y+40+menu,w->bounds.width-2,w->bounds.height-41-menu});foreign_draw_node144(handle,w->bounds.x+1,w->bounds.y+40+menu,clip);}

static unsigned foreign_cursor_kind144(uint64_t token,unsigned x,unsigned y){desktop_window*w=desktop_lookup(&model,token);if(!w||!apps[w-model.windows].foreign144||(int)x<=w->bounds.x||(int)x>=w->bounds.x+w->bounds.width-1||(int)y<w->bounds.y+40||(int)y>=w->bounds.y+w->bounds.height-1)return UINT32_MAX;unsigned id=w8_ui_cursor144(apps[w-model.windows].foreign144);return id==0?6:id==32513?1:id==32644?2:id==32645?3:id==32642?4:id==32643?5:0;}
static __attribute__((noinline)) void foreign_sync144(void){
 static unsigned last_revision;unsigned revision=w8_ui_revision144();if(revision!=last_revision){for(unsigned i=0;i<DESKTOP_WINDOWS;++i)if(model.windows[i].live&&apps[i].foreign144)invalidate(model.windows[i].bounds);last_revision=revision;}
 /* Release stale native slots before admitting a new original top-level window. */
 for(unsigned i=0;i<DESKTOP_WINDOWS;++i){desktop_window*w=model.windows+i;application*a=apps+i;if(!w->live||!a->foreign144)continue;wui_view144 v;unsigned slot=(unsigned)(a->foreign144&255);
  if(!w8_ui_at144(slot,&v)||(v.handle!=a->foreign144||!v.description.visible)){desktop_rect old=w->bounds;desktop_close(&model,desktop_token(&model,i));memset(a,0,sizeof(*a));invalidate(old);task_damage();}
 }
 for(unsigned i=0;i<WUI_WINDOWS144;++i){wui_view144 v;if(!w8_ui_at144(i,&v)||v.description.parent)continue;unsigned native=DESKTOP_WINDOWS;
  for(unsigned j=0;j<DESKTOP_WINDOWS;++j)if(model.windows[j].live&&apps[j].foreign144==v.handle){native=j;break;}
  if(native==DESKTOP_WINDOWS){if(!v.description.visible)continue;wui_rect144 r=v.description.bounds;uint64_t token=desktop_open(&model,WINDOWS8,(desktop_rect){r.x,r.y,r.width,r.height});if(!token)continue;native=(unsigned)(uint32_t)token-1;memset(apps+native,0,sizeof(application));apps[native].foreign144=v.handle;task_damage();}
  desktop_window*w=model.windows+native;application*a=apps+native;uint64_t token=desktop_token(&model,native);wui_rect144 r=v.description.bounds;
  if(a->foreign_revision144!=v.revision){window_state11*state=window_state_for11(token);wui_rect144 normal;if(state&&w8_ui_normal144(v.handle,&normal)){state->normal=(desktop_rect){normal.x,normal.y,normal.width,normal.height};state->mode=((v.description.style&0x01000000u)||((v.description.style&0x20000000u)&&w8_ui_restore_max144(v.handle)))?1u:0u;}desktop_rect old=w->bounds;desktop_place(&model,token,(desktop_rect){r.x,r.y,r.width,r.height});desktop_minimize(&model,token,!v.description.visible||(v.description.style&0x20000000)!=0);copy(a->path,v.caption,sizeof(a->path));a->foreign_revision144=v.revision;invalidate(old);invalidate(w->bounds);task_damage();}
  else if(w->bounds.x!=r.x||w->bounds.y!=r.y||w->bounds.width!=r.width||w->bounds.height!=r.height||w->minimized!=((v.description.style&0x20000000)!=0)){
   desktop_rect b=w->bounds;w8_ui_place144(v.handle,(wui_rect144){b.x,b.y,b.width,b.height},1u|(w->minimized?2u:0u)|(window_state_for11(token)->mode==1?4u:0u));
   if(b.x!=r.x||b.y!=r.y)w8_ui_input144(v.handle,3,0,((uint32_t)b.x&65535)|((uint64_t)((uint32_t)b.y&65535)<<16));
   if(b.width!=r.width||b.height!=r.height||w->minimized!=((v.description.style&0x20000000)!=0))w8_ui_input144(v.handle,5,w->minimized?1:0,(w->minimized?0u:(uint32_t)(b.width-2))|((uint64_t)(w->minimized?0u:(uint32_t)(b.height-41-(int)v.menu_height))<<16));
   if(w8_ui_at144(i,&v))a->foreign_revision144=v.revision;
  }
 }


 for(unsigned pass=0;pass<DESKTOP_WINDOWS;++pass){unsigned changed=0;for(unsigned child=0;child<DESKTOP_WINDOWS;++child){if(!model.windows[child].live||!apps[child].foreign144)continue;wui_view144 view;if(!w8_ui_at144((unsigned)(apps[child].foreign144&255),&view)||!view.description.owner)continue;unsigned owner=DESKTOP_WINDOWS;for(unsigned n=0;n<DESKTOP_WINDOWS;++n)if(model.windows[n].live&&apps[n].foreign144==view.description.owner){owner=n;break;}if(owner==DESKTOP_WINDOWS)continue;unsigned cp=model.count,op=model.count;for(unsigned n=0;n<model.count;++n){if(model.order[n]==child)cp=n;if(model.order[n]==owner)op=n;}if(cp<op){for(unsigned n=cp;n<op;++n)model.order[n]=model.order[n+1];model.order[op]=(uint8_t)child;invalidate(model.windows[child].bounds);invalidate(model.windows[owner].bounds);++model.changes;changed=1;}}if(!changed)break;}
 if(model.focused<DESKTOP_WINDOWS&&window_disabled144(model.windows+model.focused)){uint64_t owner=apps[model.focused].foreign144;for(unsigned n=model.count;n;--n){unsigned slot=model.order[n-1];if(!apps[slot].foreign144||model.windows[slot].minimized||window_disabled144(model.windows+slot))continue;wui_view144 view;if(w8_ui_at144((unsigned)(apps[slot].foreign144&255),&view)&&view.description.owner==owner){desktop_focus(&model,desktop_token(&model,slot));desktop_focus11=0;task_damage();break;}}}
#ifdef ENGINE_M14
 /* Respect native modal surfaces; requests never restore hidden/minimized windows. */
 uint64_t requested=w8_ui_foreground_request148();if(requested&&!launcher&&!context11&&!picker_live12()){for(unsigned i=0;i<DESKTOP_WINDOWS;++i)if(model.windows[i].live&&apps[i].foreign144==requested&&!model.windows[i].minimized&&!window_disabled144(model.windows+i)){desktop_focus(&model,desktop_token(&model,i));desktop_focus11=0;task_damage();whole();break;}}
#endif
 uint64_t focus=0;if(model.focused<DESKTOP_WINDOWS&&model.windows[model.focused].live&&!model.windows[model.focused].minimized&&!launcher)focus=apps[model.focused].foreign144;
 if(focus!=foreign_focus144){if(foreign_focus144)w8_ui_input144(foreign_focus144,8,focus,0);if(focus)w8_ui_input144(focus,7,foreign_focus144,0);foreign_focus144=focus;}
#ifdef ENGINE_M14
 w8_ui_foreground_changed148(desktop_focus11||file_dialog_state11.mode?0:focus);if(focus)w8_ui_modifiers145(focus,input14_snapshot());
#endif
#ifdef ENGINE_M13
 if(!dragging&&!launcher){uint64_t token=desktop_hit(&model,(int)pointer_x,(int)pointer_y);unsigned kind=foreign_cursor_kind144(token,pointer_x,pointer_y);if(kind!=UINT32_MAX&&graphics9_cursor_kind(kind))usb_mouse_draw();}
#endif
}
#ifdef ENGINE_M14
unsigned w8_desktop_foreground_allowed148(uint64_t handle){
 if(launcher||context11||picker_live12()||dragging||file_dialog_state11.mode)return 0;
 if(model.focused>=DESKTOP_WINDOWS||!model.windows[model.focused].live)return 1;
 unsigned slot=model.focused;if(!apps[slot].foreign144)return model.windows[slot].app==WINDOWS8;
 wui_view144 current,target;return w8_ui_at144((unsigned)(apps[slot].foreign144&255),&current)&&w8_ui_at144((unsigned)(handle&255),&target)&&current.process==target.process;
}
#endif
static unsigned foreign_key144(int key){
 if(launcher||model.focused>=DESKTOP_WINDOWS||!model.windows[model.focused].live||key==137||key==135)return 0;
 uint64_t handle=apps[model.focused].foreign144;if(!handle)return 0;wui_view144 v;if(!w8_ui_at144((unsigned)(handle&255),&v)||!v.description.enabled)return 1;
 if(key==144){w8_ui_input144(handle,0x10,0,0);return 1;}
 unsigned character146=0;
#ifdef ENGINE_M14
 character146=input146_key_character();w8_ui_modifiers145(handle,input146_key_snapshot());
#endif
 if((key>=32&&key<=126)||key==8||key==9||key==10||(character146&&key>=1&&key<=26)){unsigned ch=key==10&&!character146?13:(unsigned)key,vk=keymap_character145(character146?character146:ch);unsigned scan=keymap145(vk,4,input10_layout());uint64_t lp=1|((uint64_t)(scan&255)<<16)|(scan&0xff00?UINT64_C(1)<<24:0);w8_ui_input144(handle,0x100,vk,lp);w8_ui_input144(handle,0x102,ch,lp);w8_ui_input144(handle,0x101,vk,lp|UINT64_C(0xc0000000));return 1;}
 unsigned vk=key==128?0x25:key==129?0x27:key==133?0x26:key==134?0x28:key==130?0x24:key==131?0x23:key==132?0x2e:key==27?0x1b:0;
 if(vk){unsigned scan=keymap145(vk,4,input10_layout());uint64_t lp=1|((uint64_t)(scan&255)<<16)|(scan&0xff00?UINT64_C(1)<<24:0);w8_ui_input144(handle,0x100,vk,lp);w8_ui_input144(handle,0x101,vk,lp|UINT64_C(0xc0000000));}return 1;
}
static void foreign_pointer144(unsigned x,unsigned y,unsigned buttons,unsigned previous){
#ifdef ENGINE_M14
 if(picker_live12()&&picker_foreign12())return;
#endif

 uint64_t captured=w8_ui_capture_root144();uint64_t token=desktop_hit(&model,(int)x,(int)y);if(captured)for(unsigned i=0;i<DESKTOP_WINDOWS;++i)if(model.windows[i].live&&apps[i].foreign144==captured){token=desktop_token(&model,i);break;}desktop_window*w=desktop_lookup(&model,token);if(!w||dragging||launcher)return;uint64_t handle=apps[w-model.windows].foreign144;if(!handle||(!captured&&((int)x<=w->bounds.x||(int)x>=w->bounds.x+w->bounds.width-1||(int)y<w->bounds.y+40||(int)y>=w->bounds.y+w->bounds.height-1)))return;
 wui_view144 v;if(!w8_ui_at144((unsigned)(handle&255),&v)||!v.description.enabled)return;
#ifdef ENGINE_M14
 w8_ui_modifiers145(handle,input14_pointer_snapshot());
#endif
 unsigned menu=w8_ui_menuheight145(handle);if(!captured&&(int)y<w->bounds.y+40+(int)menu){if((buttons^previous)&1)w8_ui_input144(handle,buttons&1?0xa1:0xa2,5,(x&65535)|((uint64_t)(y&65535)<<16));return;}
 unsigned modifiers=0;
#ifdef ENGINE_M11
 modifiers=input11_pointer_modifiers();
#endif
 uint64_t lp=((x-(unsigned)(w->bounds.x+1))&65535)|((uint64_t)((y-(unsigned)(w->bounds.y+40+menu))&65535)<<16);unsigned flags=(buttons&1?1:0)|(buttons&2?2:0)|(buttons&4?16:0)|(modifiers&1?8:0)|(modifiers&2?4:0);
 w8_ui_input144(handle,0x20,0,lp);
 w8_ui_input144(handle,0x200,flags,lp);
 if((buttons^previous)&1)w8_ui_input144(handle,buttons&1?0x201:0x202,flags,lp);
 if((buttons^previous)&2)w8_ui_input144(handle,buttons&2?0x204:0x205,flags,lp);
 if((buttons^previous)&4)w8_ui_input144(handle,buttons&4?0x207:0x208,flags,lp);
}
