import test from 'node:test';
import assert from 'node:assert/strict';
import {documentationGroups} from './navigation.mjs';
import {nativeDesign} from './design.mjs';
const post=(path,title,category='handbook')=>({slug:path,title,category,meta:[{key:'engine_source_path',value:path}]});

test('homepage separates M12 concepts from the native M11.6 download',()=>{
 const sections=nativeDesign({development:{current_stage:'M12.0',qualified_download:'M11.6',stages:[{id:'M12.0',title:'Inventory and design contract'}]}}),payload=JSON.stringify(sections);
 assert.equal(sections.length,4);
 assert.match(payload,/M12\.0 original design concept/);
 assert.match(payload,/not a native VM capture/);
 assert.match(payload,/M11\.6 remains the current tested VMware download/);
 assert.match(payload,/evidence\/M11\/6\/setup\/vmware\/first-start-guide\.png/);
 assert.doesNotMatch(payload,/Try its matching VMware package/);
});

test('a qualified native M12 stage uses its own real capture, guide and scope',()=>{
 const payload=JSON.stringify(nativeDesign({development:{current_stage:'M12.1',qualified_download:'M12.1',stages:[{id:'M12.1',title:'Shared visual components'}]}}));
 assert.match(payload,/evidence\/M12\/1\/feature\.png/);
 assert.match(payload,/docs-handbook-install-m121/);
 assert.match(payload,/From the real M12\.1 VM/);
 assert.match(payload,/Full final M12 qualification remains M12\.18/);
 assert.doesNotMatch(payload,/M11\/6\/setup\/vmware|overview\.svg/);
});

test('M12 design follows tested installation without replacing its release',()=>{
 const posts=[post('docs/handbook/install-m116.md','Install M11.6'),post('docs/milestones/m12.md','M12','milestones'),post('docs/architecture/desktop-m12.md','M12 design','architecture'),post('docs/handbook/files-m11.md','Files')];
 const groups=documentationGroups(posts);
 assert.equal(groups[0].posts[0].title,'Install M11.6');
 assert.deepEqual(groups[1].posts.map(p=>p.title),['M12','M12 design']);
 assert.equal(groups[2].posts[0].title,'Files');
 assert.equal(new Set(groups.flatMap(g=>g.posts.map(p=>p.slug))).size,posts.length);
});

test('M12 native guides replace older installation without hiding established tasks',()=>{
 const posts=[post('docs/handbook/install-m116.md','Install M11.6'),post('docs/handbook/install-m121.md','Install M12.1'),post('docs/handbook/install-m1210.md','Install M12.10'),post('docs/handbook/icons-m122.md','Icons'),post('docs/handbook/components-m121.md','Controls'),post('docs/releases/m1210-v0.12.10.md','M12.10 release','releases')];
 const groups=documentationGroups(posts);
 assert.equal(groups[0].posts[0].title,'Install M12.10');
 assert.deepEqual(groups[1].posts.map(p=>p.title),['Controls','Icons']);
 assert.ok(groups.at(-1).posts.some(p=>p.title==='Install M12.1'));
 assert.equal(new Set(groups.flatMap(g=>g.posts.map(p=>p.slug))).size,posts.length);
});
test('current install and M11 user tasks precede architecture and history',()=>{
 const posts=[post('docs/handbook/install-m6.md','M6 installation (historical)'),post('docs/architecture/input-m11.md','Input','architecture'),post('docs/handbook/files-m11.md','Files'),post('docs/handbook/install-m10.md','Install M10'),post('docs/handbook/index.md','Handbook'),post('docs/milestones/m11.md','M11','milestones')];
 const groups=documentationGroups(posts);
 assert.equal(groups[0].posts[0].title,'Handbook');assert.equal(groups[0].posts[1].title,'Install M10');
 assert.equal(groups[1].posts[0].title,'M11');assert.equal(groups[1].posts[1].title,'Files');
 assert.equal(groups.at(-1).posts.at(-1).title,'M6 installation (historical)');
 assert.equal(new Set(groups.flatMap(g=>g.posts.map(p=>p.slug))).size,posts.length);
});
test('numeric names sort naturally and every uncategorized article stays discoverable once',()=>{
 const posts=[post('b','Guide 10'),post('a','Guide 2'),post('c','Other','custom')];
 const groups=documentationGroups(posts);assert.deepEqual(groups[0].posts.map(p=>p.title),['Guide 2','Guide 10']);
 assert.deepEqual(groups.flatMap(g=>g.posts.map(p=>p.slug)).sort(),['a','b','c']);
});

test('a new stage replaces the previous install/release in Start here; history stays last',()=>{
 const posts=[post('docs/handbook/index.md','Handbook'),post('docs/handbook/install-m10.md','Install M10 (historical)'),post('docs/handbook/install-m114.md','Install M11.4'),post('docs/releases/m10-v0.10.0.md','M10 release (historical)','releases'),post('docs/releases/m114-v0.11.4.md','M11.4 release','releases')];
 const groups=documentationGroups(posts);
 assert.deepEqual(groups[0].posts.map(p=>p.title),['Handbook','Install M11.4','M11.4 release']);
 assert.deepEqual(new Set(groups.at(-1).posts.map(p=>p.title)),new Set(['Install M10 (historical)','M10 release (historical)']));
 assert.equal(groups.flatMap(g=>g.posts).length,posts.length);
});

test('M11.5 is first and the older M11.4 install guide stays in the archive',()=>{
 const posts=[post('docs/handbook/install-m114.md','Install M11.4'),post('docs/handbook/install-m115.md','Install M11.5'),post('docs/architecture/setup-m115.md','Setup decisions','architecture')];
 const groups=documentationGroups(posts);
 assert.equal(groups[0].posts[0].title,'Install M11.5');
 assert.equal(groups.at(-1).posts[0].title,'Install M11.4');
 assert.equal(groups.flatMap(g=>g.posts).length,3);
});
