#ifndef ENGINE_UI_ICONS12_H
#define ENGINE_UI_ICONS12_H
#include <stdint.h>

/* Original 32-unit geometry. One temporary physical row, never an icon atlas. */
typedef struct { uint8_t kind,x,y,a,b,r,color; } ui12_shape;
#include <engine/ui/icons12_data.h>
#define ICON12_MAX_PHYSICAL 128u

static inline int ui12_shape_contains(const ui12_shape*s,int u,int v){
 int x=s->x*256,y=s->y*256,a=s->a*256,b=s->b*256;
 if(!s->kind){
  if(u<x||v<y||u>=x+a||v>=y+b)return 0;
  int radius=s->r*256;if(radius>a/2)radius=a/2;if(radius>b/2)radius=b/2;
  if(!radius)return 1;
  int cx=u<x+radius?x+radius:u>x+a-radius?x+a-radius:u;
  int cy=v<y+radius?y+radius:v>y+b-radius?y+b-radius:v;
  int64_t dx=u-cx,dy=v-cy;return dx*dx+dy*dy<=(int64_t)radius*radius;
 }
 int64_t dx=a-x,dy=b-y,px=u-x,py=v-y,len=dx*dx+dy*dy,dot=px*dx+py*dy;
 int64_t radius=s->r*128;
 if(!len||dot<=0)return px*px+py*py<=radius*radius;
 if(dot>=len){px=u-a;py=v-b;return px*px+py*py<=radius*radius;}
 int64_t cross=px*dy-py*dx;return cross*cross<=radius*radius*len;
}

static inline uint32_t ui12_icon_over(uint32_t old,uint32_t rgb,unsigned alpha){
 unsigned back=255-alpha,result=0;
 for(unsigned shift=0;shift<24;shift+=8)
  result|=(((((rgb>>shift)&255)*alpha+((old>>shift)&255)*back+127)/255)&255)<<shift;
 return result|(alpha+(((old>>24)*back+127)/255))<<24;
}

/* Premultiplied ARGB, independently composable over any existing surface. */
static inline void ui12_icon_row_custom(unsigned id,unsigned row,unsigned extent,unsigned dark,uint32_t ink,unsigned custom,uint32_t*out){
 if(!out||!extent||extent>ICON12_MAX_PHYSICAL)return;
 for(unsigned x=0;x<extent;++x)out[x]=0;
 if(row>=extent)return;
 if(id>=ICON12_COUNT)id=ICON12_UNKNOWN;
 for(unsigned index=icon12_offsets[id];index<icon12_offsets[id+1];++index){
  const ui12_shape*s=&icon12_shapes[index];
  int left=s->x*256,top=s->y*256,right=(s->x+s->a)*256,bottom=(s->y+s->b)*256;
  if(s->kind){left=(s->x<s->a?s->x:s->a)*256-s->r*128;right=(s->x>s->a?s->x:s->a)*256+s->r*128;top=(s->y<s->b?s->y:s->b)*256-s->r*128;bottom=(s->y>s->b?s->y:s->b)*256+s->r*128;}
  if((int)((row+1)*8192/extent)<=top||(int)(row*8192/extent)>=bottom)continue;
  int first=left*(int)extent/8192,last=(right*(int)extent+8191)/8192;
  if(first<0)first=0;if(last>(int)extent)last=extent;
  uint32_t rgb=custom&&s->color==6?(ink&0xffffff):icon12_palettes[dark!=0][s->color];
  for(int x=first;x<last;++x){
   unsigned covered=0;
   for(unsigned sy=0;sy<4;++sy)for(unsigned sx=0;sx<4;++sx)
    covered+=ui12_shape_contains(s,((x*8+(int)sx*2+1)*1024)/(int)extent,((row*8+sy*2+1)*1024)/extent);
   if(covered){
    unsigned alpha=(covered*255+8)/16;
    /* Monochrome caption cutouts remove coverage instead of painting paper. */
    if(custom&&s->color==7){uint32_t old=out[x],erased=0;for(unsigned shift=0;shift<32;shift+=8)erased|=((((old>>shift)&255)*(255-alpha)+127)/255)<<shift;out[x]=erased;}
    else out[x]=ui12_icon_over(out[x],rgb,alpha);
   }
  }
 }
}

static inline void ui12_icon_row(unsigned id,unsigned row,unsigned extent,unsigned dark,uint32_t*out){ui12_icon_row_custom(id,row,extent,dark,0,0,out);}
static inline void ui12_icon_row_ink(unsigned id,unsigned row,unsigned extent,unsigned dark,uint32_t ink,uint32_t*out){ui12_icon_row_custom(id,row,extent,dark,ink,1,out);}
void ui12_icon(unsigned,int,int,unsigned,unsigned);
void ui12_icon_ink(unsigned,int,int,unsigned,uint32_t);
#endif
