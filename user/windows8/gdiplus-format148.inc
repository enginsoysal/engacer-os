/* Independent text-format objects retain actual caller choices and range copies. */
typedef struct {int first,length;} gp_range148;
typedef struct {int flags,align,line_align,trimming,range_count;unsigned language;gp_range148 ranges[32];} gp_format148;
static gp_format148*gp_formats148[32];
static gp_format148*gp_format_find148(const void*p){for(unsigned i=0;i<32;++i)if(p&&gp_formats148[i]==p)return gp_formats148[i];return 0;}
static unsigned gp_format_new148(const gp_format148*source,void**out){if(!gp_references148)return 18;unsigned slot=0;while(slot<32&&gp_formats148[slot])++slot;if(slot==32)return 3;gp_format148*f=alloc8(sizeof(*f));if(!f)return 3;*f=*source;gp_formats148[slot]=f;*out=f;return 0;}
static unsigned MS f_GdipCreateStringFormat(int flags,unsigned language,void**out){if(!gp_output148(out))return 2;gp_format148 value={.flags=flags,.trimming=1,.language=language&65535};lock_enter142(&gp_lock148);unsigned status=gp_format_new148(&value,out);lock_leave142(&gp_lock148);return status;}
static unsigned MS f_GdipStringFormatGetGenericDefault(void**out){return f_GdipCreateStringFormat(0,0,out);}
static unsigned MS f_GdipStringFormatGetGenericTypographic(void**out){if(!gp_output148(out))return 2;gp_format148 value={.flags=0x6004};lock_enter142(&gp_lock148);unsigned status=gp_format_new148(&value,out);lock_leave142(&gp_lock148);return status;}
static unsigned MS f_GdipCloneStringFormat(void*p,void**out){if(!gp_output148(out))return 2;lock_enter142(&gp_lock148);gp_format148*f=gp_format_find148(p);unsigned status=f?gp_format_new148(f,out):2;lock_leave142(&gp_lock148);return status;}
static unsigned MS f_GdipDeleteStringFormat(void*p){lock_enter142(&gp_lock148);gp_format148*f=gp_format_find148(p);if(!f){lock_leave142(&gp_lock148);return 2;}for(unsigned i=0;i<32;++i)if(gp_formats148[i]==f){gp_formats148[i]=0;break;}free8(f);lock_leave142(&gp_lock148);return 0;}
static unsigned gp_format_property148(void*p,unsigned property,int*value,unsigned write){if(!value||(!write&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)value,4,2,0,0)))return 2;int next=write?*value:0;if(write&&property&&((property==3&&(next<0||next>5))||(property!=3&&(next<0||next>2))))return 2;lock_enter142(&gp_lock148);gp_format148*f=gp_format_find148(p);if(!f){lock_leave142(&gp_lock148);return 2;}int*field=property==0?&f->flags:property==1?&f->align:property==2?&f->line_align:&f->trimming;if(write)*field=next;else *value=*field;lock_leave142(&gp_lock148);return 0;}
#define GP_FORMAT_PROPERTY148(name,index) static unsigned MS f_GdipSetStringFormat##name(void*p,int value){return gp_format_property148(p,index,&value,1);}static unsigned MS f_GdipGetStringFormat##name(void*p,int*out){return gp_format_property148(p,index,out,0);}
GP_FORMAT_PROPERTY148(Flags,0)
GP_FORMAT_PROPERTY148(Align,1)
GP_FORMAT_PROPERTY148(LineAlign,2)
GP_FORMAT_PROPERTY148(Trimming,3)
#undef GP_FORMAT_PROPERTY148
static unsigned MS f_GdipSetStringFormatMeasurableCharacterRanges(void*p,int count,const gp_range148*input){if(!input)return 2;if(count>32)return 11;if(count>0&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,(unsigned)count*sizeof(*input),1,0,0))return 2;lock_enter142(&gp_lock148);gp_format148*f=gp_format_find148(p);if(!f){lock_leave142(&gp_lock148);return 2;}if(count>0)memcpy(f->ranges,input,(unsigned)count*sizeof(*input));f->range_count=count>0?count:0;lock_leave142(&gp_lock148);return 0;}
static unsigned MS f_GdipGetStringFormatMeasurableCharacterRangeCount(void*p,int*out){if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,4,2,0,0))return 2;lock_enter142(&gp_lock148);gp_format148*f=gp_format_find148(p);if(f)*out=f->range_count;lock_leave142(&gp_lock148);return f?0:2;}
