/* Preserve Win64 nonvolatile registers while entering the PE exception caller. */
__attribute__((used,noinline)) static NORETURN void MS software_raise_failed148(void){fail8("The software exception request could not be dispatched.");}
__attribute__((naked)) static void MS f_RaiseException(unsigned code,unsigned flags,unsigned count,const uint64_t*arguments){
 __asm__ volatile("push %%rdi; push %%rsi; mov %%rcx,%%rdi; mov %%rdx,%%rsi; mov %%r8,%%rdx; mov %%r9,%%r10; mov %0,%%eax; int $0x80; pop %%rsi; pop %%rdi; jmp software_raise_failed148"::"i"(W8_SYS_SOFTWARE148));
}

NORETURN void exception_resume148(w8_context142*context){
 uint64_t packet=(uint64_t)(uintptr_t)context-offsetof(w8_exception_packet142,context);
 sys8(W8_SYS_EXCEPTION_RETURN,packet,0,0,0,0);exit8(0xc0000028u);
}
static NORETURN void MS f_RtlUnwindEx(uint64_t target,uint64_t ip,w8_exception_record142*record,uint64_t value,w8_context142*context,uint64_t history){pe8_rtl_unwind148(target,ip,record,value,context,history);}
