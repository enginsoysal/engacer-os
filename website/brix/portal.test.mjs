import {portalDesign} from './design.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {portal,portalGroups,milestoneKey} from './portal.mjs';
const p=(path,title=path)=>({slug:path,title,meta:[{key:'engine_source_path',value:path}]});
test('current task order is explicit and independent of publication date',()=>{
 const rows=portal.sections.flatMap(s=>s.items.map(([path])=>p(path))).reverse();
 const result=portalGroups(rows,{strict:true});
 assert.deepEqual(result.groups.map(g=>g.title),['Start here','Install','Use Engacer OS','Customize','Project & development']);
 assert.equal(result.groups[1].posts[0].readerTitle,'Download the tested ISO or prepared VMware package');
 assert.equal(new Set(result.groups.flatMap(g=>g.posts.map(p=>p.slug))).size,rows.length);
});
test('historical installs do not displace current instructions and all stay reachable',()=>{
 const current=portal.sections.find(s=>s.id==='install').items[1][0];
 const rows=[p(current),p('docs/handbook/install-m1218.md'),p('docs/handbook/install-m112.md'),p('docs/handbook/install-m123.md'),p('unknown.md')];
 const r=portalGroups(rows);assert.equal(r.groups[0].posts[0].slug,current);
 assert.equal(r.archive.length,4);assert.equal(new Set([...r.groups.flatMap(g=>g.posts),...r.archive].map(p=>p.slug)).size,5);
});
test('milestone identities sort numerically rather than compact filenames',()=>{
 const rows=[p('docs/handbook/install-m1210.md'),p('docs/handbook/install-m123.md'),p('docs/handbook/install-m112.md')];
 const cmp=new Intl.Collator('en',{numeric:true}).compare;
 assert.deepEqual(rows.sort((a,b)=>cmp(milestoneKey(a),milestoneKey(b))).map(p=>p.slug),['docs/handbook/install-m112.md','docs/handbook/install-m123.md','docs/handbook/install-m1210.md']);
});
test('missing curated source fails full publication instead of silently dropping it',()=>{
 assert.throws(()=>portalGroups([],{strict:true}),/Missing curated portal source/);
});
test('full history sorts M0 through M13 with decimal and legacy compact stages',()=>{
 const paths=['docs/milestones/m12.md','docs/milestones/m4.5.md','docs/milestones/m0.md','docs/milestones/m11.md','docs/milestones/m10.md','docs/handbook/install-m45.md','docs/milestones/m2.md'];
 const cmp=new Intl.Collator('en',{numeric:true}).compare;
 const keys=paths.map(path=>milestoneKey(p(path))).sort(cmp);
 assert.deepEqual(keys.map(k=>k.split(' ')[0]),['000.000','002.000','004.005','004.005','010.000','011.000','012.000']);
});

test('M13 home distinguishes design progress, current media and pending production search',()=>{
 const sections=portalDesign(),body=JSON.stringify(sections);assert.equal(sections.length,4);
 for(const term of ['M13.0','M12.18','not a new native OS release','Production BrixCanvas still uses','documentation-archive','guide-install','guide-use','guide-customize'])assert.ok(body.includes(term),term);
 assert.ok(!body.includes('Download M13'));
});

test('native M13 homepage uses matching stage and validated shared header navigation',async()=>{
 const {portalConfiguration}=await import('./portal.mjs');const blocks=portalDesign({stage:1,searchReady:true});
 assert.deepEqual(blocks[0].props.documentationPortal,portalConfiguration());assert.equal(blocks[0].props.bg,'#f7f9f9');assert.equal(blocks[0].props.textColor,'#152434');const serialized=JSON.stringify(blocks);assert(serialized.includes('Download M13.1'));assert(!serialized.includes('CURRENT DOWNLOAD · M12.18'));assert(serialized.includes('Ctrl+K'));assert(!blocks[0].props.items.some(item=>item.href==='/search'));
});

test('published search metadata includes bounded current-guide headings and task aliases',async()=>{const {portalConfiguration}=await import('./portal.mjs');const config=portalConfiguration();for(const section of config.sections)for(const entry of section.entries){assert(entry.aliases.includes(section.title));assert(entry.aliases.length<=500);}assert(config.sections.some(section=>section.entries.some(entry=>entry.slug==='downloads'&&entry.aliases.includes('ISO VMware'))));});

