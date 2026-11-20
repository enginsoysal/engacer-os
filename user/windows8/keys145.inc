/* Query this UI thread's consumed-input state, not live hardware or posted keys. */
static int16_t MS f_GetKeyState(int key){if(key<0||key>255){last8(87);return 0;}int64_t result=ui_call144(WUI_KEYSTATE145,(unsigned)key,0,0);if(result<0){last8((unsigned)-result);return 0;}return(int16_t)(((result&0x80)?0x8000:0)|(result&1));}
static int MS f_GetKeyboardState(uint8_t*keys){if(!keys){last8(87);return 0;}int64_t result=ui_call144(WUI_KEYSTATE145,0,keys,1);if(result<0){last8((unsigned)-result);return 0;}return 1;}

#include <engine/keymap145.h>
static unsigned MS f_MapVirtualKeyW(unsigned code,unsigned type){int64_t layout=ui_call144(WUI_KEYSTATE145,0,0,2);if(layout<0){last8((unsigned)-layout);return 0;}return keymap145(code,type,(unsigned)layout);}
