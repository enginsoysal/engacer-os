/* Bounded provider locations. A USB context is the driver's generation lease. */
#ifndef ENGACER_FILES12_H
#define ENGACER_FILES12_H
#include <stdint.h>
enum {UI12_NATIVE=0,UI12_USB_DRIVES=1,UI12_USB_FOLDER=2,UI12_FILE_HISTORY=8};
enum {F12_REFRESH=50000,F12_USB_ROOT};
typedef struct {char path[256];unsigned provider,disk,context,part,offset;} ui12_file_location;
typedef struct {ui12_file_location locations[UI12_FILE_HISTORY];unsigned count,position;} ui12_file_history;
static inline unsigned ui12_location_equal(const ui12_file_location*a,const ui12_file_location*b){
 if(a->provider!=b->provider)return 0;
 if(a->provider==UI12_USB_DRIVES)return 1;
 if(a->provider==UI12_USB_FOLDER&&(a->disk!=b->disk||a->context!=b->context||a->part!=b->part))return 0;
 for(unsigned i=0;i<256;++i){if(a->path[i]!=b->path[i])return 0;if(!a->path[i])return 1;}return 0;
}
static inline void ui12_history_push(ui12_file_history*h,const ui12_file_location*before,const ui12_file_location*after){
 if(h->count>UI12_FILE_HISTORY||h->position>=h->count){h->count=h->position=0;}
 if(h->count){h->locations[h->position]=*before;if(ui12_location_equal(before,after)){h->locations[h->position]=*after;return;}h->count=h->position+1;}
 if(h->count==UI12_FILE_HISTORY){for(unsigned i=1;i<UI12_FILE_HISTORY;++i)h->locations[i-1]=h->locations[i];--h->count;}
 h->locations[h->count]=*after;h->position=h->count++;
}
static inline unsigned ui12_history_can(const ui12_file_history*h,int forward){return h->count&&h->count<=UI12_FILE_HISTORY&&h->position<h->count&&(forward?h->position+1<h->count:h->position!=0);}
static inline unsigned ui12_usb_rows(int height){int rows=(height-266)/44;if(rows<1)rows=1;if(rows>6)rows=6;return(unsigned)rows;}
#endif
