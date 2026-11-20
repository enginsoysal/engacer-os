/* Checked streaming single-folder LZX cabinet; no whole-output allocation. */
#include "cab147.h"
#include <mspack.h>
#include <lzx.h>
static unsigned u16cab147(const uint8_t *p){return p[0]|(unsigned)p[1]<<8;}
static uint32_t u32cab147(const uint8_t *p){return p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;}
static uint32_t checksum147(const uint8_t *p,unsigned n){uint32_t sum=0;while(n>=4){sum^=u32cab147(p);p+=4;n-=4;}uint32_t tail=0;for(unsigned i=0;i<n;++i)tail|=(uint32_t)p[i]<<(8*(n-1-i));return sum^tail;}
static int equal_cab147(const char *a,const char *b){unsigned i=0;while(a[i]&&a[i]==b[i])++i;return a[i]==b[i];}
void cab147_close(cab147_archive *a){if(a)free8(a);}
unsigned cab147_open(msi8_blob source,cab147_archive **out){
 if(!out)return CAB147_FORMAT;*out=0;const uint8_t *p=source.data;
 if(!p||source.size<44||source.size>8*1024*1024||u32cab147(p)!=0x4643534d||u32cab147(p+8)!=source.size||p[24]!=3||p[25]!=1||u16cab147(p+26)!=1||u16cab147(p+30))return CAB147_FORMAT;
 unsigned count=u16cab147(p+28),file_at=u32cab147(p+16),data_at=u32cab147(p+36),blocks=u16cab147(p+40),compression=u16cab147(p+42),window=(compression>>8)&31;
 if(!count||count>256||file_at<44||file_at>=source.size||data_at<file_at||data_at>=source.size||!blocks||blocks>1024||(compression&15)!=3||(compression&0xe0f0)||window<15||window>21)return CAB147_FORMAT;
 cab147_archive *a=alloc8(sizeof(*a)+count*sizeof(cab147_file));if(!a)return CAB147_MEMORY;
 a->source=source;a->count=count;a->blocks=blocks;a->window=window;a->data_at=data_at;a->bytes=0;
 unsigned at=file_at;
 for(unsigned i=0;i<count;++i){
  if(at>data_at||data_at-at<16)goto bad;cab147_file *f=a->files+i;f->size=u32cab147(p+at);f->offset=u32cab147(p+at+4);f->date=(uint16_t)u16cab147(p+at+10);f->time=(uint16_t)u16cab147(p+at+12);f->attributes=(uint16_t)u16cab147(p+at+14);
  if(u16cab147(p+at+8)||f->offset!=a->bytes||f->size>32*1024*1024-a->bytes)goto bad;a->bytes+=f->size;at+=16;unsigned n=0;f->name=(const char *)p+at;
  while(at<data_at&&p[at]){if(++n>127||p[at]<32||p[at]>=127||p[at]=='/'||p[at]=='\\')goto bad;++at;}
  if(at==data_at||!n)goto bad;++at;
  for(unsigned j=0;j<i;++j)if(equal_cab147(f->name,a->files[j].name))goto bad;
 }
 if(!a->bytes)goto bad;
 at=data_at;unsigned plain_total=0;
 for(unsigned i=0;i<blocks;++i){
  if(at>source.size||source.size-at<8)goto bad;unsigned packed=u16cab147(p+at+4),plain=u16cab147(p+at+6);uint32_t checksum=u32cab147(p+at);
  if(!packed||!plain||plain>32768||packed>source.size-at-8||plain>a->bytes-plain_total)goto bad;
  if(checksum&&checksum!=(checksum147(p+at+4,4)^checksum147(p+at+8,packed)))goto bad;plain_total+=plain;at+=8+packed;
 }
 if(at!=source.size||plain_total!=a->bytes)goto bad;*out=a;return CAB147_OK;
bad:free8(a);return CAB147_FORMAT;
}
typedef struct {const cab147_archive *archive;unsigned next,at,left,blocks;} cab147_input;
typedef struct {const cab147_archive *archive;cab147_sink sink;void *context;unsigned file,offset,written,failed;} cab147_output;
static int read147(struct mspack_file *opaque,void *buffer,int bytes){
 cab147_input *in=(void *)opaque;if(bytes<0)return -1;unsigned done=0;uint8_t *out=buffer;
 while(done<(unsigned)bytes){
  if(!in->left){if(in->blocks==in->archive->blocks)break;unsigned packed=u16cab147(in->archive->source.data+in->next+4);in->at=in->next+8;in->left=packed;in->next=in->at+packed;++in->blocks;}
  unsigned n=(unsigned)bytes-done;if(n>in->left)n=in->left;memcpy(out+done,in->archive->source.data+in->at,n);done+=n;in->at+=n;in->left-=n;
 }return (int)done;
}
static int empty147(cab147_output *out){while(out->file<out->archive->count&&!out->archive->files[out->file].size){if(out->sink(out->context,out->archive->files+out->file,0,0,0)){out->failed=1;return 0;}++out->file;}return 1;}
static int write147(struct mspack_file *opaque,void *buffer,int bytes){
 cab147_output *out=(void *)opaque;if(bytes<0||(unsigned)bytes>out->archive->bytes-out->written)return -1;unsigned done=0;
 while(done<(unsigned)bytes){
  if(!empty147(out)||out->file==out->archive->count)return -1;const cab147_file *f=out->archive->files+out->file;unsigned n=(unsigned)bytes-done;if(n>f->size-out->offset)n=f->size-out->offset;
  if(out->sink(out->context,f,out->offset,(uint8_t *)buffer+done,n)){out->failed=1;return -1;}done+=n;out->offset+=n;out->written+=n;if(out->offset==f->size){++out->file;out->offset=0;}
 }return bytes;
}
static void *allocate147(struct mspack_system *system,size_t bytes){(void)system;return alloc8(bytes);}
static void copy147(void *source,void *target,size_t bytes){memcpy(target,source,bytes);}
unsigned cab147_walk(const cab147_archive *archive,cab147_sink sink,void *context){
 if(!archive||!sink)return CAB147_FORMAT;cab147_input input={.archive=archive,.next=archive->data_at};cab147_output output={.archive=archive,.sink=sink,.context=context};
 struct mspack_system system={.read=read147,.write=write147,.alloc=allocate147,.free=free8,.copy=copy147};
 struct lzxd_stream *lzx=lzxd_init(&system,(void *)&input,(void *)&output,(int)archive->window,0,4096,archive->bytes,0);if(!lzx)return CAB147_MEMORY;
 int status=lzxd_decompress(lzx,archive->bytes);lzxd_free(lzx);if(output.failed)return CAB147_SINK;if(status||output.written!=archive->bytes)return CAB147_DECODE;if(!empty147(&output))return CAB147_SINK;return output.file==archive->count?CAB147_OK:CAB147_DECODE;
}
