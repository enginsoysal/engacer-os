/* Shared named objects with process-owned grants; one protected worker CPU. */
#ifndef W8_NAMED_OWNER
#define W8_NAMED_OWNER (input8.user_root)
#endif
#define SYNC_BASE142 META_BASE142(SPACES142)
#define SYNC_OBJECTS142 128u
#define SYNC_SEPARATOR142 0x5cu
#define SYNC_TAG142 UINT64_C(0x20000000)
typedef struct {uint32_t kind,manual;int32_t count,maximum;uint32_t refs,active,period,creator;uint64_t due;char owner[256];uint16_t name[96];uint8_t padding[24];} sync_object142;
_Static_assert(sizeof(sync_object142)==512,"Eight lazy synchronization records per page");
static uint8_t sync_used142[SYNC_OBJECTS142];static uint64_t sync_pages142[16];static unsigned sync_generation142;
static sync_object142*sync_object_at142(unsigned i){return (void*)(uintptr_t)(SYNC_BASE142+(uint64_t)i*512);}
static unsigned ensure_sync_page142(unsigned i){unsigned page=i/8;if(sync_pages142[page])return 0;uint64_t va=SYNC_BASE142+(uint64_t)page*4096,*pt=(void*)(uintptr_t)kernel_entry_pt();if(pt[(va>>12)&511])return 1;uint64_t physical=page_alloc();if(!physical)return 1;sync_pages142[page]=physical;pt[(va>>12)&511]=physical|3|NX;__asm__ volatile("invlpg (%0)"::"r"(va):"memory");++sync_resident142;group_peak142();return 0;}
static void free_sync_page142(unsigned i){unsigned page=i/8;for(unsigned n=page*8;n<page*8+8;++n)if(sync_used142[n])return;uint64_t physical=sync_pages142[page];if(!physical)return;uint64_t va=SYNC_BASE142+(uint64_t)page*4096,*pt=(void*)(uintptr_t)kernel_entry_pt();pt[(va>>12)&511]=0;__asm__ volatile("invlpg (%0)"::"r"(va):"memory");sync_pages142[page]=0;--sync_resident142;page_free(physical);}
static int sync_slot142(uint64_t h){unsigned slot=h&63;if((h&W8_HANDLE_TAG_MASK)!=SYNC_TAG142)return -1;sync_cap142*c=spaces142[active_space142]->sync_handles+slot;return c->live&&c->generation==((h&UINT64_C(0x1fffffff))>>6)&&c->object<SYNC_OBJECTS142&&sync_used142[c->object]?(int)slot:-1;}
static uint64_t sync_reference142(unsigned object,unsigned access){if(sync_generation142>=0x7fffff)return 0;unsigned slot=0;while(slot<64&&spaces142[active_space142]->sync_handles[slot].live)++slot;if(slot==64)return 0;sync_cap142*c=spaces142[active_space142]->sync_handles+slot;*c=(sync_cap142){1,++sync_generation142,object,access};++sync_object_at142(object)->refs;return SYNC_TAG142|((uint64_t)c->generation<<6)|slot;}
static void drop_sync_reference142(sync_cap142*c){unsigned object=c->object;c->live=0;if(!sync_used142[object])return;sync_object142*o=sync_object_at142(object);if(!--o->refs){memset(o,0,sizeof(*o));sync_used142[object]=0;free_sync_page142(object);}}
static void release_sync_grants142(void){for(unsigned i=0;i<64;++i)if(spaces142[active_space142]->sync_handles[i].live)drop_sync_reference142(spaces142[active_space142]->sync_handles+i);}
static unsigned sync_name142(uint16_t*name){unsigned count=0;while(count<96&&name[count])++count;if(count==96)return 206;unsigned local=0,global=0;static const uint16_t local_name[]={'L','o','c','a','l',SYNC_SEPARATOR142,0},global_name[]={'G','l','o','b','a','l',SYNC_SEPARATOR142,0};if(count>=6&&!memcmp(name,local_name,12))local=6;if(count>=7&&!memcmp(name,global_name,14))global=7;if((local||global)&&count==(local?local:global))return 87;for(unsigned i=local?local:global;i<count;++i)if(name[i]==SYNC_SEPARATOR142)return 87;if(local){memmove(name,name+local,(count-local+1)*2);count-=local;}memset(name+count,0,(96-count)*2);return 0;}
static int64_t create_sync142(uint64_t request,uint64_t output,uint64_t open_only){
 w8_sync_request142 r;w8_sync_result142 result={0};if(user8(request,&r,sizeof(r),0)||user8(output,&result,sizeof(result),1)||open_only>1)return -87;unsigned error=sync_name142(r.name);if(error)return -(int64_t)error;if(r.kind<1||r.kind>3||r.manual>1||(r.access&~0x1f0003u))return -87;
 if(open_only&&!r.name[0])return -87;if(!open_only&&((r.kind==2&&(r.manual||r.count<0||r.maximum<=0||r.count>r.maximum))||(r.kind!=2&&(r.count<0||r.count>1||r.maximum!=1))))return -87;

#ifdef ENGINE_M14
 if(mapping_name_taken146(r.name))return -6;
#endif
 unsigned object=SYNC_OBJECTS142,created=0,own=0;for(unsigned i=0;i<SYNC_OBJECTS142;++i)if(sync_used142[i]){sync_object142*o=sync_object_at142(i);if(o->creator==input8.process_id)++own;if(r.name[0]&&equal8(o->owner,W8_NAMED_OWNER)&&!memcmp(o->name,r.name,192)){if(o->kind!=r.kind)return -6;object=i;result.existed=1;break;}}
 if(object==SYNC_OBJECTS142){if(open_only)return -2;if(own>=32)return -8;for(unsigned i=0;i<SYNC_OBJECTS142;++i)if(!sync_used142[i]){object=i;break;}if(object==SYNC_OBJECTS142||ensure_sync_page142(object))return -8;sync_object142*o=sync_object_at142(object);memset(o,0,sizeof(*o));o->kind=r.kind;o->manual=r.manual;o->count=r.count;o->maximum=r.maximum;o->creator=input8.process_id;copy8(o->owner,W8_NAMED_OWNER,256);memcpy(o->name,r.name,192);sync_used142[object]=1;created=1;}
 result.handle=sync_reference142(object,open_only?r.access:0x1f0003);if(!result.handle){if(created){memset(sync_object_at142(object),0,sizeof(sync_object142));sync_used142[object]=0;free_sync_page142(object);}return -8;}return user8(output,&result,sizeof(result),1)?-87:0;
}
static void update_sync_timer142(sync_object142*o,uint64_t now){if(o->kind!=3||!o->active||now<o->due)return;o->count=1;if(o->period){uint64_t steps=(now-o->due)/o->period+1;if(steps>(UINT64_MAX-o->due)/o->period)o->active=0;else o->due+=steps*o->period;}else o->active=0;}
/* Returns -1 while unsatisfied, other negative values encode API errors. */
static int64_t evaluate_wait142(thread142*t,unsigned consume){
#ifdef ENGINE_M14
 if(t->wait_all==2)return ui_message_ready148((unsigned)(t-threads142),t->wait_handles[0])?0:-1;
#endif
 unsigned ready=0,first=UINT32_MAX;sync_object142*objects[32]={0};uint64_t now=m3_clock_ticks()*10;
 for(unsigned i=0;i<t->wait_count;++i){uint64_t h=t->wait_handles[i];int signaled=0;
  if((h&W8_HANDLE_TAG_MASK)==SYNC_TAG142){int slot=sync_slot142(h);if(slot<0)return -6;sync_cap142*cap=spaces142[active_space142]->sync_handles+slot;if(!(cap->access&0x100000))return -5;sync_object142*o=sync_object_at142(cap->object);objects[i]=o;for(unsigned j=0;j<i;++j)if(objects[j]==o)return -87;update_sync_timer142(o,now);signaled=o->count>0;}
  else if((h&W8_HANDLE_TAG_MASK)==W8_PROCESS_TAG){int64_t status=process_status142(h,0,0);if(status<0)return status==-5?-5:-6;signaled=status==0;}
  else if(h==UINT64_MAX)signaled=0;
  else if(h==UINT64_MAX-1||(h&UINT64_C(0xffffffffc0000000))==UINT64_C(0x40000000)){int slot=h==UINT64_MAX-1?(int)(t-threads142):thread_slot142(h);if(slot<0)return -6;signaled=threads142[slot].state==T142_EXITED;}
  else return -6;
  if(signaled){++ready;if(first==UINT32_MAX)first=i;}
 }
 if((t->wait_all&&ready==t->wait_count)||(!t->wait_all&&ready)){if(consume)for(unsigned i=0;i<t->wait_count;++i)if((t->wait_all||i==first)&&objects[i]&&(objects[i]->kind==2||!objects[i]->manual))--objects[i]->count;return t->wait_all?0:first;}
 return -1;
}
static void refresh_sync_waits142(void){unsigned saved=active_space142;uint64_t now=m3_clock_ticks()*10;for(unsigned p=0;p<SPACES142;++p)if(spaces142[p]){active_space142=p;for(unsigned i=0;i<THREADS142;++i){thread142*t=threads142+i;if(t->state!=T142_OBJECT)continue;int64_t result=evaluate_wait142(t,1);if(result==-1&&t->deadline!=UINT64_MAX&&now>=t->deadline)result=258;if(result!=-1){t->state=T142_READY;t->frame.rax=(uint64_t)result;}}}active_space142=saved;}
static unsigned sync_deadline_needed142(void){unsigned saved=active_space142,needed=0;for(unsigned p=0;p<SPACES142&&!needed;++p)if(spaces142[p]){active_space142=p;for(unsigned i=0;i<THREADS142&&!needed;++i){thread142*t=threads142+i;if(t->state!=T142_OBJECT)continue;if(t->deadline!=UINT64_MAX){needed=1;break;}
#ifdef ENGINE_M14
 if(t->wait_all==2&&ui_message_timer_deadline148(i,(unsigned)t->wait_handles[0])!=UINT64_MAX){needed=1;break;}
#endif
 for(unsigned n=0;n<t->wait_count;++n){int slot=sync_slot142(t->wait_handles[n]);if(slot>=0){sync_object142*o=sync_object_at142(spaces142[p]->sync_handles[slot].object);if(o->kind==3&&o->active){needed=1;break;}}}}}active_space142=saved;return needed;}
