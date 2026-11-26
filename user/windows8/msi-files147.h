#ifndef ENGINE_MSI_FILES147_H
#define ENGINE_MSI_FILES147_H
#include "msi-journal147.h"
unsigned msif_stage147(msia_plan147*,msij147*,const void*,unsigned);
unsigned msif_repair1410(msia_plan147 *,const msij147 *);
unsigned msif_promote147(const msia_plan147*);
unsigned msif_hash147(const char*,uint64_t,uint8_t[32]);
unsigned msif_verify147(const msij147*);
unsigned msif_directory147(const char*);
#endif
