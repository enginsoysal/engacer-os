/* Test-only routing fixture: confirmed MSI jobs call the production lazy service. */
#include "../../user/windows8/runtime.h"
void msi8_execute(void){
 if(job8->command!=W8_INSTALL&&job8->command!=W8_REMOVE&&job8->command!=W8_PREVIEW)fail8("This routing fixture requires an MSI operation.");
 static const uint8_t original[32]={0x6d,0xc8,0x22,0x56,0x9e,0x77,0x7d,0x9a,0x3e,0xcd,0x5f,0xfc,0xbc,0x22,0xb5,0x56,0x00,0xaf,0x87,0xe6,0xc5,0xd9,0x81,0x0a,0x64,0xe8,0x56,0x6c,0xf5,0xa4,0xaf,0x9f};
 /* Test routing supplies the independent pinned digest of the original input.
  * The unchanged service compares actual source bytes before any write. */
 if(job8->command==W8_INSTALL)memcpy(job8->source_sha147,original,32);print8("M147_TEST_ROUTE_TO_PRODUCTION_MSI_REMOVE_SERVICE\n");init_win8();pe8_run("/System/Windows/Installer/msiexec.exe","");
}
