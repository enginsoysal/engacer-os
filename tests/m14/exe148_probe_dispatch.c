/* Private native routing diagnostic, never a shipped installation route. */
#include "../../user/windows8/runtime.h"

void msi8_execute(void) {
    /* This private replacement entered through the MSI frontend. Replace its
     * diagnostic command line before initialization; pe8_run does not parse its
     * legacy arguments parameter. Kernel installation authority is unchanged. */
    copy8(job8->startup_command,
            "\"C:\\Users\\Owner\\Downloads\\SumatraPDF-3.6.1-64-install.exe\" -install -d \"C:\\Applications\\Windows\\{23170F69-40C1-2702-2606-000001000000}\"",
            sizeof(job8->startup_command));
    init_win8();
    pe8_run("/Users/Owner/Downloads/SumatraPDF-3.6.1-64-install.exe",
            "-install -d C:\\Applications\\Windows\\{23170F69-40C1-2702-2606-000001000000}");
}
