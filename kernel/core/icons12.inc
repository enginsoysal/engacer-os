/* Physical-density antialiasing with 512 bytes of bounded transient row state. */
static uint64_t icon12_draws,icon12_pixels,icon12_fallbacks;
static unsigned icon12_max_physical;
void ui12_icon(unsigned id,int x,int y,unsigned size,unsigned dark){
 if(size<8||size>64)return;
 if(id>=ICON12_COUNT)id=ICON12_UNKNOWN;
 if(!id)++icon12_fallbacks;
 int left=signed_phys92(x),top=signed_phys92(y);
 unsigned extent=(unsigned)(signed_phys92((int64_t)x+size)-left);
 if(!extent||extent>ICON12_MAX_PHYSICAL)return;
 int first_x=left<0?0:left,first_y=top<0?0:top;
 int last_x=left+(int)extent,last_y=top+(int)extent;
 if(last_x>(int)screen->framebuffer_width)last_x=screen->framebuffer_width;
 if(last_y>(int)screen->framebuffer_height)last_y=screen->framebuffer_height;
 if(clip7_active){
  int a=signed_phys92((int32_t)clip7_left),b=signed_phys92((int32_t)clip7_top),c=signed_phys92((int32_t)clip7_right),d=signed_phys92((int32_t)clip7_bottom);
  if(first_x<a)first_x=a;if(first_y<b)first_y=b;if(last_x>c)last_x=c;if(last_y>d)last_y=d;
 }
 if(first_x>=last_x||first_y>=last_y)return;
 ++icon12_draws;if(extent>icon12_max_physical)icon12_max_physical=extent;
 graphics9_dirty(first_x,first_y,last_x-first_x,last_y-first_y);
 uint32_t row[ICON12_MAX_PHYSICAL];
 for(int py=first_y;py<last_y;++py){
  ui12_icon_row(id,py-top,extent,dark,row);
  for(int px=first_x;px<last_x;++px){
   uint32_t pixel=row[px-left];unsigned alpha=pixel>>24;if(!alpha)continue;
   uint32_t rgb=0;for(unsigned shift=0;shift<24;shift+=8){unsigned value=(((pixel>>shift)&255)*255+alpha/2)/alpha;if(value>255)value=255;rgb|=value<<shift;}
   blend73(px,py,rgb,alpha,0);++icon12_pixels;
  }
 }
}
