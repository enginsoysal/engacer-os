/* Temporary category search belongs to a live Settings window generation. */
static unsigned settings_scale_fits18(unsigned);
static void settings_restore_scale18(void);
enum {S18_SEARCH=61200,S18_CLEAR,S18_RESULT=61210};
typedef struct {uint64_t owner;char query[64];unsigned cursor,anchor,active;} settings_search_record18;
static settings_search_record18 settings_search18[DESKTOP_WINDOWS];
_Static_assert(sizeof(settings_search18)<=704,"bounded Settings search; no index worker");
