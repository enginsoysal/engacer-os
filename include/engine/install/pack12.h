#ifndef ENGINE_INSTALL_PACK12_H
#define ENGINE_INSTALL_PACK12_H
#include <stdint.h>

/* Independent raw LZ4 block, maximum 4096 bytes in/out. No heap or dictionary.
 * Reject malformed lengths, back-references, flags and non-exact output before
 * a caller is permitted to submit any destination write. */
static inline unsigned pack12_decode(const uint8_t *in,unsigned bytes,uint8_t *out){
    unsigned at=0,used=0;
    if(!in||!out||!bytes||bytes>=4096)return 0;
    while(at<bytes){
        unsigned token=in[at++],n=token>>4;
        if(n==15){unsigned v;do{if(at==bytes)return 0;v=in[at++];if(v>4096-n)return 0;n+=v;}while(v==255);}
        if(n>bytes-at||n>4096-used)return 0;
        for(unsigned i=0;i<n;++i)out[used++]=in[at++];
        if(at==bytes)return used==4096 && !(token&15);
        if(bytes-at<2)return 0;
        unsigned back=(unsigned)in[at]|((unsigned)in[at+1]<<8);at+=2;
        if(!back||back>used)return 0;
        n=(token&15)+4;
        if((token&15)==15){unsigned v;do{if(at==bytes)return 0;v=in[at++];if(v>4096-n)return 0;n+=v;}while(v==255);}
        if(n>4096-used)return 0;
        for(unsigned i=0;i<n;++i){out[used]=out[used-back];++used;}
    }
    return 0;
}

static inline unsigned pack12_size(uint32_t value,const uint8_t *body,unsigned available){
    if(value&0x80000000u)return (value&0x40000000u)?0:4;
    if(!(value&0x40000000u))return available>=4096?4100:0;
    if(available<2)return 0;
    unsigned n=(unsigned)body[0]|((unsigned)body[1]<<8);
    return n && n<4094 && n<=available-2 ? n+6 : 0;
}
#endif
