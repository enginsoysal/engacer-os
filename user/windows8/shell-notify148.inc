#include <engine/winui144.h>
/* Current measured shell event: global association-cache refresh, no item IDLs. */
static void MS f_SHChangeNotify(int32_t events,unsigned flags,const void*first,const void*second){
 if((uint32_t)events!=0x08000000u||flags||first||second)fail8("This shell change-notification event/format is unsupported.");
 if((int64_t)sys8(W8_SYS_UI144,WUI_SHELL148,0,0,0,0)<=0)fail8("The native shell association refresh could not be delivered.");
}
