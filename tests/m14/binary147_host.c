/* Read original Binary streams as opaque data; never load vendor code on host. */
#include "plan147_host.c"
#include "../../user/windows8/msi_db.h"
__declspec(dllexport) unsigned binary_stream147(const char*name,void**out){msi8_blob stream=msi8_stream(name,0);*out=stream.data;return stream.size;}
__declspec(dllexport) void binary_free147(void*data){if(data)free8(data);}
