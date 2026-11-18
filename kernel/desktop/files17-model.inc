static file_filter17 *files_filter17_for(unsigned slot){
 if(slot>=DESKTOP_WINDOWS||!model.windows[slot].live||model.windows[slot].app!=FILES)return 0;
 file_filter17*f=&file_filters17[slot];uint64_t token=desktop_token(&model,slot);
 if(f->owner!=token){memset(f,0,sizeof(*f));f->owner=token;file_lists11[slot].generation=0;}
 return f;
}
static unsigned files_filter17_matches(unsigned slot,const v6_entry*e){
 file_filter17*f=files_filter17_for(slot);if(!f||!f->query[0]||apps[slot].usb_mode10)return 1;
 const char*name=file_label11(e);unsigned wanted=length(f->query);
 for(unsigned at=0;name[at]&&at<256;++at){unsigned i=0;while(i<wanted&&name[at+i]&&lower11((uint8_t)name[at+i])==lower11((uint8_t)f->query[i]))++i;if(i==wanted)return 1;}
 return 0;
}
static void files_filter17_clear(application*a){
 unsigned slot=(unsigned)(a-apps);file_filter17*f=files_filter17_for(slot);if(!f)return;
 f->query[0]=0;f->cursor=f->anchor=f->active=0;file_lists11[slot].generation=0;
}
static void files_filter17_changed(desktop_window*w,application*a,file_filter17*f){
 unsigned slot=(unsigned)(a-apps);(void)f;file_lists11[slot].generation=0;a->offset=0;
 memset(selected11[slot],0,sizeof(selected11[slot]));selection_anchor11[slot]=selection_focus11[slot]=0;
 interaction11.last_valid=0;invalidate(w->bounds);
}
