#ifndef ENGINE_WINMAP146_H
#define ENGINE_WINMAP146_H
#include <stdint.h>
#define WMAP_TAG146 UINT64_C(0xe0000000)
enum {WMAP_CREATE146=1,WMAP_OPEN146,WMAP_VIEW146,WMAP_UNMAP146,WMAP_CLOSE146,WMAP_SKIP146,WMAP_QUERY146};
typedef struct {uint64_t file,bytes;uint32_t protection,access,reserved[2];uint16_t name[96];} wmap_create146;
typedef struct {uint64_t handle,bytes;uint32_t existed,reserved;} wmap_result146;
typedef struct {uint64_t handle,base,offset,bytes;uint32_t access,reserved;} wmap_view146;
#endif
