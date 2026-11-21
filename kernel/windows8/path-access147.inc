/* Shared native Windows path grants, also compiled by the storage test adapter. */
static unsigned path8(const char*p,unsigned write){
 if(p[0]!='/'||!p[1]||length8(p)>=255)return 0;unsigned component=0;
 for(unsigned i=1;p[i];++i){if((uint8_t)p[i]<32||p[i]=='\\')return 0;if(p[i]=='/'){if(!component)return 0;component=0;}else{if(++component>63)return 0;if(p[i]=='.'&&(p[i+1]=='/'||!p[i+1])&&(i==1||p[i-1]=='/'||(p[i-1]=='.'&&(i==2||p[i-2]=='/'))))return 0;}}
 if(!component)return 0;
 if(!write)return prefix8(p,input8.user_root)||prefix8(p,input8.product_root)||equal8(p,input8.source)
#ifdef ENGINE_M14
  ||prefix8(p,"/System/Windows/Installer")||prefix8(p,"/Data/Windows/Common/Programs")
  ||equal8(p,"/System/Windows/Tools/cmd.exe")||equal8(p,"/System/Windows/Tools/xcopy.exe")
  ||(installer_authority147()&&(prefix8(p,"/Applications/Windows")||installer_user_grant147(p,0)))
#endif
  ;
#ifdef ENGINE_M14
#ifdef ENGINE_EXE_BROKER148
 if(spaces142[active_space142]->exe_context148)return prefix8(p,input8.product_root)||exe_user_grant148(p,0);
#endif
 if(installer_authority147())return (prefix8(p,input8.product_root)&&(!equal8(p,input8.product_root)||input8.command==W8_INSTALL||input8.command==W8_REMOVE))||installer_user_grant147(p,0);
#else
 if(input8.command==W8_INSTALL||input8.command==W8_REMOVE)return prefix8(p,input8.product_root)&&(!equal8(p,input8.product_root)||input8.command==W8_INSTALL||input8.command==W8_REMOVE);
#endif
 return input8.command==W8_RUN&&prefix8(p,input8.user_root)&&!equal8(p,input8.user_root);
}
