/* Native child startup is brokered by the kernel, never a host/guest OS launch. */
typedef struct {unsigned size,pad;uint64_t reserved,desktop,title;unsigned x,y,width,height,columns,rows,fill,flags;uint16_t show,reserved_bytes;unsigned pad2;uint64_t reserved_data,input,output,error;} startup142;
_Static_assert(sizeof(startup142)==104,"Win64 STARTUPINFO layout");
_Static_assert(sizeof(w8_process_result)==24,"Win64 PROCESS_INFORMATION layout");
static int first_executable142(const WCHAR*command,WCHAR*out,unsigned cap){unsigned at=0,n=0,quoted=0;if(!command)return 0;while(command[at]==' '||command[at]=='\t')++at;if(command[at]=='"'){quoted=1;++at;}
 while(command[at]){WCHAR c=command[at++];if((quoted&&c=='"')||(!quoted&&(c==' '||c=='\t')))break;if(n+1>=cap)return 0;out[n++]=c;}out[n]=0;return n!=0;
}
static int MS f_CreateProcessW(const WCHAR*application,WCHAR*command,void*process_security,void*thread_security,int inherit,unsigned flags,void*environment,const WCHAR*directory,startup142*startup,w8_process_result*result){
 if(!result||!startup||startup->size!=sizeof(*startup)||(!application&&!command)){last8(87);return 0;}memset(result,0,sizeof(*result));
 if(process_security||thread_security||(flags&~W8_CREATE_FLAGS147)||startup->reserved||startup->desktop||startup->title||startup->reserved_bytes||startup->reserved_data){last8(50);return 0;}
#ifdef ENGINE_M14
 if((startup->flags&~0x100u)){last8(50);return 0;}
#else
 if(inherit||startup->flags){last8(50);return 0;}
#endif
 w8_process_request request;memset(&request,0,sizeof(request));request.flags=flags;
#ifdef ENGINE_M14
 request.inherit147=inherit!=0;request.startup_flags147=startup->flags;request.std_handles147[0]=startup->input;request.std_handles147[1]=startup->output;request.std_handles147[2]=startup->error;
#endif
 WCHAR executable[256];const WCHAR*name=application;
 if(!name){if(!first_executable142(command,executable,256)){last8(87);return 0;}name=executable;}
 if(!*name){last8(2);return 0;}if(utf16_to8(command?command:name,request.command,sizeof(request.command))<0){last8(206);return 0;}
 unsigned relative=1,dot=0;for(unsigned i=0;name[i];++i)if(name[i]=='/'||name[i]=='\\'||name[i]==':')relative=0;
 if(!application&&relative){widecopy8(executable,name,256);unsigned n=wlen8(executable);for(unsigned i=0;i<n;++i)if(executable[i]=='.')dot=1;if(!dot){if(n+5>=256){last8(206);return 0;}executable[n++]='.';executable[n++]='e';executable[n++]='x';executable[n++]='e';executable[n]=0;}name=executable;
  char leaf[256];if(utf16_to8(name,leaf,256)<0){last8(206);return 0;}copy8(request.source,job8->source,256);char*end=request.source+len8(request.source);while(end>request.source&&end[-1]!='/')--end;*end=0;append8(request.source,leaf,256);w8_file_info info;if(stat8(request.source,&info)||info.kind!=1)request.source[0]=0;
 }
 if(!request.source[0]&&!nativepath8(name,request.source)){last8(5);return 0;}
 WCHAR working[512];if(!directory){lock_enter142(&cwd_lock143);widecopy8(working,cwd8,512);lock_leave142(&cwd_lock143);}if(!nativepath8(directory?directory:working,request.directory))return 0;
 unsigned environment_bytes=0;WCHAR*snapshot=environment_snapshot143(environment,flags,&environment_bytes);if(!snapshot)return 0;request.environment=(uint64_t)(uintptr_t)snapshot;request.environment_bytes=environment_bytes;
 int64_t status=(int64_t)sys8(W8_SYS_PROCESS_CREATE,(uint64_t)(uintptr_t)&request,(uint64_t)(uintptr_t)result,0,0,0);
 if(environment)free8(snapshot);else f_FreeEnvironmentStringsW(snapshot);
 if(status<0){last8((unsigned)-status);return 0;}last8(0);return 1;
}
static int MS f_CreateProcessA(const char*application,char*command,void*process_security,void*thread_security,int inherit,unsigned flags,void*environment,const char*directory,startup142*startup,w8_process_result*result){
 WCHAR app[256],line[1200],cwd[256];if((application&&utf8_to16(application,app,256)<0)||(command&&utf8_to16(command,line,1200)<0)||(directory&&utf8_to16(directory,cwd,256)<0)){last8(206);return 0;}
 return f_CreateProcessW(application?app:0,command?line:0,process_security,thread_security,inherit,flags,environment,directory?cwd:0,startup,result);
}
static int MS f_GetExitCodeProcess(HANDLE handle,unsigned*code){if(!code){last8(87);return 0;}int64_t state=(int64_t)sys8(W8_SYS_PROCESS_STATUS,handle,(uint64_t)(uintptr_t)code,1,0,0);if(state<0){last8(6);return 0;}if(state==259)*code=259;return 1;}
static unsigned MS f_GetProcessId(HANDLE handle){int64_t id=(int64_t)sys8(W8_SYS_PROCESS_ID,handle,0,0,0,0);if(id<0){last8(6);return 0;}return (unsigned)id;}
static int MS f_TerminateProcess(HANDLE handle,unsigned code){int64_t status=(int64_t)sys8(W8_SYS_PROCESS_TERMINATE,handle,code,0,0,0);if(status<0){last8(6);return 0;}return 1;}
static void MS f_GetStartupInfoW(startup142*startup){if(startup){memset(startup,0,sizeof(*startup));startup->size=sizeof(*startup);startup->input=1;startup->output=2;startup->error=3;
#ifdef ENGINE_M14
 startup->flags=job8->startup_flags147;if(startup->flags&0x100u){startup->input=job8->std_handles147[0];startup->output=job8->std_handles147[1];startup->error=job8->std_handles147[2];}
#endif
 }}
static void MS f_GetStartupInfoA(startup142*startup){f_GetStartupInfoW(startup);}
