/* Engacer's own bounded file-copy/delete utilities for native installers. */
#include "tools147.h"
__declspec(dllimport) const uint16_t*GetCommandLineW(void);
__declspec(dllimport) uint64_t GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(uint64_t,const void*,unsigned,unsigned*,void*);
__declspec(dllimport) int ReadFile(uint64_t,void*,unsigned,unsigned*,void*);
__declspec(dllimport) uint64_t CreateFileW(const uint16_t*,unsigned,unsigned,void*,unsigned,unsigned,uint64_t);
__declspec(dllimport) unsigned GetFileAttributesW(const uint16_t*);
__declspec(dllimport) int SetFileAttributesW(const uint16_t*,unsigned);
__declspec(dllimport) int DeleteFileW(const uint16_t*);
__declspec(dllimport) int CloseHandle(uint64_t);
__declspec(dllimport) unsigned GetLastError(void);
__declspec(dllimport) void ExitProcess(unsigned);
__declspec(dllimport) void Sleep(unsigned);
__declspec(dllimport) int MultiByteToWideChar(unsigned,unsigned,const char*,int,uint16_t*,int);
void entry(void);void*volatile tool_anchor147=&entry;
static void tool_print147(unsigned stream,const char*text){unsigned n=0;while(text[n])++n;unsigned done=0;(void)WriteFile(GetStdHandle(stream),text,n,&done,0);}
static unsigned tool_error147(const char*text,unsigned code,unsigned status){tool_print147((unsigned)-12,text);char number[16],reverse[16];unsigned n=0,at=0;do{reverse[n++]=(char)('0'+code%10);code/=10;}while(code);while(n)number[at++]=reverse[--n];number[at]=0;tool_print147((unsigned)-12,number);tool_print147((unsigned)-12,").\r\n");return status;}
#if TOOL147_KIND==1
static unsigned run147(unsigned count,uint16_t**argv){
 const uint16_t*source=0,*destination=0;unsigned overwrite=0,quiet=0;
 for(unsigned i=1;i<count;++i){if(tool_equal147(argv[i],L"/Y"))overwrite=1;else if(tool_equal147(argv[i],L"/Q"))quiet=1;else if(argv[i][0]=='/'||destination)return tool_error147("Unsupported copy arguments (Windows error ",50,4);else if(!source)source=argv[i];else destination=argv[i];}
 if(!source||!destination||!overwrite||!quiet)return tool_error147("Use xcopy SOURCE DESTINATION /Y /Q (Windows error ",87,4);uint16_t target[512];if(!tool_destination147(source,destination,target,512))return tool_error147("Unsupported copy filename pattern (Windows error ",50,4);
 unsigned source_attributes=GetFileAttributesW(source);if(source_attributes==UINT32_MAX){unsigned error=GetLastError();return tool_error147("The source could not be opened (Windows error ",error,error==2||error==3?1:4);}if(source_attributes&0x10u)return tool_error147("Directory copies are not supported by this utility profile (Windows error ",50,4);
 unsigned attributes=GetFileAttributesW(target);if(attributes!=UINT32_MAX&&(attributes&0x10u)){unsigned at=tool_length147(target),base=tool_length147(source);while(base&&source[base-1]!='\\'&&source[base-1]!='/')--base;unsigned suffix=tool_length147(source+base);if(at+suffix+2>512)return tool_error147("The destination is too long (Windows error ",206,4);if(at&&target[at-1]!='\\'&&target[at-1]!='/')target[at++]='\\';for(unsigned i=0;i<=suffix;++i)target[at+i]=source[base+i];}
 uint64_t input=CreateFileW(source,0x80000000u,1,0,3,0x80,0);if(input==UINT64_MAX)return tool_error147("The source could not be opened (Windows error ",GetLastError(),4);uint64_t output=CreateFileW(target,0x40000000u,0,0,2,0x80,0);if(output==UINT64_MAX){unsigned error=GetLastError();CloseHandle(input);return tool_error147("The destination could not be created (Windows error ",error,5);}
 uint8_t buffer[4096];unsigned status=0,error=0;
 for(;;){unsigned bytes=0;if(!ReadFile(input,buffer,sizeof(buffer),&bytes,0)||bytes>sizeof(buffer)){status=4;error=GetLastError();break;}if(!bytes)break;unsigned at=0;while(at<bytes){unsigned wrote=0;if(!WriteFile(output,buffer+at,bytes-at,&wrote,0)||!wrote||wrote>bytes-at){status=5;error=GetLastError();break;}at+=wrote;}if(status)break;}
 if(!CloseHandle(input)&&!status){status=4;error=GetLastError();}if(!CloseHandle(output)&&!status){status=5;error=GetLastError();}if(status)return tool_error147("File copy did not finish (Windows error ",error,status);tool_print147((unsigned)-11,"1 File(s) copied\r\n");return 0;
}
#elif TOOL147_KIND==2
#include "batch148.h"
static unsigned batch_delete148(unsigned count,uint16_t**argv){unsigned force=0;const uint16_t*path=0;for(unsigned i=1;i<count;++i){if(tool_equal147(argv[i],L"/F"))force=1;else if(tool_equal147(argv[i],L"/Q")){}else if(path||argv[i][0]=='/')return 50;else path=argv[i];}if(!path||tool_wild147(path))return 50;unsigned attr=GetFileAttributesW(path);if(attr==UINT32_MAX)return GetLastError();if(attr&0x10u)return 5;if(force&&(attr&1u)&&!SetFileAttributesW(path,attr&~1u))return GetLastError();return DeleteFileW(path)?0:GetLastError();}
static unsigned batch_run148(const uint16_t*path){
 if(tool_wild147(path))return 50;uint64_t file=CreateFileW(path,0x80000000u,1,0,3,0x80,0);if(file==UINT64_MAX)return GetLastError();char bytes[16385];unsigned size=0,part=0,error=0;
 while(size<sizeof(bytes)){if(!ReadFile(file,bytes+size,(unsigned)sizeof(bytes)-size,&part,0)){error=GetLastError();break;}if(!part)break;size+=part;}if(!CloseHandle(file)&&!error)error=GetLastError();if(error)return error;if(size==sizeof(bytes))return 1816;
 uint16_t script[16385];int units=MultiByteToWideChar(65001,8,bytes,(int)size,script,16384);if(units<=0)return GetLastError();script[units]=0;
 unsigned at=0,status=0,lines=0;while(at<(unsigned)units){if(++lines>128)return 1816;uint16_t line[2048];unsigned used=0;while(at<(unsigned)units&&script[at]!='\n'){if(used+1>=2048)return 1816;if(script[at]!='\r')line[used++]=script[at];++at;}if(at<(unsigned)units)++at;line[used]=0;unsigned offset=0;
  while(line[offset]){uint16_t segment[2048],storage[2048],*argv[16];int result=batch_segment148(line,&offset,path,segment,2048);if(result<0)return(unsigned)-result;if(!result)break;int count=tool_parse147(segment,storage,2048,argv,16,1);if(count<0)return(unsigned)-count;if(!count)continue;
   if(tool_equal147(argv[0],L"rem")||tool_equal147(argv[0],L"::"))continue;
   if(tool_equal147(argv[0],L"timeout")){if(count!=4||!tool_equal147(argv[1],L"/T")||!tool_equal147(argv[3],L"/NOBREAK"))return 50;unsigned seconds=0;for(unsigned i=0;argv[2][i];++i){if(argv[2][i]<'0'||argv[2][i]>'9'||seconds>60)return 87;seconds=seconds*10+argv[2][i]-'0';}if(!argv[2][0]||seconds>60)return 87;Sleep(seconds*1000);status=0;}
   else if(tool_equal147(argv[0],L"del")){status=batch_delete148((unsigned)count,argv);if(status)return status;}
   else if(tool_equal147(argv[0],L"(goto)")&&count==1){/* A missing label fails the group; '&' still runs the next command. */status=1;}
   else if(tool_equal147(argv[0],L"echo")&&count==2&&tool_equal147(argv[1],L"off"))status=0;
   else return 50;
  }
 }return status;
}
static unsigned run147(unsigned count,uint16_t**argv){unsigned at=1;if(at<count&&tool_equal147(argv[at],L"/D"))++at;if(at<count&&tool_equal147(argv[at],L"/C")&&at+2==count){unsigned n=tool_length147(argv[at+1]);if(n>=4&&tool_equal147(argv[at+1]+n-4,L".bat")){unsigned status=batch_run148(argv[at+1]);return status?tool_error147("Batch operation failed (Windows error ",status,1):0;}}if(at>=count||!tool_equal147(argv[at++],L"/C")||at>=count||!tool_equal147(argv[at++],L"del"))return tool_error147("This command profile supports /C del /F /Q FILE (Windows error ",50,1);unsigned force=0,quiet=0;const uint16_t*path=0;
 for(;at<count;++at){if(tool_equal147(argv[at],L"/F"))force=1;else if(tool_equal147(argv[at],L"/Q"))quiet=1;else if(argv[at][0]=='/'||path)return tool_error147("Unsupported delete arguments (Windows error ",50,1);else path=argv[at];}
 if(!path||!force||!quiet||tool_wild147(path))return tool_error147("This command profile requires one file, /F and /Q (Windows error ",50,1);unsigned attributes=GetFileAttributesW(path);if(attributes==UINT32_MAX){unsigned error=GetLastError();if(error==2||error==3){tool_print147((unsigned)-12,"The file was not found.\r\n");return 0;}return tool_error147("The file could not be inspected (Windows error ",error,1);}if(attributes&0x10u)return tool_error147("A directory cannot be deleted by this command (Windows error ",5,1);if((attributes&1u)&&!SetFileAttributesW(path,attributes&~1u))return tool_error147("The read-only attribute could not be cleared (Windows error ",GetLastError(),1);if(!DeleteFileW(path))return tool_error147("The file could not be deleted (Windows error ",GetLastError(),1);return 0;
}
#else
#error Select a native utility kind
#endif
void entry(void){uint16_t storage[2048],*argv[16];int count=tool_parse147(GetCommandLineW(),storage,2048,argv,16,TOOL147_KIND==2);if(count<1)ExitProcess(tool_error147("The command line is outside the supported utility profile (Windows error ",(unsigned)(count<0?-count:87),TOOL147_KIND==1?4:1));ExitProcess(run147((unsigned)count,argv));}
