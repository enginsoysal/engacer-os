/* USER32 callbacks remain in this protected runtime and use the Win64 ABI. */
#include <engine/winui144.h>
/* Adapter identity for the actual native compositor root, not an owned window. */
#define DESKTOP_HANDLE148 UINT64_C(0x5744ffffffffffff)
typedef int64_t(MS*ui_proc144)(HANDLE,unsigned,uint64_t,int64_t);
typedef struct {unsigned style;ui_proc144 proc;int cls_extra,win_extra;HANDLE instance,icon,cursor,background;const WCHAR*menu,*name;} ui_class_definition144;
typedef struct ui_class144 {struct ui_class144*next;ui_class_definition144 definition;WCHAR name[64];unsigned atom,windows;HANDLE small_icon;} ui_class144;
typedef struct ui_window_runtime144 {struct ui_window_runtime144*next;HANDLE handle,menu;ui_class144*class_;ui_proc144 proc;unsigned thread,destroying,created,extra_size;void*control;void*drop_target;unsigned drop_pending;unsigned invalid,erase,restore_max;wui_rect144 damage,normal_bounds;int64_t userdata,id;wui_description144 description;uint8_t extra[];} ui_window_runtime144;
static ui_class144 *ui_classes144;static ui_window_runtime144 *ui_runtime_windows144;
static lock142 ui_lock144;static unsigned ui_atom144=0xc000,ui_class_count144;
static int64_t MS f_DefWindowProcW(HANDLE,unsigned,uint64_t,int64_t);
static int MS f_DestroyWindow(HANDLE);
static unsigned ui_builtin144(const WCHAR*);
static void control_release144(ui_window_runtime144*);
static void drop_release144(ui_window_runtime144*);
static HANDLE MS f_SetCursor(HANDLE);
static HANDLE MS f_LoadMenuW(HANDLE,const WCHAR*);
static int MS f_DestroyMenu(HANDLE);
static int menu_paint145(HANDLE);
static int64_t menu_nonclient145(HANDLE,uint64_t,int64_t);
static int64_t paint_default144(HANDLE);
static void paint_changed144(HANDLE,unsigned);
static void paint_release144(HANDLE);
static int64_t position_changed148(HANDLE,int64_t);
static int64_t ui_call144(unsigned op,HANDLE handle,void*pointer,uint64_t arg){return(int64_t)sys8(W8_SYS_UI144,op,handle,(uint64_t)(uintptr_t)pointer,arg,0);}
static unsigned ui_wide144(WCHAR*out,unsigned cap,const WCHAR*in){unsigned n=0;while(in&&in[n]){if(n+1>=cap){last8(206);return 0;}out[n]=in[n];++n;}out[n]=0;return 1;}
static ui_class144 *ui_class_lookup144(const WCHAR*name){for(ui_class144*c=ui_classes144;c;c=c->next){if((uintptr_t)name<=65535){if(c->atom==(uintptr_t)name)return c;}else if(!f_wcscmp(c->name,name)||(int64_t)sys8(W8_SYS_TEXT143,1,(uint64_t)(uintptr_t)c->name,(uint64_t)(uintptr_t)name,0,0)==0)return c;}return 0;}
static ui_window_runtime144 *ui_window_lookup144(HANDLE handle){for(ui_window_runtime144*w=ui_runtime_windows144;w;w=w->next)if(w->handle==handle)return w;return 0;}
static unsigned ui_refresh144(ui_window_runtime144*w){wui_view144 view;int64_t status=ui_call144(WUI_QUERY144,w->handle,&view,0);if(status<0){last8((unsigned)-status);return 0;}w->description=view.description;return 1;}
static unsigned ui_sync144(ui_window_runtime144*w){int64_t result=ui_call144(WUI_UPDATE144,w->handle,&w->description,0);if(result<0){last8((unsigned)-result);return 0;}return 1;}
static unsigned MS f_RegisterClassW(const ui_class_definition144*d){
 if(!d||!d->proc||!d->name||(uintptr_t)d->name<=65535||d->cls_extra||d->win_extra<0||d->win_extra>4096){last8(87);return 0;}
 lock_enter142(&ui_lock144);if(ui_class_lookup144(d->name)){lock_leave142(&ui_lock144);last8(1410);return 0;}
 if(ui_class_count144==64||ui_atom144==65535){lock_leave142(&ui_lock144);last8(1816);return 0;}
 ui_class144*c=calloc8(1,sizeof(*c));if(!c){lock_leave142(&ui_lock144);last8(8);return 0;}if(!ui_wide144(c->name,64,d->name)){free8(c);lock_leave142(&ui_lock144);return 0;}
 c->definition=*d;c->definition.name=c->name;c->atom=++ui_atom144;c->next=ui_classes144;ui_classes144=c;++ui_class_count144;unsigned atom=c->atom;lock_leave142(&ui_lock144);return atom;
}
static int MS f_GetClassInfoW(HANDLE instance,const WCHAR*name,ui_class_definition144*out){(void)instance;lock_enter142(&ui_lock144);ui_class144*c=ui_class_lookup144(name);if(c&&out)*out=c->definition;lock_leave142(&ui_lock144);if(!c||!out){last8(c?87:1411);return 0;}return 1;}
typedef struct {unsigned size,style;ui_proc144 proc;int cls_extra,win_extra;HANDLE instance,icon,cursor,background;const WCHAR*menu,*name;HANDLE small_icon;} ui_class_ex148;
_Static_assert(sizeof(ui_class_ex148)==80,"AMD64 WNDCLASSEXW ABI");
static unsigned MS f_RegisterClassExW(const ui_class_ex148*input){
 if(!input||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,sizeof(*input),1,0,0)){last8(87);return 0;}ui_class_ex148 d=*input;if(d.size!=sizeof(d)){last8(87);return 0;}
 ui_class_definition144 definition={d.style,d.proc,d.cls_extra,d.win_extra,d.instance,d.icon,d.cursor,d.background,d.menu,d.name};lock_enter142(&ui_lock144);unsigned atom=f_RegisterClassW(&definition);if(atom){ui_class144*c=ui_class_lookup144((const WCHAR*)(uintptr_t)atom);c->small_icon=d.small_icon;}lock_leave142(&ui_lock144);return atom;
}
static int MS f_GetClassInfoExW(HANDLE instance,const WCHAR*name,ui_class_ex148*out){
 if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,sizeof(*out),3,0,0)||out->size!=sizeof(*out)){last8(87);return 0;}
 lock_enter142(&ui_lock144);ui_class144*c=ui_class_lookup144(name);if(!c||(instance&&instance!=c->definition.instance)){lock_leave142(&ui_lock144);last8(1411);return 0;}ui_class_definition144 d=c->definition;*out=(ui_class_ex148){80,d.style,d.proc,d.cls_extra,d.win_extra,d.instance,d.icon,d.cursor,d.background,d.menu,d.name,c->small_icon};lock_leave142(&ui_lock144);return 1;
}
static int MS f_UnregisterClassW(const WCHAR*name,HANDLE instance){lock_enter142(&ui_lock144);ui_class144*c=ui_class_lookup144(name);if(!c||(instance&&instance!=c->definition.instance)){lock_leave142(&ui_lock144);last8(1411);return 0;}if(c->windows){lock_leave142(&ui_lock144);last8(1412);return 0;}ui_class144**link=&ui_classes144;while(*link!=c)link=&(*link)->next;*link=c->next;--ui_class_count144;free8(c);lock_leave142(&ui_lock144);return 1;}
static int64_t MS f_CallWindowProcW(ui_proc144 proc,HANDLE window,unsigned message,uint64_t wp,int64_t lp){if(!proc){last8(87);return 0;}return proc(window,message,wp,lp);}
#ifdef ENGINE_M14
#include "subclass148.inc"
#endif
static int64_t MS f_SendMessageW(HANDLE handle,unsigned message,uint64_t wp,int64_t lp){
 lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);ui_proc144 proc=w?w->proc:0;unsigned thread=w?w->thread:0;lock_leave142(&ui_lock144);
 if(!proc){last8(1400);return 0;}if(thread!=tid142()){last8(50);return 0;}int64_t result;
