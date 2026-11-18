/* Per-window, generation-bound filename filter. No index, worker or heap cache. */
enum {F17_FILTER=61000,F17_CLEAR};
typedef struct {uint64_t owner;char query[64];unsigned cursor,anchor,active;} file_filter17;
static file_filter17 file_filters17[DESKTOP_WINDOWS];
_Static_assert(sizeof(file_filters17)<=768,"bounded current-folder filter state");
static file_filter17 *files_filter17_for(unsigned);
static unsigned files_filter17_matches(unsigned,const v6_entry*);
static void files_filter17_clear(application*);
static unsigned files_filter17_action(uint64_t,unsigned);
static unsigned files_filter17_key(desktop_window*,application*,uint64_t,int);
static unsigned files_sidebar_width17(const desktop_window*);
