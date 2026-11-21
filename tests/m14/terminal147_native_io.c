/* Labelled native fault adapter. Every other MSI native operation is unchanged. */
#define remove8 remove_native147
#include "../../user/windows8/msi-native147.c"
#undef remove8
#include <engine/winproduct147.h>
int remove8(const char*path){
 static unsigned checked,fired;static char mode[32];
 if(!checked){checked=1;void*data=0;unsigned n=load8("/Users/Owner/Documents/cleanup-mode147.txt",&data,31);if(n){copy8(mode,data,sizeof(mode));free8(data);}}
 if(!fired&&job8->command==W8_REMOVE){char wanted[256];copy8(wanted,job8->product_root,sizeof(wanted));if(equal8(mode,"pending"))append8(wanted,"/.EngacerMSI/transaction.bin",sizeof(wanted));else if(equal8(mode,"done")){if(!win_product_completion147(wanted,sizeof(wanted),job8->product_root))return -1;}else wanted[0]=0;
  if(wanted[0]&&equal8(path,wanted)){fired=1;print8("M147_TEST_IO_DELETE_REFUSAL ");print8(mode);print8("\n");return -1;}}
 return remove_native147(path);
}
