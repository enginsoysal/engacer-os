#ifndef ENGACER_BATCH148_H
#define ENGACER_BATCH148_H
/* Bounded command segmentation/expansion. No product names or script bodies. */
static int batch_segment148(const uint16_t*line,unsigned*offset,const uint16_t*self,uint16_t*out,unsigned cap){
 unsigned at=*offset,n=0,quoted=0;if(!line[at])return 0;
 while(line[at]&&tool_space147(line[at]))++at;if(line[at]=='@')++at;
 while(line[at]){unsigned c=line[at++];if(c=='"')quoted^=1;if(!quoted&&c=='&')break;
  if(c=='%'){if(!line[at]||!line[at+1]||!line[at+2]||line[at]!='~'||tool_upper147(line[at+1])!='F'||line[at+2]!='0')return -50;at+=3;for(unsigned j=0;self[j];++j){if(n+1>=cap)return -1816;out[n++]=self[j];}continue;}
  if(!quoted&&c=='>'){if(n&&out[n-1]=='2')--n;while(tool_space147(line[at]))++at;unsigned start=at;while(line[at]&&!tool_space147(line[at])&&line[at]!='&')++at;if(at-start!=3||tool_upper147(line[start])!='N'||tool_upper147(line[start+1])!='U'||tool_upper147(line[start+2])!='L')return -50;continue;}
  if(!quoted&&(c=='|'||c=='<'||c=='^'))return -50;if(n+1>=cap)return -1816;out[n++]=(uint16_t)c;
 }if(quoted)return -87;while(n&&tool_space147(out[n-1]))--n;out[n]=0;*offset=at;return 1;
}
#endif
