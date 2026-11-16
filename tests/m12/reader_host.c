/* Run the production FAT32 reader against a read-only owned image, not a model. */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#define ENGINE_M92
#define ENGINE_M10
#define ENGINE_M12
#ifndef FAT32_SOURCE12
#define FAT32_SOURCE12 "../../kernel/storage/fat32.c"
#endif
#include FAT32_SOURCE12

static FILE*image12;
static storage_disk disk12;
static uint64_t single12,bulk12,large12,bytes12,mirror12,fat_start12,fat_size12;
static unsigned corrupt12,fail12;
const storage_disk*storage_get(unsigned disk){return disk==0?&disk12:0;}
unsigned storage_partition(unsigned a,unsigned b,uint64_t*c,uint64_t*d){(void)a;(void)b;(void)c;(void)d;return B_DENIED;}
static unsigned host_read12(uint64_t lba,void*data,unsigned bytes){
 if(fail12||lba>=disk12.sectors||bytes/512>disk12.sectors-lba)return B_IO;
 assert(!_fseeki64(image12,(__int64)(lba*512),SEEK_SET));assert(fread(data,1,bytes,image12)==bytes);bytes12+=bytes;
 if(lba>=fat_start12+fat_size12&&lba<fat_start12+fat_size12*2){++mirror12;if(corrupt12)((uint8_t*)data)[0]^=1;}
 return B_OK;
}
unsigned storage_read(unsigned disk,uint64_t lba,void*data){assert(disk==0);++single12;return host_read12(lba,data,512);}
unsigned storage_transfer(unsigned disk,uint64_t lba,void*data,unsigned bytes,unsigned write){assert(disk==0&&!write&&bytes&&bytes<=4096&&bytes%512==0);++bulk12;large12+=bytes>512;return host_read12(lba,data,bytes);}
unsigned storage_flush(unsigned disk){(void)disk;abort();}
unsigned storage_can_write(const storage_disk*d){(void)d;return 0;}
void console_text(const char*s){(void)s;abort();}
void console_decimal(uint64_t n){(void)n;abort();}
v6_volume*m6_volume(void){abort();}
unsigned v6_verify(v6_volume*v,const char*p){(void)v;(void)p;abort();}
unsigned v6_read(v6_volume*v,const char*p,uint64_t o,void*d,unsigned n,unsigned*g){(void)v;(void)p;(void)o;(void)d;(void)n;(void)g;abort();}
unsigned v6_put(v6_volume*v,const char*p,uint64_t n,v6_source s,void*c){(void)v;(void)p;(void)n;(void)s;(void)c;abort();}

static void pattern12(const char*path,uint64_t expected,unsigned varied){
 uint64_t size=0;assert(rem12_read_begin(0,disk12.context,UINT32_MAX,path,&size)==B_OK&&size==expected);
 assert(rem12_read_begin(0,disk12.context,UINT32_MAX,path,&size)==B_DENIED);
 const unsigned choices[]={1,511,4095,4096,1537,512};uint8_t buffer[4096];uint64_t offset=0;unsigned index=0;
 while(offset<size){unsigned bytes=varied?choices[index++%6]:4096;if(bytes>size-offset)bytes=(unsigned)(size-offset);assert(rem12_read_next(buffer,bytes)==B_OK);for(unsigned i=0;i<bytes;++i)assert(buffer[i]==(uint8_t)(offset+i));offset+=bytes;}
 assert(rem12_read_next(buffer,1)!=B_OK);rem12_read_close();
}
int main(int argc,char**argv){
 assert(argc==2);assert(!fopen_s(&image12,argv[1],"rb"));assert(image12);assert(!_fseeki64(image12,0,SEEK_END));disk12=(storage_disk){.transport=STORAGE_USB,.sector_bytes=512,.readable=1,.sectors=(uint64_t)_ftelli64(image12)/512,.context=7};
 uint8_t boot[512];assert(host_read12(0,boot,512)==B_OK);fat_start12=r16(boot+14);fat_size12=r32(boot+36);
 pattern12("/Large.bin",64u*1024*1024,0);uint64_t full_single=single12,full_bulk=bulk12,full_large=large12,full_mirror=mirror12;
#ifdef READER_BASELINE12
 assert(!full_bulk&&!full_large&&full_single>131072);fclose(image12);printf("{\"passed\":true,\"full_bytes\":67108864,\"full_single_sector_reads\":%llu,\"full_data_commands\":0,\"full_mirror_reads\":%llu}\n",(unsigned long long)full_single,(unsigned long long)full_mirror);return 0;
#else
 assert(full_bulk<=16384&&full_large>0&&full_single<20000&&full_mirror<10000);
 uint64_t fragment_size=0;assert(rem12_read_begin(0,7,UINT32_MAX,"/Fragment.bin",&fragment_size)==B_OK);unsigned cluster=reader12.cluster,fragmented=0;
 for(unsigned i=0;i<32&&cluster;++i){unsigned next=0;assert(reader_cluster_next12(cluster,&next)==B_OK);if(next&&next!=cluster+1)fragmented=1;cluster=next;}
 assert(fragmented);rem12_read_close();pattern12("/Fragment.bin",256u*1024,1);pattern12("/Odd.bin",12345,1);
 uint64_t size=0;uint8_t data[4096];assert(rem12_read_begin(0,7,UINT32_MAX,"/Large.bin",&size)==B_OK);assert(rem12_read_next(data,4096)==B_OK);disk12.context=8;assert(rem12_read_next(data,4096)==B_ABSENT);assert(!reader_active12&&reader_fat_mask12==0);
 assert(rem12_read_begin(0,7,UINT32_MAX,"/Large.bin",&size)==B_ABSENT);assert(rem12_read_begin(0,8,UINT32_MAX,"/Large.bin",&size)==B_OK);assert(rem12_read_next(data,4096)==B_OK);rem12_read_close();
 corrupt12=1;assert(rem12_read_begin(0,8,UINT32_MAX,"/Large.bin",&size)==B_OK);assert(rem12_read_next(data,4096)!=B_OK);assert(!reader_active12);corrupt12=0;
 assert(rem12_read_begin(0,8,UINT32_MAX,"/Large.bin",&size)==B_OK);assert(rem12_read_next(data,4096)==B_OK);fail12=1;assert(rem12_read_next(data,4096)==B_IO);assert(!reader_active12);fail12=0;
 pattern12("/Odd.bin",12345,1);assert(rem12_read_begin(0,8,UINT32_MAX,"/Empty.bin",&size)==B_OK&&size==0);assert(rem12_read_next(data,1)==B_DENIED);rem12_read_close();
 assert(rem12_read_begin(0,8,UINT32_MAX,"/Large.bin",0)==B_DENIED);assert(rem12_read_next(0,4096)==B_DENIED);
 fclose(image12);printf("{\"passed\":true,\"full_bytes\":67108864,\"full_single_sector_reads\":%llu,\"full_data_commands\":%llu,\"multi_sector_commands\":%llu,\"full_mirror_reads\":%llu,\"metadata_cache_bytes\":%zu,\"checks\":[\"production 64-MiB contiguous bytes\",\"real fragmented chain bytes\",\"unaligned and odd reads\",\"generation change and replacement\",\"mirror mismatch and failed data read\",\"fresh lease after error\",\"empty file and argument/EOF bounds\"],\"writes\":0}\n",(unsigned long long)full_single,(unsigned long long)full_bulk,(unsigned long long)full_large,(unsigned long long)full_mirror,sizeof(reader_fat12)+sizeof(reader_fat_index12)+sizeof(reader_fat_mask12)+sizeof(reader_fat_next12));return 0;
#endif
}
