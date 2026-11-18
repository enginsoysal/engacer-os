#include <engine/hardware10.h>
/* Logical layout and bounded wheel events shared by native input providers. */
static unsigned layout10,caps10;static int wheel10;
void input10_toggle_caps(void){caps10^=1;}
unsigned input10_layout(void){return layout10;}
void input10_set_layout(unsigned value){if(value<2)layout10=value;}
unsigned input10_hid(unsigned code,unsigned shifted){
 if(layout10){
  static const char letters[26]={'a','x','j','e','.','u','i','d','c','h','t','n','m','b','r','l',39,'p','o','y','g','k',',','q','f',';'};
  unsigned c=0;if(code>=4&&code<=29)c=(uint8_t)letters[code-4];else if(code==45)c='[';else if(code==46)c=']';else if(code==47)c='/';else if(code==48)c='=';else if(code==51)c='s';else if(code==52)c='-';else if(code==54)c='w';else if(code==55)c='v';else if(code==56)c='z';
  if(c){if(c>='a'&&c<='z'){if(!!shifted!=!!caps10)c-=32;}else if(shifted){const char*plain="',.;[]/=-",*upper="\"<>:{}?+_";for(unsigned i=0;plain[i];++i)if(c==(uint8_t)plain[i]){c=(uint8_t)upper[i];break;}}return c;}
 }
 if(code>=4&&code<=29)return ((!!shifted!=!!caps10)?'A':'a')+code-4;
 if(code>=30&&code<=39)return (unsigned char)(shifted?"!@#$%^&*()":"1234567890")[code-30];
 if(code==41)return 27;if(code==40)return 10;if(code==42)return 8;if(code==43)return 9;if(code==44)return ' ';
 if(code==100)return shifted?'|':'\\';
 if(code>=45&&code<=56)return (unsigned char)(shifted?"_+{}|~:\"~<>?":"-=[]\\#;'`,./")[code-45];return 0;
}
void input10_wheel(int delta){
#ifdef ENGINE_M13
 if(delta)input13_note();
#endif
int old=__atomic_load_n(&wheel10,__ATOMIC_RELAXED),next;do{next=old+delta;if(next>32)next=32;if(next<-32)next=-32;}while(!__atomic_compare_exchange_n(&wheel10,&old,next,0,__ATOMIC_RELEASE,__ATOMIC_RELAXED));if(!old&&next)input_feed(138);}
int input10_take_wheel(void){return __atomic_exchange_n(&wheel10,0,__ATOMIC_ACQ_REL);}

#ifdef ENGINE_M11
static unsigned usb_modifiers11,legacy_modifiers11;
unsigned input11_modifiers(void){return usb_modifiers11|legacy_modifiers11;}
void input11_usb_modifiers(unsigned value){usb_modifiers11=((value&0x11)?1u:0u)|((value&0x22)?2u:0u)|((value&0x44)?4u:0u)|((value&0x88)?8u:0u);}
void input11_legacy_modifiers(unsigned value){legacy_modifiers11=value&15u;}
#endif

#ifdef ENGINE_M13
/* Physical holds are independent of translated keydowns and lock toggles. */
static uint64_t activity21;
static uint8_t legacy_pressed21[32];
static unsigned legacy_held21,usb_held21,pointer_held21,prefix21,pause21;
uint64_t input13_activity(void){return __atomic_load_n(&activity21,__ATOMIC_ACQUIRE);}
unsigned input13_held(void){return __atomic_load_n(&legacy_held21,__ATOMIC_ACQUIRE)||__atomic_load_n(&usb_held21,__ATOMIC_ACQUIRE)||__atomic_load_n(&pointer_held21,__ATOMIC_ACQUIRE);}
void input13_note(void){__atomic_fetch_add(&activity21,1,__ATOMIC_RELEASE);}
void input13_legacy_key(unsigned code){
 if(pause21){--pause21;return;}if(code==0xe1){pause21=5;prefix21=0;input13_note();return;}if(code==0xe0){prefix21=128;return;}if(code==0xfa||code==0xfe)return;
 unsigned key=(code&127)+prefix21;prefix21=0;unsigned mask=1u<<(key&7),old=legacy_pressed21[key>>3]&mask;
 if(code&128){if(old){legacy_pressed21[key>>3]&=(uint8_t)~mask;__atomic_fetch_sub(&legacy_held21,1,__ATOMIC_RELEASE);input13_note();}}
 else{if(!old){legacy_pressed21[key>>3]|=(uint8_t)mask;__atomic_fetch_add(&legacy_held21,1,__ATOMIC_RELEASE);}input13_note();}
}
void input13_usb_keyboard(unsigned changed,unsigned held){__atomic_store_n(&usb_held21,held,__ATOMIC_RELEASE);if(changed)input13_note();}
void input13_pointer(int dx,int dy,unsigned buttons){unsigned old=__atomic_exchange_n(&pointer_held21,buttons&7,__ATOMIC_ACQ_REL);if(dx||dy||old!=(buttons&7))input13_note();}
#endif
