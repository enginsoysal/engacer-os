/* One actual native monitor, in the compatibility coordinate space. */
#define MONITOR_HANDLE148 UINT64_C(0x4d000001)
static HANDLE MS f_MonitorFromRect(const win_rect144*input,unsigned flags){
 if(flags>2){last8(87);return 0;}if(!input||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,sizeof(*input),1,0,0)){last8(998);return 0;}win_rect144 r=*input;int64_t left=r.left,right=r.right,top=r.top,bottom=r.bottom;if(right<=left||bottom<=top){right=left+1;bottom=top+1;}wui_metrics144 m;if(!window_metrics144(&m))return 0;return flags||(left<(int64_t)m.width&&right>0&&top<(int64_t)m.height&&bottom>0)?MONITOR_HANDLE148:0;
}
static HANDLE MS f_MonitorFromPoint(uint64_t point,unsigned flags){if(flags>2){last8(87);return 0;}int32_t x=(int32_t)point,y=(int32_t)(point>>32);wui_metrics144 m;if(!window_metrics144(&m))return 0;return flags||(x>=0&&y>=0&&(unsigned)x<m.width&&(unsigned)y<m.height)?MONITOR_HANDLE148:0;}
static int monitor_info148(HANDLE monitor,void*out,unsigned wide){
 if(monitor!=MONITOR_HANDLE148){last8(87);return 0;}if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,4,1,0,0)){last8(998);return 0;}unsigned bytes=*(unsigned*)out;if(bytes!=40&&bytes!=(wide?104u:72u)){last8(87);return 0;}if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,bytes,3,0,0)){last8(998);return 0;}wui_metrics144 m;if(!window_metrics144(&m))return 0;win_rect144*r=(void*)((uint8_t*)out+4);r[0]=(win_rect144){0,0,(int)m.width,(int)m.height};r[1]=(win_rect144){0,0,(int)m.width,(int)m.work_height};*(unsigned*)((uint8_t*)out+36)=1;if(bytes!=40){memset((uint8_t*)out+40,0,wide?64:32);if(wide)memcpy((uint8_t*)out+40,u"Engacer Display",sizeof(u"Engacer Display"));else copy8((char*)out+40,"Engacer Display",32);}return 1;
}
static int MS f_GetMonitorInfoW(HANDLE monitor,void*out){return monitor_info148(monitor,out,1);}
