/* Test-only host adapter; original packages remain data, never execute. */
#include "plan147_host.c"
unsigned msi_bind147(msia_plan147*);
void msi_unbind147(void);
void print8(const char*s){(void)s;}
__declspec(dllexport) unsigned bind147(void){return msi_bind147(plan147);}
__declspec(dllexport) void unbind147(void){msi_unbind147();}
