/* Common-control content is drawn from its actual app-owned model. */
static void control_label144(HANDLE dc,int x,int y,const WCHAR*text){if(!text||(uintptr_t)text==UINT64_MAX)return;unsigned n=0;while(n<159&&text[n])++n;if(n)f_TextOutW(dc,x,y,text,(int)n);}
static void control_label_clip145(HANDLE dc,int x,int y,const WCHAR*label,win_rect144 cell){
 native_dc144*d=dc_lookup144(dc);if(!d)return;win_rect144 old=d->clip;
 if(cell.left>d->clip.left)d->clip.left=cell.left;if(cell.top>d->clip.top)d->clip.top=cell.top;
 if(cell.right<d->clip.right)d->clip.right=cell.right;if(cell.bottom<d->clip.bottom)d->clip.bottom=cell.bottom;
 if(d->clip.left<d->clip.right&&d->clip.top<d->clip.bottom)control_label144(dc,x,y,label);d->clip=old;
}
static void control_cell_label145(HANDLE dc,int minimum,int y,const WCHAR*label,win_rect144 cell,unsigned format){int x=minimum,size[2];unsigned align=format&3,n=wlen8(label);if((align==1||align==2)&&n&&f_GetTextExtentPoint32W(dc,label,(int)n,size)){x=align==1?cell.right-8-size[0]:cell.left+(cell.right-cell.left-size[0])/2;if(x<minimum)x=minimum;}control_label_clip145(dc,x,y,label,cell);}
static void control_paint144(HANDLE h,control_state144*c){native_paint144 paint;HANDLE dc=f_BeginPaint(h,&paint);if(!dc)return;
#ifdef ENGINE_M14
 if(c->font&&!f_SelectObject(dc,c->font)){f_EndPaint(h,&paint);return;}
#endif
 native_dc144*d=dc_lookup144(dc);
 ui_window_runtime144*w=ui_window_lookup144(h);if(!w||!d){f_EndPaint(h,&paint);return;}win_rect144 client=d->clip;HANDLE brush=6;f_SetBkMode(dc,1);
 ui_window_runtime144*parent=ui_window_lookup144(w->description.parent);if(c->kind==C144_STATIC&&parent&&!f_wcscmp(parent->class_->name,u"#32770"))brush=16;
 unsigned color_message=c->kind==C144_STATIC?0x138:c->kind==C144_EDIT?0x133:c->kind==C144_BUTTON?0x135:c->kind==C144_LISTBOX?0x134:0;
 if(parent&&color_message){HANDLE requested=(HANDLE)f_SendMessageW(parent->handle,color_message,dc,(int64_t)h);w=ui_window_lookup144(h);d=dc_lookup144(dc);if(!w||!d||!w->control){f_EndPaint(h,&paint);return;}c=w->control;if(requested>=1&&requested<=31)brush=requested;}
 f_FillRect(dc,&client,brush);
#ifdef ENGINE_M14
 if(c->kind==C144_PROGRESS){progress_paint148(d,c,&client,w->description.style);f_EndPaint(h,&paint);return;}
#endif
 if(c->kind==C144_LISTVIEW&&c->model){list_model144*m=c->model;int x=0;
  for(unsigned order=0;order<m->columns&&x<client.right;++order){unsigned col=0;while(col<m->columns&&m->column[col].order!=(int)order)++col;if(col==m->columns)continue;int width=m->column[col].width>0?m->column[col].width:160;control_cell_label145(dc,x+8,4,m->labels[col],(win_rect144){x,0,x+width,28},(unsigned)m->column[col].format);x+=width;}
  int y=m->columns?28:4;for(unsigned row=(unsigned)m->top;row<c->count&&y+16<=client.bottom;row++,y+=24){list_row144*r=m->rows+row;unsigned selected=(r->state&2)!=0;if(selected){win_rect144 highlight={0,y-2,client.right,y+20};f_FillRect(dc,&highlight,14);}f_SetTextColor(dc,selected?0xffffff:m->text_color);x=0;
   unsigned columns=m->columns?m->columns:1;for(unsigned order=0;order<columns&&x<client.right;++order){unsigned col=0;if(m->columns){while(col<m->columns&&m->column[col].order!=(int)order)++col;if(col==m->columns)continue;}int width=m->columns&&m->column[col].width>0?m->column[col].width:160;win_rect144 cell={x,y-2,x+width,y+22};if(col>=16){x+=width;continue;}
    WCHAR buffer[160];unsigned length,status=list_read_text145(h,c,m,row,col,buffer,160,&length);if(status!=1){f_EndPaint(h,&paint);if(status==2&&f_IsWindow(h))f_InvalidateRect(h,0,1);return;}w=ui_window_lookup144(h);r=m->rows+row;const WCHAR*label=buffer;
    int label_x=x+8;if(!col&&m->images[1]&&r->image>=0){unsigned iw,ih;if(image_size145(m->images[1],3,&iw,&ih)&&iw<=256&&ih<=24){native_dc144*current=dc_lookup144(dc);win_rect144 old=current->clip;if(cell.right<current->clip.right)current->clip.right=cell.right;f_ImageList_Draw(m->images[1],r->image,dc,x+8,y+(16-(int)ih)/2,1);current->clip=old;label_x+=(int)iw+6;}}
    control_cell_label145(dc,label_x,y,label,cell,m->columns?(unsigned)m->column[col].format:0);x+=width;
   }
  }
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
 }else if(c->kind==C144_BUTTON){
  WCHAR caption[160];unsigned used=0;for(unsigned i=0;i<159&&w->description.title[i];++i){WCHAR ch=w->description.title[i];if(ch=='&'&&w->description.title[i+1])ch=w->description.title[++i];caption[used++]=ch;}caption[used]=0;
  unsigned type=w->description.style&15;f_FillRect(dc,&client,type==1?14:17);
  win_rect144 inside={type==1?2:1,type==1?2:1,client.right-(type==1?2:1),client.bottom-(type==1?2:1)};f_FillRect(dc,&inside,c->selected>=0?17:16);
  int size[2]={0,16};unsigned length=used;f_GetTextExtentPoint32W(dc,caption,(int)length,size);f_SetTextColor(dc,w->description.enabled?0:0x808080);
#ifdef ENGINE_M14
  int group_width=size[0]+((c->style&1)&&c->image?24:0),label_x=(client.right-group_width)/2;if((c->style&1)&&c->image){f_DrawIconEx(dc,label_x,(client.bottom-16)/2,c->image,16,16,0,0,3);label_x+=24;}control_label_clip145(dc,label_x,(client.bottom-size[1])/2,caption,client);
#else
  control_label_clip145(dc,(client.right-size[0])/2,(client.bottom-size[1])/2,caption,client);
#endif
 }else if(c->kind==C144_STATIC&&c->image){unsigned width,height;if(image_size145(c->image,1,&width,&height)){unsigned style=w->description.style;int x=0,y=0;
  if(style&0x200){x=(client.right-(int)width)/2;y=(client.bottom-(int)height)/2;}
  else if(style&0x40){width=(unsigned)client.right;height=(unsigned)client.bottom;}
  if(width&&height)f_DrawIconEx(dc,x,y,c->image,(int)width,(int)height,0,0,3);}
 }else if(c->kind==C144_STATIC){unsigned type=w->description.style&31;int size[2]={0,16};unsigned n=wlen8(w->description.title);if(n>159)n=159;f_GetTextExtentPoint32W(dc,w->description.title,(int)n,size);
  int x=type==1?(client.right-size[0])/2:type==2?client.right-size[0]:0,y=w->description.style&0x200?(client.bottom-size[1])/2:0;control_label_clip145(dc,x,y,w->description.title,client);
 }else if(c->kind==C144_EDIT)control_label144(dc,4,4,c->texts[0]);
 else control_label144(dc,4,4,w->description.title);
 f_EndPaint(h,&paint);
}
