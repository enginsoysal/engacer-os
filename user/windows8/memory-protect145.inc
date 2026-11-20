/* Real process-private page permissions. Unsupported modes fail explicitly. */
static lock142 virtual_lock145;
static void *MS f_VirtualAlloc(void*requested,size_t size,unsigned flags,unsigned protect){
 if(!size||size>24*1024*1024||(flags&~0x3000u)||!(flags&0x1000u)||(protect!=4&&protect!=2)){last8(50);return 0;}
 uint64_t bytes=(size+4095)&~UINT64_C(4095);lock_enter142(&virtual_lock145);uint64_t base=requested?(uint64_t)(uintptr_t)requested:next_virtual8;
#ifdef ENGINE_M14
 if(!requested){int64_t skipped=(int64_t)sys8(W8_SYS_MAPPING146,WMAP_SKIP146,base,bytes,0,0);if(skipped<0){lock_leave142(&virtual_lock145);last8((unsigned)-skipped);return 0;}base=(uint64_t)skipped;}
#endif
 if(base<UINT64_C(0x128000000)||base>=UINT64_C(0x138000000)||bytes>UINT64_C(0x138000000)-base||(base&4095)){lock_leave142(&virtual_lock145);last8(487);return 0;}
 unsigned slot=0;while(slot<128&&virtual_blocks8[slot].live)++slot;
 if(slot==128||sys8(W8_SYS_MAP,base,bytes,protect==4?3:1,0,0)){lock_leave142(&virtual_lock145);last8(8);return 0;}
 virtual_blocks8[slot]=(virtual8){base,bytes,1};if(!requested)next_virtual8=base+((bytes+65535)&~UINT64_C(65535));lock_leave142(&virtual_lock145);return (void*)(uintptr_t)base;
}
static int MS f_VirtualFree(void*p,size_t size,unsigned type){
 uint64_t base=(uint64_t)(uintptr_t)p;lock_enter142(&virtual_lock145);
 for(unsigned i=0;i<128;++i)if(virtual_blocks8[i].live&&virtual_blocks8[i].base==base){virtual8*v=virtual_blocks8+i;if(type!=0x8000||size){lock_leave142(&virtual_lock145);last8(87);return 0;}
  if(sys8(W8_SYS_UNMAP,v->base,v->size,0,0,0)){lock_leave142(&virtual_lock145);last8(487);return 0;}v->live=0;lock_leave142(&virtual_lock145);return 1;}
 lock_leave142(&virtual_lock145);last8(487);return 0;
}
static int MS f_VirtualProtect(void*pointer,size_t size,unsigned protection,unsigned*old){
 uint64_t address=(uint64_t)(uintptr_t)pointer;if(!size||address<W8_BASE||address>=W8_LIMIT||size>W8_LIMIT-address||!old){last8(87);return 0;}
 unsigned permissions=protection==2?1:protection==4?3:protection==32?5:0;if(!permissions){last8(50);return 0;}
 uint64_t first=address&~UINT64_C(4095),end=(address+size+4095)&~UINT64_C(4095),bytes=end-first;
 int64_t result=-487;unsigned matched=0;lock_enter142(&virtual_lock145);
 for(unsigned n=0;n<128;++n){virtual8*v=virtual_blocks8+n;if(v->live&&first>=v->base&&first-v->base<v->size&&bytes<=v->size-(first-v->base)){matched=1;result=(int64_t)sys8(W8_SYS_PAGE145,first,bytes,permissions,(uint64_t)(uintptr_t)old,0);break;}}

#ifdef ENGINE_M14
 if(!matched&&(int64_t)sys8(W8_SYS_MAPPING146,WMAP_QUERY146,first,bytes,0,0)>0){matched=1;result=(int64_t)sys8(W8_SYS_PAGE145,first,bytes,permissions,(uint64_t)(uintptr_t)old,0);}
#endif
 lock_leave142(&virtual_lock145);if(!matched)result=pe8_protect145(first,bytes,permissions,(uint64_t)(uintptr_t)old);
 if(result<0){last8((unsigned)-result);return 0;}return 1;
}
