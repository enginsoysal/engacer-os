/* Production caption contracts, including exact hit boundaries and tinted ink. */
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <engine/ui/chrome12.h>
#include <engine/ui/icons12.h>
static double lum(uint32_t c){double l=0,w[]={.2126,.7152,.0722};for(unsigned i=0;i<3;++i){double v=(c>>(16-i*8)&255)/255.;l+=w[i]*(v<=.04045?v/12.92:pow((v+.055)/1.055,2.4));}return l;}
static double contrast(uint32_t a,uint32_t b){double x=lum(a),y=lum(b);return(fmax(x,y)+.05)/(fmin(x,y)+.05);}
int main(void){
 unsigned long long points=0,styles=0,tints=0;
 for(int width=188;width<=4096;width+=7)for(int y=-2;y<=42;++y)for(int x=-2;x<=width+2;++x){
  unsigned expected=0;for(unsigned part=1;part<=4;++part){ui12_caption_rect r=ui12_caption_bounds(width,part);if(x>=r.x&&x<r.x+r.width&&y>=r.y&&y<r.y+r.height){assert(!expected);expected=part;}}
  assert(ui12_caption_hit(width,x,y)==expected);++points;
 }
 for(unsigned theme=0;theme<3;++theme)for(unsigned active=0;active<2;++active)for(unsigned part=1;part<=4;++part)for(unsigned state=0;state<16;++state){
  ui12_palette p=ui12_theme(theme,0x64e2bd);ui12_style s=ui12_caption_style(p,active,part,state);
  if(!(state&UI12_DISABLED))assert(contrast(s.ink,s.fill)>=4.5);
  if((state&UI12_FOCUS)&&!(state&UI12_DISABLED))assert(contrast(s.border,s.fill)>=3);
  ++styles;
 }
 unsigned caption_icons[]={ICON12_MINIMIZE,ICON12_MAXIMIZE,ICON12_RESTORE,ICON12_CLOSE};
 for(unsigned i=0;i<4;++i)for(unsigned size=16;size<=128;size+=4)for(unsigned y=0;y<size;++y){
  unsigned id=caption_icons[i];uint32_t plain[128],tinted[130];tinted[0]=tinted[size+1]=0x12345678;
  ui12_icon_row(id,y,size,0,plain);ui12_icon_row_ink(id,y,size,0,0xff00ff,tinted+1);
  assert(tinted[0]==0x12345678&&tinted[size+1]==0x12345678);
  for(unsigned x=0;x<size;++x){uint32_t v=tinted[x+1];unsigned a=v>>24;if(id==ICON12_CLOSE||id==ICON12_MINIMIZE)assert((plain[x]>>24)==a);assert((v>>16&255)==a&&(v&255)==a&&(v>>8&255)==0);++tints;}
  if((id==ICON12_MAXIMIZE||id==ICON12_RESTORE)&&y==size/2)assert(tinted[size/2+1]==0);
 }
 printf("{\"geometry_points\":%llu,\"styles\":%llu,\"tinted_pixels\":%llu}\n",points,styles,tints);return 0;
}
