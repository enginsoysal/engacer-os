/* Pure MAX_PATH shell string operation: no filesystem access or authority. */
static unsigned pathappend_length148(const WCHAR*s){unsigned n=0;if(!s)return 260;while(n<260&&s[n])++n;return n;}
static int MS f_PathAppendW(WCHAR*path,const WCHAR*more){
 unsigned a=pathappend_length148(path),b=pathappend_length148(more);
 if(!path||!more){last8(87);return 0;}
 if(a==260||b==260){path[0]=0;last8(87);return 0;}
 WCHAR raw[260],clean[260];unsigned n=0,start=0;
 unsigned replace=(b>=2&&more[1]==':')||(b>=2&&more[0]=='\\'&&more[1]=='\\');
 if(!replace){for(unsigned i=0;i<a;++i)raw[n++]=path[i];if(b&&more[0]=='\\')start=1;if(n&&b>start&&raw[n-1]!='\\'){if(n==259){path[0]=0;last8(206);return 0;}raw[n++]='\\';}}
 if(b-start>=260-n){path[0]=0;last8(206);return 0;}
 for(unsigned i=start;i<b;++i)raw[n++]=more[i];raw[n]=0;
 unsigned component_units=0;for(unsigned i=0;i<n;++i){if(raw[i]=='\\')component_units=0;else if(++component_units>256){path[0]=0;last8(206);return 0;}}
 unsigned at=0,used=0,root=0;
 if(n>=4&&raw[0]=='\\'&&raw[1]=='\\'&&raw[2]=='?'&&raw[3]=='\\'){at=4;}
 if(n-at>=2&&raw[at+1]==':'){clean[used++]=raw[at++];clean[used++]=raw[at++];if(raw[at]=='\\')clean[used++]=raw[at++];root=used;}
 else if(n-at>=2&&raw[at]=='\\'&&raw[at+1]=='\\'){
  clean[used++]='\\';clean[used++]='\\';at+=2;
  while(at<n&&raw[at]!='\\')clean[used++]=raw[at++];if(at<n)clean[used++]=raw[at++];root=used;
 }else if(raw[at]=='\\'){clean[used++]=raw[at++];root=used;}
 while(at<n){
  unsigned component=at==0||raw[at-1]=='\\'||(at==2&&raw[1]==':');
  if(component&&raw[at]=='.'&&(at+1==n||raw[at+1]=='\\')){
   if(at+1==n&&used>root&&clean[used-1]=='\\')--used;
   at+=1+(at+1<n);continue;
  }
  if(component&&raw[at]=='.'&&at+1<n&&raw[at+1]=='.'&&(at+2==n||raw[at+2]=='\\')){
   unsigned had=used>root;
   if(used>root&&clean[used-1]=='\\')--used;
   while(used>root&&clean[used-1]!='\\')--used;
   if(had&&!used){clean[used++]='\\';root=used;}
   if(at+2==n&&used>1&&clean[used-1]=='\\'&&!(used==3&&clean[1]==':'))--used;
   at+=2+(at+2<n);continue;
  }
  clean[used++]=raw[at++];
 }
 while(used>root&&clean[used-1]=='.')--used;
 if(used==2&&clean[1]==':')clean[used++]='\\';
 if(!used)clean[used++]='\\';clean[used]=0;
 memcpy(path,clean,(used+1)*sizeof(WCHAR));return 1;
}
