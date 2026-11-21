/* Anonymous byte pipes: lazy pages, private grants and cross-process wakeups. */
#include <engine/winpipe147.h>
#define PIPE_OBJECTS147 32u
#define PIPE_CAPACITY147 3968u
typedef struct {unsigned readers,writers,head,count;uint8_t data[PIPE_CAPACITY147];} pipe_object147;
typedef struct {uint64_t handle;unsigned object,kind,access,inherit;} pipe_cap147;
typedef struct {pipe_cap147 caps[32];unsigned count;} pipe_process147;
_Static_assert(sizeof(pipe_object147)<=4096&&sizeof(pipe_process147)<=4096,"Pipe state exceeds one lazy page");
static pipe_object147*pipe_objects147[PIPE_OBJECTS147];static pipe_process147*pipe_processes147[SPACES142];static uint32_t pipe_generation147;
static uint64_t pipe_waits147,pipe_wakes147;
static void pipe_refresh147(void);
static uint64_t pipe_page147(void){uint64_t p=page_alloc();if(p){memset((void*)(uintptr_t)p,0,4096);++pipe_resident147;group_peak142();}return p;}
static void pipe_free147(void*p){page_free((uint64_t)(uintptr_t)p);--pipe_resident147;}
static pipe_cap147*pipe_find147(unsigned process,uint64_t handle){if(process>=SPACES142||!pipe_processes147[process]||(handle&WPIPE_TAG_MASK147)!=WPIPE_TAG147)return 0;unsigned slot=(unsigned)(handle&31);pipe_cap147*c=pipe_processes147[process]->caps+slot;return c->handle==handle&&c->object<PIPE_OBJECTS147&&pipe_objects147[c->object]?c:0;}
static void pipe_trim147(unsigned process){pipe_process147*p=pipe_processes147[process];if(p&&!p->count){pipe_processes147[process]=0;pipe_free147(p);}}
static uint64_t pipe_reference147(unsigned process,unsigned object,unsigned kind,unsigned access,unsigned inherit){
 if(process>=SPACES142||!spaces142[process]||pipe_generation147==UINT32_MAX)return 0;pipe_process147*p=pipe_processes147[process];if(!p){p=(void*)(uintptr_t)pipe_page147();if(!p)return 0;pipe_processes147[process]=p;}
 unsigned slot=0;while(slot<32&&p->caps[slot].handle)++slot;if(slot==32)return 0;uint64_t handle=WPIPE_TAG147|((uint64_t)++pipe_generation147<<8)|slot;p->caps[slot]=(pipe_cap147){handle,object,kind,access,inherit};++p->count;if(kind==1)++pipe_objects147[object]->readers;else ++pipe_objects147[object]->writers;return handle;
}
static unsigned pipe_close147(unsigned process,uint64_t handle){pipe_cap147*c=pipe_find147(process,handle);if(!c)return 6;unsigned object=c->object,kind=c->kind;c->handle=0;--pipe_processes147[process]->count;pipe_object147*o=pipe_objects147[object];if(kind==1)--o->readers;else --o->writers;if(!o->readers&&!o->writers){pipe_objects147[object]=0;pipe_free147(o);}pipe_trim147(process);pipe_refresh147();return 0;}
static void pipe_release147(void){unsigned process=active_space142;pipe_process147*p=pipe_processes147[process];if(!p)return;for(unsigned i=0;i<32;++i)if(p->caps[i].handle){uint64_t h=p->caps[i].handle;pipe_close147(process,h);p=pipe_processes147[process];if(!p)break;}}
static int pipe_ready147(unsigned process,thread142*t){pipe_cap147*c=pipe_find147(process,t->address);if(!c)return 1;pipe_object147*o=pipe_objects147[c->object];return t->wait_count==WPIPE_READ147?o->count||!o->writers:o->count<PIPE_CAPACITY147||!o->readers;}
static void pipe_refresh147(void){for(unsigned p=0;p<SPACES142;++p)if(spaces142[p])for(unsigned i=0;i<THREADS142;++i){thread142*t=spaces142[p]->threads+i;if(t->state==T147_PIPE&&pipe_ready147(p,t)){t->state=T142_READY;++pipe_wakes147;}}}
static NORETURN void pipe_park147(trap_frame*f,uint64_t handle,unsigned operation){++pipe_waits147;thread142*t=threads142+current142;t->address=handle;t->wait_count=operation;t->state=T147_PIPE;context8=*f;context8.rip-=2;w8_active=0;w8_escape();}
static unsigned pipe_inherit147(unsigned caller,unsigned target,const w8_process_request*request){
 if(request->inherit147>1||(request->startup_flags147&~0x100u))return 87;
 if(request->inherit147&&pipe_processes147[caller]){pipe_process147*parent=pipe_processes147[caller],*child=0;
  for(unsigned i=0;i<32;++i)if(parent->caps[i].handle&&parent->caps[i].inherit){if(!child){child=(void*)(uintptr_t)pipe_page147();if(!child)return 8;pipe_processes147[target]=child;}pipe_cap147*c=parent->caps+i;child->caps[i]=*c;++child->count;if(c->kind==1)++pipe_objects147[c->object]->readers;else ++pipe_objects147[c->object]->writers;}
 }
 if(request->startup_flags147&0x100u)for(unsigned i=0;i<3;++i){uint64_t h=request->std_handles147[i];if(!h||h==UINT64_MAX)continue;if(h>=1&&h<=3)continue;pipe_cap147*c=pipe_find147(target,h);if(!request->inherit147||!c||c->kind!=(i?2u:1u))return 6;}
 return 0;
}
static int64_t pipe_call147(uint64_t operation,uint64_t a,uint64_t b,uint64_t c,trap_frame*f){
 unsigned process=active_space142;
 if(operation==WPIPE_CREATE147){
  if(b||c)return -87;wpipe_pair147 request;if(user8(a,&request,sizeof(request),0)||request.hint>65536||request.inherit>1)return -87;unsigned object=0;while(object<PIPE_OBJECTS147&&pipe_objects147[object])++object;if(object==PIPE_OBJECTS147)return -8;
  pipe_object147*o=(void*)(uintptr_t)pipe_page147();if(!o)return -8;pipe_objects147[object]=o;request.read=pipe_reference147(process,object,1,1,request.inherit);
  if(!request.read){pipe_objects147[object]=0;pipe_free147(o);pipe_trim147(process);return -8;}
  request.write=pipe_reference147(process,object,2,2,request.inherit);if(!request.write){pipe_close147(process,request.read);return -8;}
  if(user8(a,&request,sizeof(request),1)){pipe_close147(process,request.read);pipe_close147(process,request.write);return -998;}return 0;
 }
 if(operation==WPIPE_DUPLICATE147){
  if(b||c)return -87;wpipe_duplicate147 request;if(user8(a,&request,sizeof(request),0)||request.reserved||request.inherit>1||(request.flags&~2u)||(request.access&~3u))return -87;pipe_cap147*source=pipe_find147(process,request.source);if(!source)return -6;
  unsigned access=request.flags&2?source->access:request.access;if(access&~source->access)return -5;request.result=pipe_reference147(process,source->object,source->kind,access,request.inherit);if(!request.result)return -8;if(user8(a,&request,sizeof(request),1)){pipe_close147(process,request.result);return -998;}return 0;
 }
 pipe_cap147*cap=pipe_find147(process,a);if(!cap)return -6;
 if(operation==WPIPE_CLOSE147)return b||c?-87:-(int64_t)pipe_close147(process,a);
 if(operation==WPIPE_QUERY147)return b||c?-87:(int64_t)cap->inherit;
 if(operation==WPIPE_FLAGS147){if(b&~1u||c&~1u)return -87;cap->inherit=(cap->inherit&~(unsigned)b)|((unsigned)c&(unsigned)b);return 0;}
 if(operation!=WPIPE_READ147&&operation!=WPIPE_WRITE147)return -87;
 if(c>4096)return -87;unsigned required=operation==WPIPE_READ147?1u:2u;if(cap->kind!=required||!(cap->access&required))return -5;if(!c)return 0;pipe_object147*o=pipe_objects147[cap->object];unsigned n=(unsigned)c;
 if(operation==WPIPE_READ147){
  if(!o->count){if(!o->writers)return -109;pipe_park147(f,a,(unsigned)operation);}if(n>o->count)n=o->count;unsigned first=PIPE_CAPACITY147-o->head;if(first>n)first=n;memcpy(io8,o->data+o->head,first);if(first<n)memcpy(io8+first,o->data,n-first);if(user8(b,io8,n,1))return -998;o->head=(o->head+n)%PIPE_CAPACITY147;o->count-=n;
 }else{
  if(!o->readers)return -109;if(o->count==PIPE_CAPACITY147)pipe_park147(f,a,(unsigned)operation);if(n>PIPE_CAPACITY147-o->count)n=PIPE_CAPACITY147-o->count;if(user8(b,io8,n,0))return -998;unsigned at=(o->head+o->count)%PIPE_CAPACITY147,first=PIPE_CAPACITY147-at;if(first>n)first=n;memcpy(o->data+at,io8,first);if(first<n)memcpy(o->data,io8+first,n-first);o->count+=n;
 }pipe_refresh147();return n;
}
