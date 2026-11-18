// Keep current downloads obvious and historical pages bounded as releases grow.
import assert from 'node:assert/strict';
export function stabilityScopeQualified13(result){
 return result?.passed===true&&result.diagnostic_only!==true&&result.duration_scope==='owner_revised_90_minutes'&&result.functional_completion_separate_from_duration===true&&result.eight_hour_gate_passed===false&&result.stage==='M13.13'&&result.qualification==='M13-STAGE13-VM-v1'&&Number.isFinite(result.actual_observed_seconds)&&result.actual_observed_seconds>=5400;
}
export function stabilityWarning13(progress){
 if(stabilityScopeQualified13(progress.stability_qualification))return '<p><strong>Named VMware checks complete.</strong> M13.13 meets the owner-revised ninety-minute observation scope, with separate active tasks and independent saved-data starts. The earlier eight-hour/two-hour requirement was stopped at the explicit owner direction and did not pass. This does not promise universal hardware or unlimited uptime. Historical M13.7/M13.8 natural-freeze reports remain recorded; the simulated recovery test does not establish their cause. Read the <a href="/blog/docs-handbook-stability-m1313">stability scope and data guide</a>.</p>';
 if(!(progress.owner_additions||[]).some(issue=>issue.id==='long-uptime-freeze'&&issue.status!=='resolved'))return '';
 return '<p><strong>Known freezes — testing only.</strong> Frequent freezes are reported on M13.8, following the earlier M13.7 report. Do not use these media for everyday work. Stability is not qualified. M13.9-M13.12 finish the product in order; <a href="/blog/docs-milestones-m13-13">M13.13 closes the owner-revised stability scope</a>. Historical task checks do not establish stability.</p>';
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
