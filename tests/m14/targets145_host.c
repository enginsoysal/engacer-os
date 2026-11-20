#include <stdint.h>
#define MS __attribute__((ms_abi))
#define NORETURN __attribute__((noreturn))
static void last8(unsigned value){(void)value;}
static void print8(const char*text){(void)text;}
static uint64_t pe8_main(void){return 0;}
static NORETURN void fail8(const char*text){(void)text;__builtin_trap();}
#include "../../user/windows8/target-guards145.inc"
__declspec(dllexport) uint64_t refusal_key145(unsigned provider,const char*name,unsigned ordinal){return target_key145(provider,name,ordinal);}
__declspec(dllexport) unsigned refusal_lookup145(unsigned provider,const char*name,unsigned ordinal){return guard_address145(guard_lookup145(provider,name,ordinal));}
__declspec(dllexport) unsigned refusal_bytes145(void){return sizeof(target_refusals145);}
