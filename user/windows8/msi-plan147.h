#ifndef ENGINE_MSI_PLAN147_H
#define ENGINE_MSI_PLAN147_H
#include "runtime.h"
#include "msi-properties147.h"
enum {MSIA_STANDARD147=0,MSIA_PROPERTY147=51,MSIA_DEFERRED_CHECKED147=3073,MSIA_DEFERRED_DLL147=3137};
static inline int msia_dll_type147(unsigned type){return type==MSIA_DEFERRED_CHECKED147||type==MSIA_DEFERRED_DLL147;}
typedef struct {const char *name,*condition,*source,*target;unsigned kind,sequence;} msia_action147;
typedef struct {const char *condition,*message;} msia_launch147;
typedef struct {const char *id,*parent,*target;char windows[256],relative[256];unsigned state,inside;} msia_directory147;
typedef struct {const char *id,*parent;int level;unsigned attributes,selected,condition_seen;} msia_feature147;
typedef struct {const char *id,*condition,*key;unsigned directory,attributes,selected;} msia_component147;
typedef struct {const char *id,*name;unsigned component,size,sequence,attributes,selected;uint8_t sha256[32];} msia_file147;
typedef struct {
 msip_session147 properties;
 msia_action147 *actions;msia_launch147 *launches;
 unsigned action_count,launch_count,custom_count,source_bytes,condition_unsupported;
 uint8_t source_sha256[32];char product_root[256],product[96],version[32],publisher[96],code[40];
 msia_directory147 *directories;msia_feature147 *features;msia_component147 *components;msia_file147 *files;
 unsigned directory_count,feature_count,component_count,file_count,selected_files,selected_bytes,costed,primary_directory;
 const char *cabinet;char program_alias[256],user_windows[256],format_scratch[256];unsigned format_error;
} msia_plan147;
/* Read-only preparation. No target file/registry mutation occurs here.
 * Database strings remain borrowed until close; close caller tables first. */
msia_plan147 *msia_prepare147(const void *,unsigned);
void msia_close147(msia_plan147 *);
int msia_condition147(msia_plan147 *,const char *);
unsigned msia_property_action147(msia_plan147 *,unsigned);
/* Selected clean-install feature/directory/component/file costing only.
 * It mutates session properties, never target files or registration. */
void msia_cost147(msia_plan147 *,const char *);
unsigned msia_file_path147(const msia_plan147 *,unsigned,char[256]);
unsigned msia_format147(msia_plan147 *,const char *,char *,unsigned);
#endif
