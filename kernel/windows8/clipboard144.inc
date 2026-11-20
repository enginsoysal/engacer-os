/* Session-global registered format names. No clipboard data or foreign callbacks. */
#define CLIP_FORMATS144 128u
#define CLIP_PER_PAGE144 7u
typedef struct {unsigned units;uint16_t name[256];} clip_format144;
_Static_assert(sizeof(clip_format144)*CLIP_PER_PAGE144<=4096,"Format-name page quota");
static clip_format144*clip_pages144[(CLIP_FORMATS144+CLIP_PER_PAGE144-1)/CLIP_PER_PAGE144];
static unsigned clip_count144;
static unsigned clip_name_equal144(const uint16_t*a,unsigned an,const uint16_t*b,unsigned bn){unsigned x=0,y=0;while(x<an&&y<bn){uint32_t ax,by;if(!decode_utf16_143(a,an,&x,&ax)||!decode_utf16_143(b,bn,&y,&by)||fold143(ax)!=fold143(by))return 0;}return x==an&&y==bn;}
static int64_t clip_register144(uint64_t pointer){
 uint16_t name[256];unsigned units=0;for(;units<256;++units){if(user8(pointer+(uint64_t)units*2,name+units,2,0))return -998;if(!name[units])break;}if(!units||units==256)return -87;unsigned at=0;while(at<units){uint32_t cp;if(!decode_utf16_143(name,units,&at,&cp))return -1113;}
 for(unsigned i=0;i<clip_count144;++i){clip_format144*entry=clip_pages144[i/CLIP_PER_PAGE144]+i%CLIP_PER_PAGE144;if(clip_name_equal144(name,units,entry->name,entry->units))return 0xc000+i;}
 if(clip_count144==CLIP_FORMATS144)return -1816;unsigned page=clip_count144/CLIP_PER_PAGE144;if(!clip_pages144[page]){uint64_t physical=page_alloc();if(!physical)return -8;memset((void*)(uintptr_t)physical,0,4096);clip_pages144[page]=(void*)(uintptr_t)physical;++clipboard_resident144;group_peak142();}
 clip_format144*entry=clip_pages144[page]+clip_count144%CLIP_PER_PAGE144;entry->units=units;memcpy(entry->name,name,(units+1)*2);return 0xc000+clip_count144++;
}
static int64_t clip_name144(uint64_t format,uint64_t output,uint64_t capacity){if(format<0xc000||format-0xc000>=clip_count144||!output||!capacity||capacity>INT32_MAX)return -87;unsigned i=(unsigned)(format-0xc000);clip_format144*entry=clip_pages144[i/CLIP_PER_PAGE144]+i%CLIP_PER_PAGE144;unsigned n=entry->units;if(n>=capacity)n=(unsigned)capacity-1;uint16_t buffer[256];memcpy(buffer,entry->name,n*2);buffer[n]=0;return user8(output,buffer,(n+1)*2,1)?-998:(int64_t)n;}
