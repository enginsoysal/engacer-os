#ifndef ENGINE_UI_GRAPHICS73_H
#define ENGINE_UI_GRAPHICS73_H
#include <engine/boot/boot_v0.h>
const os_boot_info_v0 *ui73_begin(const os_boot_info_v0 *);
#ifdef ENGINE_M13
void ui13_startup(unsigned phase,const char *message);
#endif
unsigned ui73_scale(void);
unsigned ui73_scale_choice(void);
const os_boot_info_v0 *ui73_set_scale(unsigned);
const char *ui73_font_license(void);
unsigned ui73_width(void);
unsigned ui73_height(void);
uint64_t ui73_framebuffer_bytes(void);
unsigned ui73_measure(const char *,unsigned);
#ifdef ENGINE_M14
#include <engine/ui/font-metrics148.h>
#include <engine/ui/image148.h>
void ui148_image(int,int,const wui_image_view148*);
unsigned ui148_font_role(unsigned);
unsigned ui148_font_height(unsigned);
unsigned ui148_font_info(unsigned,ui_font_metrics148*);
unsigned ui148_font_canonical(unsigned,ui_font_metrics148*);
#include <engine/ui/font-raster148.h>
unsigned ui148_raster_plan(unsigned,const char*,ui_raster_line148*);
unsigned ui148_raster_emit(unsigned,const char*,const ui_raster_line148*,ui_raster_write148,void*);
#endif
void ui145_argb_tile(int,int,unsigned,unsigned,const uint32_t *);
void ui73_round(unsigned,unsigned,unsigned,unsigned,unsigned,uint32_t);
void ui73_shadow(unsigned,unsigned,unsigned,unsigned);
void ui73_fit(unsigned,unsigned,unsigned,const char *,unsigned,uint32_t);
unsigned ui73_paragraph(unsigned,unsigned,unsigned,unsigned,const char *,uint32_t);
void ui73_folder(unsigned,unsigned,unsigned,uint32_t);
#ifdef ENGINE_M74
uint32_t ui74_rgb(unsigned,unsigned);
unsigned ui74_intersects(unsigned,unsigned,unsigned,unsigned);
#endif
#endif
