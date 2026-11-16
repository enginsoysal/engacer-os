/* Exercise production integer color/state/scroll rules against independent math. */
#include <assert.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <engine/ui/components12.h>

static double linear[256];
static double luminance(uint32_t c){return .2126*linear[c>>16&255]+.7152*linear[c>>8&255]+.0722*linear[c&255];}
static double contrast(uint32_t a,uint32_t b){double x=luminance(a),y=luminance(b);return x>y?(x+.05)/(y+.05):(y+.05)/(x+.05);}
int main(void){
 for(unsigned i=0;i<256;++i){double x=i/255.;linear[i]=x<=.04045?x/12.92:pow((x+.055)/1.055,2.4);}
 for(uint32_t c=0;c<=0xffffff;++c)assert(contrast(c,ui12_foreground(c))>=4.5);
 unsigned states=0;
 for(unsigned theme=0;theme<3;++theme)for(unsigned r=0;r<256;r+=17)for(unsigned g=0;g<256;g+=17)for(unsigned b=0;b<256;b+=17){
  ui12_palette p=ui12_theme(theme,(r<<16)|(g<<8)|b);
  assert(contrast(p.ink,p.paper)>=4.5&&contrast(p.muted,p.surface)>=4.5);
  assert(contrast(p.control_border,p.paper)>=3.0);
  for(unsigned state=0;state<64;++state)for(unsigned primary=0;primary<2;++primary){
   ui12_style s=ui12_control_style(p,state,primary);++states;
   if(state&UI12_DISABLED)assert(s.fill==p.paper);
   else {if(contrast(s.ink,s.fill)<4.5)fprintf(stderr,"Contrast failure: theme=%u accent=%06x state=%u primary=%u fill=%06x ink=%06x ratio=%.6f\n",theme,p.accent,state,primary,s.fill,s.ink,contrast(s.ink,s.fill));assert(contrast(s.ink,s.fill)>=4.5);if(state&UI12_FOCUS)assert(s.border==p.ink);}
  }
 }
 const unsigned values[]={0,1,7,24,25,128,4096,UINT_MAX};unsigned geometry=0;
 for(unsigned t=0;t<8;++t)for(unsigned v=0;v<8;++v)for(unsigned n=0;n<8;++n){
  unsigned track=values[t],visible=values[v],total=values[n];
  unsigned size=ui12_scroll_size(track,visible,total),last=0;assert(size<=track);
  unsigned last_value=0;
  for(unsigned k=0;k<8;++k){unsigned at=ui12_scroll_offset(track,visible,total,values[k]);assert(at<=track-size&&at>=last);last=at;unsigned value=ui12_scroll_value(track,visible,total,values[k]);assert(value>=last_value&&(visible>=total?value==0:value<=total-visible));last_value=value;++geometry;}
  if(total>visible)assert(ui12_scroll_offset(track,visible,total,UINT_MAX)==track-size);
 }
 printf("PASS: 16777216 accent colors; %u component state cases; %u bounded scroll cases.\n",states,geometry);
 return 0;
}
