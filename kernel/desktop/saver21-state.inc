/* Optional presentation feature, not an authentication or power-management service. */
enum { S21_OPEN=60200,S21_OFF,S21_ON,S21_MINUTE,S21_FIVE,S21_TEN,
 S21_LOGO,S21_CLOCK,S21_BLANK,S21_PREVIEW,S21_APPLY,S21_CANCEL,S21_DEFAULTS,S21_BACK };
typedef struct {unsigned magic,version,enabled,seconds,style;} saver_record21;
static saver_record21 saver_saved21,saver_draft21;
static uint64_t saver_owner21,saver_input21,saver_idle21,saver_frame21,saver_quiet21;
/* 0 desktop, 1 wait for preview activation release, 2 saver, 3 consume wake gesture. */
static unsigned saver_phase21,saver_style21,saver_invalid21;
static void saver_load21(void);
static void saver_cancel21(uint64_t);
static unsigned saver_action21(uint64_t,unsigned);
static void saver_settings21(desktop_window*,application*,uint64_t,int,int,int);
static unsigned saver_work21(int);
static unsigned saver_capture21(int);
static void saver_draw21(void);
_Static_assert(sizeof(saver_record21)==20,"versioned screensaver record");
_Static_assert(sizeof(saver_saved21)+sizeof(saver_draft21)+5*sizeof(uint64_t)+3*sizeof(unsigned)<=96,"bounded screensaver state");
