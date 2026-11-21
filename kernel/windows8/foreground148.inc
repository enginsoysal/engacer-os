/* Bounded bridge request; only the desktop publishes actual foreground state. */
extern unsigned w8_desktop_foreground_allowed148(uint64_t);
uint64_t w8_ui_foreground_request148(void){uint64_t handle=__atomic_exchange_n(&ui_foreground_pending148,0,__ATOMIC_ACQ_REL);ui_window144*w=ui_lookup144(handle);return w&&w->view.description.visible&&ui_enabled_chain144(w)&&!w->view.description.parent&&!(w->view.description.style&0x20000000u)?handle:0;}
void w8_ui_foreground_changed148(uint64_t handle){ui_foreground148=ui_lookup144(handle)?handle:0;}
