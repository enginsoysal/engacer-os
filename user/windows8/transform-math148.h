#ifndef ENGACER_TRANSFORM_MATH148_H
#define ENGACER_TRANSFORM_MATH148_H
#define GMATH148 __attribute__((target("sse2")))
static unsigned GMATH148 gp_matrix_valid148(const float*m){for(unsigned i=0;i<6;++i)if(!(m[i]>=-10000000.0f&&m[i]<=10000000.0f))return 0;return 1;}
static unsigned GMATH148 gp_matrix_combine148(float*target,const float*operation,int order){
 if(order!=0&&order!=1)return 2;const float*a=order?target:operation,*b=order?operation:target;float out[6]={a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3],a[4]*b[0]+a[5]*b[2]+b[4],a[4]*b[1]+a[5]*b[3]+b[5]};if(!gp_matrix_valid148(out))return 2;memcpy(target,out,sizeof(out));return 0;
}
static unsigned GMATH148 gp_rotation148(float angle,float*out){
 if(!(angle>=-10000000.0f&&angle<=10000000.0f))return 2;double degrees=angle;degrees-=(int)(degrees/360.0)*360.0;if(degrees>180.0)degrees-=360.0;if(degrees< -180.0)degrees+=360.0;double x=degrees*0.017453292519943295769,sign=1.0;if(x>1.5707963267948966){x=3.141592653589793-x;sign=-1.0;}else if(x< -1.5707963267948966){x=-3.141592653589793-x;sign=-1.0;}double q=x*x;
 double sine=x*(1.0+q*(-1.0/6.0+q*(1.0/120.0+q*(-1.0/5040.0+q*(1.0/362880.0+q*(-1.0/39916800.0+q/6227020800.0))))));double cosine=sign*(1.0+q*(-1.0/2.0+q*(1.0/24.0+q*(-1.0/720.0+q*(1.0/40320.0+q*(-1.0/3628800.0+q/479001600.0))))));out[0]=(float)cosine;out[1]=(float)sine;out[2]=(float)-sine;out[3]=(float)cosine;out[4]=out[5]=0;return 0;
}
#undef GMATH148
#endif
