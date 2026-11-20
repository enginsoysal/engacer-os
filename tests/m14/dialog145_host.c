#include "../../user/windows8/dialog-core145.h"
void*memset(void*dst,int value,size_t bytes){volatile unsigned char*p=dst;for(size_t n=0;n<bytes;++n)p[n]=(unsigned char)value;return dst;}
__declspec(dllexport) unsigned inspect145(const void*data,unsigned bytes,uint64_t*out,unsigned capacity){
 dialog_template145 parsed;unsigned error=dialog_parse145(data,bytes,&parsed);if(error)return error;
 unsigned needed=12+parsed.count*12;if(!out||capacity<needed)return 122;
 out[0]=parsed.extended;out[1]=parsed.count;out[2]=parsed.style;out[3]=parsed.exstyle;out[4]=(uint64_t)(int64_t)parsed.x;out[5]=(uint64_t)(int64_t)parsed.y;out[6]=(unsigned)parsed.width;out[7]=(unsigned)parsed.height;out[8]=parsed.font_size;out[9]=parsed.font_weight;out[10]=parsed.consumed;out[11]=parsed.help;
 for(unsigned n=0;n<parsed.count;++n){dialog_item145*item=parsed.items+n;uint64_t*p=out+12+n*12;p[0]=item->id;p[1]=item->style;p[2]=item->exstyle;p[3]=(uint64_t)(int64_t)item->x;p[4]=(uint64_t)(int64_t)item->y;p[5]=(unsigned)item->width;p[6]=(unsigned)item->height;p[7]=item->class_name.ordinal;p[8]=item->title.ordinal;p[9]=item->extra_bytes;p[10]=item->help;p[11]=item->extra_bytes?item->extra[0]:0;}
 return 0;
}
