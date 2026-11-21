/* Native display-list DCs. Every retained primitive crosses checked copied IPC. */
typedef struct native_dc144 {struct native_dc144*next;HANDLE handle,window,font;unsigned thread,menu_surface,window_surface;uint32_t foreground,background;int background_mode;win_rect144 clip;} native_dc144;
static native_dc144*dcs144;static unsigned dc_serial144,dc_count144;
static native_dc144*dc_lookup144(HANDLE h){lock_enter142(&ui_lock144);for(native_dc144*d=dcs144;d;d=d->next)if(d->handle==h&&d->thread==tid142()){lock_leave142(&ui_lock144);return d;}lock_leave142(&ui_lock144);last8(6);return 0;}
static uint32_t color_native144(uint32_t color){return((color&255)<<16)|(color&0xff00)|((color>>16)&255);}
static int draw_call144(native_dc144*d,wui_draw144*draw){if(d->window==DESKTOP_HANDLE148){last8(5);return 0;}if(d->window_surface){last8(50);return 0;}draw->clip=(wui_rect144){d->clip.left,d->clip.top,d->clip.right-d->clip.left,d->clip.bottom-d->clip.top};int64_t status=ui_call144(d->menu_surface?WUI_MENUDRAW145:WUI_DRAW144,d->window,draw,0);if(status<0){last8((unsigned)-status);return 0;}return 1;}
static HANDLE MS f_GetDC(HANDLE h){if(!h)h=DESKTOP_HANDLE148;lock_enter142(&ui_lock144);if(h!=DESKTOP_HANDLE148){ui_window_runtime144*w=ui_window_lookup144(h);if(!w||w->thread!=tid142()){lock_leave142(&ui_lock144);last8(w?50:1400);return 0;}}win_rect144 rect;if(!f_GetClientRect(h,&rect)){lock_leave142(&ui_lock144);return 0;}if(dc_count144==64){lock_leave142(&ui_lock144);last8(1816);return 0;}native_dc144*d=calloc8(1,sizeof(*d));if(!d){lock_leave142(&ui_lock144);last8(8);return 0;}d->handle=UINT64_C(0x4443000000000000)|++dc_serial144;d->window=h;d->thread=tid142();d->foreground=0;d->background=0xffffff;d->background_mode=2;d->font=UINT64_C(0x464f00000000000d);d->clip=rect;d->next=dcs144;dcs144=d;++dc_count144;HANDLE result=d->handle;lock_leave142(&ui_lock144);return result;}
static int MS f_ReleaseDC(HANDLE h,HANDLE handle){(void)h;lock_enter142(&ui_lock144);native_dc144*d=dc_lookup144(handle);if(!d){lock_leave142(&ui_lock144);last8(6);return 0;}native_dc144**link=&dcs144;while(*link!=d)link=&(*link)->next;*link=d->next;
#ifdef ENGINE_M14
 font_select148(d->font,0);
#endif
 free8(d);--dc_count144;lock_leave142(&ui_lock144);return 1;}
