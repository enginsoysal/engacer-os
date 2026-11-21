/* Bounded silent permanent deletion through ordinary checked file APIs.
 * Recycling, connected shell objects, callbacks and interactive UI are unsupported. */
typedef struct {HANDLE window;unsigned operation,pad;const WCHAR*from,*to;uint16_t flags,pad2;int aborted;void*mappings;const WCHAR*title;} shell_fileop148;
_Static_assert(sizeof(shell_fileop148)==56,"AMD64 SHFILEOPSTRUCTW");
static unsigned shell_delete_files148(WCHAR*path,unsigned length,unsigned depth,unsigned*budget){
 if(depth>=12||!*budget)return 4;--*budget;unsigned attributes=f_GetFileAttributesW(path);if(attributes==UINT32_MAX)return shell_file_error148();
 if(attributes&0x400)return 50;
 if(!(attributes&16))return f_DeleteFileW(path)?0:shell_file_error148();
 if(length+3>=260)return 206;path[length]='\\';path[length+1]='*';path[length+2]=0;
 uint64_t storage[74];HANDLE search=f_FindFirstFileW(path,storage);path[length]=0;unsigned status=0;
 if(search==UINT64_MAX){status=f_GetLastError();if(status==2)status=0;}
 else{for(;;){WCHAR*name=(WCHAR*)((uint8_t*)storage+44);unsigned n=0;while(n<260&&name[n])++n;
   if(n==260){status=206;break;}if(n&&!(name[0]=='.'&&(!name[1]||(name[1]=='.'&&!name[2])))){
    if(length+n+2>260){status=206;break;}path[length]='\\';memcpy(path+length+1,name,(n+1)*2);status=shell_delete_files148(path,length+1+n,depth+1,budget);path[length]=0;if(status)break;
   }
   if(!f_FindNextFileW(search,storage)){status=f_GetLastError();if(status==18)status=0;break;}
  }if(!f_FindClose(search)&&!status)status=shell_file_error148();}
 if(status)return status;return f_RemoveDirectoryW(path)?0:shell_file_error148();
}
static int MS f_SHFileOperationW(shell_fileop148*operation){
 if(!shell_access148(operation,sizeof(*operation),1))return 87;shell_fileop148 request=*operation;operation->aborted=1;
 if(request.operation!=3||request.to||request.mappings||(request.flags&~0x614u)||(request.flags&0x614u)!=0x614u)return 50;
 WCHAR paths[512];unsigned used=0,previous=1,terminated=0;
 if(!request.from)return 87;for(;used<512;++used){if(!shell_access148(request.from+used,2,0))return 998;WCHAR ch=request.from[used];paths[used]=ch;if(!ch&&!previous){++used;terminated=1;break;}previous=ch;}
 if(!terminated||used<3)return 87;unsigned at=0,count=0;
 /* Validate every path before the first side effect. */
 while(at+1<used&&paths[at]){unsigned start=at;while(paths[at]){if(paths[at]=='*'||paths[at]=='?')return 50;++at;}unsigned n=at-start;if(++count>16||n>=260||n<4||paths[start+1]!=':'||paths[start+2]!='\\')return 87;++at;}
 unsigned budget=1024;at=0;while(at+1<used&&paths[at]){WCHAR path[260];unsigned n=0;while(paths[at])path[n++]=paths[at++];path[n]=0;++at;unsigned status=shell_delete_files148(path,n,0,&budget);if(status)return(int)status;}
 operation->aborted=0;return 0;
}
