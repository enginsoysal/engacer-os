/* Test-only worker replacement. It never claims an original MSI installation. */
#include "../../user/windows8/runtime.h"
#include <engine/wintxn147.h>
static uint8_t block147[4096],journal147[sizeof(win_tx_header147)+sizeof(win_tx_record147)+sizeof(win_tx_file147)];
static void path147(char out[256],const char*tail){copy8(out,job8->product_root,256);append8(out,tail,256);}
static int64_t stream147(unsigned op,const void*data,uint64_t bytes){return (int64_t)sys8(W8_SYS_STREAM147,op,(uint64_t)(uintptr_t)data,bytes,0,0);}
static void check147(int okay,const char*message){if(!okay)fail8(message);}
static void hash_file147(const char*path,unsigned bytes,uint8_t hash[32]){int h=open8(path,0);check147(h>=0,"Fixture file read failed.");engine_sha256_context c;engine_sha256_init(&c);for(unsigned at=0;at<bytes;){unsigned n=bytes-at;if(n>sizeof(block147))n=sizeof(block147);check147(read8(h,block147,n)==(int)n&&engine_sha256_update(&c,block147,n),"Fixture stored bytes could not be read.");at+=n;}check147(!close8(h)&&engine_sha256_final(&c,hash),"Fixture hash close failed.");}
void msi8_execute(void){
 check147(job8->command==W8_INSTALL,"This test fixture only accepts a confirmed native INSTALL job.");
 print8("M147_TEST_ONLY_STORAGE_WORKER; NOT ORIGINAL APPLICATION QUALIFICATION\n");
 void*mode_data=0;unsigned mode_bytes=load8("/Users/Owner/Documents/storage-mode147.txt",&mode_data,64);check147(mode_bytes>0,"Owned fixture mode is missing.");char mode[64];copy8(mode,mode_data,sizeof(mode));free8(mode_data);
 char private_dir[256],stage_dir[256],staged[256],target[256],pending[256];path147(private_dir,"/.EngacerMSI");path147(stage_dir,"/.EngacerMSI/stage");path147(staged,"/.EngacerMSI/stage/payload147.bin");path147(target,"/payload147.bin");path147(pending,"/.EngacerMSI/transaction.bin");
 check147((int64_t)sys8(W8_SYS_MKDIR,(uint64_t)(uintptr_t)job8->product_root,1,0,0,0)==0&&!mkdir8(private_dir)&&!mkdir8(stage_dir),"Owned primitive root creation failed.");
 const unsigned bytes=9u*1024u*1024u+17u;check147(stream147(1,staged,bytes)==0,"Native staged stream admission failed.");engine_sha256_context hash;engine_sha256_init(&hash);
 unsigned reported=0;for(unsigned at=0;at<bytes;){unsigned n=bytes-at;if(n>sizeof(block147))n=sizeof(block147);for(unsigned j=0;j<n;++j)block147[j]=(uint8_t)((at+j)*37+19);
  check147(stream147(2,block147,n)==0&&engine_sha256_update(&hash,block147,n),"Native staged payload write failed.");at+=n;
  if(equal8(mode,"cancel")&&at>=65536){progress8(30,"M147_STREAM_CANCEL_READY");volatile uint32_t parked=1;for(;;)sys8(W8_SYS_PARK,(uint64_t)(uintptr_t)&parked,1,UINT32_MAX,0,0);}
  if(at/524288!=reported){reported=at/524288;progress8(10+(unsigned)((uint64_t)at*40/bytes),"M147_NATIVE_STREAM_WRITING");}
 }
 uint8_t expected[32],actual[32];check147(engine_sha256_final(&hash,expected),"Fixture source hash failed.");w8_file_info info;check147(stat8(staged,&info)!=0,"An incomplete staged extent became visible.");check147(stream147(5,0,0)==-87,"Unverified publication was admitted.");check147(stream147(3,0,0)==0,"Native stream seal failed.");unsigned rounds=0;
 for(;;){int64_t done=stream147(4,0,0);check147(done==0||done==1,"Native stream readback failed.");++rounds;if(done)break;progress8(65,"M147_NATIVE_STREAM_VERIFYING");}
 check147(stream147(5,0,0)==0,"Verified native stream publication failed.");hash_file147(staged,bytes,actual);check147(!memcmp(actual,expected,32),"Native stream content differs from the independent generator.");
 memset(journal147,0,sizeof(journal147));win_tx_header147*h=(void*)journal147;h->magic=WIN_TX_MAGIC147;h->schema=1;h->bytes=sizeof(journal147);h->records=h->files=1;
 hash_file147(job8->source,2003456,h->source_sha);copy8(h->code,"{23170F69-40C1-2702-2606-000001000000}",40);copy8(h->user,job8->user_root,256);copy8(h->alias,job8->windows_root,256);copy8(h->product,"Native storage fixture",96);copy8(h->version,"1",32);copy8(h->publisher,"Engacer test",96);
 win_tx_record147*r=(void*)(journal147+sizeof(*h));r->type=WIN_TX_FILE147;r->bytes=sizeof(*r)+sizeof(win_tx_file147);win_tx_file147*f=(void*)(r+1);copy8(f->path,"payload147.bin",256);memcpy(f->sha,expected,32);f->bytes=bytes;f->flags=WIN_TX_PAYLOAD147;
 check147(win_tx_digest147(journal147,sizeof(journal147),h->checksum)&&win_tx_validate147(journal147,sizeof(journal147)),"Fixture recovery image failed production admission.");
 if(equal8(mode,"corrupt-journal"))h->checksum[0]^=1;
 check147(!save8(pending,journal147,sizeof(journal147)),"Fixture recovery image could not be saved.");
 if(equal8(mode,"journal-fail")||equal8(mode,"corrupt-journal")){print8("M147_EXPECTED_FAILURE_AFTER_JOURNAL\n");fail8("Intentional test-only failure after journal publication.");}
 check147((int64_t)sys8(W8_SYS_MOVE,(uint64_t)(uintptr_t)staged,(uint64_t)(uintptr_t)target,2,0,0)==0,"Native extent promotion failed.");hash_file147(target,bytes,actual);check147(!memcmp(actual,expected,32),"Promoted native payload differs.");
 check147(!remove8(target)&&!remove8(pending)&&!remove8(stage_dir)&&!remove8(private_dir)&&!remove8(job8->product_root),"Owned successful fixture cleanup failed.");
 print8("M147_NATIVE_STREAM_JOURNAL_PROMOTION_PASS rounds=");number8(rounds);print8("\n");progress8(100,"Native storage fixture passed; no application was installed.");
}
