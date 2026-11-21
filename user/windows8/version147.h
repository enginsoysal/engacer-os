#ifndef ENGACER_VERSION147_H
#define ENGACER_VERSION147_H
/* Read-only bounded PE version-resource and VS_VERSIONINFO parsing. */
#include <stdint.h>
#include <stddef.h>
typedef int (*ver_read147)(void*,uint64_t,void*,unsigned);
typedef struct {ver_read147 read;void*context;uint64_t bytes;unsigned sections;uint32_t headers,directory,directory_bytes;uint8_t section[32][40];} ver_file147;
typedef struct {uint32_t offset,bytes;} ver_resource147;
typedef struct {unsigned start,end,key,key_units,value,value_units,value_bytes,children,type;} ver_node147;
static inline unsigned ver_u16_147(const uint8_t*p){return p[0]|((unsigned)p[1]<<8);}
static inline uint32_t ver_u32_147(const uint8_t*p){return(uint32_t)p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24);}
static inline int ver_span147(uint64_t at,uint64_t n,uint64_t bytes){return at<=bytes&&n<=bytes-at;}
static inline unsigned ver_align147(unsigned n){return(n+3u)&~3u;}
static inline int ver_read_file147(const ver_file147*f,uint64_t at,void*out,unsigned n){return ver_span147(at,n,f->bytes)&&!f->read(f->context,at,out,n);}
static inline int ver_rva147(const ver_file147*f,uint32_t at,unsigned n,uint32_t*out){
 unsigned matches=0;uint32_t found=0;if(ver_span147(at,n,f->headers)&&ver_span147(at,n,f->bytes)){found=at;++matches;}
 for(unsigned i=0;i<f->sections;++i){const uint8_t*s=f->section[i];uint32_t rva=ver_u32_147(s+12),raw=ver_u32_147(s+16),offset=ver_u32_147(s+20);if(at>=rva&&ver_span147((uint64_t)at-rva,n,raw)&&ver_span147((uint64_t)offset+at-rva,n,f->bytes)){found=offset+at-rva;++matches;}}
 if(matches!=1)return 0;*out=found;return 1;
}
static inline int ver_directory147(const ver_file147*f,uint32_t relative,void*out,unsigned n){uint32_t offset;if(!ver_span147(relative,n,f->directory_bytes)||(uint64_t)f->directory+relative>UINT32_MAX||!ver_rva147(f,f->directory+relative,n,&offset))return 0;return ver_read_file147(f,offset,out,n);}
static inline unsigned ver_open147(ver_file147*f,ver_read147 read,void*context,uint64_t bytes,ver_resource147*out){
 if(!f||!read||!out||bytes<64||bytes>32u*1024u*1024u)return 193;*f=(ver_file147){.read=read,.context=context,.bytes=bytes};uint8_t dos[64],pe[24],optional[240];
 if(!ver_read_file147(f,0,dos,64)||ver_u16_147(dos)!=0x5a4d)return 193;uint32_t at=ver_u32_147(dos+60);if(!ver_read_file147(f,at,pe,24)||ver_u32_147(pe)!=0x4550)return 193;
 f->sections=ver_u16_147(pe+6);unsigned options=ver_u16_147(pe+20);if(!f->sections||f->sections>32||options>sizeof(optional)||options<120||!ver_read_file147(f,(uint64_t)at+24,optional,options))return 193;
 unsigned magic=ver_u16_147(optional),directories=magic==0x20b?112:magic==0x10b?96:0;if(!directories||options<directories+24||ver_u32_147(optional+directories-4)<3)return 193;
 f->headers=ver_u32_147(optional+60);f->directory=ver_u32_147(optional+directories+16);f->directory_bytes=ver_u32_147(optional+directories+20);
 if(!f->directory||!f->directory_bytes)return 1812;if(f->directory_bytes>32u*1024u*1024u||!ver_span147((uint64_t)at+24+options,(uint64_t)f->sections*40,f->headers)||f->headers>bytes)return 193;
 if(!ver_read_file147(f,(uint64_t)at+24+options,f->section,f->sections*40))return 193;
 uint32_t table=0;
 for(unsigned level=0;level<3;++level){uint8_t header[16];if(!ver_directory147(f,table,header,16))return 193;unsigned named=ver_u16_147(header+12),count=named+ver_u16_147(header+14);if(count>4096||!ver_span147(table,(uint64_t)16+count*8,f->directory_bytes))return 193;
  uint32_t chosen=0;unsigned rank=4,found=0;
  for(unsigned i=0;i<count;++i){uint8_t row[8];if(!ver_directory147(f,table+16+i*8,row,8))return 193;uint32_t key=ver_u32_147(row),child=ver_u32_147(row+4);if(level<2){if(key==(level?1u:16u)){if(found)return 193;chosen=child;found=1;}}
   else if(!(key&0xffff0000u)){unsigned candidate=key==0?0:key==1033?1:2;if(candidate<rank){chosen=child;rank=candidate;found=1;}}
  }
  if(!found)return level==0?1813:level==1?1814:1815;
  if(level<2){if(!(chosen&0x80000000u))return 193;table=chosen&0x7fffffffu;}
  else{uint8_t row[16];if(chosen&0x80000000u||!ver_directory147(f,chosen,row,16))return 193;uint32_t data=ver_u32_147(row),n=ver_u32_147(row+4),offset;if(n<40||n>65535||!ver_rva147(f,data,n,&offset))return 193;*out=(ver_resource147){offset,n};return 0;}
 }return 193;
}
static inline int ver_node_parse147(const uint8_t*data,unsigned bytes,unsigned at,unsigned limit,ver_node147*out){
 if(!data||!out||limit>bytes||!ver_span147(at,6,limit))return 0;unsigned n=ver_u16_147(data+at),units=ver_u16_147(data+at+2),type=ver_u16_147(data+at+4);if(n<8||type>1||!ver_span147(at,n,limit))return 0;unsigned end=at+n,key=at+6,cursor=key,chars=0;
 for(;;){if(!ver_span147(cursor,2,end)||chars>255)return 0;unsigned c=ver_u16_147(data+cursor);cursor+=2;if(!c)break;++chars;}
 unsigned value=ver_align147(cursor),value_bytes=type?units*2u:units;if(value>end||!ver_span147(value,value_bytes,end))return 0;unsigned children=ver_align147(value+value_bytes);if(children>end)children=end;
 *out=(ver_node147){at,end,key,chars,value,units,value_bytes,children,type};return 1;
}
static inline int ver_key147(const uint8_t*data,const ver_node147*n,const uint16_t*key,unsigned units){if(n->key_units!=units)return 0;for(unsigned i=0;i<units;++i){unsigned a=ver_u16_147(data+n->key+i*2),b=key[i];if(a>='a'&&a<='z')a-=32;if(b>='a'&&b<='z')b-=32;if(a!=b)return 0;}return 1;}
static inline int ver_root147(const uint8_t*data,unsigned bytes,ver_node147*out){
 static const uint16_t root[]={ 'V','S','_','V','E','R','S','I','O','N','_','I','N','F','O'};
 if(!ver_node_parse147(data,bytes,0,bytes,out)||out->type||!ver_key147(data,out,root,15))return 0;
 if(out->value_bytes&&(out->value_bytes!=52||ver_u32_147(data+out->value)!=0xfeef04bdu||ver_u32_147(data+out->value+4)!=0x10000u))return 0;return 1;
}
static inline unsigned ver_query147(const uint8_t*data,unsigned bytes,const uint16_t*path,unsigned*offset,unsigned*length){
 if(!data||!path||!offset||!length||path[0]!='\\')return 87;ver_node147 node;if(!ver_root147(data,bytes,&node))return 13;unsigned at=1,depth=0;
 while(path[at]){if(++depth>16)return 87;unsigned start=at;while(path[at]&&path[at]!='\\'){if(at-start==128)return 87;++at;}if(at==start)return 87;unsigned found=0,cursor=node.children;ver_node147 child;
  for(unsigned count=0;cursor<node.end;++count){if(count==4096||!ver_node_parse147(data,bytes,cursor,node.end,&child))return 13;if(ver_key147(data,&child,path+start,at-start)){if(found)return 13;found=1;node.start=child.start;/* retain parent end until traversal completes */}
   unsigned next=ver_align147(child.end);if(next<=cursor)return 13;cursor=next;
  }
  if(!found)return 1814;if(!ver_node_parse147(data,bytes,node.start,bytes,&node))return 13;if(path[at]=='\\'){++at;if(!path[at])return 87;}
 }
 if(!node.value_bytes)return 1814;*offset=node.value;*length=node.value_units;return 0;
}
#endif
