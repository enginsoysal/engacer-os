#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <engine/windows8.h>
#include <engine/storage/volume6.h>

#define NX (UINT64_C(1)<<63)
static uint8_t io8[4096],file_bytes[65536],arena[65536];
static uint64_t entries[16];
static v6_entry image_file;

static const v6_entry *find8(const char *path){return !strcmp(path,"fixture")?&image_file:NULL;}
static v6_volume *m6_volume(void){return NULL;}
unsigned v6_verify(v6_volume *volume,const char *path){(void)volume;return !find8(path);}
static unsigned exact8(const char *path,uint64_t off,void *out,unsigned bytes){
 if(!find8(path)||off>image_file.size||bytes>image_file.size-off)return 1;
 memcpy(out,file_bytes+off,bytes);return 0;
}
static unsigned user8(uint64_t address,void *data,unsigned bytes,unsigned write){
 if(address<0x41000000u||address>=0x41000000u+sizeof(arena)||
    bytes>0x41000000u+sizeof(arena)-address)return 1;
 unsigned offset=(unsigned)(address-0x41000000u);
 if(write)memcpy(arena+offset,data,bytes);else memcpy(data,arena+offset,bytes);
 return 0;
}
static unsigned map8(uint64_t base,uint64_t bytes,unsigned flags){
 if(base!=0x41000000u||bytes>sizeof(arena)||flags!=3)return 1;
 memset(arena,0,sizeof(arena));
 for(unsigned i=0;i<bytes/4096;++i)entries[i]=(uint64_t)(i+1)*4096|7|NX;
 return 0;
}
static uint64_t *pte8(uint64_t address,unsigned create){
 (void)create;
 assert(address>=0x41000000u&&address<0x41000000u+sizeof(arena));
 return entries+((address-0x41000000u)/4096);
}

#include "../../kernel/windows8/pe32_1410.inc"

int main(int argc,char **argv){
 assert(argc==2);
 FILE *fixture=NULL;
 assert(fopen_s(&fixture,argv[1],"rb")==0);
 image_file.size=fread(file_bytes,1,sizeof(file_bytes),fixture);
 assert(!ferror(fixture)&&feof(fixture));fclose(fixture);
 image_file.kind=1;
 win_pe32_image1410 image;
 assert(pe32_parse_file1410("fixture",&image));
 assert(image.preferred!=W8_PE32_IMAGE1410&&image.directories[5].bytes);
 assert(!pe32_map1410("fixture",&image));
 win_pe32_directory1410 reloc=image.directories[5];
 const uint8_t *block=arena+reloc.rva;
 uint32_t target=win_pe32_u321410(block)+(win_pe32_u161410(block+8)&4095u);
 uint32_t before=0;
 for(unsigned i=0;i<image.sections;++i){
  const win_pe32_section1410 *section=image.section+i;
  if(target>=section->rva&&target-section->rva+4<=section->bytes)
   before=win_pe32_u321410(file_bytes+section->raw+target-section->rva);
 }
 assert(before&&win_pe32_u321410(arena+target)==before+W8_PE32_IMAGE1410-image.preferred);
 assert(!pe32_protect1410(W8_PE32_IMAGE1410,&image));
 assert(!(entries[image.entry/4096]&(NX|2)));
 unsigned writable=0;
 for(unsigned i=0;i<image.sections;++i){
  const win_pe32_section1410 *section=image.section+i;
  if(section->flags&0x80000000u){
   assert((entries[section->rva/4096]&(NX|2))==(NX|2));
   ++writable;
  }
 }
 assert(writable);

 uint32_t pe=win_pe32_u321410(file_bytes+60);
 file_bytes[pe+4]=0x64;
 assert(!pe32_parse_file1410("fixture",&image));
 file_bytes[pe+4]=0x4c;
 uint16_t optional=win_pe32_u161410(file_bytes+pe+20);
 uint32_t sections=pe+24+optional;
 file_bytes[sections+39]|=0x80;
 assert(!pe32_parse_file1410("fixture",&image));
 return 0;
}
