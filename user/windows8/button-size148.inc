/* Ideal geometry derives from the actual selected font and native button chrome. */
static int64_t button_ideal148(ui_window_runtime144*w,control_state144*c,uint64_t wp,int64_t lp){
 int*out=(int*)(uintptr_t)lp;if(wp){last8(87);return 0;}if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,8,3,0,0)){last8(998);return 0;}int desired=out[0];if(desired<0||desired>16384){last8(87);return 0;}
 if(!ui_refresh144(w))return 0;unsigned style=w->description.style,type=style&15;
 if(type!=0&&type!=1){out[0]=w->description.bounds.width;out[1]=w->description.bounds.height;return 1;}
 if(style&(0x2000u|0xc0u)){last8(50);return 0;}HANDLE dc=f_GetDC(w->handle);if(!dc)return 0;if(c->font&&!f_SelectObject(dc,c->font)){f_ReleaseDC(w->handle,dc);return 0;}int size[2];unsigned length=wlen8(w->description.title);if(length>159)length=159;int ok=f_GetTextExtentPoint32W(dc,w->description.title,(int)length,size);f_ReleaseDC(w->handle,dc);if(!ok)return 0;
 int width=desired?desired:size[0]+24+((c->style&1)?24:0),height=size[1]+12;if(height<32)height=32;if(width>16384||height>16384){last8(87);return 0;}out[0]=width;out[1]=height;return 1;
}
