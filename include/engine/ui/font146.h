#ifndef ENGINE_UI_FONT146_H
#define ENGINE_UI_FONT146_H
#include <stdint.h>
#include <stddef.h>
_Static_assert(sizeof(font73_glyph)==12,"Retained glyph descriptor layout");
_Static_assert(sizeof(font146_extra)==16,"Bounded Unicode glyph metadata");
_Static_assert(sizeof(font146_extras)/sizeof(font146_extras[0])==6*FONT146_CODES,"Six actual ordinary/secondary faces");

/* The generated font73.h precedes this header. No font cache is allocated. */
typedef struct {const uint8_t*at,*end;} font146_source;
typedef struct {const uint8_t*literal;unsigned count,value;} font146_span;
static inline int font146_read(font146_source*s,font146_span*out){
 if(s->at>s->end)return -1;if(s->at==s->end)return 0;
 unsigned token=*s->at++;out->literal=0;
 if(token<128){out->count=token+1;out->value=0;}
 else if(token<192){out->count=token-127;out->value=255;}
 else{out->count=token-191;out->value=0;if((size_t)(s->end-s->at)<out->count)return -1;out->literal=s->at;s->at+=out->count;}
 return 1;
}
typedef struct {font146_source source;font146_span span;unsigned used,bad;} font146_reader;
static inline font146_reader font146_begin(const font73_glyph*g){
 font146_reader r={0};unsigned size=sizeof(font73_data);
 if(g->offset>size||g->bytes>size-g->offset){r.bad=1;r.source.at=r.source.end=font73_data;return r;}
 r.source.at=font73_data+g->offset;r.source.end=r.source.at+g->bytes;return r;
}
static inline unsigned font146_pixel(font146_reader*r){
 if(r->bad)return 0;if(r->used==r->span.count){int next=font146_read(&r->source,&r->span);if(next!=1){r->bad=1;return 0;}r->used=0;}
 unsigned value=r->span.literal?r->span.literal[r->used]:r->span.value;++r->used;return value;
}
static inline unsigned font146_complete(const font146_reader*r){return !r->bad&&r->used==r->span.count&&r->source.at==r->source.end;}

static inline uint32_t font146_next(const char*text,unsigned*at,unsigned limit){
 unsigned begin=*at;if(begin>=limit||!text[begin])return 0;
 unsigned lead=(uint8_t)text[begin];*at=begin+1;if(lead<128)return lead;
 unsigned count;uint32_t value,minimum;
 if(lead>=0xc2&&lead<=0xdf){count=2;value=lead&31;minimum=128;}
 else if(lead>=0xe0&&lead<=0xef){count=3;value=lead&15;minimum=2048;}
 else if(lead>=0xf0&&lead<=0xf4){count=4;value=lead&7;minimum=65536;}
 else return '?';
 for(unsigned i=1;i<count;++i){if(begin+i>=limit)return '?';unsigned byte=(uint8_t)text[begin+i];if((byte&0xc0)!=0x80)return '?';value=(value<<6)|(byte&63);}
 if(value<minimum||value>0x10ffff||(value>=0xd800&&value<=0xdfff))return '?';
 *at=begin+count;return value;
}
static inline const font73_glyph*font146_lookup(const font73_face*f,uint32_t code,unsigned*base){
 *base=65535;if(code>=32&&code<=126)return font73_glyphs+f->first+code-32;
 if(f->first<=475&&f->first%95==0){unsigned first=f->first/95*FONT146_CODES,low=0,high=FONT146_CODES;
  while(low<high){unsigned mid=low+(high-low)/2;if(font146_extras[first+mid].codepoint<code)low=mid+1;else high=mid;}
  if(low<FONT146_CODES&&font146_extras[first+low].codepoint==code){*base=font146_extras[first+low].base;return &font146_extras[first+low].glyph;}
 }
 return font73_glyphs+f->first+'?'-32;
}
typedef struct {font146_reader delta,base;const font73_glyph*glyph,*basis;unsigned base_index,base_value;} font146_sampler;
static inline font146_sampler font146_sample_begin(const font73_glyph*g,unsigned base){
 font146_sampler s={0};s.glyph=g;s.delta=font146_begin(g);
 if(base!=65535&&base<sizeof(font73_glyphs)/sizeof(font73_glyphs[0])){s.basis=font73_glyphs+base;s.base=font146_begin(s.basis);}return s;
}
/* Consume in row order. Each retained base pixel is decoded at most once. */
static inline unsigned font146_sample(font146_sampler*s,unsigned x,unsigned y){
 unsigned alpha=font146_pixel(&s->delta),basis=0;
 if(s->basis){int bx=s->glyph->x+(int)x-s->basis->x,by=s->glyph->y+(int)y-s->basis->y;
  if(bx>=0&&by>=0&&(unsigned)bx<s->basis->width&&(unsigned)by<s->basis->height){unsigned target=(unsigned)by*s->basis->width+(unsigned)bx;
   while(s->base_index<=target){s->base_value=font146_pixel(&s->base);++s->base_index;}basis=s->base_value;
  }
 }
 return alpha^basis;
}
#endif
