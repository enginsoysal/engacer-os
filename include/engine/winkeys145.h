#ifndef ENGINE_WINKEYS145_H
#define ENGINE_WINKEYS145_H
#include <engine/winui144.h>
/* Only broker-created input snapshots carry the valid bit. Posted messages do not. */
static inline void wui_key_snapshot145(uint8_t keys[256],unsigned snapshot,unsigned mouse){
 unsigned raw=(snapshot>>8)&255;static const uint8_t codes[8]={0xa2,0xa0,0xa4,0x5b,0xa3,0xa1,0xa5,0x5c};
 for(unsigned n=0;n<8;++n)keys[codes[n]]=(raw&(1u<<n))?0x80:0;
 keys[0x10]=(snapshot&2)?0x80:0;keys[0x11]=(snapshot&1)?0x80:0;keys[0x12]=(snapshot&4)?0x80:0;
 keys[0x14]=(keys[0x14]&0x80)|((snapshot>>16)&1);
 if(mouse){keys[1]=(snapshot&0x100000)?0x80:0;keys[2]=(snapshot&0x200000)?0x80:0;keys[4]=(snapshot&0x400000)?0x80:0;}
}
static inline void wui_key_commit145(uint8_t keys[256],const wui_message144*m){
 if(!(m->reserved[1]&WUI_KEY_SNAPSHOT145))return;unsigned message=m->message;unsigned mouse=(message>=0x200&&message<=0x20e)||(message>=0xa0&&message<=0xad);
 wui_key_snapshot145(keys,m->reserved[1],mouse);
 if((message==0x100||message==0x101||message==0x104||message==0x105)&&m->wparam<256){unsigned key=(unsigned)m->wparam;
  if((key>=0x10&&key<=0x12)||(key>=0xa0&&key<=0xa5)||key==0x5b||key==0x5c)return;
  unsigned down=message==0x100||message==0x104;if(down&&(key==0x90||key==0x91)&&!(keys[key]&0x80))keys[key]^=1;
  keys[key]=(keys[key]&1)|(down?0x80:0);
 }
}
#endif
