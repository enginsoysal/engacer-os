/* Read-only source review. Original EXE execution still requires kernel admission. */
#include "runtime.h"
#include <engine/sha256.h>
#include <engine/winexe148.h>
static unsigned extension148(const char*path){unsigned n=len8(path);if(n<4||path[n-4]!='.')return 0;const char*e=path+n-3;return(e[0]=='e'||e[0]=='E')&&(e[1]=='x'||e[1]=='X')&&(e[2]=='e'||e[2]=='E');}
unsigned exe148_source(const char*path){return extension148(path);}
void exe148_review(void){
 w8_file_info before,after;if(stat8(job8->source,&before)||before.kind!=1||!before.size||before.size>64u*1024*1024)fail8("Choose an available EXE installer up to 64 MiB. No files were changed.");
 int file=open8(job8->source,0);if(file<0)fail8("The original EXE installer could not be opened. No files were changed.");
 engine_sha256_context hash;engine_sha256_init(&hash);uint8_t block[4096],digest[32];uint64_t at=0;unsigned valid=1;
 while(at<before.size){unsigned bytes=before.size-at>sizeof(block)?sizeof(block):(unsigned)(before.size-at);int got=read8(file,block,bytes);if(got!=(int)bytes||!engine_sha256_update(&hash,block,bytes)){valid=0;break;}at+=bytes;if(!(at&65535u))progress8((unsigned)(at*90/before.size),"Reviewing the original EXE installer. No installation changes yet.");}
 if(close8(file))valid=0;if(!engine_sha256_final(&hash,digest))valid=0;
 if(!valid||stat8(job8->source,&after)||before.size!=after.size||before.crc!=after.crc||before.identity!=after.identity)fail8("The installer changed or could not be read completely. Review it again.");
 memcpy(job8->source_sha147,digest,32);job8->profile147=0;
 if(before.size!=EXE148_SOURCE_BYTES||!exe_digest148(digest,EXE148_SOURCE_SHA)){copy8(job8->product,"EXE installer",96);progress8(100,"Source reviewed. Installation of this EXE is not enabled yet; no files were installed.");return;}
 copy8(job8->product,"SumatraPDF",96);copy8(job8->version,"3.6.1",32);copy8(job8->publisher,"Krzysztof Kowalczyk",96);copy8(job8->code,EXE148_CODE,40);job8->files=4;job8->registry=227;job8->shortcuts=2;job8->features=1;job8->total_bytes=0;
 for(unsigned i=0;i<4;++i)job8->total_bytes+=exe_payloads148[i].bytes;
 job8->profile147=W8_PROFILE_EXE148;
 progress8(100,"Original x64 EXE reviewed. Confirm installation to run its original setup. No files were installed during review.");
}
void exe148_execute(void){
 int64_t context=(int64_t)sys8(W8_SYS_EXE148,0,0,0,0,0);if(context!=1&&context!=2)fail8("This EXE has no kernel-owned installation admission. No original code was started.");
 int64_t error=(int64_t)sys8(W8_SYS_EXE148,1,0,0,0,0);if(error){print8("EXE preparation error: ");number8((uint64_t)-error);fail8("The installation record or destination could not be prepared. Files were kept.");}
 init_win8();w8_process_request request;memset(&request,0,sizeof(request));copy8(request.source,job8->source,256);copy8(request.directory,job8->user_root,256);append8(request.directory,"/Documents",256);
 char windows[512];if(context==2){copy8(windows,EXE148_ALIAS,512);append8(windows,"\\SumatraPDF.exe",512);}else{copy8(windows,"C:",512);append8(windows,job8->source,512);for(unsigned i=2;windows[i];++i)if(windows[i]=='/')windows[i]='\\';}
 copy8(request.command,"\"",1200);append8(request.command,windows,1200);append8(request.command,context==1?"\" -install -d \"" EXE148_ALIAS "\"":"\" -uninstall",1200);
 progress8(10,context==1?"Use the original installer window. Close it when installation has finished.":"Use the original uninstaller window. Close it when removal has finished.");
 w8_process_result result;memset(&result,0,sizeof(result));error=(int64_t)sys8(W8_SYS_PROCESS_CREATE,(uint64_t)(uintptr_t)&request,(uint64_t)(uintptr_t)&result,0,0,0);if(error){print8("Original launch error: ");number8((uint64_t)-error);fail8("The original installer could not start. Its record was kept for inspection.");}
 while((error=(int64_t)sys8(W8_SYS_EXE148,4,0,0,0,0))==0){}if(error<0)fail8("The original process group could not be observed.");
 (void)sys8(W8_SYS_PROCESS_CLOSE,result.thread,0,0,0,0);(void)sys8(W8_SYS_PROCESS_CLOSE,result.process,0,0,0,0);
 progress8(95,"Checking actual original application effects.");error=(int64_t)sys8(W8_SYS_EXE148,context==1?2:3,0,0,0,0);if(error){print8("Original effect verification error: ");number8((uint64_t)-error);fail8("The original operation did not pass verification. Files and its record were kept; success is not claimed.");}
 copy8(job8->product,"SumatraPDF",96);copy8(job8->version,"3.6.1",32);copy8(job8->publisher,"Krzysztof Kowalczyk",96);copy8(job8->code,EXE148_CODE,40);job8->profile147=W8_PROFILE_EXE148;
 print8(context==1?"M148_ORDINARY_ORIGINAL_INSTALL_VERIFIED\n":"M148_ORDINARY_ORIGINAL_REMOVE_VERIFIED\n");progress8(100,context==1?"Original installation verified. The PDF reader itself is not qualified in this release.":"Original removal verified. Your other files were preserved.");
}
