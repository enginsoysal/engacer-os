/* Test-only host adapter; original packages remain data, never execute. */
#include "plan147_host.c"
#include "../../user/windows8/msi_db.h"
unsigned msi_bind147(msia_plan147*);
void msi_unbind147(void);
void print8(const char*s){(void)s;}
__declspec(dllexport) unsigned bind147(void){return msi_bind147(plan147);}
__declspec(dllexport) void unbind147(void){msi_unbind147();}

unsigned msi_begin_deferred147(const char*);void msi_end_deferred147(void);
__declspec(dllexport) unsigned defer147(const char*data){return msi_begin_deferred147(data);}
__declspec(dllexport) void immediate147(void){msi_end_deferred147();}

unsigned msi_table147(unsigned,const char*,msi8_table*);
__declspec(dllexport) int database_count147(unsigned handle,const char*name){msi8_table table;unsigned code=msi_table147(handle,name,&table);if(code)return -(int)code;int count=(int)table.rows;if(table.data.data)free8(table.data.data);return count;}
