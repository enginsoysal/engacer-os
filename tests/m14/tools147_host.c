/* Production argument/pattern core only; reference interpretation is external. */
#include "../../user/windows8/tools147.h"
__declspec(dllexport) int parse147(const uint16_t*input,unsigned shell,uint16_t*out,unsigned cap,unsigned*offsets){uint16_t*argv[16];int count=tool_parse147(input,out,cap,argv,16,shell);if(count>=0)for(unsigned i=0;i<(unsigned)count;++i)offsets[i]=(unsigned)(argv[i]-out);return count;}
__declspec(dllexport) int destination147(const uint16_t*source,const uint16_t*target,uint16_t*out,unsigned cap){return tool_destination147(source,target,out,cap);}
