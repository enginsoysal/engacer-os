/* Production bounded atom core; own host state only. */
#include <engine/winatom147.h>
static watom_table147 table147;
__declspec(dllexport) void reset147(void){uint8_t*p=(uint8_t*)&table147;for(unsigned i=0;i<sizeof(table147);++i)p[i]=0;}
__declspec(dllexport) int add147(const uint16_t*s,unsigned n){return watom_add147(&table147,s,n,watom_case147);}
__declspec(dllexport) int find147(const uint16_t*s,unsigned n){return watom_find147(&table147,s,n,watom_case147);}
__declspec(dllexport) int delete147(unsigned atom){return watom_delete147(&table147,atom);}
__declspec(dllexport) int name147(unsigned atom,uint16_t*out,unsigned n){return watom_name_copy147(&table147,atom,out,n);}
__declspec(dllexport) unsigned used147(void){return table147.used;}
__declspec(dllexport) unsigned references147(unsigned atom){return atom>=0xc000&&atom<0xc040?table147.references[atom-0xc000]:0;}
__declspec(dllexport) unsigned valid147(void){unsigned end=0,seen=0;for(unsigned step=0;step<WATOM_SLOTS147;++step){unsigned at=WATOM_SLOTS147;for(unsigned i=0;i<WATOM_SLOTS147;++i)if(table147.references[i]&&table147.offsets[i]==end){if(at!=WATOM_SLOTS147)return 0;at=i;}if(at==WATOM_SLOTS147)break;if(!table147.lengths[at]||table147.lengths[at]>255||end+table147.lengths[at]>=WATOM_UNITS147||table147.text[end+table147.lengths[at]])return 0;end+=table147.lengths[at]+1;++seen;}unsigned live=0;for(unsigned i=0;i<WATOM_SLOTS147;++i)live+=table147.references[i]!=0;return live==seen&&end==table147.used;}
