#ifndef ENGACER_WINREVIEW147_H
#define ENGACER_WINREVIEW147_H
#include <stdint.h>
#include <engine/winproduct147.h>
/* Reuses the native app view's existing text storage; no idle allocation. */
typedef struct {
 uint32_t selected,ready,waiting,job,profile,files,registry,shortcuts,features;
 uint64_t source_size,source_first,total_bytes;
 uint32_t source_crc;
 uint8_t digest[32];
 char root[256],product[96],version[32],publisher[96],code[40];
} win_review147;
_Static_assert(sizeof(win_review147)<=1024,"One bounded installer review");
#endif
