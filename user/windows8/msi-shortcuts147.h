#ifndef ENGINE_MSI_SHORTCUTS147_H
#define ENGINE_MSI_SHORTCUTS147_H
#include "msi-files147.h"
typedef struct {unsigned flags,bytes;char relative[256];uint8_t data[];} msil_entry147;
typedef struct {unsigned count;msil_entry147*entries[32];} msil_plan147;
unsigned msil_prepare147(msia_plan147*,msij147*,msil_plan147**);
unsigned msil_stage147(const msia_plan147*,const msil_plan147*);
unsigned msil_apply147(const msia_plan147*,const msil_plan147*);
void msil_close147(msil_plan147*);
#endif
