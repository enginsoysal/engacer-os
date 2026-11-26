/* Production path grant regression for two products under one user. */
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <engine/winproduct147.h>

#define ENGINE_M14
#define APP_A WIN_PRODUCT_BASE147 "{23170F69-40C1-2702-2606-000001000000}"
#define APP_B WIN_PRODUCT_BASE147 "{83170F69-40C1-2702-2606-000001000001}"
enum { W8_INSTALL=1,W8_REMOVE,W8_RUN };
static struct { const char *user_root,*product_root,*source; unsigned command; } input8={
 "/Users/Owner",APP_A,"/Users/Owner/Downloads/app.msi",W8_INSTALL
};
static unsigned length8(const char *p){return (unsigned)strlen(p);}
static unsigned equal8(const char *a,const char *b){return strcmp(a,b)==0;}
static unsigned prefix8(const char *p,const char *root){
 size_t n=strlen(root);
 return !strncmp(p,root,n)&&(!p[n]||p[n]=='/');
}
static unsigned installer_authority147(void){return input8.command!=W8_RUN;}
static unsigned installer_user_grant147(const char *path,unsigned ancestor){
 (void)path;(void)ancestor;return 0;
}
static void copy8(char *out,const char *in,unsigned cap){
 size_t n=strlen(in);if(n>=cap)n=cap-1;memcpy(out,in,n);out[n]=0;
}
static void protected_hash143(const char *text,char *out){
 (void)text;memset(out,'0',32);out[32]=0;
}
#include "../../kernel/windows8/path-access147.inc"

int main(void){
 if(!path8("/Applications/Windows",0)||!path8(APP_B "/product.bin",0)||
    !path8(APP_B "/.EngacerMSI/transaction.bin",0))return 1;
 if(path8(APP_B "/other.dll",0)||path8(APP_B "/.EngacerMSI/source.msi",0)||
    path8(APP_B "/product.bin",1)||path8(APP_B "/../product.bin",0)||
    path8(APP_B "/product.bin/child",0))return 2;
 if(path_content1410(APP_B "/.EngacerMSI/transaction.bin")||
    !path_content1410(APP_B "/product.bin")||
    !path_content1410(APP_A "/.EngacerMSI/transaction.bin"))return 5;
 if(!path8(APP_A "/other.dll",0)||!path8(APP_A "/other.dll",1))return 3;
 if(path8(APP_A "/.Engacer",0)||path8(APP_A "/.Engacer/Registry/key",1)||
    path_content1410(APP_A "/.Engacer/Registry/key")||
    !path8(APP_A "/.EngacerMSI/transaction.bin",1))return 6;
 input8.command=W8_RUN;
 if(path8(APP_B "/product.bin",0)||path8("/Applications/Windows",0)||
    !path8(APP_A "/other.dll",0))return 4;
 const char own[]=APP_A "/.Engacer/Temp/00000000000000000000000000000000/cache.bin";
 const char foreign[]=APP_B "/.Engacer/Temp/00000000000000000000000000000000/cache.bin";
 if(!path8(own,1)||!path_content1410(own)||path8(foreign,0)||
    path8("/Users/Owner/AppData/Temp/cache.bin",1)||
    path8(APP_A "/.Engacer/Temp/11111111111111111111111111111111/cache.bin",0))return 7;
 return 0;
}
