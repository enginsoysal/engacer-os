/* Production SRW algorithm with real host address waits, not guest evidence. */
#include <stdint.h>
#include <stdlib.h>
#define MS
#define W8_SYS_PARK 1
#define W8_SYS_WAKE 2
static int(*host_wait)(volatile void*,void*,size_t,unsigned);
static void(*host_wake)(void*);
static void fail8(const char*message){(void)message;abort();}
static uint64_t sys8(uint64_t n,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t e){
 (void)c;(void)d;(void)e;
 if(n==W8_SYS_PARK){uint32_t expected=(uint32_t)b;return host_wait((void*)(uintptr_t)a,&expected,4,UINT32_MAX)?0:UINT64_MAX;}
 host_wake((void*)(uintptr_t)a);return 0;
}
#include "../../user/windows8/srw148.inc"
static uint64_t lock,left,right;
__declspec(dllexport) void bind148(void*wait,void*wake){host_wait=wait;host_wake=wake;f_InitializeSRWLock(&lock);left=right=0;}
__declspec(dllexport) int basic148(void){
 if(!f_TryAcquireSRWLockExclusive(&lock)||f_TryAcquireSRWLockExclusive(&lock)||f_TryAcquireSRWLockShared(&lock))return 0;
 f_ReleaseSRWLockExclusive(&lock);
 if(!f_TryAcquireSRWLockShared(&lock)||!f_TryAcquireSRWLockShared(&lock)||f_TryAcquireSRWLockExclusive(&lock))return 0;
 f_ReleaseSRWLockShared(&lock);f_ReleaseSRWLockShared(&lock);return lock==0;
}
__declspec(dllexport) int writer148(unsigned rounds){for(unsigned i=0;i<rounds;++i){f_AcquireSRWLockExclusive(&lock);++left;right=left*3;f_ReleaseSRWLockExclusive(&lock);}return 1;}
__declspec(dllexport) int reader148(unsigned rounds){for(unsigned i=0;i<rounds;++i){f_AcquireSRWLockShared(&lock);int valid=right==left*3;f_ReleaseSRWLockShared(&lock);if(!valid)return 0;}return 1;}
__declspec(dllexport) uint64_t count148(void){return left;}
