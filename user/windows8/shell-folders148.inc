/* Current-owner known folders, using kernel-bound roots, not mutable environment
 * overrides. Queries do not create anything unless CSIDL_FLAG_CREATE is set. */
static int shell_folder_error148(WCHAR*out,unsigned error){if(out)out[0]=0;return(int)(0x80070000u|error);}
static int MS f_SHGetFolderPathW(HANDLE owner,int csidl,HANDLE token,unsigned flags,WCHAR*out){
 (void)owner;if(!out)return(int)0x80070057u;out[0]=0;
 if(token)return(int)0x80070005u;
 if(csidl<0||((unsigned)csidl&~0xf0ffu)||flags>1||(((unsigned)csidl&0xc000u)==0xc000u))return(int)0x80070057u;
 unsigned id=(unsigned)csidl&255u;const char*suffix=0;
 switch(id){
 case 0x28:suffix="";break;
 case 0x05:suffix="/Documents";break;
 case 0x00:case 0x10:suffix="/Desktop";break;
 case 0x1a:suffix="/AppData/Roaming";break;
 case 0x1c:suffix="/AppData/Local";break;
 case 0x02:suffix="/AppData/Roaming/Microsoft/Windows/Start Menu/Programs";break;
 case 0x0b:suffix="/AppData/Roaming/Microsoft/Windows/Start Menu";break;
 case 0x07:suffix="/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup";break;
 case 0x06:suffix="/Favorites";break;
 case 0x0d:suffix="/Music";break;
 case 0x0e:suffix="/Videos";break;
 case 0x27:suffix="/Pictures";break;
 default:return id>0x3f?(int)0x80070057u:(int)0x80004001u;
 }
 char native[256],windows[512];copy8(native,job8->user_root,256);
 unsigned root=len8(native),extra=len8(suffix);if(root+extra>=256)return shell_folder_error148(out,206);append8(native,suffix,256);
 winpath8(native,windows,sizeof(windows));WCHAR result[260];if(utf8_to16(windows,result,260)<0)return shell_folder_error148(out,206);
 if(!((unsigned)csidl&0x4000u)){
  w8_file_info info;int status=stat8(native,&info);
  if(status&&((unsigned)csidl&0x8000u)){
   for(unsigned at=root+1;at<=root+extra;++at)if(!native[at]||native[at]=='/'){
    char separator=native[at];native[at]=0;
    if(stat8(native,&info)&&mkdir8(native)){native[at]=separator;return(int)0x80004005u;}
    native[at]=separator;
   }
   status=stat8(native,&info);
  }
  if(status)return shell_folder_error148(out,3);
  if(info.kind!=2)return shell_folder_error148(out,267);
 }
 memcpy(out,result,((size_t)wlen8(result)+1)*sizeof(WCHAR));return 0;
}
