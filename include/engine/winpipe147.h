#ifndef ENGINE_WINPIPE147_H
#define ENGINE_WINPIPE147_H
#include <stdint.h>
#define WPIPE_TAG147 UINT64_C(0x5049000000000000)
#define WPIPE_TAG_MASK147 UINT64_C(0xffff000000000000)
enum {WPIPE_CREATE147=1,WPIPE_READ147,WPIPE_WRITE147,WPIPE_CLOSE147,WPIPE_DUPLICATE147,WPIPE_QUERY147,WPIPE_FLAGS147};
typedef struct {uint32_t hint,inherit;uint64_t read,write;} wpipe_pair147;
typedef struct {uint64_t source,result;uint32_t inherit,flags,access,reserved;} wpipe_duplicate147;
#endif
