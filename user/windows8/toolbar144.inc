/* Bounded toolbar state, copied labels and image-list association. No drawing claim. */
typedef struct {int bitmap,command;uint8_t state,style,reserved[6];uint64_t data;int64_t string;} toolbar_button144;
_Static_assert(sizeof(toolbar_button144)==32,"Win64 TBBUTTON layout");
typedef struct {unsigned declared,width,height,bitmap_width,bitmap_height;toolbar_button144 buttons[64];WCHAR*labels[64];} toolbar144;
static void toolbar_release144(control_state144*c){toolbar144*t=c->model;if(t)for(unsigned i=0;i<64;++i)free8(t->labels[i]);}
static int64_t toolbar_message144(ui_window_runtime144*w,control_state144*c,unsigned message,uint64_t wp,int64_t lp,unsigned*handled){
 *handled=1;toolbar144*t=c->model;if(!t){t=calloc8(1,sizeof(*t));if(!t)return 0;t->width=t->height=24;t->bitmap_width=t->bitmap_height=16;c->model=t;}
 if(message==0x41e){if(wp!=sizeof(toolbar_button144)){last8(87);return 0;}t->declared=(unsigned)wp;return 0;}
 if(message==0x430){if(wp){last8(50);return 0;}if(lp){lock_enter142(&image_lock144);image_object144*image=image_find144((HANDLE)lp,3);if(!image){lock_leave142(&image_lock144);return 0;}t->bitmap_width=image->width;t->bitmap_height=image->height;t->width=image->width+8;t->height=image->height+8;lock_leave142(&image_lock144);}HANDLE old=c->image;c->image=(HANDLE)lp;return(int64_t)old;}
 if(message==0x431)return(int64_t)c->image;
 if(message==0x444){if(t->declared!=32||wp>64-c->count||(!lp&&wp)){last8(87);return 0;}const toolbar_button144*input=(const void*)(uintptr_t)lp;unsigned start=c->count;
  for(unsigned n=0;n<wp;++n){unsigned index=start+n;t->buttons[index]=input[n];if(input[n].string>65535){if(!control_text144(&t->labels[index],(const WCHAR*)(uintptr_t)input[n].string)){for(unsigned j=start;j<=index;++j){free8(t->labels[j]);t->labels[j]=0;}return 0;}}else if(input[n].string&&input[n].string!=-1){for(unsigned j=start;j<index;++j){free8(t->labels[j]);t->labels[j]=0;}last8(50);return 0;}t->buttons[index].string=t->labels[index]?(int64_t)(uintptr_t)t->labels[index]:input[n].string;}
  c->count+=(unsigned)wp;return 1;}
 if(message==0x418)return c->count;
 if(message==0x417){if(wp>=c->count||!lp)return 0;memcpy((void*)(uintptr_t)lp,t->buttons+wp,32);return 1;}
 if(message==0x41f||message==0x420){unsigned width=(unsigned)lp&65535,height=((unsigned)lp>>16)&65535;if(!width||!height){last8(87);return 0;}if(message==0x41f){t->width=width;t->height=height;}else{t->bitmap_width=width;t->bitmap_height=height;}return 1;}
 if(message==0x43a)return t->width|(t->height<<16);
 if(message==0x453){if(!lp)return 0;unsigned width=0;for(unsigned i=0;i<c->count;++i)if(!(t->buttons[i].state&8)){unsigned length=wlen8(t->labels[i]);unsigned value=t->width;if(length){unsigned text_width=length*8+12;if(text_width>value)value=text_width;}width+=value;}((int*)(uintptr_t)lp)[0]=(int)width;((int*)(uintptr_t)lp)[1]=(int)(t->height+((c->count&&t->labels[0])?20:0));return 1;}
 if(message==0x421){int size[2];if(!toolbar_message144(w,c,0x453,0,(int64_t)(uintptr_t)size,handled))return 0;win_rect144 parent;if(w->description.parent&&f_GetClientRect(w->description.parent,&parent))size[0]=parent.right;f_MoveWindow(w->handle,0,0,size[0],size[1],1);return 0;}
 if(message==0x401||message==0x411||message==0x412){for(unsigned i=0;i<c->count;++i)if(t->buttons[i].command==(int)wp){if(message==0x412)return t->buttons[i].state;if(message==0x411)t->buttons[i].state=(uint8_t)lp;else t->buttons[i].state=(uint8_t)((t->buttons[i].state&~4u)|(lp?4:0));return 1;}return message==0x412?-1:0;}
 *handled=0;return 0;
}
