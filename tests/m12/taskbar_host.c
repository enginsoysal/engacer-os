#include <engine/ui/taskbar12.h>
static unsigned checks;
unsigned taskbar12_total(void){return checks;}
unsigned taskbar12_checks(void){
#define CHECK(x) do{++checks;if(!(x))return checks;}while(0)
 struct {unsigned before,list[T12_APPS],after;} data={.before=0x12345678,.after=0x87654321};unsigned count=0;
 taskbar12_add(data.list,&count,1);taskbar12_add(data.list,&count,2);taskbar12_add(data.list,&count,1);taskbar12_add(data.list,&count,7);
 CHECK(count==3&&data.list[0]==1&&data.list[1]==2&&data.list[2]==7);
 taskbar12_add(data.list,&count,0);taskbar12_add(data.list,&count,20);CHECK(count==3);
 for(unsigned i=1;i<20;++i)taskbar12_add(data.list,&count,i);
 CHECK(count==19);for(unsigned i=0;i<19;++i)for(unsigned j=i+1;j<19;++j)CHECK(data.list[i]!=data.list[j]);
 for(unsigned i=0;i<100;++i)taskbar12_add(data.list,&count,3);
 CHECK(count==19&&data.before==0x12345678&&data.after==0x87654321);
 CHECK(taskbar12_visible(800,3)==3);CHECK(taskbar12_visible(800,16)==3);
 for(unsigned width=800;width<=8192;++width)for(unsigned apps=0;apps<20;++apps){
  unsigned visible=taskbar12_visible(width,apps);CHECK(visible<=apps);
  unsigned used=112+visible*140+(visible<apps?108:0);CHECK(used<=width-(width>=1000?180u:0u)-32);
 }
 CHECK(taskbar12_visible(0,19)==0);CHECK(taskbar12_visible(144,19)==0);
 CHECK(taskbar12_visible(0x80000000u,19)==19);CHECK(taskbar12_visible(0xffffffffu,19)==19);
 unsigned order[T12_APPS]={0},used=0,first[]={3,5,13},focus[]={5,13,3},changed[]={5,3,7};
 taskbar12_sync(order,&used,first,3);CHECK(used==3&&order[0]==3&&order[1]==5&&order[2]==13);
 taskbar12_sync(order,&used,focus,3);CHECK(used==3&&order[0]==3&&order[1]==5&&order[2]==13);
 taskbar12_sync(order,&used,changed,3);CHECK(used==3&&order[0]==3&&order[1]==5&&order[2]==7);
 taskbar12_sync(order,&used,0,0);CHECK(used==0);
 unsigned invalid[]={0,20,0xffffffffu,7,7};taskbar12_sync(order,&used,invalid,5);CHECK(used==1&&order[0]==7);
 used=21;taskbar12_sync(order,&used,first,3);CHECK(used==3&&order[0]==3&&order[1]==5&&order[2]==13);
 return 0;
}
