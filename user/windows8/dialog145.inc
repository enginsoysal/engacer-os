/* Resource dialogs run the original application procedure in its own thread. */
#include "dialog-core145.h"
typedef struct dialog_context145 {
 struct dialog_context145*next;HANDLE window,owner,previous_focus,children[DIALOG_CONTROLS145];
 ui_proc144 procedure;unsigned thread,child_count,initialized,ended,restore_owner;int64_t result;
} dialog_context145;
static dialog_context145*dialogs145;static unsigned dialog_count145;static lock142 dialog_lock145;
static dialog_context145*dialog_find145(HANDLE h){dialog_context145*found=0;lock_enter142(&dialog_lock145);for(dialog_context145*d=dialogs145;d;d=d->next)if(d->thread==tid142()&&d->window==h){found=d;break;}lock_leave142(&dialog_lock145);return found;}
static void dialog_unlink145(dialog_context145*d){lock_enter142(&dialog_lock145);dialog_context145**link=&dialogs145;while(*link&&*link!=d)link=&(*link)->next;if(*link){*link=d->next;--dialog_count145;}lock_leave142(&dialog_lock145);free8(d);}
static int MS f_EndDialog(HANDLE h,int64_t result){dialog_context145*d=dialog_find145(h);if(!d||d->ended){last8(1400);return 0;}d->result=result;d->ended=1;return 1;}
static int64_t dialog_default145(HANDLE h,unsigned message,uint64_t wp,int64_t lp){
 if(message==0x10){f_SendMessageW(h,0x111,2,0);return 0;}
 if(message==0x111&&((wp&65535)==1||(wp&65535)==2)){f_EndDialog(h,(int64_t)(wp&65535));return 0;}
 return f_DefWindowProcW(h,message,wp,lp);
}
static int64_t MS f_DefDlgProcW(HANDLE h,unsigned message,uint64_t wp,int64_t lp){return dialog_default145(h,message,wp,lp);}
static int64_t MS dialog_proc145(HANDLE h,unsigned message,uint64_t wp,int64_t lp){
 dialog_context145*d=dialog_find145(h);
 if(message==0x81){unsigned accepted=0;lock_enter142(&dialog_lock145);for(d=dialogs145;d;d=d->next)if(d->thread==tid142()&&!d->window){d->window=h;accepted=1;break;}lock_leave142(&dialog_lock145);return accepted;}
 if(!d)return f_DefWindowProcW(h,message,wp,lp);
 if(message==1)return 0; /* Dialog procedures receive WM_INITDIALOG, not WM_CREATE. */
 if(d->initialized){
  ui_proc144 proc=(ui_proc144)(uintptr_t)f_GetWindowLongPtrW(h,8);
  f_SetWindowLongPtrW(h,0,0);int64_t handled=proc?proc(h,message,wp,lp):0;
  if(message==0x82){d->ended=1;return 0;}
  if(message==0x110)return handled;
  if(handled){if((message>=0x132&&message<=0x138)||message==0x37||message==0x39||message==0x2e||message==0x2f)return handled;return f_GetWindowLongPtrW(h,0);}
 }
 if(message==0x82){d->ended=1;return 0;}
 return dialog_default145(h,message,wp,lp);
}
static HANDLE dialog_first145(dialog_context145*d,HANDLE after){
 unsigned start=0;for(unsigned n=0;n<d->child_count;++n)if(d->children[n]==after){start=n+1;break;}
 for(unsigned n=0;n<d->child_count;++n){HANDLE h=d->children[(start+n)%d->child_count];ui_window_runtime144*w=ui_window_lookup144(h);if(w&&(w->description.style&0x10000)&&w->description.visible&&w->description.enabled)return h;}
 return 0;
}
static int MS f_IsDialogMessageW(HANDLE h,const ui_msg144*m){
 dialog_context145*d=dialog_find145(h);if(!d||!m||m->message!=0x100)return 0;
 HANDLE at=m->window;for(unsigned n=0;at&&at!=h&&n<WUI_WINDOWS144;++n){ui_window_runtime144*w=ui_window_lookup144(at);at=w?w->description.parent:0;}if(at!=h)return 0;
 if(m->wp==9){HANDLE next=dialog_first145(d,f_GetFocus());if(next)f_SetFocus(next);return 1;}
 if(m->wp==13||m->wp==27){unsigned id=m->wp==27?2:1;
  if(m->wp==13)for(unsigned n=0;n<d->child_count;++n){ui_window_runtime144*w=ui_window_lookup144(d->children[n]);if(w&&control_kind144(w->class_->name)==C144_BUTTON&&(w->description.style&15)==1&&w->description.enabled){id=(unsigned)w->id;break;}}
  HANDLE button=f_GetDlgItem(h,(int)id);f_SendMessageW(h,0x111,id,(int64_t)button);return 1;
 }
 return 0;
}
static const WCHAR*dialog_class145(dialog_name145 name){
 if(!name.ordinal)return name.text;
 switch(name.ordinal){case 0x80:return u"Button";case 0x81:return u"Edit";case 0x82:return u"Static";case 0x83:return u"ListBox";case 0x84:return u"ScrollBar";case 0x85:return u"ComboBox";default:return 0;}
}
static int64_t dialog_run145(HANDLE instance,const void*bytes,unsigned length,HANDLE owner,ui_proc144 procedure,int64_t parameter){
 if(!procedure){last8(87);return -1;}if(owner&&!f_IsWindow(owner)){last8(1400);return 0;}
 ui_window_runtime144*owner_record=owner?ui_window_lookup144(owner):0;if(owner_record&&owner_record->thread!=tid142()){last8(50);return -1;}
 dialog_template145 parsed;unsigned error=dialog_parse145(bytes,length,&parsed);if(error){last8(error);return -1;}
 if(parsed.title.ordinal||(parsed.style&0x40000000)||(parsed.class_name.ordinal&&parsed.class_name.ordinal!=32770)||(parsed.class_name.text&&f_wcscmp(parsed.class_name.text,u"#32770"))){last8(50);return -1;}
 lock_enter142(&ui_lock144);ui_class144*existing=ui_class_lookup144(u"#32770");if(existing&&(existing->definition.proc!=dialog_proc145||existing->definition.win_extra<32)){lock_leave142(&ui_lock144);last8(1410);return -1;}if(!existing){ui_class_definition144 definition={0};definition.proc=dialog_proc145;definition.win_extra=32;definition.name=u"#32770";definition.background=16;definition.cursor=f_LoadCursorW(0,(const WCHAR*)(uintptr_t)32512);if(!f_RegisterClassW(&definition)){lock_leave142(&ui_lock144);return -1;}}lock_leave142(&ui_lock144);
 dialog_context145*d=calloc8(1,sizeof(*d));if(!d){last8(8);return -1;}d->thread=tid142();d->owner=owner;d->procedure=procedure;d->previous_focus=f_GetFocus();lock_enter142(&dialog_lock145);if(dialog_count145>=8){lock_leave142(&dialog_lock145);free8(d);last8(1816);return -1;}d->next=dialogs145;dialogs145=d;++dialog_count145;lock_leave142(&dialog_lock145);
 if(owner&&f_IsWindowEnabled(owner)){d->restore_owner=1;f_EnableWindow(owner,0);}
 unsigned units=f_GetDialogBaseUnits(),base_x=units&65535,base_y=units>>16;
 if(!base_x||!base_y){error=87;goto failed;}
 int width=parsed.width*(int)base_x/4+2,height=parsed.height*(int)base_y/8+41;
 wui_metrics144 metrics;if(!window_metrics144(&metrics)){error=f_GetLastError();goto failed;}
 int x=parsed.x*(int)base_x/4,y=parsed.y*(int)base_y/8;
 if((parsed.style&0x800)||(!parsed.x&&!parsed.y)){win_rect144 bounds={0,0,(int)metrics.width,(int)metrics.work_height};if(owner)f_GetWindowRect(owner,&bounds);x=bounds.left+(bounds.right-bounds.left-width)/2;y=bounds.top+(bounds.bottom-bounds.top-height)/2;if(x<0)x=0;if(y<0)y=0;}
 HANDLE menu=0;if(parsed.menu.ordinal||parsed.menu.text){menu=f_LoadMenuW(instance,parsed.menu.ordinal?(const WCHAR*)(uintptr_t)parsed.menu.ordinal:parsed.menu.text);if(!menu){error=f_GetLastError();goto failed;}}
 HANDLE h=f_CreateWindowExW(parsed.exstyle,u"#32770",parsed.title.text,parsed.style&~0x10000000u,x,y,width,height,owner,menu,instance,0);
 if(!h){if(menu)f_DestroyMenu(menu);error=f_GetLastError();goto failed;}
 f_SetWindowLongPtrW(h,8,(int64_t)(uintptr_t)procedure);
 for(unsigned n=0;n<parsed.count;++n){dialog_item145*item=parsed.items+n;const WCHAR*class_name=dialog_class145(item->class_name);if(!class_name){error=1407;goto failed;}
  HANDLE child=f_CreateWindowExW(item->exstyle,class_name,item->title.text,item->style|0x40000000u,item->x*(int)base_x/4,item->y*(int)base_y/8,item->width*(int)base_x/4,item->height*(int)base_y/8,h,item->id,instance,item->extra_bytes?(void*)item->extra:0);
  if(!child){error=f_GetLastError();goto failed;}d->children[d->child_count++]=child;
  if(item->title.ordinal){ui_window_runtime144*w=ui_window_lookup144(child);control_state144*c=w?w->control:0;
   if(!c||c->kind!=C144_STATIC||(item->style&31)!=3){error=50;goto failed;}
   HANDLE image=f_LoadImageW(instance,(const WCHAR*)(uintptr_t)item->title.ordinal,1,0,0,(item->style&0x800)?0x8000:0x8040);if(!image||!static_icon145(w,c,image)){error=f_GetLastError();goto failed;}
  }
  if(parsed.style&64)f_SendMessageW(child,0x30,UINT64_C(0x464f000000000011),0);
 }
 d->initialized=1;HANDLE first=dialog_first145(d,0);int focus=(int)f_SendMessageW(h,0x110,first,parameter);
 if(!d->ended){f_ShowWindow(h,5);if(focus&&first)f_SetFocus(first);else if(!first)f_SetFocus(h);}
 while(!d->ended){ui_msg144 message;int got=f_GetMessageW(&message,0,0,0);if(got<=0){if(!got)f_PostQuitMessage((int)message.wp);d->result=got<0?-1:0;break;}if(!f_IsDialogMessageW(h,&message)){f_TranslateMessage(&message);f_DispatchMessageW(&message);}}
 {int64_t result=d->result;if(f_IsWindow(h))f_DestroyWindow(h);if(d->restore_owner&&f_IsWindow(owner))f_EnableWindow(owner,1);if(f_IsWindow(d->previous_focus))f_SetFocus(d->previous_focus);else if(owner&&f_IsWindow(owner))f_SetFocus(owner);dialog_unlink145(d);return result;}
failed:
 if(d->window&&f_IsWindow(d->window))f_DestroyWindow(d->window);
 if(d->restore_owner&&f_IsWindow(owner))f_EnableWindow(owner,1);dialog_unlink145(d);last8(error?error:87);return -1;
}
static int64_t MS f_DialogBoxParamW(HANDLE instance,const WCHAR*name,HANDLE owner,ui_proc144 procedure,int64_t parameter){
 if(owner&&!f_IsWindow(owner)){last8(1400);return 0;}
 HANDLE resource=f_FindResourceW(instance,name,(const WCHAR*)(uintptr_t)5);if(!resource)return -1;
 unsigned bytes=f_SizeofResource(instance,resource);HANDLE loaded=f_LoadResource(instance,resource);const void*data=loaded?f_LockResource(loaded):0;if(!data)return -1;
 return dialog_run145(instance,data,bytes,owner,procedure,parameter);
}
static void dialog_cleanup_thread145(unsigned thread){for(;;){lock_enter142(&dialog_lock145);dialog_context145**link=&dialogs145;while(*link&&(*link)->thread!=thread)link=&(*link)->next;dialog_context145*d=*link;if(d){*link=d->next;--dialog_count145;}lock_leave142(&dialog_lock145);if(!d)break;if(d->restore_owner&&f_IsWindow(d->owner))f_EnableWindow(d->owner,1);free8(d);}}
static int MS f_GetDlgCtrlID(HANDLE h){ui_window_runtime144*w=ui_window_lookup144(h);if(!w){last8(1400);return 0;}return(int)w->id;}
static unsigned MS f_GetDlgItemTextW(HANDLE h,int id,WCHAR*out,int capacity){HANDLE child=f_GetDlgItem(h,id);return child?(unsigned)f_GetWindowTextW(child,out,capacity):0;}
static int MS f_CheckDlgButton(HANDLE h,int id,unsigned state){if(state>2){last8(87);return 0;}HANDLE child=f_GetDlgItem(h,id);if(!child)return 0;f_SendMessageW(child,0xf1,state,0);return 1;}
static unsigned MS f_IsDlgButtonChecked(HANDLE h,int id){HANDLE child=f_GetDlgItem(h,id);return child?(unsigned)f_SendMessageW(child,0xf0,0,0):0;}
