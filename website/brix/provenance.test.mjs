import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {documentRevision} from './provenance.mjs';

test('unchanged docs retain their real revision; changed or falsely attributed bytes cannot pass',()=>{
 const folder=fs.mkdtempSync(path.join(os.tmpdir(),'engacer-doc-provenance-'));
 const git=(...args)=>execFileSync('git',args,{cwd:folder,encoding:'utf8',stdio:['pipe','pipe','pipe']});
 const commit=message=>{git('add','.');git('-c','user.name=Engacer test','-c','user.email=test@example.invalid','-c','commit.gpgsign=false','commit','-m',message);return git('rev-parse','HEAD').trim();};
 try{git('init');git('config','core.autocrlf','false');fs.writeFileSync(path.join(folder,'guide.md'),'# Original guide\n');const original=commit('original');
 fs.writeFileSync(path.join(folder,'other.md'),'# Other document\n');const next=commit('unrelated');
 const retained=documentRevision('guide.md',next,git);assert.equal(retained.commit,original);assert.match(retained.date,/^\d{4}-\d{2}-\d{2}$/);
 fs.writeFileSync(path.join(folder,'guide.md'),'# Changed guide\n');const changed=commit('changed');assert.equal(documentRevision('guide.md',changed,git).commit,changed);
 const falseHistory=(...args)=>args[0]==='log'?original+'\n1700000000\n':git(...args);assert.throws(()=>documentRevision('guide.md',changed,falseHistory),/differs from current bytes/);
 assert.throws(()=>documentRevision('missing.md',next,git),/Missing document history/);
 }finally{const resolved=fs.realpathSync(folder),root=fs.realpathSync(os.tmpdir());assert(resolved.startsWith(root+path.sep));fs.rmSync(resolved,{recursive:true});}
});
