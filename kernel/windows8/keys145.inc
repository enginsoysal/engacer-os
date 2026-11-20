#include <engine/winkeys145.h>
#include <engine/hardware10.h>
static unsigned ui_input_snapshot145(unsigned message){
#ifdef ENGINE_M14
 unsigned mouse=(message>=0x200&&message<=0x20e)||(message>=0xa0&&message<=0xad);
 if(mouse)return WUI_KEY_SNAPSHOT145|input14_pointer_snapshot();
 if(message>=0x100&&message<=0x109)return WUI_KEY_SNAPSHOT145|input146_key_snapshot();
#else
 (void)message;
#endif
 return 0;
}
static void ui_keys_initialize145(wui_queue144*q){
#ifdef ENGINE_M14
 unsigned state=input14_snapshot();wui_key_snapshot145(q->keys,state|(input14_pointer_snapshot()&0x700000),1);q->modifiers_sent145=(state>>8)&255;
#else
 (void)q;
#endif
}
