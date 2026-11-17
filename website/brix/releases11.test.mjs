import test from 'node:test';import assert from 'node:assert/strict';
import {stageRelease11,stageRelease12,releaseLabel} from './releases11.mjs';
const release=(n,extra={})=>({tag_name:`m11${n}-v0.11.${n}`,draft:false,prerelease:false,assets:[{name:`EngacerOS-M11STAGE${n}.iso`},{name:`EngacerOS-M11STAGE${n}-VMware.zip`},{name:`m11stage${n}-build-manifest.json`}],...extra});

test('active M12 design is labeled separately and cannot replace a native download',()=>{
 const design={tag_name:'m120-v0.12.0-design',prerelease:true,draft:false,assets:[{name:'EngacerOS-M120-Design-Review2.zip'}]};
 assert.equal(releaseLabel(design,true,'m116-v0.11.6'),'Design only — no ISO');
 assert.equal(stageRelease11([design,release(5)]).label,'M11.5');
 assert.equal(releaseLabel(release(5),false,'m115-v0.11.5'),'Latest stage delivery');
});
test('stage downloads require all matching public assets and prefer the newest stage',()=>{
 assert.equal(stageRelease11([release(4)]).label,'M11.4');
 assert.equal(stageRelease11([release(4),release(5)]).tag,'m115-v0.11.5');
 assert.equal(stageRelease11([release(4),release(5,{draft:true})]).id,'M114');
 assert.equal(stageRelease11([release(4,{prerelease:true})]),null);
 assert.equal(stageRelease11([release(4,{assets:[]})]),null);
});

test('M12 downloads require native assets, numeric stage order and public qualification',()=>{
 const native=n=>({tag_name:`m12${n}-v0.12.${n}`,draft:false,prerelease:false,assets:[{name:`EngacerOS-M12STAGE${n}.iso`},{name:`EngacerOS-M12STAGE${n}-VMware.zip`},{name:`m12stage${n}-build-manifest.json`}]});
 assert.equal(stageRelease12([{tag_name:'m120-v0.12.0-design',prerelease:true,assets:[]}]),null);
 assert.equal(stageRelease12([native(1)]).guide,'install-m121');
 assert.equal(stageRelease12([native(9),native(10)]).label,'M12.10');
 assert.equal(stageRelease12([{...native(2),draft:true},native(1)]).label,'M12.1');
 assert.equal(stageRelease12([{...native(2),prerelease:true}]),null);
 assert.equal(stageRelease12([{...native(2),assets:[]}]),null);
});

import {releaseGroups,documentationRef,assertPostBounds} from './downloads.mjs';
test('current assets remain separate and every historical release is reachable exactly once',()=>{
 const rows=Array.from({length:44},(_,i)=>({tag_name:'release-'+i}));const g=releaseGroups(rows,'release-2');
 assert.deepEqual(g.current,[rows[2]]);assert.equal(g.archives.length,6);assert(g.archives.every(p=>p.length<=8));
 assert.deepEqual(new Set([...g.current,...g.archives.flat()]),new Set(rows));assert.equal(g.archives.flat().length,43);
});
test('publication rejects overlarge generated download or archive pages before API writes',()=>{
 assert.doesNotThrow(()=>assertPostBounds([{slug:'downloads',blocks:[]} ]));
 assert.throws(()=>assertPostBounds([{slug:'downloads',blocks:[],text:'x'.repeat(240*1024)}]),/payload/);
 assert.throws(()=>assertPostBounds([{slug:'archive',blocks:Array(501).fill({})}]),/block count/);
});
test('release reruns keep immutable content source when publisher tooling advances',()=>{
 const sha='a'.repeat(40);assert.equal(documentationRef({GITHUB_EVENT_NAME:'release',GITHUB_SHA:sha}),sha);
 assert.equal(documentationRef({GITHUB_EVENT_NAME:'push',GITHUB_SHA:sha}),'HEAD');
 assert.equal(documentationRef({ENGACER_DOCS_REF:sha}),sha);assert.throws(()=>documentationRef({ENGACER_DOCS_REF:'main; arbitrary'}),/canonical commit/);
});
