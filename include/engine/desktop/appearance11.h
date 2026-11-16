#ifndef ENGINE_APPEARANCE11_H
#define ENGINE_APPEARANCE11_H
#include <engine/desktop/window.h>
/* Shared stable on-disk version 1, including twenty optional normal rectangles. */
typedef struct {unsigned magic,version,accent,dark,scale,wallpaper,pattern,reserved;desktop_rect normal[20];} appearance_record11;
#endif
