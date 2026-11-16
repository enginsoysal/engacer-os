/* Versioned per-user appearance and normal app geometry; 352 bytes. */
#include <engine/desktop/appearance11.h>
static appearance_record11 appearance11;
static void appearance_load11(void);
static unsigned appearance_save11(void);
static void appearance_settings11(desktop_window*,application*,uint64_t);
static uint32_t desktop_ink11(void);

static uint32_t desktop_label_ink11(unsigned);
