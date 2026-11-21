/* Private GUI capabilities. User callbacks never execute in this broker. */
#include <engine/winqueue144.h>
#include "keys145.inc"
extern unsigned desktop_native_windows144(void);
typedef struct ui_draw_page144 {struct ui_draw_page144*next;wui_draw144 items[7];} ui_draw_page144;
_Static_assert(sizeof(ui_draw_page144)<=4096,"Draw page quota");
static unsigned ui_draw_pages144;
#ifdef ENGINE_M14
typedef struct ui_image148 ui_image148;
#endif
typedef struct {wui_view144 view;unsigned space,thread,generation,draw_count,draw_capacity;ui_draw_page144*draws;wui_rect144 normal_bounds;unsigned restore_max,menu_count,menu_capacity;ui_draw_page144*menu_draws;
#ifdef ENGINE_M14
 ui_image148*images148;unsigned image_count148;
#endif
} ui_window144;
_Static_assert(sizeof(ui_window144)<=4096,"Window metadata exceeds one page");
static ui_window144 *ui_windows144[WUI_WINDOWS144];
#ifdef ENGINE_M14
static uint64_t ui_foreground148,ui_foreground_pending148;
#endif
static wui_queue144 *ui_queues144[SPACES142][THREADS142];
static unsigned ui_generation144,ui_revision144;
static uint64_t ui_focus144[SPACES142],ui_capture144[SPACES142],ui_capture_owner144;
static void ui_timer_release144(unsigned,unsigned,uint64_t);
#ifdef ENGINE_M14
static void clip_owner_destroy146(uint64_t);
static void clip_thread_release146(unsigned,unsigned);
static void picker_owner_destroy146(uint64_t);
static void picker_thread_release146(unsigned,unsigned);
static void ui_images_release148(ui_window144*);
#endif
static unsigned ui_cursors144[SPACES142]={32512,32512,32512,32512};
#ifdef ENGINE_M73
#include <engine/ui/graphics73.h>
#endif
static void *ui_page144(void){uint64_t page=page_alloc();if(!page)return 0;memset((void*)(uintptr_t)page,0,4096);++ui_resident144;group_peak142();return(void*)(uintptr_t)page;}
static void ui_free144(void*p){if(p){page_free((uint64_t)(uintptr_t)p);--ui_resident144;}}
static ui_window144 *ui_lookup144(uint64_t handle){unsigned i=(unsigned)(handle&255);if(i>=WUI_WINDOWS144)return 0;ui_window144*w=ui_windows144[i];return w&&w->view.handle==handle?w:0;}
static ui_window144 *ui_owned144(uint64_t handle){ui_window144*w=ui_lookup144(handle);return w&&w->space==active_space142&&w->view.process==input8.process_id?w:0;}
static int ui_find144(const wui_queue144*q,const wui_filter144*f){
 for(unsigned i=0;i<q->count;++i){const wui_message144*m=q->items+i;if(wui_matches144(m,f))return (int)i;
  if(!f->window||f->window==UINT64_MAX||!m->window)continue;wui_filter144 range=*f;range.window=0;if(!wui_matches144(m,&range))continue;
  uint64_t child=m->window;for(unsigned depth=0;child&&depth<WUI_WINDOWS144;++depth){ui_window144*w=ui_lookup144(child);if(!w)break;child=w->view.description.parent;if(child==f->window)return (int)i;}
 }return -1;
}
static wui_queue144 *ui_queue144(unsigned space,unsigned thread,unsigned create){if(!ui_queues144[space][thread]&&create){ui_queues144[space][thread]=ui_page144();if(ui_queues144[space][thread])ui_keys_initialize145(ui_queues144[space][thread]);}return ui_queues144[space][thread];}
static unsigned ui_enqueue144(unsigned space,unsigned thread,const wui_message144*m,unsigned native){
 if(space>=SPACES142||!spaces142[space]||thread>=THREADS142)return 0;
 thread142*t=spaces142[space]->threads+thread;if(!t->state||t->state==T142_EXITED||t->exiting)return 0;
 wui_queue144*q=ui_queue144(space,thread,1);if(!q||!wui_push144(q,m,native))return 0;
 #ifdef ENGINE_M14
 unsigned category=8u|256u;if(m->message==0x312)category|=128u;if(native){if(m->message>=0x100&&m->message<=0x109)category=1;else if(m->message==0x200)category=2;else if(m->message>=0x201&&m->message<=0x20e)category=4;}q->new_input148|=category;
#endif
 if(t->state==T144_GUI&&(q->quit||ui_find144(q,&q->waiting)>=0)){t->state=T142_READY;t->frame.rax=0;}return 1;
}
static void ui_destroy144(uint64_t handle){
 ui_window144*w=ui_lookup144(handle);if(!w)return;
#ifdef ENGINE_M14
 clip_owner_destroy146(handle);picker_owner_destroy146(handle);ui_images_release148(w);
 if(ui_foreground148==handle)ui_foreground148=0;if(ui_foreground_pending148==handle)ui_foreground_pending148=0;
#endif
 /* Parent teardown is bounded by the global window quota. Owners are distinct. */
 for(unsigned i=0;i<WUI_WINDOWS144;++i)if(ui_windows144[i]&&(ui_windows144[i]->view.description.parent==handle||ui_windows144[i]->view.description.owner==handle))ui_destroy144(ui_windows144[i]->view.handle);
 for(unsigned i=0;i<THREADS142;++i)if(ui_queues144[w->space][i])wui_purge144(ui_queues144[w->space][i],handle);
 for(unsigned surface=0;surface<2;++surface){ui_draw_page144*draw=surface?w->menu_draws:w->draws;while(draw){ui_draw_page144*next=draw->next;ui_free144(draw);--ui_draw_pages144;draw=next;}}
 if(ui_focus144[w->space]==handle)ui_focus144[w->space]=0;if(ui_capture144[w->space]==handle)ui_capture144[w->space]=0;if(ui_capture_owner144==handle)ui_capture_owner144=0;ui_timer_release144(w->space,w->thread,handle);unsigned slot=(unsigned)(handle&255);ui_windows144[slot]=0;ui_free144(w);++ui_revision144;
}
static void ui_thread_release144(unsigned space,unsigned thread){
#ifdef ENGINE_M14
 clip_thread_release146(space,thread);picker_thread_release146(space,thread);
#endif
 for(unsigned i=0;i<WUI_WINDOWS144;++i)if(ui_windows144[i]&&ui_windows144[i]->space==space&&ui_windows144[i]->thread==thread)ui_destroy144(ui_windows144[i]->view.handle);
 ui_timer_release144(space,thread,0);ui_free144(ui_queues144[space][thread]);ui_queues144[space][thread]=0;
}
static void ui_release144(void){ui_cursors144[active_space142]=32512;for(unsigned i=0;i<THREADS142;++i)ui_thread_release144(active_space142,i);}
static unsigned ui_description144(wui_description144*d,uint64_t self){
 if(d->visible>1||d->enabled>1||d->bounds.width<0||d->bounds.height<0||d->bounds.width>16384||d->bounds.height>16384||d->bounds.x< -32768||d->bounds.x>32767||d->bounds.y< -32768||d->bounds.y>32767||d->title[127]||d->class_name[63])return 87;
 if(d->parent&&d->owner)return 87;
 uint64_t relation=d->parent?d->parent:d->owner;unsigned depth=0;
 while(relation){if(relation==self)return 87;if(++depth>=WUI_DEPTH146)return 1816;ui_window144*w=ui_owned144(relation);if(!w)return 1400;if(w->thread!=current142)return 50;relation=w->view.description.parent?w->view.description.parent:w->view.description.owner;}
 return 0;
}
#include "clipboard144.inc"
#ifdef ENGINE_M14
#include "clipboard146.inc"
#endif
#include "drawing144.inc"
#ifdef ENGINE_M14
#include "image148.inc"
#endif
#include "timers144.inc"
#ifdef ENGINE_M14
#include "message-wait148.inc"
#endif
#include "focus144.inc"
#ifdef ENGINE_M14
#include "foreground148.inc"
#endif
#ifdef ENGINE_M14
#include "picker146.inc"
#include "atom147.inc"
#endif
static int64_t ui_syscall144(uint64_t op,uint64_t handle,uint64_t pointer,uint64_t argument,uint64_t extra,trap_frame*f){
 if(extra)return -87;
#ifdef ENGINE_M14
 if(op==WUI_ATOM147)return atom_call147(handle,pointer,argument);
 if(op==WUI_MESSAGE148)return handle||argument?-87:message_call148(pointer);
 if(op==WUI_IMAGE148)return argument?-87:ui_image_call148(handle,pointer);
 if(op==WUI_FOREGROUND148){if(pointer||argument>1)return -87;if(argument)return handle?-87:(int64_t)ui_foreground148;ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;if(w->view.description.parent||!w->view.description.visible||!ui_enabled_chain144(w)||(w->view.description.style&0x20000000u))return -5;ui_window144*old=ui_lookup144(ui_foreground148);if(old&&old->space!=active_space142)return -5;if(!w8_desktop_foreground_allowed148(handle))return -5;__atomic_store_n(&ui_foreground_pending148,handle,__ATOMIC_RELEASE);++ui_revision144;return 1;}
 if(op==WUI_FONT148){ui_font_metrics148 info;if(argument||handle>UINT32_MAX||!ui148_font_info((unsigned)handle,&info))return -87;return user8(pointer,&info,sizeof(info),1)?-998:0;}
 if(op==WUI_CLIPBOARD146)return clip_call146(handle,pointer,argument);
 if(op==WUI_PICKER146)return picker_call146(handle,pointer,argument,f);
#endif
 if(op==WUI_NORMAL144){ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(argument==2)return pointer?-87:(int64_t)w->restore_max;if(argument==3){if(pointer>1||w->thread!=current142)return -87;w->restore_max=(unsigned)pointer;return 0;}if(argument>1)return -87;if(!argument)return user8(pointer,&w->normal_bounds,sizeof(w->normal_bounds),1)?-998:0;if(w->thread!=current142)return -5;wui_description144 d=w->view.description;if(user8(pointer,&d.bounds,sizeof(d.bounds),0))return -998;unsigned error=ui_description144(&d,handle);if(error)return -(int64_t)error;w->normal_bounds=d.bounds;return 0;}
 if(op==WUI_FOCUS144||op==WUI_CAPTURE144)return pointer?-87:ui_focus_call144(op,handle,argument);
 if(op==WUI_TIMER144)return argument?-87:ui_timer_set144(handle,pointer);
 if(op==WUI_DRAW144||op==WUI_MEASURE144||op==WUI_MENUDRAW145)return ui_draw_call144(op,handle,pointer,argument);
 if(op==WUI_MENUBAR145){ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;if(pointer||w->view.description.parent||(argument&&argument!=24))return -87;w->view.menu_height=(unsigned)argument;if(!argument)w->menu_count=0;w->view.revision=++ui_revision144;return 0;}
 if(op==WUI_KEYSTATE145){
#ifdef ENGINE_M14
  if(argument==2)return handle||pointer?-87:(int64_t)input10_layout();if(argument>1||(!argument&&(pointer||handle>255))||(argument&&(handle||!pointer)))return -87;wui_queue144*q=ui_queue144(active_space142,current142,1);if(!q)return -8;if(!argument)return q->keys[handle];return user8(pointer,q->keys,256,1)?-998:0;
#else
  return -50;
#endif
 }
 if(op==WUI_CLIPFORMAT144)return handle||argument?-87:clip_register144(pointer);
 if(op==WUI_CLIPNAME144)return clip_name144(handle,pointer,argument);
 if(op==WUI_METRICS144){
#ifdef ENGINE_M73
  if(handle||argument)return -87;unsigned scale=ui73_scale();if(scale<2||scale>4)return -87;unsigned width=ui73_width()*2/scale,height=ui73_height()*2/scale,x=0,y=0,buttons=0;usb_mouse_peek145(&x,&y,&buttons);wui_metrics144 metrics={width,height,height>60?height-60:0,scale,(ui73_measure("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",1)/26+1)/2,16,x,y};return user8(pointer,&metrics,sizeof(metrics),1)?-998:0;
#else
  return -50;
#endif
 }
 if(op==WUI_CURSOR144){if(pointer||argument||handle>65535)return -87;unsigned id=(unsigned)handle;if(id&&id!=32512&&id!=32513&&id!=32642&&id!=32643&&id!=32644&&id!=32645)return -50;unsigned old=ui_cursors144[active_space142];ui_cursors144[active_space142]=id;return old;}

 if(op==WUI_CREATE144||op==WUI_UPDATE144){
  if(argument)return -87;wui_description144 d;if(user8(pointer,&d,sizeof(d),0))return -998;
  unsigned error=ui_description144(&d,op==WUI_UPDATE144?handle:0);if(error)return -(int64_t)error;
  if(!d.parent&&d.visible){ui_window144*previous=op==WUI_UPDATE144?ui_owned144(handle):0;if((!previous||!previous->view.description.visible)&&desktop_native_windows144()+w8_ui_visible_roots144()>=WUI_NATIVE_ROOTS144)return -1816;}

  ui_window144*w=0;
  if(op==WUI_CREATE144){if(handle)return -87;if(ui_generation144==UINT32_MAX)return -1816;unsigned slot=0;while(slot<WUI_WINDOWS144&&ui_windows144[slot])++slot;if(slot==WUI_WINDOWS144)return -1816;
   if(!ui_queue144(active_space142,current142,1))return -8;w=ui_page144();if(!w)return -8;
   w->space=active_space142;w->thread=current142;w->generation=++ui_generation144;w->view.handle=WUI_HANDLE144|((uint64_t)w->generation<<8)|slot;w->view.process=input8.process_id;w->view.thread=(uint32_t)thread_token142(current142);ui_windows144[slot]=w;
  }else{w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;}
  unsigned units=0,position=0,bytes=0;while(units<128&&d.title[units])++units;char caption[384];
  while(position<units){uint32_t cp;if(!decode_utf16_143(d.title,units,&position,&cp)||!encode_utf8_143(cp,caption,sizeof(caption)-1,&bytes)){if(op==WUI_CREATE144)ui_destroy144(w->view.handle);return -1113;}}caption[bytes]=0;copy8(w->view.caption,caption,sizeof(w->view.caption));
  if((d.style&0x20000000u)&&(w->view.description.style&0x01000000u))w->restore_max=1;else if(!(d.style&0x20000000u))w->restore_max=0;if(op==WUI_CREATE144||!(d.style&0x21000000u))w->normal_bounds=d.bounds;else if(!(w->view.description.style&0x21000000u))w->normal_bounds=w->view.description.bounds;w->view.description=d;if(!d.enabled)ui_disable_input144(w);w->view.revision=++ui_revision144;return (int64_t)w->view.handle;
 }
 if(op==WUI_DESTROY144){ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;if(pointer||argument)return -87;ui_destroy144(handle);return 0;}
 if(op==WUI_QUERY144){ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(argument)return -87;return user8(pointer,&w->view,sizeof(w->view),1)?-998:0;}
 if(op==WUI_QUIT144){if(handle||pointer||argument>UINT32_MAX)return -87;wui_queue144*q=ui_queue144(active_space142,current142,1);if(!q)return -8;q->quit=1;q->quit_code=(uint32_t)argument;q->new_input148|=264u;return 0;}
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
  wui_queue144*q=ui_queue144(active_space142,current142,1);if(!q)return -8;
#ifdef ENGINE_M14
 if(op==WUI_PEEK144){q->new_input148&=~(8u|64u);if(!filter.first&&!filter.last){q->new_input148=0;q->timer_seen148=m3_clock_ticks()*10;}else{if(filter.first<=0x109&&filter.last>=0x100)q->new_input148&=~1u;if(filter.first<=0x200&&filter.last>=0x200)q->new_input148&=~2u;if(filter.first<=0x20e&&filter.last>=0x201)q->new_input148&=~4u;if(filter.first<=0x312&&filter.last>=0x312)q->new_input148&=~128u;if(filter.first<=0x113&&filter.last>=0x113)q->timer_seen148=m3_clock_ticks()*10;}}
#endif
 int index=ui_find144(q,&filter);
  if(index>=0){if(op==WUI_WAIT144)return 0;if(user8(pointer,q->items+index,sizeof(wui_message144),1))return -998;if(filter.remove){wui_key_commit145(q->keys,q->items+index);wui_remove144(q,(unsigned)index);}return 1;}
  if(q->quit){if(op==WUI_WAIT144)return 0;wui_message144 quit={.message=0x12,.wparam=q->quit_code};if(user8(pointer,&quit,sizeof(quit),1))return -998;if(filter.remove)q->quit=0;return 1;}
  int64_t timer=ui_timer_peek144(&filter,pointer,op==WUI_WAIT144);if(timer)return timer;
  if(op==WUI_PEEK144)return 0;if(pointer)return -87;
  q->waiting=filter;threads142[current142].deadline=ui_timer_deadline144(&filter);threads142[current142].state=T144_GUI;context8=*f;context8.rax=0;w8_active=0;w8_escape();
 }
 return -87;
}
unsigned w8_ui_revision144(void){return ui_revision144;}
unsigned w8_ui_at144(unsigned index,wui_view144*out){if(index>=WUI_WINDOWS144||!out||!ui_windows144[index])return 0;*out=ui_windows144[index]->view;return 1;}
unsigned w8_ui_input144(uint64_t handle,unsigned message,uint64_t wp,uint64_t lp){ui_window144*w=ui_lookup144(handle);if(!w)return 0;if((message==0x10||message==7||(message>=0x100&&message<=0x209))&&!ui_enabled_chain144(w))return 0;if(message==0x20&&!wp){handle=ui_input_target144(handle,0x200,&lp);wp=handle;lp=0x02000001;}else handle=ui_input_target144(handle,message,&lp);w=ui_lookup144(handle);if(!w)return 0;wui_message144 m={.window=handle,.wparam=wp,.lparam=lp,.message=message,.time=(uint32_t)(m3_clock_ticks()*10),.reserved={message==0x100||message==0x101||message==0x104||message==0x105?1u:0u,ui_input_snapshot145(message)}};return ui_enqueue144(w->space,w->thread,&m,1);}
unsigned w8_ui_modifiers145(uint64_t root,unsigned snapshot){
#ifdef ENGINE_M14
 ui_window144*w=ui_lookup144(root);if(!w||!ui_enabled_chain144(w))return 0;wui_queue144*q=ui_queue144(w->space,w->thread,1);if(!q)return 0;unsigned raw=(snapshot>>8)&255;
 static const uint8_t vk[8]={0x11,0x10,0x12,0x5b,0x11,0x10,0x12,0x5c},scan[8]={0x1d,0x2a,0x38,0x5b,0x1d,0x36,0x38,0x5c};
 for(unsigned n=0;n<8;++n){unsigned bit=1u<<n;if(!((raw^q->modifiers_sent145)&bit))continue;unsigned down=(raw&bit)!=0,alt=n==2||n==6,message=alt?(down?0x104u:0x105u):(down?0x100u:0x101u);uint64_t lp=1u|((uint64_t)scan[n]<<16);if(n==3||n==4||n==6||n==7)lp|=1u<<24;if(raw&0x44)lp|=1u<<29;if(!down)lp|=UINT64_C(3)<<30;
  uint64_t target=ui_input_target144(root,message,&lp);ui_window144*child=ui_lookup144(target);if(!child)return 0;wui_message144 m={.window=target,.wparam=vk[n],.lparam=lp,.message=message,.time=(uint32_t)(m3_clock_ticks()*10),.reserved={1,WUI_KEY_SNAPSHOT145|snapshot}};if(!ui_enqueue144(child->space,child->thread,&m,1))return 0;q->modifiers_sent145=(q->modifiers_sent145&~bit)|(raw&bit);
 }return 1;
#else
 (void)root;(void)snapshot;return 0;
#endif
}
unsigned w8_ui_cursor144(uint64_t handle){ui_window144*w=ui_lookup144(handle);return w?ui_cursors144[w->space]:32512;}
unsigned w8_ui_place144(uint64_t handle,wui_rect144 bounds,unsigned flags){ui_window144*w=ui_lookup144(handle);if(!w||(flags&~7u)||bounds.width<0||bounds.height<0||bounds.width>16384||bounds.height>16384)return 0;if(!(flags&6u))w->normal_bounds=bounds;else if(!(w->view.description.style&0x21000000u))w->normal_bounds=w->view.description.bounds;w->view.description.bounds=bounds;w->view.description.visible=flags&1;unsigned old_style=w->view.description.style;w->view.description.style&=~0x31000000u;w->restore_max=(flags&2)&&((flags&4)||(old_style&0x01000000u));w->view.description.style|=(flags&1?0x10000000u:0)|(flags&2?0x20000000u:0)|((flags&4)&&!(flags&2)?0x01000000u:0);w->view.revision=++ui_revision144;return 1;}

unsigned w8_ui_normal144(uint64_t handle,wui_rect144*out){ui_window144*w=ui_lookup144(handle);if(!w||!out)return 0;*out=w->normal_bounds;return 1;}

unsigned w8_ui_restore_max144(uint64_t handle){ui_window144*w=ui_lookup144(handle);return w?w->restore_max:0;}

unsigned w8_ui_visible_roots144(void){unsigned count=0;for(unsigned i=0;i<WUI_WINDOWS144;++i)if(ui_windows144[i]&&!ui_windows144[i]->view.description.parent&&ui_windows144[i]->view.description.visible)++count;return count;}
unsigned w8_ui_style145(uint64_t handle,uint32_t*out){ui_window144*w=ui_lookup144(handle);if(!w||!out)return 0;*out=w->view.description.style;return 1;}
