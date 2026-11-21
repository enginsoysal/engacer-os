/* Session-global atoms survive creator exit; only matching Delete releases them.
 * Broker traps are serialized on the assigned Windows execution processor. */
#include <engine/winatom147.h>
static watom_table147*atoms147;
static int64_t atom_call147(uint64_t operation,uint64_t pointer,uint64_t argument){
 if(argument)return -87;
 if(operation==WATOM_DELETE147){if(pointer>65535)return -87;int result=watom_delete147(atoms147,(unsigned)pointer);if(atoms147&&!atoms147->used){ui_free144(atoms147);atoms147=0;}return result;}
 if(operation==WATOM_NAME147){watom_name147 request;if(user8(pointer,&request,sizeof(request),0))return -998;if(!request.capacity)return -234;if(request.atom>65535||request.capacity>INT32_MAX)return -87;uint16_t output[256];unsigned capacity=request.capacity<256?request.capacity:256;int result=watom_name_copy147(atoms147,request.atom,output,capacity);if(result<0)return result;unsigned copied=(unsigned)result+(capacity>(unsigned)result);return user8(request.buffer,output,copied*2u,1)?-998:result;}
 if(operation!=WATOM_FIND147&&operation!=WATOM_ADD147)return -87;
 if(pointer<=65535)return pointer&&pointer<0xc000?(int64_t)pointer:-87;
 uint16_t name[256];unsigned n=0;for(;n<256;++n){if(pointer>UINT64_MAX-n*2u||user8(pointer+n*2u,name+n,2,0))return -998;if(!name[n])break;}if(!n||n==256)return -87;
 int found=watom_find147(atoms147,name,n,watom_case147);if(operation==WATOM_FIND147)return found;if(found<0&&found!=-2)return found;
 if(found>0&&found<0xc000)return found;if(!atoms147){atoms147=ui_page144();if(!atoms147)return -8;}
 int result=watom_add147(atoms147,name,n,watom_case147);if(result<0&&!atoms147->used){ui_free144(atoms147);atoms147=0;}return result;
}
