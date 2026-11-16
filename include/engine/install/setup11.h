#ifndef ENGINE_SETUP11_H
#define ENGINE_SETUP11_H
#include <stdint.h>
/* Initial choices only; optional package management remains independent. */
typedef struct { uint32_t layout,dark,wallpaper,pattern,scale,apps; } setup_options11;
const setup_options11 *setup_choices11(void);
static inline unsigned setup_valid11(const setup_options11 *p,uint32_t admitted){
 return p&&p->layout<2&&p->dark<2&&p->wallpaper<=0xffffff&&p->pattern<3&&
        (!p->scale||(p->scale>=2&&p->scale<=4))&&!(p->apps&~admitted);
}
#endif
