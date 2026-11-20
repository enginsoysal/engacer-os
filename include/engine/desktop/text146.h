#ifndef ENGINE_DESKTOP_TEXT146_H
#define ENGINE_DESKTOP_TEXT146_H
#include <stdint.h>
/* Streaming UTF-8 validation retains at most one scalar across storage pages. */
typedef struct {uint32_t value,minimum;unsigned remaining;} text_decoder146;
static inline unsigned text_byte146(text_decoder146*s,unsigned byte){
 if(!s->remaining){
  if(byte<128)return byte>=32||byte==9||byte==10||byte==13;
  if(byte>=0xc2&&byte<=0xdf){s->value=byte&31;s->minimum=128;s->remaining=1;return 1;}
  if(byte>=0xe0&&byte<=0xef){s->value=byte&15;s->minimum=2048;s->remaining=2;return 1;}
  if(byte>=0xf0&&byte<=0xf4){s->value=byte&7;s->minimum=65536;s->remaining=3;return 1;}return 0;
 }
 if((byte&0xc0)!=0x80)return 0;s->value=(s->value<<6)|(byte&63);
 if(--s->remaining)return 1;return s->value>=s->minimum&&s->value<=0x10ffff&&!(s->value>=0xd800&&s->value<=0xdfff);
}
static inline unsigned text_valid146(const char*text,unsigned bytes){text_decoder146 s={0};for(unsigned i=0;i<bytes;++i)if(!text_byte146(&s,(uint8_t)text[i]))return 0;return !s.remaining;}
static inline unsigned text_previous146(const char*text,unsigned at){if(at){--at;while(at&&((uint8_t)text[at]&0xc0)==0x80)--at;}return at;}
static inline unsigned text_next146(const char*text,unsigned at,unsigned bytes){if(at<bytes){++at;while(at<bytes&&((uint8_t)text[at]&0xc0)==0x80)++at;}return at;}
#endif
