#ifndef ENGACER_COMPONENTS12_H
#define ENGACER_COMPONENTS12_H
#include <stdint.h>
#include <engine/ui/luminance12.h>

enum {UI12_BODY=1,UI12_SECTION=3,UI12_HEADING=4,UI12_SECONDARY=5};
enum {UI12_HOVER=1,UI12_PRESSED=2,UI12_DISABLED=4,UI12_FOCUS=8,UI12_SELECTED=16,UI12_INACTIVE=32};
enum {UI12_CONTROL_HEIGHT=36,UI12_SETUP_HEIGHT=44,UI12_RADIUS=6,UI12_SPACE=8};
typedef struct {uint32_t paper,surface,ink,muted,line,accent,on_accent,selection,control_border;} ui12_palette;
typedef struct {uint32_t fill,ink,border;} ui12_style;

static inline uint32_t ui12_mix(uint32_t a,uint32_t b,unsigned n,unsigned d){
 uint32_t result=0;if(!d)return a;if(n>d)n=d;
 for(unsigned shift=0;shift<24;shift+=8)result|=((((a>>shift)&255)*(d-n)+((b>>shift)&255)*n)/d)<<shift;
 return result;
}
static inline uint32_t ui12_foreground(uint32_t background){
 uint32_t light=(2126u*ui12_linear[(background>>16)&255]+7152u*ui12_linear[(background>>8)&255]+722u*ui12_linear[background&255])/10000;
 return light>=11739u?0x000000u:0xffffffu;
}
static inline ui12_palette ui12_theme(unsigned theme,uint32_t accent){
 ui12_palette p=theme==2?(ui12_palette){0,0,0xffffff,0xffffff,0xffffff,0xffff00,0,0x000080,0xffffff}:
  theme?(ui12_palette){0x161d27,0x202732,0xe8edf5,0xabb7c6,0x485567,accent,0,0x25483f,0x8a99ac}:
  (ui12_palette){0xf8fafc,0xffffff,0x17212f,0x526173,0xccd4df,accent,0,0xd9efe9,0x788797};
 p.on_accent=ui12_foreground(p.accent);return p;
}
static inline ui12_style ui12_control_style(ui12_palette p,unsigned state,unsigned primary){
 ui12_style s={p.surface,p.ink,p.control_border};
 if(state&UI12_DISABLED)return(ui12_style){p.paper,ui12_mix(p.muted,p.paper,1,3),p.line};
 if(primary||(state&UI12_SELECTED)){s.fill=p.accent;s.ink=p.on_accent;}
 if(state&UI12_PRESSED)s.fill=ui12_mix(s.fill,primary?s.ink:p.accent,1,4);
 else if(state&UI12_HOVER)s.fill=ui12_mix(s.fill,primary?s.ink:p.accent,1,8);
 if(primary||(state&UI12_SELECTED))s.ink=ui12_foreground(s.fill);
 if(state&UI12_INACTIVE){s.fill=p.selection;s.ink=p.ink;}
 if(state&UI12_FOCUS)s.border=p.ink;
 return s;
}
/* Proportional scroll geometry; zero/fully visible content has no moving thumb. */
static inline unsigned ui12_scroll_size(unsigned track,unsigned visible,unsigned total){
 if(!track||!total||visible>=total)return track;
 uint64_t value=(uint64_t)track*visible/total;unsigned minimum=track<24?track:24;
 return value<minimum?minimum:(unsigned)value;
}
static inline unsigned ui12_scroll_offset(unsigned track,unsigned visible,unsigned total,unsigned first){
 if(!total||visible>=total)return 0;
 unsigned remaining=total-visible;if(first>remaining)first=remaining;
 return (unsigned)((uint64_t)(track-ui12_scroll_size(track,visible,total))*first/remaining);
}
static inline unsigned ui12_scroll_value(unsigned track,unsigned visible,unsigned total,unsigned position){
 if(!total||visible>=total)return 0;
 unsigned travel=track-ui12_scroll_size(track,visible,total);if(!travel)return 0;
 if(position>travel)position=travel;
 return (unsigned)((uint64_t)position*(total-visible)/travel);
}
#endif
