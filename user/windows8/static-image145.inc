/* Static icon handles remain app-owned; stock resource loads use shared icons. */
static unsigned static_icon145(ui_window_runtime144*w,control_state144*c,HANDLE icon){
 unsigned width=0,height=0;if(icon&&!image_size145(icon,1,&width,&height))return 0;
 HANDLE h=w->handle;c->image=icon;unsigned style=w->description.style;
 if(icon&&!(style&(0x200|0x40))){int x=w->description.bounds.x,y=w->description.bounds.y;
  if(style&0x400){x+=w->description.bounds.width-(int)width;y+=w->description.bounds.height-(int)height;}
  if(!f_MoveWindow(h,x,y,(int)width,(int)height,1))return 0;
 }
 if(f_IsWindow(h))f_InvalidateRect(h,0,1);return 1;
}
static int64_t static_message145(ui_window_runtime144*w,control_state144*c,unsigned message,uint64_t wp,int64_t lp,unsigned*handled){
 *handled=1;
 if(message==1&&(w->description.style&31)==3){
  const struct {void*parameter;HANDLE instance,menu,parent;int cy,cx,y,x;unsigned style,pad;const WCHAR*name,*class_name;unsigned exstyle,pad2;}*creation=(const void*)(uintptr_t)lp;
  if(!creation||!creation->name)return 0;
  HANDLE icon=f_LoadImageW(creation->instance,creation->name,1,0,0,(w->description.style&0x800)?0x8000:0x8040);
  return icon&&static_icon145(w,c,icon)?0:-1;
 }
 if(message==0x170||message==0x172){if((w->description.style&31)!=3||(message==0x172&&wp!=1)){last8(50);return 0;}HANDLE old=c->image;return static_icon145(w,c,message==0x170?wp:(HANDLE)lp)?(int64_t)old:0;}
 if(message==0x171||message==0x173){if(message==0x173&&wp!=1){last8(50);return 0;}return(int64_t)c->image;}
 *handled=0;return 0;
}
