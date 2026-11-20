#ifndef ENGINE_HARDWARE10_H
#define ENGINE_HARDWARE10_H
#include <engine/storage.h>
enum {HW10_DISCOVERED,HW10_READY,HW10_LIMITED,HW10_UNAVAILABLE};
enum {HW10_READ=1,HW10_WRITE=2,HW10_FLUSH=4,HW10_INPUT=8,HW10_DISPLAY=16,HW10_NETWORK=32};
typedef struct {unsigned bdf,vendor,product,class_code,state,capabilities;const char *name,*detail;} hw10_device;
typedef struct {unsigned active,bdf,status,keyboards,mice,disks,hubs;uint64_t pages,keys,motion;} usb10_info;
void hw10_refresh(void);
unsigned hw10_count(void);
const hw10_device *hw10_get(unsigned);
usb10_info usb10_current(void);
unsigned usb10_eject(unsigned,unsigned);
unsigned input10_layout(void);
#ifdef ENGINE_M11
unsigned input11_modifiers(void);
unsigned input11_pointer_modifiers(void);
uint64_t input11_pointer_ms(void);
void input11_usb_modifiers(unsigned);
void input11_legacy_modifiers(unsigned);
#endif
#ifdef ENGINE_M13
uint64_t input13_activity(void);
unsigned input13_held(void);
void input13_note(void);
void input13_legacy_key(unsigned);
void input13_usb_keyboard(unsigned,unsigned);
void input13_pointer(int,int,unsigned);
#endif
void input10_toggle_caps(void);
#ifdef ENGINE_M14
unsigned input14_snapshot(void);
unsigned input14_pointer_snapshot(void);
void input_feed_key146(uint8_t,unsigned);
void input146_begin_key(void);
void input146_end_key(void);
unsigned input146_key_snapshot(void);
unsigned input146_key_character(void);
#endif
void input10_set_layout(unsigned);
unsigned input10_hid(unsigned,unsigned);
void input10_wheel(int);
int input10_take_wheel(void);
typedef struct {char name[256];unsigned kind;uint32_t size;} rem10_entry;
unsigned rem10_volume(unsigned,unsigned*,unsigned*);
unsigned rem10_list(unsigned,unsigned,unsigned,const char*,unsigned,rem10_entry*,unsigned,unsigned*);
unsigned rem10_export(unsigned,unsigned,unsigned,const char*,const char*);
unsigned rem10_import(unsigned,unsigned,unsigned,const char*,const char*);
#ifdef ENGINE_M12
unsigned rem12_read_begin(unsigned,unsigned,unsigned,const char*,uint64_t*);
unsigned rem12_read_next(void*,unsigned);
void rem12_read_close(void);
#endif
#endif
