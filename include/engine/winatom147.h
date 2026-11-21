#ifndef ENGACER_WINATOM147_H
#define ENGACER_WINATOM147_H
#include <stdint.h>
#define WATOM_SLOTS147 64u
#define WATOM_UNITS147 1854u
enum {WATOM_FIND147=1,WATOM_ADD147,WATOM_DELETE147,WATOM_NAME147};
typedef struct {uint64_t buffer;uint32_t atom,capacity;} watom_name147;
/* One lazy broker page; original spelling survives case-insensitive additions. */
typedef struct {uint16_t references[WATOM_SLOTS147],offsets[WATOM_SLOTS147],lengths[WATOM_SLOTS147],used,reserved;uint16_t text[WATOM_UNITS147];} watom_table147;
_Static_assert(sizeof(watom_table147)==4096,"Global atoms use one lazy page");
typedef uint32_t(*watom_fold147)(uint32_t);
static inline uint32_t watom_case147(uint32_t c){return c>='a'&&c<='z'?c-32:c;}
static inline int watom_scalar147(const uint16_t*s,unsigned n,unsigned*at,uint32_t*out){if(*at>=n)return 0;uint32_t c=s[(*at)++];if(c>=0xd800&&c<=0xdbff){if(*at==n||s[*at]<0xdc00||s[*at]>0xdfff)return 0;c=0x10000+((c-0xd800)<<10)+(s[(*at)++]-0xdc00);}else if(c>=0xdc00&&c<=0xdfff)return 0;*out=c;return 1;}
static inline int watom_valid147(const uint16_t*s,unsigned n){if(!s||!n||n>255)return 0;unsigned at=0;uint32_t c;while(at<n)if(!watom_scalar147(s,n,&at,&c)||!c)return 0;return 1;}
static inline int watom_equal147(const uint16_t*a,unsigned an,const uint16_t*b,unsigned bn,watom_fold147 fold){unsigned x=0,y=0;while(x<an&&y<bn){uint32_t ac,bc;if(!watom_scalar147(a,an,&x,&ac)||!watom_scalar147(b,bn,&y,&bc))return 0;if(fold(ac)!=fold(bc))return 0;}return x==an&&y==bn;}
/* Zero means ordinary string; negative means invalid numeric form. */
static inline int watom_number147(const uint16_t*s,unsigned n){if(n<2||s[0]!='#')return 0;for(unsigned i=1;i<n;++i)if(s[i]<'0'||s[i]>'9')return 0;unsigned value=0;for(unsigned i=1;i<n;++i){if(value>(0xbfffu-(s[i]-'0'))/10)return -87;value=value*10+s[i]-'0';}return value?(int)value:-87;}
static inline int watom_find147(const watom_table147*t,const uint16_t*s,unsigned n,watom_fold147 fold){if(!watom_valid147(s,n))return -87;int number=watom_number147(s,n);if(number)return number;if(t)for(unsigned i=0;i<WATOM_SLOTS147;++i)if(t->references[i]&&watom_equal147(t->text+t->offsets[i],t->lengths[i],s,n,fold))return(int)(0xc000u+i);return -2;}
static inline int watom_add147(watom_table147*t,const uint16_t*s,unsigned n,watom_fold147 fold){int found=watom_find147(t,s,n,fold);if(found!=-2){if(found<0||found<0xc000)return found;unsigned i=(unsigned)found-0xc000u;if(t->references[i]==65535)return -1816;++t->references[i];return found;}
 if(!t)return -8;if(n+1>WATOM_UNITS147-t->used)return -1816;unsigned i=0;while(i<WATOM_SLOTS147&&t->references[i])++i;if(i==WATOM_SLOTS147)return -1816;t->offsets[i]=t->used;t->lengths[i]=(uint16_t)n;t->references[i]=1;for(unsigned k=0;k<n;++k)t->text[t->used+k]=s[k];t->text[t->used+n]=0;t->used=(uint16_t)(t->used+n+1);return(int)(0xc000u+i);
}
static inline int watom_delete147(watom_table147*t,unsigned atom){if(atom<0xc000)return 0;unsigned i=atom-0xc000u;if(!t||i>=WATOM_SLOTS147||!t->references[i])return -6;if(--t->references[i])return 0;unsigned start=t->offsets[i],n=t->lengths[i]+1;for(unsigned k=start+n;k<t->used;++k)t->text[k-n]=t->text[k];t->used=(uint16_t)(t->used-n);for(unsigned k=0;k<WATOM_SLOTS147;++k)if(t->references[k]&&t->offsets[k]>start)t->offsets[k]=(uint16_t)(t->offsets[k]-n);t->lengths[i]=t->offsets[i]=0;return 0;}
static inline int watom_name_copy147(const watom_table147*t,unsigned atom,uint16_t*out,unsigned capacity){if(!capacity)return -234;if(!out)return -87;uint16_t digits[8];const uint16_t*s=0;unsigned n=0;if(atom&&atom<0xc000){digits[n++]='#';uint16_t reverse[6];unsigned count=0;do{reverse[count++]=(uint16_t)('0'+atom%10);atom/=10;}while(atom);while(count)digits[n++]=reverse[--count];s=digits;}else{unsigned i=atom-0xc000u;if(!t||i>=WATOM_SLOTS147||!t->references[i])return -6;s=t->text+t->offsets[i];n=t->lengths[i];}unsigned copied=n<capacity?n:capacity;for(unsigned i=0;i<copied;++i)out[i]=s[i];if(copied<capacity)out[copied]=0;return(int)copied;}
#endif
