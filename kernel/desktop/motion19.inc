/* Bounded native input-to-presentation diagnostics, never an idle worker.
   Samples end after CPU composition, framebuffer writes and cursor presentation.
   External virtual/physical scanout and host transport are separate measures. */
typedef struct {
 uint64_t sequence,received_us,completed_us;
 int32_t x,y;
 uint32_t flags,paint;
} motion_sample19;
static volatile struct {uint64_t count;motion_sample19 samples[64];} motion19;
static void motion_record19(unsigned buttons,unsigned surface){
 uint64_t received=input13_pointer_us();if(!received)return;
 uint64_t completed=m3_clock_microseconds();if(completed<received)return;
 uint64_t sequence=motion19.count;
 motion19.samples[sequence&63]=(motion_sample19){sequence+1,received,completed,(int32_t)pointer_x,(int32_t)pointer_y,(dragging?1u:0)|(drag_resize?2u:0)|surface|(context11?8u:0)|(launcher?16u:0)|(buttons<<8),(uint32_t)paints};
 __atomic_store_n(&motion19.count,sequence+1,__ATOMIC_RELEASE);
}
