#ifndef ENGACER_TASKBAR12_H
#define ENGACER_TASKBAR12_H
#define T12_APPS 20u
/* Preserve pin/MRU order while deriving a bounded unique app union. */
static inline void taskbar12_add(unsigned *list,unsigned *count,unsigned app){
 if(!app||app>=T12_APPS||*count>=T12_APPS)return;
 for(unsigned i=0;i<*count;++i)if(list[i]==app)return;
 list[(*count)++]=app;
}
/* Z-order changes must not reorder existing app buttons. Reconcile presence,
 * preserving first appearance until the app's final window disappears. */
static inline void taskbar12_sync(unsigned *order,unsigned *count,const unsigned *live,unsigned live_count){
 unsigned mask=0;
 for(unsigned i=0;i<live_count;++i)if(live[i]&&live[i]<T12_APPS)mask|=1u<<live[i];
 if(*count>T12_APPS)*count=0;
 unsigned kept=0;
 for(unsigned i=0;i<*count;++i)if(order[i]&&order[i]<T12_APPS&&(mask&(1u<<order[i])))order[kept++]=order[i];
 *count=kept;
 for(unsigned i=0;i<live_count;++i)taskbar12_add(order,count,live[i]);
}
static inline unsigned taskbar12_visible(unsigned width,unsigned count){
 unsigned reserve=(width>=1000?180u:0u)+32u+112u;
 unsigned space=width>reserve?width-reserve:0;
 unsigned visible=space/140;
 if(visible<count)visible=space>108?(space-108)/140:0;
 return visible<count?visible:count;
}
#endif