#ifdef ENGINE_M14
 result=subclass_dispatch148(proc,handle,message,wp,lp);
 if(message==0x82)subclass_release148(handle);
#else
 result=proc(handle,message,wp,lp);
#endif
 paint_changed144(handle,message);return result;
}
static HANDLE MS f_CreateWindowExW(unsigned exstyle,const WCHAR*class_name,const WCHAR*name,unsigned style,int x,int y,int width,int height,HANDLE parent,HANDLE menu,HANDLE instance,void*parameter){
 lock_enter142(&ui_lock144);ui_class144*c=ui_class_lookup144(class_name);if(!c&&ui_builtin144(class_name))c=ui_class_lookup144(class_name);if(!c){lock_leave142(&ui_lock144);last8(1407);return 0;}
 ui_window_runtime144*w=calloc8(1,sizeof(*w)+(unsigned)c->definition.win_extra);if(!w){lock_leave142(&ui_lock144);last8(8);return 0;}
 unsigned loaded_menu=0;if(!(style&0x40000000)&&!menu&&c->definition.menu){const WCHAR*resource=c->definition.menu;lock_leave142(&ui_lock144);menu=f_LoadMenuW(instance,resource);lock_enter142(&ui_lock144);if(!menu){free8(w);lock_leave142(&ui_lock144);return 0;}loaded_menu=1;}
 w->class_=c;w->proc=c->definition.proc;w->thread=tid142();w->extra_size=(unsigned)c->definition.win_extra;w->menu=menu;w->id=(int64_t)menu;
 wui_description144*d=&w->description;d->parent=(style&0x40000000)?parent:0;d->owner=(style&0x40000000)?0:parent;d->style=style;d->exstyle=exstyle;d->enabled=!(style&0x08000000);d->bounds=(wui_rect144){x==(int)0x80000000?80:x,y==(int)0x80000000?70:y,width==(int)0x80000000?760:width,height==(int)0x80000000?500:height};
 w->normal_bounds=d->bounds;
 const WCHAR*caption=name;if((uintptr_t)name&&((uintptr_t)name<=65535)){if(!f_wcscmp(c->name,u"Static")&&(style&31)==3)caption=0;else{if(loaded_menu)f_DestroyMenu(menu);free8(w);lock_leave142(&ui_lock144);last8(87);return 0;}}
 if(!ui_wide144(d->title,128,caption)||!ui_wide144(d->class_name,64,c->name)){if(loaded_menu)f_DestroyMenu(menu);free8(w);lock_leave142(&ui_lock144);return 0;}
 int64_t result=ui_call144(WUI_CREATE144,0,d,0);if(result<0){if(loaded_menu)f_DestroyMenu(menu);free8(w);lock_leave142(&ui_lock144);last8((unsigned)-result);return 0;}
 HANDLE handle=(HANDLE)result;w->handle=handle;w->next=ui_runtime_windows144;ui_runtime_windows144=w;++c->windows;lock_leave142(&ui_lock144);
 if(!(style&0x40000000)&&menu&&!menu_paint145(handle)){f_DestroyWindow(handle);return 0;}
 struct {void*parameter;HANDLE instance,menu,parent;int cy,cx,y,x;unsigned style,pad;const WCHAR*name,*class_name;unsigned exstyle,pad2;} creation={parameter,instance,menu,parent,height,width,y,x,style,0,name,class_name,exstyle,0};
 int64_t accepted=f_SendMessageW(handle,0x81,0,(int64_t)(uintptr_t)&creation);
 if(!accepted){f_DestroyWindow(handle);return 0;}
 lock_enter142(&ui_lock144);w=ui_window_lookup144(handle);if(w)w->created=1;lock_leave142(&ui_lock144);if(!w)return 0;
 if(f_SendMessageW(handle,1,0,(int64_t)(uintptr_t)&creation)==-1){f_DestroyWindow(handle);return 0;}
 lock_enter142(&ui_lock144);w=ui_window_lookup144(handle);unsigned shown=0;if(w){w->description.visible=(style&0x10000000)!=0;shown=ui_sync144(w);}lock_leave142(&ui_lock144);if(w&&!shown){unsigned error=f_GetLastError();f_DestroyWindow(handle);last8(error);return 0;}if(w&&(style&0x10000000)){f_SendMessageW(handle,0x18,1,0);lock_enter142(&ui_lock144);w=ui_window_lookup144(handle);lock_leave142(&ui_lock144);}return w?handle:0;
}
static int MS f_DestroyWindow(HANDLE handle){
 if(handle==DESKTOP_HANDLE148){last8(5);return 0;}
 lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);if(!w||w->thread!=tid142()){lock_leave142(&ui_lock144);last8(w?5:1400);return 0;}if(w->destroying){lock_leave142(&ui_lock144);return 1;}w->destroying=1;lock_leave142(&ui_lock144);
 if(w->created)f_SendMessageW(handle,2,0,0);
 for(;;){HANDLE child=0;lock_enter142(&ui_lock144);for(ui_window_runtime144*n=ui_runtime_windows144;n;n=n->next)if(!n->destroying&&(n->description.parent==handle||n->description.owner==handle)){child=n->handle;break;}lock_leave142(&ui_lock144);if(!child)break;f_DestroyWindow(child);}
 drop_release144(w);paint_release144(handle);f_SendMessageW(handle,0x82,0,0);lock_enter142(&ui_lock144);w=ui_window_lookup144(handle);if(w){ui_window_runtime144**link=&ui_runtime_windows144;while(*link&&*link!=w)link=&(*link)->next;if(*link)*link=w->next;--w->class_->windows;control_release144(w);if(!(w->description.style&0x40000000)&&w->menu)f_DestroyMenu(w->menu);ui_call144(WUI_DESTROY144,handle,0,0);free8(w);}lock_leave142(&ui_lock144);return 1;
}
static int MS f_PostMessageW(HANDLE handle,unsigned message,uint64_t wp,int64_t lp){wui_message144 m={.message=message,.wparam=wp,.lparam=(uint64_t)lp};int64_t result=ui_call144(handle?WUI_POST144:WUI_THREAD_POST144,handle?handle:tid142(),&m,0);if(result<0){last8((unsigned)-result);return 0;}return 1;}
static void MS f_PostQuitMessage(int code){int64_t result=ui_call144(WUI_QUIT144,0,0,(uint32_t)code);if(result<0)last8((unsigned)-result);}

