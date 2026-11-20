/* Composite combo windows retain real edit children and copied item data. */
typedef struct {unsigned mask,pad;int64_t index;WCHAR*text;int capacity,image,selected_image,overlay,indent,pad2;int64_t data;} combo_item144;
_Static_assert(sizeof(combo_item144)==56,"Win64 COMBOBOXEXITEMW layout");
typedef struct {WCHAR*text;int image,selected_image,overlay,indent;int64_t data;} combo_entry144;
typedef struct {combo_entry144*items;unsigned count,capacity,extended,changed,dropped;} combo_model144;
static void combo_release144(control_state144*c){combo_model144*m=c->model;if(m){for(unsigned i=0;i<m->count;++i)free8(m->items[i].text);free8(m->items);}}
static combo_model144*combo_model_for144(control_state144*c){if(c->kind==C144_COMBOEX){ui_window_runtime144*w=ui_window_lookup144(c->child);if(!w||!w->control)return 0;c=w->control;}if(!c->model)c->model=calloc8(1,sizeof(combo_model144));return c->model;}
static int combo_insert144(combo_model144*m,int64_t at,const combo_item144*item){if(!m||!item||item->mask&~0x7fu||m->count==256){last8(87);return -1;}if(at<0||(uint64_t)at>m->count)at=m->count;combo_entry144 entry={0};if((item->mask&1)&&!control_text144(&entry.text,item->text))return -1;if(item->mask&2)entry.image=item->image;if(item->mask&4)entry.selected_image=item->selected_image;if(item->mask&8)entry.overlay=item->overlay;if(item->mask&16)entry.indent=item->indent;if(item->mask&32)entry.data=item->data;
 if(m->count==m->capacity){unsigned cap=m->capacity?m->capacity*2:16;combo_entry144*next=calloc8(cap,sizeof(*next));if(!next){free8(entry.text);last8(8);return -1;}if(m->items)memcpy(next,m->items,m->count*sizeof(*next));free8(m->items);m->items=next;m->capacity=cap;}memmove(m->items+at+1,m->items+at,(m->count-(unsigned)at)*sizeof(entry));m->items[at]=entry;++m->count;return(int)at;}
static int64_t combo_message144(ui_window_runtime144*w,control_state144*c,unsigned msg,uint64_t wp,int64_t lp,unsigned*handled){
 *handled=1;
 if(msg==1){int width=w->description.bounds.width;if(c->kind==C144_COMBOEX){c->child=f_CreateWindowExW(0,u"ComboBox",u"",0x50000002,0,0,width,24,w->handle,1001,0,0);ui_window_runtime144*child=ui_window_lookup144(c->child);c->edit=child&&child->control?((control_state144*)child->control)->edit:0;}else if((w->description.style&3)!=3)c->edit=f_CreateWindowExW(0,u"Edit",w->description.title,0x50000080,2,2,width>22?width-22:0,20,w->handle,1002,0,0);if((c->kind==C144_COMBOEX&&!c->child)||((w->description.style&3)!=3&&!c->edit))return -1;w->description.bounds.height=24;ui_sync144(w);return 0;}
 if(msg==5){int width=w->description.bounds.width;if(c->kind==C144_COMBOEX&&c->child)f_MoveWindow(c->child,0,0,width,24,1);else if(c->edit)f_MoveWindow(c->edit,2,2,width>22?width-22:0,20,1);return 0;}
 if(msg==0xc||msg==0xd||msg==0xe){if(c->edit)return f_SendMessageW(c->edit,msg,wp,lp);return f_DefWindowProcW(w->handle,msg,wp,lp);}
 if(msg==0x30){c->font=wp;if(c->child)f_SendMessageW(c->child,msg,wp,lp);if(c->edit)f_SendMessageW(c->edit,msg,wp,lp);return 0;}
 if(c->kind==C144_COMBOEX){if(msg==0x402){HANDLE old=c->image;c->image=(HANDLE)lp;return(int64_t)old;}if(msg==0x403)return(int64_t)c->image;if(msg==0x406)return(int64_t)c->child;if(msg==0x407)return(int64_t)c->edit;if(msg==0x40e){unsigned old=c->style;c->style=wp?(old&~(unsigned)wp)|((unsigned)lp&(unsigned)wp):(unsigned)lp;return old;}if(msg==0x409)return c->style;}
 if(c->kind==C144_COMBOEX&&msg>=0x140&&msg<=0x165)return f_SendMessageW(c->child,msg,wp,lp);
 combo_model144*m=combo_model_for144(c);if(!m)return 0;
 if(msg==0x40b&&c->kind==C144_COMBOEX){const combo_item144*item=(void*)(uintptr_t)lp;return item?combo_insert144(m,item->index,item):-1;}
 if(msg==0x143||msg==0x14a){combo_item144 item={.mask=1,.text=(WCHAR*)(uintptr_t)lp};return combo_insert144(m,msg==0x143?-1:(int)wp,&item);}
 if(msg==0x146)return m->count;
 if(msg==0x147)return c->selected;
 if(msg==0x14e){int at=(int)wp;if(at< -1||(at>=0&&(unsigned)at>=m->count))return -1;c->selected=at;if(c->edit)f_SetWindowTextW(c->edit,at>=0?m->items[at].text:u"");return at;}
 if(msg==0x14b){for(unsigned i=0;i<m->count;++i)free8(m->items[i].text);if(m->items)memset(m->items,0,m->capacity*sizeof(*m->items));m->count=0;c->selected=-1;if(c->edit)f_SetWindowTextW(c->edit,u"");return 0;}
 if(msg==0x144){if(wp>=m->count)return -1;free8(m->items[wp].text);memmove(m->items+wp,m->items+wp+1,(m->count-(unsigned)wp-1)*sizeof(*m->items));--m->count;memset(m->items+m->count,0,sizeof(*m->items));if(c->selected>=(int)m->count)c->selected=-1;return m->count;}
 if(msg==0x148||msg==0x149){if(wp>=m->count||(msg==0x148&&!lp))return -1;unsigned n=wlen8(m->items[wp].text);if(msg==0x148){if(n)memcpy((void*)(uintptr_t)lp,m->items[wp].text,n*2);((WCHAR*)(uintptr_t)lp)[n]=0;}return n;}
 if(msg==0x150)return wp<m->count?m->items[wp].data:-1;
 if(msg==0x151){if(wp>=m->count)return -1;m->items[wp].data=lp;return 0;}
 if(msg==0x140||msg==0x142)return c->edit?f_SendMessageW(c->edit,msg==0x140?0xb0:0xb1,msg==0x140?wp:(unsigned)lp&65535,msg==0x140?lp:((unsigned)lp>>16)&65535):0;
 *handled=0;return 0;
}