#ifdef ENGINE_M14
/* A true full-window metadata DC. Non-client pixel submission is not enabled. */
static HANDLE MS f_GetWindowDC(HANDLE h){HANDLE dc=f_GetDC(h);if(!dc)return 0;win_rect144 r;if(!f_GetWindowRect(h?h:DESKTOP_HANDLE148,&r)){f_ReleaseDC(h,dc);return 0;}native_dc144*d=dc_lookup144(dc);d->window_surface=1;d->clip=(win_rect144){0,0,r.right-r.left,r.bottom-r.top};return dc;}
#endif
static int MS f_GetDeviceCaps(HANDLE dc,int index){if(!dc_lookup144(dc))return 0;wui_metrics144 metrics;if(!window_metrics144(&metrics))return 0;switch(index){case 2:case 14:case 36:return 1;case 8:return(int)metrics.width;case 10:return(int)metrics.height;case 12:return 32;case 24:return -1;case 88:case 90:return 96;default:last8(50);return 0;}}
static int MS f_InvalidateRect(HANDLE h,const win_rect144*in,int erase){ui_window_runtime144*w=ui_window_lookup144(h);if(!w||w->thread!=tid142()){last8(w?50:1400);return 0;}win_rect144 client;if(!f_GetClientRect(h,&client))return 0;win_rect144 r=in?*in:client;if(r.left<0)r.left=0;if(r.top<0)r.top=0;if(r.right>client.right)r.right=client.right;if(r.bottom>client.bottom)r.bottom=client.bottom;if(r.left>=r.right||r.top>=r.bottom)return 1;if(w->invalid){if(r.left>w->damage.x)r.left=w->damage.x;if(r.top>w->damage.y)r.top=w->damage.y;if(r.right<w->damage.x+w->damage.width)r.right=w->damage.x+w->damage.width;if(r.bottom<w->damage.y+w->damage.height)r.bottom=w->damage.y+w->damage.height;}w->damage=(wui_rect144){r.left,r.top,r.right-r.left,r.bottom-r.top};w->invalid=1;w->erase|=erase!=0;return 1;}
static int MS f_ValidateRect(HANDLE h,const win_rect144*r){ui_window_runtime144*w=ui_window_lookup144(h);if(!w||w->thread!=tid142()){last8(w?50:1400);return 0;}if(r&&w->invalid&&(r->left>w->damage.x||r->top>w->damage.y||r->right<w->damage.x+w->damage.width||r->bottom<w->damage.y+w->damage.height)){last8(50);return 0;}w->invalid=w->erase=0;return 1;}
static int MS f_GetUpdateRect(HANDLE h,win_rect144*out,int erase){(void)erase;ui_window_runtime144*w=ui_window_lookup144(h);if(!w){last8(1400);return 0;}if(out)*out=w->invalid?(win_rect144){w->damage.x,w->damage.y,w->damage.x+w->damage.width,w->damage.y+w->damage.height}:(win_rect144){0,0,0,0};return w->invalid!=0;}
static int paint_peek144(ui_msg144*out,HANDLE window,unsigned first,unsigned last,unsigned remove){(void)remove;if(window==UINT64_MAX||((first||last)&&(0xf<first||0xf>last)))return 0;for(ui_window_runtime144*w=ui_runtime_windows144;w;w=w->next){if(!w->invalid||w->thread!=tid142()||!w->description.visible)continue;HANDLE parent=w->handle;unsigned depth=0;while(window&&parent!=window&&parent&&depth++<WUI_WINDOWS144){ui_window_runtime144*p=ui_window_lookup144(parent);parent=p?p->description.parent:0;}if(window&&parent!=window)continue;*out=(ui_msg144){.window=w->handle,.message=0xf};return 1;}return 0;}
static int MS f_UpdateWindow(HANDLE h){ui_window_runtime144*w=ui_window_lookup144(h);if(!w){last8(1400);return 0;}if(w->invalid)f_SendMessageW(h,0xf,0,0);return 1;}
typedef struct {HANDLE dc;int erase;win_rect144 rect;int restore,increment;uint8_t reserved[32];unsigned pad;} native_paint144;
_Static_assert(sizeof(native_paint144)==72,"Win64 PAINTSTRUCT layout");
static HANDLE MS f_BeginPaint(HANDLE h,native_paint144*out){if(!out){last8(87);return 0;}ui_window_runtime144*w=ui_window_lookup144(h);if(!w){last8(1400);return 0;}HANDLE dc=f_GetDC(h);if(!dc)return 0;memset(out,0,sizeof(*out));out->dc=dc;out->erase=(int)w->erase;f_GetClientRect(h,&out->rect);native_dc144*d=dc_lookup144(dc);wui_draw144 clear={.kind=3};if(!draw_call144(d,&clear)){f_ReleaseDC(h,dc);return 0;}f_ValidateRect(h,0);return dc;}
static int MS f_EndPaint(HANDLE h,const native_paint144*paint){if(!paint){last8(87);return 0;}return f_ReleaseDC(h,paint->dc);}
static uint32_t MS f_SetTextColor(HANDLE dc,uint32_t color){native_dc144*d=dc_lookup144(dc);if(!d)return UINT32_MAX;uint32_t old=d->foreground;d->foreground=color&0xffffff;return old;}
static uint32_t MS f_SetBkColor(HANDLE dc,uint32_t color){native_dc144*d=dc_lookup144(dc);if(!d)return UINT32_MAX;uint32_t old=d->background;d->background=color&0xffffff;return old;}
static int MS f_SetBkMode(HANDLE dc,int mode){native_dc144*d=dc_lookup144(dc);if(!d||mode<1||mode>2){last8(87);return 0;}int old=d->background_mode;d->background_mode=mode;return old;}
static unsigned MS f_GetSysColor(int index){switch(index){case 5:case 14:return 0xffffff;case 8:case 18:return 0;case 15:return 0xf0f0f0;case 13:return 0xc77800;case 16:return 0xa0a0a0;default:last8(50);return 0;}}
static HANDLE MS f_GetSysColorBrush(int index){if(index<0||index>30){last8(87);return 0;}return(HANDLE)(unsigned)index+1;}
static int MS f_FillRect(HANDLE dc,const win_rect144*r,HANDLE brush){native_dc144*d=dc_lookup144(dc);if(!d||!r||brush<1||brush>31){last8(50);return 0;}if(r->left>=r->right||r->top>=r->bottom)return 1;int64_t width=(int64_t)r->right-r->left,height=(int64_t)r->bottom-r->top;if(width>16384||height>16384){last8(87);return 0;}wui_draw144 draw={.kind=1,.color=color_native144(f_GetSysColor((int)brush-1)),.bounds={r->left,r->top,(int)width,(int)height}};return draw_call144(d,&draw);}
static int text_command144(const WCHAR*text,int count,wui_draw144*draw){if(count<0||count>159||(!text&&count)){last8(87);return 0;}WCHAR copy[160];if(count)memcpy(copy,text,(unsigned)count*2);copy[count]=0;if(utf16_to8(copy,draw->text,sizeof(draw->text))<0){last8(1113);return 0;}return 1;}
static int MS f_GetTextExtentPoint32W(HANDLE dc,const WCHAR*text,int count,void*out){native_dc144*d=dc_lookup144(dc);if(!d||!out){last8(87);return 0;}wui_draw144 draw={0};
#ifdef ENGINE_M14
 ui_font_metrics148 m;if(!font_info148(d->font,&m,0))return 0;draw.bounds.height=(int)m.em;
#endif
if(!text_command144(text,count,&draw))return 0;int64_t result=ui_call144(WUI_MEASURE144,0,&draw,0);if(result<0){last8((unsigned)-result);return 0;}((int*)out)[0]=(int)(uint32_t)result;((int*)out)[1]=(int)((uint64_t)result>>32);return 1;}
static int MS f_TextOutW(HANDLE dc,int x,int y,const WCHAR*text,int count){native_dc144*d=dc_lookup144(dc);if(!d)return 0;wui_draw144 draw={.kind=2,.color=color_native144(d->foreground),.bounds={x,y,0,16}};
#ifdef ENGINE_M14
 ui_font_metrics148 m;logfont148 lf;if(!font_info148(d->font,&m,&lf))return 0;draw.bounds.height=(int)m.em;
#endif
 if(!text_command144(text,count,&draw))return 0;if(d->background_mode==2){int size[2];if(!f_GetTextExtentPoint32W(dc,text,count,size))return 0;wui_draw144 background={.kind=1,.color=color_native144(d->background),.bounds={x,y,size[0],size[1]}};if(!draw_call144(d,&background))return 0;}if(!draw_call144(d,&draw))return 0;
#ifdef ENGINE_M14
 if(lf.underline||lf.strike){int size[2];if(!f_GetTextExtentPoint32W(dc,text,count,size))return 0;wui_draw144 line={.kind=1,.color=draw.color,.bounds={x,y, size[0],1}};if(lf.underline){line.bounds.y=y+(int)m.ascent+1;if(!draw_call144(d,&line))return 0;}if(lf.strike){line.bounds.y=y+(int)m.ascent/2;if(!draw_call144(d,&line))return 0;}}
#endif
 return 1;}
