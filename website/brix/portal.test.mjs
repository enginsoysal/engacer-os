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

test('M13 home distinguishes design progress, current media and pending production search',()=>{
 const sections=portalDesign(),body=JSON.stringify(sections);assert.equal(sections.length,4);
 for(const term of ['M13.0','M12.18','not a new native OS release','Production BrixCanvas still uses','documentation-archive','guide-install','guide-use','guide-customize'])assert.ok(body.includes(term),term);
 assert.ok(!body.includes('Download M13'));
});
