/* Registered control procedures execute in CPL3. Unsupported custom messages fail explicitly. */
enum {C144_BUTTON=1,C144_EDIT,C144_STATIC,C144_LISTBOX,C144_COMBO,C144_LISTVIEW,C144_HEADER,C144_STATUS,C144_TOOLBAR,C144_REBAR,C144_COMBOEX,C144_TREE,C144_TAB,C144_UPDOWN,C144_PROGRESS,C144_HOTKEY,C144_ANIMATE,C144_TOOLTIP};
typedef struct {const WCHAR*name;unsigned kind,group;} control_class144;
static const control_class144 control_classes144[]={
 {u"Button",C144_BUTTON,0},{u"Edit",C144_EDIT,0},{u"Static",C144_STATIC,0},{u"ListBox",C144_LISTBOX,0},{u"ComboBox",C144_COMBO,0},
 {u"SysListView32",C144_LISTVIEW,1},{u"SysHeader32",C144_HEADER,1},{u"msctls_statusbar32",C144_STATUS,4},{u"ToolbarWindow32",C144_TOOLBAR,4},{u"ReBarWindow32",C144_REBAR,0x400},{u"ComboBoxEx32",C144_COMBOEX,0x200},
 {u"SysTreeView32",C144_TREE,2},{u"SysTabControl32",C144_TAB,8},{u"msctls_updown32",C144_UPDOWN,16},{u"msctls_progress32",C144_PROGRESS,32},{u"msctls_hotkey32",C144_HOTKEY,64},{u"SysAnimate32",C144_ANIMATE,128},{u"tooltips_class32",C144_TOOLTIP,0xff}
};
typedef struct {unsigned kind,unicode,redraw,checked,style,count,parts;int selected;unsigned selection_start,selection_end;HANDLE font,image,child,edit;int edges[16];WCHAR*texts[16];void*model;} control_state144;
static unsigned control_kind144(const WCHAR*name){for(unsigned i=0;i<sizeof(control_classes144)/sizeof(control_classes144[0]);++i)if(!f_wcscmp(name,control_classes144[i].name))return control_classes144[i].kind;return 0;}
static void toolbar_release144(control_state144*);
static void list_release144(control_state144*);
static void combo_release144(control_state144*);
static void control_release144(ui_window_runtime144*w){control_state144*c=w->control;if(!c)return;for(unsigned i=0;i<16;++i)free8(c->texts[i]);if(c->kind==C144_TOOLBAR)toolbar_release144(c);if(c->kind==C144_LISTVIEW)list_release144(c);if(c->kind==C144_COMBO||c->kind==C144_COMBOEX)combo_release144(c);
#ifdef ENGINE_M14
 if(c->kind==C144_BUTTON&&(c->style&1)&&c->image)f_DestroyIcon(c->image);
#endif
 free8(c->model);free8(c);w->control=0;}
