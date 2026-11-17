#ifndef ENGACER_SEARCH12_H
#define ENGACER_SEARCH12_H
/* ASCII catalogue labels and query are validated bounded strings. Rank exact,
 * prefix, then substring matches; never inspect executable paths or scan disk. */
static inline unsigned search12_fold(unsigned c){return c>='A'&&c<='Z'?c+32:c;}
static inline unsigned search12_rank(const char *label,const char *query){
 if(!label||!query)return 3;
 if(!*query)return 1;
 for(unsigned i=0;label[i];++i){
  unsigned n=0;
  while(query[n]&&label[i+n]&&search12_fold((unsigned char)label[i+n])==search12_fold((unsigned char)query[n]))++n;
  if(!query[n])return i?2:label[n]?1:0;
 }
 return 3;
}
#endif
