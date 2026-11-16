/* Production rasterization versus independent closest-point geometry. */
#include <assert.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <fcntl.h>
#include <io.h>
#endif
#include <engine/ui/icons12.h>

static int reference(const ui12_shape*s,int u,int v){
 double x=s->x*256.,y=s->y*256.,a=s->a*256.,b=s->b*256.;
 if(!s->kind){
  if(u<x||v<y||u>=x+a||v>=y+b)return 0;
  double r=fmin(s->r*256.,fmin(a/2,b/2));
  double cx=fmax(x+r,fmin(u,x+a-r)),cy=fmax(y+r,fmin(v,y+b-r));
  return (u-cx)*(u-cx)+(v-cy)*(v-cy)<=r*r+1e-7;
 }
 double dx=a-x,dy=b-y,len=dx*dx+dy*dy;
 double t=len?fmax(0.,fmin(1.,((u-x)*dx+(v-y)*dy)/len)):0.;
 double px=u-(x+t*dx),py=v-(y+t*dy),r=s->r*128.;
 return px*px+py*py<=r*r+1e-7;
}
static uint64_t fingerprint(unsigned id,unsigned extent,unsigned theme){
 uint64_t result=UINT64_C(1469598103934665603);uint32_t row[130];unsigned covered=0;
 for(unsigned y=0;y<extent;++y){
  for(unsigned i=0;i<130;++i)row[i]=0x12345678;
  ui12_icon_row(id,y,extent,theme,row+1);
  assert(row[0]==0x12345678&&row[extent+1]==0x12345678);
  for(unsigned x=0;x<extent;++x){uint32_t p=row[x+1];unsigned a=p>>24;covered+=!!a;
   assert((p>>16&255)<=a&&(p>>8&255)<=a&&(p&255)<=a);
   result^=p;result*=UINT64_C(1099511628211);
  }
 }
 assert(covered>extent);return result;
}
int main(int argc,char**argv){
 if(argc==5&&!strcmp(argv[1],"dump")){
#ifdef _WIN32
  if(_setmode(_fileno(stdout),_O_BINARY)==-1)return 4;
#endif
  unsigned id=(unsigned)strtoul(argv[2],0,10),extent=(unsigned)strtoul(argv[3],0,10),theme=(unsigned)strtoul(argv[4],0,10);
  if(!extent||extent>128)return 2;
  uint32_t row[128];for(unsigned y=0;y<extent;++y){ui12_icon_row(id,y,extent,theme,row);if(fwrite(row,4,extent,stdout)!=extent)return 3;}return 0;
 }
 unsigned samples=0,cases=0;
 for(unsigned i=0;i<sizeof(icon12_shapes)/sizeof(*icon12_shapes);++i)
  for(int y=-129;y<=8321;y+=131)for(int x=-129;x<=8321;x+=131){assert(ui12_shape_contains(&icon12_shapes[i],x,y)==reference(&icon12_shapes[i],x,y));++samples;}
 unsigned sizes[]={8,16,20,24,26,32,39,40,42,48,63,64,96,128};
 for(unsigned theme=0;theme<2;++theme)for(unsigned size=0;size<sizeof(sizes)/sizeof(*sizes);++size){
  uint64_t apps[20]={0};
  for(unsigned id=0;id<ICON12_COUNT;++id){uint64_t hash=fingerprint(id,sizes[size],theme);++cases;if(id&&id<20){for(unsigned prior=1;prior<id;++prior)assert(apps[prior]!=hash);apps[id]=hash;}}
  assert(fingerprint(UINT_MAX,sizes[size],theme)==fingerprint(ICON12_UNKNOWN,sizes[size],theme));
 }
 uint32_t untouched[128];for(unsigned i=0;i<128;++i)untouched[i]=0xabcdef01;
 ui12_icon_row(1,0,0,0,untouched);ui12_icon_row(1,0,129,0,untouched);
 for(unsigned i=0;i<128;++i)assert(untouched[i]==0xabcdef01);
 assert(ICON12_WINDOWS_APPS==19&&ICON12_COUNT==57);
 printf("PASS: %u independent geometry samples, %u icon/theme/extent cases, 19 distinct app identities, fallback and row bounds.\n",samples,cases);
 return 0;
}
