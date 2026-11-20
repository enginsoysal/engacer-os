/* Test adapter for the production one-shot and incremental SHA-256 APIs. */
#include <engine/sha256.h>
void *memcpy(void *d,const void *s,size_t n){uint8_t *a=d;const uint8_t *b=s;for(size_t i=0;i<n;++i)a[i]=b[i];return d;}
void *memset(void *d,int value,size_t n){uint8_t *a=d;for(size_t i=0;i<n;++i)a[i]=(uint8_t)value;return d;}
__declspec(dllexport) void one147(const void *data,size_t length,uint8_t out[32]){engine_sha256(data,length,out);}
__declspec(dllexport) int stream147(const void *data,size_t length,const unsigned *chunks,unsigned count,uint8_t out[32]){
 engine_sha256_context context;engine_sha256_init(&context);size_t at=0;
 for(unsigned i=0;i<count;++i){if(chunks[i]>length-at)return 0;if(!engine_sha256_update(&context,(const uint8_t *)data+at,chunks[i]))return 0;at+=chunks[i];}
 if(at!=length||!engine_sha256_final(&context,out))return 0;return !engine_sha256_update(&context,0,0)&&!engine_sha256_final(&context,out);
}
__declspec(dllexport) int bounds147(void){engine_sha256_context context;uint8_t out[32];engine_sha256_init(&context);if(engine_sha256_update(&context,0,1))return 1;if(!engine_sha256_update(&context,0,0))return 2;context.bytes=UINT64_MAX/8;if(engine_sha256_update(&context,"x",1))return 3;context.used=64;if(engine_sha256_final(&context,out))return 4;return 0;}
