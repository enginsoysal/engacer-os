/* Process-owned list model. Rows are original-app data, never native Files data. */
typedef struct {unsigned mask;int item,subitem;unsigned state,state_mask,pad;WCHAR*text;int capacity,image;int64_t parameter;int indent,group;unsigned columns,pad2;unsigned*column_ids;int*formats;int group_index,pad3;} list_item144;
_Static_assert(sizeof(list_item144)==88,"Win64 LVITEMW layout");
typedef struct {unsigned mask;int format,width,pad;WCHAR*text;int capacity,subitem,image,order,min_width,default_width,ideal_width,pad2;} list_column144;
_Static_assert(sizeof(list_column144)==56,"Win64 LVCOLUMNW layout");
typedef struct {unsigned state;int image;int64_t parameter;WCHAR*text[16];} list_row144;
typedef struct {HANDLE images[4];unsigned extended,columns,capacity;int selection,top;uint32_t background,text_background,text_color;list_column144 column[32];WCHAR*labels[32];list_row144*rows;} list_model144;
static void list_row_release144(list_row144*r){for(unsigned j=0;j<16;++j)if((uintptr_t)r->text[j]!=UINT64_MAX)free8(r->text[j]);}
static void list_release144(control_state144*c){list_model144*m=c->model;if(!m)return;for(unsigned i=0;i<c->count;++i)list_row_release144(m->rows+i);for(unsigned i=0;i<32;++i)free8(m->labels[i]);free8(m->rows);}
static unsigned list_reserve144(list_model144*m,unsigned count){if(count>2048){last8(1816);return 0;}if(count<=m->capacity)return 1;unsigned cap=m->capacity?m->capacity*2:16;if(cap<count)cap=count;if(cap>2048)cap=2048;list_row144*rows=calloc8(cap,sizeof(*rows));if(!rows){last8(8);return 0;}if(m->rows)memcpy(rows,m->rows,m->capacity*sizeof(*rows));free8(m->rows);m->rows=rows;m->capacity=cap;return 1;}
static unsigned list_assign144(list_row144*r,const list_item144*in){if(in->subitem<0||in->subitem>=16||in->mask&~0xfu){last8(50);return 0;}if(in->mask&1){WCHAR**slot=r->text+in->subitem;if((uintptr_t)in->text==UINT64_MAX){if((uintptr_t)*slot!=UINT64_MAX)free8(*slot);*slot=in->text;}else{WCHAR*copy=0;if(!control_text144(&copy,in->text))return 0;if((uintptr_t)*slot!=UINT64_MAX)free8(*slot);*slot=copy;}}if(in->mask&2)r->image=in->image;if(in->mask&4)r->parameter=in->parameter;if(in->mask&8)r->state=(r->state&~in->state_mask)|(in->state&in->state_mask);return 1;}
static int64_t list_message144(ui_window_runtime144*w,control_state144*c,unsigned msg,uint64_t wp,int64_t lp,unsigned*handled){
 *handled=1;list_model144*m=c->model;if(!m){m=calloc8(1,sizeof(*m));if(!m)return 0;m->selection=-1;m->background=m->text_background=0xffffff;c->model=m;}
 if(msg==0x1003)return wp<4?(int64_t)m->images[wp]:0;
 if(msg==0x1002){if(wp>=4){last8(87);return 0;}HANDLE old=m->images[wp];m->images[wp]=(HANDLE)lp;return(int64_t)old;}
 if(msg==0x1037)return m->extended;
 if(msg==0x1036){unsigned old=m->extended;if(wp)m->extended=(old&~(unsigned)wp)|((unsigned)lp&(unsigned)wp);else m->extended=(unsigned)lp;return old;}
 if(msg==0x1004)return c->count;
 if(msg==0x104d){const list_item144*in=(void*)(uintptr_t)lp;if(!in||in->subitem||in->item<0||!list_reserve144(m,c->count+1))return -1;unsigned at=(unsigned)in->item;if(at>c->count)at=c->count;list_row144 row={0};if(!list_assign144(&row,in)){list_row_release144(&row);return -1;}memmove(m->rows+at+1,m->rows+at,(c->count-at)*sizeof(row));m->rows[at]=row;++c->count;return at;}
 if(msg==0x1008){if(wp>=c->count)return 0;list_row_release144(m->rows+wp);memmove(m->rows+wp,m->rows+wp+1,(c->count-(unsigned)wp-1)*sizeof(*m->rows));--c->count;memset(m->rows+c->count,0,sizeof(*m->rows));return 1;}
 if(msg==0x1009){for(unsigned i=0;i<c->count;++i)list_row_release144(m->rows+i);if(m->rows)memset(m->rows,0,m->capacity*sizeof(*m->rows));c->count=0;m->selection=-1;return 1;}
 if(msg==0x104c){const list_item144*in=(void*)(uintptr_t)lp;return in&&in->item>=0&&(unsigned)in->item<c->count?list_assign144(m->rows+in->item,in):0;}
 if(msg==0x104b){list_item144*out=(void*)(uintptr_t)lp;if(!out||out->item<0||(unsigned)out->item>=c->count||out->subitem<0||out->subitem>=16)return 0;list_row144*r=m->rows+out->item;if(out->mask&2)out->image=r->image;if(out->mask&4)out->parameter=r->parameter;if(out->mask&8)out->state=r->state&out->state_mask;if(out->mask&1){WCHAR*text=r->text[out->subitem];if((uintptr_t)text==UINT64_MAX){last8(50);return 0;}if(out->text&&out->capacity>0){unsigned n=wlen8(text);if(n>=(unsigned)out->capacity)n=(unsigned)out->capacity-1;if(n)memcpy(out->text,text,n*2);out->text[n]=0;}}return 1;}
 if(msg==0x102b){const list_item144*in=(void*)(uintptr_t)lp;if(!in)return 0;int index=(int)wp;if(index< -1||(index>=0&&(unsigned)index>=c->count))return 0;for(unsigned i=0;i<c->count;++i)if(index==-1||i==(unsigned)index)m->rows[i].state=(m->rows[i].state&~in->state_mask)|(in->state&in->state_mask);return 1;}
 if(msg==0x102c)return wp<c->count?m->rows[wp].state&(unsigned)lp:0;
 if(msg==0x1032){unsigned count=0;for(unsigned i=0;i<c->count;++i)count+=(m->rows[i].state&2)!=0;return count;}
 if(msg==0x100c){int start=(int)wp;unsigned required=(unsigned)lp&3;for(unsigned i=start<0?0:(unsigned)start+1;i<c->count;++i)if((m->rows[i].state&required)==required)return i;return -1;}
 if(msg==0x1042)return m->selection;
 if(msg==0x1043){int old=m->selection;if((int)lp>=-1&&((int)lp<0||(unsigned)lp<c->count))m->selection=(int)lp;return old;}
 if(msg==0x1061){const list_column144*in=(void*)(uintptr_t)lp;if(!in||wp>m->columns||m->columns==32)return -1;WCHAR*label=0;if((in->mask&4)&&!control_text144(&label,in->text))return -1;unsigned at=(unsigned)wp;memmove(m->column+at+1,m->column+at,(m->columns-at)*sizeof(*in));memmove(m->labels+at+1,m->labels+at,(m->columns-at)*sizeof(void*));m->column[at]=*in;m->column[at].text=label;m->labels[at]=label;++m->columns;return at;}
 if(msg==0x101c){if(wp>=m->columns)return 0;free8(m->labels[wp]);memmove(m->column+wp,m->column+wp+1,(m->columns-(unsigned)wp-1)*sizeof(*m->column));memmove(m->labels+wp,m->labels+wp+1,(m->columns-(unsigned)wp-1)*sizeof(void*));--m->columns;m->labels[m->columns]=0;return 1;}
 if(msg==0x101d)return wp<m->columns?m->column[wp].width:0;
 if(msg==0x101e){if(wp>=m->columns)return 0;if(lp<0){last8(50);return 0;}m->column[wp].width=(int)lp;return 1;}
 if(msg==0x1000)return m->background;
 if(msg==0x1001){m->background=(uint32_t)lp;return 1;}
 if(msg==0x1023)return m->text_color;
 if(msg==0x1024){m->text_color=(uint32_t)lp;return 1;}
 if(msg==0x1025)return m->text_background;
 if(msg==0x1026){m->text_background=(uint32_t)lp;return 1;}
 if(msg==0x1027)return m->top;
 if(msg==0x1028){win_rect144 r;return f_GetClientRect(w->handle,&r)?r.bottom/24:0;}
 if(msg==0x1013){if(wp>=c->count)return 0;m->top=(int)wp;return 1;}
 *handled=0;return 0;
}
