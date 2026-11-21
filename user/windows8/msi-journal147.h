#ifndef ENGINE_MSI_JOURNAL147_H
#define ENGINE_MSI_JOURNAL147_H
#include "msi-plan147.h"
#include <engine/wintxn147.h>
typedef struct {uint8_t*data;unsigned bytes,capacity;} msij147;
msij147 *msij_create147(const msia_plan147*);
void msij_close147(msij147*);
unsigned msij_append147(msij147*,unsigned,const void*,unsigned);
unsigned msij_file147(msij147*,unsigned,const char*,uint64_t,const uint8_t[32],unsigned);
unsigned msij_properties147(msij147*,const msip_session147*);
unsigned msij_seal147(msij147*);
unsigned msij_write147(msij147*,const char*);
msij147 *msij_read147(const char*,const char*,const char*);
#endif
