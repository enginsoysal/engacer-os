/* Normal exit keeps mappings alive throughout reverse-order DLL notifications.
 * The kernel, rather than a callback, ultimately releases process ownership.
 * Forced cancellation and unhandled faults deliberately bypass this routine. */
void pe8_shutdown(void){
 if(terminating142)return;terminating142=1;
 for(unsigned pass=0;pass<MODULES141;++pass){
  int chosen=-1;
  for(unsigned i=0;i<MODULES141;++i)if(modules141[i].state&&modules141[i].attached&&(chosen<0||modules141[i].sequence>modules141[chosen].sequence))chosen=(int)i;
  if(chosen<0)break;module141*m=modules141+chosen;m->attached=0;
  if(m->dll&&m->entry)(void)((int(MS*)(void*,unsigned,void*))(m->base+m->entry))(m->base,0,(void*)(uintptr_t)1);
 }
}
