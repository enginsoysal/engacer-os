/* Reuse existing control fields: no progress allocation or animation timer. */
static int progress_clamp148(const control_state144*c,int64_t value){return value<c->edges[0]?c->edges[0]:value>c->edges[1]?c->edges[1]:(int)value;}
static int64_t progress_message148(ui_window_runtime144*w,control_state144*c,unsigned msg,uint64_t wp,int64_t lp,unsigned*handled){
 *handled=1;int old=c->selected;unsigned changed=0;int64_t result=0;
 if(msg==0x406||msg==0x401){result=((unsigned)c->edges[0]&65535u)|(((unsigned)c->edges[1]&65535u)<<16);int low=msg==0x406?(int32_t)wp:(int)((uint64_t)lp&65535u),high=msg==0x406?(int32_t)lp:(int)(((uint64_t)lp>>16)&65535u);changed=low!=c->edges[0]||high!=c->edges[1];c->edges[0]=low;c->edges[1]=high;c->selected=progress_clamp148(c,c->selected);}
 else if(msg==0x402||msg==0x403){result=old;c->selected=progress_clamp148(c,msg==0x402?(int32_t)wp:(int64_t)c->selected+(int32_t)wp);}
 else if(msg==0x404){result=c->edges[2];c->edges[2]=(int32_t)wp;}
 else if(msg==0x405){result=old;int64_t value=(int64_t)c->selected+c->edges[2],span=(int64_t)c->edges[1]-c->edges[0];if(span>0&&(value<c->edges[0]||value>c->edges[1])){int64_t offset=(value-c->edges[0])%span;if(offset<0)offset+=span;value=c->edges[0]+offset;}c->selected=progress_clamp148(c,value);}
 else if(msg==0x407){if(lp){if(sys8(W8_SYS_ACCESS,(uint64_t)lp,8,2,0,0)){last8(998);return 0;}memcpy((void*)(uintptr_t)lp,c->edges,8);}return wp?c->edges[0]:c->edges[1];}
 else if(msg==0x408)return c->selected;
 else{*handled=0;return 0;}
 if(c->redraw&&(changed||old!=c->selected))f_InvalidateRect(w->handle,0,0);return result;
}
static void progress_paint148(native_dc144*d,control_state144*c,const win_rect144*client,unsigned style){
 f_FillRect(d->handle,client,17);win_rect144 inside={2,2,client->right-2,client->bottom-2};if(inside.right<=inside.left||inside.bottom<=inside.top)return;f_FillRect(d->handle,&inside,16);int64_t span=(int64_t)c->edges[1]-c->edges[0],position=(int64_t)c->selected-c->edges[0];if(span<=0||position<=0)return;if(position>span)position=span;win_rect144 bar=inside;if(style&4)bar.top=bar.bottom-(int)(((int64_t)bar.bottom-bar.top)*position/span);else bar.right=bar.left+(int)(((int64_t)bar.right-bar.left)*position/span);if(bar.right<=bar.left||bar.bottom<=bar.top)return;wui_draw144 draw={.kind=1,.color=0x2a9d8f,.bounds={bar.left,bar.top,bar.right-bar.left,bar.bottom-bar.top}};draw_call144(d,&draw);
}
