/* CALCRECT performs real selected-font measurement; unsupported painting refuses. */
static int MS f_DrawTextExW(HANDLE dc,WCHAR*input,int count,win_rect144*out,unsigned format,void*parameters){
 native_dc144*d=dc_lookup144(dc);if(!d)return 0;if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,sizeof(*out),3,0,0)){last8(998);return 0;}
 if(parameters||!(format&0x400u)||(format&~0x2f20u)){last8(50);return 0;}if(count< -1||count>159||(!input&&count)){last8(87);return 0;}
 unsigned units=count<0?0:(unsigned)count;WCHAR source[160];if(count<0){while(units<160){uint64_t address=(uint64_t)(uintptr_t)(input+units);unsigned span=(4096-(unsigned)(address&4095))/2;if(!span)span=1;if(span>160-units)span=160-units;if(sys8(W8_SYS_ACCESS,address,span*2,1,0,0)){last8(998);return 0;}unsigned end=units+span;while(units<end&&input[units])++units;if(units<end)break;}if(units==160){last8(206);return 0;}}
 if(units&&sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)input,units*2,1,0,0)){last8(998);return 0;}if(units)memcpy(source,input,units*2);source[units]=0;
 WCHAR line[160];unsigned length=0,lines=0,maximum=0;ui_font_metrics148 m;if(!font_info148(d->font,&m,0))return 0;
 for(unsigned at=0;at<units;++at){WCHAR ch=source[at];if(!ch)break;if(ch=='\t'){last8(50);return 0;}
  if(ch=='&'&&!(format&0x800u)){if(at+1>=units)continue;if(source[at+1]=='&')++at;else continue;}
  if(ch=='\r'||ch=='\n'){if(ch=='\r'&&at+1<units&&source[at+1]=='\n')++at;if(format&0x20u)continue;int size[2];if(!f_GetTextExtentPoint32W(dc,line,(int)length,size))return 0;if((unsigned)size[0]>maximum)maximum=(unsigned)size[0];++lines;length=0;continue;}
  line[length++]=ch;
 }
 if(length||(format&0x20u)){int size[2];if(!f_GetTextExtentPoint32W(dc,line,(int)length,size))return 0;if((unsigned)size[0]>maximum)maximum=(unsigned)size[0];++lines;}
 uint64_t height=(uint64_t)lines*m.height;int64_t right=(int64_t)out->left+maximum,bottom=(int64_t)out->top+(int64_t)height;if(right>INT32_MAX||bottom>INT32_MAX){last8(87);return 0;}out->right=(int)right;out->bottom=(int)bottom;return height?(int)height:1;
}
static int MS f_DrawTextW(HANDLE dc,const WCHAR*text,int count,win_rect144*out,unsigned flags){return f_DrawTextExW(dc,(WCHAR*)text,count,out,flags,0);}
