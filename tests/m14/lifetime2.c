/* Host check of the production callback dispatcher, not native acceptance. */
#include "runtime.h"
#include "module142.h"
#define MODULES141 32
static module141 modules141[MODULES141];
static unsigned terminating142;
#include "lifetime142.inc"
static unsigned observed[32],calls,bad;
static int MS notify(void*base,unsigned reason,void*reserved){
 unsigned id=0;for(unsigned i=0;i<MODULES141;++i)if(modules141[i].base==base){id=i;break;}
 if(reason||!reserved||modules141[id].attached)bad=1;
 observed[calls++]=id;
 /* Recursive cleanup must never notify another DLL twice. */
 pe8_shutdown();return 1;
}
__declspec(dllexport) unsigned test_lifetime(void){
 calls=bad=terminating142=0;
 for(unsigned i=0;i<sizeof(modules141);++i)((volatile unsigned char*)modules141)[i]=0;
 for(unsigned i=0;i<6;++i){module141*m=modules141+i;m->state=2;m->attached=1;m->dll=i!=0;m->entry=1;m->base=(void*)((uintptr_t)notify-1);m->sequence=i+1;}
 /* Give each callback a distinct identity while preserving the same entry. */
 for(unsigned i=0;i<6;++i){modules141[i].base=(void*)((uintptr_t)notify-16-i);modules141[i].entry=16+i;}
 modules141[2].attached=0; /* Already unloaded: no second notification. */
 modules141[3].entry=0; /* A resource-only DLL has no callback. */
 pe8_shutdown();pe8_shutdown();
 if(bad||calls!=3||observed[0]!=5||observed[1]!=4||observed[2]!=1)return 1;
 for(unsigned i=0;i<6;++i)if(modules141[i].attached)return 2;
 /* Shutdown cannot unmap a dependency while other callbacks still use it. */
 for(unsigned i=0;i<6;++i)if(modules141[i].state!=2||!modules141[i].base)return 3;
 return 0;
}
