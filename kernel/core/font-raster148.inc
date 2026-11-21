/* Canonical 96-DPI glyph packets reuse immutable OFL native coverage. */
static const font73_face*raster_face148(unsigned tag){unsigned em=tag&0xffffu,kind=tag&0xffff0000u,index=UINT32_MAX;
 if(!kind)index=em==14?12:em==16?0:em==21?15:em==28?18:UINT32_MAX;
 else if(kind==UI_FONT_REGULAR148)index=em==14?12:em==16?0:em==21?13:em==24?1:em==28?14:em==32?2:UINT32_MAX;
 else if(kind==UI_FONT_SEMIBOLD148)index=em==21?15:em==28?18:em==32?16:em==42?17:em==56?20:UINT32_MAX;
 return index<sizeof(font73_faces)/sizeof(*font73_faces)&&font73_faces[index].size==em?font73_faces+index:0;}
unsigned ui148_raster_plan(unsigned em,const char*text,ui_raster_line148*out){
 const font73_face*f=raster_face148(em);if(!f||!text||!out)return 0;memset(out,0,sizeof(*out));out->bytes=sizeof(*out);out->height=f->height;out->ascent=f->ascent;out->em=f->size;
 for(unsigned at=0;at<512&&text[at];){uint32_t code=font146_next(text,&at,512);if(code<32||out->count==160)return 0;unsigned base;const font73_glyph*g=font146_lookup(f,code,&base);unsigned bytes=(unsigned)g->width*g->height;if(g->width>64||g->height>UI_RASTER_MAX_HEIGHT148||bytes>UI_RASTER_CAP148-out->bytes)return 0;out->glyphs[out->count++]=(ui_raster_glyph148){out->bytes,g->width,g->height,g->x,g->y,g->advance};out->bytes+=bytes;out->width+=g->advance;}
 return out->bytes;
}
unsigned ui148_raster_emit(unsigned em,const char*text,const ui_raster_line148*line,ui_raster_write148 write,void*context){
 const font73_face*f=raster_face148(em);if(!f||!text||!line||!write)return 0;unsigned at=0;
 for(unsigned n=0;n<line->count;++n){uint32_t code=font146_next(text,&at,512);unsigned base;const font73_glyph*g=font146_lookup(f,code,&base);const ui_raster_glyph148*d=line->glyphs+n;uint8_t row[64];if(d->width!=g->width||d->height!=g->height||g->width>sizeof(row))return 0; font146_sampler sample=font146_sample_begin(g,base);
  for(unsigned y=0;y<g->height;++y){for(unsigned x=0;x<g->width;++x)row[x]=(uint8_t)font146_sample(&sample,x,y);if(g->width&&!write(context,d->offset+y*g->width,row,g->width))return 0;}
  if(sample.delta.bad||sample.base.bad)return 0;
 }return 1;
}
