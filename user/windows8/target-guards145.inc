/* One refusal body, not hundreds of pretend API implementations. */
#include "target-refusals145.inc"
static void target_hex145(uint64_t value){char text[17];static const char digits[]="0123456789abcdef";for(unsigned n=0;n<16;++n)text[n]=digits[(value>>(60-n*4))&15];text[16]=0;print8(text);}
static NORETURN void MS target_guard145(uint64_t arg1,uint64_t arg2,uint64_t arg3,uint64_t arg4){
 uint64_t caller=(uint64_t)(uintptr_t)__builtin_return_address(0);last8(50);
 print8("Unavailable Win32 API caller=0x");target_hex145(caller);print8(" main=0x");target_hex145(pe8_main());print8("\n");
 print8("ABI GPR arguments: 0x");target_hex145(arg1);print8(" 0x");target_hex145(arg2);print8(" 0x");target_hex145(arg3);print8(" 0x");target_hex145(arg4);print8("\n");
 fail8("Required Windows API is unavailable; see the call-site diagnostic.");
}
static unsigned guard_address145(void*address){return address==(void*)(uintptr_t)target_guard145;}
static uint64_t target_key145(unsigned provider,const char*name,unsigned ordinal){
 uint64_t key=UINT64_C(14695981039346656037);unsigned seed[3]={provider&255,(provider>>8)&255,name?0u:1u};
 for(unsigned n=0;n<3;++n)key=(key^seed[n])*UINT64_C(1099511628211);
 if(name){unsigned n=0;for(;n<256&&name[n];++n)key=(key^(uint8_t)name[n])*UINT64_C(1099511628211);if(n==256)return 0;}
 else{key=(key^(ordinal&255))*UINT64_C(1099511628211);key=(key^((ordinal>>8)&255))*UINT64_C(1099511628211);}
 return key;
}
static void*guard_lookup145(unsigned provider,const char*name,unsigned ordinal){
 uint64_t key=target_key145(provider,name,ordinal);unsigned low=0,high=sizeof(target_refusals145)/sizeof(target_refusals145[0]);
 while(low<high){unsigned mid=low+(high-low)/2;if(target_refusals145[mid]<key)low=mid+1;else high=mid;}
 return low<sizeof(target_refusals145)/sizeof(target_refusals145[0])&&target_refusals145[low]==key?(void*)(uintptr_t)target_guard145:0;
}
