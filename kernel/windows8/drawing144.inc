/* Copied retained primitives, bounded independently from guest address spaces. */
static unsigned ui_draw_text144(const char*text){unsigned n=0,at=0;while(n<512&&text[n])++n;if(n==512)return 0;while(at<n){uint32_t cp;if(!decode_utf8_143(text,n,&at,&cp))return 0;}return 1;}
static int64_t ui_draw_store144(ui_window144*w,const wui_draw144*draw,unsigned menu){
 unsigned*count=menu?&w->menu_count:&w->draw_count,*capacity=menu?&w->menu_capacity:&w->draw_capacity;ui_draw_page144**head=menu?&w->menu_draws:&w->draws;
 if(*count==(menu?64u:224u))return -1816;
 if(*count==*capacity){if(ui_draw_pages144==128)return -1816;ui_draw_page144*page=ui_page144();if(!page)return -8;ui_draw_page144**link=head;while(*link)link=&(*link)->next;*link=page;*capacity+=7;++ui_draw_pages144;}
 ui_draw_page144*page=*head;unsigned index=*count;while(index>=7){page=page->next;index-=7;}page->items[index]=*draw;++*count;w->view.revision=++ui_revision144;return 0;
}
static int64_t ui_draw_call144(uint64_t op,uint64_t handle,uint64_t pointer,uint64_t argument){
 if(argument)return -87;wui_draw144 draw;if(user8(pointer,&draw,sizeof(draw),0))return -998;
 if(op==WUI_MEASURE144){if(handle||!ui_draw_text144(draw.text))return -87;
#ifdef ENGINE_M73
#ifdef ENGINE_M14
 unsigned role=ui148_font_role((unsigned)draw.bounds.height);if(!role)return -87;
 return (int64_t)((uint64_t)ui148_font_height((unsigned)draw.bounds.height)<<32)|ui73_measure(draw.text,role);
#else
 return (int64_t)((uint64_t)16<<32)|ui73_measure(draw.text,1);
#endif
#else
 return -50;
#endif
 }
 ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;
 unsigned menu=op==WUI_MENUDRAW145;if(menu&&(!w->view.menu_height||w->view.description.parent))return -87;
 unsigned*count=menu?&w->menu_count:&w->draw_count;
 if(draw.kind==3){
#ifdef ENGINE_M14
 if(!menu)ui_images_release148(w);
#endif
 *count=0;w->view.revision=++ui_revision144;return 0;}
 if(draw.kind!=1&&draw.kind!=2&&draw.kind!=4)return -50;
#ifdef ENGINE_M14
 if(draw.kind==2&&!ui148_font_role((unsigned)draw.bounds.height))return -87;
#endif
 if(draw.kind==4&&(draw.bounds.width<1||draw.bounds.width>16||draw.bounds.height<1||draw.bounds.height>8))return -87;
 if(draw.color&0xff000000u||draw.bounds.width<0||draw.bounds.height<0||draw.bounds.width>16384||draw.bounds.height>16384||draw.clip.width<0||draw.clip.height<0||draw.clip.width>16384||draw.clip.height>16384||draw.bounds.x< -32768||draw.bounds.x>32767||draw.bounds.y< -32768||draw.bounds.y>32767||draw.clip.x< -32768||draw.clip.x>32767||draw.clip.y< -32768||draw.clip.y>32767||(draw.kind!=4&&!ui_draw_text144(draw.text)))return -87;
 return ui_draw_store144(w,&draw,menu);
}
unsigned w8_ui_draw_at144(uint64_t handle,unsigned index,wui_draw144*out){ui_window144*w=ui_lookup144(handle);if(!w||!out||index>=w->draw_count)return 0;ui_draw_page144*page=w->draws;while(index>=7){page=page->next;index-=7;}*out=page->items[index];return 1;}
unsigned w8_ui_menudraw_at145(uint64_t handle,unsigned index,wui_draw144*out){ui_window144*w=ui_lookup144(handle);if(!w||!out||index>=w->menu_count)return 0;ui_draw_page144*page=w->menu_draws;while(index>=7){page=page->next;index-=7;}*out=page->items[index];return 1;}
unsigned w8_ui_menuheight145(uint64_t handle){ui_window144*w=ui_lookup144(handle);return w?w->view.menu_height:0;}
