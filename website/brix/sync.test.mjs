import test from 'node:test';
import assert from 'node:assert/strict';
import {assertSite,planSync,retryDelay} from './sync.mjs';
const post={slug:'docs-handbook-index',title:'Handbook',status:'published',bodyFormat:'brix',blocks:[{id:'a',type:'text',props:{text:'Guide'}}],meta:[{key:'engine_source_path',value:'docs/handbook/index.md'}]};

test('publication retries only repeatable operations and obeys bounded server delay',()=>{
 for(const method of ['GET','PATCH']){
  assert.equal(retryDelay(method,429,0,'30'),30000);
  assert.equal(retryDelay(method,429,0,'120'),null);
  assert.equal(retryDelay(method,429,0,'Mon, 16 Nov 2026 14:00:30 GMT',Date.parse('2026-11-16T14:00:00Z')),30000);
  assert.equal(retryDelay(method,502,2,null),8000);
  assert.equal(retryDelay(method,502,3,null),null);
  assert.equal(retryDelay(method,'timeout',0),2000);
  for(const status of [400,401,403,404,409,422])assert.equal(retryDelay(method,status,0,null),null);
 }
 assert.equal(retryDelay('POST',429,0,'30'),null);
 assert.equal(retryDelay('POST',502,0,null),null);
 assert.equal(retryDelay('POST','timeout',0),null);
});
test('reject a key for any other site before writing',()=>assert.throws(()=>assertSite({slug:'another-site',title:'Codename: Engine OS'}),/different website/));
test('accept only the renamed canonical site identity',()=>{
 assert.doesNotThrow(()=>assertSite({slug:'codename-engine-os-ltvck',title:'Engacer OS'}));
 assert.throws(()=>assertSite({slug:'codename-engine-os-ltvck',title:'Another project'}),/Unexpected website identity/);
});
test('never overwrite a matching slug owned by the author rather than the publisher',()=>assert.throws(()=>planSync([post],[{slug:post.slug,title:'Owner content',meta:[]}]),/Unmanaged slug collision/));
test('preserve unrelated author articles',()=>assert.deepEqual(planSync([post],[post,{slug:'owner-news',status:'published',meta:[]}]),[]));
test('archive removed generated sources as drafts rather than delete them',()=>assert.deepEqual(planSync([],[post]).map(x=>x.kind),['archive']));
test('recover only the exact, empty publisher-created draft',()=>{
 const old={slug:post.slug,status:'draft',author:'Engine OS project',excerpt:'Engine OS generated draft: docs/handbook/index.md',blocks:[]};
 assert.equal(planSync([post],[old])[0].kind,'update');
 assert.equal(planSync([post],[{...old,author:'Engacer OS project',excerpt:'Engacer OS generated draft: docs/handbook/index.md'}])[0].kind,'update');
 assert.throws(()=>planSync([post],[{...old,blocks:[{type:'text'}]}]),/Unmanaged slug collision/);
});
test('a mixed plan with a later collision is rejected before any operations are returned',()=>assert.throws(()=>planSync([post,{...post,slug:'second'}],[{slug:'second'}]),/Unmanaged slug collision/));

test('removed generated download archive pages become drafts while author pages remain untouched',()=>{
 const archive={...post,slug:'downloads-archive-9',meta:[{key:'engine_source_path',value:'@release-archive/9'}]};
 assert.deepEqual(planSync([],[archive]).map(x=>x.kind),['archive']);
 assert.deepEqual(planSync([],[{...archive,meta:[]}]),[]);
});

import {assertPostEqual} from './sync.mjs';
test('generated archive excerpts explicitly replace the publisher-created draft marker',()=>{
 const expected={...post,excerpt:'Historical release assets and checksums.'};
 assert.doesNotThrow(()=>assertPostEqual(expected,{...expected}));
 assert.throws(()=>assertPostEqual(expected,{...expected,excerpt:'Engacer OS generated draft: @release-archive/1'}),/mismatched fields excerpt/);
});
test('publication readback identifies a changed field without dumping whole article bodies',()=>{
 assert.throws(()=>assertPostEqual({...post,blocks:[]},{...post,blocks:[{type:'text'}]}),/mismatched fields blocks/);
});
