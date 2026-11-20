/* Private GUI capabilities. User callbacks never execute in this broker. */
#include <engine/winqueue144.h>
typedef struct {wui_view144 view;unsigned space,thread,generation;} ui_window144;
_Static_assert(sizeof(ui_window144)<=4096,"Window metadata exceeds one page");
static ui_window144 *ui_windows144[WUI_WINDOWS144];
static wui_queue144 *ui_queues144[SPACES142][THREADS142];
static unsigned ui_generation144,ui_revision144;
static void *ui_page144(void){uint64_t page=page_alloc();if(!page)return 0;memset((void*)(uintptr_t)page,0,4096);++ui_resident144;group_peak142();return(void*)(uintptr_t)page;}
static void ui_free144(void*p){if(p){page_free((uint64_t)(uintptr_t)p);--ui_resident144;}}
static ui_window144 *ui_lookup144(uint64_t handle){unsigned i=(unsigned)(handle&255);if(i>=WUI_WINDOWS144)return 0;ui_window144*w=ui_windows144[i];return w&&w->view.handle==handle?w:0;}
static ui_window144 *ui_owned144(uint64_t handle){ui_window144*w=ui_lookup144(handle);return w&&w->space==active_space142&&w->view.process==input8.process_id?w:0;}
static wui_queue144 *ui_queue144(unsigned space,unsigned thread,unsigned create){if(!ui_queues144[space][thread]&&create)ui_queues144[space][thread]=ui_page144();return ui_queues144[space][thread];}
static unsigned ui_enqueue144(unsigned space,unsigned thread,const wui_message144*m,unsigned native){
 if(space>=SPACES142||!spaces142[space]||thread>=THREADS142)return 0;
 thread142*t=spaces142[space]->threads+thread;if(!t->state||t->state==T142_EXITED||t->exiting)return 0;
 wui_queue144*q=ui_queue144(space,thread,1);if(!q||!wui_push144(q,m,native))return 0;
 if(t->state==T144_GUI&&(q->quit||wui_find144(q,&q->waiting)>=0)){t->state=T142_READY;t->frame.rax=0;}return 1;
}
static void ui_destroy144(uint64_t handle){
 ui_window144*w=ui_lookup144(handle);if(!w)return;
 /* Parent teardown is bounded by the global window quota. Owners are distinct. */
 for(unsigned i=0;i<WUI_WINDOWS144;++i)if(ui_windows144[i]&&(ui_windows144[i]->view.description.parent==handle||ui_windows144[i]->view.description.owner==handle))ui_destroy144(ui_windows144[i]->view.handle);
 for(unsigned i=0;i<THREADS142;++i)if(ui_queues144[w->space][i])wui_purge144(ui_queues144[w->space][i],handle);
 unsigned slot=(unsigned)(handle&255);ui_windows144[slot]=0;ui_free144(w);++ui_revision144;
}
static void ui_thread_release144(unsigned space,unsigned thread){
 for(unsigned i=0;i<WUI_WINDOWS144;++i)if(ui_windows144[i]&&ui_windows144[i]->space==space&&ui_windows144[i]->thread==thread)ui_destroy144(ui_windows144[i]->view.handle);
 ui_free144(ui_queues144[space][thread]);ui_queues144[space][thread]=0;
}
static void ui_release144(void){for(unsigned i=0;i<THREADS142;++i)ui_thread_release144(active_space142,i);}
static unsigned ui_description144(wui_description144*d,uint64_t self){
 if(d->visible>1||d->enabled>1||d->bounds.width<0||d->bounds.height<0||d->bounds.width>16384||d->bounds.height>16384||d->bounds.x< -32768||d->bounds.x>32767||d->bounds.y< -32768||d->bounds.y>32767||d->title[127]||d->class_name[63])return 87;
 if(d->parent&&d->owner)return 87;
 uint64_t relation=d->parent?d->parent:d->owner;unsigned depth=0;
 while(relation){if(relation==self||++depth>WUI_WINDOWS144)return 87;ui_window144*w=ui_owned144(relation);if(!w)return 1400;if(w->thread!=current142)return 50;relation=w->view.description.parent?w->view.description.parent:w->view.description.owner;}
 return 0;
}
static int64_t ui_syscall144(uint64_t op,uint64_t handle,uint64_t pointer,uint64_t argument,uint64_t extra,trap_frame*f){
 if(extra)return -87;
 if(op==WUI_CREATE144||op==WUI_UPDATE144){
  if(argument)return -87;wui_description144 d;if(user8(pointer,&d,sizeof(d),0))return -998;
  unsigned error=ui_description144(&d,op==WUI_UPDATE144?handle:0);if(error)return -(int64_t)error;
  ui_window144*w=0;
  if(op==WUI_CREATE144){if(handle)return -87;if(ui_generation144==UINT32_MAX)return -1816;unsigned slot=0;while(slot<WUI_WINDOWS144&&ui_windows144[slot])++slot;if(slot==WUI_WINDOWS144)return -1816;
   if(!ui_queue144(active_space142,current142,1))return -8;w=ui_page144();if(!w)return -8;
   w->space=active_space142;w->thread=current142;w->generation=++ui_generation144;w->view.handle=WUI_HANDLE144|((uint64_t)w->generation<<8)|slot;w->view.process=input8.process_id;w->view.thread=(uint32_t)thread_token142(current142);ui_windows144[slot]=w;
  }else{w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;}
  unsigned units=0,position=0,bytes=0;while(units<128&&d.title[units])++units;char caption[384];
  while(position<units){uint32_t cp;if(!decode_utf16_143(d.title,units,&position,&cp)||!encode_utf8_143(cp,caption,sizeof(caption)-1,&bytes)){if(op==WUI_CREATE144)ui_destroy144(w->view.handle);return -1113;}}caption[bytes]=0;copy8(w->view.caption,caption,sizeof(w->view.caption));
  w->view.description=d;w->view.revision=++ui_revision144;return (int64_t)w->view.handle;
 }
 if(op==WUI_DESTROY144){ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;if(pointer||argument)return -87;ui_destroy144(handle);return 0;}
 if(op==WUI_QUERY144){ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(argument)return -87;return user8(pointer,&w->view,sizeof(w->view),1)?-998:0;}
 if(op==WUI_QUIT144){if(handle||pointer||argument>UINT32_MAX)return -87;wui_queue144*q=ui_queue144(active_space142,current142,1);if(!q)return -8;q->quit=1;q->quit_code=(uint32_t)argument;return 0;}
 if(op==WUI_POST144||op==WUI_THREAD_POST144){
  if(argument)return -87;wui_message144 m;if(user8(pointer,&m,sizeof(m),0)||m.reserved[0]||m.reserved[1])return -87;
  unsigned thread=current142;
  if(op==WUI_POST144){ui_window144*w=ui_owned144(handle);if(!w)return -1400;thread=w->thread;m.window=handle;}
  else{int slot=thread_slot142(handle);if(slot<0)return -1444;thread=(unsigned)slot;m.window=0;}
  m.time=(uint32_t)(m3_clock_ticks()*10);return ui_enqueue144(active_space142,thread,&m,0)?0:-1816;
 }
 if(op==WUI_PEEK144||op==WUI_WAIT144){
  if(handle||!argument)return -87;wui_filter144 filter;if(user8(argument,&filter,sizeof(filter),0)||filter.reserved||filter.remove>1)return -87;
  if(filter.window&&filter.window!=UINT64_MAX&&!ui_owned144(filter.window))return -1400;
  wui_queue144*q=ui_queue144(active_space142,current142,1);if(!q)return -8;int index=wui_find144(q,&filter);
  if(index>=0){if(op==WUI_WAIT144)return 0;if(user8(pointer,q->items+index,sizeof(wui_message144),1))return -998;if(filter.remove)wui_remove144(q,(unsigned)index);return 1;}
  if(q->quit){if(op==WUI_WAIT144)return 0;wui_message144 quit={.message=0x12,.wparam=q->quit_code};if(user8(pointer,&quit,sizeof(quit),1))return -998;if(filter.remove)q->quit=0;return 1;}
  if(op==WUI_PEEK144)return 0;if(pointer)return -87;
  q->waiting=filter;threads142[current142].state=T144_GUI;context8=*f;context8.rax=0;w8_active=0;w8_escape();
 }
 return -87;
}
unsigned w8_ui_revision144(void){return ui_revision144;}
unsigned w8_ui_at144(unsigned index,wui_view144*out){if(index>=WUI_WINDOWS144||!out||!ui_windows144[index])return 0;*out=ui_windows144[index]->view;return 1;}
unsigned w8_ui_input144(uint64_t handle,unsigned message,uint64_t wp,uint64_t lp){ui_window144*w=ui_lookup144(handle);if(!w)return 0;wui_message144 m={.window=handle,.wparam=wp,.lparam=lp,.message=message,.time=(uint32_t)(m3_clock_ticks()*10)};return ui_enqueue144(w->space,w->thread,&m,1);}
unsigned w8_ui_place144(uint64_t handle,wui_rect144 bounds,unsigned visible){ui_window144*w=ui_lookup144(handle);if(!w||visible>1||bounds.width<0||bounds.height<0||bounds.width>16384||bounds.height>16384)return 0;w->view.description.bounds=bounds;w->view.description.visible=visible;w->view.revision=++ui_revision144;return 1;}
