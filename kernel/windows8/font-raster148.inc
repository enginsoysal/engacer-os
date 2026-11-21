/* Only copied public glyph coverage crosses the user boundary. */
static unsigned ui_raster_write_user148(void*context,unsigned offset,const uint8_t*bytes,unsigned count){uint64_t output=*(const uint64_t*)context;return !user8(output+offset,(void*)bytes,count,1);}
static int64_t ui_raster_call148(uint64_t em,uint64_t pointer){
 ui_raster_request148 request;if(em>UINT32_MAX||user8(pointer,&request,sizeof(request),0)||request.render>1||!terminated142(request.text,512))return -87;
 if(request.capacity<sizeof(ui_raster_info148)||request.capacity>UI_RASTER_CAP148||request.output<W8_BASE||request.output>=W8_LIMIT||request.capacity>W8_LIMIT-request.output)return -87;
 ui_raster_line148*line=ui_page144();if(!line)return -8;int64_t result=-87;unsigned bytes=ui148_raster_plan((unsigned)em,request.text,line);if(!bytes)goto done;
 if(request.render&&request.capacity<bytes){result=-122;goto done;}unsigned extent=request.render?bytes:sizeof(ui_raster_info148);
 for(uint64_t at=request.output&~UINT64_C(4095);at<request.output+extent;at+=4096){uint64_t*p=pte8(at,0);if(!p||!(*p&(1|RESERVED141))||!(*p&2)){result=-998;goto done;}}
 if(user8(request.output,line,request.render?sizeof(*line):sizeof(ui_raster_info148),1)||(request.render&&!ui148_raster_emit((unsigned)em,request.text,line,ui_raster_write_user148,&request.output))){result=-998;goto done;}result=bytes;
 done:ui_free144(line);return result;
}
