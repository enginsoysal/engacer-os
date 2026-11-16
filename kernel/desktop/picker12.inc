/* Shared native Open/Save/folder picker. All writes follow explicit acceptance. */
static unsigned picker_live12(void){return file_dialog_state11.mode==P12_DIALOG;}
static unsigned picker_owner12(uint64_t token){return picker_live12()&&file_dialog_state11.owner==token&&desktop_lookup(&model,token);}
static unsigned picker_control12(uint64_t token,unsigned command){return picker_owner12(token)&&file_dialog_owner_focused11()&&((command>=P12_CANCEL&&command<=P12_DISCARD_OPEN)||(command>=P12_ROW&&command<P12_ROW+V6_ENTRIES));}
static unsigned picker_folder12(const char*path){const v6_entry*e=entry(path);return equal(path,"/")||(e&&e->kind==2);}
static unsigned picker_busy12(void){download7_info d=download7_current();return files_busy12()||(d.state>=DOWNLOAD7_RESOLVING&&d.state<=DOWNLOAD7_RECEIVING)||w8_pending();}
static unsigned picker_writable12(const char*path){return picker_folder12(path)&&writable72(path)&&!file_in_bin11(path)&&!m6_volume()->readonly;}
static unsigned picker_string12(const char*s){for(unsigned i=0;i<256;++i)if(!s[i])return i&&s[0]=='/';return 0;}
static void picker_pref_path12(char*out){root_path(out,"AppData/file-dialogs12.bin");}
static void picker_load12(void){
 if(picker_preferences_loaded12)return;picker_preferences_loaded12=1;memset(&picker_preferences,0,sizeof(picker_preferences));
 char path[256];picker_pref_path12(path);unsigned bytes=0;picker_preferences12 record;
 if(v6_verify(m6_volume(),path)||v6_read(m6_volume(),path,0,&record,sizeof(record),&bytes)||bytes!=sizeof(record)||record.magic!=UINT64_C(0x31524b4350494c46)||record.version!=1||record.reserved||record.padding||record.crc!=m4_crc(&record,784))return;
 for(unsigned i=0;i<3;++i)if(record.paths[i][0]&&!picker_string12(record.paths[i]))return;
 picker_preferences=record;
}
static unsigned picker_category12(void){return picker12.purpose==P12_TEXT_SAVE?1:picker12.purpose==P12_ZIP_FOLDER?2:0;}
static unsigned picker_remember12(void){
 unsigned category=picker_category12();copy(picker_preferences.paths[category],picker12.path,256);
 picker_preferences.magic=UINT64_C(0x31524b4350494c46);picker_preferences.version=1;picker_preferences.reserved=picker_preferences.padding=0;
 picker_preferences.crc=m4_crc(&picker_preferences,784);char path[256];picker_pref_path12(path);
 return m6_volume()->readonly?V6_RO:v6_put(m6_volume(),path,sizeof(picker_preferences),memory_source,&picker_preferences);
}
static void picker_error12(const char*message){copy(picker12.error,message,sizeof(picker12.error));whole();}
static void picker_visit12(const char*path,unsigned push){
 if(!picker_folder12(path)){picker_error12("That folder is no longer available. Choose another location.");return;}
 if(push&&(!picker12.history_count||!equal(path,picker12.path))){
  unsigned n=picker12.history_count?picker12.history_position+1:0;
  if(n==8){for(unsigned i=0;i<7;++i)memcpy(picker12.history[i],picker12.history[i+1],256);n=7;}
  copy(picker12.history[n],path,256);picker12.history_position=n;picker12.history_count=n+1;
 }
 copy(picker12.path,path,256);copy(picker12.address,path,256);picker12.address_cursor=picker12.address_anchor=length(path);
 picker12.selected=UINT32_MAX;picker12.offset=0;picker12.generation=0;picker12.error[0]=0;whole();
}
static void picker_begin12(uint64_t token,unsigned purpose){
 desktop_window*w=desktop_lookup(&model,token);if(!w)return;application*a=&apps[w-model.windows];
 if(file_dialog_state11.mode){notice(a,"Finish or cancel the current file dialog first.");whole();return;}
 if(a->stopped){notice(a,"This app is stopped. Its file dialog cannot start.");whole();return;}
 if(model.width<560||model.height<500){notice(a,"Choose a smaller display size in Settings to make room for the file dialog.");whole();return;}
 picker_load12();memset(&picker12,0,sizeof(picker12));picker12.purpose=purpose;picker12.selected=UINT32_MAX;
 char path[256];unsigned category=picker_category12();copy(path,picker_preferences.paths[category],256);
 if(!picker_string12(path)||!picker_folder12(path)||(purpose!=P12_TEXT_OPEN&&purpose!=P12_IMAGE_OPEN&&purpose!=P12_ZIP_OPEN&&!picker_writable12(path)))root_path(path,purpose==P12_ZIP_FOLDER||purpose==P12_ZIP_OPEN?"Downloads":purpose==P12_IMAGE_OPEN?"Pictures":"Documents");
 if(purpose==P12_TEXT_SAVE){copy(picker12.name,a->path[0]?file_basename11(a->path):"Note.txt",256);picker12.name_cursor=length(picker12.name);picker12.name_anchor=0;}
 file_dialog_open11(P12_DIALOG,token,0);file_dialog_state11.focus=purpose==P12_TEXT_SAVE?2:1;picker_visit12(path,1);
 serial_text("M128_PICKER_OPEN purpose=");serial_hex(purpose);serial_text("\n");
}
static unsigned picker_match12(const v6_entry*e){
 if(e->kind==2)return 1;if(e->kind!=1||picker12.purpose==P12_ZIP_FOLDER)return 0;
 if(picker12.filter)return 1;const char*extension=ui12_file_extension(file_basename11(e->path));
 if(picker12.purpose==P12_IMAGE_OPEN)return !ui12_file_natural(extension,"bmp");
 if(picker12.purpose==P12_ZIP_OPEN)return !ui12_file_natural(extension,"zip");
 return !ui12_file_natural(extension,"txt")||!ui12_file_natural(extension,"md")||!ui12_file_natural(extension,"log")||!ui12_file_natural(extension,"ini")||!ui12_file_natural(extension,"cfg")||!ui12_file_natural(extension,"json")||!ui12_file_natural(extension,"csv");
}
static void picker_list12(void){
 if(picker12.generation==m6_volume()->generation)return;picker12.count=0;
 for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*e=&m6_volume()->entries[i];if(!e->kind||!file_direct_child11(e->path,picker12.path)||!picker_match12(e))continue;
  unsigned n=picker12.count++;while(n){unsigned old=picker12.order[n-1];const v6_entry*b=&m6_volume()->entries[old];if(ui12_file_order(file_basename11(e->path),e->kind,e->size,i,file_basename11(b->path),b->kind,b->size,old,0,0)>=0)break;picker12.order[n]=picker12.order[n-1];--n;}picker12.order[n]=(uint16_t)i;
 }
 unsigned selected=0;for(unsigned i=0;i<picker12.count;++i)selected|=picker12.order[i]==picker12.selected;
 if(selected&&picker12.selected_path[0]){const v6_entry*e=&m6_volume()->entries[picker12.selected];if(!equal(e->path,picker12.selected_path)||e->kind!=picker12.selected_kind||e->first!=picker12.selected_first||e->size!=picker12.selected_size||e->crc!=picker12.selected_crc){selected=0;copy(picker12.error,"The selected item changed. Select it again before opening.",sizeof(picker12.error));}}
 if(!selected)picker12.selected=UINT32_MAX;if(picker12.offset>=picker12.count)picker12.offset=0;picker12.generation=m6_volume()->generation;
}
static void picker_select12(unsigned index){const v6_entry*e=&m6_volume()->entries[index];picker12.selected=index;copy(picker12.selected_path,e->path,256);picker12.selected_first=e->first;picker12.selected_size=e->size;picker12.selected_crc=e->crc;picker12.selected_kind=e->kind;}
static const v6_entry*picker_selected12(void){
 picker_list12();if(picker12.selected>=V6_ENTRIES)return 0;const v6_entry*e=&m6_volume()->entries[picker12.selected];
 return e->kind&&file_direct_child11(e->path,picker12.path)&&picker_match12(e)?e:0;
}
static void picker_close12(application*a,const char*message,unsigned remember){
 unsigned failed=remember?picker_remember12():0;file_dialog_state11.mode=0;picker12.phase=0;control_active=0;
 if(a)notice(a,failed?"Your choice completed; its location could not be remembered on disk.":message);i11_cancel(&interaction11);whole();
}
static unsigned picker_other_open12(uint64_t token,const char*path){
 for(unsigned i=0;i<DESKTOP_WINDOWS;++i)if(model.windows[i].live&&desktop_token(&model,i)!=token&&model.windows[i].app!=FILES&&apps[i].path[0]&&equal(apps[i].path,path))return 1;return 0;
}
static void picker_snapshot12(const v6_entry*e){picker12.target_first=e->first;picker12.target_size=e->size;picker12.target_crc=e->crc;}
static unsigned picker_unchanged12(const v6_entry*e){return e&&e->kind==1&&e->first==picker12.target_first&&e->size==picker12.target_size&&e->crc==picker12.target_crc;}
static void picker_editor_open12(desktop_window*w,application*a,const char*path,unsigned decision){
 unsigned slot=(unsigned)(w-model.windows),status=app7_document12(slot,path,&a->view,0);
 if(status){picker12.phase=0;picker_error12(status==V6_LIMIT?"Text Editor accepts at most 8191 bytes. Your current document is kept.":status==V6_INVALID?"This is not a supported ASCII text file. Your current document is kept.":"The selected file could not be verified. Your current document is kept.");return;}
 if(a->dirty&&!decision){copy(picker12.pending,path,256);picker_snapshot12(entry(path));picker12.phase=P12_DIRTY_REVIEW;file_dialog_state11.focus=5;whole();return;}
 if(decision==1){save_document(a);if(a->dirty||a->stopped){picker_error12("Your current document could not be saved. Keep it open and try again.");return;}
  status=app7_document12(slot,path,&a->view,0);if(status){picker_error12("Your document was saved, but the new file could not be opened. It is still kept.");return;}}
 /* app7_request validates the response before changing the display snapshot. */
 status=app7_document12(slot,path,&a->view,1);if(status){if(status==APP12_DOCUMENT_STOPPED)a->stopped=1;picker_error12("The new file was not accepted. The previous text is retained.");return;}
 copy(a->path,path,256);a->existed=1;a->source_crc=entry(path)->crc;a->closing=0;(void)send_app(a,APP7_KEY,130,0,0);
 picker_close12(a,"Opened the selected text file.",1);invalidate(w->bounds);serial_text("M128_TEXT_OPENED\n");
}
static void picker_save12(desktop_window*w,application*a,unsigned replace){
 char name[256],target[256];copy(name,picker12.name,256);
 if(!picker12.filter&&!ui12_file_extension(name)[0]&&length(name)+4<sizeof(name))append(name,".txt",256);
 if(!file_name_valid11(name)){picker_error12("Use a name of 1-63 supported characters, without a trailing dot or space.");return;}
 if(!picker_writable12(picker12.path)||picker_busy12()){picker_error12("Choose a writable folder and finish any file transfer first. Your text is kept.");return;}
 if(file_join11(target,picker12.path,name)){picker_error12("The folder and filename exceed the supported path length.");return;}
 const v6_entry*e=file_case_entry11(target);uint64_t token=desktop_token(&model,w-model.windows);
 if(e&&(e->kind!=1||!writable72(e->path)||file_in_bin11(e->path)||picker_other_open12(token,e->path))){picker_error12("That target is protected, a folder or open in another app. Choose a different name.");return;}
 if(e){copy(target,e->path,256);if(!replace){copy(picker12.pending,target,256);picker_snapshot12(e);picker12.phase=P12_REPLACE_REVIEW;file_dialog_state11.focus=5;whole();return;}
  if(!equal(target,picker12.pending)||!picker_unchanged12(e)){picker12.phase=0;picker_error12("The destination changed after review. Review it again; your text is kept.");return;}}
 else if(replace){picker12.phase=0;picker_error12("The reviewed destination is no longer available. Choose the target again.");return;}
 unsigned status=v6_put(m6_volume(),target,a->length,memory_source,a->text);
 if(status||v6_verify(m6_volume(),target)){picker_error12("Save failed. Your original document and unsaved text remain available.");return;}
 copy(a->path,target,256);a->existed=1;a->source_crc=entry(target)->crc;a->closing=0;(void)send_app(a,APP7_SAVED,0,0,0);
 picker_close12(a,"Saved in your chosen folder.",1);invalidate(w->bounds);serial_text("M128_SAVE_AS_PASS\n");
}
static void picker_accept12(unsigned decision){
 desktop_window*w=desktop_lookup(&model,file_dialog_state11.owner);if(!w){file_dialog_state11.mode=0;whole();return;}application*a=&apps[w-model.windows];
 if(picker12.phase==P12_FOLDER_REVIEW){
  if(!file_name_valid11(file_dialog_state11.input)||!picker_writable12(picker12.path)||picker_busy12()){picker_error12("Choose a valid folder name in a writable location and finish active transfers.");return;}
  char target[256];if(file_join11(target,picker12.path,file_dialog_state11.input)){picker_error12("This folder path is too long.");return;}
  unsigned status=v6_mkdir(m6_volume(),target);if(status){picker_error12(file_error_text11(status));return;}picker12.phase=0;file_dialog_state11.focus=1;picker_visit12(target,1);return;
 }
 if(picker12.phase==P12_REPLACE_REVIEW){picker_save12(w,a,1);return;}
 if(picker12.phase==P12_DIRTY_REVIEW){
  if(!picker_unchanged12(entry(picker12.pending))){picker12.phase=0;picker_error12("The selected file changed. Choose it again; your unsaved text is kept.");return;}
  char path[256];copy(path,picker12.pending,256);picker_editor_open12(w,a,path,decision);return;
 }
 const v6_entry*e=picker_selected12();
 if(picker12.purpose==P12_ZIP_FOLDER){char folder[256];copy(folder,e&&e->kind==2?e->path:picker12.path,256);
  if(!picker_writable12(folder)||picker_busy12()){picker_error12("Choose one of your writable folders and finish active file transfers first.");return;}
  unsigned status=zip_extract_at74(a,folder);if(status){picker_error12("Extraction stopped. The ZIP is kept; inspect any partial output in Files.");return;}copy(picker12.path,folder,256);picker_close12(a,"Extracted into a new folder at your chosen location.",1);serial_text("M128_FOLDER_CHOSEN\n");return;
 }
 if(e&&e->kind==2){char path[256];copy(path,e->path,256);picker_visit12(path,1);return;}
 if(picker12.purpose==P12_TEXT_SAVE){picker_save12(w,a,0);return;}
 if(!e||e->kind!=1){picker_error12("Select a file in the list, then choose Open.");return;}
 char path[256];copy(path,e->path,256);
 if(picker12.purpose==P12_TEXT_OPEN){picker_editor_open12(w,a,path,0);return;}
 char previous[256];copy(previous,a->path,256);copy(a->path,path,256);
 unsigned status=picker12.purpose==P12_IMAGE_OPEN?image_load74(a):zip_load74(a);
 if(status){copy(a->path,previous,256);if(picker12.purpose==P12_IMAGE_OPEN)(void)image_load74(a);else(void)zip_load74(a);picker_error12("This file does not match the supported format or size. The original file is unchanged.");return;}
 picker_close12(a,"Opened the selected file.",1);serial_text("M128_FORMAT_OPENED\n");
}
static unsigned picker_action12(uint64_t token,unsigned command){
 desktop_window*w=desktop_lookup(&model,token);
 if(command==P12_OPEN||command==P12_SAVE_AS||command==P12_EXTRACT_TO||command==IMAGE_CHOOSE74||command==ZIP_CHOOSE74){
  if(!w)return 0;unsigned purpose=command==P12_EXTRACT_TO?P12_ZIP_FOLDER:command==P12_SAVE_AS?P12_TEXT_SAVE:w->app==EDITOR?P12_TEXT_OPEN:w->app==IMAGES74?P12_IMAGE_OPEN:w->app==ARCHIVES74?P12_ZIP_OPEN:0;
  if((command==IMAGE_CHOOSE74&&w->app!=IMAGES74)||!purpose||(command==P12_SAVE_AS&&w->app!=EDITOR)||((command==P12_EXTRACT_TO||command==ZIP_CHOOSE74)&&w->app!=ARCHIVES74))return 0;
  picker_begin12(token,purpose);return 1;
 }
 if(!picker_owner12(token)||command<P12_CANCEL||command>P12_DISCARD_OPEN)return 0;
 picker12.error[0]=0;
 if(command==P12_CANCEL){picker_close12(0,"",0);serial_text("M128_PICKER_CANCELLED\n");return 1;}
 if(command==P12_REVIEW_BACK){picker12.phase=0;file_dialog_state11.focus=picker12.purpose==P12_TEXT_SAVE?2:1;whole();return 1;}
 if(command==P12_REPLACE||command==P12_SAVE_OPEN||command==P12_DISCARD_OPEN||command==P12_ACCEPT){picker_accept12(command==P12_SAVE_OPEN?1:command==P12_DISCARD_OPEN?2:0);return 1;}
 if(picker12.phase){if(command==P12_NAME&&picker12.phase==P12_FOLDER_REVIEW){file_dialog_state11.focus=2;file_dialog_state11.cursor=length(file_dialog_state11.input);file_dialog_state11.anchor=0;whole();}return 1;}
 if(command==P12_ADDRESS){file_dialog_state11.focus=0;picker12.address_cursor=length(picker12.address);picker12.address_anchor=0;}
 else if(command==P12_NAME){file_dialog_state11.focus=2;picker12.name_cursor=length(picker12.name);picker12.name_anchor=0;}
 else if(command==P12_BACK||command==P12_FORWARD){unsigned p=picker12.history_position;if(command==P12_BACK&&p)--p;else if(command==P12_FORWARD&&p+1<picker12.history_count)++p;char path[256];copy(path,picker12.history[p],256);if(picker_folder12(path)){picker12.history_position=p;picker_visit12(path,0);}else picker_error12("That previous folder is no longer available. Your current folder is kept.");}
 else if(command==P12_UP){char path[256];file_parent11(path,picker12.path);picker_visit12(path,1);}
 else if(command>=P12_HOME&&command<=P12_PICTURES){char path[256];if(command==P12_HOME)home72(path);else root_path(path,command==P12_DOCUMENTS?"Documents":command==P12_DOWNLOADS?"Downloads":"Pictures");picker_visit12(path,1);}
 else if(command==P12_FILTER){picker12.filter^=1;picker12.generation=0;picker12.offset=0;picker12.selected=UINT32_MAX;}
 else if(command==P12_PREVIOUS)picker12.offset=picker12.offset>=picker12.rows?picker12.offset-picker12.rows:0;
 else if(command==P12_NEXT){picker_list12();if(picker12.offset+picker12.rows<picker12.count)picker12.offset+=picker12.rows;}
 else if(command==P12_NEW_FOLDER){if(!picker_writable12(picker12.path)||picker_busy12()){picker_error12("This location does not accept a new folder right now.");return 1;}picker12.phase=P12_FOLDER_REVIEW;copy(file_dialog_state11.input,"New folder",256);file_dialog_state11.cursor=10;file_dialog_state11.anchor=0;file_dialog_state11.focus=2;}
 whole();return 1;
}
static unsigned picker_dispatch12(i11_target target,unsigned event){
 if(!picker_owner12(target.window))return 0;
 if(target.kind==I11_BACKGROUND&&(event&I11_SELECT)){desktop_focus(&model,target.window);desktop_focus11=0;whole();return 1;}
 if(target.action<P12_ROW||target.action>=P12_ROW+V6_ENTRIES)return 0;
 if(picker12.phase)return 1;unsigned index=target.action-P12_ROW;const v6_entry*e=&m6_volume()->entries[index];
 if(!e->kind||!file_direct_child11(e->path,picker12.path)||!picker_match12(e))return 1;
 if(event&I11_SELECT){picker_select12(index);file_dialog_state11.focus=1;picker12.error[0]=0;if(e->kind==1&&picker12.purpose==P12_TEXT_SAVE){copy(picker12.name,file_basename11(e->path),256);picker12.name_cursor=picker12.name_anchor=length(picker12.name);}whole();}
 if(event&I11_ACTIVATE){if(e->kind==2){char path[256];copy(path,e->path,256);picker_visit12(path,1);}else picker_accept12(0);}return 1;
}
static unsigned picker_focus_enabled12(unsigned i){
 if(i==2)return picker12.purpose==P12_TEXT_SAVE;if(i==3)return picker12.purpose!=P12_ZIP_FOLDER;
 if(i==6)return picker12.history_position>0;if(i==7)return picker12.history_position+1<picker12.history_count;
 if(i==8)return !equal(picker12.path,"/");if(i==13)return picker_writable12(picker12.path)&&!picker_busy12();if(i==14)return picker12.offset>0;if(i==15)return picker12.offset+picker12.rows<picker12.count;return 1;
}
static unsigned picker_key12(int key){
 if(!picker_live12()||!file_dialog_owner_focused11())return 0;if(key==135||key==137)return 0;
 file_dialog11*d=&file_dialog_state11;uint64_t token=d->owner;
 if(key==27){picker_action12(token,picker12.phase?P12_REVIEW_BACK:P12_CANCEL);return 1;}
 if(picker12.phase){
  if(picker12.phase==P12_FOLDER_REVIEW&&d->focus==2&&key!=9&&key!=136&&key!=10){if(file_text_key11(d->input,&d->cursor,&d->anchor,key)){picker12.error[0]=0;whole();}return 1;}
  if(key==9||key==136){unsigned choices[4]={4,5,7,0},n=3;if(picker12.phase==P12_DIRTY_REVIEW){choices[0]=4;choices[1]=6;choices[2]=5;choices[3]=7;n=4;}else if(picker12.phase==P12_FOLDER_REVIEW){choices[0]=2;choices[1]=4;choices[2]=5;choices[3]=7;n=4;}unsigned at=0;while(at<n&&choices[at]!=d->focus)++at;if(at==n)at=0;else at=(at+(key==9?1:n-1))%n;d->focus=choices[at];whole();return 1;}
  if(key==10||key==32)picker_action12(token,d->focus==7?P12_CANCEL:d->focus==5?P12_REVIEW_BACK:d->focus==6?P12_DISCARD_OPEN:picker12.phase==P12_REPLACE_REVIEW?P12_REPLACE:picker12.phase==P12_DIRTY_REVIEW?P12_SAVE_OPEN:P12_ACCEPT);
  return 1;
 }
 if((input11_modifiers()&4)&&(key==128||key==129||key==133)){picker_action12(token,key==128?P12_BACK:key==129?P12_FORWARD:P12_UP);return 1;}
 if(key==12){d->focus=0;picker12.address_cursor=length(picker12.address);picker12.address_anchor=0;whole();return 1;}
 if(key==9||key==136){do{d->focus=(d->focus+(key==9?1:15))%16;}while(!picker_focus_enabled12(d->focus));whole();return 1;}
 if(d->focus==0){if(key==10){char path[256];const char*s=picker12.address;if(!file_compare_text11(s,"Home"))home72(path);else if(!file_compare_text11(s,"Documents"))root_path(path,"Documents");else if(!file_compare_text11(s,"Downloads"))root_path(path,"Downloads");else if(!file_compare_text11(s,"Pictures"))root_path(path,"Pictures");else if(s[0]=='/')copy(path,s,256);else if(file_join11(path,picker12.path,s)){picker_error12("This location is too long.");return 1;}
   if(!file_compare_text11(s,"USB drives")||!memcmp(s,"USB:",4)){picker_error12("Use Files to copy a USB file into Downloads first. Direct USB editing is unavailable.");return 1;}
   picker_visit12(path,1);d->focus=1;return 1;}
  if(file_text_key11(picker12.address,&picker12.address_cursor,&picker12.address_anchor,key)){picker12.error[0]=0;whole();}return 1;
 }
 if(d->focus==2){if(key==10)picker_accept12(0);else if(file_text_key11(picker12.name,&picker12.name_cursor,&picker12.name_anchor,key)){picker12.selected=UINT32_MAX;picker12.error[0]=0;whole();}return 1;}
 if(d->focus==1){picker_list12();unsigned n=0;while(n<picker12.count&&picker12.order[n]!=picker12.selected)++n;
  if(key==133||key==134||key==130||key==131){if(!picker12.count)return 1;if(n==picker12.count)n=0;else if(key==133&&n)--n;else if(key==134&&n+1<picker12.count)++n;else if(key==130)n=0;else if(key==131)n=picker12.count-1;
   picker_select12(picker12.order[n]);if(picker12.rows)picker12.offset=n/picker12.rows*picker12.rows;whole();return 1;}
  if(key==8){picker_action12(token,P12_BACK);return 1;}if(key==10){const v6_entry*e=picker_selected12();if(e&&e->kind==2){char path[256];copy(path,e->path,256);picker_visit12(path,1);}else picker_accept12(0);return 1;}
  return 1;
 }
 if(key==10||key==32){const unsigned commands[]={P12_ADDRESS,0,P12_NAME,P12_FILTER,P12_ACCEPT,P12_CANCEL,P12_BACK,P12_FORWARD,P12_UP,P12_HOME,P12_DOCUMENTS,P12_DOWNLOADS,P12_PICTURES,P12_NEW_FOLDER,P12_PREVIOUS,P12_NEXT};if(d->focus<16)picker_action12(token,commands[d->focus]);}return 1;
}
static unsigned picker_shortcut12(int key){
 if(picker_live12()&&file_dialog_owner_focused11())return 0;desktop_window*w=model.focused<DESKTOP_WINDOWS?&model.windows[model.focused]:0;if(!w||!w->live||desktop_focus11||launcher||w->app!=EDITOR)return 0;
 if(key==15||(key==19&&(input11_modifiers()&2))){picker_begin12(desktop_token(&model,model.focused),key==15?P12_TEXT_OPEN:P12_TEXT_SAVE);return 1;}return 0;
}
static void picker_button12(int x,int y,int width,const char*label,unsigned command,unsigned enabled,unsigned primary,unsigned focus){file_dialog_button11(x,y,width,label,command,enabled,primary,focus,command==P12_REPLACE||command==P12_DISCARD_OPEN);}
static unsigned picker_draw12(void){
 if(!picker_live12())return 0;if(!desktop_lookup(&model,file_dialog_state11.owner)){file_dialog_state11.mode=0;return 1;}if(!file_dialog_owner_focused11())return 1;
 file_dialog11*d=&file_dialog_state11;int width=model.width>900?860:(int)model.width-40,height=model.height>712?620:(int)model.height-92,x=((int)model.width-width)/2,y=((int)model.height-60-height)/2;
 ui73_shadow(x,y,width,height);ui73_round(x,y,width,height,12,paper());ui73_fit(x+24,y+20,width-48,picker12.phase==P12_REPLACE_REVIEW?"Replace this file?":picker12.phase==P12_DIRTY_REVIEW?"Keep your current changes?":picker12.phase==P12_FOLDER_REVIEW?"Create a folder":picker12.purpose==P12_TEXT_SAVE?"Save as":picker12.purpose==P12_ZIP_FOLDER?"Choose an extraction folder":"Open a file",UI12_SECTION,ink());
 if(picker12.phase){
  if(picker12.phase==P12_FOLDER_REVIEW){ui73_fit(x+24,y+62,width-48,picker12.path,1,ink());text(x+24,y+106,"Folder name",1,ink());desktop_rect r={x+24,y+138,width-48,40};file_text_field11(r,d->input,d->cursor,d->anchor,d->focus==2,0);file_control11(d->owner,r,P12_NAME);}
  else{ui73_paragraph(x+24,y+64,width-48,2,picker12.phase==P12_REPLACE_REVIEW?"Replacing removes this destination's previous contents. Your original document stays open until the new save succeeds.":"Your current document has unsaved changes. Save it, discard those changes explicitly, or return to your choice.",ink());text(x+24,y+120,picker12.phase==P12_REPLACE_REVIEW?"Destination file":"Selected file",1,ink());ui73_paragraph(x+24,y+148,width-48,3,file_basename11(picker12.pending),ink());desktop_rect r={x+24,y+228,width-48,36};file_text_field11(r,picker12.pending,length(picker12.pending),length(picker12.pending),0,0);}
  ui73_paragraph(x+24,y+height-152,width-48,2,picker12.error[0]?picker12.error:"Back returns without changing the file. Cancel keeps your work.",picker12.error[0]?0xc75652:ink());
  int bw=(width-56)/2;if(picker12.phase==P12_DIRTY_REVIEW){picker_button12(x+24,y+height-100,bw,"Save and open",P12_SAVE_OPEN,1,1,4);picker_button12(x+32+bw,y+height-100,bw,"Discard and open",P12_DISCARD_OPEN,1,0,6);}
  else picker_button12(x+24,y+height-100,bw,picker12.phase==P12_FOLDER_REVIEW?"Create and open":"Replace file",picker12.phase==P12_FOLDER_REVIEW?P12_ACCEPT:P12_REPLACE,1,1,4);
  picker_button12(x+24,y+height-54,bw,"Back",P12_REVIEW_BACK,1,0,5);picker_button12(x+32+bw,y+height-54,bw,"Cancel",P12_CANCEL,1,0,7);return 1;
 }
 ui73_fit(x+24,y+54,width-48,"Native files. For USB files, first copy them into Downloads with Files.",UI12_SECONDARY,ink());
 picker_button12(x+24,y+84,44,"<",P12_BACK,picker12.history_position>0,0,6);picker_button12(x+76,y+84,44,">",P12_FORWARD,picker12.history_position+1<picker12.history_count,0,7);picker_button12(x+128,y+84,44,"Up",P12_UP,!equal(picker12.path,"/"),0,8);
 desktop_rect address={x+184,y+84,width-208,36};file_text_field11(address,picker12.address,picker12.address_cursor,picker12.address_anchor,d->focus==0,0);file_control11(d->owner,address,P12_ADDRESS);
 const char*places[]={"Home","Documents","Downloads","Pictures"};unsigned commands[]={P12_HOME,P12_DOCUMENTS,P12_DOWNLOADS,P12_PICTURES};int pw=(width-72)/4;
 for(unsigned i=0;i<4;++i)picker_button12(x+24+(pw+8)*(int)i,y+130,pw,places[i],commands[i],1,0,9+i);
 picker_list12();int top=y+190,bottom=y+height-178;picker12.rows=bottom>top?(unsigned)(bottom-top)/36:1;if(!picker12.rows)picker12.rows=1;if(picker12.rows>10)picker12.rows=10;
 text(x+32,y+174,"Name",UI12_SECONDARY,ink());if(width>=640)text(x+width-144,y+174,"Type",UI12_SECONDARY,ink());
 for(unsigned row=0;row<picker12.rows&&picker12.offset+row<picker12.count;++row){unsigned index=picker12.order[picker12.offset+row];const v6_entry*e=&m6_volume()->entries[index];desktop_rect r={x+24,top+(int)row*36,width-48,36};
  if(index==picker12.selected)rectangle(r,file_tint11());if(index==picker12.selected&&d->focus==1)file_focus_rect11(r);file_icon11(r.x+8,r.y+7,22,e);ui73_fit(r.x+40,r.y+8,r.width-(width>=640?190:52),file_basename11(e->path),1,ink());if(width>=640)ui73_fit(x+width-144,r.y+8,116,ui12_file_type(file_basename11(e->path),e->kind),UI12_SECONDARY,ink());file_control11(d->owner,r,P12_ROW+index);
 }
 if(!picker12.count)ui73_fit(x+32,top+12,width-64,"No matching items. Choose another folder or file type.",1,ink());
 int controls_y=y+height-164;picker_button12(x+24,controls_y,64,"Prev",P12_PREVIOUS,picker12.offset>0,0,14);picker_button12(x+96,controls_y,64,"Next",P12_NEXT,picker12.offset+picker12.rows<picker12.count,0,15);
 picker_button12(x+168,controls_y,108,"New folder",P12_NEW_FOLDER,picker_writable12(picker12.path)&&!picker_busy12(),0,13);
 if(picker12.purpose==P12_TEXT_SAVE){text(x+24,y+height-116,"Name",UI12_SECONDARY,ink());desktop_rect field={x+84,y+height-122,width-108,36};file_text_field11(field,picker12.name,picker12.name_cursor,picker12.name_anchor,d->focus==2,0);file_control11(d->owner,field,P12_NAME);}
 if(picker12.purpose!=P12_ZIP_FOLDER)picker_button12(x+width-228,controls_y,204,picker12.filter?"All files":picker12.purpose==P12_IMAGE_OPEN?"BMP images":picker12.purpose==P12_ZIP_OPEN?"ZIP archives":picker12.purpose==P12_TEXT_SAVE?"Text (.txt)":"Text files",P12_FILTER,1,0,3);
 ui73_fit(x+24,y+height-76,width-48,picker12.error[0]?picker12.error:picker12.purpose==P12_TEXT_SAVE?"Text type adds .txt when no extension is supplied. The original is kept.":"Click selects. Double-click or Enter opens. Escape cancels.",UI12_SECONDARY,picker12.error[0]?0xc75652:ink());
 picker_button12(x+24,y+height-46,120,"Cancel",P12_CANCEL,1,0,5);picker_button12(x+width-190,y+height-46,166,picker12.purpose==P12_TEXT_SAVE?"Save":picker12.purpose==P12_ZIP_FOLDER?"Choose folder":"Open",P12_ACCEPT,1,1,4);
 return 1;
}
