#ifndef ENGACER_MSI_REMOVE147_H
#define ENGACER_MSI_REMOVE147_H
#include "msi-files147.h"
/* Caller validates the cached source and restores/costs its original selection. */
/* 2 means no completion record. Other errors retain it for retry/inspection. */
unsigned msir_finish147(unsigned*);
unsigned msir_remove147(msia_plan147*,msij147*,unsigned*);
#endif
