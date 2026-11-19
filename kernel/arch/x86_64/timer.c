#include <engine/base.h>
/* Legacy PC baseline only. APIC/per-CPU timers replace this during the SMP step. */
void timer_start(void) {
    out8(0x20,0x11);out8(0xa0,0x11);
    out8(0x21,0x20);out8(0xa1,0x28);
    out8(0x21,4);out8(0xa1,2);
    out8(0x21,1);out8(0xa1,1);
    /* PIT channel zero, low/high byte, mode 2; approximately 100 Hz. */
    out8(0x43,0x34);out8(0x40,0x9c);out8(0x40,0x2e);
    out8(0xa1,255);out8(0x21,254);
}
void timer_stop(void) {out8(0x21,255);out8(0xa1,255);}
void timer_acknowledge(void) {out8(0x20,0x20);}

/* Share the existing PIT interrupt between network deadlines and Windows waits. */
static unsigned timer_owners142,timer_saved142;
void timer_claim142(unsigned owner,unsigned active){
 uint64_t flags;__asm__ volatile("pushfq;popq %0;cli":"=r"(flags)::"memory");
 unsigned previous=timer_owners142;if(active)timer_owners142|=owner;else timer_owners142&=~owner;
 if(!previous&&timer_owners142)timer_saved142=in8(0x21)&1;
 if(timer_owners142)out8(0x21,in8(0x21)&~1u);
 else if(previous)out8(0x21,(uint8_t)((in8(0x21)&~1u)|timer_saved142));
 if(flags&512)__asm__ volatile("sti":::"memory");
}
