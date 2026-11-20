/* Bounded child overlay with original menu callbacks and blocking message wait. */
typedef struct {HANDLE owner,window,menu,previous_focus;unsigned position,depth,finished,command,opening_release,rows,top,entered,initialized;int selected;struct {HANDLE menu;unsigned position,top;int selected;} history[16];} menu_track145;
static unsigned menu_tracking145;
static int menu_entry145(HANDLE menu,unsigned index,menu_info144*out){memset(out,0,sizeof(*out));out->size=sizeof(*out);out->mask=0x107;return f_GetMenuItemInfoW(menu,index,1,out);}
static void menu_layout145(menu_track145*t){win_rect144 client;int count=f_GetMenuItemCount(t->menu);if(count<=0||!f_GetClientRect(t->owner,&client)||client.bottom<32){t->finished=1;return;}unsigned rows=(unsigned)(client.bottom-4)/24;if(rows>28)rows=28;if(rows>(unsigned)count)rows=(unsigned)count;t->rows=rows;ui_window_runtime144*w=ui_window_lookup144(t->window);if(w)f_MoveWindow(t->window,w->description.bounds.x,0,w->description.bounds.width,(int)rows*24+4,1);}
static void menu_popup_paint145(menu_track145*t){native_paint144 paint;HANDLE dc=f_BeginPaint(t->window,&paint);if(!dc)return;f_FillRect(dc,&paint.rect,16);f_SetBkMode(dc,1);
 lock_enter142(&menu_lock144);menu144*m=menu_lookup144(t->menu);unsigned at=0;for(menu_item144*i=m?m->items:0;i;i=i->next,++at){if(at<t->top)continue;if(at>=t->top+t->rows)break;int y=2+(int)(at-t->top)*24;
  if(i->type&0x800){win_rect144 line={6,y+11,paint.rect.right-6,y+12};f_FillRect(dc,&line,17);continue;}
  if(t->selected==(int)at){win_rect144 selected={1,y,paint.rect.right-1,y+24};f_FillRect(dc,&selected,14);}
  f_SetTextColor(dc,i->state&3?0x808080:t->selected==(int)at?0xffffff:0);WCHAR label[160];unsigned n=menu_label145(i->text,label);native_dc144*d=dc_lookup144(dc);win_rect144 old=d->clip;d->clip.right=paint.rect.right-22;f_TextOutW(dc,24,y+4,label,(int)n);d->clip=old;
  if(i->state&8)f_TextOutW(dc,6,y+4,u"*",1);if(i->submenu)f_TextOutW(dc,paint.rect.right-16,y+4,u">",1);
 }lock_leave142(&menu_lock144);f_EndPaint(t->window,&paint);
}
static void menu_choose145(menu_track145*t){if(t->selected<0)return;menu_info144 item;if(!menu_entry145(t->menu,(unsigned)t->selected,&item)||item.state&3||item.type&0x800)return;
 if(item.submenu){if(t->depth==16){last8(1816);t->finished=1;return;}t->history[t->depth].menu=t->menu;t->history[t->depth].position=t->position;t->history[t->depth].selected=t->selected;t->history[t->depth++].top=t->top;t->menu=item.submenu;t->position=(unsigned)t->selected;t->selected=-1;t->top=0;f_SendMessageW(t->owner,0x117,t->menu,t->position);if(!f_IsWindow(t->owner)||!f_IsWindow(t->window)||!f_IsMenu(t->menu)){t->finished=1;return;}menu_layout145(t);f_InvalidateRect(t->window,0,1);
 }else{t->command=item.id;t->finished=1;}
}
static int64_t MS menu_popup_proc145(HANDLE h,unsigned message,uint64_t wp,int64_t lp){
 if(message==0x81)return 1;menu_track145*t=(void*)(uintptr_t)f_GetWindowLongPtrW(h,-21);if(!t)return f_DefWindowProcW(h,message,wp,lp);
 if(message==0x82||message==0x10||message==0x215){t->finished=1;return 0;}
 if(message==0xf){menu_popup_paint145(t);return 0;}
 if(message==0x200||message==0x201||message==0x202){win_rect144 rect;f_GetClientRect(h,&rect);int x=(int16_t)(lp&65535),y=(int16_t)((uint64_t)lp>>16);int inside=x>=0&&x<rect.right&&y>=2&&y<rect.bottom-2;
  int row=inside?(int)t->top+(y-2)/24:-1;int count=f_GetMenuItemCount(t->menu);if(row>=count)row=-1;if(row!=t->selected){t->selected=row;f_InvalidateRect(h,0,0);}
  if(message==0x201&&!inside)t->finished=1;
  if(message==0x202){if(inside)menu_choose145(t);else if(!t->opening_release)t->finished=1;t->opening_release=0;}return 0;
 }
 if(message==0x100){int count=f_GetMenuItemCount(t->menu);if(count<0){t->finished=1;return 0;}
  if(wp==27){t->finished=1;return 0;}if(wp==13||wp==0x27){menu_choose145(t);return 0;}
  if(wp==0x25&&t->depth){f_SendMessageW(t->owner,0x125,t->menu,0);--t->depth;t->menu=t->history[t->depth].menu;t->position=t->history[t->depth].position;t->selected=t->history[t->depth].selected;t->top=t->history[t->depth].top;menu_layout145(t);f_InvalidateRect(h,0,1);return 0;}
  if(wp==0x26||wp==0x28||wp==0x24||wp==0x23){int direction=wp==0x26||wp==0x23?-1:1,row=wp==0x24?-1:wp==0x23?count:t->selected;
   for(int n=0;n<count;++n){row=(row+direction+count)%count;menu_info144 item;if(menu_entry145(t->menu,(unsigned)row,&item)&&!(item.state&3)&&!(item.type&0x800)){t->selected=row;break;}}
   if(t->selected>=0){if((unsigned)t->selected<t->top)t->top=(unsigned)t->selected;else if((unsigned)t->selected>=t->top+t->rows)t->top=(unsigned)t->selected-t->rows+1;}f_InvalidateRect(h,0,0);return 0;
  }
 }return f_DefWindowProcW(h,message,wp,lp);
}
static unsigned menu_open145(HANDLE owner,HANDLE menu,unsigned position,int left){
 lock_enter142(&ui_lock144);if(menu_tracking145>=8){lock_leave142(&ui_lock144);last8(1816);return 0;}++menu_tracking145;
 ui_class144*cls=ui_class_lookup144(u"Engacer.Menu145");if(cls&&cls->definition.proc!=menu_popup_proc145){--menu_tracking145;lock_leave142(&ui_lock144);last8(1410);return 0;}
 if(!cls){ui_class_definition144 definition={0};definition.name=u"Engacer.Menu145";definition.proc=menu_popup_proc145;definition.background=16;if(!f_RegisterClassW(&definition)){--menu_tracking145;lock_leave142(&ui_lock144);return 0;}}lock_leave142(&ui_lock144);
 menu_track145 t={.owner=owner,.menu=menu,.position=position,.selected=-1,.opening_release=1,.previous_focus=f_GetFocus()};
 f_SendMessageW(owner,0x211,0,0);t.entered=1;if(!f_IsWindow(owner))goto done;f_SendMessageW(owner,0x117,menu,position);t.initialized=1;if(!f_IsWindow(owner)||!f_IsMenu(menu))goto done;
 win_rect144 client;if(!f_GetClientRect(owner,&client)||client.right<48||client.bottom<32)goto done;unsigned rows=(unsigned)(client.bottom-4)/24;if(rows>28)rows=28;t.rows=rows;
 int width=client.right<300?client.right:300;if(left+width>client.right)left=client.right-width;if(left<0)left=0;
 int count=f_GetMenuItemCount(menu);if(count<=0)goto done;if(rows>(unsigned)count)rows=(unsigned)count;
 t.window=f_CreateWindowExW(8,u"Engacer.Menu145",u"",0x40800000,left,0,width,(int)rows*24+4,owner,0,0,0);if(!t.window)goto done;
 f_SetWindowLongPtrW(t.window,-21,(int64_t)(uintptr_t)&t);f_ShowWindow(t.window,5);f_SetFocus(t.window);f_SetCapture(t.window);
 while(!t.finished&&f_IsWindow(t.window)&&f_IsWindow(owner)){ui_msg144 message;int got=f_GetMessageW(&message,0,0,0);if(got<=0){if(!got)f_PostQuitMessage((int)message.wp);break;}f_TranslateMessage(&message);f_DispatchMessageW(&message);}
done:
 if(t.window){if(f_GetCapture()==t.window)f_ReleaseCapture();if(f_IsWindow(t.window))f_DestroyWindow(t.window);if(f_IsWindow(t.previous_focus))f_SetFocus(t.previous_focus);}
 if(f_IsWindow(owner)){if(t.initialized){f_SendMessageW(owner,0x125,t.menu,0);while(t.depth){--t.depth;f_SendMessageW(owner,0x125,t.history[t.depth].menu,0);}}if(t.entered)f_SendMessageW(owner,0x212,0,0);}
 lock_enter142(&ui_lock144);--menu_tracking145;lock_leave142(&ui_lock144);return t.command;
}
