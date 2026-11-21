/* Private native routing diagnostic, never a shipped installation route. */
#include "../../user/windows8/runtime.h"

void msi8_execute(void) {
    /* This private replacement entered through the MSI frontend. Replace its
     * diagnostic command line before initialization; pe8_run does not parse its
     * legacy arguments parameter. Kernel installation authority is unchanged. */
    copy8(job8->startup_command,
            "\"C:\\Users\\Owner\\Downloads\\SumatraPDF-3.6.1-64-install.exe\" -install -d \"",
            sizeof(job8->startup_command));
    append8(job8->startup_command,job8->windows_root,sizeof(job8->startup_command));
    append8(job8->startup_command,"\"",sizeof(job8->startup_command));
    init_win8();
    pe8_run("/Users/Owner/Downloads/SumatraPDF-3.6.1-64-install.exe",0);
}
