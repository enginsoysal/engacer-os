#ifndef ENGINE_KEYEVENT146_H
#define ENGINE_KEYEVENT146_H
#include <stdint.h>
/* Two bytes per queued key retain modifiers, Caps Lock and pre-control text. */
static inline uint16_t keyevent_pack146(unsigned snapshot,unsigned character){
 return(uint16_t)(((snapshot>>8)&255)|((character<128?character:0)<<8)|((snapshot&0x10000)?0x8000:0));
}
static inline unsigned keyevent_snapshot146(uint16_t event){
 unsigned raw=event&255;return(raw<<8)|((raw&0x11)?1u:0u)|((raw&0x22)?2u:0u)|((raw&0x44)?4u:0u)|((raw&0x88)?8u:0u)|((event&0x8000)?0x10000u:0u);
}
static inline unsigned keyevent_character146(uint16_t event){return(event>>8)&127;}
#endif
