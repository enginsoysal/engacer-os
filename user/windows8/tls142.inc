/* Static PE TLS is separate from dynamically allocated TlsAlloc indexes. */
static void *tls_vector142[16][MODULES141],*tls_storage142[16][MODULES141];
static void tls_vector_bind142(void){*(uint64_t*)(uintptr_t)(teb142()+0x58)=(uint64_t)(uintptr_t)tls_vector142[tid142()&255];}
static void tls_allocate142(module141*m,unsigned index,unsigned row){
 if(!m->tls_present||tls_storage142[row][index])return;
 uint64_t bytes=(uint64_t)m->tls_bytes+m->tls_zero,align=m->tls_alignment;
 void*storage=alloc8((size_t)(bytes+align));if(!storage)fail8("The Windows static TLS memory quota was reached.");
 uint8_t*data=(void*)(((uint64_t)(uintptr_t)storage+align-1)&~(align-1));
 memcpy(data,(void*)(uintptr_t)m->tls_template,m->tls_bytes);memset(data+m->tls_bytes,0,m->tls_zero);
 tls_storage142[row][index]=storage;tls_vector142[row][index]=data;
}
static unsigned tls_terminating142,tls_attaching142[16],tls_detaching142[16];
static void tls_notify_impl142(module141*m,unsigned reason){
 if(!m->tls_callbacks)return;
 for(unsigned i=0;i<64;++i){uint64_t callback=u64(rva141(m,(uint64_t)m->tls_callbacks+i*8,8));if(!callback)return;
  if(sys8(W8_SYS_ACCESS,callback,1,4,0,0))fail8("A Windows TLS callback is not executable user code.");
  ((void(MS*)(void*,unsigned,void*))(uintptr_t)callback)(m->base,reason,reason==0&&tls_terminating142?(void*)(uintptr_t)1:0);
 }fail8("The Windows TLS callback array exceeds its bound.");
}
static void tls_end142(module141*m,unsigned reason){tls_terminating142=1;tls_notify_impl142(m,reason);tls_terminating142=0;}
static void (*tls_notify142)(module141*,unsigned)=tls_end142;
static void tls_prepare142(module141*m,unsigned index,unsigned directory,unsigned bytes){
 if(!directory)return;if(bytes<40)fail8("The Windows TLS directory is truncated.");
 uint8_t*d=rva141(m,directory,40);uint64_t base=(uint64_t)(uintptr_t)m->base,start=u64(d),end=u64(d+8),at=u64(d+16),callbacks=u64(d+24);uint32_t zero=u32(d+32),flags=u32(d+36),alignment=(flags>>20)&15;
 if((flags&~0xf00000u)||end<start||end-start>65536||zero>65536-(end-start)||alignment>13)fail8("The Windows TLS template exceeds its bound.");
 if(start||end){if(start<base||!range141(start-base,end-start,m->size))fail8("The Windows TLS template is outside its image.");}
 if(at<base||(at&3))fail8("The Windows TLS index is invalid.");uint32_t*slot=rva141(m,at-base,4);*slot=index;
 if(callbacks){if(callbacks<base)fail8("The Windows TLS callback array is invalid.");unsigned ended=0;for(unsigned i=0;i<64;++i){uint64_t callback=u64(rva141(m,callbacks-base+(uint64_t)i*8,8));if(!callback){ended=1;break;}if(callback<base||callback-base>=m->size)fail8("A Windows TLS callback is outside its image.");}if(!ended)fail8("The Windows TLS callback array is not terminated.");m->tls_callbacks=(uint32_t)(callbacks-base);}
 m->tls_template=start;m->tls_bytes=(uint32_t)(end-start);m->tls_zero=zero;m->tls_alignment=alignment?UINT32_C(1)<<(alignment-1):16;m->tls_present=1;
 unsigned total=0;for(unsigned i=0;i<MODULES141;++i)if(modules141[i].tls_present)total+=modules141[i].tls_bytes+modules141[i].tls_zero;
 if(total>1024*1024)fail8("The Windows aggregate static TLS quota was reached.");
 w8_thread_snapshot threads[16];if((int64_t)sys8(W8_SYS_THREAD_LIST,(uint64_t)(uintptr_t)threads,0,0,0,0)<0)fail8("Windows thread TLS ownership could not be read.");
 for(unsigned row=0;row<16;++row)if(threads[row].state)tls_allocate142(m,index,row);tls_vector_bind142();
}
static void tls_release_module142(unsigned index){for(unsigned row=0;row<16;++row){free8(tls_storage142[row][index]);tls_storage142[row][index]=tls_vector142[row][index]=0;}}
static void tls_thread_notify142(unsigned reason){
 unsigned previous=reason==2?0:UINT32_MAX;
 for(unsigned pass=0;pass<MODULES141;++pass){int chosen=-1;
  for(unsigned i=0;i<MODULES141;++i){module141*m=modules141+i;if(!m->state||!m->attached)continue;if(reason==2){if(m->sequence>previous&&(chosen<0||m->sequence<modules141[chosen].sequence))chosen=(int)i;}else if(m->sequence<previous&&(chosen<0||m->sequence>modules141[chosen].sequence))chosen=(int)i;}
  if(chosen<0)break;module141*m=modules141+chosen;previous=m->sequence;
  tls_notify_impl142(m,reason);if(m->dll&&m->entry)(void)((int(MS*)(void*,unsigned,void*))(m->base+m->entry))(m->base,reason,0);
 }
}
void pe8_thread_attach(void){lock_enter142(&loader_lock142);unsigned row=tid142()&255;for(unsigned i=0;i<MODULES141;++i)if(modules141[i].state)tls_allocate142(modules141+i,i,row);tls_vector_bind142();tls_attaching142[row]=1;tls_thread_notify142(2);tls_attaching142[row]=0;lock_leave142(&loader_lock142);}
void pe8_thread_detach(void){lock_enter142(&loader_lock142);unsigned row=tid142()&255;if(tls_attaching142[row]||tls_detaching142[row])fail8("A Windows TLS callback attempted recursive thread termination.");tls_detaching142[row]=1;tls_thread_notify142(3);for(unsigned i=0;i<MODULES141;++i){free8(tls_storage142[row][i]);tls_storage142[row][i]=tls_vector142[row][i]=0;}tls_detaching142[row]=0;lock_leave142(&loader_lock142);}
