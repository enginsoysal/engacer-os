// Keep unchanged documents pinned to their actual last edit, with identical current bytes.
export function documentRevision(path,ref,git){
 const [commit,seconds]=git('log','-1','--format=%H%n%ct',ref,'--',path).trim().split(/\r?\n/);
 if(!/^[0-9a-f]{40}$/.test(commit||'')||!/^\d+$/.test(seconds||''))throw Error('Missing document history: '+path);
 const current=git('rev-parse',ref+':'+path).trim(),previous=git('rev-parse',commit+':'+path).trim();
 if(current!==previous)throw Error('Document provenance differs from current bytes: '+path);
 return {commit,date:new Date(Number(seconds)*1000).toISOString().slice(0,10),blob:current};
}
