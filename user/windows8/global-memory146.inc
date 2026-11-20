/* Process-private global memory, distinct from LocalAlloc and raw heap objects. */
#define GLOBAL_SLOTS146 128u
#define GLOBAL_TAG146 UINT64_C(0x474d000000000000)
#define GLOBAL_SYSTEM146 0x80000000u
typedef struct {void*pointer;size_t bytes;uint64_t handle;unsigned locks,flags;} global_object146;
_Static_assert(sizeof(global_object146)==32,"Bounded global-memory metadata");
static global_object146 *global_objects146;
static unsigned global_count146,global_generation146;
static lock142 global_lock146;
static global_object146 *global_find146(uint64_t handle){
 if(!handle||!global_objects146)return 0;
 for(unsigned i=0;i<GLOBAL_SLOTS146;++i)if(global_objects146[i].handle==handle)return global_objects146+i;
 return 0;
}
static uint64_t MS f_GlobalAlloc(unsigned flags,size_t bytes){
 /* DISCARDABLE and DDESHARE are obsolete allocation hints, not sharing grants. */
 if(flags&~0x2142u){last8(50);return 0;}if(bytes>24*1024*1024){last8(8);return 0;}
 lock_enter142(&global_lock146);
 if(global_count146==GLOBAL_SLOTS146||global_generation146==UINT32_MAX){lock_leave142(&global_lock146);last8(1816);return 0;}
 if(!global_objects146){global_objects146=calloc8(GLOBAL_SLOTS146,sizeof(*global_objects146));if(!global_objects146){lock_leave142(&global_lock146);last8(8);return 0;}}
 unsigned slot=0;while(global_objects146[slot].handle)++slot;
 void*pointer=0;size_t actual=0;if(bytes||!(flags&2)){pointer=alloc8(bytes?bytes:1);if(!pointer){if(!global_count146){free8(global_objects146);global_objects146=0;}lock_leave142(&global_lock146);last8(8);return 0;}actual=allocation_size8(pointer);if(flags&0x40)memset(pointer,0,actual);}
 uint64_t generation=++global_generation146;
 uint64_t handle=flags&2?GLOBAL_TAG146|(generation<<8)|slot:(uint64_t)(uintptr_t)pointer;
 global_objects146[slot]=(global_object146){pointer,actual,handle,0,flags&2};++global_count146;
 lock_leave142(&global_lock146);return handle;
}
static uint64_t MS f_GlobalFree(uint64_t handle){
 if(!handle)return 0;lock_enter142(&global_lock146);global_object146*object=global_find146(handle);
 if(!object||(object->flags&GLOBAL_SYSTEM146)){lock_leave142(&global_lock146);last8(object?5:6);return handle;}
 /* Windows permits freeing a locked object; callers must not retain its pointer. */
 free8(object->pointer);memset(object,0,sizeof(*object));if(!--global_count146){free8(global_objects146);global_objects146=0;}
 lock_leave142(&global_lock146);return 0;
}
static void *MS f_GlobalLock(uint64_t handle){
 lock_enter142(&global_lock146);global_object146*object=global_find146(handle);
 if(!object||!object->pointer){unsigned error=object?157:6;lock_leave142(&global_lock146);last8(error);return 0;}
 if((object->flags&2)&&object->locks==255){lock_leave142(&global_lock146);last8(1816);return 0;}
 if(object->flags&2)++object->locks;void*pointer=object->pointer;lock_leave142(&global_lock146);return pointer;
}
static int MS f_GlobalUnlock(uint64_t handle){
 lock_enter142(&global_lock146);global_object146*object=global_find146(handle);
 if(!object){lock_leave142(&global_lock146);last8(6);return 0;}
 if(!(object->flags&2)){lock_leave142(&global_lock146);return 1;}
 if(!object->locks){lock_leave142(&global_lock146);last8(158);return 0;}
 unsigned remaining=--object->locks;lock_leave142(&global_lock146);if(!remaining)last8(0);return remaining!=0;
}
static size_t MS f_GlobalSize(uint64_t handle){
 lock_enter142(&global_lock146);global_object146*object=global_find146(handle);size_t bytes=object?object->bytes:0;
 lock_leave142(&global_lock146);if(!object)last8(6);return bytes;
}
static unsigned MS f_GlobalFlags(uint64_t handle){
 lock_enter142(&global_lock146);global_object146*object=global_find146(handle);
 unsigned flags=object?(object->pointer?object->locks:0x4000):0x8000;lock_leave142(&global_lock146);if(!object)last8(6);return flags;
}
static uint64_t MS f_GlobalHandle(const void*pointer){
 uint64_t handle=0;lock_enter142(&global_lock146);
 if(pointer&&global_objects146)for(unsigned i=0;i<GLOBAL_SLOTS146;++i)if(global_objects146[i].handle&&global_objects146[i].pointer==pointer){handle=global_objects146[i].handle;break;}
 lock_leave142(&global_lock146);if(!handle)last8(6);return handle;
}
static unsigned global_contains146(const void*pointer){
 unsigned found=0;lock_enter142(&global_lock146);
 if(pointer&&global_objects146)for(unsigned i=0;i<GLOBAL_SLOTS146;++i){global_object146*object=global_objects146+i;if(object->handle&&(object->pointer==pointer||object->handle==(uint64_t)(uintptr_t)pointer)){found=1;break;}}
 lock_leave142(&global_lock146);return found;
}
