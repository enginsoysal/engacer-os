#define W8_USER
#include <engine/winqueue144.h>
static wui_queue144 queue;
__declspec(dllexport) void reset144(void){queue.count=queue.quit=queue.quit_code=0;}
__declspec(dllexport) unsigned push144(const wui_message144*m,unsigned native){return (unsigned)wui_push144(&queue,m,native);}
__declspec(dllexport) unsigned peek144(const wui_filter144*f,wui_message144*out){int i=wui_find144(&queue,f);if(i<0)return 0;*out=queue.items[i];if(f->remove)wui_remove144(&queue,(unsigned)i);return 1;}
__declspec(dllexport) unsigned count144(void){return queue.count;}
__declspec(dllexport) void purge144(uint64_t window){wui_purge144(&queue,window);}
