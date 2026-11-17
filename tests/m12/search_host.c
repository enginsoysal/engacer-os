#include <engine/ui/search12.h>
#include <engine/desktop/start11.h>
unsigned search12_checks(void){
 unsigned n=0;
#define CHECK(x) do{++n;if(!(x))return n;}while(0)
 CHECK(search12_rank("Calculator","Calculator")==0);
 CHECK(search12_rank("Calculator","cAlCuLaToR")==0);
 CHECK(search12_rank("Calculator","calc")==1);
 CHECK(search12_rank("Text Editor","editor")==2);
 CHECK(search12_rank("Text Editor","text")==1);
 CHECK(search12_rank("Text Editor","terminal")==3);
 CHECK(search12_rank("","terminal")==3);
 CHECK(search12_rank("Terminal","")==1);
 CHECK(search12_rank("Calculator","Calculator plus")==3);
 CHECK(search12_rank("Folder Calculator","Calculator")==2);
 CHECK(search12_rank("Aaaab","aaab")==2);
 CHECK(search12_rank(0,"calc")==3);
 CHECK(search12_rank("calc",0)==3);
 char label[256],query[256];
 for(unsigned i=0;i<255;++i)label[i]=query[i]='x';
 label[255]=query[255]=0;
 CHECK(search12_rank(label,query)==0);
 query[254]='y';CHECK(search12_rank(label,query)==3);
 /* Ranking must not need to change the persisted catalogue/preferences ABI. */
 CHECK(S11_APPS+S11_PINS==52);
 return 0;
}
