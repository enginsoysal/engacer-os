/* Ordinary pointer/space activation; group boxes and disabled controls do not click. */
static int64_t button_input145(ui_window_runtime144*w,control_state144*c,unsigned message,uint64_t wp,int64_t lp,unsigned*handled){
 *handled=1;unsigned type=w->description.style&15;HANDLE h=w->handle;
 if(message==0x215){c->selected=-1;f_InvalidateRect(h,0,0);return 0;}
 if(message==0x201){if(type!=7&&w->description.enabled){c->selected=0;f_SetFocus(h);f_SetCapture(h);f_InvalidateRect(h,0,0);}return 0;}
 if(message==0x202){int was_pressed=c->selected>=0;c->selected=-1;win_rect144 client;f_GetClientRect(h,&client);int x=(int16_t)(lp&65535),y=(int16_t)((uint64_t)lp>>16);HANDLE parent=w->description.parent;unsigned id=(unsigned)w->id;
  unsigned clicked=was_pressed&&type!=7&&w->description.enabled&&x>=0&&y>=0&&x<client.right&&y<client.bottom;
  if(clicked&&type==3)c->checked=!c->checked;else if(clicked&&type==6)c->checked=(c->checked+1)%3;
  if(f_GetCapture()==h)f_ReleaseCapture();f_InvalidateRect(h,0,0);if(clicked&&parent)f_SendMessageW(parent,0x111,id&65535,(int64_t)h);return 0;
 }
 if((message==0x100||message==0x101)&&wp==32){if(type!=7&&w->description.enabled){if(message==0x100)c->selected=0;else{int was_pressed=c->selected>=0;c->selected=-1;if(was_pressed)f_SendMessageW(h,0xf5,0,0);}f_InvalidateRect(h,0,0);}return 0;}
 *handled=0;return 0;
}
