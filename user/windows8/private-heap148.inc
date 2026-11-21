/* Bounded independent growable heaps. Segment metadata shares committed pages;
 * destroying a heap really unmaps its pages, including outstanding blocks. */
typedef struct heap_block148 {size_t size,requested;struct heap_block148*next;unsigned free,reserved;} heap_block148;
typedef struct heap_segment148 {struct heap_segment148*next;size_t bytes;heap_block148*first;uint64_t reserved;} heap_segment148;
typedef struct {HANDLE handle;heap_segment148*segments;size_t committed;unsigned flags,reserved;} heap148;
_Static_assert(sizeof(heap_block148)==32&&sizeof(heap_segment148)==32,"Heap payloads remain 16-byte aligned");
static heap148 heaps148[8];static unsigned heap_generation148;static lock142 heap_api_lock148;
#define HEAP_LIMIT148 (24u*1024u*1024u)
static heap148*heap_find148(HANDLE handle){for(unsigned i=0;i<8;++i)if(heaps148[i].handle==handle&&handle)return heaps148+i;return 0;}
static heap_segment148*heap_segment_add148(heap148*h,size_t bytes){
 bytes=(bytes+4095)&~(size_t)4095;if(bytes>HEAP_LIMIT148-h->committed)return 0;
 heap_segment148*s=f_VirtualAlloc(0,bytes,0x3000,4);if(!s)return 0;
 s->next=h->segments;s->bytes=bytes;s->first=(void*)(s+1);s->reserved=0;
 *s->first=(heap_block148){bytes-sizeof(*s)-sizeof(heap_block148),0,0,1,0};h->segments=s;h->committed+=bytes;return s;
}
static heap_block148*heap_block_find148(heap148*h,const void*p){for(heap_segment148*s=h->segments;s;s=s->next)for(heap_block148*b=s->first;b;b=b->next)if(b+1==p&&!b->free)return b;return 0;}
static void heap_split148(heap_block148*b,size_t bytes){
 if(b->size>=bytes+sizeof(*b)+16){heap_block148*tail=(void*)((uint8_t*)(b+1)+bytes);*tail=(heap_block148){b->size-bytes-sizeof(*b),0,b->next,1,0};b->next=tail;b->size=bytes;}
}
static void heap_coalesce148(heap148*h){for(heap_segment148*s=h->segments;s;s=s->next)for(heap_block148*b=s->first;b&&b->next;){heap_block148*n=b->next;if(b->free&&n->free&&(uint8_t*)(b+1)+b->size==(uint8_t*)n){b->size+=sizeof(*n)+n->size;b->next=n->next;}else b=n;}}
static void*heap_allocate148(heap148*h,unsigned flags,size_t bytes){
 if(bytes>HEAP_LIMIT148-sizeof(heap_segment148)-sizeof(heap_block148))return 0;
 size_t aligned=((bytes?bytes:1)+15)&~(size_t)15;heap_block148*found=0;
 for(heap_segment148*s=h->segments;s&&!found;s=s->next)for(heap_block148*b=s->first;b;b=b->next)if(b->free&&b->size>=aligned){found=b;break;}
 if(!found){size_t extent=aligned+sizeof(heap_segment148)+sizeof(heap_block148);if(extent<65536)extent=65536;heap_segment148*s=heap_segment_add148(h,extent);if(!s)return 0;found=s->first;}
 heap_split148(found,aligned);found->free=0;found->requested=bytes;void*p=found+1;if(flags&8)memset(p,0,bytes);return p;
}
static HANDLE MS f_HeapCreate(unsigned flags,size_t initial,size_t maximum){
 if((flags&~1u)||maximum){last8(50);return 0;}if(initial>HEAP_LIMIT148){last8(8);return 0;}
 lock_enter142(&heap_api_lock148);unsigned slot=0;while(slot<8&&heaps148[slot].handle)++slot;
 if(slot==8||heap_generation148==0x1fffff){lock_leave142(&heap_api_lock148);last8(8);return 0;}
 heap148*h=heaps148+slot;memset(h,0,sizeof(*h));h->flags=flags;
 if(!heap_segment_add148(h,initial?initial:4096)){memset(h,0,sizeof(*h));lock_leave142(&heap_api_lock148);last8(8);return 0;}
 h->handle=UINT64_C(0x58000000)+(uint64_t)(++heap_generation148)*8+slot;HANDLE result=h->handle;lock_leave142(&heap_api_lock148);return result;
}
static int MS f_HeapDestroy(HANDLE handle){
 lock_enter142(&heap_api_lock148);heap148*h=heap_find148(handle);if(!h){lock_leave142(&heap_api_lock148);last8(6);return 0;}
 while(h->segments){heap_segment148*s=h->segments,*next=s->next;size_t bytes=s->bytes;if(!f_VirtualFree(s,0,0x8000)){lock_leave142(&heap_api_lock148);return 0;}h->segments=next;h->committed-=bytes;}
 memset(h,0,sizeof(*h));lock_leave142(&heap_api_lock148);return 1;
}
static void*MS f_HeapAlloc(HANDLE handle,unsigned flags,size_t bytes){
 if(handle==PROCESS_HEAP144)return process_heap_alloc144(handle,flags,bytes);
 if(flags&~9u){last8(50);return 0;}lock_enter142(&heap_api_lock148);heap148*h=heap_find148(handle);
 if(!h){lock_leave142(&heap_api_lock148);last8(6);return 0;}void*p=heap_allocate148(h,flags,bytes);lock_leave142(&heap_api_lock148);return p;
}
static int MS f_HeapFree(HANDLE handle,unsigned flags,void*p){
 if(handle==PROCESS_HEAP144)return process_heap_free144(handle,flags,p);
 if(flags&~1u){last8(87);return 0;}lock_enter142(&heap_api_lock148);heap148*h=heap_find148(handle);
 if(!h){lock_leave142(&heap_api_lock148);last8(6);return 0;}heap_block148*b=p?heap_block_find148(h,p):0;
 if(p&&!b){lock_leave142(&heap_api_lock148);last8(87);return 0;}if(b){b->free=1;b->requested=0;heap_coalesce148(h);}lock_leave142(&heap_api_lock148);return 1;
}
static size_t MS f_HeapSize(HANDLE handle,unsigned flags,const void*p){
 if(handle==PROCESS_HEAP144)return process_heap_size144(handle,flags,p);
 if(flags&~1u){last8(87);return SIZE_MAX;}lock_enter142(&heap_api_lock148);heap148*h=heap_find148(handle);heap_block148*b=h?heap_block_find148(h,p):0;
 size_t result=b?b->size:SIZE_MAX;lock_leave142(&heap_api_lock148);if(!b)last8(h?87:6);return result;
}
static void*MS f_HeapReAlloc(HANDLE handle,unsigned flags,void*p,size_t bytes){
 if((flags&~25u)||!p){last8(!p?87:50);return 0;}
 if(handle==PROCESS_HEAP144){size_t old=allocation_size8(p);if(old==SIZE_MAX){last8(87);return 0;}if(bytes>old&&(flags&16))return 0;void*result=realloc8(p,bytes?bytes:1);if(result&&(flags&8)&&bytes>old)memset((uint8_t*)result+old,0,bytes-old);return result;}
 lock_enter142(&heap_api_lock148);heap148*h=heap_find148(handle);heap_block148*b=h?heap_block_find148(h,p):0;
 if(!b){lock_leave142(&heap_api_lock148);last8(h?87:6);return 0;}
 if(bytes>HEAP_LIMIT148-64){lock_leave142(&heap_api_lock148);return 0;}
 size_t aligned=((bytes?bytes:1)+15)&~(size_t)15,old=b->requested;
 if(aligned>b->size&&b->next&&b->next->free&&b->size+sizeof(*b)+b->next->size>=aligned){heap_block148*n=b->next;b->size+=sizeof(*n)+n->size;b->next=n->next;}
 if(aligned<=b->size){heap_split148(b,aligned);b->requested=bytes;if((flags&8)&&bytes>old)memset((uint8_t*)p+old,0,bytes-old);heap_coalesce148(h);lock_leave142(&heap_api_lock148);return p;}
 if(flags&16){lock_leave142(&heap_api_lock148);return 0;}
 void*result=heap_allocate148(h,flags,bytes);if(result){memcpy(result,p,old<bytes?old:bytes);b->free=1;b->requested=0;heap_coalesce148(h);}lock_leave142(&heap_api_lock148);return result;
}
