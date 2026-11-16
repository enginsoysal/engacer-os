#define _CRT_SECURE_NO_WARNINGS
#define ENGINE_M12
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <engine/desktop/app.h>
#include <engine/install/m6.h>
#define APP7_SLOTS 8u
typedef struct {unsigned live,kind;uint8_t input[APP7_TEXT];} instance;
static instance instances[APP7_SLOTS];
volatile unsigned app7_active;
static v6_volume volume;
static uint8_t original[APP7_TEXT],source[APP7_TEXT];
static uint32_t original_crc;static unsigned reads,transfers,calls,maximum,fault,changed,stop;
v6_volume*m6_volume(void){return &volume;}
unsigned v6_read(v6_volume*v,const char*path,uint64_t off,void*out,unsigned n,unsigned*got){
    if(v!=&volume||strcmp(path,"/Users/Owner/Source.txt")||off+n>volume.entries[0].size||n>4096)abort();
    ++reads;if(fault&&off)return V6_IO;if(n>maximum)maximum=n;
    memcpy(out,source+off,n);*got=n;if(changed&&off)volume.entries[0].first++;return 0;
}
static void transfer(instance*p,unsigned offset,void*data,unsigned n,int to_user){
    if(p!=&instances[0]||!to_user||offset<offsetof(app7_mailbox,input)||offset+n>offsetof(app7_mailbox,input)+APP7_TEXT)abort();
    ++transfers;memcpy(p->input+offset - offsetof(app7_mailbox,input),data,n);
}
static unsigned request7(unsigned slot,unsigned command,unsigned key,const void*data,unsigned n,app7_view*view,unsigned prepared){
    if(slot||command!=APP7_LOAD||key||data||prepared!=1||n!=volume.entries[0].size||memcmp(instances[0].input,source,n))abort();
    ++calls;if(stop)return V6_INVALID;memcpy(view->text,source,n);view->text[n]=0;view->length=view->cursor=n;view->dirty=0;return 0;
}
#include "../../kernel/desktop/document12.inc"
static void reset(app7_view*view){
    memset(&volume,0,sizeof(volume));volume.mounted=1;strcpy(volume.entries[0].path,"/Users/Owner/Source.txt");volume.entries[0].kind=1;volume.entries[0].first=160;volume.entries[0].size=8191;volume.entries[0].crc=original_crc;
    instances[0].live=1;instances[0].kind=2;memset(instances[0].input,0xa5,APP7_TEXT);memcpy(source,original,APP7_TEXT);
    memset(view,0,sizeof(*view));strcpy(view->text,"Keep unsaved work");view->length=view->cursor=17;view->dirty=1;
    reads=transfers=calls=maximum=fault=changed=stop=app7_active=0;
}
#define CHECK(x) do{if(!(x)){fprintf(stderr,"Failed line %d\n",__LINE__);return 1;}}while(0)
int main(int argc,char**argv){
    if(argc!=2)return 2;FILE*file=fopen(argv[1],"rb");if(!file)return 3;
    if(fread(&original_crc,4,1,file)!=1||fread(original,1,8191,file)!=8191)return 4;fclose(file);
    app7_view view;const char*path="/Users/Owner/Source.txt";
    reset(&view);CHECK(!app7_document12(0,path,&view,0)&&reads==2&&!transfers&&!calls&&!strcmp(view.text,"Keep unsaved work")&&view.dirty);
    reset(&view);CHECK(!app7_document12(0,path,&view,1)&&reads==2&&transfers==2&&calls==1&&maximum==4096&&view.length==8191&&!view.dirty&&!memcmp(view.text,original,8191)&&!view.text[8191]);
    reset(&view);volume.entries[0].size=0;volume.entries[0].crc=0;CHECK(!app7_document12(0,path,&view,1)&&!reads&&!transfers&&calls==1&&!view.length);
    reset(&view);volume.entries[0].size=8192;CHECK(app7_document12(0,path,&view,1)==V6_LIMIT&&!reads&&!calls);
    reset(&view);source[4098]=0;CHECK(app7_document12(0,path,&view,1)==V6_INVALID&&!calls&&view.dirty&&!strcmp(view.text,"Keep unsaved work"));
    reset(&view);source[100]=0xc3;CHECK(app7_document12(0,path,&view,1)==V6_INVALID&&!calls&&view.dirty);
    reset(&view);volume.entries[0].crc^=1;CHECK(app7_document12(0,path,&view,1)==V6_INVALID&&!calls&&view.dirty);
    reset(&view);fault=1;CHECK(app7_document12(0,path,&view,1)==V6_IO&&!calls&&view.dirty&&!strcmp(view.text,"Keep unsaved work"));
    reset(&view);changed=1;CHECK(app7_document12(0,path,&view,1)==V6_INVALID&&!calls&&view.dirty);
    reset(&view);stop=1;CHECK(app7_document12(0,path,&view,1)==APP12_DOCUMENT_STOPPED&&calls==1&&view.dirty&&!strcmp(view.text,"Keep unsaved work"));
    reset(&view);CHECK(app7_document12(0,"/missing",&view,1)==V6_NOTFOUND&&!reads&&!calls);
    reset(&view);CHECK(app7_document12(8,path,&view,1)==V6_INVALID&&app7_document12(0,0,&view,1)==V6_INVALID&&app7_document12(0,path,0,1)==V6_INVALID&&app7_document12(0,path,&view,2)==V6_INVALID&&!reads&&!calls);
    reset(&view);instances[0].kind=4;CHECK(app7_document12(0,path,&view,1)==V6_INVALID&&!reads&&!calls);
    reset(&view);app7_active=1;CHECK(app7_document12(0,path,&view,1)==V6_INVALID&&!reads&&!calls);
    puts("{\"passed\":true,\"checks\":14,\"maximum_read_bytes\":4096,\"new_kernel_payload_buffers\":0,\"old_view_preserved_on_errors\":true}");return 0;
}
