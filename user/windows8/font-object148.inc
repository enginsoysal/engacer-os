/* Logical font objects share immutable native raster strikes; no glyph cache. */
#include <engine/winui144.h>
typedef struct {int32_t height,width,escapement,orientation,weight;uint8_t italic,underline,strike,charset,out_precision,clip_precision,quality,pitch;WCHAR face[32];} logfont148;
_Static_assert(sizeof(logfont148)==92,"Win64 LOGFONTW layout");
typedef struct font_object148 {struct font_object148*next;HANDLE handle;logfont148 logical;ui_font_metrics148 metrics;unsigned selected;} font_object148;
static font_object148*fonts148;static unsigned font_count148,font_sequence148;static lock142 font_lock148;
#define FONT_PREFIX148 UINT64_C(0x464f000000000000)
static unsigned font_handle148(HANDLE h){return(h&UINT64_C(0xffff000000000000))==FONT_PREFIX148;}
static unsigned font_stock148(HANDLE h){return h== (FONT_PREFIX148|12)||h==(FONT_PREFIX148|13)||h==(FONT_PREFIX148|14)||h==(FONT_PREFIX148|17);}
static font_object148*font_find148(HANDLE h){for(font_object148*f=fonts148;f;f=f->next)if(f->handle==h)return f;return 0;}
static unsigned font_query148(unsigned em,ui_font_metrics148*out){int64_t r=sys8(W8_SYS_UI144,WUI_FONT148,em,(uint64_t)(uintptr_t)out,0,0);if(r<0){last8((unsigned)-r);return 0;}return 1;}
static unsigned font_info148(HANDLE h,ui_font_metrics148*out,logfont148*logical){
 lock_enter142(&font_lock148);font_object148*f=font_find148(h);if(f){if(out)*out=f->metrics;if(logical)*logical=f->logical;lock_leave142(&font_lock148);return 1;}
 lock_leave142(&font_lock148);if(!font_stock148(h)){last8(6);return 0;}if(out&&!font_query148(16,out))return 0;if(logical){memset(logical,0,sizeof(*logical));logical->height=-16;logical->weight=400;memcpy(logical->face,u"Inter",12);}return 1;
}
static unsigned font_select148(HANDLE h,unsigned add){if(font_stock148(h))return 1;lock_enter142(&font_lock148);font_object148*f=font_find148(h);if(f){if(add)++f->selected;else if(f->selected)--f->selected;}lock_leave142(&font_lock148);if(!f)last8(6);return f!=0;}
static HANDLE MS f_CreateFontIndirectW(const logfont148*input){
 if(!input||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,sizeof(*input),1,0,0)){last8(998);return 0;}logfont148 logical=*input;
 if(logical.width||logical.escapement||logical.orientation||logical.italic){last8(50);return 0;}if(logical.weight<0||logical.weight>1000){last8(87);return 0;}logical.face[31]=0;
 unsigned sizes[4]={14,16,21,28};uint64_t best=UINT64_MAX;ui_font_metrics148 chosen={0};
 int64_t desired=logical.height<0?-(int64_t)logical.height:logical.height;if(!desired)desired=16;int weight=logical.weight?logical.weight:400;
 for(unsigned i=0;i<4;++i){ui_font_metrics148 m;if(!font_query148(sizes[i],&m))return 0;int64_t distance=(logical.height>0?m.height:m.em)-desired;if(distance<0)distance=-distance;int wd=(int)m.weight-weight;if(wd<0)wd=-wd;uint64_t score=(uint64_t)distance*1024+(unsigned)wd;if(score<best){best=score;chosen=m;}}
 lock_enter142(&font_lock148);if(font_count148==64||font_sequence148==UINT32_MAX){lock_leave142(&font_lock148);last8(1816);return 0;}font_object148*f=calloc8(1,sizeof(*f));if(!f){lock_leave142(&font_lock148);last8(8);return 0;}
 f->handle=FONT_PREFIX148|UINT64_C(0x100000000)|++font_sequence148;f->logical=logical;f->metrics=chosen;f->next=fonts148;fonts148=f;++font_count148;HANDLE h=f->handle;lock_leave142(&font_lock148);return h;
}
static HANDLE MS f_GetStockObject(int id){HANDLE h=FONT_PREFIX148|(unsigned)id;if(font_stock148(h))return h;last8(50);return 0;}
static int font_delete148(HANDLE h){if(font_stock148(h))return 1;lock_enter142(&font_lock148);font_object148*f=font_find148(h);if(!f||f->selected){lock_leave142(&font_lock148);last8(f?170:6);return 0;}font_object148**link=&fonts148;while(*link!=f)link=&(*link)->next;*link=f->next;--font_count148;free8(f);lock_leave142(&font_lock148);return 1;}
static int MS f_GetObjectW(HANDLE h,int bytes,void*out){logfont148 lf;if(!font_info148(h,0,&lf))return 0;if(!out)return sizeof(lf);if(bytes<0||bytes>(int)sizeof(lf)){last8(50);return 0;}if(!bytes)return 0;if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,(unsigned)bytes,2,0,0)){last8(998);return 0;}memcpy(out,&lf,(unsigned)bytes);return bytes;}
