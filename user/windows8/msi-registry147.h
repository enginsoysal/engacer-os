#ifndef ENGINE_MSI_REGISTRY147_H
#define ENGINE_MSI_REGISTRY147_H
#include "msi-journal147.h"
unsigned msireg_appsearch147(msia_plan147*);
unsigned msireg_snapshot147(msia_plan147*,msij147*);
unsigned msireg_apply147(const msij147*);
unsigned msireg_undo147(const msij147*);
#endif
