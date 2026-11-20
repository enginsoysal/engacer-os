#ifndef ENGINE_WINQUEUE144_H
#define ENGINE_WINQUEUE144_H
#include <engine/winui144.h>
/* Caller serializes access. No allocation, foreign pointers or timer polling. */
typedef struct {wui_message144 items[WUI_QUEUE144];uint32_t count,quit,quit_code;wui_filter144 waiting;uint8_t keys[256];uint32_t modifiers_sent145;} wui_queue144;
_Static_assert(sizeof(wui_queue144)<=4096,"A GUI queue must fit one lazy page");
static inline unsigned wui_matches144(const wui_message144*m,const wui_filter144*f){
 if(m->message==0x12)return 1;
 return (!f->window||(f->window==UINT64_MAX?!m->window:m->window==f->window))&&((!f->first&&!f->last)||(m->message>=f->first&&m->message<=f->last));
}
static inline int wui_push144(wui_queue144*q,const wui_message144*m,unsigned native){
 /* Only an adjacent motion can be replaced without moving it past a key. */
 if(native&&q->count&&m->message==0x200){wui_message144*last=q->items+q->count-1;if(last->message==m->message&&last->window==m->window){*last=*m;return 1;}}
 if(q->count>=(native?WUI_QUEUE144:WUI_APP_QUEUE144))return 0;
 q->items[q->count++]=*m;return 1;
}
static inline int wui_find144(const wui_queue144*q,const wui_filter144*f){for(unsigned i=0;i<q->count;++i)if(wui_matches144(q->items+i,f))return (int)i;return -1;}
static inline void wui_remove144(wui_queue144*q,unsigned i){if(i>=q->count)return;for(;i+1<q->count;++i)q->items[i]=q->items[i+1];--q->count;}
static inline void wui_purge144(wui_queue144*q,uint64_t window){for(unsigned i=0;i<q->count;)if(q->items[i].window==window)wui_remove144(q,i);else ++i;}
#endif
