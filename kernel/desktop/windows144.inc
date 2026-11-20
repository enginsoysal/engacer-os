/* Native compositor bridge: records only, never application code pointers. */
static uint64_t foreign_focus144;
static unsigned foreign_cursor_kind144(uint64_t token,unsigned x,unsigned y){desktop_window*w=desktop_lookup(&model,token);if(!w||!apps[w-model.windows].foreign144||(int)x<=w->bounds.x||(int)x>=w->bounds.x+w->bounds.width-1||(int)y<w->bounds.y+40||(int)y>=w->bounds.y+w->bounds.height-1)return UINT32_MAX;unsigned id=w8_ui_cursor144(apps[w-model.windows].foreign144);return id==0?6:id==32513?1:id==32644?2:id==32645?3:id==32642?4:id==32643?5:0;}
static void foreign_sync144(void){
 /* Release stale native slots before admitting a new original top-level window. */
 for(unsigned i=0;i<DESKTOP_WINDOWS;++i){desktop_window*w=model.windows+i;application*a=apps+i;if(!w->live||!a->foreign144)continue;wui_view144 v;unsigned slot=(unsigned)(a->foreign144&255);
  if(!w8_ui_at144(slot,&v)||(v.handle!=a->foreign144||!v.description.visible)){desktop_rect old=w->bounds;desktop_close(&model,desktop_token(&model,i));memset(a,0,sizeof(*a));invalidate(old);task_damage();}
 }
 for(unsigned i=0;i<WUI_WINDOWS144;++i){wui_view144 v;if(!w8_ui_at144(i,&v)||v.description.parent)continue;unsigned native=DESKTOP_WINDOWS;
  for(unsigned j=0;j<DESKTOP_WINDOWS;++j)if(model.windows[j].live&&apps[j].foreign144==v.handle){native=j;break;}
  if(native==DESKTOP_WINDOWS){if(!v.description.visible)continue;wui_rect144 r=v.description.bounds;uint64_t token=desktop_open(&model,WINDOWS8,(desktop_rect){r.x,r.y,r.width,r.height});if(!token)continue;native=(unsigned)(uint32_t)token-1;memset(apps+native,0,sizeof(application));apps[native].foreign144=v.handle;task_damage();}
  desktop_window*w=model.windows+native;application*a=apps+native;uint64_t token=desktop_token(&model,native);wui_rect144 r=v.description.bounds;
  if(a->foreign_revision144!=v.revision){desktop_rect old=w->bounds;desktop_place(&model,token,(desktop_rect){r.x,r.y,r.width,r.height});desktop_minimize(&model,token,!v.description.visible||(v.description.style&0x20000000)!=0);copy(a->path,v.caption,sizeof(a->path));a->foreign_revision144=v.revision;invalidate(old);invalidate(w->bounds);task_damage();}
  else if(w->bounds.x!=r.x||w->bounds.y!=r.y||w->bounds.width!=r.width||w->bounds.height!=r.height||w->minimized!=((v.description.style&0x20000000)!=0)){
   desktop_rect b=w->bounds;w8_ui_place144(v.handle,(wui_rect144){b.x,b.y,b.width,b.height},1u|(w->minimized?2u:0u));
   if(b.x!=r.x||b.y!=r.y)w8_ui_input144(v.handle,3,0,((uint32_t)b.x&65535)|((uint64_t)((uint32_t)b.y&65535)<<16));
   if(b.width!=r.width||b.height!=r.height||w->minimized!=((v.description.style&0x20000000)!=0))w8_ui_input144(v.handle,5,w->minimized?1:0,(uint32_t)(b.width-2)|((uint64_t)(uint32_t)(b.height-41)<<16));
   if(w8_ui_at144(i,&v))a->foreign_revision144=v.revision;
  }
 }
 uint64_t focus=0;if(model.focused<DESKTOP_WINDOWS&&model.windows[model.focused].live&&!model.windows[model.focused].minimized&&!launcher)focus=apps[model.focused].foreign144;
 if(focus!=foreign_focus144){if(foreign_focus144)w8_ui_input144(foreign_focus144,8,focus,0);if(focus)w8_ui_input144(focus,7,foreign_focus144,0);foreign_focus144=focus;}
#ifdef ENGINE_M13
 if(!dragging&&!launcher){uint64_t token=desktop_hit(&model,(int)pointer_x,(int)pointer_y);unsigned kind=foreign_cursor_kind144(token,pointer_x,pointer_y);if(kind!=UINT32_MAX)graphics9_cursor_kind(kind);}
#endif
}
static unsigned foreign_key144(int key){
 if(launcher||model.focused>=DESKTOP_WINDOWS||!model.windows[model.focused].live||key==137||key==135)return 0;
 uint64_t handle=apps[model.focused].foreign144;if(!handle)return 0;wui_view144 v;if(!w8_ui_at144((unsigned)(handle&255),&v)||!v.description.enabled)return 1;
 if(key==144){w8_ui_input144(handle,0x10,0,0);return 1;}
 if((key>=32&&key<=126)||key==8||key==9||key==10){w8_ui_input144(handle,0x102,key==10?13:(unsigned)key,1);return 1;}
 unsigned vk=key==128?0x25:key==129?0x27:key==133?0x26:key==134?0x28:key==27?0x1b:0;
 if(vk){w8_ui_input144(handle,0x100,vk,1);w8_ui_input144(handle,0x101,vk,UINT64_C(0xc0000001));}return 1;
}
static void foreign_pointer144(unsigned x,unsigned y,unsigned buttons,unsigned previous){
 uint64_t token=desktop_hit(&model,(int)x,(int)y);desktop_window*w=desktop_lookup(&model,token);if(!w||dragging||launcher)return;uint64_t handle=apps[w-model.windows].foreign144;if(!handle||(int)x<=w->bounds.x||(int)x>=w->bounds.x+w->bounds.width-1||(int)y<w->bounds.y+40||(int)y>=w->bounds.y+w->bounds.height-1)return;
 wui_view144 v;if(!w8_ui_at144((unsigned)(handle&255),&v)||!v.description.enabled)return;
 uint64_t lp=((x-(unsigned)(w->bounds.x+1))&65535)|((uint64_t)((y-(unsigned)(w->bounds.y+40))&65535)<<16);unsigned flags=(buttons&1?1:0)|(buttons&2?2:0);
 static uint64_t cursor_owner144;if(cursor_owner144!=handle){cursor_owner144=handle;w8_ui_input144(handle,0x20,handle,0x02000001);}
 w8_ui_input144(handle,0x200,flags,lp);
 if((buttons^previous)&1)w8_ui_input144(handle,buttons&1?0x201:0x202,flags,lp);
 if((buttons^previous)&2)w8_ui_input144(handle,buttons&2?0x204:0x205,flags,lp);
}
