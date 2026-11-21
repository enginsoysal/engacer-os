/* Preserve Win64 nonvolatile registers while entering the PE exception caller. */
__attribute__((used,noinline)) static NORETURN void MS software_raise_failed148(void){fail8("The software exception request could not be dispatched.");}
__attribute__((naked)) static void MS f_RaiseException(unsigned code,unsigned flags,unsigned count,const uint64_t*arguments){
 __asm__ volatile("push %%rdi; push %%rsi; mov %%rcx,%%rdi; mov %%rdx,%%rsi; mov %%r8,%%rdx; mov %%r9,%%r10; mov %0,%%eax; int $0x80; pop %%rsi; pop %%rdi; jmp software_raise_failed148"::"i"(W8_SYS_SOFTWARE148));
}
