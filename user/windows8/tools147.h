#ifndef ENGACER_TOOLS147_H
#define ENGACER_TOOLS147_H
#include <stdint.h>
/* Bounded Windows-style argument quoting for noninteractive file utilities.
 * Unbalanced quotes and unsupported command-shell operators refuse. */
static inline int tool_space147(uint16_t c){return c==' '||c=='\t';}
static inline unsigned tool_length147(const uint16_t*s){unsigned n=0;while(s[n])++n;return n;}
static inline unsigned tool_upper147(unsigned c){return c>='a'&&c<='z'?c-32:c;}
static inline int tool_equal147(const uint16_t*a,const uint16_t*b){unsigned n=0;while(a[n]&&tool_upper147(a[n])==tool_upper147(b[n]))++n;return a[n]==b[n];}
static inline int tool_parse147(const uint16_t*input,uint16_t*storage,unsigned capacity,uint16_t**argv,unsigned limit,unsigned shell){
 if(!input||!storage||!argv||!capacity||!limit)return -87;unsigned in=0,out=0,count=0;while(in<capacity&&input[in])++in;if(in==capacity)return -87;unsigned length=in;in=0;
 while(in<length){while(in<length&&tool_space147(input[in]))++in;if(in==length)break;if(count==limit)return -1816;argv[count++]=storage+out;unsigned quoted=0;
  while(in<length&&(quoted||!tool_space147(input[in]))){unsigned slashes=0;while(in<length&&input[in]=='\\'){++slashes;++in;}
   if(in<length&&input[in]=='"'){for(unsigned i=0;i<slashes/2;++i){if(out+1>=capacity)return -1816;storage[out++]='\\';}if(slashes&1){if(out+1>=capacity)return -1816;storage[out++]='"';++in;}else if(quoted&&in+1<length&&input[in+1]=='"'){if(out+1>=capacity)return -1816;storage[out++]='"';in+=2;}else{quoted^=1;++in;}continue;}
   for(unsigned i=0;i<slashes;++i){if(out+1>=capacity)return -1816;storage[out++]='\\';}if(in==length||(!quoted&&tool_space147(input[in])))break;unsigned c=input[in++];if(shell&&((!quoted&&(c=='&'||c=='|'||c=='<'||c=='>'||c=='^'))||c=='%'))return -50;if(out+1>=capacity)return -1816;storage[out++]=(uint16_t)c;
  }
  if(quoted)return -87;storage[out++]=0;
 }return(int)count;
}
static inline int tool_wild147(const uint16_t*s){for(unsigned i=0;s[i];++i)if(s[i]=='*'||s[i]=='?')return 1;return 0;}
static inline int tool_destination147(const uint16_t*source,const uint16_t*destination,uint16_t*out,unsigned capacity){
 if(!source||!destination||!out||!capacity||tool_wild147(source))return 0;unsigned n=tool_length147(destination);if(!n||n>=capacity)return 0;for(unsigned i=0;i<=n;++i)out[i]=destination[i];
 if(out[n-1]=='*'){for(unsigned i=0;i+1<n;++i)if(out[i]=='*'||out[i]=='?')return 0;unsigned dot=n;while(dot&&out[dot-1]!='.'&&out[dot-1]!='\\'&&out[dot-1]!='/')--dot;if(!dot||out[dot-1]!='.')return 0;
  if(dot==n-1){unsigned extension=tool_length147(source);while(extension&&source[extension-1]!='.'&&source[extension-1]!='\\'&&source[extension-1]!='/')--extension;if(!extension||source[extension-1]!='.')return 0;unsigned units=tool_length147(source+extension);if(n-1+units>=capacity)return 0;for(unsigned i=0;i<=units;++i)out[n-1+i]=source[extension+i];}
  else out[n-1]=0;
 }else if(tool_wild147(out))return 0;return 1;
}
#endif
