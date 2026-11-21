/* Immutable snapshots of actual live Windows execution-domain processes.
 * Native desktop components are outside this compatibility PID namespace. */
#define SNAPSHOT_TAG148 UINT64_C(0xe0000000)
typedef struct {uint32_t size,usage,pid,pad;uint64_t heap;uint32_t module,threads,parent;int32_t priority;uint32_t flags;WCHAR name[260];uint32_t tail;} process_entry148;
_Static_assert(sizeof(process_entry148)==568&&offsetof(process_entry148,name)==44,"AMD64 PROCESSENTRY32W layout");
typedef struct {HANDLE handle;unsigned next,reserved;w8_process_snapshot148 view;} snapshot148;
static snapshot148*snapshots148[8];static unsigned snapshot_generation148;static lock142 snapshot_lock148;
static snapshot148*snapshot_find148(HANDLE handle){unsigned slot=(unsigned)(handle&7u);snapshot148*s=snapshots148[slot];return s&&s->handle==handle?s:0;}
static int snapshot_close148(HANDLE handle){lock_enter142(&snapshot_lock148);snapshot148*s=snapshot_find148(handle);if(!s){lock_leave142(&snapshot_lock148);last8(6);return 0;}snapshots148[handle&7u]=0;free8(s);lock_leave142(&snapshot_lock148);return 1;}
static HANDLE MS f_CreateToolhelp32Snapshot(unsigned flags,unsigned pid){
 (void)pid;if(flags!=2){last8(50);return UINT64_MAX;}
 lock_enter142(&snapshot_lock148);unsigned slot=0;while(slot<8&&snapshots148[slot])++slot;
 if(slot==8||snapshot_generation148==0xffffff){lock_leave142(&snapshot_lock148);last8(8);return UINT64_MAX;}
 snapshot148*s=calloc8(1,sizeof(*s));if(!s){lock_leave142(&snapshot_lock148);last8(8);return UINT64_MAX;}
 int64_t status=(int64_t)sys8(W8_SYS_PROCESSES148,(uint64_t)(uintptr_t)&s->view,0,0,0,0);
 if(status<0||s->view.count>W8_PROCESS_SNAPSHOT_MAX148){free8(s);lock_leave142(&snapshot_lock148);last8(status<0?(unsigned)-status:13);return UINT64_MAX;}
 s->handle=SNAPSHOT_TAG148|((uint64_t)(++snapshot_generation148)<<3)|slot;snapshots148[slot]=s;HANDLE result=s->handle;lock_leave142(&snapshot_lock148);return result;
}
static int process_next148(HANDLE handle,process_entry148*out,unsigned first){
 if(!out){last8(87);return 0;}if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,sizeof(*out),3,0,0)){last8(998);return 0;}if(out->size!=sizeof(*out)){last8(24);return 0;}
 lock_enter142(&snapshot_lock148);snapshot148*s=snapshot_find148(handle);if(!s){lock_leave142(&snapshot_lock148);last8(6);return 0;}if(first)s->next=0;
 if(s->next>=s->view.count){lock_leave142(&snapshot_lock148);last8(18);return 0;}
 w8_process_record148 record=s->view.records[s->next];process_entry148 result={.size=sizeof(result),.pid=record.pid,.threads=record.threads,.parent=record.parent,.priority=8};
 if(utf8_to16(record.name,result.name,260)<0){lock_leave142(&snapshot_lock148);last8(1113);return 0;}++s->next;lock_leave142(&snapshot_lock148);memcpy(out,&result,sizeof(result));return 1;
}
static int MS f_Process32FirstW(HANDLE handle,process_entry148*out){return process_next148(handle,out,1);}
static int MS f_Process32NextW(HANDLE handle,process_entry148*out){return process_next148(handle,out,0);}
