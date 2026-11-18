// Keep current downloads obvious and historical pages bounded as releases grow.
import assert from 'node:assert/strict';
export function stabilityWarning13(progress){
 if(!(progress.owner_additions||[]).some(issue=>issue.id==='long-uptime-freeze'&&issue.status!=='resolved'))return '';
 return '<p><strong>Known freezes — testing only.</strong> Frequent freezes are reported on M13.8, following the earlier M13.7 report. Do not use these media for everyday work. Stability is not qualified. M13.9 addresses the faults; M13.12 covers integration and <a href="/blog/docs-milestones-m13-13">M13.13 is the blocking eight-hour stability release gate</a>. Historical task checks do not establish stability.</p>';
}
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
