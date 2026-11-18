/* Original M13.5 folded-light wallpaper. Integer spans, no image/cache/timer. */
static uint32_t blend15(uint32_t a,uint32_t b,unsigned weight){
 uint32_t out=0;for(unsigned shift=0;shift<=16;shift+=8){int x=(a>>shift)&255,y=(b>>shift)&255;out|=(uint32_t)(x+(y-x)*(int)weight/256)<<shift;}return out;
}
static void wallpaper15(desktop_rect dirty){
 uint32_t base=appearance11.wallpaper;unsigned pattern=appearance11.pattern;
 if(access_flags16&1){rectangle(dirty,0);return;}if(pattern==1){rectangle(dirty,base);return;}
 unsigned width=model.width,height=model.height;
 for(int row=dirty.y;row<dirty.y+dirty.height;++row){
  unsigned shade=(unsigned)row*(pattern==2?40u:24u)/height;uint32_t wash=blend15(base,0xffffff,shade);gui6_rect(0,(unsigned)row,width,1,wash);
  if(pattern!=0)continue;
  unsigned t=(unsigned)row*1024/height;
  for(unsigned layer=0;layer<3;++layer){
   int64_t fixed=(int64_t)width*(594+(int)layer*112)-(int64_t)width*t*t/4096;
   int edge=(int)(fixed/1024);if(edge<0)edge=0;if(edge>=(int)width||edge>=dirty.x+dirty.width)continue;
   uint32_t target=layer==1?0x91bac8:preferences.accent;
   uint32_t fold=blend15(wash,target,layer==0?40:layer==1?24:56);
   gui6_rect((unsigned)edge,(unsigned)row,width-(unsigned)edge,1,fold);
   unsigned fraction=(unsigned)(fixed&1023);gui6_rect((unsigned)edge,(unsigned)row,1,1,blend15(fold,wash,fraction/4));
  }
 }
}
static void snap_outline15(desktop_rect r){
 ui12_palette p=desktop_palette16();uint32_t border=(access_flags16&1)?p.ink:preferences.accent;
 rectangle((desktop_rect){r.x+6,r.y+6,r.width-12,2},border);rectangle((desktop_rect){r.x+6,r.y+r.height-8,r.width-12,2},border);rectangle((desktop_rect){r.x+6,r.y+6,2,r.height-12},border);rectangle((desktop_rect){r.x+r.width-8,r.y+6,2,r.height-12},border);
}
