#include <engine/winpicker146.h>
#include <engine/desktop/text146.h>
/* One native owner dialog; source IDs and locations, never file payloads. */
enum {P12_TEXT_OPEN=1,P12_TEXT_SAVE,P12_IMAGE_OPEN,P12_ZIP_OPEN,P12_ZIP_FOLDER,P12_WINDOWS_INSPECT,P12_FOREIGN_OPEN146,P12_FOREIGN_SAVE146,P12_WINDOWS_MSI147};
enum {P12_OPEN=54000,P12_SAVE_AS,P12_EXTRACT_TO,
 P12_CANCEL=54010,P12_ACCEPT,P12_BACK,P12_FORWARD,P12_UP,P12_HOME,P12_DOCUMENTS,
 P12_DOWNLOADS,P12_PICTURES,P12_ADDRESS,P12_NAME,P12_FILTER,P12_PREVIOUS,P12_NEXT,
 P12_NEW_FOLDER,P12_REPLACE,P12_REVIEW_BACK,P12_SAVE_OPEN,P12_DISCARD_OPEN,
 P12_ROW=55000};
enum {P12_DIALOG=10,P12_REPLACE_REVIEW=1,P12_DIRTY_REVIEW,P12_FOLDER_REVIEW};
typedef struct {
 unsigned purpose,phase,filter,selected,offset,count,rows,history_count,history_position;
 unsigned address_cursor,address_anchor,name_cursor,name_anchor;
 uint64_t generation,target_first,target_size,selected_first,selected_size;uint32_t target_crc,selected_crc,selected_kind;
 char path[256],address[256],name[256],pending[256],selected_path[256],error[160];
 char history[8][256];uint16_t order[V6_ENTRIES];
} picker_state12;
typedef struct {uint64_t magic;uint32_t version,reserved;char paths[3][256];uint32_t crc,padding;} picker_preferences12;
_Static_assert(sizeof(picker_state12)<=8192,"One bounded shared picker");
_Static_assert(sizeof(picker_preferences12)==792,"Versioned optional dialog locations");
static picker_state12 picker12;
static picker_preferences12 picker_preferences;
static unsigned picker_preferences_loaded12;
static void picker_begin12(uint64_t,unsigned);
static unsigned picker_action12(uint64_t,unsigned);
static unsigned picker_key12(int);
static unsigned picker_dispatch12(i11_target,unsigned);
static unsigned picker_control12(uint64_t,unsigned);
static unsigned picker_draw12(void);
static unsigned picker_shortcut12(int);
static unsigned picker_busy12(void);

static uint64_t picker_foreign_generation146;
static unsigned picker_foreign12(void){return picker12.purpose==P12_FOREIGN_OPEN146||picker12.purpose==P12_FOREIGN_SAVE146;}
static unsigned picker_saving12(void){return picker12.purpose==P12_TEXT_SAVE||picker12.purpose==P12_FOREIGN_SAVE146;}
static unsigned picker_foreign_accept146(unsigned);
static void picker_foreign_sync146(void);
static void picker_foreign_cancel146(void);
static const char*picker_foreign_title146(const char*);
static const char*picker_foreign_filter146(const char*);
