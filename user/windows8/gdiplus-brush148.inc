/* Real independently owned ARGB solid brushes, consumed by implemented drawing. */
typedef struct {uint32_t color;} gp_brush148;
static gp_brush148*gp_brushes148[32];
static gp_brush148*gp_brush_find148(const void*p){for(unsigned i=0;i<32;++i)if(p&&gp_brushes148[i]==p)return gp_brushes148[i];return 0;}
static unsigned gp_brush_new148(unsigned color,void**out){if(!gp_references148)return 18;unsigned slot=0;while(slot<32&&gp_brushes148[slot])++slot;if(slot==32)return 3;gp_brush148*b=alloc8(sizeof(*b));if(!b)return 3;b->color=color;gp_brushes148[slot]=b;*out=b;return 0;}
static unsigned MS f_GdipCreateSolidFill(unsigned color,void**out){if(!gp_output148(out))return 2;lock_enter142(&gp_lock148);unsigned status=gp_brush_new148(color,out);lock_leave142(&gp_lock148);return status;}
static unsigned MS f_GdipSetSolidFillColor(void*p,unsigned color){lock_enter142(&gp_lock148);gp_brush148*b=gp_brush_find148(p);if(b)b->color=color;lock_leave142(&gp_lock148);return b?0:2;}
static unsigned MS f_GdipGetSolidFillColor(void*p,unsigned*out){if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,4,2,0,0))return 2;lock_enter142(&gp_lock148);gp_brush148*b=gp_brush_find148(p);if(b)*out=b->color;lock_leave142(&gp_lock148);return b?0:2;}
static unsigned MS f_GdipGetBrushType(void*p,int*out){if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,4,2,0,0))return 2;lock_enter142(&gp_lock148);unsigned valid=gp_brush_find148(p)!=0;if(valid)*out=0;lock_leave142(&gp_lock148);return valid?0:2;}
static unsigned MS f_GdipCloneBrush(void*p,void**out){if(!gp_output148(out))return 2;lock_enter142(&gp_lock148);gp_brush148*b=gp_brush_find148(p);unsigned status=b?gp_brush_new148(b->color,out):2;lock_leave142(&gp_lock148);return status;}
static unsigned MS f_GdipDeleteBrush(void*p){lock_enter142(&gp_lock148);gp_brush148*b=gp_brush_find148(p);if(!b){lock_leave142(&gp_lock148);return 2;}for(unsigned i=0;i<32;++i)if(gp_brushes148[i]==b){gp_brushes148[i]=0;break;}free8(b);lock_leave142(&gp_lock148);return 0;}