typedef struct {HANDLE window;unsigned message,pad;uint64_t wp;int64_t lp;unsigned time;int x,y;unsigned private_;} ui_msg144;
_Static_assert(sizeof(ui_msg144)==48,"Win64 MSG layout");
static int paint_peek144(ui_msg144*,HANDLE,unsigned,unsigned,unsigned);
#ifdef ENGINE_M14
static void gp_message148(unsigned);
#endif
static int ui_peek144(ui_msg144*out,HANDLE window,unsigned first,unsigned last,unsigned remove){if(!out){last8(87);return -1;}wui_filter144 filter={window,first,last,remove,0};wui_message144 m;int64_t result=ui_call144(WUI_PEEK144,0,&m,(uint64_t)(uintptr_t)&filter);if(result<0){last8((unsigned)-result);return -1;}if(result){*out=(ui_msg144){m.window,m.message,0,m.wparam,(int64_t)m.lparam,m.time,m.x,m.y,m.reserved[0]};
#ifdef ENGINE_M14
 gp_message148(m.message);
#endif
 }if(!result)return paint_peek144(out,window,first,last,remove);return(int)result;}
static int MS f_PeekMessageW(ui_msg144*out,HANDLE window,unsigned first,unsigned last,unsigned remove){if(remove&~1u){last8(87);return 0;}return ui_peek144(out,window,first,last,remove)>0;}
static int MS f_GetMessageW(ui_msg144*out,HANDLE window,unsigned first,unsigned last){for(;;){int result=ui_peek144(out,window,first,last,1);if(result<0)return -1;if(result)return out->message!=0x12;wui_filter144 filter={window,first,last,1,0};int64_t status=ui_call144(WUI_WAIT144,0,0,(uint64_t)(uintptr_t)&filter);if(status<0){last8((unsigned)-status);return -1;}}}
static int64_t MS f_DispatchMessageW(const ui_msg144*m){if(!m)return 0;if(m->message==0x113&&m->lp){typedef void(MS*timer_proc144)(HANDLE,unsigned,uint64_t,unsigned);((timer_proc144)(uintptr_t)m->lp)(m->window,m->message,m->wp,m->time);return 0;}return m->window?f_SendMessageW(m->window,m->message,m->wp,m->lp):0;}
static int MS f_TranslateMessage(const ui_msg144*m){if(!m||m->private_)return 0;if(m->message==0x100&&m->wp>=32&&m->wp<=126)return f_PostMessageW(m->window,0x102,m->wp,m->lp);return 0;}
static int MS ui_settext144(HANDLE handle,const WCHAR*text){WCHAR copy[128];if(!ui_wide144(copy,128,text))return 0;lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);unsigned ok=0;if(w&&w->thread==tid142()&&ui_refresh144(w)){wui_description144 previous=w->description;memcpy(w->description.title,copy,(wlen8(copy)+1)*2);ok=ui_sync144(w);if(!ok)w->description=previous;}lock_leave142(&ui_lock144);if(!w)last8(1400);return(int)ok;}
static int MS ui_gettext144(HANDLE handle,WCHAR*out,int capacity){if(!out||capacity<=0){last8(87);return 0;}lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);unsigned n=0;if(w){while(w->description.title[n]&&n+1<(unsigned)capacity){out[n]=w->description.title[n];++n;}out[n]=0;}lock_leave142(&ui_lock144);if(!w)last8(1400);return(int)n;}
static int MS ui_textlength144(HANDLE handle){lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);unsigned n=w?wlen8(w->description.title):0;lock_leave142(&ui_lock144);if(!w)last8(1400);return(int)n;}
static int64_t MS f_DefWindowProcW(HANDLE handle,unsigned message,uint64_t wp,int64_t lp){switch(message){case 0xa1:return menu_nonclient145(handle,wp,lp);case 0xf:return paint_default144(handle);case 0x81:return 1;case 0x20:{ui_window_runtime144*w=ui_window_lookup144(handle);HANDLE parent=w?w->description.parent:0;if(parent&&f_SendMessageW(parent,message,wp,lp))return 1;if(wp!=handle)return 0;w=ui_window_lookup144(handle);if(w&&w->class_->definition.cursor){f_SetCursor(w->class_->definition.cursor);return 1;}return 0;}case 0x10:return f_DestroyWindow(handle)?0:0;case 0xc:return ui_settext144(handle,(const WCHAR*)(uintptr_t)lp);case 0xd:return ui_gettext144(handle,(WCHAR*)(uintptr_t)lp,(int)wp);case 0xe:return ui_textlength144(handle);case 0x47:return position_changed148(handle,lp);case 0x84:return 1;default:return 0;}}
static int64_t MS f_GetWindowLongPtrW(HANDLE handle,int index){lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);int64_t value=0;if(w){if(index==-21)value=w->userdata;else if(index==-4)value=(int64_t)(uintptr_t)w->proc;else if(index==-16)value=w->description.style;else if(index==-20)value=w->description.exstyle;else if(index==-12)value=w->id;else if(index>=0&&(unsigned)index<=w->extra_size&&w->extra_size-(unsigned)index>=8)memcpy(&value,w->extra+index,8);else last8(1413);}lock_leave142(&ui_lock144);if(!w)last8(1400);return value;}
static int MS f_GetWindowLongW(HANDLE handle,int index){
 if(handle==DESKTOP_HANDLE148){if(index==-16)return 0x10000000;if(index==-20)return 0;last8(50);return 0;}
 lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);int32_t value=0;if(!w){lock_leave142(&ui_lock144);last8(1400);return 0;}
 if((index==-16||index==-20)&&!ui_refresh144(w)){lock_leave142(&ui_lock144);return 0;}
 if(index==-16)value=(int32_t)w->description.style;else if(index==-20)value=(int32_t)w->description.exstyle;else if(index==-12)value=(int32_t)w->id;else if(index>=0&&(unsigned)index<=w->extra_size&&w->extra_size-(unsigned)index>=4)memcpy(&value,w->extra+index,4);else last8(index<0?50:1413);lock_leave142(&ui_lock144);return value;
}
static int64_t MS f_SetWindowLongPtrW(HANDLE handle,int index,int64_t value){lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);int64_t old=0;if(w&&w->thread==tid142()){if(index==-21){old=w->userdata;w->userdata=value;}else if(index==-4){old=(int64_t)(uintptr_t)w->proc;if(value)w->proc=(ui_proc144)(uintptr_t)value;else last8(87);}else if(index==-12){old=w->id;w->id=value;}else if(index>=0&&(unsigned)index<=w->extra_size&&w->extra_size-(unsigned)index>=8){memcpy(&old,w->extra+index,8);memcpy(w->extra+index,&value,8);}else last8(50);}else last8(w?5:1400);lock_leave142(&ui_lock144);return old;}
static int show_window144(HANDLE handle,int command,unsigned*previous){if(command<0||command>11){last8(87);return 0;}lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);if(!w||w->thread!=tid142()||!ui_refresh144(w)){lock_leave142(&ui_lock144);last8(w?5:1400);return 0;}ui_call144(WUI_NORMAL144,handle,&w->normal_bounds,0);w->restore_max=(unsigned)ui_call144(WUI_NORMAL144,handle,0,2);wui_description144 old=w->description;wui_rect144 normal=w->normal_bounds;unsigned restore=w->restore_max;*previous=old.visible;if(!(old.style&0x21000000u)&&command!=1&&command!=4&&command!=9)w->normal_bounds=old.bounds;
 if(command==10)command=1;w->description.visible=command!=0;if(command)w->description.style|=0x10000000;else w->description.style&=~0x10000000u;
 if(command==2||command==6||command==7||command==11){w->restore_max=((old.style&0x01000000u)!=0)||w->restore_max;w->description.style=(w->description.style&~0x01000000u)|0x20000000u;}
 else if(command==3||(command==9&&(old.style&0x20000000u)&&w->restore_max)){wui_metrics144 metrics;int64_t status=ui_call144(WUI_METRICS144,0,&metrics,0);if(status<0){w->description=old;w->normal_bounds=normal;lock_leave142(&ui_lock144);last8((unsigned)-status);return 0;}w->description.bounds=(wui_rect144){0,0,(int)metrics.width,(int)metrics.work_height};w->description.style=(w->description.style&~0x20000000u)|0x01000000u;}
 else if(command==1||command==4||command==9){w->description.bounds=w->normal_bounds;w->description.style&=~0x21000000u;w->restore_max=0;}
 wui_description144 current=w->description;unsigned ok=ui_sync144(w);if(!ok){w->description=old;w->normal_bounds=normal;w->restore_max=restore;}lock_leave142(&ui_lock144);if(!ok)return 0;
 if(old.visible!=current.visible)f_SendMessageW(handle,0x18,current.visible,0);if(old.bounds.x!=current.bounds.x||old.bounds.y!=current.bounds.y)f_SendMessageW(handle,3,0,(current.bounds.x&65535)|((int64_t)(current.bounds.y&65535)<<16));if(old.bounds.width!=current.bounds.width||old.bounds.height!=current.bounds.height||((old.style^current.style)&0x21000000u)){wui_rect144 r=current.bounds;unsigned width=(unsigned)(r.width>2?r.width-2:0),height=(unsigned)(r.height>41?r.height-41:0);unsigned kind=current.style&0x20000000u?1:current.style&0x01000000u?2:0;if(kind==1)width=height=0;f_SendMessageW(handle,5,kind,(width&65535)|((int64_t)(height&65535)<<16));}return 1;}
