#ifndef ENGINE_SHA256_H
#define ENGINE_SHA256_H
#include <engine/base.h>
void engine_sha256(const void*,size_t,uint8_t[32]);
typedef struct {uint32_t state[8];uint64_t bytes;unsigned used;uint8_t block[64];} engine_sha256_context;
void engine_sha256_init(engine_sha256_context*);
/* Update/final return zero for invalid state, pointers or an excessive length.
 * Final consumes the context; initialize it again before another digest. */
int engine_sha256_update(engine_sha256_context*,const void*,size_t);
int engine_sha256_final(engine_sha256_context*,uint8_t[32]);
#endif
