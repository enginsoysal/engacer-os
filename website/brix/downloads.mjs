// Keep current downloads obvious and historical pages bounded as releases grow.
import assert from 'node:assert/strict';
export function workdayQualified13(result){
 return result?.passed===true&&result.diagnostic_only!==true&&result.stage==='M13.13'&&result.qualification==='M13-STAGE13-VM-v1'&&Number.isFinite(result.actual_workday_seconds)&&result.actual_workday_seconds>=28800&&Number.isFinite(result.uninterrupted_idle_seconds)&&result.uninterrupted_idle_seconds>=7200;
}
export function stabilityWarning13(progress){
 if(workdayQualified13(progress.stability_qualification))return '<p><strong>Eight-hour VMware workday qualified.</strong> M13.13 passed its named enabled-device VMware scenario, including two uninterrupted idle hours, active tasks and independent saved-data starts. This does not promise universal hardware or unlimited uptime. Historical M13.7/M13.8 natural-freeze reports remain recorded; the simulated recovery test does not establish their cause. Read the <a href="/blog/docs-handbook-stability-m1313">stability scope and data guide</a>.</p>';
 if(!(progress.owner_additions||[]).some(issue=>issue.id==='long-uptime-freeze'&&issue.status!=='resolved'))return '';
 return '<p><strong>Known freezes — testing only.</strong> Frequent freezes are reported on M13.8, following the earlier M13.7 report. Do not use these media for everyday work. Stability is not qualified. M13.9-M13.12 finish the product in order; <a href="/blog/docs-milestones-m13-13">M13.13 is the blocking eight-hour stability release gate</a>. Historical task checks do not establish stability.</p>';
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
