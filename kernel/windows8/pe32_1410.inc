/* Checked native i386 mapping. All addresses stay in the child space. */
#include <engine/winpe32_1410.h>
#define W8_PE32_IMAGE1410 UINT32_C(0x41000000)

static unsigned pe32_file_read1410(void *path,unsigned offset,void *out,unsigned bytes){
 return exact8(path,offset,out,bytes);
}
static inline unsigned pe32_parse_file1410(const char *source,win_pe32_image1410 *image){
 const v6_entry *file=find8(source);
 return file&&file->kind==1&&file->size<=WIN_PE32_FILE_LIMIT1410&&
        !v6_verify(m6_volume(),source)&&
        win_pe32_parse1410(pe32_file_read1410,(void*)source,(uint32_t)file->size,image);
}
static unsigned pe32_copy1410(const char *source,uint32_t from,uint32_t to,unsigned bytes){
 while(bytes){
  unsigned chunk=bytes>sizeof(io8)?sizeof(io8):bytes;
  if(exact8(source,from,io8,chunk)||user8(to,io8,chunk,1))return 1;
  from+=chunk;to+=chunk;bytes-=chunk;
 }
 return 0;
}
static unsigned pe32_relocate1410(const win_pe32_image1410 *image,uint32_t base){
 uint32_t delta=base-image->preferred;
 if(!delta)return 0;
 win_pe32_directory1410 directory=image->directories[5];
 if(!directory.bytes)return 1;
 for(unsigned at=0;at<directory.bytes;){
  uint32_t header[2];
  if(directory.bytes-at<sizeof(header)||
     user8(base+directory.rva+at,header,sizeof(header),0))return 1;
  uint32_t page=header[0],size=header[1];
  if((page&4095)||size<sizeof(header)||(size&1)||size>directory.bytes-at)return 1;
  for(unsigned item=sizeof(header);item<size;item+=2){
   uint16_t entry;
   if(user8(base+directory.rva+at+item,&entry,sizeof(entry),0))return 1;
   unsigned type=entry>>12;
   if(!type)continue;
   unsigned offset=entry&4095;
   if(type!=3||page>UINT32_MAX-offset)return 1;
   uint32_t rva=page+offset;
   if(!win_pe32_mapped1410(image,rva,4))return 1;
   /* A fixup must not mutate the relocation records being parsed. */
   if(rva<directory.rva+directory.bytes&&directory.rva<rva+4)return 1;
   uint32_t value;
   if(user8(base+rva,&value,sizeof(value),0))return 1;
   value+=delta;
   if(user8(base+rva,&value,sizeof(value),1))return 1;
  }
  at+=size;
 }
 return 0;
}
static inline unsigned pe32_protect1410(uint32_t base,const win_pe32_image1410 *image){
 for(uint32_t page=0;page<image->bytes;page+=4096){
  uint64_t *entry=pte8(base+page,0);
  if(!entry||!(*entry&1))return 1;
  *entry=(*entry&UINT64_C(0x000ffffffffff000))|5|NX;
 }
 for(unsigned i=0;i<image->sections;++i){
  const win_pe32_section1410 *section=image->section+i;
  uint64_t flags=section->flags&0x20000000u?0:
                 section->flags&0x80000000u?NX|2:NX;
  for(uint32_t page=0;page<section->size;page+=4096){
   uint64_t *entry=pte8(base+section->rva+page,0);
   *entry=(*entry&UINT64_C(0x000ffffffffff000))|5|flags;
  }
 }
 return 0;
}
static inline unsigned pe32_map1410(const char *source,const win_pe32_image1410 *image){
 uint32_t base=W8_PE32_IMAGE1410;
 if(!w8_user_range1410(1,base,image->bytes)||map8(base,image->bytes,3)||
    pe32_copy1410(source,0,base,image->headers))return 1;
 for(unsigned i=0;i<image->sections;++i){
  const win_pe32_section1410 *section=image->section+i;
  if(pe32_copy1410(source,section->raw,base+section->rva,section->bytes))return 1;
 }
 return pe32_relocate1410(image,base);
}
