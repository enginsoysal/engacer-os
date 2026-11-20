/* Common-control content is drawn from its actual app-owned model. */
static void control_label144(HANDLE dc,int x,int y,const WCHAR*text){if(!text||(uintptr_t)text==UINT64_MAX)return;unsigned n=0;while(n<159&&text[n])++n;if(n)f_TextOutW(dc,x,y,text,(int)n);}
static void control_label_clip145(HANDLE dc,int x,int y,const WCHAR*label,win_rect144 cell){
 native_dc144*d=dc_lookup144(dc);if(!d)return;win_rect144 old=d->clip;
 if(cell.left>d->clip.left)d->clip.left=cell.left;if(cell.top>d->clip.top)d->clip.top=cell.top;
 if(cell.right<d->clip.right)d->clip.right=cell.right;if(cell.bottom<d->clip.bottom)d->clip.bottom=cell.bottom;
 if(d->clip.left<d->clip.right&&d->clip.top<d->clip.bottom)control_label144(dc,x,y,label);d->clip=old;
}
static void control_paint144(HANDLE h,control_state144*c){native_paint144 paint;HANDLE dc=f_BeginPaint(h,&paint);if(!dc)return;native_dc144*d=dc_lookup144(dc);win_rect144 client;f_GetClientRect(h,&client);wui_draw144 clear={.kind=3};if(!draw_call144(d,&clear)){f_EndPaint(h,&paint);return;}f_FillRect(dc,&client,6);f_SetBkMode(dc,1);
 ui_window_runtime144*w=ui_window_lookup144(h);if(!w){f_EndPaint(h,&paint);return;}
 if(c->kind==C144_LISTVIEW&&c->model){list_model144*m=c->model;int x=8;for(unsigned col=0;col<m->columns&&x<client.right;++col){control_label144(dc,x,4,m->labels[col]);x+=m->column[col].width>0?m->column[col].width:160;}
  int y=m->columns?28:4;for(unsigned row=(unsigned)m->top;row<c->count&&y+16<=client.bottom;row++,y+=24){list_row144*r=m->rows+row;if(r->state&2){win_rect144 selected={0,y-2,client.right,y+20};f_FillRect(dc,&selected,14);f_SetTextColor(dc,0xffffff);}else f_SetTextColor(dc,0);x=8;unsigned columns=m->columns?m->columns:1;for(unsigned col=0;col<columns&&col<16&&x<client.right;++col){WCHAR*label=r->text[col];WCHAR buffer[160];if((uintptr_t)label==UINT64_MAX){struct {HANDLE window,id;unsigned code,pad;list_item144 item;} notification={0};notification.window=h;notification.id=(HANDLE)w->id;notification.code=(unsigned)-177;notification.item=(list_item144){.mask=1,.item=(int)row,.subitem=(int)col,.text=buffer,.capacity=160,.parameter=r->parameter};buffer[0]=0;f_SendMessageW(w->description.parent,0x4e,(HANDLE)w->id,(int64_t)(uintptr_t)&notification);ui_window_runtime144*live=ui_window_lookup144(h);if(!live){f_EndPaint(h,&paint);return;}w=live;c=w->control;m=c?c->model:0;if(!m||row>=c->count){f_EndPaint(h,&paint);return;}r=m->rows+row;label=notification.item.text;}control_label144(dc,x,y,label);x+=m->columns&&m->column[col].width>0?m->column[col].width:160;}}
 }else if(c->kind==C144_TOOLBAR&&c->model){toolbar144*t=c->model;f_FillRect(dc,&client,16);
  for(unsigned n=0;n<c->count;++n){toolbar_button144*b=t->buttons+n;win_rect144 cell;if(!toolbar_rect145(w,c,n,&cell)||cell.left>=client.right)continue;
   if(b->style&1){win_rect144 line={cell.left+(cell.right-cell.left)/2,4,cell.left+(cell.right-cell.left)/2+1,cell.bottom-4};f_FillRect(dc,&line,17);continue;}
   if(t->pressed==(int)n||(b->state&1)){win_rect144 selected={cell.left+1,cell.top+1,cell.right-1,cell.bottom-1};f_FillRect(dc,&selected,17);}
   int list=(w->description.style&0x1000)!=0,icon=c->image&&b->bitmap>=0;
   int tx=cell.left+(cell.right-cell.left-(int)t->label_width[n])/2,ty=4+(icon?(int)t->bitmap_height+4:0);
   if(icon){int ix=list?cell.left+6:cell.left+(cell.right-cell.left-(int)t->bitmap_width)/2;int iy=list?(cell.bottom-(int)t->bitmap_height)/2:4;f_ImageList_Draw(c->image,b->bitmap,dc,ix,iy,1);}
   if(list){tx=cell.left+6+(icon?(int)t->bitmap_width+6:0);ty=(cell.bottom-16)/2;}
   f_SetTextColor(dc,b->state&4?0:0x808080);control_label_clip145(dc,tx,ty,t->labels[n],cell);
  }
 }else if(c->kind==C144_STATUS){int x=6;for(unsigned n=0;n<c->parts&&n<16&&x<client.right;++n){control_label144(dc,x,4,c->texts[n]);if(c->edges[n]<0)break;x=c->edges[n]+6;}
 }else if(c->kind==C144_EDIT)control_label144(dc,4,4,c->texts[0]);
 else control_label144(dc,4,4,w->description.title);
 f_EndPaint(h,&paint);
}
