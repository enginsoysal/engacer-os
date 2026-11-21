/* Checked same-process client/screen translation, with no geometry mutation. */
static int MS f_MapWindowPoints(HANDLE from,HANDLE to,void*points,unsigned count){
 if(count>64){last8(87);return 0;}int source_x=0,source_y=0,target_x=0,target_y=0;wui_view144 view;
 if(from&&from!=DESKTOP_HANDLE148){if(!window_view144(from,&view))return 0;if(view.description.exstyle&0x400000u){last8(50);return 0;}if(!window_origin144(from,&source_x,&source_y))return 0;}
 if(to&&to!=DESKTOP_HANDLE148){if(!window_view144(to,&view))return 0;if(view.description.exstyle&0x400000u){last8(50);return 0;}if(!window_origin144(to,&target_x,&target_y))return 0;}
 int64_t dx=(int64_t)source_x-target_x,dy=(int64_t)source_y-target_y;int32_t copy[128];if(from==to)dx=dy=0;if(count&&(!points||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)points,(uint64_t)count*8,3,0,0))){last8(998);return 0;}if(count)memcpy(copy,points,count*8);
 for(unsigned i=0;i<count;++i){int64_t x=(int64_t)copy[i*2]+dx,y=(int64_t)copy[i*2+1]+dy;if(x<INT32_MIN||x>INT32_MAX||y<INT32_MIN||y>INT32_MAX){last8(87);return 0;}copy[i*2]=(int)x;copy[i*2+1]=(int)y;}
 if(count)memcpy(points,copy,count*8);return(int)(((unsigned)dx&65535u)|(((unsigned)dy&65535u)<<16));
}
