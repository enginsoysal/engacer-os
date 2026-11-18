/* Fixed-size setup model; no per-page allocation or network dependency. */
static setup_options11 setup11={0,DISTRO_DESKTOP_DARK,DISTRO_DESKTOP_WALLPAPER,0,0,DISTRO_APPS74_MASK};
static unsigned keyboard_page11,apps_page11,name_cursor11=5,name_anchor11;
static char keyboard_test11[32];
static unsigned keyboard_test_length11;
#ifdef ENGINE_M13
static unsigned startup_options13;
#endif
const setup_options11 *setup_choices11(void){return &setup11;}
static unsigned setup_action11(unsigned);
static unsigned setup_key11(int);
