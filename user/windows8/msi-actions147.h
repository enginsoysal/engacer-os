#ifndef ENGACER_MSI_ACTIONS147_H
#define ENGACER_MSI_ACTIONS147_H
#include "msi-journal147.h"
#include "msi-custom147.h"
typedef struct {unsigned index,operation,file;char data[4097];} msica_item147;
typedef struct {unsigned count;msica_item147*items[16];} msica147;
/* Inspect actual selected bodies and commands before any target mutation. */
unsigned msica_prepare147(msia_plan147*,msica147**);
void msica_close147(msica147*);
unsigned msica_records147(const msica147*,const msia_plan147*,msij147*);
unsigned msica_run147(const msica147*,msia_plan147*,unsigned,msia_custom_result147*);
/* Return 2 for unrecognized staging data, preserving it as user content. */
unsigned msica_clean147(const msia_plan147*,const char*);
#endif
