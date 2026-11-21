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
 /* The route is deliberately disabled until source leases, effect validation
  * and removal are wired through a complete ordinary admission path. */
 progress8(100,"Original SumatraPDF x64 identified. EXE installation review is in development; no files were installed.");
}
