/* Menus are measured and painted from the application's real owned menu tree. */
static unsigned menu_label145(const WCHAR*source,WCHAR*out){unsigned n=0;if(source)for(unsigned at=0;source[at]&&source[at]!=9&&n<159;++at){if(source[at]=='&'){if(source[at+1]!='&')continue;++at;}out[n++]=source[at];}out[n]=0;return n;}
static int menu_width145(HANDLE dc,const WCHAR*text){WCHAR label[160];unsigned n=menu_label145(text,label);int size[2];return f_GetTextExtentPoint32W(dc,label,(int)n,size)?size[0]+24:0;}
static int menu_paint145(HANDLE h){
 ui_window_runtime144*w=ui_window_lookup144(h);if(!w||w->thread!=tid142()||w->description.parent){last8(w?5:1400);return 0;}HANDLE menu=w->menu;
 int64_t status=ui_call144(WUI_MENUBAR145,h,0,menu?24:0);if(status<0){last8((unsigned)-status);return 0;}if(!menu)return 1;
 HANDLE dc=f_GetDC(h);native_dc144*d=dc_lookup144(dc);if(!d)return 0;d->menu_surface=1;d->clip=(win_rect144){0,0,w->description.bounds.width-2,24};d->background_mode=1;
 wui_draw144 clear={.kind=3};int ok=draw_call144(d,&clear)&&f_FillRect(dc,&d->clip,16);int x=0;
 lock_enter142(&menu_lock144);menu144*m=menu_lookup144(menu);if(!m)ok=0;unsigned count=0;
 for(menu_item144*i=m?m->items:0;ok&&i&&x<d->clip.right;i=i->next){if(++count>32){last8(1816);ok=0;break;}WCHAR label[160];unsigned n=menu_label145(i->text,label);int width=menu_width145(dc,i->text);if(!width){ok=0;break;}f_SetTextColor(dc,i->state&3?0x808080:0);ok=f_TextOutW(dc,x+12,4,label,(int)n);x+=width;}
 lock_leave142(&menu_lock144);f_ReleaseDC(h,dc);return ok;
}
static unsigned menu_open145(HANDLE,HANDLE,unsigned,int);
static int64_t menu_nonclient145(HANDLE h,uint64_t hit,int64_t position){
 if(hit!=5)return 0;ui_window_runtime144*w=ui_window_lookup144(h);if(!w||!w->description.enabled)return 0;
 int x=(int16_t)(position&65535)-w->description.bounds.x-1;HANDLE menu=w->menu;if(!menu)return 0;
 f_SendMessageW(h,0x116,menu,0);if(!f_IsWindow(h))return 0;
 HANDLE dc=f_GetDC(h);if(!dc)return 0;HANDLE sub=0;unsigned id=0,index=0;int left=0,chosen_left=0;
 lock_enter142(&menu_lock144);menu144*m=menu_lookup144(menu);for(menu_item144*i=m?m->items:0;i&&index<32;i=i->next,++index){int width=menu_width145(dc,i->text);if(x>=left&&x<left+width){if(!(i->state&3)){sub=i->submenu;id=i->id;chosen_left=left;}break;}left+=width;}lock_leave142(&menu_lock144);f_ReleaseDC(h,dc);
 if(sub){unsigned command=menu_open145(h,sub,index,chosen_left);if(command&&f_IsWindow(h))f_SendMessageW(h,0x111,command,0);}else if(id)f_SendMessageW(h,0x111,id,0);return 0;
}
