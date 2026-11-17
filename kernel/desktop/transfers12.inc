/* Shared command admission and bounded compact command menu. */
static unsigned files_can_command12(uint64_t token,unsigned command){
 desktop_window*w=file_owner_window11(token);if(!w)return 0;application*a=&apps[w-model.windows];
 unsigned selected=file_selected_count11(a),busy=files_busy12()||file_dialog_state11.mode||w8_pending(),native=!a->usb_mode10;
 unsigned writable=native&&files_native_ready12(a)&&writable72(a->path)&&!file_in_bin11(a->path)&&!m6_volume()->readonly;
 if(command==F11_COPY){if(!a->usb_mode10)return selected!=0;if(a->usb_mode10!=2||selected!=1||!a->usb_selected10)return 0;rem10_entry item;unsigned total=0;return !rem10_list(a->usb_disk10,a->usb_context10,a->usb_part10,a->usb_path10,a->usb_selected10-1,&item,1,&total)&&a->usb_selected10<=total&&item.kind==1;}
 if(command==F11_PASTE)return !busy&&writable&&clipboard_kind11==2&&file_clip11.count;
 if(command==FILE_FOLDER||command==F11_NEW_TEXT)return !busy&&writable;
 if(command==F11_UNDO)return !busy&&!m6_volume()->readonly&&file_undo_state11.kind;
 if(command==F11_JOB_DETAILS)return !busy&&file_job_result11[0];
 if(command==F11_RESTORE)return !busy&&native&&!m6_volume()->readonly&&file_is_bin11(a->path)&&selected;
 if(command==F11_PROPERTIES)return !busy&&selected==1;
 if(command==F11_CUT||command==F11_RENAME||command==F11_RECYCLE){
  if(busy||!native||!writable||!selected||(command==F11_RENAME&&selected!=1))return 0;
  for(unsigned row=0;row<children72(a);++row)if(selected_row11(a,row)){const v6_entry*e=child_at(a,row);if(!e||!file_user_item11(e->path)||file_open_under11(e->path))return 0;}return 1;
 }
 return 0;
}
static void files_commands_menu12(uint64_t token){
 desktop_window*w=file_owner_window11(token);if(!w)return;application*a=&apps[w-model.windows];file_menu_begin11(token,pointer_x,pointer_y);
 const char*names[]={"Copy  (Ctrl+C)","Cut  (Ctrl+X)","Paste  (Ctrl+V)","Rename...  (F2)","Move to Recycle Bin","New folder...","New text file...","Undo last supported action","Properties","Last transfer details"};
 unsigned commands[]={F11_COPY,F11_CUT,F11_PASTE,F11_RENAME,F11_RECYCLE,FILE_FOLDER,F11_NEW_TEXT,F11_UNDO,F11_PROPERTIES,F11_JOB_DETAILS};
 for(unsigned i=0;i<10;++i)file_menu_add11(names[i],commands[i],files_can_command12(token,commands[i]));
 copy(file_menu_reason11,a->usb_mode10?"USB: copy one file; native folders offer more actions.":files_busy12()?"A transfer is running. Wait for it or choose Cancel in Files.":file_dialog_state11.mode?"Finish or cancel the current file dialog before changing files.":!writable72(a->path)?"This location is protected. Use Home for your own files.":!file_selected_count11(a)?"Select an item first. Paste also needs files copied to the clipboard.":"Close any app using the item before moving, renaming or recycling it.",128);file_menu_fit11();
}
