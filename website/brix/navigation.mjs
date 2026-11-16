// Reader-first order: current tasks precede internals and historical releases.
const source=p=>p.meta?.find(m=>m.key==='engine_source_path')?.value||'';
const compare=new Intl.Collator('en',{numeric:true,sensitivity:'base'}).compare;
export function documentationGroups(posts){
 const remaining=new Map(posts.map(p=>[p.slug,p]));const groups=[];
 const add=(title,description,items)=>{const unique=items.filter(p=>p&&remaining.delete(p.slug));if(unique.length)groups.push({title,description,posts:unique});};
 const find=path=>posts.find(p=>source(p)===path);
 const numbers=Array.from({length:18},(_,i)=>18-i);
 const currentInstall=numbers.map(n=>find(`docs/handbook/install-m12${n}.md`)).find(Boolean)||find('docs/handbook/install-m116.md')||find('docs/handbook/install-m115.md')||find('docs/handbook/install-m114.md')||find('docs/handbook/install-m10.md');
 const currentRelease=numbers.map(n=>find(`docs/releases/m12${n}-v0.12.${n}.md`)).find(Boolean)||find('docs/releases/m116-v0.11.6.md')||find('docs/releases/m115-v0.11.5.md')||find('docs/releases/m114-v0.11.4.md')||find('docs/releases/m10-v0.10.0.md');
 add('1. Start here','Install the tested release, understand what works and find downloads.',[
  find('docs/handbook/index.md'),currentInstall,find('docs/roadmap/status.md'),posts.find(p=>p.slug==='downloads'),currentRelease]);
 const stageNumber=p=>Number(source(p).match(/m12(\d+)\.md$/)?.[1]||0);
 const stageGuides=category=>posts.filter(p=>source(p).startsWith(`docs/${category}/`)&&/m12\d+\.md$/.test(source(p))&&!/\/install-m12/.test(source(p))).sort((a,b)=>stageNumber(a)-stageNumber(b)||compare(a.title,b.title));
 add('2. M12 desktop experience','Ordered native stage guides and decisions; original design concepts remain clearly labeled.',[
  find('docs/milestones/m12.md'),...stageGuides('handbook'),find('docs/handbook/desktop-m12.md'),...stageGuides('architecture'),find('docs/architecture/desktop-m12.md'),find('docs/architecture/m12-inventory.md')]);
 add('3. M11 desktop and installation refresh','User guides, interaction decisions and qualification, in milestone order.',[
  find('docs/milestones/m11.md'),find('docs/handbook/desktop-install-m11.md'),find('docs/handbook/files-m11.md'),find('docs/handbook/start-m11.md'),find('docs/handbook/windows-m11.md'),find('docs/architecture/desktop-m11.md'),find('docs/architecture/input-m11.md'),find('docs/architecture/files-m11.md'),find('docs/architecture/start-m11.md'),find('docs/architecture/windows-m11.md'),find('docs/architecture/setup-m115.md'),find('docs/architecture/qualification-m116.md'),find('docs/architecture/usability-review-m116.md')]);
 const sorted=()=>[...remaining.values()].sort((a,b)=>compare(a.title,b.title));
 const historical=p=>/docs\/handbook\/install-(?:m11[456]|m12\d+)\.md$/.test(source(p))||/\(historical\)$/.test(p.title)||source(p).startsWith('docs/roadmap/history/')||p.category==='releases';
 add('4. Everyday use and customization','Current manuals for files, devices, distributions and ordinary tasks.',sorted().filter(p=>p.category==='handbook'&&!historical(p)));
 add('5. Architecture and development','Technical reference, source builds and design decisions.',sorted().filter(p=>!['handbook','roadmap','milestones','evidence','website','downloads','releases'].includes(p.category)&&!historical(p)));
 add('6. Roadmap and verification','Current plans and test evidence; qualification is always scoped.',sorted().filter(p=>['roadmap','milestones','evidence'].includes(p.category)&&!historical(p)));
 add('7. Website maintenance','How the English website follows canonical GitHub documentation.',sorted().filter(p=>p.category==='website'));
 add('8. Historical releases and earlier milestones','Archive material. Use the current installation guide above for the tested download.',sorted());
 return groups;
}