test('current download retains an unresolved owner stability report without claiming a fix',()=>{const ownerIssues=[{id:'long-uptime-freeze',status:'investigation_planned'}];const current=JSON.stringify(portalDesign({stage:8,searchReady:true,ownerIssues}));assert(current.includes('Known freezes: testing only'));assert(current.includes('does not claim a fix'));assert(!JSON.stringify(portalDesign({stage:6,ownerIssues})).includes('Known freezes: testing only'));assert(!JSON.stringify(portalDesign({stage:9,ownerIssues:[{id:'long-uptime-freeze',status:'resolved'}]})).includes('Known freezes: testing only'));});

test('known M13 freezes have visible testing-only status and a blocking stability gate',async()=>{const issues=[{id:"long-uptime-freeze",status:"investigating"}];const home=JSON.stringify(portalDesign({stage:8,searchReady:true,ownerIssues:issues}));for(const term of ["KNOWN FREEZES · TESTING ONLY","M13.8 (testing only)","Do not use this build for everyday work","M13.13","Stability is not qualified"])assert(home.includes(term),term);const {stabilityWarning13}=await import("./downloads.mjs");const warning=stabilityWarning13({owner_additions:issues});for(const term of ["M13.8","testing only","M13.13","eight-hour"])assert(warning.includes(term),term);assert.equal(stabilityWarning13({owner_additions:[{id:"long-uptime-freeze",status:"resolved"}]}),"");});

test('workday publication cannot replace pending status with a partial duration or diagnostic pass',async()=>{
 const {workdayQualified13,stabilityWarning13}=await import('./downloads.mjs');
 const ownerIssues=[{id:'long-uptime-freeze',status:'qualified_current_candidate'}];
 const complete={passed:true,stage:'M13.13',qualification:'M13-STAGE13-VM-v1',actual_workday_seconds:28800,uninterrupted_idle_seconds:7200};
 for(const result of [undefined,{...complete,passed:false},{...complete,diagnostic_only:true},{...complete,actual_workday_seconds:28799},{...complete,uninterrupted_idle_seconds:7199},{...complete,stage:'M13.12'},{...complete,actual_workday_seconds:Infinity}]){
  assert.equal(workdayQualified13(result),false);
  const home=JSON.stringify(portalDesign({stage:13,ownerIssues,stabilityQualification:result}));
  assert(home.includes('STABILITY PENDING · TESTING ONLY'));
  assert(!home.includes('EIGHT-HOUR VM WORKDAY QUALIFIED'));
  assert(stabilityWarning13({owner_additions:ownerIssues,stability_qualification:result}).includes('Stability is not qualified'));
 }
});

test('qualified named-workday copy preserves historical cause and device limitations',async()=>{
 const {stabilityWarning13}=await import('./downloads.mjs');
 const result={passed:true,stage:'M13.13',qualification:'M13-STAGE13-VM-v1',actual_workday_seconds:28801,uninterrupted_idle_seconds:7201};
 const ownerIssues=[{id:'long-uptime-freeze',status:'qualified_current_candidate'}];
 const home=JSON.stringify(portalDesign({stage:13,ownerIssues,stabilityQualification:result}));
 for(const term of ['EIGHT-HOUR VM WORKDAY QUALIFIED','Next: hardware recognition.','Historical natural-freeze causes remain unestablished','unlimited uptime are not qualified'])assert(home.includes(term),term);
 assert(!home.includes('STABILITY PENDING · TESTING ONLY'));
 assert(!home.includes('Download M13.13 (testing only)'));
 const warning=stabilityWarning13({owner_additions:ownerIssues,stability_qualification:result});
 for(const term of ['Eight-hour VMware workday qualified','M13.7/M13.8','does not establish their cause','stability-m1313'])assert(warning.includes(term),term);
 assert(!JSON.stringify(portalDesign({stage:12,ownerIssues,stabilityQualification:result})).includes('EIGHT-HOUR VM WORKDAY QUALIFIED'));
});
