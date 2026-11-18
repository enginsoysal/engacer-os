#include <assert.h>
#include <stdio.h>
#include <engine/ui/desktop12.h>
static int intersects(ui12_desktop_cell a,ui12_desktop_cell b){
 return a.x<b.x+b.width&&a.x+a.width>b.x&&a.y<b.y+b.height&&a.y+a.height>b.y;
}
int main(void){
 unsigned layouts=0,objects=0,keys=0;
 for(unsigned height=480;height<=2160;height+=17)for(unsigned width=640;width<=3840;width+=31){
  ui12_desktop_cell cells[132];unsigned count=ui12_desktop_capacity(width,height);
  assert(count&&count<=128);
  for(unsigned i=0;i<count+4;++i){
   cells[i]=ui12_desktop_position(height,i<4?i:i-4,i<4);
   assert(cells[i].x>=0&&cells[i].x+cells[i].width<=(int)width);
   assert(cells[i].y>=24&&cells[i].y+cells[i].height<=(int)height-148);
   for(unsigned j=0;j<i;++j)assert(!intersects(cells[i],cells[j]));
   ++objects;
  }
  ++layouts;
 }
 for(unsigned height=480;height<=2160;height+=17)for(unsigned total=4;total<=132;total+=7){
  for(unsigned from=0;from<total;++from)for(unsigned k=0;k<4;++k){
   unsigned key=(unsigned[]){128,129,133,134}[k];
   unsigned next=ui12_desktop_neighbor(height,from,total,key);
   assert(next<total);ui12_desktop_cell a=ui12_desktop_position(height,from<4?from:from-4,from<4);
   ui12_desktop_cell b=ui12_desktop_position(height,next<4?next:next-4,next<4);
   if(next!=from){
    assert(k<2?a.y==b.y:a.x==b.x);
    assert(k==0?b.x<a.x:k==1?b.x>a.x:k==2?b.y<a.y:b.y>a.y);
   }
   /* Independent exhaustive oracle: no closer real object may exist. */
   int distance=next==from?0x7fffffff:(k<2?(b.x>a.x?b.x-a.x:a.x-b.x):(b.y>a.y?b.y-a.y:a.y-b.y));
   for(unsigned n=0;n<total;++n){ui12_desktop_cell c=ui12_desktop_position(height,n<4?n:n-4,n<4);
    if(k<2&&c.y==a.y){int delta=k==0?a.x-c.x:c.x-a.x;assert(delta<=0||delta>=distance);}
    if(k>=2&&c.x==a.x){int delta=k==2?a.y-c.y:c.y-a.y;assert(delta<=0||delta>=distance);}
   }
   ++keys;
  }
 }
 assert(ui12_desktop_neighbor(800,0,10,129)==4);
 assert(ui12_desktop_neighbor(800,4,10,128)==0);
 for(unsigned visible=0;visible<16;++visible)for(unsigned from=0;from<14;++from){
  if(from<4&&!(visible&(1u<<from)))continue;
  for(unsigned k=0;k<4;++k){
   unsigned key=(unsigned[]){128,129,133,134}[k];
   unsigned next=ui12_desktop_neighbor_visible(800,from,14,key,visible);
   assert(next<14&&(next>=4||(visible&(1u<<next))));
   ui12_desktop_cell a=ui12_desktop_position(800,from<4?from:from-4,from<4);
   ui12_desktop_cell b=ui12_desktop_position(800,next<4?next:next-4,next<4);
   int distance=next==from?0x7fffffff:(k<2?(b.x>a.x?b.x-a.x:a.x-b.x):(b.y>a.y?b.y-a.y:a.y-b.y));
   for(unsigned n=0;n<14;++n){
    if(n<4&&!(visible&(1u<<n)))continue;
    ui12_desktop_cell c=ui12_desktop_position(800,n<4?n:n-4,n<4);
    if(k<2&&c.y==a.y){int delta=k==0?a.x-c.x:c.x-a.x;assert(delta<=0||delta>=distance);}
    if(k>=2&&c.x==a.x){int delta=k==2?a.y-c.y:c.y-a.y;assert(delta<=0||delta>=distance);}
   }
   ++keys;
  }
 }
 assert(ui12_desktop_neighbor_visible(800,4,10,128,0)==4);
 printf("PASS: %u layouts, %u bounded non-overlapping objects, %u spatial-key cases.\n",layouts,objects,keys);
 return 0;
}
