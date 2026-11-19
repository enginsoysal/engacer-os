/* Path queries do not create directories; unique temporary files use CREATE_NEW. */
static unsigned MS f_GetTempPathW(unsigned capacity,WCHAR*out){
 if(capacity&&!out){last8(87);return 0;}WCHAR selected[512],path[512];unsigned length=0;
 const WCHAR*names[]={u"TMP",u"TEMP",u"USERPROFILE"};for(unsigned i=0;i<3;++i){length=f_GetEnvironmentVariableW(names[i],selected,512);if(length>=512){last8(206);return 0;}if(length)break;}
 if(!length)widecopy8(selected,u"C:\\Windows\\",512);length=f_GetFullPathNameW(selected,512,path,0);if(!length)return 0;if(length>=512){last8(206);return 0;}
 if(path[length-1]!='\\')path[length++]='\\';path[length]=0;if(length>260){last8(206);return 0;}if(capacity>length)memcpy(out,path,(length+1)*2);return capacity>length?length:length+1;
}
static unsigned MS f_GetTempPathA(unsigned capacity,char*out){
 if((capacity&&!out)||capacity>INT32_MAX){last8(87);return 0;}WCHAR path[261];unsigned length=f_GetTempPathW(261,path);if(!length||length>=261)return 0;
 int bytes=f_WideCharToMultiByte(65001,0,path,-1,0,0,0,0);if(bytes<=0)return 0;if(capacity>=(unsigned)bytes)f_WideCharToMultiByte(65001,0,path,-1,out,(int)capacity,0,0);return capacity>=(unsigned)bytes?(unsigned)bytes-1:(unsigned)bytes;
}
static lock142 temporary_lock143;static unsigned temporary_sequence143;
static unsigned MS f_GetTempFileNameW(const WCHAR*directory,const WCHAR*prefix,unsigned unique,WCHAR*out){
 if(!directory||!prefix||!out){last8(87);return 0;}unsigned dn=0,pn=0,error=environment_length143(directory,512,&dn);if(!error)error=environment_length143(prefix,256,&pn);if(error){last8(error);return 0;}if(dn>246){last8(111);return 0;}
 WCHAR folder[512],begin[8];unsigned fn=f_GetFullPathNameW(directory,512,folder,0);if(!fn)return 0;if(fn>=512){last8(206);return 0;}
 unsigned copied=0,characters=0;while(copied<pn&&characters<3){WCHAR ch=prefix[copied];begin[copied]=ch;++copied;if(ch>=0xd800&&ch<=0xdbff){begin[copied]=prefix[copied];++copied;}++characters;}
 static const WCHAR hex[]=u"0123456789ABCDEF";for(unsigned attempt=0;attempt<1024;++attempt){unsigned number=unique;
  if(!unique){lock_enter142(&temporary_lock143);if(!temporary_sequence143)temporary_sequence143=(unsigned)sys8(W8_SYS_TIME,0,0,0,0,0)^job8->process_id;number=++temporary_sequence143&65535;if(!number)number=++temporary_sequence143&65535;lock_leave142(&temporary_lock143);}
  WCHAR name[260];unsigned used=fn;if(used+1+copied+8>=260){last8(206);return 0;}memcpy(name,folder,used*2);if(used&&name[used-1]!='\\')name[used++]='\\';memcpy(name+used,begin,copied*2);used+=copied;
  for(unsigned i=0;i<4;++i)name[used++]=hex[(number>>(12-i*4))&15];memcpy(name+used,u".TMP",10);used+=4;
  if(unique){memcpy(out,name,(used+1)*2);return unique;}
  HANDLE file=f_CreateFileW(name,0x40000000u,0,0,1,128,0);if(file==UINT64_MAX){if(f_GetLastError()==80)continue;return 0;}if(file_api143(file,7,0,0)<0)return 0;memcpy(out,name,(used+1)*2);return number;
 }last8(80);return 0;
}
static unsigned MS f_GetTempFileNameA(const char*directory,const char*prefix,unsigned unique,char*out){
 if(!directory||!prefix||!out){last8(87);return 0;}WCHAR folder[512],start[256],name[260];if(!f_MultiByteToWideChar(65001,8,directory,-1,folder,512)||!f_MultiByteToWideChar(65001,8,prefix,-1,start,256))return 0;
 unsigned result=f_GetTempFileNameW(folder,start,unique?unique:1,name);if(!result)return 0;int bytes=f_WideCharToMultiByte(65001,0,name,-1,0,0,0,0);if(bytes<=0)return 0;if(bytes>260){last8(111);return 0;}
 if(!unique){result=f_GetTempFileNameW(folder,start,0,name);if(!result)return 0;}if(!f_WideCharToMultiByte(65001,0,name,-1,out,260,0,0))return 0;return result;
}
