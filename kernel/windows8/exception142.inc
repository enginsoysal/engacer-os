/* Checked fault packets on lazy, private exception stacks. */
#define EXCEPTION_LOW142(i) (UINT64_C(0x108000000)+(uint64_t)(i)*0x10000)
static unsigned access_exception142(uint64_t address,unsigned permissions){uint64_t*p=pte8(address,0);return address>=W8_BASE&&address<W8_LIMIT&&p&&(*p&(1|RESERVED141))&&(!(permissions&2)||(*p&2))&&(!(permissions&4)||!(*p&NX));}
static unsigned enter_exception142(trap_frame*f,uint64_t address){
 thread142*t=threads142+current142;uint64_t entry=spaces142[active_space142]->exception_entry;if(!entry||t->exception_depth==4||!access_exception142(entry,4))return 0;
 uint64_t low=EXCEPTION_LOW142(current142),top=low+32768;
 if(!t->exception_stack){if(reserve141(low,32768,3,1))return 0;t->exception_stack=low;}
 uint64_t ceiling=t->exception_depth?f->rsp:top;if(ceiling>top||ceiling<low+8192)return 0;
 uint64_t packet=(ceiling-sizeof(w8_exception_packet142)-256)&~UINT64_C(15);if(packet<low+4096)return 0;
 w8_exception_packet142 value={0};w8_context142*c=&value.context;
 c->flags=0x10000f;c->cs=0x1b;c->ss=0x23;c->eflags=(uint32_t)f->rflags;
#define SAVE142(name) c->name=f->name
 SAVE142(rax);SAVE142(rcx);SAVE142(rdx);SAVE142(rbx);SAVE142(rsp);SAVE142(rbp);SAVE142(rsi);SAVE142(rdi);SAVE142(r8);SAVE142(r9);SAVE142(r10);SAVE142(r11);SAVE142(r12);SAVE142(r13);SAVE142(r14);SAVE142(r15);SAVE142(rip);
#undef SAVE142
 __asm__ volatile("fxsave64 %0":"=m"(c->fx)::"memory");memcpy(&c->mxcsr,c->fx+24,4);
 value.record.code=f->vector==14?0xc0000005u:f->vector==6?0xc000001du:f->vector==0?0xc0000094u:0xc0000001u;value.record.address=f->rip;
 if(f->vector==14){value.record.count=2;value.record.arguments[0]=(f->error&16)?8:(f->error&2)?1:0;value.record.arguments[1]=address;}
 value.pointers.record=packet+offsetof(w8_exception_packet142,record);value.pointers.context=packet+offsetof(w8_exception_packet142,context);
 if(user8(packet,&value,sizeof(value),1))return 0;uint64_t zero=0;if(user8(packet-8,&zero,8,1))return 0;
 t->exception_packets[t->exception_depth++]=packet;f->rip=entry;f->rsp=packet-8;f->rdi=packet;f->rflags=0x202;return 1;
}
static int64_t return_exception142(trap_frame*f,uint64_t packet){
 thread142*t=threads142+current142;if(!t->exception_depth||t->exception_packets[t->exception_depth-1]!=packet){finish8(0xc0000028u);return -1;}
 w8_context142 c;if(user8(packet+offsetof(w8_exception_packet142,context),&c,sizeof(c),0)||!access_exception142(c.rip,4)||!c.rsp||!access_exception142(c.rsp-1,2)){finish8(0xc0000028u);return -1;}
 _Alignas(16) uint8_t trusted_fx[512];__asm__ volatile("fxsave64 %0":"=m"(trusted_fx));uint32_t mask;memcpy(&mask,trusted_fx+28,4);if(!mask)mask=0xffbf;if(c.mxcsr&~mask){finish8(0xc0000028u);return -1;}memcpy(c.fx+24,&c.mxcsr,4);
#define RESTORE142(name) f->name=c.name
 RESTORE142(rax);RESTORE142(rcx);RESTORE142(rdx);RESTORE142(rbx);RESTORE142(rsp);RESTORE142(rbp);RESTORE142(rsi);RESTORE142(rdi);RESTORE142(r8);RESTORE142(r9);RESTORE142(r10);RESTORE142(r11);RESTORE142(r12);RESTORE142(r13);RESTORE142(r14);RESTORE142(r15);RESTORE142(rip);
#undef RESTORE142
 f->cs=0x1b;f->ss=0x23;f->rflags=(c.eflags&0x240dd5u)|0x202u;--t->exception_depth;__asm__ volatile("fxrstor64 %0"::"m"(c.fx):"memory");return (int64_t)c.rax;
}
