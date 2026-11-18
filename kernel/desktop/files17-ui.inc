static unsigned files_sidebar_width17(const desktop_window*w){return file_sidebar11(w)?192u:0u;}
static void files_filter17_draw(desktop_window*w,application*a,uint64_t token,desktop_rect r){
 (void)w;file_filter17*f=files_filter17_for((unsigned)(a-apps));ui12_palette p=desktop_palette16();
 unsigned enabled=!a->usb_mode10&&files_native_ready12(a)&&!file_block_owner11(token);
 if(!enabled){component_button12(token,r,"",F17_FILTER,0,0);ui73_fit(r.x+10,r.y+8,r.width-20,a->usb_mode10?"System folders only":"Filter unavailable",UI12_SECONDARY,p.muted);return;}
 unsigned focus=f->active&&control_active&&focused_control_window==token&&focused_action==F17_FILTER;
 int clear=f->query[0]?36:0;desktop_rect input={r.x,r.y,r.width-clear,r.height};
 file_text_field11(input,f->query,f->cursor,f->anchor,focus,0);file_control11(token,input,F17_FILTER);access_capture16(token,F17_FILTER,"Filter names in this folder (Ctrl+F)",2);
 if(!f->query[0])ui73_fit(input.x+10,input.y+8,input.width-20,"Filter names",UI12_BODY,p.muted);
 if(clear){button(token,r.x+r.width-32,r.y,32,"x",F17_CLEAR,0);access_capture16(token,F17_CLEAR,"Clear filename filter",1);}
}
static unsigned files_filter17_action(uint64_t token,unsigned command){
 if(command!=F17_FILTER&&command!=F17_CLEAR)return 0;
 desktop_window*w=desktop_lookup(&model,token);if(!w||w->app!=FILES||file_block_owner11(token))return 1;
 application*a=&apps[w-model.windows];file_filter17*f=files_filter17_for((unsigned)(a-apps));
 if(a->usb_mode10||!files_native_ready12(a)){notice(a,"Filename filtering is available in system folders. USB navigation and transfers remain available.");invalidate(w->bounds);return 1;}
 if(command==F17_CLEAR){f->query[0]=0;f->cursor=f->anchor=0;files_filter17_changed(w,a,f);}
 else{f->cursor=length(f->query);f->anchor=0;}
 f->active=1;file_windows11[a-apps].address_active=0;control_active=1;focused_control_window=token;focused_action=F17_FILTER;invalidate(w->bounds);return 1;
}
