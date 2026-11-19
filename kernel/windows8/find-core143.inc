/* Selected Unicode scalar wildcard profile, with one shared invariant case table. */
static unsigned find_match_core143(const char*pattern,unsigned pn,const char*name,unsigned nn,unsigned*matched){
 unsigned at=0;uint32_t scalar;while(at<pn)if(!decode_utf8_143(pattern,pn,&at,&scalar))return 1113;at=0;while(at<nn)if(!decode_utf8_143(name,nn,&at,&scalar))return 1113;
 unsigned pi=0,ni=0,star=UINT32_MAX,retry=0;
 while(ni<nn){
  if(pi<pn&&pattern[pi]=='*'){star=++pi;retry=ni;continue;}
  unsigned next_name=ni,next_pattern=pi;uint32_t nc,pc=0;decode_utf8_143(name,nn,&next_name,&nc);
  if(pi<pn&&decode_utf8_143(pattern,pn,&next_pattern,&pc)&&(pc=='?'||fold143(pc)==fold143(nc))){ni=next_name;pi=next_pattern;continue;}
  if(star!=UINT32_MAX&&retry<nn){decode_utf8_143(name,nn,&retry,&nc);ni=retry;pi=star;continue;}
  *matched=0;return 0;
 }
 while(pi<pn&&pattern[pi]=='*')++pi;
 *matched=pi==pn||(pn-pi==2&&pattern[pi]=='.'&&pattern[pi+1]=='*');return 0;
}
