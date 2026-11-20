#ifndef ENGACER_DIALOG_CORE145_H
#define ENGACER_DIALOG_CORE145_H
#include <stddef.h>
#include <stdint.h>
#define DIALOG_CONTROLS145 31u
typedef struct {const uint16_t*text;unsigned ordinal;} dialog_name145;
typedef struct {uint32_t style,exstyle,id,help;int x,y,width,height;dialog_name145 class_name,title;const uint8_t*extra;unsigned extra_bytes;} dialog_item145;
typedef struct {uint32_t style,exstyle,help;unsigned extended,count,font_size,font_weight,font_italic,font_charset;int x,y,width,height;dialog_name145 menu,class_name,title,font;dialog_item145 items[DIALOG_CONTROLS145];size_t consumed;} dialog_template145;
typedef struct {const uint8_t*data;size_t size,at;} dialog_reader145;
static unsigned dialog_u16_145(const uint8_t*p){return(unsigned)p[0]|((unsigned)p[1]<<8);}
static uint32_t dialog_u32_145(const uint8_t*p){return(uint32_t)dialog_u16_145(p)|((uint32_t)dialog_u16_145(p+2)<<16);}
static int dialog_span145(dialog_reader145*r,size_t bytes){return r->at<=r->size&&bytes<=r->size-r->at;}
static unsigned dialog_name_read145(dialog_reader145*r,dialog_name145*out){
 if(!dialog_span145(r,2))return 193;unsigned first=dialog_u16_145(r->data+r->at);out->text=0;out->ordinal=0;
 if(!first){r->at+=2;return 0;}
 if(first==65535){if(!dialog_span145(r,4))return 193;out->ordinal=dialog_u16_145(r->data+r->at+2);r->at+=4;return out->ordinal?0:193;}
 out->text=(const uint16_t*)(const void*)(r->data+r->at);
 for(unsigned n=0;n<=2047;++n){if(!dialog_span145(r,2))return 193;unsigned value=dialog_u16_145(r->data+r->at);r->at+=2;if(!value)return 0;}
 return 206;
}
static unsigned dialog_parse145(const void*data,size_t bytes,dialog_template145*out){
 if(!data||!out||bytes<18||bytes>65536)return 193;
 *out=(dialog_template145){0};dialog_reader145 r={(const uint8_t*)data,bytes,0};
 unsigned extended=dialog_u16_145(r.data+2)==65535;out->extended=extended;
 if(extended){if(bytes<26||dialog_u16_145(r.data)!=1)return 193;out->help=dialog_u32_145(r.data+4);out->exstyle=dialog_u32_145(r.data+8);out->style=dialog_u32_145(r.data+12);out->count=dialog_u16_145(r.data+16);r.at=18;}
 else{out->style=dialog_u32_145(r.data);out->exstyle=dialog_u32_145(r.data+4);out->count=dialog_u16_145(r.data+8);r.at=10;}
 out->x=(int16_t)dialog_u16_145(r.data+r.at);out->y=(int16_t)dialog_u16_145(r.data+r.at+2);out->width=(int16_t)dialog_u16_145(r.data+r.at+4);out->height=(int16_t)dialog_u16_145(r.data+r.at+6);r.at+=8;
 if(out->width<0||out->height<0)return 193;if(out->count>DIALOG_CONTROLS145)return 1816;
 unsigned error=dialog_name_read145(&r,&out->menu);if(error)return error;error=dialog_name_read145(&r,&out->class_name);if(error)return error;error=dialog_name_read145(&r,&out->title);if(error)return error;
 if(out->style&64){unsigned fixed=extended?6:2;if(!dialog_span145(&r,fixed))return 193;out->font_size=dialog_u16_145(r.data+r.at);if(extended){out->font_weight=dialog_u16_145(r.data+r.at+2);out->font_italic=r.data[r.at+4];out->font_charset=r.data[r.at+5];}r.at+=fixed;error=dialog_name_read145(&r,&out->font);if(error)return error;if(out->font.ordinal)return 193;}
 for(unsigned n=0;n<out->count;++n){
  r.at=(r.at+3)&~(size_t)3;unsigned fixed=extended?24:18;if(!dialog_span145(&r,fixed))return 193;dialog_item145*item=out->items+n;const uint8_t*p=r.data+r.at;
  if(extended){item->help=dialog_u32_145(p);item->exstyle=dialog_u32_145(p+4);item->style=dialog_u32_145(p+8);p+=12;}
  else{item->style=dialog_u32_145(p);item->exstyle=dialog_u32_145(p+4);p+=8;}
  item->x=(int16_t)dialog_u16_145(p);item->y=(int16_t)dialog_u16_145(p+2);item->width=(int16_t)dialog_u16_145(p+4);item->height=(int16_t)dialog_u16_145(p+6);item->id=extended?dialog_u32_145(p+8):dialog_u16_145(p+8);r.at+=fixed;
  if(item->width<0||item->height<0)return 193;
  error=dialog_name_read145(&r,&item->class_name);if(error)return error;error=dialog_name_read145(&r,&item->title);if(error)return error;
  if(!dialog_span145(&r,2))return 193;unsigned extra=dialog_u16_145(r.data+r.at);
  if(extended){r.at+=2;item->extra=r.data+r.at;item->extra_bytes=extra;}
  else{if(extra&&extra<2)return 193;item->extra=r.data+r.at;item->extra_bytes=extra;if(!extra)r.at+=2;}
  if(!dialog_span145(&r,item->extra_bytes))return 193;r.at+=item->extra_bytes;
 }
 out->consumed=r.at;return 0;
}
#endif
