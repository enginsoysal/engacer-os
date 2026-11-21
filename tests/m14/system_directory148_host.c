#include <stdint.h>
#include <string.h>
#include <assert.h>
#define MS
typedef uint16_t WCHAR;
static unsigned error;
static void last8(unsigned value){error=value;}
#include "../../user/windows8/system-directory148.inc"
int main(void){
 const WCHAR expected[]=u"C:\\Windows\\System32";
 for(unsigned cap=0;cap<=40;++cap){
  WCHAR output[42];for(unsigned i=0;i<42;++i)output[i]=0x9b9b;
  error=123;unsigned n=f_GetSystemDirectoryW(output,cap);
  assert(n==(cap<=19?20u:19u)&&error==123);
  if(cap<=19){for(unsigned i=0;i<42;++i)assert(output[i]==0x9b9b);}
  else{assert(!memcmp(output,expected,sizeof(expected)));for(unsigned i=20;i<42;++i)assert(output[i]==0x9b9b);}
 }
 assert(f_GetSystemDirectoryW(0,0)==20);error=0;
 assert(!f_GetSystemDirectoryW(0,20)&&error==87);
 return 0;
}
