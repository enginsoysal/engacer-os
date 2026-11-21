/* Shell argv ownership is one LocalFree-compatible process allocation. */
static unsigned argv_space148(WCHAR c){return c==' '||c=='\t';}
static unsigned argv_parse148(const WCHAR*input,unsigned length,WCHAR**argv,WCHAR*storage,unsigned limit){
 unsigned at=0,out=0,count=1;if(argv){if(!limit)return 0;argv[0]=storage;}
#define ARGV_EMIT148(c) do{if(storage)storage[out]=(WCHAR)(c);++out;}while(0)
 if(length&&input[0]=='"'){++at;while(at<length&&input[at]!='"'){ARGV_EMIT148(input[at]);++at;}if(at<length)++at;}
 else while(at<length&&!argv_space148(input[at])){ARGV_EMIT148(input[at]);++at;}
 ARGV_EMIT148(0);
 while(at<length){while(at<length&&argv_space148(input[at]))++at;if(at==length)break;if(argv){if(count==limit)return 0;argv[count]=storage+out;}++count;unsigned quoted=0;
  while(at<length&&(quoted||!argv_space148(input[at]))){unsigned slashes=0;while(at<length&&input[at]=='\\'){++slashes;++at;}
   if(at<length&&input[at]=='"'){for(unsigned i=0;i<slashes/2;++i)ARGV_EMIT148('\\');if(slashes&1){ARGV_EMIT148('"');++at;}else if(quoted&&at+1<length&&input[at+1]=='"'){ARGV_EMIT148('"');at+=2;quoted=0;}else{quoted^=1;++at;}continue;}
   for(unsigned i=0;i<slashes;++i)ARGV_EMIT148('\\');if(at==length||(!quoted&&argv_space148(input[at])))break;ARGV_EMIT148(input[at]);++at;
  }ARGV_EMIT148(0);
 }
 if(argv)argv[count]=0;
#undef ARGV_EMIT148
 return count;
}
static WCHAR**MS f_CommandLineToArgvW(const WCHAR*input,int*argc){
 if(!argc||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)argc,4,2,0,0)||!input){last8(87);return 0;}*argc=0;unsigned length=0;
 while(length<32768){uint64_t address=(uint64_t)(uintptr_t)(input+length);unsigned units=(4096-(unsigned)(address&4095))/2;if(!units)units=1;if(units>32768-length)units=32768-length;if(sys8(W8_SYS_ACCESS,address,units*2,1,0,0)){last8(998);return 0;}unsigned end=length+units;while(length<end&&input[length])++length;if(length<end)break;}
 if(length==32768){last8(206);return 0;}WCHAR module[512];if(!length){length=f_GetModuleFileNameW(0,module,512);if(!length||length>=512)return 0;WCHAR**result=alloc8(16+((size_t)length+1)*2);if(!result){last8(8);return 0;}result[0]=(WCHAR*)(result+2);result[1]=0;memcpy(result[0],module,((size_t)length+1)*2);*argc=1;return result;}
 unsigned count=argv_parse148(input,length,0,0,0);WCHAR**result=alloc8(((size_t)count+1)*8+((size_t)length+2)*2);if(!result){last8(8);return 0;}
 unsigned actual=argv_parse148(input,length,result,(WCHAR*)(result+count+1),count);if(!actual){free8(result);last8(87);return 0;}*argc=(int)actual;return result;
}
