#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <engine/ui/fileview12.h>
int main(void){
 const char*names[]={"","a","A","a0","a00","a1","a01","a2","a10","a0000000000000000000000010","a9999999999999999999999999","a10000000000000000000000000",".config","item.txt","Item.TXT","item.bmp","other.txt"};
 unsigned count=sizeof(names)/sizeof(*names),pairs=0,triples=0,layouts=0;
 for(unsigned key=0;key<3;++key)for(unsigned reverse=0;reverse<2;++reverse)for(unsigned i=0;i<count;++i)for(unsigned j=0;j<count;++j){
  int a=ui12_file_order(names[i],1,i*17,i,names[j],1,j*17,j,key,reverse),b=ui12_file_order(names[j],1,j*17,j,names[i],1,i*17,i,key,reverse);assert((a<0)==(b>0)&&(a>0)==(b<0));++pairs;
  for(unsigned k=0;k<count;++k){int c=ui12_file_order(names[j],1,j*17,j,names[k],1,k*17,k,key,reverse),d=ui12_file_order(names[i],1,i*17,i,names[k],1,k*17,k,key,reverse);if(a<=0&&c<=0)assert(d<=0);++triples;}
  assert(ui12_file_order(names[i],2,999,80,names[j],1,0,1,key,reverse)<0);
 }
 assert(ui12_file_natural("File2","File10")<0);assert(ui12_file_natural("File2","File02")<0);
 assert(ui12_file_natural("9999999999999999999999999","10000000000000000000000000")<0);
 assert(ui12_file_order("same",1,1,2,"SAME",1,1,7,0,1)<0);
 assert(!strcmp(ui12_file_extension(".config"),""));assert(!strcmp(ui12_file_extension("a.b.txt"),"txt"));
 assert(!strcmp(ui12_file_type("a.MD",1),ui12_file_type("b.txt",1)));assert(ui12_file_order("a.txt",1,0,1,"b.md",1,0,2,2,0)<0);
 for(int width=300;width<=1920;++width){ui12_file_columns c=ui12_file_details(width);assert(c.name>=192);if(c.size_visible)assert(c.size==96);if(c.type_visible)assert(c.type==148&&width>=560);assert(c.name+(c.size_visible?108:0)+(c.type_visible?160:0)==width);
  for(int height=100;height<=1800;height+=11)for(unsigned icons=0;icons<2;++icons){unsigned cols=ui12_file_columns_count(width,icons),rows=ui12_file_rows_count(height,icons),native=ui12_file_page_count(width,height,icons,0),usb=ui12_file_page_count(width,height,icons,1);assert(cols>=1&&rows>=1&&native>=1&&native<=128&&usb>=1&&usb<=6);++layouts;}}
 printf("PASS: %u comparator pairs, %u transitivity triples, folders-first/reverse/stable identities, unbounded numeric strings and %u responsive layouts.\n",pairs,triples,layouts);return 0;
}
