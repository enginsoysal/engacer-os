/* Keep both Windows address windows disjoint from the kernel and each other. */
#include <assert.h>
#include <engine/windows8.h>

int main(void){
 assert(W8_X86_BASE>=UINT64_C(0x40000000));
 assert(W8_X86_LIMIT<UINT64_C(0x100000000));
 assert((W8_X86_BASE>>30)==((W8_X86_LIMIT-1)>>30));
 assert(w8_user_range1410(1,W8_X86_BASE,4096));
 assert(w8_user_range1410(1,W8_X86_LIMIT-4096,4096));
 assert(!w8_user_range1410(1,W8_X86_BASE-1,1));
 assert(!w8_user_range1410(1,W8_X86_LIMIT,0));
 assert(!w8_user_range1410(1,W8_X86_LIMIT-4096,4097));
 assert(!w8_user_range1410(1,W8_X86_BASE,UINT64_MAX));
 assert(!w8_user_range1410(1,W8_BASE,1));
 assert(w8_user_range1410(0,W8_BASE,W8_LIMIT-W8_BASE));
 assert(!w8_user_range1410(0,W8_X86_BASE,1));
 assert(!w8_user_range1410(0,W8_LIMIT-1,2));
 return 0;
}
