/* One global flyout, backed by existing providers; not another app/window. */
enum {TR12_OPEN=58000,TR12_QUICK,TR12_USB,TR12_CALENDAR,TR12_NETWORK,TR12_SOUND,TR12_DATE,TR12_CLOSE,TR12_USB_OPEN,
 TR12_QUIETER=58010,TR12_LOUDER,TR12_MUTE,TR12_RETRY,TR12_DEVICES,TR12_SETTINGS,TR12_MEDIA,
 TR12_MONTH_PREV=58020,TR12_MONTH_NEXT,TR12_TODAY,TR12_CALENDAR_APP,
 TR12_USB_PREV=58030,TR12_USB_NEXT,TR12_REFRESH,
 TR12_DAY=58100,TR12_DRIVE=58200,TR12_EJECT=58220,TR12_END=58300};
static unsigned tray_open12,tray_focus12,tray_usb_page12,tray_year12,tray_month12,tray_day12,tray_previous_volume12;
static desktop_rect tray_bounds12;
static char tray_notice12[160];
static void tray_bar12(int);
static void tray_draw12(void);
static void tray_close12(void);
static void tray_changed12(void);
static unsigned tray_action12(uint64_t,unsigned);
static unsigned tray_key12(int);
static i11_target tray_target12(int,int);

_Static_assert(TR12_DAY+31<TR12_DRIVE&&TR12_EJECT+STORAGE_MAX<TR12_END,"disjoint tray actions");
_Static_assert(sizeof(tray_notice12)+sizeof(tray_bounds12)+7*sizeof(unsigned)<=256,"bounded flyout state");
