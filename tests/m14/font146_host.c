#include "font73.h"
#include <engine/ui/font146.h>
void*memset(void*out,int value,size_t count){volatile uint8_t*p=out;for(size_t n=0;n<count;++n)p[n]=(uint8_t)value;return out;}
void*memcpy(void*out,const void*in,size_t count){uint8_t*p=out;const uint8_t*q=in;for(size_t n=0;n<count;++n)p[n]=q[n];return out;}
__declspec(dllexport) const char*license146(void){return font73_license;}
__declspec(dllexport) unsigned raster146(unsigned extra,unsigned index,uint8_t*out,unsigned capacity,int*metrics){
 const font73_glyph*g;unsigned base=65535;
 if(extra){if(index>=sizeof(font146_extras)/sizeof(font146_extras[0]))return 0;g=&font146_extras[index].glyph;base=font146_extras[index].base;}
 else{if(index>=sizeof(font73_glyphs)/sizeof(font73_glyphs[0]))return 0;g=font73_glyphs+index;}
 unsigned count=(unsigned)g->width*g->height;if(count>capacity)return 0;
 metrics[0]=g->width;metrics[1]=g->height;metrics[2]=g->x;metrics[3]=g->y;metrics[4]=g->advance;metrics[5]=(int)base;
 font146_sampler sampler=font146_sample_begin(g,base);unsigned at=0;
 for(unsigned y=0;y<g->height;++y)for(unsigned x=0;x<g->width;++x)out[at++]=(uint8_t)font146_sample(&sampler,x,y);
 return font146_complete(&sampler.delta)&&!sampler.base.bad;
}
__declspec(dllexport) unsigned lookup146(unsigned face,unsigned scalar,int*metrics){
 if(face>=sizeof(font73_faces)/sizeof(font73_faces[0]))return 0;unsigned base;const font73_glyph*g=font146_lookup(font73_faces+face,scalar,&base);
 metrics[0]=g->width;metrics[1]=g->height;metrics[2]=g->x;metrics[3]=g->y;metrics[4]=g->advance;metrics[5]=(int)base;return 1;
}
__declspec(dllexport) unsigned scalars146(const char*text,unsigned bytes,uint32_t*out,unsigned*positions,unsigned capacity){
 unsigned count=0,at=0;while(at<bytes&&text[at]){if(count>=capacity)return 0;unsigned before=at;out[count]=font146_next(text,&at,bytes);if(at<=before||at>bytes)return 0;positions[count++]=at;}return count;
}
__declspec(dllexport) int packets146(const uint8_t*data,unsigned bytes,uint8_t*out,unsigned capacity,unsigned*written){
 font146_source source={data,data+bytes};font146_span span;*written=0;
 for(;;){int result=font146_read(&source,&span);if(result<=0)return result;if(span.count>capacity-*written)return 122;
  for(unsigned n=0;n<span.count;++n)out[(*written)++]=span.literal?span.literal[n]:(uint8_t)span.value;
 }
}
