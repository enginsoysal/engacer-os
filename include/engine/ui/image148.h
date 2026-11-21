#ifndef ENGACER_UI_IMAGE148_H
#define ENGACER_UI_IMAGE148_H
#include <stdint.h>
/* Source bytes are copied into broker-owned pages before publication. */
typedef struct {uint64_t pixels;uint32_t width,height;int32_t stride;uint32_t format;int32_t x,y,clip_x,clip_y,clip_width,clip_height;uint32_t reserved[2];} wui_image_request148;
_Static_assert(sizeof(wui_image_request148)==56,"Fixed copied image request ABI");
/* Kernel-only page views: never exported through a user query. */
typedef struct {uint64_t tables[2];uint32_t width,height,format,reserved;} wui_image_view148;
#endif
