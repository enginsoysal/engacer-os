import fs from 'node:fs';
export const portal=JSON.parse(fs.readFileSync(new URL('./portal.json',import.meta.url),'utf8'));
export const sourcePath=p=>p.meta?.find(m=>m.key==='engine_source_path')?.value||'';
const compare=new Intl.Collator('en',{numeric:true,sensitivity:'base'}).compare;
export function milestoneKey(p){
 const s=sourcePath(p),match=s.match(/\/(?:[^/]*-)?m(1[123])(\d*)(?:[-.]|$)/i);
 return match?`${match[1].padStart(3,'0')}.${(match[2]||'0').padStart(3,'0')} ${s}`:s;
}
export function portalGroups(posts,{strict=false}={}){
 const bySource=new Map(posts.map(p=>[sourcePath(p),p]));const used=new Set();
 const groups=portal.sections.map(s=>({...s,posts:s.items.flatMap(([path,label])=>{
  const p=bySource.get(path);if(!p){if(strict)throw Error(`Missing curated portal source: ${path}`);return [];}
  if(used.has(p.slug))throw Error(`Duplicate curated portal source: ${path}`);used.add(p.slug);return [{...p,readerTitle:label}];
 })}));
 const archive=posts.filter(p=>!used.has(p.slug)).sort((a,b)=>compare(milestoneKey(a),milestoneKey(b)));
 return {groups:groups.filter(g=>g.posts.length),archive};
}
