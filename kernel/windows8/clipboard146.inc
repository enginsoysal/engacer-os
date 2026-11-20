/* Session text clipboard: checked copies, no application pointers retained. */
extern unsigned desktop_clipboard_read146(char*,char*,unsigned,uint64_t*);
extern unsigned desktop_clipboard_write146(const char*,const char*,unsigned);
static unsigned clip_open146,clip_space146,clip_thread146;
static uint64_t clip_open_window146,clip_owner146;
static unsigned clip_caller146(void){return clip_open146&&clip_space146==active_space142&&clip_thread146==current142;}
static ui_window144 *clip_live_owner146(void){
 ui_window144*w=ui_lookup144(clip_owner146);
 if(w&&spaces142[w->space]){thread142*t=spaces142[w->space]->threads+w->thread;if(t->state&&t->state!=T142_EXITED&&!t->exiting)return w;}
 clip_owner146=0;return 0;
}
static unsigned clip_can_notify146(void){
 ui_window144*w=clip_live_owner146();if(!w)return 1;
 wui_queue144*q=ui_queue144(w->space,w->thread,1);return q&&q->count<WUI_QUEUE144;
}
static unsigned clip_notify146(void){
 ui_window144*w=clip_live_owner146();if(!w)return 1;
 wui_message144 message={.window=w->view.handle,.message=0x307,.time=(uint32_t)(m3_clock_ticks()*10)};
 return ui_enqueue144(w->space,w->thread,&message,1);
}
unsigned w8_clipboard_native_allowed146(void){return !clip_open146&&clip_can_notify146();}
unsigned w8_clipboard_native_readable146(void){return !clip_open146;}
void w8_clipboard_native_changed146(void){if(clip_notify146())clip_owner146=0;else serial_text("M146_CLIPBOARD_NOTIFY_REFUSED\n");}
static void clip_owner_destroy146(uint64_t window){if(clip_owner146==window)clip_owner146=0;if(clip_open146&&clip_open_window146==window){clip_open146=0;clip_open_window146=0;}}
static void clip_thread_release146(unsigned space,unsigned thread){if(clip_open146&&clip_space146==space&&clip_thread146==thread){clip_open146=0;clip_open_window146=0;}}
static void *clip_page146(void){uint64_t page=page_alloc();if(!page)return 0;++clipboard_resident144;group_peak142();return(void*)(uintptr_t)page;}
static void clip_free146(void*page){if(page){page_free((uint64_t)(uintptr_t)page);--clipboard_resident144;}}
static unsigned clip_byte146(const char*first,const char*second,unsigned at){return(uint8_t)(at<4096?first[at]:second[at-4096]);}
static unsigned clip_valid146(const char*first,const char*second,unsigned bytes){
 if(!bytes||clip_byte146(first,second,bytes-1))return 0;unsigned at=0;
 while(at+1<bytes){char sample[4]={0};unsigned n=bytes-1-at;if(n>4)n=4;for(unsigned i=0;i<n;++i)sample[i]=(char)clip_byte146(first,second,at+i);
  unsigned consumed=0;uint32_t scalar;if(!decode_utf8_143(sample,n,&consumed,&scalar)||!scalar)return 0;at+=consumed;
 }return at==bytes-1;
}
static int64_t clip_call146(uint64_t operation,uint64_t pointer,uint64_t argument){
 if(operation==WCLIP_OPEN146){
  if(argument)return -87;if(pointer&&!ui_owned144(pointer))return -1400;
  if(clip_open146)return clip_caller146()&&clip_open_window146==pointer?0:-5;
  clip_open146=1;clip_space146=active_space142;clip_thread146=current142;clip_open_window146=pointer;return 1;
 }
 if(operation==WCLIP_OPEN_WINDOW146)return pointer||argument?-87:(int64_t)(clip_open146?clip_open_window146:0);
 if(operation==WCLIP_STATE146){
  if(argument>1)return -87;if(argument&&!clip_caller146())return -1418;
  wclip_state146 state={0};state.bytes=desktop_clipboard_read146(0,0,0,&state.revision);ui_window144*w=clip_live_owner146();state.owner=w?w->view.handle:0;
  return user8(pointer,&state,sizeof(state),1)?-998:0;
 }
 if(!clip_caller146())return -1418;
 if(operation==WCLIP_CLOSE146){if(pointer||argument)return -87;clip_open146=0;clip_open_window146=0;return 0;}
 if(operation==WCLIP_EMPTY146){
  if(pointer||argument)return -87;uint64_t revision;desktop_clipboard_read146(0,0,0,&revision);if(revision>=INT64_MAX)return -1816;
  if(!clip_can_notify146()||!clip_notify146())return -1816;unsigned error=desktop_clipboard_write146(0,0,0);if(error)return -(int64_t)error;clip_owner146=clip_open_window146;return 0;
 }
 if(operation!=WCLIP_READ146&&operation!=WCLIP_WRITE146)return -87;
 wclip_transfer146 request;if(argument)return -87;if(user8(pointer,&request,sizeof(request),0))return -998;
 if(request.reserved||!request.buffer||!request.bytes||request.bytes>8192)return -87;
 uint64_t revision=0;unsigned bytes=desktop_clipboard_read146(0,0,0,&revision);
 if(operation==WCLIP_WRITE146){if(request.revision)return -87;if(!clip_open_window146||clip_owner146!=clip_open_window146)return -1418;bytes=request.bytes;}
 else{if(request.revision!=revision)return -1237;if(!bytes)return -1168;if(request.bytes<bytes)return -122;}
 char*first=clip_page146();char*second=bytes>4096?clip_page146():0;int64_t result=-8;
 if(!first||(bytes>4096&&!second))goto done;
 if(operation==WCLIP_WRITE146){
  unsigned n=bytes>4096?4096:bytes;if(user8(request.buffer,first,n,0)||(bytes>n&&user8(request.buffer+n,second,bytes-n,0))){result=-998;goto done;}
  if(!clip_valid146(first,second,bytes)){result=-1113;goto done;}
  unsigned error=desktop_clipboard_write146(first,second,bytes);result=error?-(int64_t)error:(int64_t)(revision+1);
 }else{
  uint64_t fresh;unsigned actual=desktop_clipboard_read146(first,second,bytes,&fresh);if(actual!=bytes||fresh!=revision){result=-1237;goto done;}
  if(!clip_valid146(first,second,bytes)){result=-1113;goto done;}
  unsigned n=bytes>4096?4096:bytes;result=user8(request.buffer,first,n,1)||(bytes>n&&user8(request.buffer+n,second,bytes-n,1))?-998:0;
 }
done:clip_free146(second);clip_free146(first);return result;
}
