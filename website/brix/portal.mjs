import fs from 'node:fs';
export const portal=JSON.parse(fs.readFileSync(new URL('./portal.json',import.meta.url),'utf8'));
export const sourcePath=p=>p.meta?.find(m=>m.key==='engine_source_path')?.value||'';
const compare=new Intl.Collator('en',{numeric:true,sensitivity:'base'}).compare;
export function milestoneKey(p){
 const s=sourcePath(p),match=s.split('/').at(-1).match(/(?:^|-)m(\d+)(?:[.-](\d+))?(?:[-.]|$)/i);
 if(!match)return `999.999 ${s}`;
 const raw=match[1],legacy={45:[4,5],51:[5,1],71:[7,1],72:[7,2],73:[7,3],74:[7,4],75:[7,5],91:[9,1],92:[9,2]};
 const pair=raw.length>2&&/^(11|12|13|14)/.test(raw)?[Number(raw.slice(0,2)),Number(raw.slice(2))]:legacy[raw]||[Number(raw),Number(match[2]||0)];
 return `${String(pair[0]).padStart(3,'0')}.${String(pair[1]).padStart(3,'0')} ${s}`;
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

export function portalConfiguration(){
 return {version:1,sections:portal.sections.map(section=>({title:section.title,entries:section.items.map(([source,title])=>({slug:source==='@releases'?'downloads':'docs-'+source.replace(/\.md$/i,'').replace(/^docs\//,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,''),title,aliases:(section.title+' '+(source==='@releases'?'ISO VMware download release checksums':fs.readFileSync(new URL('../../'+source,import.meta.url),'utf8').split(/\r?\n/).filter(line=>/^#{1,3}\s/.test(line)).slice(0,12).map(line=>line.replace(/^#+\s*/,'' )).join(' '))).slice(0,500),group:source==='@releases'?'Downloads':section.id==='project'?'Development':'Guides'}))}))};
}
