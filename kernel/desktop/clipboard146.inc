/* Reuse the existing bounded native text buffer; no mirrored history or polling. */
#ifdef ENGINE_M14
static uint64_t clipboard_revision146=1;
#endif
static unsigned native_clipboard_allowed146(void){
#ifdef ENGINE_M14
 return clipboard_revision146<INT64_MAX&&w8_clipboard_native_allowed146();
#else
 return 1;
#endif
}
static unsigned native_clipboard_readable146(void){
#ifdef ENGINE_M14
 return w8_clipboard_native_readable146();
#else
 return 1;
#endif
}
static void file_clipboard_clear11(void){
#ifdef ENGINE_M14
 uint64_t first=(uint64_t)(uintptr_t)file_clip11.roots;
 for(unsigned i=0;i<file_clip11.pages;++i)page_free(first+(uint64_t)i*4096);
 file_clip11.roots=0;file_clip11.pages=0;
#endif
 file_clip11.count=0;
}
static int file_clipboard_store11(const file_root11 *roots,unsigned count,unsigned kind){
 unsigned bytes=count*sizeof(*roots);
#ifdef ENGINE_M14
 unsigned pages=(bytes+4095)/4096;
 if(pages>file_clip11.pages){
  uint64_t first=pages_alloc_run(pages);
  if(!first)return 0;
  file_clipboard_clear11();
  file_clip11.roots=(void*)(uintptr_t)first;
  file_clip11.pages=pages;
 }
#endif
 memcpy(file_clip11.roots,roots,bytes);
 file_clip11.count=count;file_clip11.kind=kind;
 return 1;
}
static void native_clipboard_changed146(unsigned kind){
 clipboard_kind11=kind;if(kind!=2)file_clipboard_clear11();
 if(kind!=1){clipboard_length=0;clipboard[0]=0;}
#ifdef ENGINE_M14
 ++clipboard_revision146;w8_clipboard_native_changed146();
#endif
}
static unsigned native_clipboard_text146(const char*text,unsigned bytes){
 if(bytes>=sizeof(clipboard)||!native_clipboard_allowed146())return 0;
 if(text!=clipboard)memcpy(clipboard,text,bytes);clipboard[bytes]=0;clipboard_length=bytes;native_clipboard_changed146(1);return 1;
}
#ifdef ENGINE_M14
unsigned desktop_clipboard_read146(char*first,char*second,unsigned capacity,uint64_t*revision){
 *revision=clipboard_revision146;if(clipboard_kind11!=1)return 0;unsigned bytes=clipboard_length+1;
 if(first&&capacity>=bytes){unsigned n=bytes>4096?4096:bytes;memcpy(first,clipboard,n);if(bytes>n&&second)memcpy(second,clipboard+n,bytes-n);}
 return bytes;
}
unsigned desktop_clipboard_write146(const char*first,const char*second,unsigned bytes){
 if(clipboard_revision146>=INT64_MAX||bytes>sizeof(clipboard)||(!first&&bytes)||(bytes>4096&&!second))return 1816;
 if(bytes){unsigned n=bytes>4096?4096:bytes;memcpy(clipboard,first,n);if(bytes>n)memcpy(clipboard+n,second,bytes-n);clipboard_length=bytes-1;clipboard_kind11=1;}
 else{clipboard_length=0;clipboard[0]=0;clipboard_kind11=0;}
 file_clipboard_clear11();++clipboard_revision146;return 0;
}
#endif
