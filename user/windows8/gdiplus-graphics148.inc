/* Raster graphics contexts reference real bitmap storage; no rendering stubs. */
typedef struct {gp_bitmap148*image;HANDLE dc;int settings[4];} gp_graphics148;
static gp_graphics148*gp_contexts148[32];
static gp_graphics148*gp_context_find148(const void*pointer){for(unsigned i=0;i<32;++i)if(pointer&&gp_contexts148[i]==pointer)return gp_contexts148[i];return 0;}
static unsigned MS f_GdipGetImageGraphicsContext(void*pointer,void**output){
 if(!output||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)output,8,2,0,0))return 2;*output=0;
 lock_enter142(&gp_lock148);gp_bitmap148*image=gp_bitmap_find148(pointer);if(!image){lock_leave142(&gp_lock148);return 2;}
 unsigned slot=0;while(slot<32&&gp_contexts148[slot])++slot;if(slot==32){lock_leave142(&gp_lock148);return 3;}
 gp_graphics148*context=alloc8(sizeof(*context));if(!context){lock_leave142(&gp_lock148);return 3;}*context=(gp_graphics148){image,0,{0,3,0,1}};++image->contexts;gp_contexts148[slot]=context;*output=context;lock_leave142(&gp_lock148);return 0;
}
/* HDC storage stays borrowed. Queries and client clears use the actual native DC. */
static unsigned MS f_GdipCreateFromHDC(HANDLE dc,void**output){
 if(!output||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)output,8,2,0,0))return 2;*output=0;if(!dc||!dc_lookup144(dc))return 2;
 lock_enter142(&gp_lock148);if(!gp_references148){lock_leave142(&gp_lock148);return 18;}unsigned slot=0;while(slot<32&&gp_contexts148[slot])++slot;if(slot==32){lock_leave142(&gp_lock148);return 3;}gp_graphics148*context=alloc8(sizeof(*context));if(!context){lock_leave142(&gp_lock148);return 3;}*context=(gp_graphics148){0,dc,{0,3,0,1}};gp_contexts148[slot]=context;*output=context;lock_leave142(&gp_lock148);return 0;
}
static unsigned gp_dpi148(void*pointer,void*out,unsigned vertical){
 if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,4,2,0,0))return 2;lock_enter142(&gp_lock148);gp_graphics148*context=gp_context_find148(pointer);if(!context){lock_leave142(&gp_lock148);return 2;}if(context->dc&&f_GetDeviceCaps(context->dc,vertical?90:88)!=96){lock_leave142(&gp_lock148);return 2;}uint32_t dpi=0x42c00000u;memcpy(out,&dpi,4);lock_leave142(&gp_lock148);return 0;
}
static unsigned MS f_GdipGetDpiX(void*g,void*out){lock_enter142(&ui_lock144);unsigned status=gp_dpi148(g,out,0);lock_leave142(&ui_lock144);return status;}
static unsigned MS f_GdipGetDpiY(void*g,void*out){lock_enter142(&ui_lock144);unsigned status=gp_dpi148(g,out,1);lock_leave142(&ui_lock144);return status;}
static unsigned gp_setting148(void*pointer,unsigned index,int*value,unsigned write){
 if(!value||(!write&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)value,4,2,0,0)))return 2;
 int next=write?*value:0;if(write){if(index==1){if(next<0||next>5)return 2;if(next<2)next=3;else if(next==2)next=4;}else if(index==2){if(next<0||next>5)return 2;}else if(index==3&&(next<1||next>6))return 2;}
 lock_enter142(&gp_lock148);gp_graphics148*context=gp_context_find148(pointer);if(!context){lock_leave142(&gp_lock148);return 2;}if(write)context->settings[index]=next;else *value=context->settings[index];lock_leave142(&gp_lock148);return 0;
}
#define GP_SETTING148(name,index) static unsigned MS f_GdipSet##name(void*g,int value){return gp_setting148(g,index,&value,1);}static unsigned MS f_GdipGet##name(void*g,int*out){return gp_setting148(g,index,out,0);}
GP_SETTING148(CompositingQuality,0)
GP_SETTING148(SmoothingMode,1)
GP_SETTING148(TextRenderingHint,2)
GP_SETTING148(PageUnit,3)
#undef GP_SETTING148
static unsigned MS f_GdipDeleteGraphics(void*pointer){lock_enter142(&gp_lock148);gp_graphics148*context=gp_context_find148(pointer);if(!context){lock_leave142(&gp_lock148);return 2;}for(unsigned i=0;i<32;++i)if(gp_contexts148[i]==context){gp_contexts148[i]=0;break;}if(context->image)--context->image->contexts;free8(context);lock_leave142(&gp_lock148);return 0;}
static unsigned gp_clear148(void*pointer,unsigned color){
 lock_enter142(&gp_lock148);gp_graphics148*context=gp_context_find148(pointer);if(!context){lock_leave142(&gp_lock148);return 2;}if(context->dc){native_dc144*d=dc_lookup144(context->dc);if(!d){lock_leave142(&gp_lock148);return 2;}if(d->window_surface||d->window==DESKTOP_HANDLE148||(color>>24)!=255){lock_leave142(&gp_lock148);return 6;}wui_draw144 draw={.kind=1,.color=color&0xffffffu,.bounds={d->clip.left,d->clip.top,d->clip.right-d->clip.left,d->clip.bottom-d->clip.top}};int ok=draw_call144(d,&draw);lock_leave142(&gp_lock148);return ok?0:7;}
 gp_bitmap148*image=context->image;unsigned bpp=gp_pixel_bytes148(image->format);
 uint64_t pitch=image->stride<0?-(int64_t)image->stride:image->stride,base=(uint64_t)(uintptr_t)image->pixels;if(image->stride<0)base-=pitch*((unsigned)image->height-1);
 if(sys8(W8_SYS_ACCESS,base,pitch*(unsigned)image->height,2,0,0)){lock_leave142(&gp_lock148);return 2;}
 unsigned alpha=image->format==0x26200a?color>>24:255;
 for(int y=0;y<image->height;++y){uint8_t*row=image->pixels+(int64_t)y*image->stride;for(int x=0;x<image->width;++x){uint8_t*p=row+(size_t)x*bpp;p[0]=(uint8_t)color;p[1]=(uint8_t)(color>>8);p[2]=(uint8_t)(color>>16);if(bpp==4)p[3]=(uint8_t)alpha;}}
 lock_leave142(&gp_lock148);return 0;
}

/* All mixed DC/graphics operations acquire UI before graphics metadata. */
static unsigned MS f_GdipGraphicsClear(void*pointer,unsigned color){lock_enter142(&ui_lock144);unsigned status=gp_clear148(pointer,color);lock_leave142(&ui_lock144);return status;}
