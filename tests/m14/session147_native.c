/* Owned MSI-core qualification inside a native protected Windows process. */
#include <stddef.h>
#include <stdint.h>
__declspec(dllimport) uint64_t GlobalAlloc(unsigned,uint64_t);
__declspec(dllimport) uint64_t GlobalFree(uint64_t);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void *,unsigned,unsigned *,void *);
__declspec(dllimport) void ExitProcess(unsigned);
void *memset(void *out,int value,size_t n){unsigned char *p=out;for(size_t i=0;i<n;++i)p[i]=(unsigned char)value;return out;}
void *memcpy(void *out,const void *in,size_t n){unsigned char *p=out;const unsigned char *s=in;for(size_t i=0;i<n;++i)p[i]=s[i];return out;}
#include "../../user/windows8/msi-condition147.h"
#include "../../user/windows8/msi-properties147.h"
static void check147(int yes,unsigned code){if(!yes)ExitProcess(code);}
static void *allocate147(void *context,size_t bytes){(void)context;return (void *)(uintptr_t)GlobalAlloc(0,bytes);}
static void release147(void *context,void *p){(void)context;check147(!GlobalFree((uint64_t)(uintptr_t)p),70);}
static const char *lookup147(void *context,unsigned prefix,const char *name){if(prefix)return "";return msip_get147(context,name);}
void entry(void);void *volatile anchor147=&entry;
void entry(void){
 msip_session147 session={.alloc=allocate147,.release=release147};
 check147(!msip_set147(&session,"NPP_LANG","english"),10);
 check147(!msip_set147(&session,"INSTALLFOLDER","C:\\Program Files\\Notepad++\\"),11);
 check147(!msip_set147(&session,"LocalizationFolder","C:\\Program Files\\Notepad++\\localization\\"),12);
 check147(!msip_set147(&session,"SystemFolder","C:\\Windows\\System32\\"),13);
 check147(msic_evaluate147("NPP_LANG AND NOT Installed",lookup147,&session)==1,14);
 check147(msic_evaluate147("NPP_LANG AND Installed AND REMOVE=\"ALL\"",lookup147,&session)==0,15);
 check147(msic_evaluate147("NOT WIX_DOWNGRADE_DETECTED",lookup147,&session)==1,16);
 char formatted[512];check147(!msip_format147(&session,"\"[SystemFolder]xcopy.exe\" \"[LocalizationFolder][NPP_LANG].xml\" \"[INSTALLFOLDER]nativeLang.xml*\" /Y /Q",formatted,sizeof(formatted),0,0),17);
 check147(msip_same147(formatted,"\"C:\\Windows\\System32\\xcopy.exe\" \"C:\\Program Files\\Notepad++\\localization\\english.xml\" \"C:\\Program Files\\Notepad++\\nativeLang.xml*\" /Y /Q"),18);
 check147(!msip_set147(&session,"Installed","1")&&!msip_set147(&session,"REMOVE","ALL"),19);
 check147(msic_evaluate147("NPP_LANG AND Installed AND REMOVE=\"ALL\"",lookup147,&session)==1,20);
 check147(msic_evaluate147("NPP_LANG AND NOT Installed",lookup147,&session)==0,21);
 check147(msic_evaluate147("1 OR (Invalid AND)",lookup147,&session)==3,22);
 check147(msic_evaluate147("A == 1",lookup147,&session)==3,23);
 check147(msic_evaluate147("65537<<1 AND 65537>>1",lookup147,&session)==1,24);
 check147(msic_evaluate147("\"AbC\"~=\"abc\"",lookup147,&session)==1,25);
 check147(!msip_set147(&session,"Unicode","caf\xc3\xa9"),26);
 check147(!msip_format147(&session,"[Unicode]",formatted,sizeof(formatted),0,0)&&msip_same147(formatted,"caf\xc3\xa9"),27);
 formatted[0]='x';check147(msip_format147(&session,"[SystemFolder]",formatted,1,0,0)==1816&&!formatted[0],28);
 check147(!msip_set147(&session,"NPP_LANG",0)&&!msip_get147(&session,"NPP_LANG")[0],29);
 msip_destroy147(&session);check147(!session.count&&!session.bytes&&!session.capacity&&!session.items,30);
 static const char message[]="M147_MSI_SESSION_CONDITIONS_PROPERTIES_FORMATTING_PASS\r\n";unsigned wrote=0;check147(WriteFile(GetStdHandle((unsigned)-11),message,sizeof(message)-1,&wrote,0)&&wrote==sizeof(message)-1,31);ExitProcess(0);
}