static int MS f_ShowWindow(HANDLE handle,int command){unsigned previous=0;show_window144(handle,command,&previous);return(int)previous;}

static HANDLE MS f_GetParent(HANDLE handle){if(handle==DESKTOP_HANDLE148)return 0;lock_enter142(&ui_lock144);ui_window_runtime144*w=ui_window_lookup144(handle);HANDLE parent=w?(w->description.parent?w->description.parent:w->description.owner):0;lock_leave142(&ui_lock144);if(!w)last8(1400);return parent;}
static int MS f_IsWindow(HANDLE handle){if(handle==DESKTOP_HANDLE148){wui_metrics144 metrics;return ui_call144(WUI_METRICS144,0,&metrics,0)>=0;}lock_enter142(&ui_lock144);unsigned found=ui_window_lookup144(handle)!=0;lock_leave142(&ui_lock144);return(int)found;}

static int MS f_SetWindowTextW(HANDLE handle,const WCHAR*text){return(int)f_SendMessageW(handle,0xc,0,(int64_t)(uintptr_t)text);}
static int MS f_GetWindowTextW(HANDLE handle,WCHAR*out,int capacity){return(int)f_SendMessageW(handle,0xd,(unsigned)capacity,(int64_t)(uintptr_t)out);}
static int MS f_GetWindowTextLengthW(HANDLE handle){return(int)f_SendMessageW(handle,0xe,0,0);}
