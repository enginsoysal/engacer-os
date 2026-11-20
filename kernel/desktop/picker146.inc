/* The existing native picker serves a generation-bound Windows request. */
static void picker_foreign_cancel146(void){
#ifdef ENGINE_M14
 if(picker_foreign_generation146)w8_picker_complete146(picker_foreign_generation146,0,picker12.filter,0);
#endif
 picker_foreign_generation146=0;
}
static const char*picker_foreign_title146(const char*fallback){
 if(picker12.phase)return fallback;
#ifdef ENGINE_M14
 const wpick_view146*v=picker_foreign12()?w8_picker_native146():0;if(v&&v->generation==picker_foreign_generation146&&v->title[0])return v->title;
#endif
 return fallback;
}
static const char*picker_foreign_filter146(const char*fallback){
#ifdef ENGINE_M14
 const wpick_view146*v=picker_foreign12()?w8_picker_native146():0;if(v&&v->generation==picker_foreign_generation146&&picker12.filter<v->filter_count)return v->filters[picker12.filter].label;
#endif
 return fallback;
}
#ifdef ENGINE_M14
static unsigned picker_name146(const char*name){
 unsigned n=length(name);if(!n||n>63||equal(name,".")||equal(name,"..")||name[n-1]==' '||name[n-1]=='.'||!text_valid146(name,n))return 0;
 char stem[5]={0};unsigned stem_bytes=0;while(stem_bytes<n&&name[stem_bytes]!='.'&&stem_bytes<5){unsigned c=(uint8_t)name[stem_bytes];if(stem_bytes<4)stem[stem_bytes]=(char)(c>='a'&&c<='z'?c-32:c);++stem_bytes;}
 if((stem_bytes==3&&(equal(stem,"CON")||equal(stem,"PRN")||equal(stem,"AUX")||equal(stem,"NUL")))||(stem_bytes==4&&stem[3]>='1'&&stem[3]<='9'&&((stem[0]=='C'&&stem[1]=='O'&&stem[2]=='M')||(stem[0]=='L'&&stem[1]=='P'&&stem[2]=='T'))))return 0;
 for(unsigned i=0;i<n;++i){unsigned c=(uint8_t)name[i];if(c=='/'||c==0x5c||c==':'||c=='*'||c=='?'||c=='"'||c=='<'||c=='>'||c=='|')return 0;}return 1;
}
static void picker_finish146(const char*path){
 if(!w8_picker_complete146(picker_foreign_generation146,path,picker12.filter,0)){picker_error12("This request is no longer available. Cancel and try again.");return;}
 picker_foreign_generation146=0;picker_close12(0,"",0);serial_text("M146_COMMON_PICKER_SELECTED\n");
}
#endif
static unsigned picker_foreign_accept146(unsigned decision){
 (void)decision;if(!picker_foreign12())return 0;
#ifdef ENGINE_M14
 const wpick_view146*v=w8_picker_native146();if(!v||v->generation!=picker_foreign_generation146){picker_close12(0,"",0);return 1;}
 const v6_entry*selected=picker_selected12();if(!picker12.phase&&selected&&selected->kind==2){char path[256];copy(path,selected->path,256);picker_visit12(path,1);return 1;}
 if(!picker_saving12()){
  if(!selected||selected->kind!=1){picker_error12("Select a file in the list, then choose Open.");return 1;}
  char path[256];copy(path,selected->path,256);picker_finish146(path);return 1;
 }
 char name[256],target[256];copy(name,picker12.name,256);
 if(!ui12_file_extension(name)[0]&&v->extension[0]){if(length(name)+length(v->extension)+2>sizeof(name)){picker_error12("The filename is too long.");return 1;}append(name,".",256);append(name,v->extension,256);}
 if(!picker_name146(name)){picker_error12("Use a valid UTF-8 filename of 1-63 bytes, without a trailing dot or space.");return 1;}
 if(!picker_writable12(picker12.path)||picker_busy12()||!w8_picker_allowed146(v->generation,picker12.path,1)){picker_error12("Choose one of your writable folders and finish active transfers first.");return 1;}
 if(file_join11(target,picker12.path,name)){picker_error12("The folder and filename exceed the supported path length.");return 1;}
 const v6_entry*existing=w8_picker_existing146(v->generation,target);
 if(existing){if(existing->kind!=1||!w8_picker_allowed146(v->generation,existing->path,1)){picker_error12("That destination is protected or is a folder. Choose another filename.");return 1;}
  copy(target,existing->path,256);
  if(picker12.phase!=P12_REPLACE_REVIEW){copy(picker12.pending,target,256);picker_snapshot12(existing);picker12.phase=P12_REPLACE_REVIEW;file_dialog_state11.focus=5;whole();return 1;}
  if(!equal(target,picker12.pending)||!picker_unchanged12(existing)){picker12.phase=0;picker_error12("The destination changed. Review it again before replacing it.");return 1;}
 }else if(picker12.phase==P12_REPLACE_REVIEW){picker12.phase=0;picker_error12("The reviewed destination is no longer available. Choose it again.");return 1;}
 picker_finish146(target);
#endif
 return 1;
}
static void picker_foreign_sync146(void){
#ifdef ENGINE_M14
 const wpick_view146*v=w8_picker_native146();
 if(picker_foreign_generation146){if(!v||v->generation!=picker_foreign_generation146||!picker_live12()||!desktop_lookup(&model,file_dialog_state11.owner)){
   picker_foreign_cancel146();if(picker_foreign12()&&picker_live12()){file_dialog_state11.mode=0;control_active=0;i11_cancel(&interaction11);whole();}
  }return;}
 if(!v)return;uint64_t token=0;for(unsigned i=0;i<DESKTOP_WINDOWS;++i)if(model.windows[i].live&&apps[i].foreign144==v->owner){token=desktop_token(&model,i);break;}
 if(!token||file_dialog_state11.mode||files_busy12()||model.width<560||model.height<512){w8_picker_complete146(v->generation,0,0,0xffff);return;}
 if(!w8_picker_display146(v->generation))return;
 memset(&picker12,0,sizeof(picker12));picker12.purpose=v->save?P12_FOREIGN_SAVE146:P12_FOREIGN_OPEN146;picker12.selected=UINT32_MAX;picker12.filter=v->filter_index;picker_foreign_generation146=v->generation;
 copy(picker12.name,v->name,256);picker12.name_cursor=length(picker12.name);picker12.name_anchor=0;
 file_dialog_open11(P12_DIALOG,token,0);file_dialog_state11.focus=v->save?2:1;picker_visit12(v->directory,1);serial_text("M146_COMMON_PICKER_OPEN\n");
#endif
}
