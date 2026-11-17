/* Compile actual prior/current native round raster bodies with bounded host probes. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define ENGINE_M92 1
#define ENGINE_M74 1
#define ENGINE_M9 1
#define ENGINE_M12 1
static struct {unsigned framebuffer_width,framebuffer_height;} display,*screen=&display;
static unsigned scale73=2,clip7_active,clip7_left,clip7_top,clip7_right,clip7_bottom,which;
static uint32_t *images[2];
static uint64_t visits[2],blends[2],pumps[2],dirty[2],cases;
static int32_t signed_phys92(int64_t n){int64_t value=n*scale73;return (int32_t)(value>=0?value/2:-((-value+1)/2));}
static unsigned phys73(unsigned n){return (unsigned)signed_phys92((int32_t)n);}
static unsigned audio74_pending(void){return 1;}
static void audio74_pump(void){++pumps[which];}
static void graphics9_dirty(unsigned x,unsigned y,unsigned w,unsigned h){dirty[which]=dirty[which]*131+x+3*y+5*w+7*h;}
static void blend73(unsigned x,unsigned y,uint32_t rgb,unsigned alpha,unsigned clipped){
 (void)clipped;assert(x<screen->framebuffer_width&&y<screen->framebuffer_height&&alpha<=255);++blends[which];if(!alpha)return;
 uint32_t *p=images[which]+64+(size_t)y*screen->framebuffer_width+x,bg=*p,value=0;
 for(unsigned shift=0;shift<24;shift+=8)value|=(((((rgb>>shift)&255)*alpha+((bg>>shift)&255)*(255-alpha)+127)/255)<<shift);
 *p=value;
}
#include "raster-baseline.h"
#include "raster-current.h"
static uint32_t rng=0x173192;
static unsigned random17(unsigned limit){rng^=rng<<13;rng^=rng>>17;rng^=rng<<5;return limit?rng%limit:0;}
static void initialize(unsigned width,unsigned height){
 display.framebuffer_width=width;display.framebuffer_height=height;size_t count=(size_t)width*height;
 for(unsigned n=0;n<2;++n){for(unsigned i=0;i<64;++i)images[n][i]=images[n][count+64+i]=0xa517cafe;for(size_t i=0;i<count;++i)images[n][i+64]=(uint32_t)(i*104729)&0xffffff;visits[n]=blends[n]=pumps[n]=dirty[n]=0;}
}
static void equal17(void){
 size_t count=(size_t)display.framebuffer_width*display.framebuffer_height;assert(!memcmp(images[0]+64,images[1]+64,count*4));assert(blends[0]==blends[1]&&pumps[0]==pumps[1]&&dirty[0]==dirty[1]);
 for(unsigned n=0;n<2;++n)for(unsigned i=0;i<64;++i)assert(images[n][i]==0xa517cafe&&images[n][count+64+i]==0xa517cafe);++cases;
}
int main(void){
 const size_t capacity=(size_t)3840*2160+128;for(unsigned n=0;n<2;++n){images[n]=malloc(capacity*4);assert(images[n]);}
 const unsigned alpha[]={0,3,127,255};
 for(scale73=2;scale73<=4;++scale73)for(unsigned round=0;round<256;++round)for(unsigned a=0;a<4;++a){
  initialize(160,120);int x=(int)random17(221)-90,y=(int)random17(181)-70;unsigned w=random17(181),h=random17(161),r=random17(41);clip7_active=round&1;clip7_left=7;clip7_top=9;clip7_right=160*2/scale73-8;clip7_bottom=120*2/scale73-5;
  which=0;baseline17((unsigned)x,(unsigned)y,w,h,r,0x397a5c,alpha[a]);which=1;current17((unsigned)x,(unsigned)y,w,h,r,0x397a5c,alpha[a]);equal17();
 }
 scale73=4;clip7_active=0;initialize(3840,2160);clock_t times[2];
 for(which=0;which<2;++which){clock_t start=clock();for(unsigned layer=8;layer;--layer){if(which)current17(380-layer,190-layer+4,1080+2*layer,720+2*layer,12+layer,0x081824,3);else baseline17(380-layer,190-layer+4,1080+2*layer,720+2*layer,12+layer,0x081824,3);}times[which]=clock()-start;}
 equal17();assert(visits[1]*5<visits[0]);
 printf("{\"passed\":true,\"pixel_cases\":%llu,\"baseline_visits\":%llu,\"current_visits\":%llu,\"equal_blend_calls\":%llu,\"equal_audio_pumps\":%llu,\"baseline_cpu_ms\":%.3f,\"current_cpu_ms\":%.3f,\"host_buffer_bytes\":%llu,\"guard_bytes_unchanged\":true}\n",(unsigned long long)cases,(unsigned long long)visits[0],(unsigned long long)visits[1],(unsigned long long)blends[0],(unsigned long long)pumps[0],1000.*times[0]/CLOCKS_PER_SEC,1000.*times[1]/CLOCKS_PER_SEC,(unsigned long long)(capacity*8));
 for(unsigned n=0;n<2;++n)free(images[n]);return 0;
}
