#ifndef ENGACER_TASKBAR12_H
#define ENGACER_TASKBAR12_H
#define T12_APPS 20u
/* Preserve pin/MRU order while deriving a bounded unique app union. */
static inline void taskbar12_add(unsigned *list,unsigned *count,unsigned app){
 if(!app||app>=T12_APPS||*count>=T12_APPS)return;
 for(unsigned i=0;i<*count;++i)if(list[i]==app)return;
 list[(*count)++]=app;
}
static inline unsigned taskbar12_visible(unsigned width,unsigned count){
 unsigned reserve=(width>=1000?180u:0u)+32u+112u;
 unsigned space=width>reserve?width-reserve:0;
 unsigned visible=space/140;
 if(visible<count)visible=space>108?(space-108)/140:0;
 return visible<count?visible:count;
}
#endif
