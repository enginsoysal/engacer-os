/* Original clipped CPU compositor. Font coverage is generated from OFL Inter. */
#include <engine/ui/graphics73.h>
#ifdef ENGINE_M12
#include <engine/ui/icons12.h>
#endif
#include "font73.h"
#ifdef FONT146_PACKET
#include <engine/ui/font146.h>
#endif
#ifdef ENGINE_M14
#include <engine/ui/premultiplied148.h>
#endif
#ifdef ENGINE_M12
_Static_assert(sizeof(font73_faces)/sizeof(font73_faces[0])>=21,"Semantic typography requires all 21 bounded physical font faces");
#endif
#ifdef ENGINE_M74
#include <engine/audio74.h>
#endif
static unsigned scale73=2,active73;
static unsigned choice73;
unsigned verbose73;
static os_boot_info_v0 view73;
static volatile uint32_t *pixel73(unsigned x,unsigned y){
#ifdef ENGINE_M9
 return pixel9(x,y);
#else
 return (volatile uint32_t*)(uintptr_t)(screen->framebuffer.physical_address+(uint64_t)y*screen->framebuffer_stride_bytes+x*4);
#endif
}
unsigned ui73_scale(void){return scale73;}
unsigned ui73_scale_choice(void){return choice73;}
const char *ui73_font_license(void){return font73_license;}
const os_boot_info_v0 *ui73_set_scale(unsigned choice){
 unsigned wanted=choice?choice:screen->framebuffer_width>=3840&&screen->framebuffer_height>=2000?4:screen->framebuffer_width>=2560&&screen->framebuffer_height>=1400?3:2;
 unsigned min_width=1024,min_height=768;
#ifdef ENGINE_M12
 min_width=800;min_height=600;
#endif
 if(wanted<2||wanted>4||screen->framebuffer_width*2/wanted<min_width||screen->framebuffer_height*2/wanted<min_height)return 0;
 scale73=wanted;choice73=choice;view73.framebuffer_width=screen->framebuffer_width*2/wanted;view73.framebuffer_height=screen->framebuffer_height*2/wanted;gui6_repaint=1;
 serial_text("M73_SCALE_APPLIED choice=");serial_hex(choice);serial_text(" actual=");serial_hex(wanted);serial_text("\n");return &view73;
}
unsigned ui73_width(void){return screen->framebuffer_width;}
unsigned ui73_height(void){return screen->framebuffer_height;}
uint64_t ui73_framebuffer_bytes(void){return (uint64_t)screen->framebuffer_stride_bytes*screen->framebuffer_height;}
#ifdef ENGINE_M74
unsigned ui74_intersects(unsigned x,unsigned y,unsigned w,unsigned h){
#ifdef ENGINE_M92
 int64_t sx=(int32_t)x,sy=(int32_t)y;return !clip7_active||(sx<clip7_right&&sy<clip7_bottom&&sx+w>clip7_left&&sy+h>clip7_top);
#else
 return !clip7_active||(x<clip7_right&&y<clip7_bottom&&x+w>clip7_left&&y+h>clip7_top);
#endif
}
uint32_t ui74_rgb(unsigned x,unsigned y){
 if(x>=screen->framebuffer_width||y>=screen->framebuffer_height)return 0;
 uint32_t raw=*pixel73(x,y);
 return color(raw)&0xffffff;
}
#endif
const os_boot_info_v0 *ui73_begin(const os_boot_info_v0*boot){
#ifdef ENGINE_M9
 graphics9_begin();
#endif
 scale73=boot->framebuffer_width>=3840&&boot->framebuffer_height>=2000?4:boot->framebuffer_width>=2560&&boot->framebuffer_height>=1400?3:2;
 view73=*boot;view73.framebuffer_width=boot->framebuffer_width*2/scale73;view73.framebuffer_height=boot->framebuffer_height*2/scale73;active73=1;
 serial_text("M73_DISPLAY physical=");serial_hex(boot->framebuffer_width);serial_text("x");serial_hex(boot->framebuffer_height);serial_text(" scale_half=");serial_hex(scale73);serial_text(" logical=");serial_hex(view73.framebuffer_width);serial_text("x");serial_hex(view73.framebuffer_height);serial_text("\n");
 return &view73;
}
#ifdef ENGINE_M92
static int32_t signed_phys92(int64_t n){int64_t value=n*scale73;return (int32_t)(value>=0?value/2:-((-value+1)/2));}
static unsigned phys73(unsigned n){return (unsigned)signed_phys92((int32_t)n);}
#else
static unsigned phys73(unsigned n){return n*scale73/2;}
#endif
static void blend73(unsigned x,unsigned y,uint32_t rgb,unsigned a,unsigned clipped){
 if(!a||x>=screen->framebuffer_width||y>=screen->framebuffer_height)return;
 if(clipped&&clip7_active&&(x<phys73(clip7_left)||x>=phys73(clip7_right)||y<phys73(clip7_top)||y>=phys73(clip7_bottom)))return;
 volatile uint32_t*p=pixel73(x,y);
 uint32_t fg=color(rgb);if(a==255){*p=fg;return;}uint32_t bg=*p;
 unsigned r=(((fg>>16)&255)*a+((bg>>16)&255)*(255-a)+127)/255;
 unsigned g=(((fg>>8)&255)*a+((bg>>8)&255)*(255-a)+127)/255;
 unsigned b=((fg&255)*a+(bg&255)*(255-a)+127)/255;*p=(r<<16)|(g<<8)|b;
}
#ifdef ENGINE_M12
#include "icons12.inc"
#endif
/* Small copied icon tiles reuse the compositor's clipped straight-alpha blend. */
void ui145_argb_tile(int x,int y,unsigned width,unsigned height,const uint32_t*pixels){
 if(!pixels||!width||width>16||!height||height>8)return;
 for(unsigned row=0;row<height;++row)for(unsigned col=0;col<width;++col){
  uint32_t value=pixels[row*width+col];unsigned alpha=value>>24;if(!alpha)continue;
  int left=(int)phys73((unsigned)(x+(int)col)),right=(int)phys73((unsigned)(x+(int)col+1));
  int top=(int)phys73((unsigned)(y+(int)row)),bottom=(int)phys73((unsigned)(y+(int)row+1));
  if(left<0)left=0;if(top<0)top=0;
  if(right>(int)screen->framebuffer_width)right=(int)screen->framebuffer_width;
  if(bottom>(int)screen->framebuffer_height)bottom=(int)screen->framebuffer_height;
  for(int yy=top;yy<bottom;++yy)for(int xx=left;xx<right;++xx)blend73((unsigned)xx,(unsigned)yy,value&0xffffffu,alpha,1);
 }
}
#ifdef ENGINE_M14
static void image_premul148(unsigned x,unsigned y,uint32_t value){
 unsigned alpha=value>>24;if(!alpha)return;if(alpha==255){blend73(x,y,value&0xffffff,255,0);return;}volatile uint32_t*p=pixel73(x,y);uint32_t fg=color(value&0xffffff),bg=*p;
 *p=pargb_over148((alpha<<24)|fg,bg)&0xffffffu;
}
void ui148_image(int x,int y,const wui_image_view148*image){
 if(!image||!image->width||!image->height)return;int64_t left=x,top=y,right=left+image->width,bottom=top+image->height;if(left<0)left=0;if(top<0)top=0;if(right>view73.framebuffer_width)right=view73.framebuffer_width;if(bottom>view73.framebuffer_height)bottom=view73.framebuffer_height;
 if(clip7_active){if(left<clip7_left)left=clip7_left;if(top<clip7_top)top=clip7_top;if(right>clip7_right)right=clip7_right;if(bottom>clip7_bottom)bottom=clip7_bottom;}if(left>=right||top>=bottom)return;
#ifdef ENGINE_M9
 graphics9_dirty(phys73((unsigned)left),phys73((unsigned)top),phys73((unsigned)right)-phys73((unsigned)left),phys73((unsigned)bottom)-phys73((unsigned)top));
#endif
 for(int64_t row=top;row<bottom;++row){unsigned py=phys73((unsigned)row),pb=phys73((unsigned)row+1);for(int64_t col=left;col<right;++col){uint64_t offset=((uint64_t)(row-y)*image->width+(unsigned)(col-x))*4;unsigned page=(unsigned)(offset/4096);const uint64_t*table=(const uint64_t*)(uintptr_t)image->tables[page/512];const uint32_t*p=(const uint32_t*)(uintptr_t)(table[page%512]+offset%4096);uint32_t value=*p;unsigned alpha=value>>24;if(!alpha)continue;if(image->format==1&&alpha!=255)value=pargb_color148(value);unsigned px=phys73((unsigned)col),pr=phys73((unsigned)col+1);for(unsigned yy=py;yy<pb;++yy)for(unsigned xx=px;xx<pr;++xx){image_premul148(xx,yy,value);}}}
}
#endif
static inline void fill_row73(unsigned x,unsigned y,unsigned width,uint32_t value){
 uint32_t*p=(uint32_t*)pixel73(x,y);size_t count=width;
 __asm__ volatile("cld; rep stosl":"+D"(p),"+c"(count):"a"(value):"memory","cc");
}
static void rect73(unsigned x,unsigned y,unsigned w,unsigned h,uint32_t rgb){
 if(!x&&!y)gui6_repaint=1;
#ifdef ENGINE_M92
 int64_t sx=(int32_t)x,sy=(int32_t)y,ex=sx+w,ey=sy+h;
 if(sx<0)sx=0;if(sy<0)sy=0;if(ex>view73.framebuffer_width)ex=view73.framebuffer_width;if(ey>view73.framebuffer_height)ey=view73.framebuffer_height;
 if(sx>=ex||sy>=ey)return;x=(unsigned)sx;y=(unsigned)sy;w=(unsigned)(ex-sx);h=(unsigned)(ey-sy);
#endif
 if(x>=view73.framebuffer_width||y>=view73.framebuffer_height)return;
 if(w>view73.framebuffer_width-x)w=view73.framebuffer_width-x;if(h>view73.framebuffer_height-y)h=view73.framebuffer_height-y;
 unsigned right=x+w,bottom=y+h;
 if(clip7_active){if(x<clip7_left)x=clip7_left;if(y<clip7_top)y=clip7_top;if(right>clip7_right)right=clip7_right;if(bottom>clip7_bottom)bottom=clip7_bottom;}
 if(x>=right||y>=bottom)return;
 unsigned px=phys73(x),py=phys73(y),pr=phys73(right),pb=phys73(bottom);uint32_t value=color(rgb);
#ifdef ENGINE_M9
 graphics9_dirty(px,py,pr-px,pb-py);
#endif
 for(unsigned j=py;j<pb;++j){
#ifdef ENGINE_M74
 if(!(j&15)&&audio74_pending())audio74_pump();
#endif
 /* Fill the bounded clipped row in one architectural string operation.
    This keeps stride/audio servicing intact without per-pixel loop overhead. */
 fill_row73(px,j,pr-px,value);}
}
static void round_alpha73(unsigned x,unsigned y,unsigned w,unsigned h,unsigned radius,uint32_t rgb,unsigned alpha,const int64_t*cover){
 if(!w||!h)return;
#ifdef ENGINE_M92
 int px=signed_phys92((int32_t)x),py=signed_phys92((int32_t)y);int ex=signed_phys92((int64_t)(int32_t)x+w),ey=signed_phys92((int64_t)(int32_t)y+h);
 if(ex<=0||ey<=0||px>=(int)screen->framebuffer_width||py>=(int)screen->framebuffer_height)return;
 unsigned pw=(unsigned)(ex-px),ph=(unsigned)(ey-py),r=phys73(radius);
#else
 unsigned px=phys73(x),py=phys73(y),pw=phys73(x+w)-px,ph=phys73(y+h)-py,r=phys73(radius);
#endif
 if(r>pw/2)r=pw/2;if(r>ph/2)r=ph/2;
#ifdef ENGINE_M92
 unsigned l=px<0?0:(unsigned)px,t=py<0?0:(unsigned)py,right=(unsigned)ex,bottom=(unsigned)ey;
#else
 unsigned l=px,t=py,right=px+pw,bottom=py+ph;
#endif
 if(clip7_active){if(l<phys73(clip7_left))l=phys73(clip7_left);if(t<phys73(clip7_top))t=phys73(clip7_top);if(right>phys73(clip7_right))right=phys73(clip7_right);if(bottom>phys73(clip7_bottom))bottom=phys73(clip7_bottom);}
 if(right>screen->framebuffer_width)right=screen->framebuffer_width;if(bottom>screen->framebuffer_height)bottom=screen->framebuffer_height;
#ifdef ENGINE_M9
 if(l<right&&t<bottom)graphics9_dirty(l,t,right-l,bottom-t);
#endif
 uint32_t opaque_value=alpha==255?color(rgb):0;
 for(unsigned yy=t;yy<bottom;++yy){
#ifdef ENGINE_M74
 if(!(yy&15)&&audio74_pending())audio74_pump();
#endif
 /* Opaque straight spans need one bounded fill. Shadows may omit only
    pixels guaranteed covered by their immediately following opaque surface. */
 unsigned span_left=right,span_right=right,dy_row=yy-py;
 if(alpha==255){
  int64_t left=l,end=right;
  if(r&&(dy_row<r||dy_row>=ph-r)){if(left<(int64_t)px+r)left=(int64_t)px+r;if(end>(int64_t)px+pw-r)end=(int64_t)px+pw-r;}
  if(left<end){span_left=(unsigned)left;span_right=(unsigned)end;}
 }else if(cover&&(int64_t)yy>=cover[1]&&(int64_t)yy<cover[3]){
  int64_t left=cover[0],end=cover[2];
  if((int64_t)yy<cover[1]+cover[4]||(int64_t)yy>=cover[3]-cover[4]){left+=cover[4];end-=cover[4];}
  if(left<(int64_t)l)left=l;if(end>(int64_t)right)end=right;
  if(left<end){span_left=(unsigned)left;span_right=(unsigned)end;}
 }
 for(unsigned xx=l;xx<right;++xx){
 if(xx==span_left&&span_left<span_right){if(alpha==255)fill_row73(span_left,yy,span_right-span_left,opaque_value);xx=span_right-1;continue;}
 unsigned dx=xx-px,dy=yy-py;
 /* Shadow interiors are covered by the opaque surface: never blend them. */
 if(alpha<255&&dx>=r&&dx<pw-r&&dy>=r&&dy<ph-r){
#ifdef ENGINE_M12
  /* Jump across covered shadow interiors without visiting every pixel. */
  unsigned skip=pw-r-dx;if(skip>right-xx)skip=right-xx;xx+=skip-1;
#endif
  continue;
 }
 if(!r||(dx>=r&&dx<pw-r)||(dy>=r&&dy<ph-r)){blend73(xx,yy,rgb,alpha,0);continue;}
 int cx=(int)(dx<r?r:pw-r),cy=(int)(dy<r?r:ph-r);unsigned covered=0;
 for(unsigned sy=0;sy<4;++sy)for(unsigned sx=0;sx<4;++sx){int vx=(int)dx*8+(int)sx*2+1-cx*8,vy=(int)dy*8+(int)sy*2+1-cy*8;if(vx*vx+vy*vy<=(int)(r*r*64))++covered;}
 blend73(xx,yy,rgb,(covered*alpha+8)/16,0);}}
}
void ui73_round(unsigned x,unsigned y,unsigned w,unsigned h,unsigned r,uint32_t c){round_alpha73(x,y,w,h,r,c,255,0);}
void ui73_shadow(unsigned x,unsigned y,unsigned w,unsigned h){
 /* Current callers immediately paint an opaque surface, radius <=16.
    Keep all corner antialiasing and exterior shadow pixels; skip its covered
    cross-shaped interior. Stack-only geometry adds no retained state. */
 int64_t cover[5]={phys73(x),phys73(y),phys73(x+w),phys73(y+h),(16*scale73+1)/2};
 for(unsigned i=8;i;--i)
#ifndef ENGINE_M92
 if(x>=i&&y>=i)
#endif
 round_alpha73(x-i,y-i+4,w+2*i,h+2*i,12+i,0x081824,3,cover);
}
static const font73_face *face73(unsigned role){
#ifdef ENGINE_M12
 if(role==3||(role>=4&&role!=5))return &font73_faces[15+(role>=4?3:0)+scale73-2];
#endif
#ifdef ENGINE_M11
 if(role==5)return &font73_faces[12+scale73-2];
#endif
 unsigned logical=role>=4?32:role==3?24:16,actual=logical*scale73/2;
 unsigned index=actual==16?0:actual==24?1:actual==32?2:actual==36?3:actual==48?4:5;
 return &font73_faces[index+(role>=3?6:0)];
}
#ifdef ENGINE_M14
unsigned ui148_font_role(unsigned em){switch(em){case 0:case 16:return 1;case 14:return 5;case 21:return 3;case 28:return 4;default:return 0;}}
unsigned ui148_font_height(unsigned em){unsigned role=ui148_font_role(em);return role?(face73(role)->height*2+scale73-1)/scale73:0;}
unsigned ui148_font_info(unsigned em,ui_font_metrics148*out){
 unsigned role=ui148_font_role(em);if(!role||!out)return 0;const font73_face*f=face73(role);unsigned maximum=0,total=0,last=126;
 for(unsigned i=0;i<95;++i){unsigned advance=font73_glyphs[f->first+i].advance;if(advance>maximum)maximum=advance;if((i+32>='A'&&i+32<='Z')||(i+32>='a'&&i+32<='z'))total+=advance;}
#ifdef FONT146_PACKET
 if(f->first<=475&&f->first%95==0)for(unsigned i=0;i<FONT146_CODES;++i){const font146_extra*e=font146_extras+f->first/95*FONT146_CODES+i;if(e->codepoint>last)last=e->codepoint;if(e->glyph.advance>maximum)maximum=e->glyph.advance;}
#endif
 unsigned height=ui148_font_height(em),ascent=(f->ascent*2+scale73-1)/scale73;
 *out=(ui_font_metrics148){em?em:16,height,ascent,height-ascent,role==3||role==4?600:400,(total*2+26*scale73)/(52*scale73),(maximum*2+scale73-1)/scale73,32,last};return 1;
}
#endif
#ifdef FONT146_PACKET
unsigned ui73_measure(const char*s,unsigned role){const font73_face*f=face73(role);unsigned width=0,at=0;while(at<1024&&s[at]){uint32_t code=font146_next(s,&at,1024);if(!code)break;unsigned base;const font73_glyph*g=font146_lookup(f,code,&base);width+=g->advance;}return(width*2+scale73-1)/scale73;}
#else
unsigned ui73_measure(const char*s,unsigned role){const font73_face*f=face73(role);unsigned width=0;for(unsigned n=0;s[n]&&n<1024;++n){unsigned c=(uint8_t)s[n];if(c<32||c>126)c='?';width+=font73_glyphs[f->first+c-32].advance;}return (width*2+scale73-1)/scale73;}
#endif
static void text73(unsigned x,unsigned y,const char*s,unsigned role,uint32_t rgb){
 const font73_face*f=face73(role);unsigned pen=phys73(x),baseline=phys73(y)+f->ascent;
#ifdef FONT146_PACKET
 for(unsigned n=0;n<1024&&s[n];){uint32_t code=font146_next(s,&n,1024);unsigned base;const font73_glyph*g=font146_lookup(f,code,&base);
#else
 for(unsigned n=0;s[n]&&n<1024;++n){unsigned c=(uint8_t)s[n];if(c<32||c>126)c='?';const font73_glyph*g=&font73_glyphs[f->first+c-32];unsigned pixel_index=0;
#endif
#ifdef ENGINE_M9
 int left=(int)pen+g->x,top=(int)baseline+g->y,right=left+g->width,bottom=top+g->height;
 if(clip7_active){if(left<(int)phys73(clip7_left))left=(int)phys73(clip7_left);if(top<(int)phys73(clip7_top))top=(int)phys73(clip7_top);if(right>(int)phys73(clip7_right))right=(int)phys73(clip7_right);if(bottom>(int)phys73(clip7_bottom))bottom=(int)phys73(clip7_bottom);}
 if(left<0)left=0;if(top<0)top=0;
 if(right<=left||bottom<=top){pen+=g->advance;continue;}
 graphics9_dirty((unsigned)left,(unsigned)top,(unsigned)(right-left),(unsigned)(bottom-top));
#endif
#ifdef FONT146_PACKET
 if(base==65535){font146_reader reader=font146_begin(g);font146_span span;unsigned pixel_index=0,pixels=(unsigned)g->width*g->height;
  while(!reader.bad&&font146_read(&reader.source,&span)==1){if(span.count>pixels-pixel_index)break;
   if(span.literal||span.value)for(unsigned i=0;i<span.count;++i){unsigned alpha=span.literal?span.literal[i]:span.value,index=pixel_index+i;if(alpha&&g->width){int dx=(int)pen+g->x+(int)(index%g->width),dy=(int)baseline+g->y+(int)(index/g->width);if(dx>=0&&dy>=0)blend73((unsigned)dx,(unsigned)dy,rgb,alpha,1);}}
   pixel_index+=span.count;
  }
 }else{font146_sampler sampler=font146_sample_begin(g,base);for(unsigned row=0;row<g->height;++row)for(unsigned col=0;col<g->width;++col){unsigned alpha=font146_sample(&sampler,col,row);if(alpha){int dx=(int)pen+g->x+(int)col,dy=(int)baseline+g->y+(int)row;if(dx>=0&&dy>=0)blend73((unsigned)dx,(unsigned)dy,rgb,alpha,1);}}}
#else
 for(unsigned at=0;at<g->bytes;at+=2){unsigned count=font73_data[g->offset+at],alpha=font73_data[g->offset+at+1];
 for(unsigned i=0;i<count;++i,++pixel_index)if(alpha&&g->width){int dx=(int)pen+g->x+(int)(pixel_index%g->width),dy=(int)baseline+g->y+(int)(pixel_index/g->width);if(dx>=0&&dy>=0)blend73((unsigned)dx,(unsigned)dy,rgb,alpha,1);}}
#endif
 pen+=g->advance;}
}
#ifdef FONT146_PACKET
static unsigned font_previous146(const char*text,unsigned at){if(at){--at;while(at&&((uint8_t)text[at]&0xc0)==0x80)--at;}return at;}
void ui73_fit(unsigned x,unsigned y,unsigned width,const char*s,unsigned role,uint32_t rgb){
 char out[256];unsigned n=0;while(s[n]&&n<252){unsigned next=n;font146_next(s,&next,1024);if(next<=n||next>252)break;for(unsigned i=n;i<next;++i)out[i]=s[i];out[next]=0;if(ui73_measure(out,role)>width)break;n=next;}
 if(s[n]){while(n){out[n]=0;if(ui73_measure(out,role)+ui73_measure("...",role)<=width)break;n=font_previous146(out,n);}out[n++]='.';out[n++]='.';out[n++]='.';}out[n]=0;text73(x,y,out,role,rgb);
}
unsigned ui73_paragraph(unsigned x,unsigned y,unsigned width,unsigned max_lines,const char*s,uint32_t rgb){
 unsigned at=0,line=0;while(s[at]&&line<max_lines){char out[256];unsigned n=0,last_space=0,start=at;
  while(s[at]&&s[at]!='\n'&&n<252){unsigned step=0;font146_next(s+at,&step,4);if(!step||n+step>252)break;unsigned previous_at=at,previous_n=n;for(unsigned i=0;i<step;++i)out[n++]=s[at++];out[n]=0;if(step==1&&out[n-1]==' ')last_space=n;
   if(ui73_measure(out,1)>width){if(last_space){at=start+last_space;n=last_space-1;}else{at=previous_at;n=previous_n;}break;}}
  if(!n&&s[at]&&s[at]!='\n'){unsigned step=0;font146_next(s+at,&step,4);at+=step?step:1;continue;}out[n]=0;text73(x,y+line*24,out,1,rgb);++line;
  if(s[at]=='\n')++at;while(s[at]==' ')++at;}
 if(s[at]){serial_text("M73_TEXT_OVERFLOW\n");return 1;}return 0;
}
#else
void ui73_fit(unsigned x,unsigned y,unsigned width,const char*s,unsigned role,uint32_t rgb){
 char out[256];unsigned n=0;while(s[n]&&n<252){out[n]=s[n];out[n+1]=0;if(ui73_measure(out,role)>width)break;++n;}
 if(s[n]){while(n){out[n]=0;if(ui73_measure(out,role)+ui73_measure("...",role)<=width)break;--n;}out[n++]='.';out[n++]='.';out[n++]='.';}out[n]=0;text73(x,y,out,role,rgb);
}
unsigned ui73_paragraph(unsigned x,unsigned y,unsigned width,unsigned max_lines,const char*s,uint32_t rgb){
 unsigned at=0,line=0;while(s[at]&&line<max_lines){char out[256];unsigned n=0,last_space=0,start=at;
 while(s[at]&&s[at]!='\n'&&n<252){out[n++]=s[at++];out[n]=0;if(out[n-1]==' ')last_space=n;if(ui73_measure(out,1)>width){if(last_space){at=start+last_space;n=last_space-1;}else{--at;--n;}break;}}
 if(!n&&s[at]&&s[at]!='\n'){++at;continue;}out[n]=0;text73(x,y+line*24,out,1,rgb);++line;
 if(s[at]=='\n')++at;while(s[at]==' ')++at;}
 if(s[at]){serial_text("M73_TEXT_OVERFLOW\n");return 1;}return 0;
}
#endif
void ui73_folder(unsigned x,unsigned y,unsigned size,uint32_t tint){
 ui73_round(x,y,size/2,11,4,0xc3974e);ui73_round(x,y+6,size,size*3/4,5,tint);ui73_round(x+2,y+8,size-4,3,1,0xffe7b2);
}
static void cursor73(unsigned x,unsigned y){
#ifdef ENGINE_M9
 if(shadow9){graphics9_cursor(x,y,scale73);return;}
#endif
 static uint32_t saved[32*48];static unsigned ox,oy,visible;
#ifdef ENGINE_M12
 static unsigned ow,oh;
#endif
 unsigned w=phys73(15),h=phys73(24);if(gui6_repaint){visible=0;gui6_repaint=0;}
#ifdef ENGINE_M12
 if(visible)for(unsigned j=0;j<oh;++j)for(unsigned i=0;i<ow;++i){volatile uint32_t*p=(volatile uint32_t*)(uintptr_t)(screen->framebuffer.physical_address+(uint64_t)(oy+j)*screen->framebuffer_stride_bytes+(ox+i)*4);*p=saved[j*ow+i];}
 if(x>=screen->framebuffer_width||y>=screen->framebuffer_height){visible=0;return;}
 if(w>screen->framebuffer_width-x)w=screen->framebuffer_width-x;if(h>screen->framebuffer_height-y)h=screen->framebuffer_height-y;
#else
 if(visible)for(unsigned j=0;j<h;++j)for(unsigned i=0;i<w;++i){volatile uint32_t*p=(volatile uint32_t*)(uintptr_t)(screen->framebuffer.physical_address+(uint64_t)(oy+j)*screen->framebuffer_stride_bytes+(ox+i)*4);*p=saved[j*w+i];}
 if(x+w>screen->framebuffer_width)x=screen->framebuffer_width-w;if(y+h>screen->framebuffer_height)y=screen->framebuffer_height-h;
#endif
 for(unsigned j=0;j<h;++j)for(unsigned i=0;i<w;++i){volatile uint32_t*p=(volatile uint32_t*)(uintptr_t)(screen->framebuffer.physical_address+(uint64_t)(y+j)*screen->framebuffer_stride_bytes+(x+i)*4);saved[j*w+i]=*p;
 unsigned covered=0,edge=0;for(unsigned sy=0;sy<4;++sy)for(unsigned sx=0;sx<4;++sx){int lx=(int)(i*8+sx*2+1)*2/(int)scale73,ly=(int)(j*8+sy*2+1)*2/(int)scale73;
 if(lx>=8&&ly>=8&&lx<=ly/2+8&&ly<152){++covered;if(lx<16||lx>ly/2||ly>136)++edge;}}
 if(covered)blend73(x+i,y+j,edge*2>=covered?0x173442:0xffffff,covered*255/16,0);}
#ifdef ENGINE_M12
 ow=w;oh=h;
#endif
 ox=x;oy=y;visible=1;
}
