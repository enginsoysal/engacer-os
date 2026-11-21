/* SID serialization is data handling, never a grant of native authority. */
static unsigned sid_size148(const void*pointer){
 if(!pointer||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)pointer,8,1,0,0))return 0;const uint8_t*sid=pointer;
 if(sid[0]!=1||sid[1]>15)return 0;unsigned bytes=8+(unsigned)sid[1]*4;if(sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)pointer,bytes,1,0,0))return 0;return bytes;
}
static int MS f_AllocateAndInitializeSid(const uint8_t*authority,uint8_t count,unsigned s0,unsigned s1,unsigned s2,unsigned s3,unsigned s4,unsigned s5,unsigned s6,unsigned s7,void**out){
 if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,8,2,0,0)){last8(87);return 0;}*out=0;
 if(!authority||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)authority,6,1,0,0)){last8(87);return 0;}if(count>8){last8(1337);return 0;}
 uint8_t*sid=alloc8(8+(size_t)count*4);if(!sid){last8(8);return 0;}sid[0]=1;sid[1]=count;memcpy(sid+2,authority,6);unsigned values[8]={s0,s1,s2,s3,s4,s5,s6,s7};memcpy(sid+8,values,(size_t)count*4);*out=sid;return 1;
}
static void*MS f_FreeSid(void*pointer){if(!pointer)return 0;if(allocation_size8(pointer)==SIZE_MAX){last8(87);return pointer;}free8(pointer);return 0;}
static int MS f_IsValidSid(const void*sid){return sid_size148(sid)!=0;}
static unsigned MS f_GetLengthSid(const void*sid){unsigned size=sid_size148(sid);if(!size)last8(1337);return size;}
static int MS f_EqualSid(const void*a,const void*b){unsigned first=sid_size148(a),second=sid_size148(b);if(!first||!second){last8(1337);return 0;}return first==second&&!memcmp(a,b,first);}
