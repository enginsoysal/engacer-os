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
 const rows=[p('docs/handbook/install-m1218.md'),p('docs/handbook/install-m112.md'),p('docs/handbook/install-m123.md'),p('unknown.md')];
 const r=portalGroups(rows);assert.equal(r.groups[0].posts[0].slug,'docs/handbook/install-m1218.md');
 assert.equal(r.archive.length,3);assert.equal(new Set([...r.groups.flatMap(g=>g.posts),...r.archive].map(p=>p.slug)).size,4);
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
 assert.deepEqual(blocks[0].props.documentationPortal,portalConfiguration());const serialized=JSON.stringify(blocks);assert(serialized.includes('Download M13.1'));assert(!serialized.includes('CURRENT DOWNLOAD · M12.18'));assert(serialized.includes('Ctrl+K'));assert(!blocks[0].props.items.some(item=>item.href==='/search'));
});
