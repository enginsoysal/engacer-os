/* Checked process-private image-list operations; no foreign graphics pointers. */
static int MS f_ImageList_GetIconSize(HANDLE list,int*width,int*height){
 if(!width||!height){last8(87);return 0;}lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);if(p){*width=(int)p->width;*height=(int)p->height;}lock_leave142(&image_lock144);return p!=0;
}
static int MS f_ImageList_Remove(HANDLE list,int index){
 lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);if(!p||index< -1||(index>=0&&(unsigned)index>=p->count)){lock_leave142(&image_lock144);if(p)last8(87);return 0;}
 size_t bytes=(size_t)p->width*p->height*4;if(index<0){for(unsigned n=0;n<p->count;++n){image_free144(p->items[n],bytes);p->items[n]=0;}p->count=0;}
 else{unsigned at=(unsigned)index;image_free144(p->items[at],bytes);memmove(p->items+at,p->items+at+1,(p->count-at-1)*sizeof(void*));p->items[--p->count]=0;}
 lock_leave142(&image_lock144);return 1;
}
static int MS f_ImageList_SetIconSize(HANDLE list,int width,int height){
 if(width<=0||height<=0||width>1024||height>1024){last8(87);return 0;}
 lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);if(!p){lock_leave142(&image_lock144);return 0;}
 size_t bytes=(size_t)p->width*p->height*4;for(unsigned n=0;n<p->count;++n){image_free144(p->items[n],bytes);p->items[n]=0;}p->count=0;p->width=(unsigned)width;p->height=(unsigned)height;lock_leave142(&image_lock144);return 1;
}
static uint32_t image_over145(uint32_t foreground,uint32_t background){unsigned alpha=foreground>>24;uint32_t result=0xff000000u;for(unsigned shift=0;shift<24;shift+=8)result|=((((foreground>>shift)&255)*alpha+((background>>shift)&255)*(255-alpha)+127)/255)<<shift;return result;}
static HANDLE MS f_ImageList_GetIcon(HANDLE list,int index,unsigned flags){
 if(flags&~1u){last8(50);return 0;}lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);if(!p||index<0||(unsigned)index>=p->count){lock_leave142(&image_lock144);if(p)last8(87);return 0;}
 image_object144*icon=image_new144(1,p->width,p->height);if(!icon){lock_leave142(&image_lock144);return 0;}size_t bytes=(size_t)p->width*p->height*4;icon->pixels=image_memory144(bytes);if(!icon->pixels){image_destroy144(icon);lock_leave142(&image_lock144);return 0;}
 memcpy(icon->pixels,p->items[index],bytes);if(!(flags&1)&&p->background!=UINT32_MAX){uint32_t color=((p->background&255)<<16)|(p->background&0xff00)|((p->background>>16)&255);for(unsigned n=0;n<p->width*p->height;++n)icon->pixels[n]=image_over145(icon->pixels[n],color);}
 HANDLE result=icon->handle;lock_leave142(&image_lock144);return result;
}
static uint32_t MS f_ImageList_SetBkColor(HANDLE list,uint32_t color){
 if((color&0xff000000u)&&color!=UINT32_MAX){last8(50);return UINT32_MAX;}
 lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);uint32_t old=p?p->background:UINT32_MAX;if(p)p->background=color;lock_leave142(&image_lock144);return old;
}
static uint32_t MS f_ImageList_GetBkColor(HANDLE list){
 lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);uint32_t color=p?p->background:UINT32_MAX;lock_leave142(&image_lock144);return color;
}
static int MS f_ImageList_Add(HANDLE list,HANDLE bitmap,HANDLE mask){
 lock_enter142(&image_lock144);image_object144*p=image_find144(list,3),*source=image_find144(bitmap,2),*bits=p&&(p->resource&1)&&mask?image_find144(mask,2):0;
 if(!p||!source||(p&&(p->resource&1)&&mask&&!bits)||source->height<p->height||source->width%p->width||(bits&&(bits->width<source->width||bits->height<p->height))){lock_leave142(&image_lock144);last8(87);return -1;}
 unsigned count=source->width/p->width,first=p->count;if(!count||!image_capacity144(p,first+count)){lock_leave142(&image_lock144);return -1;}size_t bytes=(size_t)p->width*p->height*4;unsigned done=0;
 for(;done<count;++done){uint32_t*copy=image_memory144(bytes);if(!copy)break;for(unsigned y=0;y<p->height;++y)for(unsigned x=0;x<p->width;++x){unsigned at=y*source->width+done*p->width+x;uint32_t value=source->pixels[at];if(bits){unsigned transparent=(bits->pixels[y*bits->width+done*p->width+x]&0xffffffu)!=0;value=transparent?value&0xffffffu:value|0xff000000u;}copy[y*p->width+x]=value;}p->items[first+done]=copy;}
 if(done!=count){while(done){--done;image_free144(p->items[first+done],bytes);p->items[first+done]=0;}lock_leave142(&image_lock144);return -1;}p->count+=count;lock_leave142(&image_lock144);return(int)first;
}
/* Drag services and atlas bitmap exposure are explicitly unavailable. */
static int MS f_ImageList_BeginDrag(HANDLE list,int index,int x,int y){(void)x;(void)y;lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);unsigned valid=p&&index>=0&&(unsigned)index<p->count;lock_leave142(&image_lock144);last8(valid?50:87);return 0;}
static int MS f_ImageList_DragEnter(HANDLE window,int x,int y){(void)x;(void)y;if(window&&!f_IsWindow(window)){last8(1400);return 0;}last8(50);return 0;}
static int MS f_ImageList_DragMove(int x,int y){(void)x;(void)y;last8(50);return 0;}
static int MS f_ImageList_DragShowNolock(int show){(void)show;last8(50);return 0;}
static void MS f_ImageList_EndDrag(void){/* BeginDrag never creates an active operation. */last8(50);}
static int MS f_ImageList_GetImageInfo(HANDLE list,int index,void*out){
 lock_enter142(&image_lock144);image_object144*p=image_find144(list,3);unsigned valid=p&&index>=0&&(unsigned)index<p->count&&out;lock_leave142(&image_lock144);last8(valid?50:87);return 0;
}
