#ifndef ENGACER_FONT_RASTER148_H
#define ENGACER_FONT_RASTER148_H
#include <stdint.h>
#define UI_RASTER_CAP148 (128u*1024u)
typedef struct {uint32_t offset,width,height;int32_t x,y;uint32_t advance;} ui_raster_glyph148;
typedef struct {uint32_t bytes,count,width,height,ascent,em,reserved[2];} ui_raster_info148;
typedef struct {uint32_t bytes,count,width,height,ascent,em,reserved[2];ui_raster_glyph148 glyphs[160];} ui_raster_line148;
typedef struct {uint64_t output;uint32_t capacity,render;char text[512];} ui_raster_request148;
_Static_assert(sizeof(ui_raster_line148)==3872,"One bounded glyph metadata page");
_Static_assert(sizeof(ui_raster_request148)==528,"Fixed raster request ABI");
typedef unsigned(*ui_raster_write148)(void*,unsigned,const uint8_t*,unsigned);
#endif