static int64_t wait_objects142(trap_frame*f,uint64_t address){
 w8_wait_request142 r;if(user8(address,&r,sizeof(r),0))return -87;
#ifdef ENGINE_M14
 if(r.all==2){if(r.count||(r.pad&~0x1dffu))return -87;wui_queue144*q=ui_queue144(active_space142,current142,1);if(!q)return -8;thread142*t=threads142+current142;t->wait_count=0;t->wait_all=2;t->wait_handles[0]=r.pad;if(ui_message_ready148(current142,r.pad))return 0;if(!r.timeout)return 258;t->state=T142_OBJECT;t->deadline=r.timeout==UINT32_MAX?UINT64_MAX:m3_clock_ticks()*10+r.timeout;context8=*f;context8.rax=0;w8_active=0;w8_escape();}
#endif
 if(!r.count||r.count>32||r.all>1||r.pad)return -87;for(unsigned i=0;i<r.count;++i)for(unsigned j=0;j<i;++j)if(r.handles[i]==r.handles[j])return -87;
 thread142*t=threads142+current142;t->wait_count=r.count;t->wait_all=r.all;memcpy(t->wait_handles,r.handles,r.count*8);int64_t result=evaluate_wait142(t,1);if(result!=-1)return result;if(!r.timeout)return 258;t->state=T142_OBJECT;t->deadline=r.timeout==UINT32_MAX?UINT64_MAX:m3_clock_ticks()*10+r.timeout;context8=*f;context8.rax=0;w8_active=0;w8_escape();
}
static int64_t operate_sync142(uint64_t h,uint64_t operation,uint64_t value,uint64_t argument){
 int slot=sync_slot142(h);if(slot<0)return -6;sync_cap142*cap=spaces142[active_space142]->sync_handles+slot;if(!(cap->access&2))return -5;sync_object142*o=sync_object_at142(cap->object);
 if(operation==1||operation==2){if(o->kind!=1)return -6;o->count=operation==1;}
 else if(operation==3){if(o->kind!=2)return -6;if(!value||value>INT32_MAX)return -87;if(value>(uint64_t)(o->maximum-o->count))return -298;int previous=o->count;if(argument&&user8(argument,&previous,4,1))return -87;o->count+=(int)value;}
 else if(operation==4){if(o->kind!=3)return -6;if(argument>INT32_MAX)return -87;o->due=value;o->period=(unsigned)argument;o->count=0;o->active=1;}
 else if(operation==5){if(o->kind!=3)return -6;o->active=0;}
 else return -87;refresh_sync_waits142();return 0;
}
static int64_t close_sync142(uint64_t h){int slot=sync_slot142(h);if(slot<0)return -6;drop_sync_reference142(spaces142[active_space142]->sync_handles+slot);refresh_sync_waits142();return 0;}
