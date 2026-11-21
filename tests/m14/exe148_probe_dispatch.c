/* Private native routing diagnostic, never a shipped installation route. */
#include "../../user/windows8/runtime.h"

void msi8_execute(void) {
    init_win8();
    pe8_run("/Users/Owner/Downloads/SumatraPDF-3.6.1-64-install.exe",
            "-install -d C:\\Applications\\Windows\\{23170F69-40C1-2702-2606-000001000000}");
}
