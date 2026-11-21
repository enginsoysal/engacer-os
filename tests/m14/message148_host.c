#include <assert.h>
#include <string.h>
#include <engine/winmessage148.h>
int main(void){
 watom_table147 table={0},atoms={0};
 uint16_t task[]={'T','a','s','k','b','a','r','C','r','e','a','t','e','d'};
 int id=wmessage_register148(&table,task,14);assert(id==0xc000);
 unsigned used=table.used;
 for(unsigned i=0;i<70000;++i)assert(wmessage_register148(&table,task,14)==id);
 assert(table.used==used&&table.references[0]==1);
 uint16_t number[]={'#','1'};
 assert(wmessage_register148(&table,number,2)==0xc001);
 assert(watom_add147(&atoms,task,14,watom_case147)==0xc000);
 assert(!watom_delete147(&atoms,0xc000));
 assert(wmessage_register148(&table,task,14)==id);
 uint16_t unicode[]={0xd83d,0xde80};
 assert(wmessage_register148(&table,unicode,2)==0xc002);
 assert(wmessage_register148(&table,unicode,1)==-87);
 assert(wmessage_register148(&table,0,0)==-87);
 for(unsigned i=3;i<64;++i){uint16_t name[]={0x400,(uint16_t)(0x500+i)};assert(wmessage_register148(&table,name,2)==(int)(0xc000+i));}
 watom_table147 before=table;uint16_t extra[]={0x777};
 assert(wmessage_register148(&table,extra,1)==-1816);
 assert(!memcmp(&before,&table,sizeof(table)));
 assert(wmessage_register148(&table,task,14)==id);
 memset(&table,0,sizeof(table));uint16_t longname[255];
 for(unsigned i=0;i<255;++i)longname[i]='a';
 for(unsigned i=0;i<7;++i){longname[0]=(uint16_t)('a'+i);assert(wmessage_register148(&table,longname,255)==(int)(0xc000+i));}
 before=table;longname[0]='z';assert(wmessage_register148(&table,longname,255)==-1816);
 assert(!memcmp(&before,&table,sizeof(table)));
 return 0;
}
