#ifndef ENGINE_KEYMAP145_H
#define ENGINE_KEYMAP145_H
#include <stdint.h>
#include <engine/keymap-us145.inc>
/* Native Dvorak remaps logical keys exactly as input10_hid does. */
static inline unsigned keymap_logical145(unsigned vk,unsigned layout){
 if(!layout)return vk;
 if(vk>='A'&&vk<='Z'){static const uint8_t logical[26]={'A','X','J','E',0xbe,'U','I','D','C','H','T','N','M','B','R','L',0xde,'P','O','Y','G','K',0xbc,'Q','F',0xba};return logical[vk-'A'];}
 switch(vk){case 0xbd:return 0xdb;case 0xbb:return 0xdd;case 0xdb:return 0xbf;case 0xdd:return 0xbb;case 0xba:return 'S';case 0xde:return 0xbd;case 0xbc:return 'W';case 0xbe:return 'V';case 0xbf:return 'Z';default:return vk;}
}
static inline unsigned keymap_scan145(unsigned code,unsigned layout){
 unsigned low=code&255,vk=0;if(low>=128)return 0;
 if(code<128)vk=keymap_us_plain145[low];else if((code&~255u)==0xe000)vk=keymap_us_e0145[low];else if((code&~255u)==0xe100)vk=keymap_us_e1145[low];
 return keymap_logical145(vk,layout);
}
static inline unsigned keymap145(unsigned code,unsigned type,unsigned layout){
 if(type==1||type==3){unsigned vk=keymap_scan145(code,layout);if(type==1){if(vk==0xa0||vk==0xa1)return 0x10;if(vk==0xa2||vk==0xa3)return 0x11;if(vk==0xa4||vk==0xa5)return 0x12;}return vk;}
 if(code>255)return 0;if(type==2)return keymap_us_char145[code];if(type!=0&&type!=4)return 0;
 if(layout&&((code>='A'&&code<='Z')||(code>=0xba&&code<=0xc0)||(code>=0xdb&&code<=0xde))){for(unsigned scan=1;scan<128;++scan)if(keymap_scan145(scan,layout)==code)return scan;return 0;}
 return type==4?keymap_us_vk_ext145[code]:keymap_us_vk_scan145[code];
}
#endif
