/* One visual preview owner, five original values, and eight category bytes. */
enum {S13_APPEARANCE=59000,S13_DISPLAY,S13_INPUT,S13_SYSTEM,S13_ACCESS,S13_CANCEL=59005,S13_DEFAULTS,
 S13_ACCENT_DEFAULT=59010,S13_CLICK_FAST=59020,S13_CLICK_NORMAL,S13_CLICK_SLOW};
typedef struct {uint64_t owner;unsigned accent,dark,scale,wallpaper,pattern;} settings_preview_record13;
static settings_preview_record13 settings_preview13;
static uint8_t settings_page13[DESKTOP_WINDOWS];
static unsigned settings_invalid13;
static void settings_open13(uint64_t);
static unsigned settings_close13(uint64_t);
static void settings_draw13(desktop_window*,application*,uint64_t);
static unsigned settings_action13(uint64_t,unsigned);
static unsigned settings_key13(int);
_Static_assert(sizeof(settings_preview13)+sizeof(settings_page13)+sizeof(settings_invalid13)<=64,"bounded settings state");
