import test from 'node:test';import assert from 'node:assert/strict';
import {stageRelease11,releaseLabel} from './releases11.mjs';
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
