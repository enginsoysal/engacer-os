/* Original shared identity assets. Rendering never loads or executes a file. */
static unsigned shell_suffix12(const char*path,const char*extension){
 const char*dot=0;for(unsigned n=0;path[n];++n){if(path[n]=='/')dot=0;else if(path[n]=='.')dot=path+n+1;}
 if(!dot)return 0;
 while(*dot&&*extension){unsigned c=(uint8_t)*dot++;if(c>='A'&&c<='Z')c+=32;if(c!=(unsigned)*extension++)return 0;}
 return !*dot&&!*extension;
}
static unsigned shell_path_icon12(const char*path,unsigned kind){
 if(kind==2)return ICON12_FOLDER;
 if(shell_suffix12(path,"txt")||shell_suffix12(path,"md")||shell_suffix12(path,"log")||shell_suffix12(path,"json")||shell_suffix12(path,"ini"))return ICON12_TEXT;
 if(shell_suffix12(path,"bmp"))return ICON12_IMAGE_FILE;
 if(shell_suffix12(path,"wav"))return ICON12_AUDIO_FILE;
 if(shell_suffix12(path,"zip"))return ICON12_ARCHIVE_FILE;
 if(shell_suffix12(path,"msi"))return ICON12_PACKAGE;
 if(shell_suffix12(path,"exe")||shell_suffix12(path,"elf"))return ICON12_EXECUTABLE;
 return ICON12_UNKNOWN;
}
static unsigned shell_entry_icon12(const v6_entry*e){
 if(e->kind==2&&!memcmp(e->path,"/Applications/",14)){
  #define ICON_APP_NAME12(symbol,kind,id,title,worker,ready) {#id,kind},
  static const struct{const char*name;unsigned icon;}names[]={APP74_CATALOG(ICON_APP_NAME12)};
  #undef ICON_APP_NAME12
  for(unsigned i=0;i<sizeof(names)/sizeof(*names);++i)if(equal(e->path+14,names[i].name))return names[i].icon;
 }
 return shell_path_icon12(file_label11(e),e->kind);
}
static void shell_file_icon12(int x,int y,unsigned size,const v6_entry*e){
 ui12_icon(shell_entry_icon12(e),x,y,size,preferences.dark);
 if(shell_suffix12(file_label11(e),"link"))ui12_icon(ICON12_SHORTCUT,x,y+(int)size/2,size/2,preferences.dark);
}
static void icon_button12(uint64_t token,int x,int y,int width,const char*label,unsigned action,unsigned primary,unsigned icon){
 button(token,x,y,width,"",action,primary);
 unsigned state=component_state12(token,action);
 ui12_style style=ui12_control_style(ui12_theme(preferences.dark,preferences.accent),state,primary);
 ui12_icon(icon,x+7,y+10+!!(state&UI12_PRESSED),16,preferences.dark);
 if(width>=60)ui73_fit(x+29,y+8+!!(state&UI12_PRESSED),width-35,label,1,style.ink);
}
