/* Formatted measurement uses the same real raster strikes as native text. */
typedef struct {float x,y,width,height;} gp_rect148;
static unsigned gp_text_input148(const WCHAR*input,int count,WCHAR*out,unsigned*length){
 if(!input||count< -1||count>159)return 2;unsigned units=count<0?0:(unsigned)count;if(count<0){while(units<160){uint64_t address=(uint64_t)(uintptr_t)(input+units);unsigned span=(4096-(unsigned)(address&4095))/2;if(!span)span=1;if(span>160-units)span=160-units;if(sys8(W8_SYS_ACCESS,address,span*2,1,0,0))return 2;unsigned end=units+span;while(units<end&&input[units])++units;if(units<end)break;}if(units==160)return 11;}
 if(units&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,units*2,1,0,0))return 2;if(units)memcpy(out,input,units*2);out[units]=0;for(unsigned i=0;i<units;++i)if(!out[i])return 6;*length=units;return 0;
}
static unsigned gp_text_width148(const WCHAR*text,unsigned count,unsigned em,unsigned*width){wui_draw144 draw={0};if(!text_command144(text,(int)count,&draw))return 2;ui_raster_info148 info;ui_raster_request148 request={.output=(uint64_t)(uintptr_t)&info,.capacity=sizeof(info)};memcpy(request.text,draw.text,sizeof(request.text));int64_t bytes=ui_call144(WUI_RASTER148,em,&request,0);if(bytes<0)return bytes==-8?3:2;*width=info.width;return 0;}
static unsigned MS __attribute__((target("sse2"))) f_GdipMeasureString(void*graphics,const WCHAR*input,int count,void*font,const gp_rect148*layout,void*format,gp_rect148*out,int*fitted,int*filled){
 if(!layout||!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)layout,sizeof(*layout),1,0,0)||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,sizeof(*out),2,0,0)||(fitted&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)fitted,4,2,0,0))||(filled&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)filled,4,2,0,0)))return 2;
 gp_rect148 box=*layout;if(!(box.x>=-10000000.0f&&box.x<=10000000.0f&&box.y>=-10000000.0f&&box.y<=10000000.0f&&box.width>=0.0f&&box.width<=10000000.0f&&box.height>=0.0f&&box.height<=10000000.0f))return 2;WCHAR text[160];unsigned units=0,status=gp_text_input148(input,count,text,&units);if(status)return status;
 lock_enter142(&ui_lock144);lock_enter142(&gp_lock148);gp_graphics148*g=gp_context_find148(graphics);gp_font148*f=gp_font_find148(font);gp_format148 defaults={.trimming=1};gp_format148*fmt=format?gp_format_find148(format):&defaults;ui_font_metrics148 m;
 if(!g||!f||!fmt||(g->dc&&!dc_lookup144(g->dc))||!font_info148(f->font,&m,0)){status=2;goto done;}
 if((fmt->flags&~0x7804u)||fmt->trimming>1||(g->settings[3]!=1&&g->settings[3]!=2&&g->settings[3]!=3)){status=6;goto done;}
 unsigned at=0,lines=0,maximum=0;while(at<units){unsigned start=at;while(at<units&&text[at]!='\r'&&text[at]!='\n'){if(text[at]=='\t'){status=6;goto done;}++at;}unsigned used=at-start;if(!(fmt->flags&0x800))while(used&&text[start+used-1]==' ')--used;unsigned width;if((status=gp_text_width148(text+start,used,m.em,&width)))goto done;if(width>maximum)maximum=width;if(++lines>32){status=11;goto done;}if(at<units){WCHAR ch=text[at++];if(ch=='\r'&&at<units&&text[at]=='\n')++at;}}
 float factor=g->settings[3]==3?0.75f:1.0f,padding=units&&!(fmt->flags&4)?(float)m.em/3.0f:0.0f,width=((float)maximum+padding)*factor,height=(float)(lines*m.height)*factor;
 /* Wrapped, clipped and partial-fit layout must be implemented before it succeeds. */
 if((box.width>0&&width>box.width)||(box.height>0&&height>box.height)){print8("Unsupported GDI+ text layout: wrapped or partial-fit rectangle.\n");status=6;goto done;}
 gp_rect148 result={box.x,box.y,width,height};if(box.width>0&&fmt->align)result.x+=(box.width-width)*(fmt->align==1?0.5f:1.0f);if(box.height>0&&fmt->line_align)result.y+=(box.height-height)*(fmt->line_align==1?0.5f:1.0f);*out=result;if(fitted)*fitted=(int)units;if(filled)*filled=(int)lines;status=0;
 done:lock_leave142(&gp_lock148);lock_leave142(&ui_lock144);return status;
}
