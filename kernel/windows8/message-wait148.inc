/* Queue-only MsgWait uses the existing object-wait scheduler and lazy queue. */
static uint64_t ui_message_timer_deadline148(unsigned thread,unsigned mask){
 if(!(mask&16u))return UINT64_MAX;ui_timer_page144*page=ui_timer_pages144[active_space142];wui_queue144*q=ui_queue144(active_space142,thread,0);uint64_t due=UINT64_MAX;if(page&&q)for(unsigned i=0;i<64;++i){ui_timer_record144*t=page->items+i;if(t->period&&t->thread==thread&&t->due>q->timer_seen148&&t->due<due)due=t->due;}return due;
}
static unsigned ui_message_ready148(unsigned thread,uint64_t mask){wui_queue144*q=ui_queue144(active_space142,thread,0);if(!q)return 0;if(q->new_input148&(unsigned)mask)return 1;uint64_t due=ui_message_timer_deadline148(thread,(unsigned)mask);return due!=UINT64_MAX&&due<=m3_clock_ticks()*10;}
