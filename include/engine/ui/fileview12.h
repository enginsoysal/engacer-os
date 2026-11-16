/* Shared presentation geometry and deterministic natural filename ordering. */
#ifndef ENGACER_FILEVIEW12_H
#define ENGACER_FILEVIEW12_H
#include <stdint.h>
enum {F12_COLUMN_NAME=51000,F12_COLUMN_SIZE,F12_COLUMN_TYPE,UI12_FILE_ICON_HEIGHT=112};
typedef struct {int name,type,size;unsigned type_visible,size_visible;} ui12_file_columns;
static inline ui12_file_columns ui12_file_details(int width){
 ui12_file_columns c={width,0,0,0,0};
 if(width>=360){c.size=96;c.size_visible=1;c.name-=108;}
 if(width>=560){c.type=148;c.type_visible=1;c.name-=160;}
 return c;
}
static inline unsigned ui12_file_columns_count(int width,unsigned icons){unsigned n=icons&&width>0?(unsigned)width/156:1;return n?n:1;}
static inline unsigned ui12_file_rows_count(int height,unsigned icons){int n=icons?(height-8)/UI12_FILE_ICON_HEIGHT:(height-40)/44;if(n<1)n=1;if(n>128)n=128;return(unsigned)n;}
static inline unsigned ui12_file_page_count(int width,int height,unsigned icons,unsigned usb){unsigned n=ui12_file_columns_count(width,icons)*ui12_file_rows_count(height,icons),cap=usb?6:128;return n>cap?cap:n;}
static inline unsigned ui12_file_lower(unsigned c){return c>='A'&&c<='Z'?c+32:c;}
static inline int ui12_file_natural(const char*a,const char*b){
 unsigned i=0,j=0;
 while(a[i]&&b[j]){
  if(a[i]>='0'&&a[i]<='9'&&b[j]>='0'&&b[j]<='9'){
   unsigned ai=i,bj=j;while(a[i]=='0')++i;while(b[j]=='0')++j;unsigned ae=i,be=j;
   while(a[ae]>='0'&&a[ae]<='9')++ae;while(b[be]>='0'&&b[be]<='9')++be;
   if(ae-i!=be-j)return ae-i<be-j?-1:1;
   for(unsigned n=0;n<ae-i;++n)if(a[i+n]!=b[j+n])return a[i+n]<b[j+n]?-1:1;
   if(ae-ai!=be-bj)return ae-ai<be-bj?-1:1;i=ae;j=be;continue;
  }
  unsigned x=ui12_file_lower((uint8_t)a[i]),y=ui12_file_lower((uint8_t)b[j]);if(x!=y)return x<y?-1:1;++i;++j;
 }
 return a[i]?1:b[j]?-1:0;
}
static inline const char*ui12_file_extension(const char*s){const char*dot="";for(unsigned i=0;s[i];++i)if(i&&s[i]=='.')dot=s+i+1;return dot;}
static inline const char*ui12_file_type(const char*name,unsigned kind){
 if(kind==2)return "Folder";const char*e=ui12_file_extension(name);
 if(!ui12_file_natural(e,"txt")||!ui12_file_natural(e,"md")||!ui12_file_natural(e,"log"))return "Text document";
 if(!ui12_file_natural(e,"link"))return "Shortcut";if(!ui12_file_natural(e,"bmp"))return "BMP image";
 if(!ui12_file_natural(e,"wav"))return "WAV audio";if(!ui12_file_natural(e,"zip"))return "ZIP archive";
 if(!ui12_file_natural(e,"msi"))return "MSI package";if(!ui12_file_natural(e,"exe"))return "EXE file";return "File";
}
static inline int ui12_file_order(const char*a,unsigned ak,uint64_t as,unsigned ai,const char*b,unsigned bk,uint64_t bs,unsigned bi,unsigned sort,unsigned reverse){
 if((ak==2)!=(bk==2))return ak==2?-1:1;
 int c=0;if(sort==1&&ak!=2&&as!=bs)c=as<bs?-1:1;else if(sort==2&&ak!=2)c=ui12_file_natural(ui12_file_type(a,ak),ui12_file_type(b,bk));
 if(!c)c=ui12_file_natural(a,b);if(c)return reverse?-c:c;
 return ai<bi?-1:ai>bi?1:0;
}
#endif
