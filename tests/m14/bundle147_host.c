#include <engine/winbundle147.h>
int memcmp(const void*a,const void*b,size_t n){const uint8_t*x=a,*y=b;for(size_t i=0;i<n;++i)if(x[i]!=y[i])return x[i]<y[i]?-1:1;return 0;}
__declspec(dllexport) int parse147(const void*p,size_t n){winbundle147 v;return winbundle_parse147(p,n,&v)?(v.dll?2:1):0;}
