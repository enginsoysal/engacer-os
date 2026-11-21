/* Lazy FLS for the current one-fiber-per-native-thread execution profile.
 * Fiber switching is not implemented. Callbacks run outside the state lock. */
typedef struct {
 uint64_t callbacks[64],values[16][64];
 unsigned char state[64];
 unsigned busy,cleaning;
} fls_context147;
static fls_context147 *fls147;
static lock142 fls_lock147;
static void fls_release147(void){
 if(!fls147||fls147->busy)return;
 for(unsigned i=0;i<64;++i)if(fls147->state[i])return;
 fls_context147 *old=fls147;fls147=0;free8(old);
}
static unsigned MS f_FlsAlloc(uint64_t callback){
 lock_enter142(&fls_lock147);
 if(!fls147)fls147=calloc8(1,sizeof(*fls147));
 if(!fls147){lock_leave142(&fls_lock147);last8(8);return UINT32_MAX;}
 for(unsigned i=0;i<64;++i)if(!fls147->state[i]){
  fls147->callbacks[i]=callback;fls147->state[i]=1;
  for(unsigned row=0;row<16;++row)fls147->values[row][i]=0;
  lock_leave142(&fls_lock147);return i;
 }
 lock_leave142(&fls_lock147);last8(259);return UINT32_MAX;
}
static int MS f_FlsFree(unsigned index){
 uint64_t values[16],callback;lock_enter142(&fls_lock147);
 if(!fls147||index>=64||fls147->state[index]!=1){lock_leave142(&fls_lock147);last8(87);return 0;}
 fls_context147 *context=fls147;context->state[index]=2;++context->busy;callback=context->callbacks[index];
 for(unsigned row=0;row<16;++row){values[row]=context->values[row][index];context->values[row][index]=0;}
 lock_leave142(&fls_lock147);
 if(callback)for(unsigned row=0;row<16;++row)if(values[row])((void(MS*)(void*))(uintptr_t)callback)((void*)(uintptr_t)values[row]);
 lock_enter142(&fls_lock147);context->callbacks[index]=0;context->state[index]=0;--context->busy;fls_release147();lock_leave142(&fls_lock147);return 1;
}
static uint64_t MS f_FlsGetValue(unsigned index){
 unsigned row=tid142()&255;lock_enter142(&fls_lock147);
 int valid=fls147&&row<16&&index<64&&fls147->state[index]==1;uint64_t value=valid?fls147->values[row][index]:0;
 lock_leave142(&fls_lock147);last8(valid?0:87);return value;
}
static int MS f_FlsSetValue(unsigned index,uint64_t value){
 unsigned row=tid142()&255;lock_enter142(&fls_lock147);
 int valid=fls147&&row<16&&index<64&&fls147->state[index]==1;if(valid)fls147->values[row][index]=value;
 lock_leave142(&fls_lock147);if(!valid)last8(87);return valid;
}
void fls_thread_exit147(void){
 unsigned row=tid142()&255;if(row>=16)fail8("Invalid native FLS thread slot.");
 lock_enter142(&fls_lock147);if(!fls147){lock_leave142(&fls_lock147);return;}
 fls_context147 *context=fls147;if(context->cleaning&(1u<<row)){lock_leave142(&fls_lock147);fail8("Recursive FLS thread termination.");}
 context->cleaning|=1u<<row;++context->busy;lock_leave142(&fls_lock147);
 for(unsigned pass=0;pass<4;++pass){
  uint64_t values[64],callbacks[64];unsigned count=0;lock_enter142(&fls_lock147);
  for(unsigned i=0;i<64;++i){values[i]=context->values[row][i];callbacks[i]=context->state[i]==1?context->callbacks[i]:0;context->values[row][i]=0;if(values[i]&&callbacks[i])++count;}
  lock_leave142(&fls_lock147);if(!count)break;
  for(unsigned i=0;i<64;++i)if(values[i]&&callbacks[i])((void(MS*)(void*))(uintptr_t)callbacks[i])((void*)(uintptr_t)values[i]);
 }
 lock_enter142(&fls_lock147);unsigned pending=0;
 for(unsigned i=0;i<64;++i)if(context->values[row][i]&&context->state[i]==1&&context->callbacks[i])pending=1;
 context->cleaning&=~(1u<<row);--context->busy;fls_release147();lock_leave142(&fls_lock147);
 if(pending)fail8("FLS callbacks repeatedly rearmed data beyond the cleanup bound.");
}
