/* AMD64 public 16-byte SLIST ABI, implemented with real atomic exchange.
 * No hidden allocation or per-list lock. Push/pop APIs remain separate work. */
typedef struct {uint64_t low,high;} slist_header147;
static slist_header147 *slist_head147(void*head){
 if(!head||((uintptr_t)head&15))fail8("A Windows SLIST header is not 16-byte aligned.");
 return head;
}
static void MS f_InitializeSListHead(void*head){slist_header147*h=slist_head147(head);h->low=h->high=0;}
static int slist_exchange147(slist_header147*h,uint64_t*low,uint64_t*high,uint64_t next_low,uint64_t next_high){
 unsigned char success;uint64_t a=*low,d=*high;
 __asm__ volatile("lock cmpxchg16b %1; sete %0":"=qm"(success),"+m"(*h),"+a"(a),"+d"(d):"b"(next_low),"c"(next_high):"cc","memory");
 *low=a;*high=d;return success;
}
static void *MS f_InterlockedFlushSList(void*head){
 slist_header147*h=slist_head147(head);
 if(!f_IsProcessorFeaturePresent(14))fail8("The AMD64 SLIST profile requires CMPXCHG16B.");
 uint64_t low=__atomic_load_n(&h->low,__ATOMIC_ACQUIRE),high=__atomic_load_n(&h->high,__ATOMIC_ACQUIRE);
 for(;;){
  uint64_t first=high&~UINT64_C(15);if(!first)return 0;
  uint64_t sequence=(low+UINT64_C(65536))&~UINT64_C(65535);
  if(slist_exchange147(h,&low,&high,sequence,high&15))return(void*)(uintptr_t)first;
 }
}
