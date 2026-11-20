/* Image objects remain private; only bounded copied ARGB tiles reach the kernel. */
static int image_pixels145(native_dc144*dc,int x,int y,unsigned width,unsigned height,const uint32_t*pixels,unsigned source_width,unsigned source_height){
 if(!width||!height||width>256||height>256||!pixels||!source_width||!source_height){last8(87);return 0;}
 if(x< -32768||y< -32768||(int64_t)x+width>32767||(int64_t)y+height>32767){last8(87);return 0;}
 for(unsigned top=0;top<height;top+=8)for(unsigned left=0;left<width;left+=16){
  unsigned w=width-left<16?width-left:16,h=height-top<8?height-top:8;
  wui_draw144 draw={.kind=4,.bounds={x+(int)left,y+(int)top,(int)w,(int)h}};
  for(unsigned row=0;row<h;++row)for(unsigned col=0;col<w;++col){
   unsigned sx=(left+col)*source_width/width,sy=(top+row)*source_height/height;
   draw.pixels[row*w+col]=pixels[sy*source_width+sx];
  }
  if(!draw_call144(dc,&draw))return 0;
 }
 return 1;
}
static int MS f_ImageList_Draw(HANDLE list,int index,HANDLE dc,int x,int y,unsigned flags){
 native_dc144*d=dc_lookup144(dc);if(!d)return 0;if(flags&~1u){last8(50);return 0;}
 lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);
 if(!p||index<0||(unsigned)index>=p->count){lock_leave142(&image_lock144);last8(87);return 0;}
 int result=image_pixels145(d,x,y,p->width,p->height,p->items[index],p->width,p->height);
 lock_leave142(&image_lock144);return result;
}
static int MS f_DrawIconEx(HANDLE dc,int x,int y,HANDLE icon,int width,int height,unsigned step,HANDLE background,unsigned flags){
 native_dc144*d=dc_lookup144(dc);if(!d)return 0;
 if(step||background||(flags!=2&&flags!=3)){last8(50);return 0;}
 lock_enter142(&image_lock144);image_object144*p=image_find144(icon,1);
 if(!p){lock_leave142(&image_lock144);return 0;}
 if(!width)width=(int)p->width;if(!height)height=(int)p->height;
 int result=width>0&&height>0?image_pixels145(d,x,y,(unsigned)width,(unsigned)height,p->pixels,p->width,p->height):0;
 if(width<0||height<0)last8(87);lock_leave142(&image_lock144);return result;
}
static int MS f_DrawIcon(HANDLE dc,int x,int y,HANDLE icon){return f_DrawIconEx(dc,x,y,icon,0,0,0,0,3);}
