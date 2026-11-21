/* Selected UTF-8 ACP/OEM and explicit Windows-1252 codec profile. */
static const uint16_t cp1252_high147[]={0x20ac,0x81,0x201a,0x192,0x201e,0x2026,0x2020,0x2021,0x2c6,0x2030,0x160,0x2039,0x152,0x8d,0x17d,0x8f,0x90,0x2018,0x2019,0x201c,0x201d,0x2022,0x2013,0x2014,0x2dc,0x2122,0x161,0x203a,0x153,0x9d,0x17e,0x178};
static unsigned MS f_GetOEMCP(void){return 65001;}
static unsigned MS f_GetACP(void){return 65001;}
/* UTF-8 is variable-width, not a Windows double-byte code page. Neither
 * supported explicit encoding has DBCS lead ranges; preserve last error on
 * valid negative results and reject unsupported code pages explicitly. */
static int MS f_IsDBCSLeadByte(uint8_t value){(void)value;return 0;}
static int MS f_IsDBCSLeadByteEx(unsigned cp,uint8_t value){(void)value;if(cp!=0&&cp!=1&&cp!=3&&cp!=65001&&cp!=1252)last8(87);return 0;}
static int MS f_MultiByteToWideChar(unsigned cp,unsigned flags,const char*src,int count,WCHAR*out,int capacity){
 if(!src||count==0||count< -1||capacity<0||(capacity&&!out)||(flags&~8u)||(cp!=0&&cp!=1&&cp!=65001&&cp!=1252)){last8(87);return 0;}unsigned n=count<0?len8(src)+1:(unsigned)count,used=0;

 for(unsigned i=0;i<n;){unsigned v=(uint8_t)src[i++],extra=0,min=0;if(cp==1252){if(v>=128&&v<160)v=cp1252_high147[v-128];}else{if(v>0xf4){last8(1113);return 0;}if(v>=0xf0){v&=7;extra=3;min=65536;}else if(v>=0xe0){v&=15;extra=2;min=2048;}else if(v>=0xc2){v&=31;extra=1;min=128;}else if(v>=128){last8(1113);return 0;}if(extra>n-i){last8(1113);return 0;}for(unsigned j=0;j<extra;++j){unsigned b=(uint8_t)src[i++];if((b&0xc0)!=0x80){last8(1113);return 0;}v=(v<<6)|(b&63);}if(v<min||v>0x10ffff||(v>=0xd800&&v<=0xdfff)){last8(1113);return 0;}}
  unsigned units=v>65535?2:1;if(capacity&&used+units>(unsigned)capacity){last8(122);return 0;}if(out&&capacity){if(units==1)out[used]=(WCHAR)v;else{v-=0x10000;out[used]=(WCHAR)(0xd800+(v>>10));out[used+1]=(WCHAR)(0xdc00+(v&1023));}}used+=units;
 }return (int)used;
}
static int MS f_WideCharToMultiByte(unsigned cp,unsigned flags,const WCHAR*src,int count,char*out,int capacity,const char*default_char,int*used_default){
 if(!src||count==0||count< -1||capacity<0||(capacity&&!out)||(flags&~0x400u)||(cp!=0&&cp!=1&&cp!=65001&&cp!=1252)){last8(87);return 0;}unsigned n=count<0?wlen8(src)+1:(unsigned)count,used=0;if(used_default)*used_default=0;
 for(unsigned i=0;i<n;++i){unsigned v=src[i];if(v>=0xd800&&v<=0xdbff){if(i+1>=n||src[i+1]<0xdc00||src[i+1]>0xdfff){last8(1113);return 0;}v=0x10000+((v-0xd800)<<10)+(src[++i]-0xdc00);}else if(v>=0xdc00&&v<=0xdfff){last8(1113);return 0;}
  unsigned encoded147=UINT32_MAX;if(cp==1252){if(v<128||(v>=160&&v<=255))encoded147=v;else for(unsigned k=0;k<32;++k)if(v==cp1252_high147[k]){encoded147=k+128;break;}if(encoded147>255){encoded147=(uint8_t)(default_char?*default_char:'?');if(used_default)*used_default=1;}}
  unsigned bytes=cp==1252?1:v<128?1:v<2048?2:v<65536?3:4;if(capacity&&used+bytes>(unsigned)capacity){last8(122);return 0;}if(out&&capacity){if(cp==1252){out[used]=(char)encoded147;}else if(bytes==1)out[used]=(char)v;else{out[used]=(char)((bytes==2?0xc0:bytes==3?0xe0:0xf0)|(v>>(6*(bytes-1))));for(unsigned j=1;j<bytes;++j)out[used+j]=(char)(0x80|((v>>(6*(bytes-j-1)))&63));}}used+=bytes;
 }return (int)used;
}
#ifdef ENGINE_M14
static int MS f_IsValidCodePage(unsigned cp){return cp==65001||cp==1252;}
static int MS f_GetCPInfo(unsigned cp,void*out){
 if(!out||(cp!=0&&cp!=1&&!f_IsValidCodePage(cp))){last8(87);return 0;}
 unsigned char info[20]={0};unsigned size=cp==1252?1u:4u;memcpy(info,&size,4);info[4]='?';memcpy(out,info,sizeof(info));return 1;
}
#endif
