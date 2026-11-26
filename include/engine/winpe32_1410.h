#ifndef ENGINE_WINPE32_1410_H
#define ENGINE_WINPE32_1410_H
#include <engine/base.h>

#define WIN_PE32_SECTIONS1410 32u
#define WIN_PE32_FILE_LIMIT1410 (32u*1024u*1024u)

typedef unsigned (*win_pe32_read1410)(void*,unsigned,void*,unsigned);
typedef struct {uint32_t rva,size,raw,bytes,flags;} win_pe32_section1410;
typedef struct {uint32_t rva,bytes;} win_pe32_directory1410;
typedef struct {
 uint32_t preferred,entry,bytes,headers,sections;
 win_pe32_directory1410 directories[16];
 win_pe32_section1410 section[WIN_PE32_SECTIONS1410];
} win_pe32_image1410;

static inline uint16_t win_pe32_u161410(const void *bytes){
 uint16_t value;memcpy(&value,bytes,sizeof(value));return value;
}
static inline uint32_t win_pe32_u321410(const void *bytes){
 uint32_t value;memcpy(&value,bytes,sizeof(value));return value;
}
static inline unsigned win_pe32_range1410(uint32_t offset,uint32_t bytes,uint32_t limit){
 return offset<=limit&&bytes<=limit-offset;
}
static inline unsigned win_pe32_mapped1410(const win_pe32_image1410 *image,uint32_t rva,uint32_t bytes){
 if(win_pe32_range1410(rva,bytes,image->headers))return 1;
 for(unsigned i=0;i<image->sections;++i){
  const win_pe32_section1410 *section=image->section+i;
  if(rva>=section->rva&&win_pe32_range1410(rva-section->rva,bytes,section->size))return 1;
 }
 return 0;
}
static inline unsigned win_pe32_parse1410(win_pe32_read1410 read,void *context,
                                         uint32_t length,win_pe32_image1410 *image){
 uint8_t dos[64],coff[24],optional[224];
 if(length<sizeof(dos)||length>WIN_PE32_FILE_LIMIT1410||
    read(context,0,dos,sizeof(dos))||memcmp(dos,"MZ",2))return 0;
 uint32_t offset=win_pe32_u321410(dos+60);
 if(offset<sizeof(dos)||!win_pe32_range1410(offset,sizeof(coff),length)||
    read(context,offset,coff,sizeof(coff))||memcmp(coff,"PE\0\0",4)||
    win_pe32_u161410(coff+4)!=0x014c)return 0;
 unsigned sections=win_pe32_u161410(coff+6),opts=win_pe32_u161410(coff+20);
 unsigned flags=win_pe32_u161410(coff+22);
 offset+=sizeof(coff);
 if(!sections||sections>WIN_PE32_SECTIONS1410||opts<96||opts>sizeof(optional)||
    !(flags&2)||(flags&0x2000)||!win_pe32_range1410(offset,opts+sections*40u,length)||
    read(context,offset,optional,opts)||win_pe32_u161410(optional)!=0x010b)return 0;
 unsigned file_alignment=win_pe32_u321410(optional+36);
 unsigned subsystem=win_pe32_u161410(optional+68),directories=win_pe32_u321410(optional+92);
 if(win_pe32_u321410(optional+32)!=4096||file_alignment<512||file_alignment>4096||
    (file_alignment&(file_alignment-1))||(subsystem!=2&&subsystem!=3)||
    directories>16||96+directories*8u>opts)return 0;
 memset(image,0,sizeof(*image));
 image->preferred=win_pe32_u321410(optional+28);image->entry=win_pe32_u321410(optional+16);
 image->bytes=win_pe32_u321410(optional+56);image->headers=win_pe32_u321410(optional+60);
 image->sections=sections;offset+=opts;
 if(!image->bytes||(image->bytes&4095)||image->bytes>WIN_PE32_FILE_LIMIT1410||
    image->headers<offset+sections*40u||image->headers>length||image->headers>image->bytes||
    (image->headers&(file_alignment-1))||!image->entry||image->entry>=image->bytes||
    (image->preferred&65535))return 0;
 unsigned previous=(image->headers+4095u)&~4095u,entry=0;
 for(unsigned i=0;i<sections;++i){
  uint8_t table[40];
  if(read(context,offset+i*40u,table,sizeof(table)))return 0;
  win_pe32_section1410 *target=image->section+i;
  target->rva=win_pe32_u321410(table+12);target->raw=win_pe32_u321410(table+20);
  target->bytes=win_pe32_u321410(table+16);target->size=win_pe32_u321410(table+8);
  if(target->bytes>target->size)target->size=target->bytes;
  target->flags=win_pe32_u321410(table+36);
  if(!target->size||(target->rva&4095)||target->rva<previous||
     !win_pe32_range1410(target->rva,target->size,image->bytes)||
     (target->flags&0xa0000000u)==0xa0000000u)return 0;
  if(target->bytes){
   if(target->raw<image->headers||(target->raw&(file_alignment-1))||
      !win_pe32_range1410(target->raw,target->bytes,length))return 0;
   for(unsigned j=0;j<i;++j){
    const win_pe32_section1410 *prior=image->section+j;
    if(prior->bytes&&target->raw<prior->raw+prior->bytes&&prior->raw<target->raw+target->bytes)return 0;
   }
  }
  previous=(target->rva+target->size+4095u)&~4095u;
  if((target->flags&0x20000000u)&&image->entry>=target->rva&&
     image->entry-target->rva<target->bytes)entry=1;
 }
 if(!entry)return 0;
 for(unsigned i=0;i<directories;++i){
  uint32_t rva=win_pe32_u321410(optional+96+i*8u),bytes=win_pe32_u321410(optional+100+i*8u);
  if((!rva)!=(!bytes))return 0;
  if(bytes&&(i==4?!win_pe32_range1410(rva,bytes,length):!win_pe32_mapped1410(image,rva,bytes)))return 0;
  image->directories[i]=(win_pe32_directory1410){rva,bytes};
 }
 return 1;
}
#endif
