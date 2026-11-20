/* Native input acts on original app rows; callbacks may replace the whole model. */
typedef struct {HANDLE window,id;unsigned code,pad;int item,subitem;unsigned new_state,old_state,changed;int x,y,pad2;int64_t parameter;unsigned keys,pad3;} list_notify145;
_Static_assert(sizeof(list_notify145)==72,"Win64 NMITEMACTIVATE layout");
static unsigned list_live145(HANDLE h,control_state144*c,list_model144*m){ui_window_runtime144*w=ui_window_lookup144(h);return w&&w->control==c&&c->model==m;}
static int64_t list_send145(HANDLE h,unsigned code,int item,unsigned old,unsigned next,int64_t parameter,int x,int y){ui_window_runtime144*w=ui_window_lookup144(h);if(!w||!w->description.parent)return 0;list_notify145 info={.window=h,.id=(HANDLE)w->id,.code=code,.item=item,.old_state=old,.new_state=next,.changed=old!=next?8u:0,.x=x,.y=y,.parameter=parameter};return f_SendMessageW(w->description.parent,0x4e,(HANDLE)w->id,(int64_t)(uintptr_t)&info);}
static int list_select145(HANDLE h,control_state144*c,list_model144*m,int index){
 if(m->sorting||m->input_depth>=8||index< -1||(index>=0&&(unsigned)index>=c->count)){last8(87);return -1;}++m->input_depth;int result=-1;unsigned changes=0;
 typedef struct {unsigned index,old,next,pad;int64_t parameter;} change145;change145*items=0;uint64_t revision=m->revision;
 for(unsigned n=0;n<c->count;++n){unsigned next=(m->rows[n].state&~3u)|((int)n==index?3u:0);changes+=next!=m->rows[n].state;}
 if(!changes){m->selection=index;result=1;goto done;}
 items=alloc8((size_t)changes*sizeof(*items));if(!items){last8(8);goto done;}unsigned at=0;
 for(unsigned n=0;n<c->count;++n){list_row144*r=m->rows+n;unsigned next=(r->state&~3u)|((int)n==index?3u:0);if(next!=r->state)items[at++]=(change145){.index=n,.old=r->state,.next=next,.parameter=r->parameter};}
 for(unsigned n=0;n<changes;++n){change145*i=items+n;int64_t veto=list_send145(h,(unsigned)-100,(int)i->index,i->old,i->next,i->parameter,0,0);if(!list_live145(h,c,m)||m->revision!=revision)goto done;if(veto){result=0;goto done;}}
 for(unsigned n=0;n<changes;++n)m->rows[items[n].index].state=items[n].next;m->selection=index;revision=++m->revision;f_InvalidateRect(h,0,0);result=1;
 for(unsigned n=0;n<changes;++n){change145*i=items+n;list_send145(h,(unsigned)-101,(int)i->index,i->old,i->next,i->parameter,0,0);if(!list_live145(h,c,m)||m->revision!=revision){result=-1;break;}}
done:free8(items);if(list_live145(h,c,m))--m->input_depth;return result;
}
static int list_hit145(ui_window_runtime144*w,control_state144*c,list_model144*m,int x,int y){win_rect144 rect;if(!f_GetClientRect(w->handle,&rect)||x<0||x>=rect.right)return -1;int top=m->columns?28:4;if(y<top||y>=rect.bottom)return -1;int row=m->top+(y-top)/24;return row>=0&&(unsigned)row<c->count?row:-1;}
static void list_activate145(HANDLE h,control_state144*c,list_model144*m,int row,unsigned code,int x,int y){if(row<0||(unsigned)row>=c->count)return;uint64_t revision=m->revision;int64_t parameter=m->rows[row].parameter;list_send145(h,code,row,0,0,parameter,x,y);if(list_live145(h,c,m)&&m->revision==revision)list_send145(h,(unsigned)-114,row,0,0,parameter,x,y);}
static int64_t list_input145(ui_window_runtime144*w,control_state144*c,unsigned message,uint64_t wp,int64_t lp,unsigned*handled){
 *handled=1;list_model144*m=c->model;HANDLE h=w->handle;if(!m){*handled=0;return 0;}
 if(message==7||message==8){list_send145(h,message==7?(unsigned)-7:(unsigned)-8,-1,0,0,0,0,0);return 0;}
 if(message==0x215){m->pressed=-1;return 0;}
 if(message==0x201){if(!w->description.enabled)return 0;f_SetFocus(h);if(!list_live145(h,c,m))return 0;int x=(int16_t)(lp&65535),y=(int16_t)((uint64_t)lp>>16),row=list_hit145(w,c,m,x,y);int result=list_select145(h,c,m,row);if(result<0||!list_live145(h,c,m))return 0;m->pressed=row;m->press_revision=m->revision;f_SetCapture(h);return 0;}
 if(message==0x202){int row=m->pressed;m->pressed=-1;uint64_t revision=m->press_revision;int x=(int16_t)(lp&65535),y=(int16_t)((uint64_t)lp>>16);if(f_GetCapture()==h)f_ReleaseCapture();if(!list_live145(h,c,m)||m->revision!=revision||row<0||row!=list_hit145(w,c,m,x,y))return 0;
  int64_t parameter=m->rows[row].parameter;list_send145(h,(unsigned)-2,row,0,0,parameter,x,y);if(!list_live145(h,c,m)||m->revision!=revision)return 0;
  unsigned now=f_GetTickCount();int dx=x-m->last_x,dy=y-m->last_y;unsigned double_=m->last_tick&&m->last_item==row&&(unsigned)(now-m->last_tick)<=500&&dx>=-4&&dx<=4&&dy>=-4&&dy<=4;
  m->last_tick=double_?0:now;m->last_item=row;m->last_x=x;m->last_y=y;if(double_&&(m->rows[row].state&2))list_activate145(h,c,m,row,(unsigned)-3,x,y);return 0;
 }
 if(message==0x100){uint64_t revision=m->revision;struct __attribute__((packed)) {HANDLE window,id;unsigned code,pad;uint16_t key;unsigned flags;} key={h,(HANDLE)w->id,(unsigned)-155,0,(uint16_t)wp,0};_Static_assert(sizeof(key)==30,"Packed Win64 NMLVKEYDOWN layout");f_SendMessageW(w->description.parent,0x4e,(HANDLE)w->id,(int64_t)(uintptr_t)&key);if(!list_live145(h,c,m)||m->revision!=revision)return 0;
  if(wp==13){list_activate145(h,c,m,m->selection,(unsigned)-4,0,0);return 0;}
  if(wp==0x26||wp==0x28||wp==0x24||wp==0x23){if(!c->count)return 0;int row=wp==0x24?0:wp==0x23?(int)c->count-1:m->selection+(wp==0x26?-1:1);if(row<0)row=0;if((unsigned)row>=c->count)row=(int)c->count-1;
   if(list_select145(h,c,m,row)>0&&list_live145(h,c,m)){win_rect144 rect;f_GetClientRect(h,&rect);int rows=(rect.bottom-(m->columns?28:4))/24;if(rows<1)rows=1;if(row<m->top)m->top=row;if(row>=m->top+rows)m->top=row-rows+1;f_InvalidateRect(h,0,0);}return 0;
  }return 0;
 }
 *handled=0;return 0;
}
