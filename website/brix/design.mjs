// Native Brix composition matching the owner's preferred local documentation design.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const progress=JSON.parse(fs.readFileSync(new URL('../../docs/milestones/m11-progress.json',import.meta.url),'utf8'));
const developmentProgress=JSON.parse(fs.readFileSync(new URL('../../docs/milestones/m12-progress.json',import.meta.url),'utf8'));
let sequence=0;
const site='https://engaceros.brixcanvas.com';
const expanded=Number(progress.current_stage.split('.')[1])>=5;
const final=progress.qualified_download==='M11.6';
const ink='#152434',muted='#5a6976',teal='#087c71',dark='#101e2c',paper='#f7f9f9';
const b=(type,props)=>({id:`engine-home-${++sequence}`,type,props});
const text=(value,size=16,color=muted,more={})=>b('text',{text:value,size,color,padX:0,py:10,lineHeight:1.65,...more});
const heading=(value,size=26,color=ink,more={})=>b('heading',{text:value,size,color,level:2,weight:600,padX:0,py:12,fluid:true,...more});
const button=(label,href,more={})=>b('button',{label,href,bg:teal,color:'#ffffff',hoverBg:'#065f56',radius:'none',size:'sm',align:'left',padX:0,py:12,...more});
const layout=(columns,more={})=>b('layout',{columns:columns.map(children=>({children})),contentWidth:1280,padY:0,...more});
const card=(n,title,description,label,slug)=>[
 text(n,11,teal,{letterSpacing:'1.2px',weight:600}),heading(title,21,ink,{level:3}),text(description,14),
 button(label,`${site}/blog/${slug}`,{bg:'#ffffff',color:teal,hoverBg:'#edf5f2',size:'sm'}),
];
export function nativeDesign({development=developmentProgress}={}){
 sequence=0;
 const native=/^M12\.(?:[1-9]|1[0-8])$/.test(development.qualified_download);
 const label=native?development.qualified_download:progress.qualified_download;
 const number=native?Number(label.split('.')[1]):0;
 const delivery=development.stages.find(s=>s.id===label);
 const guide=native?`install-m12${number}`:progress.release_guide;
 const knownIssueBrix=native?(development.known_issues||[]).filter(issue=>issue.status==='open').map(issue=>b('alert',{variant:'info',title:'Retained test observation · '+issue.observed_in,text:issue.observation+' Read the matching release scope before testing.'})):[];
 const header=b('menubrix',{brand:'E_  ENGACER OS',brandHref:'/',items:[{label:'Documentation',href:'/blog/documentation'},{label:'Downloads',href:'/blog/downloads'},{label:'GitHub ↗',href:'https://github.com/enginsoysal/engacer-os'},{label:'Search',href:'/search'}],mode:'inline',width:'full',shape:'square',size:'l',bg:dark,textColor:'#d5e1e8',hoverColor:'#35ceba',blur:false,border:false,shadow:false});
 header.style={bg:{color:dark}};
 const status=layout([[text('● Independent kernel. Open source.',11,'#50616c',{py:6})],[text('INDEPENDENT · BUILT FROM SCRATCH',10,'#50616c',{align:'right',letterSpacing:'1px',py:6})]],{bg:{kind:'color',color:'#eaf0f0'},borderBottom:1,borderColor:'#dbe3e6'});
 const terminal=layout([[
   text('PROJECT SNAPSHOT / X86-64',10,'#90a6b8',{letterSpacing:'1.5px',py:10}),
   heading('ENGACER OS',18,'#e4edf1',{py:12}),
   text('Original kernel · BIOS + UEFI boot',13,'#35ceba'),
   text('Tested native delivery: '+label+' · Scoped VM tests',12,'#90a6b8'),
   text(development.current_stage+' · '+development.stages.find(s=>s.id===development.current_stage).title,13,'#35ceba'),
   text('M12.0–M12.18 · Ordered delivery with tests and publication',12,'#90a6b8'),
   b('code',{code:'Next → Review → Install → Restart\nIDE / SATA / supported SCSI / NVMe\nDevices · USB file copies · Safe removal'}),
 ]],{bg:{kind:'color',color:dark},border:1,borderColor:'#35ceba',radius:4,padY:18,minH:320,valign:'center'});
 const hero=layout([[
   text('THE ENGACER OS KNOWLEDGE BASE',11,teal,{letterSpacing:'1.6px',weight:600,py:12}),
   heading('The M12 desktop',52,ink,{level:1,py:0,letterSpacing:'-1.8px'}),
   heading('made familiar.',52,teal,{py:0,letterSpacing:'-1.8px'}),
   text(native?`${label} delivers ${delivery.title.toLowerCase()} in the real native desktop. Use its matching ISO, VMware package and stage guide. Each remaining M12 stage follows in order with its own tests and publication.`:'M12.0 establishes the design: recognizable app icons, consistent Files navigation, clear controls and a coherent desktop. Nineteen stages follow in order. These concepts are not a new native build; M11.6 remains the current tested VMware download.',18,muted,{py:20}),
   layout([[button('See the M12 plan →',`${site}/blog/docs-milestones-m12`,{size:'sm'})],[button(`Download ${label} ↓`,`${site}/blog/downloads`,{variant:'outline',bg:ink,size:'sm'})]]),
 ],[terminal]],{padY:52,valign:'center'});
 hero.props.columns[0].width=55;hero.props.columns[1].width=45;
 hero.props.columns[0].children.at(-1).props.columns[0].width=60;
 hero.props.columns[0].children.at(-1).props.columns[1].width=40;
 const cards=layout([
   native?card('01 / CURRENT NATIVE STAGE',delivery.title,'Use the real native desktop with the behavior qualified for this stage. Its matching guide explains the controls, evidence and limits.','Read the stage guide ↗','docs-handbook-'+guide):card('01 / M12 DESIGN','One coherent desktop.','Recognizable icons, shared controls and a Files window that keeps Back, breadcrumbs and the sidebar visible, including USB empty states.','Explore the design contract ↗','docs-architecture-desktop-m12'),
   card('02 / TESTED DOWNLOAD','Install in VMware','The current qualified download is '+label+'. Use its prepared VMware ZIP and matching installation guide. Read the exact tested profiles and limits before choosing other hardware.','Open the setup guide ↗','docs-handbook-'+(guide||'install-m116')),
   card('03 / MAKE IT YOURS','Build your own distro.','Choose your accent, wallpaper, window style and default content with a validated distribution profile.','Open the distro guide ↗','docs-handbook-distributions'),
 ],{bg:{kind:'color',color:'#ffffff'},border:1,borderColor:'#dbe3e6',divided:true,ruleColor:'#dbe3e6',radius:4,padY:24});
 cards.props.columns.forEach(column=>{column.width=100/3;});
 const bottom=layout([[
   text('BUILT IN THE OPEN',11,teal,{letterSpacing:'1.5px'}),heading('Understand the decisions behind the OS.',19),
   text('Explore the kernel contracts, memory model, filesystem layout and compatibility roadmap. Every milestone links implementation claims to evidence.',14),
   button('Explore the architecture →',`${site}/blog/docs-architecture-overview`,{bg:paper,color:teal,hoverBg:'#edf5f2'}),
 ],[
   text('ONE SOURCE OF TRUTH',11,teal,{letterSpacing:'1.5px'}),heading('Documentation that follows the code.',19),
   text('Guides identify their canonical GitHub source commit. Official releases supply original download files and complete SHA256 checksums.',14),
   button('View the milestone plan →',`${site}/blog/docs-roadmap-milestones`,{bg:paper,color:teal,hoverBg:'#edf5f2'}),
 ]],{padY:32,borderBottom:1,borderColor:'#dbe3e6'});
 bottom.props.columns.forEach(column=>{column.width=50;});
 const main=layout([[
   hero,...knownIssueBrix,...(native?[heading('From the real '+label+' VM',27,ink,{py:18}),b('image',{url:`https://raw.githubusercontent.com/enginsoysal/engacer-os/main/evidence/M12/${number}/feature.png`,alt:`Native Engacer OS ${label} from its actual tested native guest, not a design concept. Read its matching stage qualification and capture provenance.`,naturalSize:true,radius:8})]:[heading('M12.0 original design concept',27,ink,{py:18}),b('image',{url:'https://raw.githubusercontent.com/enginsoysal/engacer-os/main/docs/architecture/figures/m12/overview.svg',alt:'Original M12.0 design concept, not a native VM capture. Distinct app icons and a proposed Start layout.',naturalSize:true,radius:8}),heading('From the real M11.6 VM — current tested download',27,ink,{py:18}),b('image',{url:'https://raw.githubusercontent.com/enginsoysal/engacer-os/main/evidence/M11/6/setup/vmware/first-start-guide.png',alt:'Native Engacer OS M11.6 in the tested VMware guest. This remains the qualified download while M12 development proceeds.',naturalSize:true,radius:8})]),heading('A good place to start',27,ink,{py:24}),cards,
   b('alert',{variant:'info',title:'Development progress and tested downloads',text:native?`${label} is a scoped native delivery. ${number===18?'The final M12 named virtual regression is recorded in its acceptance.':'Full final M12 qualification remains M12.18; later stages follow in order.'} Earlier M11 results do not qualify these new bytes. Read the matching release scope. Physical hardware, 3D and general Windows compatibility remain unqualified.`:'M12.0 is a design-only delivery. M12.1–M12.18 follow in order, each with scoped tests, guides and publication before the next begins. M11.6 remains the published native ISO and VMware package. Read its matching release scope. Qualification covers named virtual profiles; physical hardware, 3D and general Windows compatibility remain unqualified.'}),bottom,
 ]],{bg:{kind:'color',color:paper},padY:12});
 const footer=b('socialcircles',{copyright:'Engacer OS / MIT licensed · Documentation & releases on GitHub',bg:paper,circleBg:teal,items:[{label:'github',href:'https://github.com/enginsoysal/engacer-os'},{label:'website',href:`${site}/blog/documentation`}]});
 return [header,status,main,footer];
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const out=process.argv[2]||'build/brix/design';fs.mkdirSync(out,{recursive:true});
 nativeDesign().forEach((section,index)=>fs.writeFileSync(path.join(out,`${index+1}.json`),JSON.stringify({brixcanvas:1,section})));
 console.log('Prepared four native Brix clipboard payloads for the complete homepage.');
}
