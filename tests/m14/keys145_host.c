#define W8_USER 1
#include <engine/winkeys145.h>
#include <engine/winqueue144.h>
__declspec(dllexport) unsigned queue_size145(void){return sizeof(wui_queue144);}
__declspec(dllexport) unsigned state145(unsigned raw,unsigned flags,unsigned message,unsigned key,unsigned posted){
 uint8_t keys[256]={0};wui_message144 m={0};m.message=message;m.wparam=key;m.reserved[1]=posted?0:WUI_KEY_SNAPSHOT145|(raw<<8)|flags;wui_key_commit145(keys,&m);unsigned result=0;static const uint8_t codes[8]={0xa2,0xa0,0xa4,0x5b,0xa3,0xa1,0xa5,0x5c};for(unsigned n=0;n<8;++n)if(keys[codes[n]]&0x80)result|=1u<<n;result|=(unsigned)(keys[0x10]>>7)<<8;result|=(unsigned)(keys[0x11]>>7)<<9;result|=(unsigned)(keys[0x12]>>7)<<10;result|=(unsigned)(keys[1]>>7)<<11;result|=(unsigned)(keys[2]>>7)<<12;result|=(unsigned)(keys[4]>>7)<<13;result|=(keys[0x14]&1)<<14;result|=(unsigned)(keys['A']>>7)<<15;return result;
}
