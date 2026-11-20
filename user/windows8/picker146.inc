/* Checked native common dialogs; modal callbacks remain in this private process. */
#include <engine/winpicker146.h>
static unsigned common_errors146[16];
static int common_dialog146(void*ofn,unsigned save){
 unsigned thread=tid142()&255;if(thread>=16)return 0;common_errors146[thread]=0;
 WCHAR directory[512];lock_enter142(&cwd_lock143);widecopy8(directory,cwd8,512);lock_leave142(&cwd_lock143);
 int64_t generation=ui_call144(WUI_PICKER146,save?WPICK_SAVE146:WPICK_OPEN146,ofn,(uint64_t)(uintptr_t)directory);
 if(generation<0){common_errors146[thread]=(unsigned)-generation;return 0;}
 for(;;){
  int64_t status=ui_call144(WUI_PICKER146,WPICK_RESULT146,0,(uint64_t)generation);
  if(status!=2){if(status<0)common_errors146[thread]=(unsigned)-status;return status==1;}
  ui_msg144 message;int received=ui_peek144(&message,0,0,0,1);
  if(received<0){ui_call144(WUI_PICKER146,WPICK_CANCEL146,0,(uint64_t)generation);common_errors146[thread]=0xffff;return 0;}
  if(received){if(message.message==0x12){f_PostQuitMessage((int)message.wp);ui_call144(WUI_PICKER146,WPICK_CANCEL146,0,(uint64_t)generation);return 0;}f_TranslateMessage(&message);f_DispatchMessageW(&message);}
  else{status=ui_call144(WUI_PICKER146,WPICK_WAIT146,0,(uint64_t)generation);if(status<0){ui_call144(WUI_PICKER146,WPICK_CANCEL146,0,(uint64_t)generation);common_errors146[thread]=(unsigned)-status;return 0;}}
 }
}
static int MS f_GetOpenFileNameW(void*ofn){return common_dialog146(ofn,0);}
static int MS f_GetSaveFileNameW(void*ofn){return common_dialog146(ofn,1);}
static unsigned MS f_CommDlgExtendedError(void){unsigned thread=tid142()&255;return thread<16?common_errors146[thread]:0xffff;}
