/* One outstanding top-level filter frame per native i386 process. */
#include <engine/winexception32_1410.h>
#define PE32_EXCEPTION1410 UINT32_C(0x5fd00000)

typedef struct {
 win_exception_pointers321410 pointers;
 win_exception_record321410 exception;
 win_context321410 context;
} pe32_exception1410;

static unsigned pe32_executable1410(uint32_t address){
 uint64_t *entry=pte8(address,0);
 return entry&&(*entry&5)==5&&!(*entry&NX);
}
static unsigned pe32_set_filter1410(uint32_t filter){
 private_space142 *space=spaces142[active_space142];
 if(filter&&!pe32_executable1410(filter))return pe32_error1410(998,0);
 uint64_t *page=pte8(PE32_EXCEPTION1410,0);
 if(filter&&(!page||!(*page&1))&&map8(PE32_EXCEPTION1410,8192,3))
  return pe32_error1410(8,0);
 uint32_t replaced=space->compat_filter;
 space->compat_filter=filter;
 return replaced;
}
static unsigned pe32_fault_status1410(const trap_frame *frame){
 switch(frame->vector){
 case 0:return 0xc0000094u;
 case 6:return 0xc000001du;
 case 14:return 0xc0000005u;
 default:return 0;
 }
}
static unsigned pe32_deliver_exception1410(trap_frame *frame,uint64_t address){
 private_space142 *space=spaces142[active_space142];
 unsigned status=pe32_fault_status1410(frame);
 if(!status||space->compat_exception||!space->compat_filter||
    !pe32_executable1410(space->compat_filter))return 0;
 pe32_exception1410 packet;
 memset(&packet,0,sizeof(packet));
 packet.pointers.record=PE32_EXCEPTION1410+offsetof(pe32_exception1410,exception);
 packet.pointers.context=PE32_EXCEPTION1410+offsetof(pe32_exception1410,context);
 packet.exception.code=status;packet.exception.address=(uint32_t)frame->rip;
 if(frame->vector==14){
  packet.exception.count=2;
  packet.exception.arguments[0]=(frame->error&16)?8:(frame->error&2)?1:0;
  packet.exception.arguments[1]=(uint32_t)address;
 }
 packet.context=(win_context321410){.flags=WIN32_FULL_CONTEXT1410,
  .ds=0x23,.es=0x23,.cs=0x3b,.ss=0x23,
  .edi=(uint32_t)frame->rdi,.esi=(uint32_t)frame->rsi,.ebx=(uint32_t)frame->rbx,
  .edx=(uint32_t)frame->rdx,.ecx=(uint32_t)frame->rcx,.eax=(uint32_t)frame->rax,
  .ebp=(uint32_t)frame->rbp,.eip=(uint32_t)frame->rip,
  .eflags=(uint32_t)frame->rflags,.esp=(uint32_t)frame->rsp};
 uint32_t stack=PE32_EXCEPTION1410+8192-8;
 uint32_t arguments[]={PE32_EXCEPTION_RETURN1410,PE32_EXCEPTION1410};
 if(user8(PE32_EXCEPTION1410,&packet,sizeof(packet),1)||user8(stack,arguments,sizeof(arguments),1))return 0;
 space->compat_exception=status;
 frame->rip=space->compat_filter;frame->rsp=stack;
 frame->rflags=(frame->rflags&~UINT64_C(0x500))|UINT64_C(0x202);
 return 1;
}
static uint32_t pe32_finish_filter1410(trap_frame *frame,uint32_t disposition){
 private_space142 *space=spaces142[active_space142];
 unsigned status=space->compat_exception;
 if(!status){finish8(0xc000001du);return 0;}
 if(disposition!=UINT32_MAX){finish8(status);return 0;}
 win_context321410 saved;
 if(user8(PE32_EXCEPTION1410+offsetof(pe32_exception1410,context),&saved,sizeof(saved),0)||
    saved.flags!=WIN32_FULL_CONTEXT1410||saved.cs!=0x3b||saved.ss!=0x23||
    !pe32_executable1410(saved.eip)||saved.esp<=PE32_STACK1410-PE32_STACK_BYTES1410||
    saved.esp>PE32_STACK1410){
  finish8(status);return 0;
 }
 space->compat_exception=0;
 frame->rdi=saved.edi;frame->rsi=saved.esi;frame->rbx=saved.ebx;
 frame->rdx=saved.edx;frame->rcx=saved.ecx;frame->rbp=saved.ebp;
 frame->rip=saved.eip;frame->rsp=saved.esp;
 /* Keep privilege, virtualisation and interrupt-control bits kernel-owned. */
 frame->rflags=(saved.eflags&0x8d5u)|0x202u;
 return saved.eax;
}
