/* One geometry/style contract for native caption drawing and input. */
#ifndef ENGINE_UI_CHROME12_H
#define ENGINE_UI_CHROME12_H
#include <engine/ui/components12.h>
enum {UI12_CAPTION_HEIGHT=40,UI12_CAPTION_MIN=1,UI12_CAPTION_MAX,UI12_CAPTION_CLOSE,UI12_CAPTION_MENU};
typedef struct {int x,y,width,height;} ui12_caption_rect;
static inline ui12_caption_rect ui12_caption_bounds(int width,unsigned part){
 if(part==UI12_CAPTION_MENU)return(ui12_caption_rect){4,4,32,32};
 if(part>=UI12_CAPTION_MIN&&part<=UI12_CAPTION_CLOSE)return(ui12_caption_rect){width-136+(int)(part-1)*44,2,44,36};
 return(ui12_caption_rect){0,0,0,0};
}
static inline unsigned ui12_caption_hit(int width,int x,int y){
 if(width<188||x<0||x>=width||y<0||y>=UI12_CAPTION_HEIGHT)return 0;
 for(unsigned part=1;part<=4;++part){ui12_caption_rect r=ui12_caption_bounds(width,part);if(x>=r.x&&x<r.x+r.width&&y>=r.y&&y<r.y+r.height)return part;}
 return 0;
}
static inline uint32_t ui12_caption_fill(ui12_palette p,unsigned active){return active?p.surface:p.paper;}
static inline ui12_style ui12_caption_style(ui12_palette p,unsigned active,unsigned part,unsigned state){
 uint32_t fill=ui12_caption_fill(p,active);ui12_style s={fill,active?p.ink:p.muted,fill};
 if(state&UI12_DISABLED){s.ink=p.muted;return s;}
 if(state&(UI12_HOVER|UI12_PRESSED)){
  s.fill=part==UI12_CAPTION_CLOSE?((state&UI12_PRESSED)?0x88180f:0xb42318):ui12_mix(fill,p.ink,1,(state&UI12_PRESSED)?5:10);
  s.ink=part==UI12_CAPTION_CLOSE?0xffffff:p.ink;
 }
 if(state&UI12_FOCUS)s.border=ui12_foreground(s.fill);
 return s;
}
#endif
