#ifndef ENGINE_WINMIGRATION1410_H
#define ENGINE_WINMIGRATION1410_H

#include <engine/wintxn147.h>

/* The current legacy value must still match the committed postimage. A
 * pre-existing identical value gives no evidence of a write by this app.
 * The caller separately excludes competing claims from other products.
 */
static inline unsigned win_migration_postimage1410(
 uint32_t type,const uint8_t *value,unsigned bytes,
 uint32_t after_type,const uint8_t *after,unsigned after_bytes,
 unsigned before_exists,uint32_t before_type,const uint8_t *before,unsigned before_bytes){
 if(type!=after_type||bytes!=after_bytes||memcmp(value,after,bytes))return 0;
 return !before_exists||before_type!=after_type||before_bytes!=after_bytes||
        memcmp(before,after,after_bytes);
}

static inline unsigned win_migration_same_value1410(
 unsigned root,unsigned view,const char *key,const char *name,
 const win_tx_reg147 *other,const char *other_key,const char *other_name){
 if(root!=other->root||(root==2&&view!=other->view))return 0;
 return win_tx_equal147(key,other_key)&&win_tx_equal147(name,other_name);
}

#endif
