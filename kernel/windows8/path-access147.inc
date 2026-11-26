/* Shared native Windows path grants, also compiled by the storage test adapter. */
#ifdef ENGINE_M14
/* Related-product checks need catalog records, never another product's payload. */
static unsigned installer_catalog_read1410(const char*p){
 if(equal8(p,"/Applications/Windows"))return 1;
 if(!prefix8(p,"/Applications/Windows"))return 0;
 const char*code=p+sizeof(WIN_PRODUCT_BASE147)-1;
 if(length8(code)<=38||code[38]!='/')return 0;
 char guid[39];memcpy(guid,code,38);guid[38]=0;
 if(!win_product_guid147(guid,1))return 0;
 const char*record=code+38;
 if(equal8(record,"/.EngacerMSI/transaction.bin"))return 2;
 return equal8(record,"/product.bin");
}
#endif
static unsigned path8(const char*p,unsigned write){
 if(p[0]!='/'||!p[1]||length8(p)>=255)return 0;unsigned component=0;
 for(unsigned i=1;p[i];++i){if((uint8_t)p[i]<32||p[i]=='\\')return 0;if(p[i]=='/'){if(!component)return 0;component=0;}else{if(++component>63)return 0;if(p[i]=='.'&&(p[i+1]=='/'||!p[i+1])&&(i==1||p[i-1]=='/'||(p[i-1]=='.'&&(i==2||p[i-2]=='/'))))return 0;}}
 if(!component)return 0;
 if(!write)return prefix8(p,input8.user_root)||prefix8(p,input8.product_root)||equal8(p,input8.source)
#ifdef ENGINE_M14
  ||prefix8(p,"/System/Windows/Installer")||prefix8(p,"/Data/Windows/Common/Programs")
  ||equal8(p,"/System/Windows/Tools/cmd.exe")||equal8(p,"/System/Windows/Tools/xcopy.exe")
  ||(installer_authority147()&&(installer_catalog_read1410(p)||installer_user_grant147(p,0)))
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

/* Related-product checks only stat a foreign pending transaction. */
static unsigned path_content1410(const char*p){
 if(!path8(p,0))return 0;
#ifdef ENGINE_M14
 if(!prefix8(p,input8.product_root)&&installer_catalog_read1410(p)==2)return 0;
#endif
 return 1;
}
