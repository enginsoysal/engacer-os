#include <stdint.h>

static unsigned identity = BUNDLE_IDENTITY;
/* Keep a relocation in each DLL to exercise normal rebasing in the loader. */
static unsigned *volatile marker = &identity;
__declspec(dllexport) unsigned BundleIdentity(void){return *marker;}
