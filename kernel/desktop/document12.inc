#include <engine/desktop/text146.h>
/* Stage checked text in the worker's existing IPC input pages. The old kernel
 * view is not replaced until the normal broker validates a successful reply. */
unsigned app7_document12(unsigned slot,const char*path,app7_view*view,unsigned apply){
    if(slot>=APP7_SLOTS||!instances[slot].live||instances[slot].kind!=2||app7_active||!path||!view||apply>1)return V6_INVALID;
    v6_volume*v=m6_volume();if(!v||!v->mounted)return V6_INVALID;
    const v6_entry*e=0;
    for(unsigned i=0;i<V6_ENTRIES;++i){const v6_entry*item=&v->entries[i];unsigned j=0;
        while(j<256&&item->path[j]&&item->path[j]==path[j])++j;
        if(j<256&&!item->path[j]&&!path[j]&&item->kind==1){e=item;break;}}
    if(!e)return V6_NOTFOUND;if(e->size>=APP7_TEXT)return V6_LIMIT;
    uint64_t first=e->first,total=e->size;uint32_t expected=e->crc,sum=~0u;text_decoder146 decoder={0};
    for(uint64_t off=0;off<total;){
        unsigned n=(unsigned)(total-off>V6_PAGE?V6_PAGE:total-off),got=0;
        if(v6_read(v,path,off,v->page,n,&got)||got!=n)return V6_IO;
        for(unsigned i=0;i<n;++i){unsigned c=v->page[i];
            if(!text_byte146(&decoder,c))return V6_INVALID;
            sum^=c;for(unsigned bit=0;bit<8;++bit)sum=(sum>>1)^(0xedb88320u&-(sum&1));}
        if(apply)transfer(&instances[slot],offsetof(app7_mailbox,input)+(unsigned)off,v->page,n,1);
        off+=n;
    }
    if(decoder.remaining)return V6_INVALID;
    unsigned at=0;while(at<256&&e->path[at]&&e->path[at]==path[at])++at;
    if(at==256||e->path[at]||path[at]||e->kind!=1||e->first!=first||e->size!=total||e->crc!=expected||~sum!=expected)return V6_INVALID;
    if(!apply)return V6_OK;
    return request7(slot,APP7_LOAD,0,0,(unsigned)total,view,1)?APP12_DOCUMENT_STOPPED:V6_OK;
}
