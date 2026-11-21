/* Pointer-sized process-local SRW locks. Uncontended calls allocate nothing;
 * contention parks on the existing value-checked kernel wait contract. */
static void srw_check148(uint64_t*lock){if(!lock||((uintptr_t)lock&7u))fail8("Invalid slim reader/writer lock address.");}
static void MS f_InitializeSRWLock(uint64_t*lock){srw_check148(lock);__atomic_store_n(lock,0,__ATOMIC_RELAXED);}
static uint8_t MS f_TryAcquireSRWLockExclusive(uint64_t*lock){srw_check148(lock);uint64_t expected=0;return __atomic_compare_exchange_n(lock,&expected,1,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED);}
static uint8_t MS f_TryAcquireSRWLockShared(uint64_t*lock){
 srw_check148(lock);uint64_t value=__atomic_load_n(lock,__ATOMIC_RELAXED);
 for(;;){if(value&1u)return 0;if(value>=UINT32_MAX-1u)fail8("Slim reader/writer reader count exceeded its limit.");if(__atomic_compare_exchange_n(lock,&value,value+2,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED))return 1;}
}
static void srw_park148(uint64_t*lock,uint64_t value){if((int64_t)sys8(W8_SYS_PARK,(uint64_t)(uintptr_t)lock,(uint32_t)value,UINT32_MAX,0,0)<0)fail8("Slim reader/writer wait failed.");}
static void MS f_AcquireSRWLockExclusive(uint64_t*lock){
 srw_check148(lock);for(;;){uint64_t expected=0;if(__atomic_compare_exchange_n(lock,&expected,1,0,__ATOMIC_ACQUIRE,__ATOMIC_RELAXED))return;srw_park148(lock,expected);}
}
static void MS f_AcquireSRWLockShared(uint64_t*lock){
 srw_check148(lock);for(;;){if(f_TryAcquireSRWLockShared(lock))return;uint64_t value=__atomic_load_n(lock,__ATOMIC_RELAXED);if(value&1u)srw_park148(lock,value);}
}
static void MS f_ReleaseSRWLockExclusive(uint64_t*lock){
 srw_check148(lock);uint64_t expected=1;if(!__atomic_compare_exchange_n(lock,&expected,0,0,__ATOMIC_RELEASE,__ATOMIC_RELAXED))fail8("Slim reader/writer exclusive release has no exclusive lock.");sys8(W8_SYS_WAKE,(uint64_t)(uintptr_t)lock,UINT32_MAX,0,0,0);
}
static void MS f_ReleaseSRWLockShared(uint64_t*lock){
 srw_check148(lock);uint64_t value=__atomic_load_n(lock,__ATOMIC_RELAXED);
 for(;;){if(!value||(value&1u))fail8("Slim reader/writer shared release has no shared lock.");if(__atomic_compare_exchange_n(lock,&value,value-2,0,__ATOMIC_RELEASE,__ATOMIC_RELAXED))break;}
 if(value==2)sys8(W8_SYS_WAKE,(uint64_t)(uintptr_t)lock,UINT32_MAX,0,0,0);
}
