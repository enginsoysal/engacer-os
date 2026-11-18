static unsigned files_filter17_key(desktop_window*w,application*a,uint64_t token,int key){
 if(!a||file_block_owner11(token))return 0;
 file_filter17*f=files_filter17_for((unsigned)(a-apps));
 if(key==6){files_filter17_action(token,F17_FILTER);return 1;}
 if(!f->active||!control_active||focused_control_window!=token||focused_action!=F17_FILTER)return 0;
 if(a->usb_mode10){f->active=0;return 0;}
 if(key==9||key==136){f->active=0;return 0;}
 if(key==27){if(f->query[0]){f->query[0]=0;f->cursor=f->anchor=0;files_filter17_changed(w,a,f);}else{f->active=0;control_active=0;invalidate(w->bounds);}return 1;}
 if(key==10){f->active=0;control_active=0;if(children72(a))select_row11(a,0,0,0);invalidate(w->bounds);return 1;}
 char previous[64];copy(previous,f->query,sizeof(previous));
 if(file_text_capacity11(f->query,sizeof(f->query),&f->cursor,&f->anchor,key)){
  if(!equal(previous,f->query))files_filter17_changed(w,a,f);else invalidate(w->bounds);return 1;
 }
 return 0;
}