static unsigned control_text144(WCHAR**out,const WCHAR*text){unsigned n=wlen8(text);if(n>2047){last8(206);return 0;}WCHAR*copy=alloc8(((size_t)n+1)*2);if(!copy){last8(8);return 0;}if(text)memcpy(copy,text,(size_t)n*2);copy[n]=0;free8(*out);*out=copy;return 1;}
#include "toolbar144.inc"
#include "listview144.inc"
#include "list-input145.inc"
#include "combo144.inc"
#include "rebar144.inc"
#include "edit-input144.inc"
#include "button-input145.inc"
#include "static-image145.inc"
#ifdef ENGINE_M14
#include "progress148.inc"
#endif
#include "control-paint144.inc"
#ifdef ENGINE_M14
#include "button-size148.inc"
#endif
static int64_t MS control_proc144(HANDLE handle,unsigned message,uint64_t wp,int64_t lp){
 ui_window_runtime144*w=ui_window_lookup144(handle);if(!w){last8(1400);return 0;}control_state144*c=w->control;
 if(message==0x81){if(c)return 0;unsigned kind=control_kind144(w->class_->name);if(!kind)return 0;c=calloc8(1,sizeof(*c));if(!c)return 0;c->kind=kind;c->unicode=1;c->redraw=1;c->selected=-1;
#ifdef ENGINE_M14
 if(kind==C144_PROGRESS){if(w->description.style&8){free8(c);last8(50);return 0;}c->selected=0;c->edges[1]=100;c->edges[2]=10;}
#endif
 w->control=c;return 1;}
 if(!c)return f_DefWindowProcW(handle,message,wp,lp);
 if(c->kind==C144_STATIC){unsigned handled;int64_t result=static_message145(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(c->kind==C144_REBAR&&(message==0x111||message==0x4e))return w->description.parent?f_SendMessageW(w->description.parent,message,wp,lp):0;
 if((c->kind==C144_COMBO||c->kind==C144_COMBOEX)&&message!=0x82){unsigned handled;int64_t result=combo_message144(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(c->kind==C144_REBAR&&(message==5||message>=0x400)){unsigned handled;int64_t result=rebar_message144(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(c->kind==C144_EDIT){unsigned handled;int64_t result=edit_input144(w,c,message,wp,lp,&handled);if(handled)return result;}
#ifdef ENGINE_M14
 if(c->kind==C144_PROGRESS&&message>=0x400){unsigned handled;int64_t result=progress_message148(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(c->kind==C144_BUTTON&&message==0x1601)return button_ideal148(w,c,wp,lp);
 if(c->kind==C144_BUTTON&&message==0x160c){unsigned type=w->description.style&15;if(wp){last8(87);return 0;}if(type!=0&&type!=1&&type!=14&&type!=15){last8(50);return 0;}HANDLE icon=lp?shield_create148():0;if(lp&&!icon)return 0;HANDLE previous=c->image;c->image=icon;c->style=(c->style&~1u)|(lp?1u:0u);f_InvalidateRect(handle,0,0);return(int64_t)previous;}
 if(c->kind==C144_BUTTON&&message==0xf6){if(wp!=1){last8(50);return 0;}return(int64_t)c->image;}

#endif
 if(c->kind==C144_BUTTON){unsigned handled;int64_t result=button_input145(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(c->kind==C144_LISTVIEW){unsigned handled;int64_t result=list_input145(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(c->kind==C144_TOOLBAR&&c->model&&(message==0x201||message==0x202||message==0x215)){
  toolbar144*t=c->model;
  if(message==0x215){t->pressed=-1;f_InvalidateRect(handle,0,0);return 0;}
  int hit=toolbar_hit145(w,c,(int16_t)(lp&65535),(int16_t)((uint64_t)lp>>16));
  if(message==0x201){if(hit>=0&&(t->buttons[hit].state&4)&&!(t->buttons[hit].style&1)){t->pressed=hit;f_SetFocus(handle);f_SetCapture(handle);f_InvalidateRect(handle,0,0);}return 0;}
  int pressed=t->pressed;t->pressed=-1;HANDLE parent=w->description.parent;
  int command=pressed>=0&&pressed==hit&&(t->buttons[hit].state&4)&&!(t->buttons[hit].style&1)?t->buttons[hit].command:0;
  if(f_GetCapture()==handle)f_ReleaseCapture();f_InvalidateRect(handle,0,0);
  if(command&&f_IsWindow(parent))f_SendMessageW(parent,0x111,(unsigned)command&65535,(int64_t)handle);return 0;
 }
 if(message==0xf){control_paint144(handle,c);return 0;}
 if(message==0x82){control_release144(w);return 0;}
 if(message==0x30){c->font=wp;return 0;}if(message==0x31)return(int64_t)c->font;
 if(message==0xb){c->redraw=wp!=0;return 0;}
 if(message==0x2005){unsigned old=c->unicode;c->unicode=wp!=0;return old;}if(message==0x2006)return c->unicode;
 if(c->kind==C144_BUTTON){if(message==0xf0)return c->checked;if(message==0xf1){if(wp>2){last8(87);return 0;}c->checked=(unsigned)wp;return 0;}if(message==0xf3){w->description.style=(w->description.style&~0xffffu)|((unsigned)wp&65535);ui_sync144(w);return 0;}if(message==0xf5){HANDLE parent=w->description.parent;if(parent)f_SendMessageW(parent,0x111,(uint64_t)(w->id&65535),(int64_t)handle);return 0;}}
 if(c->kind==C144_EDIT){
  if(message==0xc){const WCHAR*text=(const WCHAR*)(uintptr_t)lp;if(!control_text144(&c->texts[0],text))return 0;c->selection_start=c->selection_end=0;WCHAR preview[128];widecopy8(preview,text,128);return f_DefWindowProcW(handle,message,wp,(int64_t)(uintptr_t)preview);}
  if(message==0xe)return wlen8(c->texts[0]);
  if(message==0xd){if(!lp||!wp)return 0;unsigned count=wlen8(c->texts[0]);if(count>=wp)count=(unsigned)wp-1;if(count)memcpy((void*)(uintptr_t)lp,c->texts[0],(size_t)count*2);((WCHAR*)(uintptr_t)lp)[count]=0;return count;}
  if(message==0xb0){unsigned start=c->selection_start<c->selection_end?c->selection_start:c->selection_end,end=c->selection_start>c->selection_end?c->selection_start:c->selection_end;if(wp)*(unsigned*)(uintptr_t)wp=start;if(lp)*(unsigned*)(uintptr_t)lp=end;return(start&65535)|(end<<16);}
  if(message==0xb1){unsigned length=wlen8(c->texts[0]);int start=(int)wp,end=(int)lp;if(start<0){c->selection_start=c->selection_end;return 0;}c->selection_start=(unsigned)start>length?length:(unsigned)start;c->selection_end=end<0||(unsigned)end>length?length:(unsigned)end;return 0;}
 }

 if(c->kind==C144_STATUS){
  if(message==0x404){if(wp>16||(!lp&&wp)){last8(87);return 0;}c->parts=(unsigned)wp;for(unsigned i=0;i<c->parts;++i)c->edges[i]=((const int*)(uintptr_t)lp)[i];return 1;}
  if(message==0x40b){unsigned index=(unsigned)wp&255;if(index>=16||(wp&0xf000)){last8(50);return 0;}return control_text144(c->texts+index,(const WCHAR*)(uintptr_t)lp);}
  if(message==0x40d){unsigned index=(unsigned)wp&255;if(index>=16||!lp){last8(87);return 0;}unsigned n=wlen8(c->texts[index]);if(c->texts[index])memcpy((void*)(uintptr_t)lp,c->texts[index],(size_t)n*2);((WCHAR*)(uintptr_t)lp)[n]=0;return n;}
  if(message==0x40c){unsigned index=(unsigned)wp&255;return index<16?wlen8(c->texts[index]):0;}
  if(message==0x406){unsigned count=(unsigned)wp;if(count>c->parts)count=c->parts;if(lp)memcpy((void*)(uintptr_t)lp,c->edges,count*4);return c->parts;}
  if(message==0x409){c->style=wp!=0;return 0;}
 }
 if(c->kind==C144_LISTVIEW&&message>=0x400){unsigned handled;int64_t result=list_message144(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(c->kind==C144_TOOLBAR&&message>=0x400){unsigned handled;int64_t result=toolbar_message144(w,c,message,wp,lp,&handled);if(handled)return result;}
 if(message>=0x400){print8("Unsupported control message: ");char name[128];if(utf16_to8(w->class_->name,name,sizeof(name))<0)copy8(name,"control",sizeof(name));print8(name);print8(" message=");number8(message);print8("\n");fail8("A required Windows common-control message is not implemented.");}
 return f_DefWindowProcW(handle,message,wp,lp);
}
static unsigned ui_builtin144(const WCHAR*name){
 if((uintptr_t)name<=65535)return 0;lock_enter142(&ui_lock144);for(unsigned i=0;i<sizeof(control_classes144)/sizeof(control_classes144[0]);++i){const control_class144*d=control_classes144+i;if(f_wcscmp(d->name,name))continue;
  if(ui_class_lookup144(d->name)){lock_leave142(&ui_lock144);return 1;}ui_class_definition144 definition={0};definition.style=8;definition.proc=control_proc144;definition.name=d->name;definition.cursor=UINT64_C(0x43000000)|(d->kind==C144_EDIT?32513:32512);unsigned registered=f_RegisterClassW(&definition)!=0;lock_leave142(&ui_lock144);return registered;
 }lock_leave142(&ui_lock144);return 0;
}

static int MS f_InitCommonControlsEx(const unsigned*value){if(!value||value[0]!=8||(value[1]&~0x6ffu)){last8(value&&value[0]==8?50:87);return 0;}for(unsigned i=0;i<sizeof(control_classes144)/sizeof(control_classes144[0]);++i){const control_class144*d=control_classes144+i;if(d->group&&(d->group&value[1])&&!ui_builtin144(d->name))return 0;}return 1;}
static void MS f_InitCommonControls(void){const unsigned initial[2]={8,0xff};if(!f_InitCommonControlsEx(initial))fail8("Windows common-control registration failed.");}

static HANDLE MS f_CreateStatusWindowW(unsigned style,const WCHAR*text,HANDLE parent,unsigned id){win_rect144 client;if(!f_GetClientRect(parent,&client))return 0;return f_CreateWindowExW(0,u"msctls_statusbar32",text,style,0,client.bottom>24?client.bottom-24:0,client.right,24,parent,id,0,0);}
