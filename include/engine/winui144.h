#ifndef ENGINE_WINUI144_H
#define ENGINE_WINUI144_H
#include <stdint.h>
#include <engine/ui/font-metrics148.h>
#include <engine/ui/image148.h>
#define WUI_WINDOWS144 128u
#define WUI_DEPTH146 32u
#define WUI_NATIVE_ROOTS144 8u
#define WUI_QUEUE144 64u
#define WUI_APP_QUEUE144 56u
#define WUI_HANDLE144 UINT64_C(0x5744000000000000)
enum {WUI_CREATE144=1,WUI_DESTROY144,WUI_UPDATE144,WUI_POST144,WUI_PEEK144,WUI_WAIT144,WUI_THREAD_POST144,WUI_QUERY144,WUI_QUIT144,WUI_METRICS144,WUI_CURSOR144,WUI_CLIPFORMAT144,WUI_CLIPNAME144,WUI_DRAW144,WUI_MEASURE144,WUI_TIMER144,WUI_FOCUS144,WUI_CAPTURE144,WUI_NORMAL144,WUI_MENUBAR145,WUI_MENUDRAW145,WUI_KEYSTATE145,WUI_CLIPBOARD146,WUI_PICKER146,WUI_ATOM147,WUI_MESSAGE148,WUI_FONT148,WUI_IMAGE148,WUI_FOREGROUND148};
enum {WCLIP_OPEN146=1,WCLIP_CLOSE146,WCLIP_EMPTY146,WCLIP_STATE146,WCLIP_READ146,WCLIP_WRITE146,WCLIP_OPEN_WINDOW146};
typedef struct {uint64_t revision,owner;uint32_t bytes,reserved;} wclip_state146;
typedef struct {uint64_t revision,buffer;uint32_t bytes,reserved;} wclip_transfer146;
#define WUI_KEY_SNAPSHOT145 0x80000000u
typedef struct {int32_t x,y,width,height;} wui_rect144;
/* Kind 4 carries at most 128 straight-alpha ARGB pixels, never a user pointer. */
typedef struct {wui_rect144 bounds,clip;uint32_t kind,color;union {char text[512];uint32_t pixels[128];};} wui_draw144;
typedef struct {uint32_t width,height,work_height,scale,base_x,base_y,pointer_x,pointer_y;} wui_metrics144;
typedef struct {uint64_t id,callback;uint32_t period,reserved;} wui_timer144;
/* Fixed-width copied IPC; these are not pointers into kernel memory. */
typedef struct {uint64_t window,wparam,lparam;uint32_t message,time;int32_t x,y;uint32_t reserved[2];} wui_message144;
typedef struct {uint64_t window;uint32_t first,last,remove,reserved;} wui_filter144;
typedef struct {uint64_t parent,owner;wui_rect144 bounds;uint32_t style,exstyle,visible,enabled;uint16_t title[128],class_name[64];} wui_description144;
/* menu_height occupies the former reserved word; the copied record size is stable. */
typedef struct {uint64_t handle;wui_description144 description;uint32_t process,thread,revision,menu_height;char caption[384];} wui_view144;
#ifndef W8_USER
unsigned w8_ui_at144(unsigned,wui_view144*);
#ifdef ENGINE_M14
unsigned w8_ui_image148(uint64_t,uint64_t,wui_image_view148*);
uint64_t w8_ui_foreground_request148(void);
void w8_ui_foreground_changed148(uint64_t);
#endif
unsigned w8_ui_draw_at144(uint64_t,unsigned,wui_draw144*);
unsigned w8_ui_input144(uint64_t,unsigned,uint64_t,uint64_t);
unsigned w8_ui_place144(uint64_t,wui_rect144,unsigned);
unsigned w8_ui_revision144(void);
unsigned w8_ui_cursor144(uint64_t);
uint64_t w8_ui_capture_root144(void);
unsigned w8_ui_normal144(uint64_t,wui_rect144*);
unsigned w8_ui_restore_max144(uint64_t);
unsigned w8_ui_visible_roots144(void);
unsigned w8_ui_style145(uint64_t,uint32_t *);
unsigned w8_ui_menuheight145(uint64_t);
unsigned w8_ui_menudraw_at145(uint64_t,unsigned,wui_draw144*);
unsigned w8_ui_modifiers145(uint64_t,unsigned);
#ifdef ENGINE_M14
unsigned w8_clipboard_native_allowed146(void);
unsigned w8_clipboard_native_readable146(void);
void w8_clipboard_native_changed146(void);
#endif
#endif
#endif
