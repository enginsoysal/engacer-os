#ifndef ENGINE_MSI_PLAN147_H
#define ENGINE_MSI_PLAN147_H
#include "runtime.h"
#include "msi-properties147.h"
enum {MSIA_STANDARD147=0,MSIA_PROPERTY147=51,MSIA_DEFERRED_DLL147=3137};
typedef struct {const char *name,*condition,*source,*target;unsigned kind,sequence;} msia_action147;
typedef struct {const char *condition,*message;} msia_launch147;
typedef struct {
 msip_session147 properties;
 msia_action147 *actions;msia_launch147 *launches;
 unsigned action_count,launch_count,custom_count,source_bytes,condition_unsupported;
 uint8_t source_sha256[32];char product_root[256],product[96],version[32],publisher[96],code[40];
} msia_plan147;
/* Read-only preparation. No target file/registry mutation occurs here.
 * Database strings remain borrowed until close; close caller tables first. */
msia_plan147 *msia_prepare147(const void *,unsigned);
void msia_close147(msia_plan147 *);
int msia_condition147(msia_plan147 *,const char *);
unsigned msia_property_action147(msia_plan147 *,unsigned);
#endif
