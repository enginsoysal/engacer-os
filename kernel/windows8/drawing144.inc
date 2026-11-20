/* Copied retained primitives, bounded independently from guest address spaces. */
static unsigned ui_draw_text144(const char*text){unsigned n=0,at=0;while(n<512&&text[n])++n;if(n==512)return 0;while(at<n){uint32_t cp;if(!decode_utf8_143(text,n,&at,&cp))return 0;}return 1;}
static int64_t ui_draw_call144(uint64_t op,uint64_t handle,uint64_t pointer,uint64_t argument){
 if(argument)return -87;wui_draw144 draw;if(user8(pointer,&draw,sizeof(draw),0))return -998;
 if(op==WUI_MEASURE144){if(handle||!ui_draw_text144(draw.text))return -87;
#ifdef ENGINE_M73
 return (int64_t)((uint64_t)16<<32)|ui73_measure(draw.text,1);
#else
 return -50;
#endif
 }
 ui_window144*w=ui_owned144(handle);if(!w)return -1400;if(w->thread!=current142)return -5;
 if(draw.kind==3){w->draw_count=0;w->view.revision=++ui_revision144;return 0;}
 if(draw.kind!=1&&draw.kind!=2&&draw.kind!=4)return -50;
 if(draw.kind==4&&(draw.bounds.width<1||draw.bounds.width>16||draw.bounds.height<1||draw.bounds.height>8))return -87;
 if(draw.color&0xff000000u||draw.bounds.width<0||draw.bounds.height<0||draw.bounds.width>16384||draw.bounds.height>16384||draw.clip.width<0||draw.clip.height<0||draw.clip.width>16384||draw.clip.height>16384||draw.bounds.x< -32768||draw.bounds.x>32767||draw.bounds.y< -32768||draw.bounds.y>32767||draw.clip.x< -32768||draw.clip.x>32767||draw.clip.y< -32768||draw.clip.y>32767||(draw.kind!=4&&!ui_draw_text144(draw.text)))return -87;
 if(w->draw_count==224)return -1816;
 if(w->draw_count==w->draw_capacity){if(ui_draw_pages144==128)return -1816;ui_draw_page144*page=ui_page144();if(!page)return -8;ui_draw_page144**link=&w->draws;while(*link)link=&(*link)->next;*link=page;w->draw_capacity+=7;++ui_draw_pages144;}
 ui_draw_page144*page=w->draws;unsigned index=w->draw_count;while(index>=7){page=page->next;index-=7;}page->items[index]=draw;++w->draw_count;w->view.revision=++ui_revision144;return 0;
}
unsigned w8_ui_draw_at144(uint64_t handle,unsigned index,wui_draw144*out){ui_window144*w=ui_lookup144(handle);if(!w||!out||index>=w->draw_count)return 0;ui_draw_page144*page=w->draws;while(index>=7){page=page->next;index-=7;}*out=page->items[index];return 1;}
