#ifndef ENGINE_WINPRODUCT147_H
#define ENGINE_WINPRODUCT147_H
/* A Windows product grant names exactly one canonical GUID directory. */
#define WIN_PRODUCT_BASE147 "/Applications/Windows/"
static inline int win_product_guid147(const char*s,unsigned canonical){
 if(!s)return 0;unsigned n=0;while(n<=38&&s[n])++n;if(n!=38||s[0]!='{'||s[37]!='}')return 0;
 for(unsigned i=1;i<37;++i){unsigned c=(unsigned char)s[i];if(i==9||i==14||i==19||i==24){if(c!='-')return 0;}else if(!((c>='0'&&c<='9')||(c>='A'&&c<='F')||(!canonical&&c>='a'&&c<='f')))return 0;}return 1;
}
static inline int win_product_root147(const char*s){if(!s)return 0;const char*base=WIN_PRODUCT_BASE147;unsigned n=0;for(;base[n];++n)if(s[n]!=base[n])return 0;return win_product_guid147(s+n,1);}
static inline int win_product_make147(char*out,unsigned capacity,const char*code){if(!out||!capacity)return 0;out[0]=0;if(capacity<sizeof(WIN_PRODUCT_BASE147)+38||!win_product_guid147(code,0))return 0;unsigned at=0;const char*base=WIN_PRODUCT_BASE147;for(;base[at];++at)out[at]=base[at];for(unsigned i=0;i<=38;++i){char c=code[i];out[at+i]=c>='a'&&c<='f'?c-32:c;}return 1;}
/* Outside the product root: its last file may disappear before cleanup ends. */
#define WIN_PRODUCT_DONE_BASE147 "/Data/Windows/Transactions/"
static inline int win_product_completion147(char*out,unsigned capacity,const char*root){
 if(out&&capacity)out[0]=0;if(!out||!win_product_root147(root)||capacity<sizeof(WIN_PRODUCT_DONE_BASE147)+38+5)return 0;
 const char*base=WIN_PRODUCT_DONE_BASE147,*code=root+sizeof(WIN_PRODUCT_BASE147)-1,*tail=".done";unsigned at=0;for(unsigned i=0;base[i];++i)out[at++]=base[i];for(unsigned i=0;i<38;++i)out[at++]=code[i];for(unsigned i=0;tail[i];++i)out[at++]=tail[i];out[at]=0;return 1;
}
#endif