static int64_t paint_default144(HANDLE h){native_paint144 paint;HANDLE dc=f_BeginPaint(h,&paint);if(!dc)return 0;ui_window_runtime144*w=ui_window_lookup144(h);if(w&&w->class_->definition.background)f_FillRect(dc,&paint.rect,w->class_->definition.background);f_EndPaint(h,&paint);return 0;}

static void paint_changed144(HANDLE h,unsigned message){if(message==5){ui_window_runtime144*w=ui_window_lookup144(h);if(w&&!w->description.parent&&w->menu)menu_paint145(h);}if(message==5||message==0xc||message==0x30||message==0x18||message==0x444||message==0x401||message==0x104d||message==0x104c||message==0x1074||message==0x1008||message==0x1009||message==0x102b||message==0x1061||message==0x41f||message==0x404||message==0x40b)f_InvalidateRect(h,0,1);}
static void paint_release144(HANDLE h){lock_enter142(&ui_lock144);native_dc144**link=&dcs144;while(*link){native_dc144*d=*link;if(d->window==h){*link=d->next;
#ifdef ENGINE_M14
 font_select148(d->font,0);
#endif
 free8(d);--dc_count144;}else link=&d->next;}lock_leave142(&ui_lock144);}

static uint64_t MS f_SetTimer(HANDLE window,uint64_t id,unsigned interval,void*callback){if(id>INT64_MAX){last8(87);return 0;}wui_timer144 timer={id,(uint64_t)(uintptr_t)callback,interval?interval:10,0};int64_t result=ui_call144(WUI_TIMER144,window,&timer,0);if(result<0){last8((unsigned)-result);return 0;}return(uint64_t)result;}
static int MS f_KillTimer(HANDLE window,uint64_t id){wui_timer144 timer={.id=id};int64_t result=ui_call144(WUI_TIMER144,window,&timer,0);if(result<0){last8((unsigned)-result);return 0;}return(int)result;}
