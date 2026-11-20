#ifndef ENGINE_WINPICKER146_H
#define ENGINE_WINPICKER146_H
#include <stdint.h>
#define WPICK_FILTERS146 12u
#define WPICK_FILTER_TEXT146 1920u
#define WPICK_PATTERN146 256u
enum {WPICK_OPEN146=1,WPICK_SAVE146,WPICK_RESULT146,WPICK_WAIT146,WPICK_CANCEL146};
typedef struct {
 uint32_t size,pad0;uint64_t owner,instance,filter,custom_filter;uint32_t custom_capacity,filter_index;
 uint64_t file;uint32_t file_capacity,pad1;uint64_t file_title;uint32_t title_capacity,pad2;
 uint64_t initial_directory,title;uint32_t flags;uint16_t file_offset,file_extension;
 uint64_t default_extension,custom_data,hook,template_name,reserved_pointer;uint32_t reserved,flags_ex;
} wpick_ofn146;
_Static_assert(sizeof(wpick_ofn146)==152,"Classic Win64 OPENFILENAMEW layout");
typedef struct {uint16_t label,pattern;} wpick_filter146;
typedef struct {
 uint64_t generation,owner;uint32_t save,flags,filter_count,filter_index;
 char directory[256],name[256],title[128],extension[32],user_root[256],product_root[256];
 wpick_filter146 filters[WPICK_FILTERS146];char filter_text[WPICK_FILTER_TEXT146];
} wpick_view146;
static inline const char*wpick_label146(const wpick_view146*v,unsigned index){return index<v->filter_count&&v->filters[index].label<WPICK_FILTER_TEXT146?v->filter_text+v->filters[index].label:"";}
static inline const char*wpick_pattern146(const wpick_view146*v,unsigned index){return index<v->filter_count&&v->filters[index].pattern<WPICK_FILTER_TEXT146?v->filter_text+v->filters[index].pattern:"";}
#ifndef W8_USER
#include <engine/install/m6.h>
unsigned w8_picker_view146(wpick_view146*);
const wpick_view146*w8_picker_native146(void);
const v6_entry*w8_picker_existing146(uint64_t,const char*);
unsigned w8_picker_display146(uint64_t);
unsigned w8_picker_allowed146(uint64_t,const char*,unsigned);
unsigned w8_picker_matches146(uint64_t,const char*,unsigned);
unsigned w8_picker_complete146(uint64_t,const char*,unsigned,unsigned);
#endif
#endif
