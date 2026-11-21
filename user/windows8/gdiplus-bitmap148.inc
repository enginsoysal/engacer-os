/* Bounded process-owned GDI+ raster objects. External scan lines stay borrowed. */
typedef struct {int width,height,stride;unsigned format,owned,contexts;uint8_t*pixels;} gp_bitmap148;
static gp_bitmap148*gp_bitmaps148[32];
static gp_bitmap148*gp_bitmap_find148(const void*image){for(unsigned i=0;i<32;++i)if(image&&gp_bitmaps148[i]==image)return gp_bitmaps148[i];return 0;}
static unsigned gp_pixel_bytes148(unsigned format){return format==0x21808?3:format==0x22009||format==0x26200a?4:0;}
static unsigned MS f_GdipCreateBitmapFromScan0(int width,int height,int stride,unsigned format,uint8_t*scan,void**output){
 if(!output||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)output,8,2,0,0))return 2;*output=0;
 unsigned bpp=gp_pixel_bytes148(format);if(width<=0||height<=0||!bpp)return 2;
 uint64_t row=((uint64_t)(unsigned)width*bpp+3)&~UINT64_C(3);if(row>INT32_MAX)return 3;
 uint64_t pitch=scan?(stride<0?-(int64_t)stride:stride):row;
 if(scan&&(!stride||(stride&3)||pitch<row))return 2;
 if(pitch>24*1024*1024u||(uint64_t)(unsigned)height>24*1024*1024u/pitch)return 3;
 uint64_t bytes=pitch*(unsigned)height;
 if(scan){uint64_t base=(uint64_t)(uintptr_t)scan,offset=pitch*((unsigned)height-1);if(stride<0){if(base<offset)return 2;base-=offset;}if(sys8(W8_SYS_ACCESS,base,bytes,3,0,0))return 2;}
 lock_enter142(&gp_lock148);if(!gp_references148){lock_leave142(&gp_lock148);return 18;}unsigned slot=0;while(slot<32&&gp_bitmaps148[slot])++slot;if(slot==32){lock_leave142(&gp_lock148);return 3;}
 gp_bitmap148*image=alloc8(sizeof(*image));if(!image){lock_leave142(&gp_lock148);return 3;}
 uint8_t*pixels=scan?scan:calloc8(1,(size_t)bytes);if(!pixels){free8(image);lock_leave142(&gp_lock148);return 3;}
 *image=(gp_bitmap148){width,height,scan?stride:(int)row,format,scan==0,0,pixels};gp_bitmaps148[slot]=image;*output=image;lock_leave142(&gp_lock148);return 0;
}
static unsigned MS f_GdipDisposeImage(void*pointer){lock_enter142(&gp_lock148);gp_bitmap148*image=gp_bitmap_find148(pointer);if(!image){lock_leave142(&gp_lock148);return 2;}if(image->contexts){lock_leave142(&gp_lock148);return 4;}for(unsigned i=0;i<32;++i)if(gp_bitmaps148[i]==image){gp_bitmaps148[i]=0;break;}if(image->owned)free8(image->pixels);free8(image);lock_leave142(&gp_lock148);return 0;}
static unsigned gp_dimension148(void*pointer,unsigned*out,unsigned height){if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,4,2,0,0))return 2;lock_enter142(&gp_lock148);gp_bitmap148*image=gp_bitmap_find148(pointer);if(!image){lock_leave142(&gp_lock148);return 2;}*out=(unsigned)(height?image->height:image->width);lock_leave142(&gp_lock148);return 0;}
static unsigned MS f_GdipGetImageWidth(void*image,unsigned*out){return gp_dimension148(image,out,0);}
static unsigned MS f_GdipGetImageHeight(void*image,unsigned*out){return gp_dimension148(image,out,1);}
static unsigned gp_pixel148(void*pointer,int x,int y,unsigned*color,unsigned write){
 if(!color||(!write&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)color,4,2,0,0)))return 2;
 lock_enter142(&gp_lock148);gp_bitmap148*image=gp_bitmap_find148(pointer);if(!image||x<0||y<0||x>=image->width||y>=image->height){lock_leave142(&gp_lock148);return 2;}
 unsigned bpp=gp_pixel_bytes148(image->format);uint8_t*p=image->pixels+(int64_t)y*image->stride+(size_t)x*bpp;
 if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)p,bpp,write?2:1,0,0)){lock_leave142(&gp_lock148);return 2;}
 unsigned alpha=image->format==0x26200a;
 if(write){p[0]=(uint8_t)*color;p[1]=(uint8_t)(*color>>8);p[2]=(uint8_t)(*color>>16);if(bpp==4)p[3]=(uint8_t)(alpha?*color>>24:255);}
 else *color=((alpha?(unsigned)p[3]:255)<<24)|((unsigned)p[2]<<16)|((unsigned)p[1]<<8)|p[0];
 lock_leave142(&gp_lock148);return 0;
}
static unsigned MS f_GdipBitmapGetPixel(void*image,int x,int y,unsigned*color){return gp_pixel148(image,x,y,color,0);}
static unsigned MS f_GdipBitmapSetPixel(void*image,int x,int y,unsigned color){return gp_pixel148(image,x,y,&color,1);}
