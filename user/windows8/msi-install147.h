#ifndef ENGACER_MSI_INSTALL147_H
#define ENGACER_MSI_INSTALL147_H
#include "msi-plan147.h"
/* Fresh-install controller. Unsupported effects refuse before target creation.
 * A failure after journal publication deliberately leaves recovery ownership. */
unsigned msia_install147(msia_plan147*,const void*,unsigned);
unsigned msia_admit147(msia_plan147*);
#endif
