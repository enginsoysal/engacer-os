/* Real row-vector affine state; bounded independently owned matrix values. */
#define GT148 __attribute__((target("sse2")))
#include "transform-math148.h"
typedef struct {float elements[6];} gp_matrix148;
static gp_matrix148*gp_matrices148[32];
static gp_matrix148*gp_matrix_find148(const void*p){for(unsigned i=0;i<32;++i)if(p&&gp_matrices148[i]==p)return gp_matrices148[i];return 0;}

static unsigned GT148 gp_transform_identity148(const gp_graphics148*g){const float*m=g->world148;return m[0]==1.0f&&m[1]==0.0f&&m[2]==0.0f&&m[3]==1.0f&&m[4]==0.0f&&m[5]==0.0f;}


static unsigned GT148 gp_world_apply148(void*pointer,const float*operation,int order){if(!gp_matrix_valid148(operation))return 2;lock_enter142(&gp_lock148);gp_graphics148*g=gp_context_find148(pointer);unsigned status=g?gp_matrix_combine148(g->world148,operation,order):2;lock_leave142(&gp_lock148);return status;}
static unsigned MS GT148 f_GdipRotateWorldTransform(void*g,float angle,int order){float operation[6];unsigned status=gp_rotation148(angle,operation);return status?status:gp_world_apply148(g,operation,order);}
static unsigned MS GT148 f_GdipTranslateWorldTransform(void*g,float x,float y,int order){float operation[6]={1,0,0,1,x,y};return gp_world_apply148(g,operation,order);}
static unsigned MS GT148 f_GdipScaleWorldTransform(void*g,float x,float y,int order){float operation[6]={x,0,0,y,0,0};return gp_world_apply148(g,operation,order);}
static unsigned MS f_GdipResetWorldTransform(void*p){lock_enter142(&gp_lock148);gp_graphics148*g=gp_context_find148(p);if(g){const float identity[6]={1,0,0,1,0,0};memcpy(g->world148,identity,sizeof(identity));}lock_leave142(&gp_lock148);return g?0:2;}
static unsigned gp_matrix_new148(const float*elements,void**out){if(!gp_output148(out))return 2;if(!gp_references148)return 18;unsigned slot=0;while(slot<32&&gp_matrices148[slot])++slot;if(slot==32)return 3;gp_matrix148*m=alloc8(sizeof(*m));if(!m)return 3;memcpy(m->elements,elements,24);gp_matrices148[slot]=m;*out=m;return 0;}
static unsigned MS f_GdipCreateMatrix(void**out){const float identity[6]={1,0,0,1,0,0};lock_enter142(&gp_lock148);unsigned status=gp_matrix_new148(identity,out);lock_leave142(&gp_lock148);return status;}
static unsigned MS GT148 f_GdipCreateMatrix2(float a,float b,float c,float d,float x,float y,void**out){float elements[6]={a,b,c,d,x,y};if(!gp_matrix_valid148(elements))return 2;lock_enter142(&gp_lock148);unsigned status=gp_matrix_new148(elements,out);lock_leave142(&gp_lock148);return status;}
static unsigned MS f_GdipDeleteMatrix(void*p){lock_enter142(&gp_lock148);gp_matrix148*m=gp_matrix_find148(p);if(!m){lock_leave142(&gp_lock148);return 2;}for(unsigned i=0;i<32;++i)if(gp_matrices148[i]==m){gp_matrices148[i]=0;break;}free8(m);lock_leave142(&gp_lock148);return 0;}
static unsigned MS f_GdipGetMatrixElements(void*p,float*out){if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,24,2,0,0))return 2;lock_enter142(&gp_lock148);gp_matrix148*m=gp_matrix_find148(p);if(m)memcpy(out,m->elements,24);lock_leave142(&gp_lock148);return m?0:2;}
static unsigned MS f_GdipGetWorldTransform(void*p,void*matrix){lock_enter142(&gp_lock148);gp_matrix148*m=gp_matrix_find148(matrix);gp_graphics148*g=gp_context_find148(p);if(m&&g)memcpy(m->elements,g->world148,24);lock_leave142(&gp_lock148);return m&&g?0:2;}
static unsigned MS f_GdipSetWorldTransform(void*p,void*matrix){lock_enter142(&gp_lock148);gp_matrix148*m=gp_matrix_find148(matrix);gp_graphics148*g=gp_context_find148(p);if(m&&g)memcpy(g->world148,m->elements,24);lock_leave142(&gp_lock148);return m&&g?0:2;}
static unsigned MS GT148 f_GdipMultiplyWorldTransform(void*p,void*matrix,int order){lock_enter142(&gp_lock148);gp_matrix148*m=gp_matrix_find148(matrix);gp_graphics148*g=gp_context_find148(p);unsigned status=m&&g?gp_matrix_combine148(g->world148,m->elements,order):2;lock_leave142(&gp_lock148);return status;}
#undef GT148
