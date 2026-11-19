/* Process-owned synchronization objects; all state transitions share one lock. */
typedef struct {unsigned kind,refs,manual;int count,maximum;WCHAR name[96];uint64_t due;unsigned active,period;} object142;
typedef struct {unsigned live,generation,object;} object_handle142;
static object142 objects142[32];
static object_handle142 object_handles142[64];
static unsigned object_generation142;
static lock142 event_lock142;
static uint32_t event_sequence142;
static void signal142(void){__atomic_add_fetch(&event_sequence142,1,__ATOMIC_RELEASE);sys8(W8_SYS_WAKE,(uint64_t)(uintptr_t)&event_sequence142,UINT32_MAX,0,0,0);}
static int object_slot142(HANDLE h){unsigned slot=(unsigned)(h&63);return (h&UINT64_C(0xffffffffe0000000))==UINT64_C(0x20000000)&&object_handles142[slot].live&&object_handles142[slot].generation==((h&0x1fffffffu)>>6)?(int)slot:-1;}
static object142 *object_get142(HANDLE h){int slot=object_slot142(h);return slot<0?0:objects142+object_handles142[slot].object;}
static HANDLE object_reference142(unsigned object){
 unsigned slot=0;while(slot<64&&object_handles142[slot].live)++slot;
 if(slot==64||object_generation142>=0x7fffffu){last8(8);return 0;}
 object_handles142[slot]=(object_handle142){1,++object_generation142,object};++objects142[object].refs;
 return UINT64_C(0x20000000)|((uint64_t)object_handles142[slot].generation<<6)|slot;
}
static HANDLE object_create142(unsigned kind,int count,int maximum,unsigned manual,const WCHAR*name){
 if(name&&wlen8(name)>95){last8(206);return 0;}
 lock_enter142(&event_lock142);
 for(unsigned i=0;name&&*name&&i<32;++i)if(objects142[i].kind&&!f_wcscmp(objects142[i].name,name)){
  HANDLE h=objects142[i].kind==kind?object_reference142(i):0;lock_leave142(&event_lock142);last8(h?183:6);return h;
 }
 unsigned i=0;while(i<32&&objects142[i].kind)++i;if(i==32){lock_leave142(&event_lock142);last8(8);return 0;}
 object142*o=objects142+i;memset(o,0,sizeof(*o));o->kind=kind;o->count=count;o->maximum=maximum;o->manual=manual;widecopy8(o->name,name,96);
 HANDLE h=object_reference142(i);if(!h)memset(o,0,sizeof(*o));lock_leave142(&event_lock142);if(h)last8(0);return h;
}
static HANDLE MS f_CreateEventW(void*security,int manual,int initial,const WCHAR*name){if(security){last8(50);return 0;}return object_create142(1,initial!=0,1,manual!=0,name);}
static HANDLE MS f_CreateSemaphoreW(void*security,int initial,int maximum,const WCHAR*name){if(security||initial<0||maximum<=0||initial>maximum){last8(87);return 0;}return object_create142(2,initial,maximum,0,name);}
static int MS f_SetEvent(HANDLE h){lock_enter142(&event_lock142);object142*o=object_get142(h);int valid=o&&o->kind==1;if(valid){o->count=1;signal142();}lock_leave142(&event_lock142);if(!valid)last8(6);return valid;}
static int MS f_ResetEvent(HANDLE h){lock_enter142(&event_lock142);object142*o=object_get142(h);int valid=o&&o->kind==1;if(valid)o->count=0;lock_leave142(&event_lock142);if(!valid)last8(6);return valid;}
static int MS f_ReleaseSemaphore(HANDLE h,int count,int*previous){
 lock_enter142(&event_lock142);object142*o=object_get142(h);unsigned error=!o||o->kind!=2?6:count<=0?87:count>o->maximum-o->count?298:0;
 if(!error){if(previous)*previous=o->count;o->count+=count;signal142();}lock_leave142(&event_lock142);if(error)last8(error);return !error;
}
static HANDLE MS f_OpenEventW(unsigned access,int inherit,const WCHAR*name){
 if(!name||!name[0]||wlen8(name)>95||inherit||(access&~0x1f0003u)){last8(87);return 0;}
 lock_enter142(&event_lock142);HANDLE result=0;for(unsigned i=0;i<32;++i)if(objects142[i].kind==1&&!f_wcscmp(objects142[i].name,name)){result=object_reference142(i);break;}
 lock_leave142(&event_lock142);if(!result)last8(2);return result;
}
static HANDLE MS f_CreateWaitableTimerW(void*security,int manual,const WCHAR*name){if(security){last8(50);return 0;}return object_create142(3,0,1,manual!=0,name);}
static int MS f_SetWaitableTimer(HANDLE h,const int64_t*due,int period,void*callback,void*argument,int resume){
 (void)argument;if(!due||period<0){last8(87);return 0;}if(callback||resume){last8(50);return 0;}
 int64_t value=*due;uint64_t now=sys8(W8_SYS_TIME,0,0,0,0,0),delay;
 if(value<0){uint64_t units=(uint64_t)(-(value+1))+1;delay=units/10000+(units%10000!=0);}
 else{uint64_t clock=sys8(W8_SYS_TIME,1,0,0,0,0),units=(uint64_t)value>clock?(uint64_t)value-clock:0;delay=units/10000+(units%10000!=0);}
 if(delay>UINT64_MAX-now){last8(87);return 0;}
 lock_enter142(&event_lock142);object142*o=object_get142(h);int valid=o&&o->kind==3;
 if(valid){o->due=now+delay;o->period=(unsigned)period;o->count=0;o->active=1;signal142();}lock_leave142(&event_lock142);if(!valid)last8(6);return valid;
}
static int MS f_CancelWaitableTimer(HANDLE h){lock_enter142(&event_lock142);object142*o=object_get142(h);int valid=o&&o->kind==3;if(valid){o->active=0;signal142();}lock_leave142(&event_lock142);if(!valid)last8(6);return valid;}
static unsigned MS f_WaitForMultipleObjects(unsigned count,const HANDLE*handles,int all,unsigned timeout){
 if(!count||count>32||!handles){last8(87);return UINT32_MAX;}HANDLE list[32];memcpy(list,handles,count*sizeof(HANDLE));
 for(unsigned i=0;i<count;++i)for(unsigned j=0;j<i;++j)if(list[i]==list[j]){last8(87);return UINT32_MAX;}
 uint64_t start=sys8(W8_SYS_TIME,0,0,0,0,0);
 for(;;){lock_enter142(&event_lock142);unsigned ready=0,first=UINT32_MAX,error=0;uint64_t now=sys8(W8_SYS_TIME,0,0,0,0,0),next=UINT64_MAX;object142*seen[32]={0};
  for(unsigned i=0;i<count;++i){HANDLE h=list[i];int signaled=0;
   if((h&W8_HANDLE_TAG_MASK)==W8_PROCESS_TAG){int64_t state=(int64_t)sys8(W8_SYS_PROCESS_STATUS,h,0,0,0,0);if(state<0)error=6;else signaled=state==0;}
   else if(h==UINT64_MAX){signaled=0;}
   else if(h==UINT64_MAX-1||(h&UINT64_C(0xffffffffc0000000))==UINT64_C(0x40000000)){int64_t state=(int64_t)sys8(W8_SYS_THREAD_STATUS,h,0,0,0,0);if(state<0)error=6;else signaled=state==0;}
   else{object142*o=object_get142(h);seen[i]=o;if(!o){error=6;continue;}for(unsigned j=0;j<i;++j)if(seen[j]==o)error=87;
    if(o->kind==3&&o->active){if(now>=o->due){o->count=1;if(o->period){uint64_t steps=(now-o->due)/o->period+1;if(steps>(UINT64_MAX-o->due)/o->period)o->active=0;else o->due+=steps*o->period;}else o->active=0;}if(o->active&&o->due<next)next=o->due;}
    signaled=o->count>0;
   }if(signaled){++ready;if(first==UINT32_MAX)first=i;}
  }
  if(error){lock_leave142(&event_lock142);last8(error);return UINT32_MAX;}
  if((all&&ready==count)||(!all&&ready)){for(unsigned i=0;i<count;++i)if((all||i==first)&&seen[i]){object142*o=seen[i];if(o->kind==2||!o->manual)--o->count;}lock_leave142(&event_lock142);return all?0:first;}
  uint32_t sequence=__atomic_load_n(&event_sequence142,__ATOMIC_ACQUIRE);lock_leave142(&event_lock142);
  uint64_t elapsed=now-start;if(timeout!=UINT32_MAX&&elapsed>=timeout)return 258;
  uint64_t delay=timeout==UINT32_MAX?UINT32_MAX:timeout-elapsed;if(next!=UINT64_MAX&&next>now&&next-now<delay)delay=next-now;
  if((int64_t)sys8(W8_SYS_PARK,(uint64_t)(uintptr_t)&event_sequence142,sequence,delay,0,0)<0){last8(87);return UINT32_MAX;}
 }
}
static unsigned MS f_WaitForSingleObject(HANDLE h,unsigned timeout){return f_WaitForMultipleObjects(1,&h,0,timeout);}
static int MS f_CloseHandle(HANDLE h){
 if((h&W8_HANDLE_TAG_MASK)==W8_PROCESS_TAG){if((int64_t)sys8(W8_SYS_PROCESS_CLOSE,h,0,0,0,0)<0){last8(6);return 0;}return 1;}
 if((h&UINT64_C(0xffffffffc0000000))==UINT64_C(0x40000000)){if((int64_t)sys8(W8_SYS_THREAD_CLOSE,h,0,0,0,0)<0){last8(6);return 0;}return 1;}
 if(h>=256&&h<288){if(close8((int)(h-256))){last8(29);return 0;}return 1;}
 lock_enter142(&event_lock142);int slot=object_slot142(h);if(slot>=0){object142*o=objects142+object_handles142[slot].object;object_handles142[slot].live=0;if(!--o->refs)memset(o,0,sizeof(*o));signal142();}lock_leave142(&event_lock142);if(slot<0)last8(6);return slot>=0;
}
