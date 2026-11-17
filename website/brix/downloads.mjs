// Keep current downloads obvious and historical pages bounded as releases grow.
import assert from 'node:assert/strict';
export function releaseGroups(releases,currentTag){
 const current=releases.find(r=>r.tag_name===currentTag)||releases[0];
 const history=releases.filter(r=>r!==current),archives=[];
 for(let i=0;i<history.length;i+=8)archives.push(history.slice(i,i+8));
 return {current:current?[current]:[],archives};
}
export function documentationRef(env){
 const requested=env.ENGACER_DOCS_REF||(env.GITHUB_EVENT_NAME==='release'?env.GITHUB_SHA:null);
 if(!requested)return 'HEAD';
 assert(/^[a-f0-9]{40}$/.test(requested),'Documentation source must be a full canonical commit');
 return requested;
}
export function assertPostBounds(posts){
 for(const post of posts){
  assert(Buffer.byteLength(JSON.stringify(post))<=240*1024,`Article exceeds bounded API payload: ${post.slug}`);
  assert(post.blocks.length<=500,`Article exceeds bounded block count: ${post.slug}`);
 }
}
