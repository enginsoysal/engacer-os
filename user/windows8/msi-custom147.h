#ifndef ENGACER_MSI_CUSTOM147_H
#define ENGACER_MSI_CUSTOM147_H
#include "msi-plan147.h"
typedef struct {unsigned invoked,body_status,continued,engine_error;} msia_custom_result147;
/* Caller has preflighted the original binary and its expected external effects.
 * Actual body result is always retained, including authored Continue handling. */
unsigned msia_deferred147(unsigned,unsigned,const WCHAR*,const char*,const char*,msia_custom_result147*);
#endif
