/* Measure once on insertion; pointer movement never issues font-measure syscalls. */
static int toolbar_measure145(const WCHAR*label){
 if(!label)return 0;unsigned n=wlen8(label);if(n>159){last8(206);return -1;}
 wui_draw144 draw={0};if(utf16_to8(label,draw.text,sizeof(draw.text))<0){last8(1113);return -1;}
 int64_t result=ui_call144(WUI_MEASURE144,0,&draw,0);if(result<0){last8((unsigned)-result);return -1;}
 return(int)(uint32_t)result;
}
static int toolbar_rect145(ui_window_runtime144*w,control_state144*c,unsigned index,win_rect144*out){
 toolbar144*t=c->model;if(!t||index>=c->count||(t->buttons[index].state&8)||!out)return 0;
 unsigned list=(w->description.style&0x1000)!=0,standard=t->width,height=t->height;
 for(unsigned n=0;n<c->count;++n)if(!(t->buttons[n].style&1)&&!(t->buttons[n].state&8)){
  unsigned width=t->label_width[n]+12+(list&&c->image?t->bitmap_width+6:0);
  if(width>standard)standard=width;
  unsigned needed=(c->image?t->bitmap_height:0)+(t->labels[n]?20:0)+8;
  if(list)needed=(t->bitmap_height>16?t->bitmap_height:16)+8;
  if(needed>height)height=needed;
 }
 int left=6;for(unsigned n=0;n<=index;++n){toolbar_button144*b=t->buttons+n;if(b->state&8)continue;
  unsigned width=b->style&1?(b->bitmap>0?(unsigned)b->bitmap:8):standard;
  if(!(b->style&1)&&(b->style&16)){width=t->label_width[n]+12+(list&&c->image?t->bitmap_width+6:0);if(width<t->width)width=t->width;}
  if(n==index){*out=(win_rect144){left,0,left+(int)width,(int)height};return 1;}left+=(int)width;
 }
 return 0;
}
static int toolbar_hit145(ui_window_runtime144*w,control_state144*c,int x,int y){
 for(unsigned n=0;n<c->count;++n){win_rect144 r;if(toolbar_rect145(w,c,n,&r)&&x>=r.left&&x<r.right&&y>=r.top&&y<r.bottom)return(int)n;}
 return -1;
}
